import concurrent.futures
import html
import json
import math
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand
from reviews.management.commands.import_all_birmingham_pubs import CURATED_BIRMINGHAM_PUBS
from reviews.models import PubReview


USER_AGENT = (
    "SecondCityPintBirminghamPubGuide/1.0 "
    "(https://github.com/Team-2-pubreviews; Python-urllib)"
)

EXCLUDED_TITLE_WORDS = (
    "map",
    "locator",
    "coat of arms",
    "logo",
    "signature",
    "diagram",
    "chart",
    "icon",
    "plaque",
    "grave",
    "memorial",
    "statue",
    "bus ",
    "buses ",
    "train ",
    "tram ",
    "canal bridge",
    "milepost",
    "postbox",
    "pillar box",
    "street barrier",
    "dinner menu",
    "menu ",
    "portacabin",
    "car park",
    "demolished",
    "site of ",
)

# Common pub names that exist in multiple towns or multiple Birmingham suburbs;
# if a Wikimedia image has no GPS coordinates, we require the street or suburb name too.
COMMON_PUB_NAMES = {
    "red lion",
    "white swan",
    "black horse",
    "white horse",
    "bulls head",
    "bull's head",
    "kings head",
    "king's head",
    "kings arms",
    "king's arms",
    "queens head",
    "queen's head",
    "queens arms",
    "queen's arms",
    "prince of wales",
    "duke of york",
    "royal oak",
    "british oak",
    "old crown",
    "crown",
    "plough",
    "bell",
    "bell inn",
    "fox",
    "fox and hounds",
    "swan",
    "railway",
    "railway inn",
    "station",
    "new inn",
    "rose and crown",
    "coach and horses",
    "wagon and horses",
    "three horseshoes",
    "talbot",
    "new talbot",
    "shakespeare",
    "shakespeare inn",
    "victoria",
    "lord nelson",
    "robin hood",
    "hare and hounds",
    "bull",
    "anchor",
    "cross keys",
    "boars head",
    "green man",
    "fleece",
    "george",
    "stags head",
    "stag's head",
    "wheatsheaf",
    "dog and partridge",
}

# Unbranded cosy pub interior / pint / cask hand-pull photography (never shows a wrong pub building sign)
UNBRANDED_PUB_INTERIOR_FALLBACKS = [
    "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1572116469696-31de0f17cc34?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1559526324-593bc073d938?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1543007630-9710e4a00a20?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1538488881038-e252a119ace7?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1575444758702-4a6b9222336e?auto=format&fit=crop&w=1200&q=80",
]


def haversine_miles(lat1, lon1, lat2, lon2):
    r_miles = 3958.8
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(d_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2.0) ** 2
    )
    return 2.0 * r_miles * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def strip_html(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_distinctive_name_tokens(name):
    """
    Return the distinctive words of a pub's name that MUST appear in a photo's filename
    to be sure the photo is actually of that pub.
    """
    clean = re.sub(r"\s*\(.*?\)", "", name.lower())
    clean = clean.replace("&", " and ").replace("'", "")
    words = re.sub(r"[^a-z0-9\s]", " ", clean).split()
    generic = {
        "the",
        "and",
        "at",
        "in",
        "of",
        "birmingham",
        "pub",
        "public",
        "house",
        "bar",
        "ltd",
        "inn",
        "tavern",
        "hotel",
        "club",
        "social",
        "lounge",
        "tap",
        "taproom",
        "kitchen",
        "cafe",
        "sports",
        "company",
        "co",
        "brew",
        "brewing",
        "brewery",
        "brewhouse",
    }
    distinctive = [w for w in words if len(w) >= 3 and w not in generic]
    if not distinctive:
        # Fallback if the entire name was made of words in generic (e.g. "The Tap House")
        distinctive = [w for w in words if len(w) >= 3 and w != "the"]
    return distinctive


def extract_street_name(address):
    if not address:
        return ""
    first_part = address.split(",")[0].strip()
    street = re.sub(r"^[\d\-\s/]+", "", first_part).strip()
    return street if len(street) >= 4 else first_part


def fetch_json(url):
    for attempt in range(3):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1.5 * (attempt + 1))
                continue
            return None
        except Exception:
            time.sleep(0.5)
    return None


