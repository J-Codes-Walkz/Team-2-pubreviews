import json
import os
import tempfile
from unittest import mock
from decimal import Decimal
from pathlib import Path
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from .forms import validate_uploaded_image_file
from .models import Category, PubReview, Comment


VALID_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


# client.login() doesn't pass a request, which django-axes needs, so tests that just
# need a logged-in user use Django's plain backend. LoginRateLimitTests covers axes.
PLAIN_LOGIN = override_settings(
    AUTHENTICATION_BACKENDS=["django.contrib.auth.backends.ModelBackend"]
)


@PLAIN_LOGIN
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
        self.assertFalse(PubReview.objects.filter(pk=self.placeholder.pk).exists())
        new_review = PubReview.objects.get(title="Best Pint of Bathams in Digbeth")

        self.assertTrue(new_review.likes.filter(pk=self.other_user.pk).exists())
        self.assertTrue(new_review.bookmarks.filter(pk=self.other_user.pk).exists())
        self.assertEqual(new_review.comments.count(), 1)
        comment.refresh_from_db()
        self.assertEqual(comment.review_id, new_review.pk)
        self.assertEqual(new_review.latitude, 52.4751)
        self.assertEqual(new_review.longitude, -1.8942)

    def test_deleting_review_preserves_pub_and_other_users_activity(self):
        review = PubReview.objects.create(
            title="Great Evening at The Wellington",
            pub_name="The Wellington",
            category=self.category,
            brum_area=PubReview.BrumArea.CITY_CENTRE,
            address="37 Bennetts Hill",
            postcode="B2 5SN",
            author=self.reviewer,
            pint_quality_rating=5,
            atmosphere_rating=5,
            value_rating=4,
            pint_ordered="Wye Valley HPA",
            pint_price="4.80",
            content="16 real ales on tap!",
            status=PubReview.Status.PUBLISHED,
        )
        review.likes.add(self.other_user)
        review.bookmarks.add(self.other_user)
        Comment.objects.create(
            review=review,
            author=self.other_user,
            pint_quality_rating=5,
            atmosphere_rating=4,
            value_rating=4,
            body="Roof terrace is class.",
        )

        self.client.login(username="pint_reviewer", password="StrongPassword123!")
        response = self.client.post(reverse("reviews:delete", kwargs={"slug": review.slug}))
        self.assertEqual(response.status_code, 302)

        # Pub listing still exists under pub_directory and keeps other user's activity
        review.refresh_from_db()
        self.assertEqual(review.author, self.directory_user)
        self.assertEqual(review.pint_ordered, "")
        self.assertIsNone(review.pint_price)
        self.assertTrue(review.likes.filter(pk=self.other_user.pk).exists())
        self.assertTrue(review.bookmarks.filter(pk=self.other_user.pk).exists())
        self.assertEqual(review.comments.count(), 1)


