from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reviews.models import Category, PubReview, Comment


class Command(BaseCommand):
    help = "Seeds the database with authentic Birmingham pub reviews, categories, users, and comments."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Pouring fresh pints for The Second City Pint..."))

        # 1. Users
        users_data = [
            ("brummie_pete", "pete@secondcitypint.co.uk"),
            ("jq_hannah", "hannah@secondcitypint.co.uk"),
            ("digbeth_dan", "dan@secondcitypint.co.uk"),
            ("harborne_helen", "helen@secondcitypint.co.uk"),
        ]
        users = {}
        for username, email in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email},
            )
            if created:
                user.set_password("BrumPint2025!")
                user.save()
            users[username] = user

        # 2. Categories
        categories_data = [
            ("Traditional Victorian Boozer", "Ornate tilework, etched glass, mahogany bars, and proper hand-pulled cask."),
            ("Craft Taproom", "Independent keg lines, hazy IPAs, sour beers, and industrial Brum heritage."),
            ("Historic Coaching Inn", "Centuries-old timber frames, courtyard gardens, and rich Second City folklore."),
            ("Community Local", "Friendly neighbourhood gem with cheese & onion cobs, darts, and loyal regulars."),
            ("Gastropub & Craft Bar", "Curated beer list paired with elevated kitchen plates."),
        ]
        categories = {}
        for name, desc in categories_data:
            cat, _ = Category.objects.update_or_create(
                name=name,
                defaults={"description": desc},
            )
            categories[name] = cat

        # 3. Pub Reviews
        reviews_data = [
            {
                "title": "Dazzling Tiles, Blazing Fires & Unbeatable Bathams Near Upper Dean Street",
                "pub_name": "The Craven Arms",
                "category": categories["Traditional Victorian Boozer"],
                "brum_area": PubReview.BrumArea.CITY_CENTRE,
                "author": users["brummie_pete"],
                "price_point": PubReview.PricePoint.STANDARD,
                "has_beer_garden": True,
                "is_dog_friendly": True,
                "shows_live_sports": False,
                "serves_cask_ale": True,
                "serves_cobs_or_food": True,
                "pint_quality_rating": 5,
                "atmosphere_rating": 5,
                "value_rating": 5,
                "featured_image": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "A tiled Black Country brewery jewel tucked just behind the Bullring serving the best pint of Holden's and Bathams in central Brum.",
                "content": (
                    "Tucked away on Upper Dean Street just a stone's throw from the Bullring markets, The Craven Arms "
                    "is an absolute masterclass in what a traditional Birmingham boozer should be. The exterior ceramics "
                    "and stained glass windows immediately let you know you're stepping into somewhere special.\n\n"
                    "At the bar, the hand-pulls gleam. The pint of Holden's Golden Glow was cellar-cool, crystal clear, "
                    "and kept with textbook care. Pair it with one of their legendary crusty cheese and onion cobs (with "
                    "a generous slab of butter) and grab a leather banquette by the fireplace. Zero piped music, proper "
                    "conversation, and a cosy enclosed courtyard out back."
                ),
                "comments": [
                    (users["jq_hannah"], "Their crusty ham and mustard cobs have saved my Saturday shopping trips more times than I can count!"),
                    (users["digbeth_dan"], "Best kept cask line in the city centre by a country mile."),
                ],
            },
            {
                "title": "650 Years of Brummie History and a Sun-Trap Courtyard in Digbeth",
                "pub_name": "The Old Crown",
                "category": categories["Historic Coaching Inn"],
                "brum_area": PubReview.BrumArea.DIGBETH,
                "author": users["digbeth_dan"],
                "price_point": PubReview.PricePoint.STANDARD,
                "has_beer_garden": True,
                "is_dog_friendly": True,
                "shows_live_sports": True,
                "serves_cask_ale": True,
                "serves_cobs_or_food": True,
                "pint_quality_rating": 4,
                "atmosphere_rating": 5,
                "value_rating": 4,
                "featured_image": "https://images.unsplash.com/photo-1572116469696-31de0f17cc34?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "Birmingham's oldest secular building dating back to 1368 — unbeatable beer garden energy and hearty pub grub in the heart of Digbeth.",
                "content": (
                    "Standing proud on High Street Deritend since 1368, The Old Crown has survived the English Civil War, "
                    "industrialisation, and centuries of Digbeth nightlife. The black-and-white timber framing still "
                    "stops you in your tracks as you walk down from town.\n\n"
                    "Inside you'll find low beams and snug corners, while out back sits one of Birmingham's liveliest "
                    "courtyard beer gardens. Whether you're dropping in for a pre-match pint, a Sunday roast, or a sunny "
                    "afternoon session with the dog, it delivers warmth and unmistakable Second City pride."
                ),
                "comments": [
                    (users["harborne_helen"], "That beer garden on a Friday evening in May is unbeatable."),
                ],
            },
            {
                "title": "Stirchley's Beer Mile Crown Jewel: Fresh Tank Pale & Warehouse Vibes",
                "pub_name": "Attic Brew Co. Taproom",
                "category": categories["Craft Taproom"],
                "brum_area": PubReview.BrumArea.STIRCHLEY,
                "author": users["jq_hannah"],
                "price_point": PubReview.PricePoint.PREMIUM,
                "has_beer_garden": True,
                "is_dog_friendly": True,
                "shows_live_sports": False,
                "serves_cask_ale": False,
                "serves_cobs_or_food": True,
                "pint_quality_rating": 5,
                "atmosphere_rating": 5,
                "value_rating": 4,
                "featured_image": "https://images.unsplash.com/photo-1559526324-593bc073d938?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "Drinking Intuition Pale Ale metres from the fermentation tanks in Stirchley's thriving independent beer quarter.",
                "content": (
                    "If you want to understand why Stirchley was named one of the best places to live in the UK, start "
                    "on Mary Vale Road at Attic Brew Co. Sitting right alongside the stainless steel brewing kit, the "
                    "taproom pours the freshest pint of Intuition Pale Ale you will ever taste.\n\n"
                    "There are rotating street food traders parked outside every weekend, plenty of bench seating, "
                    "friendly staff who genuinely love talking hops, and arguably the highest dog-to-human ratio in "
                    "South Birmingham."
                ),
                "comments": [
                    (users["brummie_pete"], "Even as a die-hard cask drinker, a fresh pint of Intuition straight from the taproom converts me every time."),
                    (users["harborne_helen"], "Love combining a stop here with Glasshouse down the canal towpath!"),
                ],
            },
            {
                "title": "A Cathedral of Snob Screens, Minton Tiles and Thai Street Food",
                "pub_name": "The Bartons Arms",
                "category": categories["Traditional Victorian Boozer"],
                "brum_area": PubReview.BrumArea.ASTON,
                "author": users["brummie_pete"],
                "price_point": PubReview.PricePoint.STANDARD,
                "has_beer_garden": False,
                "is_dog_friendly": False,
                "shows_live_sports": True,
                "serves_cask_ale": True,
                "serves_cobs_or_food": True,
                "pint_quality_rating": 5,
                "atmosphere_rating": 5,
                "value_rating": 5,
                "featured_image": "https://images.unsplash.com/photo-1543007630-9710e4a00a20?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "Grade II* listed Victorian palace in Aston where Laurel & Hardy once drank — complete with rare snob screens and Oakham ales.",
                "content": (
                    "The Bartons Arms is architectural theatre. Built in 1901 by James & Lister Lea, every inch of the "
                    "walls and staircase is wrapped in breathtaking Craven Dunnill tiles, cut glass mirrors, and original "
                    "mahogany snob screens that once allowed middle-class drinkers to see without being seen.\n\n"
                    "The Oakham Citra and JHB on hand-pull are always in tip-top condition, and the fragrant Thai menu "
                    "served in the grand back lounge makes the trip up to Aston essential for any pub lover."
                ),
                "comments": [
                    (users["digbeth_dan"], "Those tiled staircases belong in a museum, yet you can stand there with a £4.50 pint of Citra!"),
                ],
            },
            {
                "title": "Jewellery Quarter Heritage Meets Proper Cask and a Secret Upstairs Terrace",
                "pub_name": "The Lord Clifden",
                "category": categories["Community Local"],
                "brum_area": PubReview.BrumArea.JEWELLERY_QUARTER,
                "author": users["jq_hannah"],
                "price_point": PubReview.PricePoint.STANDARD,
                "has_beer_garden": True,
                "is_dog_friendly": True,
                "shows_live_sports": True,
                "serves_cask_ale": True,
                "serves_cobs_or_food": True,
                "pint_quality_rating": 4,
                "atmosphere_rating": 4,
                "value_rating": 4,
                "featured_image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "An anchor of Great Hampton Street history with a bustling garden, live football screens, and solid ales.",
                "content": (
                    "A classic Jewellery Quarter red-brick corner pub that bridges the gap between traditional after-work "
                    "boozer and weekend hangout. Great selection on draught, reliable match-day atmosphere when Villa or "
                    "Blues are on the box, and a spacious outdoor area at the rear."
                ),
                "comments": [],
            },
            {
                "title": "Harborne's Cosy Weatherboarded Gem for Sunday Roasts and Fireside Ales",
                "pub_name": "The Plough",
                "category": categories["Gastropub & Craft Bar"],
                "brum_area": PubReview.BrumArea.HARBORNE,
                "author": users["harborne_helen"],
                "price_point": PubReview.PricePoint.PREMIUM,
                "has_beer_garden": True,
                "is_dog_friendly": True,
                "shows_live_sports": False,
                "serves_cask_ale": True,
                "serves_cobs_or_food": True,
                "pint_quality_rating": 4,
                "atmosphere_rating": 5,
                "value_rating": 4,
                "featured_image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",
                "excerpt": "Mismatch vintage furniture, a leafy heated garden, and well-kept Purecraft & local guest ales on Harborne High Street.",
                "content": (
                    "Sitting at the top of Harborne High Street, The Plough blends village local charm with one of the "
                    "best kitchens in the suburbs. While it's famous for stone-baked pizzas and epic Sunday roasts, "
                    "don't sleep on the bar area: local Purity and guest cask lines are poured with care, and dogs get "
                    "treated like royalty."
                ),
                "comments": [
                    (users["jq_hannah"], "Hands down the best heated garden in Harborne for a crisp autumn pint."),
                ],
            },
        ]

        for item in reviews_data:
            comments_list = item.pop("comments", [])
            review, _ = PubReview.objects.update_or_create(
                title=item["title"],
                defaults=item,
            )
            # Add likes from sample users
            review.likes.add(users["brummie_pete"], users["jq_hannah"], users["digbeth_dan"])

            for commenter, body in comments_list:
                Comment.objects.get_or_create(
                    review=review,
                    author=commenter,
                    body=body,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Seeded {Category.objects.count()} categories, "
                f"{PubReview.objects.count()} Birmingham pub reviews, and "
                f"{Comment.objects.count()} comments."
            )
        )
