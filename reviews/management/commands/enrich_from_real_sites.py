import concurrent.futures
import html
import json
import math
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from reviews.management.commands.import_all_birmingham_pubs import CURATED_BIRMINGHAM_PUBS
from reviews.models import Category, PubReview


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
WIKI_USER_AGENT = (
    "SecondCityPintBirminghamPubGuide/1.0 "
    "(https://github.com/Team-2-pubreviews; Python-urllib)"
)

NON_PUB_NAMES = [
    "Slimming World Franchise",
    "Masshouse Convenience Store",
    "The Bannatyne Spa",
    "Bannatyne's Health Club",
    "David Lloyd Leisure Birmingham",
    "Flex Fitness Birmingham Ltd",
    "Exousia Community Church",
    "Bofa Inspire",
    "St Gerards Church Centre",
    "British Muslim Association",
    "Yardley Community Services",
    "Staynewhall Square Ltd",
    "Sun Valley Amusements",
    "Performances Birmingham Ltd",
    "BIRMINGHAM REP ENTERPRISES LIMITED",
    "The Old Rep Theatre",
    "Hopwood Village Hall",
    "Broadway Dance Centre",
    "Master HUNG",
    "Avenue Food",
    "Food at the Hare",
    "The Duck Pond Cafe",
    "Xover Spaces",
    "Rear Of",
    "Barnt Green Waters",
    "Spearmint Rhino",
]