@PLAIN_LOGIN
class SecurityAndValidationTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="alice_brum", password="StrongPassword123!"
        )
        self.intruder = User.objects.create_user(
            username="bob_intruder", password="StrongPassword123!"
        )
        self.published_review = PubReview.objects.create(
            title="The Old Joint Stock Review",
            pub_name="The Old Joint Stock",
            brum_area=PubReview.BrumArea.CITY_CENTRE,
            author=self.author,
            pint_quality_rating=5,
            atmosphere_rating=5,
            value_rating=4,
            content="Stunning domed glass ceiling.",
            status=PubReview.Status.PUBLISHED,
        )
        self.draft_review = PubReview.objects.create(
            title="Secret Draft Review",
            pub_name="The Secret Snug",
            brum_area=PubReview.BrumArea.MOSELEY,
            author=self.author,
            pint_quality_rating=4,
            atmosphere_rating=4,
            value_rating=4,
            content="Still writing this review...",
            status=PubReview.Status.DRAFT,
        )

    def test_non_author_cannot_edit_or_delete_review(self):
        self.client.login(username="bob_intruder", password="StrongPassword123!")
        edit_res = self.client.post(
            reverse("reviews:edit", kwargs={"slug": self.published_review.slug}),
            {"title": "Hacked Title"},
        )
        self.assertEqual(edit_res.status_code, 403)
        del_res = self.client.post(
            reverse("reviews:delete", kwargs={"slug": self.published_review.slug})
        )
        self.assertEqual(del_res.status_code, 403)

    def test_unpublished_draft_cannot_be_viewed_liked_bookmarked_or_commented_by_others(self):
        self.client.login(username="bob_intruder", password="StrongPassword123!")
        detail_res = self.client.get(
            reverse("reviews:detail", kwargs={"slug": self.draft_review.slug})
        )
        self.assertEqual(detail_res.status_code, 404)

        like_res = self.client.post(
            reverse("reviews:like", kwargs={"slug": self.draft_review.slug})
        )
        self.assertEqual(like_res.status_code, 404)

        bookmark_res = self.client.post(
            reverse("reviews:bookmark", kwargs={"slug": self.draft_review.slug})
        )
        self.assertEqual(bookmark_res.status_code, 404)

        comment_res = self.client.post(
            reverse("reviews:add_comment", kwargs={"slug": self.draft_review.slug}),
            {
                "pint_quality_rating": 5,
                "atmosphere_rating": 5,
                "value_rating": 5,
                "body": "Trying to comment on a draft",
            },
        )
        self.assertEqual(comment_res.status_code, 404)

    def test_open_redirect_blocked_on_bookmark_toggle(self):
        self.client.login(username="bob_intruder", password="StrongPassword123!")
        res = self.client.post(
            reverse("reviews:bookmark", kwargs={"slug": self.published_review.slug}),
            {"next": "https://malicious.example.com/phish"},
        )
        self.assertEqual(res.status_code, 302)
        self.assertTrue(
            res["Location"].startswith(
                reverse("reviews:detail", kwargs={"slug": self.published_review.slug})
            )
        )

    def test_fake_image_file_rejected_and_real_png_accepted(self):
        self.client.login(username="alice_brum", password="StrongPassword123!")
        fake_jpg = SimpleUploadedFile(
            "not_an_image.jpg",
            b"<script>alert('xss')</script>",
            content_type="image/jpeg",
        )
        self.client.post(
            reverse("reviews:add_comment", kwargs={"slug": self.published_review.slug}),
            {
                "pint_quality_rating": 5,
                "atmosphere_rating": 5,
                "value_rating": 5,
                "body": "Uploading fake image",
                "uploaded_image": fake_jpg,
            },
        )
        self.assertEqual(Comment.objects.count(), 0)

        real_png = SimpleUploadedFile(
            "pint.png", VALID_PNG_BYTES, content_type="image/png"
        )
        original_card_image = self.published_review.image_url
        self.client.post(
            reverse("reviews:add_comment", kwargs={"slug": self.published_review.slug}),
            {
                "pint_quality_rating": 5,
                "atmosphere_rating": 5,
                "value_rating": 5,
                "pint_ordered": "Attic Intuition",
                "pint_price": "5.20",
                "body": "Real PNG photo upload!",
                "uploaded_image": real_png,
            },
        )
        self.assertEqual(Comment.objects.count(), 1)
        self.published_review.refresh_from_db()
        # Pub card image must remain the pub's own featured_image, while gallery_photos includes the upload
        self.assertEqual(self.published_review.image_url, original_card_image)
        self.assertEqual(len(self.published_review.gallery_photos), 1)

    def test_negative_or_excessive_pint_price_rejected(self):
        self.client.login(username="alice_brum", password="StrongPassword123!")
        self.client.post(
            reverse("reviews:add_comment", kwargs={"slug": self.published_review.slug}),
            {
                "pint_quality_rating": 5,
                "atmosphere_rating": 5,
                "value_rating": 5,
                "pint_price": "-10.00",
                "body": "Trying negative pint price",
            },
        )
        self.assertEqual(Comment.objects.count(), 0)

    def test_deleting_draft_really_deletes_it_and_never_publishes_it(self):
        # The live site always has the directory guide account (it's in the fixture)
        User.objects.create_user(username="pub_directory")
        self.client.login(username="alice_brum", password="StrongPassword123!")
        self.client.post(reverse("reviews:delete", kwargs={"slug": self.draft_review.slug}))
        self.assertFalse(PubReview.objects.filter(pk=self.draft_review.pk).exists())

    def test_editing_review_whose_saved_photo_is_missing_does_not_crash(self):
        with tempfile.TemporaryDirectory() as media_dir, override_settings(MEDIA_ROOT=media_dir):
            self.published_review.uploaded_image = SimpleUploadedFile(
                "pint.png", VALID_PNG_BYTES, content_type="image/png"
            )
            self.published_review.save()
            # Simulate Heroku wiping uploaded files after a restart
            os.remove(self.published_review.uploaded_image.path)
            saved_file = PubReview.objects.get(pk=self.published_review.pk).uploaded_image
            self.assertIs(validate_uploaded_image_file(saved_file), saved_file)

    def test_card_thumbnail_only_rewrites_real_unsplash_urls(self):
        review = self.published_review
        review.featured_image = "https://images.unsplash.com/photo-1?w=1200&q=80"
        self.assertIn("w=500", review.card_image_url)
        review.featured_image = "https://evil.example/images.unsplash.com/x?w=1200&q=80"
        self.assertEqual(review.card_image_url, review.featured_image)


