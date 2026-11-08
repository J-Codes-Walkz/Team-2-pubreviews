# The Second City Pint 🍺

**Birmingham's community pub review site.** Find a proper pint in Brum, read honest reviews from fellow Brummies, and share your own: pint quality, atmosphere, value, what's on tap, real pint prices (£), and whether they do a decent cob.

Built by **Team 2** as a Django full-stack project.

- **Live site:** [second-city-pint-f74826035477.herokuapp.com](https://second-city-pint-f74826035477.herokuapp.com/)
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
7. [Running Locally](#running-locally) (including the [Admin panel](#admin-panel))
8. [Deployment](#deployment)
9. [Security](#security)
10. [Testing](#testing)
11. [Project Mind Map](#project-mind-map)
12. [Team](#team)
13. [Credits](#credits)

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

We worked in a single **mini sprint** managed on a [GitHub Projects board](https://github.com/users/J-Codes-Walkz/projects/8) with **Backlog → Todo → In Progress → Completed** columns.

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

**Definition of Done:** acceptance criteria are met, the feature works on the deployed site, it has been manually tested, and the issue is closed and moved to **Completed**.

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
- **Auto-Fill Review Form & Direct Photo Upload:** Clicking "Review This Pub" or selecting a pub from the 470-pub autocomplete datalist auto-fills its district, street address, postcode, category, price tier, and amenities. Users can upload a photo directly from their device (validated for size and image header bytes) with a live preview. On the live site, uploads are stored on Cloudinary so they survive Heroku restarts.
- **My Pint Passport (`/passport/<username>/`):** Gamified user profile tracking **32 Birmingham District Stamps**, **9 Collectible Brummie Badges** with live progress bars, a **Want to Visit** wishlist (bookmarks), cheered pints, and private drafts.
- **User accounts & permissions:** Register, log in, and log out using Django's auth system. Logged-in users can edit or delete **only their own** reviews and comments, while existing community activity (comments, likes, bookmarks) is preserved when a pub's review is created or removed.
- **Feedback messages & custom error pages:** Bootstrap 5 toast notifications after every CRUD/auth action, plus branded `404.html` and `500.html` pages.
- **Admin panel:** Manage reviews, categories, and comments with filters, search, pint price visibility, and bulk comment approval.

### Future features

- Interactive embedded cluster map view of all 470 Birmingham pubs.
- Password reset by email (the site has no email service yet, so there is no "Forgot password?" link).
- A Content-Security-Policy header (needs care because the site loads Bootstrap, Font Awesome and Google Fonts from CDNs).

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
- **Framework:** Django 5.2 (long-term support release, security fixes until April 2028)
- **Front end:** Bootstrap 5.3, Font Awesome 6, Google Fonts (Fraunces, Plus Jakarta Sans)
- **Database:** SQLite (local), PostgreSQL (production via `dj-database-url` & `psycopg2-binary`)
- **Deployment:** Heroku (Python 3.12), Gunicorn, WhiteNoise, Cloudinary (uploaded photos)
- **Security:** django-axes (login rate limiting), gitleaks (secret scanning), pip-audit (dependency scanning), GitHub CodeQL
- **Tools:** Git, GitHub, GitHub Projects, VS Code, Claude Code, [graphify](https://github.com/Graphify-Labs/graphify) (project mind map)

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

# 5. Run the server
python manage.py runserver
```

Then open http://127.0.0.1:8000.

### Admin panel

The Django admin at `/admin` is where admins manage pub reviews, categories, comments (including bulk approval) and users. It needs a **superuser** account:

```bash
python manage.py createsuperuser
```

Choose a username, an optional email and a strong password when prompted. The password is not shown as you type.

- Each developer creates their own superuser on their own local database. Accounts are never added to `birmingham_pubs.json`, and an automated test checks for this.
- The live site has its own superuser, created once with `heroku run python manage.py createsuperuser`.
- Admin logins are kept in the team's password manager, never in the repo, issues or chat.
- The admin login is rate-limited in the same way as the site login (see [Security](#security)).

---

## Deployment

The site runs on **Heroku** (EU region) with a Basic web dyno and a Heroku Postgres (Essential-0) database. Uploaded photos are stored on **Cloudinary**, because Heroku's disk is wiped on every restart.

**Files Heroku uses**
- `Procfile`: `release: python manage.py migrate --noinput` applies any new migrations on every deploy, before the new version goes live, and `web: gunicorn second_city_pint.wsgi` runs the site.
- `.python-version`: pins Python 3.12, the version the project is developed and tested on.
- `requirements.txt`: the packages Heroku installs.

**Steps**

1. Create a Heroku app (EU region) and attach **Heroku Postgres**.
2. Create a free [Cloudinary](https://cloudinary.com/) account and copy its **API environment variable** (`cloudinary://…`).
3. Set these **config vars** in Heroku → Settings → Reveal Config Vars:

   | Key | Value |
   |---|---|
   | `DJANGO_SECRET_KEY` | a long random string, generated fresh and never committed |
   | `DJANGO_DEBUG` | `False` |
   | `DJANGO_ALLOWED_HOSTS` | the app's domain, e.g. `your-app-name-1234abcd.herokuapp.com` |
   | `CLOUDINARY_URL` | the Cloudinary API environment variable from step 2 |
   | `DATABASE_URL` | set automatically by Heroku Postgres |

   `DJANGO_CSRF_TRUSTED_ORIGINS` is optional; it defaults to `https://` plus each allowed host.

4. Deploy the `main` branch: `git push heroku main`, or connect the GitHub repo in the Heroku **Deploy** tab. The release step runs the migrations.
5. Load the 470 Birmingham pubs and create the admin account (one time only):
   ```bash
   heroku run python manage.py loaddata birmingham_pubs.json
   heroku run python manage.py createsuperuser
   ```

**Fail-safes:** on Heroku, debug mode defaults to **off** even if `DJANGO_DEBUG` is missing, and the site refuses to start without a real `DJANGO_SECRET_KEY`. That way a missed config var can't put the live site into debug mode or leave it with the public development key.

---

## Security

A pre-launch security review was run across the whole project (not just recent changes) before the first deploy on 4 November 2026.

| Area | What is in place |
|---|---|
| Secrets | Secret key, database and Cloudinary credentials live only in Heroku config vars; `.env`, the database and `media/` are gitignored. A gitleaks scan of the full git history found no leaked secrets, and a gitleaks pre-commit hook blocks new ones. |
| Logins | Django's built-in auth with slow password hashing. **django-axes** locks out an account and address combination for **1 hour after 5 wrong passwords**, on both the site login and `/admin`. It reads the visitor's real address from the last `X-Forwarded-For` entry, which Heroku's router adds, so one attacker can't lock everyone out. |
| Permissions | Only a review's or comment's author can edit or delete it (403 otherwise), checked in the views and not just by hiding buttons. Drafts are private, and deleting one really deletes it. |
| Input | CSRF protection on every form, the Django ORM only (no raw SQL), no `|safe` on user content, uploads limited to 5 MB and real JPEG/PNG/GIF/WebP files, pint prices limited to £1–£25, and `next` redirects limited to this site. |
| HTTPS & headers | HTTPS redirect, HSTS (1 year), secure and HttpOnly cookies, `X-Frame-Options: DENY` and `nosniff`. `python manage.py check --deploy` reports no issues. |
| Dependencies | Django 5.2 LTS (receives security fixes until April 2028). `pip-audit` found no known vulnerabilities in the packages the site runs on. GitHub CodeQL scans every pull request. |

**Known gaps** (see [Future features](#future-features)): no Content-Security-Policy header yet, and no password reset by email.

---

## Testing

### Automated tests (`reviews/tests.py`)

Run the automated test suite with:

```bash
python manage.py test
```

**17 tests, all passing.** The suite covers:
- **Activity Preservation:** Creating a review for a `pub_directory` pub transfers existing comments, likes, bookmarks, and GPS coordinates; deleting a published review reverts the pub back to `pub_directory` without losing other users' comments, likes, or bookmarks.
- **Security & Access Control:** Non-authors receive `403 Forbidden` when attempting to edit or delete another user's review; unpublished drafts return `404` on detail, like, bookmark, and comment endpoints; deleting a draft really deletes it instead of publishing it; open-redirect payloads on bookmark `next` URLs are blocked.
- **Upload & Price Validation:** Fake image uploads (e.g. HTML/script renamed to `.jpg`) and negative pint prices are rejected by server-side validation; valid PNG uploads and pint prices (`£1.00–£25.00`) are accepted; editing a review whose saved photo has gone missing from disk does not crash; card thumbnails are only rewritten for real Unsplash addresses.
- **Pint Passport & Sorting:** `/passport/pub_directory/` returns `404`; `total_cheers_received` only counts likes on the user's own authored reviews; GPS proximity sorting (`sort=nearest`) and pint price sorting (`sort=cheapest_pint`) rank pubs accurately.
- **Login Rate Limiting:** 5 wrong passwords lock the account out from that address (even the right password then gets `429 Too Many Requests`), the same account can still log in from another address, and the visitor's address is read from Heroku's last `X-Forwarded-For` entry.
- **Fixture Security:** Verifies `birmingham_pubs.json` contains no personal user accounts or crackable password hashes.

The tests that only need a logged-in user use Django's plain login backend, because the test shortcut `client.login()` doesn't pass the request that django-axes needs. The rate-limit tests log in through the real login page with axes switched on.

The tests for the draft, missing-photo and Unsplash fixes in the Bugs table below were run against the old code first, to confirm they fail there and pass with the fix.

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
| After the test account was removed, `loaddata birmingham_pubs` failed on a fresh database (FOREIGN KEY error) because The Farthings still had that account's like and bookmark | Emptied that pub's `likes` and `bookmarks` in the fixture; checked by loading it into a fresh database |
| Deleting a private draft turned it into a public directory listing, because the `pub_directory` check in `ReviewDeleteView` is always true | Only **published** reviews revert to a listing; drafts are really deleted (test added) |
| Editing a review crashed (`FileNotFoundError`) if its saved photo was gone from disk, which happens on Heroku after every restart | `validate_uploaded_image_file` only checks brand-new uploads, not the already-saved file (test added) |
| CodeQL alert (high): `card_image_url` matched `"images.unsplash.com/"` anywhere in the URL | Compares the URL's real hostname with `urlparse` (test added) |
| Uploaded photos would show as broken images on the live site: Django only serves `media/` in debug mode, and Heroku wipes uploads on restart | Uploads are stored on Cloudinary when `CLOUDINARY_URL` is set |
| Django 5.1 no longer receives security fixes, and logins had no limit on password guesses | Upgraded to Django 5.2 LTS and added django-axes (tests added) |

---

## Project Mind Map

A knowledge graph of the whole project (Python code, templates, README and requirements) is kept in `graphify-out/`. It was built with [graphify](https://github.com/Graphify-Labs/graphify) and is used as a mind map: it shows which models, views, forms, tests, pages and documented features connect to each other, and which parts everything else depends on.

| File | What it is |
|---|---|
| [graphify-out/graph.html](./graphify-out/graph.html) | The interactive graph. GitHub shows this file as source code, so download it (or clone the repo) and open it in a browser. It loads one script from the internet, so it needs a connection. |
| [graphify-out/GRAPH_REPORT.md](./graphify-out/GRAPH_REPORT.md) | A plain-language report: the most connected nodes, surprising connections and questions worth asking. |
| [graphify-out/graph.json](./graphify-out/graph.json) | The raw graph data. |

**How it grew**, refreshed at each stage of the project:

| Date | Stage | Nodes | Links | Clusters |
|---|---|---|---|---|
| 4 November 2026 | Sprint 1: Must Haves built, security hardening, before the first deploy | 306 | 511 | 18 |

<p>
  <img src="./docs/images/mind-map-2026-11-04.png" alt="The mind map on 4 November 2026: 306 nodes in 18 clusters, with the PubReview model at the centre" width="820">
</p>

The 4 November build read 40 files: the 28 Python files by parsing them directly (free), and 12 templates and documents with AI (124,617 tokens). Of the 18 clusters, 4 are single files (the empty `__init__.py` package markers); the rest line up with real parts of the project, such as the pub import scripts, the `PubReview` model, upload and price validation, GPS sorting and the Heroku stack.

**How it was used.** The most connected nodes are the `PubReview` (46 links), `Comment` (15) and `Category` (13) models, which confirms that almost everything rests on `PubReview`. It is the bridge between the import scripts, views, forms, tests and GPS sorting, so a change to it needs the full test suite run. `SecurityAndValidationTests` is the next biggest bridge, joining the upload and price validation to the model, which is where the security tests should sit. The graph also grouped the GPS sorting flow (browser location → `requestUserGPS` → the server-side sort) and the "community engagement loop" (rate, cheer, bookmark, Pint Passport) as single features across several files.

**Where it was wrong or incomplete.** Links marked "inferred" in the report are the AI's reasoning, not read from a file, and two of its "surprising connections" were checked against the code:

| The graph says | Checked against the code |
|---|---|
| The review form's pub auto-fill "shares data with" the `birmingham_pubs.json` fixture | **Right in spirit, but indirect.** The form builds its pub list from the `PubReview` table at request time (`reviews/views.py`); the fixture is only how those rows got into the database. |
| The review detail page "implements" author-only edit/delete (403) | **Overstated.** The page only hides the Edit and Delete buttons from other users. The real protection is the `test_func` check in `ReviewUpdateView` and `ReviewDeleteView`, which returns 403 even if someone types the URL. |

Its health check also reported **120 links whose far end isn't a real node**. Checking them showed that about three quarters are the code parser's `import` links to outside libraries such as `re`, `json`, `math` and parts of Django, which it records without full nodes (they appear in the graph as bare placeholders). About a sixth are function calls it couldn't trace to a definition, and the rest are links from the AI reader that named a code item slightly differently from the parser. It also found no symbols in 5 Python files (`settings.py`, the two `urls.py` files, `asgi.py` and `wsgi.py`), because they hold settings and URL lists rather than classes or functions. So the graph is a guide, not a complete or perfectly current map: a missing link doesn't prove two things are unconnected.

Screenshots, the 470-pub fixture, uploaded media and the local database are left out of the graph (see `.graphifyignore`): they are test evidence or data, not project structure. To refresh it after new work, run `/graphify . --update` in Claude Code. Only the three files above are committed; the cache stays local (see `.gitignore`).

---

## Team

| Name | GitHub |
|---|---|
| Jamie Walker | [@J-Codes-Walkz](https://github.com/J-Codes-Walkz) |
| Paul Brotheridge | [@paulybruv](https://github.com/paulybruv) |
| Manj Nagra | [@manjnagra12-lgtm](https://github.com/manjnagra12-lgtm) |

---

## Credits

- Verified Birmingham pub photography from [Wikimedia Commons](https://commons.wikimedia.org/) & [Geograph Britain and Ireland](https://www.geograph.org.uk/), with fallback pub interior imagery from [Unsplash](https://unsplash.com/).
- Address, postcode, and GPS data from OpenStreetMap & UK Food Standards Agency (Birmingham City Council).
- [Django documentation](https://docs.djangoproject.com/) and [Bootstrap documentation](https://getbootstrap.com/).
- Icons from [Font Awesome](https://fontawesome.com/).