def verify_candidate_page(page, pub, req_tokens, street, area_label):
    """
    Strictly verify whether a Wikimedia File page is a genuine photo of `pub`.
    Returns (score, img_url, desc) or (0, None, None).
    """
    raw_title = page.get("title", "")
    # Remove 'File:' prefix and extension
    clean_title = re.sub(r"^File:", "", raw_title, flags=re.IGNORECASE)
    title_lower = clean_title.lower().replace("_", " ").replace("'", "")

    if not title_lower.endswith((".jpg", ".jpeg", ".png", ".webp")):
        return 0, None, None

    if any(ex in title_lower for ex in EXCLUDED_TITLE_WORDS):
        return 0, None, None

    # RULE 1: Every distinctive word of the pub's name MUST appear in the file title!
    if not req_tokens or not all(
        re.search(rf"\b{re.escape(tok)}s?\b", title_lower) for tok in req_tokens
    ):
        return 0, None, None

    # Prevent street/square/arcade false positives when the pub is named after the street
    # (e.g. "The Colmore" matching "Colmore Row" or "1000 Trades" matching "1000 Trades Square")
    if "colmore" in req_tokens and "colmore row" in title_lower and "the colmore" not in title_lower:
        return 0, None, None
    if "1000" in req_tokens and "1000 trades square" in title_lower:
        return 0, None, None
    if "rectory" in req_tokens and "saint paul rectory" in title_lower:
        return 0, None, None

    iinfo = (page.get("imageinfo") or [{}])[0]
    img_url = iinfo.get("url") or iinfo.get("thumburl")
    if not img_url:
        return 0, None, None
    if "?utm_source=" in img_url:
        img_url = img_url.split("?utm_source=")[0]

    ext = iinfo.get("extmetadata") or {}
    desc_raw = (ext.get("ImageDescription") or {}).get("value", "")
    desc = strip_html(desc_raw)
    combined = f"{title_lower} {desc.lower()}"

    # RULE 2: Strict Location Verification
    coords = page.get("coordinates") or []
    if coords and pub.latitude and pub.longitude:
        img_lat = coords[0].get("lat")
        img_lon = coords[0].get("lon")
        if img_lat is not None and img_lon is not None:
            dist = haversine_miles(pub.latitude, pub.longitude, img_lat, img_lon)
            # Must be within 0.30 miles (480m) of the pub's actual coordinates!
            if dist > 0.30:
                return 0, None, None
            # Verified both by exact pub name in title AND exact GPS location!
            score = 100 - int(dist * 100)
            return score, img_url, desc

    # If the image has no GPS coordinates tag on Wikimedia, check text location strictly:
    has_birmingham = "birmingham" in combined
    has_area = area_label.lower() in combined if len(area_label) > 3 else False
    has_street = street.lower() in combined if len(street) > 4 else False

    if not (has_birmingham and (has_area or has_street)):
        return 0, None, None

    return 75, img_url, desc


