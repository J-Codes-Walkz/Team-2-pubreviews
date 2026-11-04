import json
from pathlib import Path
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Category, PubReview, Comment


class ReviewActivityPreservationTests(TestCase):
    def setUp(self):
        self.directory_user = User.objects.create_user(
            username="pub_directory",
            email="directory@secondcitypint.co.uk",
        )
        self.directory_user.set_unusable_password()
        self.directory_user.save()

        self.other_user = User.objects.create_user(
            username="brummie_fan",
            email="fan@example.com",
            password="StrongPassword123!",
        )
        self.reviewer = User.objects.create_user(
            username="pint_reviewer",
            email="reviewer@example.com",
            password="StrongPassword123!",
        )
        self.category = Category.objects.create(
            name="Traditional Pub & Ale House",
            slug="traditional-pub-ale-house",
        )
        self.placeholder = PubReview.objects.create(
            title="The Craven Arms — Digbeth & Deritend",
            pub_name="The Craven Arms",
            category=self.category,
            brum_area=PubReview.BrumArea.DIGBETH,
            address="75-77 Upper Dean St",
            postcode="B5 4SG",
            latitude=52.4751,
            longitude=-1.8942,
            author=self.directory_user,
            price_point=PubReview.PricePoint.STANDARD,
            pint_quality_rating=4,
            atmosphere_rating=4,
            value_rating=4,
            content="Directory listing for The Craven Arms.",
            status=PubReview.Status.PUBLISHED,
        )

    def test_posting_review_moves_comments_likes_and_bookmarks_from_placeholder(self):
        # Another user likes, bookmarks, and comments on the directory listing
        self.placeholder.likes.add(self.other_user)
        self.placeholder.bookmarks.add(self.other_user)
        comment = Comment.objects.create(
            review=self.placeholder,
            author=self.other_user,
            pint_quality_rating=5,
            atmosphere_rating=5,
            value_rating=4,
            pint_ordered="Holdens Golden Glow",
            pint_price="4.40",
            body="Proper tiled boozer with a great pint of Holdens!",
        )

        # Now self.reviewer logs in and posts a full review of the same pub
        self.client.login(username="pint_reviewer", password="StrongPassword123!")
        response = self.client.post(
            reverse("reviews:create"),
            {
                "title": "Best Pint of Bathams in Digbeth",
                "pub_name": "The Craven Arms",
                "category": self.category.pk,
                "brum_area": PubReview.BrumArea.DIGBETH,
                "address": "75-77 Upper Dean St",
                "postcode": "B5 4SG",
                "price_point": PubReview.PricePoint.STANDARD,
                "pint_quality_rating": 5,
                "atmosphere_rating": 5,
                "value_rating": 5,
                "pint_ordered": "Bathams Best Bitter",
                "pint_price": "4.50",
                "serves_cask_ale": True,
                "serves_cobs_or_food": True,
                "has_beer_garden": True,
                "is_dog_friendly": True,
                "shows_live_sports": False,
                "excerpt": "Unbeatable Victorian pub near the Bullring.",
                "content": "Superb cask keep and iconic tiled exterior.",
                "featured_image": "",
                "status": PubReview.Status.PUBLISHED,
            },
        )
        self.assertEqual(response.status_code, 302)

        # The placeholder should be gone, replaced by the new review
        self.assertFalse(PubReview.objects.filter(pk=self.placeholder.pk).exists())
        new_review = PubReview.objects.get(title="Best Pint of Bathams in Digbeth")

        # Verify comments, likes, bookmarks, and GPS coordinates were preserved on the new review
        self.assertTrue(new_review.likes.filter(pk=self.other_user.pk).exists())
        self.assertTrue(new_review.bookmarks.filter(pk=self.other_user.pk).exists())
        self.assertEqual(new_review.comments.count(), 1)
        comment.refresh_from_db()
        self.assertEqual(comment.review_id, new_review.pk)
        self.assertEqual(new_review.latitude, 52.4751)
        self.assertEqual(new_review.longitude, -1.8942)


class FixtureSecurityTests(TestCase):
    def test_fixture_contains_no_personal_accounts_or_password_hashes(self):
        fixture_path = Path(__file__).resolve().parent / "fixtures" / "birmingham_pubs.json"
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        user_entries = [obj for obj in data if obj.get("model") == "auth.user"]
        self.assertEqual(len(user_entries), 1)
        self.assertEqual(user_entries[0]["fields"]["username"], "pub_directory")
        self.assertFalse(user_entries[0]["fields"]["password"].startswith("pbkdf2_"))