DUPLICATE_FSA_NAMES = [
    "Hennesseys Bar",
    "Clearys Public House",
    "The Green  Man",
    "The Bournbrook Inn Public House",
    "Country Girl",
    "Bristol Pear",
    "The Bell",
    "The Village",
    "The Weoley Castle Inn",
    "Moseley Arms Public House",
    "The Great Stone",
    "Witton Arms",
    "Kingfisher",
    "Royal Oak",
    "Shakespeare Inn",
    "The Shakespeare",
    "Old Contemptibles",
    "Craven Arms",
    "Head of Steam",
    "Hare & Hounds",
    "Hare And Hounds P H",
    "White Swan",
    "Tap and Spile",
    "Jewellers Arms",
    "The Prince of Wales",
    "Malt House",
    "Stirchley United Working Men Club",
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
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_name(name):
    n = re.sub(r"\s*\(.*?\)", "", name.lower())
    n = n.replace("&", " and ").replace("'", "")
    n = re.sub(r"\b(the|public house|p\s*h|pub|ltd|limited|birmingham)\b", " ", n)
    n = re.sub(r"[^a-z0-9\s]", " ", n)
    return re.sub(r"\s+", " ", n).strip()


def fetch_osm_birmingham_venues():
    """
    Fast OpenStreetMap Overpass GET query for Birmingham pub & bar nodes and ways.
    """
    queries = [
        '[out:json][timeout:25];(node["amenity"="pub"](52.38,-2.03,52.58,-1.75);node["amenity"="bar"](52.38,-2.03,52.58,-1.75);way["amenity"="pub"](52.38,-2.03,52.58,-1.75);way["amenity"="bar"](52.38,-2.03,52.58,-1.75););out center tags;',
        '[out:json][timeout:25];node["amenity"="pub"](52.38,-2.03,52.58,-1.75);out;',
    ]
    endpoints = [
        "https://overpass.private.coffee/api/interpreter",
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
    ]
    for q in queries:
        for ep in endpoints:
            try:
                url = f"{ep}?data={urllib.parse.quote(q)}"
                req = urllib.request.Request(
                    url, headers={"User-Agent": WIKI_USER_AGENT}
                )
                with urllib.request.urlopen(req, timeout=25) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                    elements = payload.get("elements", [])
                    if elements:
                        return elements
            except Exception:
                continue
    return []


def fetch_website_meta_description(url):
    """
    Fetch the official website of a pub/bar and extract its own meta description
    or og:description so we use how the venue describes itself on its own site.
    """
    if not url or not url.startswith(("http://", "https://")):
        return None
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.9",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
            raw = resp.read(65536).decode("utf-8", errors="ignore")
    except Exception:
        return None

    patterns = [
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']{25,400})["\']',
        r'<meta[^>]+content=["\']([^"\']{25,400})["\'][^>]+name=["\']description["\']',
        r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']{25,400})["\']',
        r'<meta[^>]+content=["\']([^"\']{25,400})["\'][^>]+property=["\']og:description["\']',
    ]
    for pat in patterns:
        m = re.search(pat, raw, flags=re.IGNORECASE)
        if m:
            desc = strip_html(m.group(1))
            bad_phrases = (
                "cookies",
                "javascript is required",
                "domain for sale",
                "just a moment",
                "access denied",
                "wordpress",
                "welcome to our website",
                "sign in",
                "log in",
            )
            if len(desc) >= 30 and not any(bp in desc.lower() for bp in bad_phrases):
                return desc
    return None


def fetch_web_search_description(pub):
    """
    Search Bing RSS for the pub's official website or pub-guide description
    (e.g. from the pub's own site, CAMRA WhatPub, DesignMyNight, etc.).
    Returns (snippet, official_url) or (None, None).
    """
    clean_name = re.sub(r"\s*\(.*?\)", "", pub.pub_name).strip()
    area_word = pub.get_brum_area_display().split("&")[0].split(",")[0].strip()
    q = f'"{clean_name}" {pub.postcode or area_word} Birmingham pub OR bar OR club'
    params = urllib.parse.urlencode({"q": q, "format": "rss"})
    url = f"https://www.bing.com/search?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            xml_bytes = resp.read()
        root = ET.fromstring(xml_bytes)
    except Exception:
        return None, None

    norm_tokens = [
        w
        for w in normalize_name(clean_name).split()
        if len(w) >= 3
    ]
    if not norm_tokens:
        return None, None

    best_snippet = None
    best_link = None

    for item in root.findall(".//item")[:5]:
        title = strip_html(item.findtext("title") or "")
        desc = strip_html(item.findtext("description") or "")
        link = (item.findtext("link") or "").strip()
        combined = f"{title} {desc}".lower()

        # Verify the search result is actually about this Birmingham venue
        if not all(tok in combined for tok in norm_tokens[:2]):
            continue
        if (
            "birmingham" not in combined
            and area_word.lower() not in combined
            and (not pub.postcode or pub.postcode.split()[0].lower() not in combined)
        ):
            continue

        # Skip generic directory index pages or food hygiene score tables
        if any(
            skip in combined
            for skip in (
                "food hygiene rating",
                "scores on the doors",
                "check company",
                "companies house",
                "find open hours",
                "endole",
                "192.com",
            )
        ):
            continue

        if len(desc) >= 40:
            # Clean trailing date or breadcrumb junk
            clean_desc = re.sub(r"^[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}\s*[·\-—]\s*", "", desc).strip()
            if len(clean_desc) >= 40:
                best_snippet = clean_desc
                best_link = link
                break

    return best_snippet, best_link


def classify_true_category(pub, osm_tags, ext_text, categories):
    """
    Accurately classify every Birmingham venue based on its name, OSM tags,
    and external website/guide description.
    """
    name_l = pub.pub_name.lower()
    combined = " ".join(
        filter(
            None,
            [
                name_l,
                (ext_text or "").lower(),
                (osm_tags.get("description") or "").lower(),
                (osm_tags.get("cuisine") or "").lower(),
                (osm_tags.get("amenity") or "").lower(),
            ],
        )
    )

    # 1. Sports Bars, Pool/Games Bars & Social / Members / Sports Clubs
    if any(
        w in name_l
        for w in (
            "social club",
            "working men",
            "conservative club",
            "liberal club",
            "all services club",
            "legion",
            "sports club",
            "sports & social",
            "sports and social",
            "sports bar",
            "sport and pool",
            "rugby",
            "cricket",
            "football club",
            "fc",
            "sailing club",
            "hard courts",
            "squash",
            "golf club",
            "bowls club",
            "bowling club",
            "athletic",
            "supporters club",
            "masonic",
            "irish centre",
            "corks",
            "dingle social",
            "heartlands club",
            "quarry club",
            "harborne club",
            "crown club",
            "banbury club",
            "minworth club",
            "sutton coldfield club",
            "vaughans members",
            "grange members",
            "hamstead social",
            "home guard club",
            "lourdes social",
            "pst community",
            "rise club",
            "royal 1 club",
            "wythall community club",
            "rubery memorial club",
            "castle bromwich mens club",
            "st thomas' association",
            "shenley lane community",
            "railway club",
            "lin's bar",
            "ex-servicemen",
            "ex servicemen",
            "e 57 club",
            "ivy leaf",
            "pavillion",
            "pavilions club",
            "royal air force association",
            "avenue club",
            "crown at kingstanding",
            "tennis court",
            "holte pub",
            "roxy ball room",
            "roxy lanes",
            "walkabout",
            "box",
            "toca social",
            "flight club",
            "boom battle bar",
            "clays birmingham",
            "bowlplex",
            "shooters",
            "hennessey",
            "norton's",
            "tally ho",
        )
    ) or osm_tags.get("amenity") == "social_club":
        return categories["Sports Bar & Social Club"]

    # 2. Live Music & Indie Venues
    if any(
        w in name_l
        for w in (
            "hare & hounds",
            "hare and hounds",
            "jam house",
            "actress & bishop",
            "actress and bishop",
            "scruffy murphy",
            "flapper",
            "dead wax",
            "night owl",
            "castle & falcon",
            "castle and falcon",
            "subside",
            "sunflower lounge",
            "spotted dog",
            "fiddle & bone",
            "wagon & horses",
            "barfly",
            "tunnel club",
            "juke",
            "dark horse",
        )
    ) or osm_tags.get("live_music") == "yes":
        return categories["Live Music & Indie Venue"]

    # 3. Craft Beer Bars, Microbreweries & Taprooms
    if (
        any(
            w in name_l
            for w in (
                "brew",
                "taproom",
                "tap ",
                " tap",
                "ale hub",
                "craft ",
                "head of steam",
                "post office vaults",
                "tilt",
                "wolf",
                "1000 trades",
                "purecraft",
                "colmore",
                "cork & cage",
                "wildcat",
                "sommar",
                "glasshouse",
                "attic",
                "burning soul",
                "dig brew",
                "birmingham brewing",
                "two towers",
                "gunmakers",
                "halton turner",
                "indian brewery",
                "hop & scotch",
                "kilder",
                "autobrew",
                "sobremesa",
                "cherry reds",
                "wellington",
                "hop garden",
                "barrel store",
                "whiskey club",
                "boldmere oak",
            )
        )
        or osm_tags.get("microbrewery") == "yes"
        or "craft beer" in combined
        or "taproom" in combined
        or "microbrewery" in combined
    ):
        return categories["Craft Beer Bar & Taproom"]

    # 4. Cocktail, Wine, Late-Night & Lounge Bars
    if (
        any(
            w in name_l
            for w in (
                "cocktail",
                "theatrix",
                "be at one",
                "all bar one",
                "slug & lettuce",
                "slug and lettuce",
                "pitcher & piano",
                "pitcher and piano",
                "lost & found",
                "lost and found",
                "alchemist",
                "botanist",
                "dirty martini",
                "tonight, josephine",
                "tonight josephine",
                "barbara",
                "bier haus",
                "biergarten",
                "zumhof",
                "popworld",
                "reflex",
                "players",
                "scarlets",
                "missing",
                "eden bar",
                "nightingale",
                "village inn",
                "equator",
                "fox and chance",
                "40 st paul",
                "passing fancies",
                "ikigai",
                "couch",
                "pineapple club",
                "lounge",
                "bar 90",
                "bar one",
                "grace + james",
                "blue piano",
                "simple things",
                "son caney",
                "lab 11",
                "gatecrasher",
                "chic birmingham",
                "bonnie rogues",
                "tropicana",
                "rosie's",
                "henman and cooper",
                "albert's schloss",
                "connollys wine",
                "glamorous show bar",
                "the o bar",
                "sugar suite",
                "rumrum",
                "le bar jester",
                "club maragh",
                "cuban embassy",
                "cloak & dagger",
                "talk bar",
                "sophy volt",
                "sobar",
                "plonk",
                "isla",
                "deadbeat",
                "club sensations",
                "circo bar",
                "la sante",
                "simpsons gin bar",
                "distillery sutton",
                "schooners",
            )
        )
        or osm_tags.get("amenity") in ("bar", "nightclub")
        or "cocktail bar" in combined
        or "nightclub" in combined
        or "wine bar" in combined
        or "gin bar" in combined
    ):
        return categories["Cocktail, Late-Night & Lounge Bar"]

    # 5. Gastropubs, Bar & Grills, Desi Pubs, Carveries & Food-Led Pubs
    if (
        any(
            w in name_l
            for w in (
                "kitchen",
                "gastropub",
                "carvery",
                "toby ",
                "harvester",
                "brewers fayre",
                "beefeater",
                "hungry horse",
                "sizzling",
                "miller & carter",
                "vintage inn",
                "ember inn",
                "wetherspoon",
                "square peg",
                "briar rose",
                "dragon inn",
                "soloman cutler",
                "figure of eight",
                "elizabeth of york",
                "pump house",
                "charlie hall",
                "spread eagle",
                "black horse",
                "soho tavern",
                "hen and chicken",
                "hen & chicken",
                "covered wagon",
                "red lion",
                "roebuck",
                "grove pub",
                "grove bar",
                "copper fox",
                "plough",
                "physician",
                "high field",
                "edgbaston",
                "canal house",
                "button factory",
                "rectory",
                "pig & tail",
                "cock & hoop",
                "one trick pony",
                "fletchers",
                "harborne stores",
                "paperache",
                "o'neills",
                "kennedy's",
                "sly old fox",
                "babylon grill",
                "alfred works",
                "barrell bar & grill",
                "serious steaks",
                "rahya",
                "turtle bay",
                "peg & grill",
                "herberts yard",
                "soak bar",
                "shack",
                "arthur robertson",
                "r & r bar",
                "ba-ha vegan",
                "mare pool",
                "old school house",
                "newhall street tavern",
                "goose selly oak",
                "bristol pear",
                "country girl",
                "london and north western",
                "bishop vesey",
                "bottle of sack",
            )
        )
        or any(
            c in (osm_tags.get("cuisine") or "").lower()
            for c in ("indian", "curry", "grill", "steak", "carvery", "gastropub", "pizza", "tapas")
        )
        or any(
            kw in combined
            for kw in ("gastropub", "carvery", "desi pub", "indian grill", "mixed grill", "bar & grill", "bar and grill", "bar & kitchen")
        )
    ):
        return categories["Gastropub, Bar & Kitchen"]

    # 6. Traditional Pubs & Historic Ale Houses
    if (
        any(
            w in name_l
            for w in (
                "craven arms",
                "old crown",
                "old joint stock",
                "old contemptibles",
                "bartons arms",
                "barton arms",
                "white swan",
                "anchor",
                "jewellers arms",
                "lord clifden",
                "rose villa",
                "queens arms",
                "british oak",
                "fighting cocks",
                "prince of wales",
                "bull's head",
                "bulls head",
                "big bulls head",
                "brasshouse",
                "malt house",
                "tap & spile",
                "tap and spile",
                "shakespeare",
                "trocadero",
                "victoria",
                "bacchus",
                "patrick kavanagh",
                "bell harborne",
                "green man",
                "white horse",
                "king's arms",
                "kings arms",
                "jug of ale",
                "station",
                "bournbrook",
                "selly park tavern",
                "calthorpe arms",
                "sacks of potatoes",
                "sir charles napier",
                "lamp tavern",
                "old moseley arms",
                "moseley arms",
                "fountain",
                "old windmill",
            )
        )
        or osm_tags.get("real_ale") == "yes"
        or osm_tags.get("camra") == "yes"
        or "camra" in combined
        or "real ale" in combined
        or "cask ale" in combined
        or "grade ii" in combined
    ):
        return categories["Traditional Pub & Ale House"]

    return categories["Neighbourhood Pub & Local"]


def build_pub_description(pub, cat, osm_tags, site_desc, web_snippet, web_link, curated_map):
    area_display = pub.get_brum_area_display()
    cat_name = cat.name
    loc_str = ", ".join(p for p in [pub.address, pub.postcode] if p) or area_display

    curated = curated_map.get(pub.pub_name.lower().strip())
    osm_desc = (osm_tags.get("description") or "").strip()
    website = osm_tags.get("website") or osm_tags.get("contact:website") or web_link or ""

    # Priority order for card description:
    # 1. Curated Birmingham pub description (hand-verified for the 105 flagship pubs)
    # 2. Official website meta description (`site_desc`)
    # 3. Web search snippet from the pub's own site / WhatPub / DesignMyNight (`web_snippet`)
    # 4. OpenStreetMap `description` tag
    # 5. Accurate venue summary based on its true style and Birmingham address
    if curated:
        title = curated[0]
        excerpt = curated[1]
        if site_desc and site_desc.lower() not in excerpt.lower():
            extra_source = site_desc
        elif web_snippet and web_snippet.lower() not in excerpt.lower():
            extra_source = web_snippet
        else:
            extra_source = None
    elif site_desc:
        title = f"{pub.pub_name} — {cat_name} in {area_display}"
        excerpt = site_desc
        extra_source = web_snippet if (web_snippet and web_snippet != site_desc) else None
    elif web_snippet:
        title = f"{pub.pub_name} — {cat_name} in {area_display}"
        excerpt = web_snippet
        extra_source = None
    elif osm_desc and len(osm_desc) > 25:
        title = f"{pub.pub_name} — {cat_name} in {area_display}"
        excerpt = f"{osm_desc.rstrip('.')} — located at {loc_str} in {area_display}."
        extra_source = None
    else:
        title = f"{pub.pub_name} — {cat_name} in {area_display}"
        extra_source = None
        if cat_name == "Sports Bar & Social Club":
            excerpt = (
                f"{pub.pub_name} is a {area_display} social club and sports venue at {loc_str}, "
                f"welcoming members and guests for matchdays, social events, and draught pints."
            )
        elif cat_name == "Cocktail, Late-Night & Lounge Bar":
            excerpt = (
                f"{pub.pub_name} is a bar and lounge at {loc_str} in {area_display}, "
                f"serving cocktails, spirits, draught beers, and late-night hospitality."
            )
        elif cat_name == "Craft Beer Bar & Taproom":
            excerpt = (
                f"{pub.pub_name} is an independent craft beer bar and taproom at {loc_str} in {area_display}, "
                f"pouring rotating keg and cask lines."
            )
        elif cat_name == "Live Music & Indie Venue":
            excerpt = (
                f"{pub.pub_name} is a {area_display} live music venue and bar at {loc_str}, "
                f"known for gigs, DJ nights, and a lively crowd."
            )
        elif cat_name == "Gastropub, Bar & Kitchen":
            excerpt = (
                f"{pub.pub_name} is a popular bar and kitchen at {loc_str} in {area_display}, "
                f"serving freshly prepared food, grills, and draught pints."
            )
        elif cat_name == "Traditional Pub & Ale House":
            excerpt = (
                f"{pub.pub_name} is an established {area_display} pub and ale house at {loc_str}, "
                f"known for well-kept draught pints and classic pub character."
            )
        else:
            excerpt = (
                f"{pub.pub_name} is a local pub at {loc_str} in {area_display}, "
                f"serving draught beers, spirits, and neighbourhood hospitality."
            )

    if len(excerpt) > 218:
        excerpt = excerpt[:215] + "..."

    paragraphs = [
        f"{pub.pub_name} ({cat_name}) is situated at {loc_str} in the {area_display} district of Birmingham.",
        excerpt,
    ]
    if extra_source:
        paragraphs.append(extra_source)
    if osm_desc and osm_desc not in excerpt:
        paragraphs.append(f"OpenStreetMap Note: {osm_desc}")
    if website:
        paragraphs.append(f"Website / Listing: {website}")
    paragraphs.append(
        f"Visited {pub.pub_name} recently? Click 'Review This Pub' to share your rating "
        f"for pint quality, atmosphere, and value."
    )

    content = "\n\n".join(paragraphs)
    return title[:195], excerpt[:218], content


class Command(BaseCommand):
    help = "Cleans non-pubs/duplicates and enriches pubs from OSM, official websites, and web search."

    def handle(self, *args, **options):
        # 1. Remove non-pub businesses and duplicate FSA rows
        del_non, _ = PubReview.objects.filter(pub_name__in=NON_PUB_NAMES).delete()
        del_dup, _ = PubReview.objects.filter(pub_name__in=DUPLICATE_FSA_NAMES).delete()
        self.stdout.write(
            f"Cleaned {del_non} non-pub businesses and {del_dup} duplicate FSA entries."
        )

        # 2. Ensure all 7 accurate categories exist
        category_specs = [
            ("Traditional Pub & Ale House", "traditional-pub-ale-house"),
            ("Neighbourhood Pub & Local", "neighbourhood-pub-local"),
            ("Craft Beer Bar & Taproom", "craft-taproom"),
            ("Gastropub, Bar & Kitchen", "gastropub-bar-kitchen"),
            ("Cocktail, Late-Night & Lounge Bar", "cocktail-late-night-bar"),
            ("Sports Bar & Social Club", "sports-social-club"),
            ("Live Music & Indie Venue", "live-music-venue"),
        ]
        categories = {}
        for name, slug in category_specs:
            cat_obj, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
            if cat_obj.name != name:
                cat_obj.name = name
                cat_obj.save()
            categories[name] = cat_obj

        # 3. Fetch OpenStreetMap tags
        self.stdout.write("Fetching OpenStreetMap Birmingham pub/bar tags...")
        osm_elements = fetch_osm_birmingham_venues()
        self.stdout.write(f"  Fetched {len(osm_elements)} OpenStreetMap records.")

        osm_by_name = {}
        for el in osm_elements:
            tags = el.get("tags") or {}
            name = tags.get("name", "").strip()
            lat = el.get("lat") or (el.get("center") or {}).get("lat")
            lon = el.get("lon") or (el.get("center") or {}).get("lon")
            if name:
                norm = normalize_name(name)
                if norm:
                    osm_by_name.setdefault(norm, []).append((lat, lon, tags))

        curated_map = {}
        for item in CURATED_BIRMINGHAM_PUBS:
            curated_map[item[0].lower().strip()] = (str(item[-2]), str(item[-1]))

        pubs = list(PubReview.objects.select_related("category").all())
        total = len(pubs)

        # 4. Batch-fetch Wikimedia/Geograph descriptions for all pubs with verified Wikimedia photos (4 HTTP requests total)
        self.stdout.write("Batch-fetching Wikimedia/Geograph descriptions for verified pub photos...")
        wiki_file_to_pubs = {}
        for p in pubs:
            if "upload.wikimedia.org/wikipedia/commons/" in p.featured_image:
                fname = urllib.parse.unquote(p.featured_image.split("/")[-1]).strip()
                if fname:
                    wiki_file_to_pubs.setdefault(f"File:{fname}", []).append(p)

        wiki_captions_by_pk = {}
        file_titles = list(wiki_file_to_pubs.keys())
        for i in range(0, len(file_titles), 40):
            batch_titles = file_titles[i : i + 40]
            params = urllib.parse.urlencode(
                {
                    "action": "query",
                    "titles": "|".join(batch_titles),
                    "prop": "imageinfo",
                    "iiprop": "extmetadata",
                    "format": "json",
                }
            )
            url = f"https://commons.wikimedia.org/w/api.php?{params}"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": WIKI_USER_AGENT})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                pages = (data.get("query") or {}).get("pages") or {}
                for page in pages.values():
                    t = page.get("title", "")
                    iinfo = (page.get("imageinfo") or [{}])[0]
                    ext = iinfo.get("extmetadata") or {}
                    raw_desc = (ext.get("ImageDescription") or {}).get("value", "")
                    clean_desc = strip_html(raw_desc)
                    clean_desc = re.sub(r"\(C\).*$", "", clean_desc).strip()
                    if len(clean_desc) >= 25:
                        # Match back to pub(s)
                        for k, pub_list in wiki_file_to_pubs.items():
                            if k.replace("_", " ").lower() == t.replace("_", " ").lower():
                                for pub_obj in pub_list:
                                    wiki_captions_by_pk[pub_obj.pk] = clean_desc
            except Exception:
                continue

        self.stdout.write(
            f"  Fetched {len(wiki_captions_by_pk)} Wikimedia/Geograph descriptions. Checking official pub websites..."
        )

        def match_osm(pub):
            norm = normalize_name(pub.pub_name)
            for lat, lon, tags in osm_by_name.get(norm, []):
                if pub.latitude and pub.longitude and lat and lon:
                    if haversine_miles(pub.latitude, pub.longitude, lat, lon) <= 0.5:
                        return tags
                else:
                    return tags
            return {}

        def process_pub(pub):
            osm_tags = match_osm(pub)
            website = osm_tags.get("website") or osm_tags.get("contact:website")
            site_desc = fetch_website_meta_description(website) if website else None
            wiki_desc = wiki_captions_by_pk.get(pub.pk)
            return pub, osm_tags, site_desc, wiki_desc, website

        osm_count = 0
        web_count = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(process_pub, p) for p in pubs]
            for idx, future in enumerate(concurrent.futures.as_completed(futures), 1):
                pub, osm_tags, site_desc, wiki_desc, website = future.result()
                if osm_tags:
                    osm_count += 1
                if site_desc or wiki_desc:
                    web_count += 1

                ext_text = " ".join(filter(None, [site_desc, wiki_desc]))
                cat = classify_true_category(pub, osm_tags, ext_text, categories)
                pub.category = cat

                raw_title, excerpt, content = build_pub_description(
                    pub, cat, osm_tags, site_desc, wiki_desc, website, curated_map
                )
                pub._new_raw_title = raw_title
                pub.excerpt = excerpt
                pub.content = content

                if idx % 100 == 0 or idx == total:
                    self.stdout.write(
                        f"  Processed {idx}/{total} pubs (OSM matched: {osm_count}, Web/Site descriptions: {web_count})..."
                    )

        # Save unique titles and descriptions
        for pub in pubs:
            pub.title = f"__tmp_{pub.pk}__"
        PubReview.objects.bulk_update(pubs, ["title"], batch_size=200)

        seen_titles = set()
        for pub in pubs:
            base = pub._new_raw_title[:180].strip()
            cand = base
            if cand.lower() in seen_titles:
                suffix = pub.postcode or pub.address.split(",")[0].strip() or str(pub.pk)
                cand = f"{base[:160]} ({suffix})"
                if cand.lower() in seen_titles:
                    cand = f"{base[:155]} ({suffix} #{pub.pk})"
            seen_titles.add(cand.lower())
            pub.title = cand

        PubReview.objects.bulk_update(
            pubs, ["title", "category", "excerpt", "content"], batch_size=100
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! {total} genuine Birmingham pubs & bars updated ({osm_count} OSM matches, {web_count} official site/web descriptions)."
            )
        )
