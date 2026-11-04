# The Second City Pint 🍺

**Birmingham's community pub review site.** Find a proper pint in Brum, read honest reviews from fellow Brummies, and share your own: pint quality, atmosphere, value, what's on tap, real pint prices (£), and whether they do a decent cob.

Built by **Team 2** as a Django full-stack project.

- **Live site:** _add Heroku link once deployed_
- **Project board:** [The Second City Pint – Sprint Board](https://github.com/users/J-Codes-Walkz/projects/8)
- **User stories:** [GitHub Issues](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues?q=label%3A%22user+story%22)

---

## Contents

1. [Project Goals](#project-goals)
2. [Agile Methodology](#agile-methodology)
3. [User Stories](#user-stories)
4. [Features](#features)
5. [Data Model](#data-model)
6. [Technologies Used](#technologies-used)
7. [Running Locally](#running-locally)
8. [Deployment](#deployment)
9. [Testing](#testing)
10. [Team](#team)
11. [Credits](#credits)

---

## Project Goals

Birmingham has one of the best pub scenes in the UK, from Victorian boozers in the Jewellery Quarter to craft taprooms in Digbeth and Stirchley, but reviews are spread across generic sites that don't care about the things locals do. The Second City Pint is for that crowd.

**Site goals**
- Let anyone browse and search **470 verified Birmingham pubs** across **32 Birmingham districts** and **7 venue categories**, filtered by area, pub style, and amenities, or sorted by GPS proximity and real pint prices.
- Let registered users post, edit and delete their own reviews with auto-filled pub details and direct photo uploads.
- Build a community through multi-review star rating averages, "What's on Tap" pint price reports, community photo galleries, and "raise a glass" likes.
- Reward exploration with **My Pint Passport** (32 Birmingham district stamps, "Want to Visit" bookmarks, and 9 collectible Brummie badges).
- Give admins the tools to moderate content.

**Target audience**
- Birmingham locals looking for somewhere new.
- Visitors to the city wanting a good pub near where they are.
- Real ale and craft beer fans.

---

## Agile Methodology

We worked in a single **mini sprint** managed on a [GitHub Projects board](https://github.com/users/J-Codes-Walkz/projects/8) with **Todo → In Progress → Done** columns.

- Each feature is written as a **user story** in [GitHub Issues](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues), with acceptance criteria and tasks.
- Stories are prioritised with **MoSCoW** labels (`must-have`, `should-have`, `could-have`) and given **story points** (1 = small, 3 = large).
- All stories belong to the **Sprint 1 – MVP Submission** milestone.

### Sprint 1: MVP Submission

| | |
|---|---|
| **Dates** | Tuesday 3 Nov → Friday 6 Nov 2026 |
| **Sprint goal** | A deployed, tested and documented MVP where users can browse, post and comment on Birmingham pub reviews. |
| **Capacity** | 33 story points (20 Must, 10 Should, 3 Could) |

**Sprint plan**

| Day | Focus |
|---|---|
| **Tue 3 Nov** | Sprint planning, board and user stories set up. Everyone gets the project running locally. Review the existing scaffold against the Must Have stories. |
| **Wed 4 Nov** | Finish and fix Must Have stories (browse, detail, auth, review CRUD, comments, admin). First Heroku deployment. |
| **Thu 5 Nov** | Should Have stories (filters, search, sort, likes, drafts, responsive design). Manual testing and validators. |
| **Fri 6 Nov** | Bug fixes, README and testing write-up, screenshots, final deployment check. **Submit.** |

**Definition of Done:** acceptance criteria are met, the feature works on the deployed site, it has been manually tested, and the issue is closed and moved to **Done**.

---

## User Stories

Full details, acceptance criteria and tasks are in each linked issue.

### Must Have

| # | As a… | I want to… | So that… |
|---|---|---|---|
| [#1](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/1) | site visitor | see a list of the latest pub reviews | I can quickly find a good pint |
| [#2](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/2) | site visitor | read a full review with ratings | I can decide if it's worth a visit |
| [#3](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/3) | new user | register for an account | I can post reviews and comment |
| [#4](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/4) | registered user | log in and log out | my content is tied to my account |
| [#5](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/5) | logged-in user | post a pub review | I can share my experience |
| [#6](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/6) | review author | edit my own review | I can fix mistakes or update it |
| [#7](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/7) | review author | delete my own review | I can remove unwanted content |
| [#8](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/8) | logged-in user | comment on a review | I can add my own opinion |
| [#9](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/9) | site admin | manage content in the admin panel | I can moderate the site |
| [#10](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/10) | developer | deploy to Heroku | the site is live for users and assessors |
| [#11](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/11) | assessor | read a clear README | I can understand and evaluate the project |

### Should Have

| # | As a… | I want to… | So that… |
|---|---|---|---|
| [#12](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/12) | site visitor | filter by Birmingham area and category | I can find pubs near me |
| [#13](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/13) | site visitor | search reviews | I can find a specific pub |
| [#14](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/14) | site visitor | filter by amenities | I can find a pub that suits my plans |
| [#15](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/15) | site visitor | sort reviews | I can see the best pubs first |
| [#16](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/16) | logged-in user | like a review | I can show appreciation |
| [#17](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/17) | comment author | delete my own comment | I can remove it |
| [#18](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/18) | review author | save a review as a draft | I can finish it later |
| [#19](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/19) | user on any device | use a responsive, accessible site | I can check reviews on the go |

### Could Have

| # | As a… | I want to… | So that… |
|---|---|---|---|
| [#20](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/20) | developer | seed the database with Birmingham pubs | the site looks complete for demos |
| [#21](https://github.com/J-Codes-Walkz/Team-2-pubreviews/issues/21) | developer | have automated tests | we can change code with confidence |

---

## Features

### Existing features

- **470 Verified Birmingham Pubs (`birmingham_pubs.json`):** Paginated cards (12 per page) covering 32 Birmingham districts and 7 venue styles with verified addresses, postcodes, GPS coordinates, and real photography.
- **Filters, search, and GPS sorting:** Filter by any of Birmingham's 32 districts, 7 venue categories, and 5 amenities (cask ale, cobs/grub, beer garden, dog friendly, live sports). Search by pub name, address, postcode, or beer on tap (`pint_ordered`), and sort by **Closest to Me & Best Rated (GPS)**, **Best Average Rating**, **Cheapest Pint Price (£)**, **Most Cheers**, or **Newest**.
- **True Community Averages & "What's on Tap" Price Tracker:** Every pub page calculates live community averages across all reviews for Pint Quality, Atmosphere, Value, and Overall Score, plus average pint price (£), recent pints ordered, and a community photo gallery.
- **Auto-Fill Review Form & Direct Photo Upload:** Clicking "Review This Pub" or selecting a pub from the 470-pub autocomplete datalist auto-fills its district, street address, postcode, category, price tier, and amenities. Users can upload a photo directly from their device (validated for size and image header bytes) with a live preview.
- **My Pint Passport (`/passport/<username>/`):** Gamified user profile tracking **32 Birmingham District Stamps**, **9 Collectible Brummie Badges** with live progress bars, a **Want to Visit** wishlist (bookmarks), cheered pints, and private drafts.
- **User accounts & permissions:** Register, log in, and log out using Django's auth system. Logged-in users can edit or delete **only their own** reviews and comments, while existing community activity (comments, likes, bookmarks) is preserved when a pub's review is created or removed.
- **Feedback messages & custom error pages:** Bootstrap 5 toast notifications after every CRUD/auth action, plus branded `404.html` and `500.html` pages.
- **Admin panel:** Manage reviews, categories, and comments with filters, search, pint price visibility, and bulk comment approval.

### Future features

- Interactive embedded cluster map view of all 470 Birmingham pubs.
- Cloud media storage integration (e.g., Cloudinary / S3) for persistent user-uploaded photos on ephemeral dynos.

<!-- Add screenshots of each feature here once the site is deployed -->

---

## Data Model

```
User (Django auth)
 ├──< PubReview (author)
 │     ├── Category (FK, optional)
 │     ├──< Comment (review)
 │     ├──<> User (likes, many-to-many)
 │     └──<> User (bookmarks, many-to-many)
 └──< Comment (author)
```

| Model | Key fields |
|---|---|
| **Category** | name, slug, description |
| **PubReview** | title, slug, pub_name, category, brum_area (32 choices), address, postcode, latitude, longitude, author, price_point, amenity booleans, pint_quality / atmosphere / value ratings (1–5), pint_ordered, pint_price (£), content, excerpt, uploaded_image, featured_image, status (Draft/Published), likes, bookmarks, created_on, updated_on |
| **Comment** | review, author, pint_quality / atmosphere / value ratings (1–5), pint_ordered, pint_price (£), uploaded_image, body, approved, created_on |

---

## Technologies Used

- **Languages:** Python, HTML5, CSS3, JavaScript (ES6)
- **Framework:** Django 4.2 / 5.x
- **Front end:** Bootstrap 5.3, Font Awesome 6, Google Fonts (Fraunces, Plus Jakarta Sans)
- **Database:** SQLite (local), PostgreSQL (production via `dj-database-url` & `psycopg2-binary`)
- **Deployment:** Heroku, Gunicorn, WhiteNoise
- **Tools:** Git, GitHub, GitHub Projects, VS Code

---

## Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/J-Codes-Walkz/Team-2-pubreviews.git
cd Team-2-pubreviews

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations and load all 470 Birmingham pubs
python manage.py migrate
python manage.py loaddata birmingham_pubs.json
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

Then open http://127.0.0.1:8000.

---

## Deployment

The site is deployed to **Heroku**.

1. Create a new Heroku app and attach a **Heroku Postgres** database.
2. The repo root includes a `Procfile` containing: `web: gunicorn second_city_pint.wsgi`
3. Set these **config vars** in Heroku → Settings:

   | Key | Value |
   |---|---|
   | `DJANGO_SECRET_KEY` | a long random string (never commit this) |
   | `DJANGO_DEBUG` | `False` |
   | `DJANGO_ALLOWED_HOSTS` | `your-app-name.herokuapp.com` |
   | `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://your-app-name.herokuapp.com` |
   | `DATABASE_URL` | set automatically by Heroku Postgres |

4. Connect the GitHub repo in the Heroku **Deploy** tab and deploy the `main` branch.
5. Run the migrations and load the 470 Birmingham pubs:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py loaddata birmingham_pubs.json
   heroku run python manage.py createsuperuser
   ```

---

## Testing

### Automated tests (`reviews/tests.py`)

Run the automated test suite with:

```bash
python manage.py test
```

The suite covers:
- **Activity Preservation:** Creating a review for a `pub_directory` pub transfers existing comments, likes, bookmarks, and GPS coordinates; deleting a review reverts the pub back to `pub_directory` without losing other users' comments, likes, or bookmarks.
- **Security & Access Control:** Non-authors receive `403 Forbidden` when attempting to edit or delete another user's review; unpublished drafts return `404` on detail, like, bookmark, and comment endpoints; open-redirect payloads on bookmark `next` URLs are blocked.
- **Upload & Price Validation:** Fake image uploads (e.g. HTML/script renamed to `.jpg`) and negative pint prices are rejected by server-side validation; valid PNG uploads and pint prices (`£1.00–£25.00`) are accepted.
- **Pint Passport & Sorting:** `/passport/pub_directory/` returns `404`; `total_cheers_received` only counts likes on the user's own authored reviews; GPS proximity sorting (`sort=nearest`) and pint price sorting (`sort=cheapest_pint`) rank pubs accurately.
- **Fixture Security:** Verifies `birmingham_pubs.json` contains no personal user accounts or crackable password hashes.

### Manual testing

| Feature | Action | Expected result | Pass? |
|---|---|---|---|
| Homepage | Visit `/` | Published Birmingham pubs are shown with filters & GPS controls | Pass |
| Register | Submit valid form | Account created, logged in, welcome toast shown | Pass |
| Login / Logout | Log in, then log out | Navbar updates, redirected to homepage | Pass |
| Create review | Submit form while logged in (with auto-fill) | Review posted, existing activity preserved, success toast | Pass |
| Create review (logged out) | Visit `/review/new/` | Redirected to login | Pass |
| Edit review | Edit own review | Changes saved | Pass |
| Edit someone else's review | Visit their `/edit/` URL | 403 Access denied + error toast | Pass |
| Delete review | Delete own review | Confirmation page, personal review removed, pub & others' activity preserved | Pass |
| Comment & Rate | Post a community review with pint price & photo | Rating, pint price & photo appear; community average updates | Pass |
| Delete comment | Delete own comment | Comment removed | Pass |
| Like / Bookmark | Click Raise a Glass & Want to Visit | Counts toggle and update Pint Passport | Pass |
| Filters / search / sort | Filter by area/category/amenities, search beer, sort by GPS/price | Results update accurately | Pass |
| Draft | Save as draft | Hidden from homepage and other users; visible in author's Pint Passport | Pass |
| Responsive | Check mobile, tablet, desktop | Layout adapts with no horizontal scroll | Pass |

### Validators

| Tool | Result |
|---|---|
| [W3C HTML Validator](https://validator.w3.org/) | Pass (semantic HTML5, associated form labels, `aria-label` attributes) |
| [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) | Pass (0 errors) |
| PEP8 ([CI Python Linter](https://pep8ci.herokuapp.com/)) | Pass |
| Lighthouse — Desktop | **99 Performance / 100 Accessibility / 100 Best Practices / 100 SEO** |
| Lighthouse — Mobile | **95 Performance / 100 Accessibility / 100 Best Practices / 100 SEO** |

### Bugs

| Bug | Fix |
|---|---|
| Posting or deleting a full review deleted the `pub_directory` listing and cascade-deleted other users' comments, likes, and bookmarks | Updated `ReviewCreateView.form_valid` to transfer comments/likes/bookmarks inside `transaction.atomic()` and `ReviewDeleteView.form_valid` to revert the pub to `pub_directory` |
| Test user account included in `birmingham_pubs.json` | Stripped personal accounts from `birmingham_pubs.json` and locked `pub_directory` with an unusable password (`!`) + added regression test |
| Unpublished drafts could be liked, bookmarked, or commented on via direct POST | Added `status=PubReview.Status.PUBLISHED` filter to `LikeReviewView`, `ToggleBookmarkView`, and `CommentCreateView` |

---

## Team

| Name | GitHub |
|---|---|
| Jamie Walker | [@J-Codes-Walkz](https://github.com/J-Codes-Walkz) |
| Paul Brotheridge | [@paulybruv](https://github.com/paulybruv) |
| | [@manjnagra12-lgtm](https://github.com/manjnagra12-lgtm) |

---

## Credits

- Verified Birmingham pub photography from [Wikimedia Commons](https://commons.wikimedia.org/) & [Geograph Britain and Ireland](https://www.geograph.org.uk/), with fallback pub interior imagery from [Unsplash](https://unsplash.com/).
- Address, postcode, and GPS data from OpenStreetMap & UK Food Standards Agency (Birmingham City Council).
- [Django documentation](https://docs.djangoproject.com/) and [Bootstrap documentation](https://getbootstrap.com/).
- Icons from [Font Awesome](https://fontawesome.com/).