@PLAIN_LOGIN
class PintPassportAndSortingTests(TestCase):
    def setUp(self):
        self.dir_user = User.objects.create_user(username="pub_directory")
        self.dir_user.set_unusable_password()
        self.dir_user.save()

        self.user_a = User.objects.create_user(
            username="user_a", password="StrongPassword123!"
        )
        self.user_b = User.objects.create_user(
            username="user_b", password="StrongPassword123!"
        )
        self.pub_near = PubReview.objects.create(
            title="Stirchley Taproom",
            pub_name="Attic Brew Co",
            brum_area=PubReview.BrumArea.STIRCHLEY,
            latitude=52.4325,
            longitude=-1.9221,
            author=self.user_a,
            pint_quality_rating=5,
            atmosphere_rating=5,
            value_rating=4,
            pint_ordered="Intuition Pale",
            pint_price=Decimal("4.80"),
            serves_cask_ale=True,
            status=PubReview.Status.PUBLISHED,
            content="Great taproom.",
        )
        self.pub_far = PubReview.objects.create(
            title="Sutton Local",
            pub_name="The Station",
            brum_area=PubReview.BrumArea.SUTTON_COLDFIELD,
            latitude=52.5630,
            longitude=-1.8240,
            author=self.user_b,
            pint_quality_rating=4,
            atmosphere_rating=4,
            value_rating=5,
            pint_ordered="Carling",
            pint_price=Decimal("3.60"),
            status=PubReview.Status.PUBLISHED,
            content="Cheap pint near the station.",
        )

    def test_pub_directory_passport_returns_404(self):
        res = self.client.get(
            reverse("reviews:passport", kwargs={"username": "pub_directory"})
        )
        self.assertEqual(res.status_code, 404)

    def test_passport_cheers_count_only_includes_own_authored_reviews(self):
        self.pub_near.likes.add(self.user_b)
        self.pub_far.likes.add(self.user_a)
        Comment.objects.create(
            review=self.pub_near,
            author=self.user_b,
            pint_quality_rating=5,
            atmosphere_rating=5,
            value_rating=5,
            body="Loved visiting Stirchley!",
        )
        res = self.client.get(
            reverse("reviews:passport", kwargs={"username": "user_b"})
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["total_cheers_received"], 1)

    def test_gps_nearest_and_cheapest_pint_sorting(self):
        gps_res = self.client.get(
            reverse("reviews:index"),
            {"sort": "nearest", "lat": "52.4325", "lng": "-1.9221"},
        )
        self.assertEqual(gps_res.status_code, 200)
        self.assertEqual(gps_res.context["reviews"][0], self.pub_near)

        cheap_res = self.client.get(
            reverse("reviews:index"),
            {"sort": "cheapest_pint"},
        )
        self.assertEqual(cheap_res.status_code, 200)
        self.assertEqual(cheap_res.context["reviews"][0], self.pub_far)


class FixtureSecurityTests(TestCase):
    def test_fixture_contains_no_personal_accounts_or_password_hashes(self):
        fixture_path = Path(__file__).resolve().parent / "fixtures" / "birmingham_pubs.json"
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        user_entries = [obj for obj in data if obj.get("model") == "auth.user"]
        self.assertEqual(len(user_entries), 1)
        self.assertEqual(user_entries[0]["fields"]["username"], "pub_directory")
        self.assertFalse(user_entries[0]["fields"]["password"].startswith("pbkdf2_"))


class LoginRateLimitTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="brum_user", password="StrongPassword123!")

    def try_login(self, password, ip="203.0.113.7"):
        return self.client.post(
            reverse("login"),
            {"username": "brum_user", "password": password},
            REMOTE_ADDR=ip,
        )

    def test_five_wrong_passwords_lock_out_even_the_right_one(self):
        for _ in range(5):
            self.try_login("wrong-guess")
        response = self.try_login("StrongPassword123!")
        self.assertEqual(response.status_code, 429)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_lockout_is_per_address_so_others_can_still_log_in(self):
        for _ in range(5):
            self.try_login("wrong-guess", ip="203.0.113.7")
        response = self.try_login("StrongPassword123!", ip="198.51.100.20")
        self.assertEqual(response.status_code, 302)
        self.assertIn("_auth_user_id", self.client.session)

    def test_client_ip_uses_herokus_last_forwarded_address(self):
        from django.test import RequestFactory
        from second_city_pint import settings as project_settings

        request = RequestFactory().get(
            "/", HTTP_X_FORWARDED_FOR="6.6.6.6, 203.0.113.7", REMOTE_ADDR="10.0.0.1"
        )
        with mock.patch.object(project_settings, "ON_HEROKU", True):
            self.assertEqual(project_settings.client_ip(request), "203.0.113.7")
        with mock.patch.object(project_settings, "ON_HEROKU", False):
            self.assertEqual(project_settings.client_ip(request), "10.0.0.1")