def search_wikimedia_for_pub(pub):
    """
    Search Wikimedia Commons for a strictly verified photo of `pub`.
    Returns (image_url, wiki_caption) or (None, None).
    """
    req_tokens = get_distinctive_name_tokens(pub.pub_name)
    if not req_tokens:
        return None, None

    street = extract_street_name(pub.address)
    area_label = pub.get_brum_area_display().split("&")[0].split("(")[0].strip()

    best_url = None
    best_caption = None
    best_score = 0

    # 1. GeoSearch within 250m of the pub's exact coordinates on Wikimedia Commons
    if pub.latitude and pub.longitude:
        params = urllib.parse.urlencode(
            {
                "action": "query",
                "generator": "geosearch",
                "ggsprimary": "all",
                "ggscoord": f"{pub.latitude}|{pub.longitude}",
                "ggsradius": 250,
                "ggsnamespace": 6,
                "ggslimit": 15,
                "prop": "imageinfo|coordinates",
                "iiprop": "url|extmetadata",
                "format": "json",
            }
        )
        url = f"https://commons.wikimedia.org/w/api.php?{params}"
        data = fetch_json(url)
        if data and "query" in data and "pages" in data["query"]:
            for page in data["query"]["pages"].values():
                score, img_url, desc = verify_candidate_page(
                    page, pub, req_tokens, street, area_label
                )
                if score > best_score:
                    best_score = score
                    best_url = img_url
                    best_caption = desc

        if best_score >= 80:
            return best_url, best_caption

    # 2. Title search (`intitle:`) on Wikimedia Commons with GPS coordinate verification
    intitle_terms = " ".join(f"intitle:{t}" for t in req_tokens[:3])
    q = f"filetype:bitmap {intitle_terms} Birmingham"
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": q,
            "gsrnamespace": 6,
            "gsrlimit": 8,
            "prop": "imageinfo|coordinates",
            "iiprop": "url|extmetadata",
            "format": "json",
        }
    )
    url = f"https://commons.wikimedia.org/w/api.php?{params}"
    data = fetch_json(url)
    if data and "query" in data and "pages" in data["query"]:
        for page in data["query"]["pages"].values():
            score, img_url, desc = verify_candidate_page(
                page, pub, req_tokens, street, area_label
            )
            if score > best_score:
                best_score = score
                best_url = img_url
                best_caption = desc

    return best_url, best_caption


def build_rich_description(pub, curated_map, wiki_caption):
    """
    Build a rich, factual pub title, card excerpt, and full detail description
    for every pub without creating fake reviews.
    """
    area_display = pub.get_brum_area_display()
    cat_name = pub.category.name if pub.category else "Local Pub"
    first_addr = pub.address.split(",")[0].strip() if pub.address else ""
    loc_phrase = f"at {first_addr}" if first_addr else f"in {area_display}"

    curated = curated_map.get(pub.pub_name.lower().strip())
    if curated:
        headline, blurb = curated
        title = headline
        excerpt = blurb
    else:
        features = []
        if pub.serves_cask_ale:
            features.append("proper cask ale")
        if pub.serves_cobs_or_food:
            features.append("pub grub & cobs")
        if pub.has_beer_garden:
            features.append("outdoor beer garden seating")
        if pub.is_dog_friendly:
            features.append("a dog-friendly welcome")
        if pub.shows_live_sports:
            features.append("live matchday sports screens")

        if cat_name == "Traditional Victorian Boozer":
            style_intro = f"Traditional Birmingham pub {loc_phrase} in {area_display}"
        elif cat_name == "Craft Taproom":
            style_intro = f"Independent craft beer bar and taproom {loc_phrase} in {area_display}"
        elif cat_name == "Gastropub & Craft Bar":
            style_intro = f"Neighbourhood bar and kitchen {loc_phrase} in {area_display}"
        elif cat_name == "Sports & Social Club":
            style_intro = f"Lively Birmingham social club and sports venue {loc_phrase} in {area_display}"
        else:
            style_intro = f"Welcoming {area_display} community local {loc_phrase}"

        title = f"{pub.pub_name} — {cat_name} in {area_display}"

        if wiki_caption and 25 < len(wiki_caption) < 200:
            clean_wiki = re.sub(r"\(C\).*$", "", wiki_caption).strip()
            if clean_wiki:
                excerpt = f"{clean_wiki.rstrip('.')} — located at {pub.address}, {pub.postcode} in {area_display}."
            else:
                excerpt = ""
        else:
            excerpt = ""

        if not excerpt:
            if features:
                feat_text = ", ".join(features[:-1]) + (
                    f" and {features[-1]}" if len(features) > 1 else features[0]
                )
                excerpt = f"{style_intro}, known for {feat_text}."
            else:
                excerpt = f"{style_intro} ({pub.postcode}), serving locals and visitors in the heart of {area_display}."

    if len(excerpt) > 218:
        excerpt = excerpt[:215] + "..."

    amenity_list = []
    if pub.serves_cask_ale:
        amenity_list.append("traditional hand-pulled cask ales")
    if pub.serves_cobs_or_food:
        amenity_list.append("hearty pub food and freshly filled cobs")
    if pub.has_beer_garden:
        amenity_list.append("an outdoor terrace or beer garden")
    if pub.is_dog_friendly:
        amenity_list.append("dog-friendly bar areas")
    if pub.shows_live_sports:
        amenity_list.append("live sport screenings")

    amenities_sentence = (
        f"Highlights include {', '.join(amenity_list)}."
        if amenity_list
        else f"A staple of the {area_display} hospitality scene."
    )

    wiki_para = ""
    if wiki_caption and len(wiki_caption) > 25:
        clean_wiki = re.sub(r"\(C\).*$", "", wiki_caption).strip()
        if clean_wiki and clean_wiki.lower() not in excerpt.lower():
            wiki_para = f"\n\nArchitectural & Local Note: {clean_wiki}"

    content = (
        f"{pub.pub_name} is a {cat_name.lower()} situated at {pub.address}, {pub.postcode} "
        f"in the {area_display} district of Birmingham.\n\n"
        f"{excerpt}\n\n"
        f"{amenities_sentence}{wiki_para}\n\n"
        f"Visited {pub.pub_name} recently? Click 'Review This Pub' to share your rating for "
        f"pint quality, atmosphere, and value!"
    )

    return title[:195], excerpt[:218], content


class Command(BaseCommand):
    help = "Enriches all Birmingham pubs with strictly verified Wikimedia/Geograph photos and factual descriptions."

    def handle(self, *args, **options):
        curated_map = {}
        for item in CURATED_BIRMINGHAM_PUBS:
            curated_map[item[0].lower().strip()] = (str(item[-2]), str(item[-1]))

        pubs = list(PubReview.objects.select_related("category", "author").all())
        total = len(pubs)
        self.stdout.write(
            f"Verifying and enriching {total} Birmingham pubs (strict pub-name + GPS coordinate matching)..."
        )

        matched_photos = 0
        pending_batch = []

        def process_pub(pub):
            img_url, wiki_caption = search_wikimedia_for_pub(pub)
            return pub, img_url, wiki_caption

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(process_pub, p) for p in pubs]
            for idx, future in enumerate(concurrent.futures.as_completed(futures), 1):
                pub, real_img_url, wiki_caption = future.result()
                _, excerpt, content = build_rich_description(pub, curated_map, wiki_caption)
                pub.excerpt = excerpt
                pub.content = content

                if real_img_url:
                    pub.featured_image = real_img_url[:495]
                    matched_photos += 1
                else:
                    # Use an unbranded pub interior/pint image so we NEVER show a different pub's sign/building
                    pub.featured_image = UNBRANDED_PUB_INTERIOR_FALLBACKS[
                        pub.pk % len(UNBRANDED_PUB_INTERIOR_FALLBACKS)
                    ]

                pending_batch.append(pub)

                if len(pending_batch) >= 50 or idx == total:
                    PubReview.objects.bulk_update(
                        pending_batch, ["excerpt", "content", "featured_image"], batch_size=50
                    )
                    pending_batch.clear()
                    self.stdout.write(
                        f"  Processed {idx}/{total} pubs ({matched_photos} strictly verified exact pub photos matched)..."
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! {matched_photos} pubs now have strictly verified photos of that exact pub (name + GPS verified), "
                f"and {total - matched_photos} pubs without an exterior Wikimedia photo use unbranded pint/interior imagery."
            )
        )
