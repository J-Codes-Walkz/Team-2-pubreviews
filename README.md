# The Second City Pint 🍺

**Birmingham's community pub review site.** Find a proper pint in Brum, read honest reviews from fellow Brummies, and share your own: pint quality, atmosphere, value, and whether they do a decent cob.

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

Birmingham has one of the best pub scenes in the UK, from Victorian boozers in the Jewellery Quarter to craft taprooms in Digbeth, but reviews are spread across generic sites that don't care about the things locals do. The Second City Pint is for that crowd.

**Site goals**
- Let anyone browse and search Birmingham pub reviews by area, pub type and amenities.
- Let registered users post, edit and delete their own reviews.
- Build a community through comments and "raise a glass" likes.
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

### Won't Have (this sprint)

- User profile pages
- Map view of pubs
- Uploading images directly (we use image URLs for now)

---

## Features

### Existing features

- **Homepage review feed:** paginated cards (9 per page) showing pub image, name, area, overall rating and excerpt.
- **Filters and search:** filter by Birmingham area (City Centre, Digbeth, Jewellery Quarter, Harborne, Moseley, Stirchley, Kings Heath, Aston, Edgbaston, Bournville), category and amenities. Keyword search, and sort by newest, top pint or most liked.
- **Review detail page:** ratings for pint quality, atmosphere and value, an overall score, price point (£ / ££ / £££) and amenity badges (cask ale, cobs/food, beer garden, dog friendly, live sports).
- **User accounts:** register, log in and log out using Django's auth system.
- **Review CRUD:** logged-in users can create reviews and edit or delete **only their own**. Reviews can be saved as drafts.
- **Comments:** logged-in users can comment on reviews and delete their own comments.
- **Likes:** "raise a glass" to a review, and toggle it off again.
- **Feedback messages:** success, warning and error messages after every action.
- **Admin panel:** manage reviews, categories and comments, with filters and bulk comment approval.
- **Seed data:** `populate_birmingham_pubs` loads sample Birmingham pubs, users and comments.

### Future features

- User profile pages listing a user's reviews.
- Interactive map of reviewed pubs.
- Image uploads via Cloudinary.

<!-- Add screenshots of each feature here once the site is deployed -->

---

## Data Model

```
User (Django auth)
 ├──< PubReview (author)
 │     ├── Category (FK, optional)
 │     ├──< Comment (review)
 │     └──<> User (likes, many-to-many)
 └──< Comment (author)
```

| Model | Key fields |
|---|---|
| **Category** | name, slug, description |
| **PubReview** | title, slug, pub_name, category, brum_area, author, price_point, amenity booleans, pint_quality / atmosphere / value ratings (1–5), content, excerpt, featured_image, status (Draft/Published), likes, created_on, updated_on |
| **Comment** | review, author, body, approved, created_on |

---

## Technologies Used

- **Languages:** Python, HTML, CSS, JavaScript
- **Framework:** Django 4.2 / 5.x
- **Front end:** Bootstrap 5.3, Font Awesome 6, Google Fonts (Fraunces, Plus Jakarta Sans)
- **Database:** SQLite (local), PostgreSQL (production via `dj-database-url`)
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

# 4. Set up the database and sample data
python manage.py migrate
python manage.py populate_birmingham_pubs
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

Then open http://127.0.0.1:8000.

---

## Deployment

The site is deployed to **Heroku**.

1. Create a new Heroku app and attach a **Heroku Postgres** database.
2. Add a `Procfile` to the repo root containing: `web: gunicorn second_city_pint.wsgi`
3. Set these **config vars** in Heroku → Settings:

   | Key | Value |
   |---|---|
   | `DJANGO_SECRET_KEY` | a long random string (never commit this) |
   | `DJANGO_DEBUG` | `False` |
   | `DJANGO_ALLOWED_HOSTS` | `your-app-name.herokuapp.com` |
   | `DATABASE_URL` | set automatically by Heroku Postgres |

4. Connect the GitHub repo in the Heroku **Deploy** tab and deploy the `main` branch.
5. Run the migrations and seed data:
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py populate_birmingham_pubs
   heroku run python manage.py createsuperuser
   ```

---

## Testing

<!-- Fill in during Thu/Fri of the sprint -->

### Manual testing

| Feature | Action | Expected result | Pass? |
|---|---|---|---|
| Homepage | Visit `/` | Published reviews are shown, newest first | |
| Register | Submit valid form | Account created, logged in, welcome message | |
| Login / Logout | Log in, then log out | Navbar updates, redirected to homepage | |
| Create review | Submit form while logged in | Review posted, success message | |
| Create review (logged out) | Visit `/review/new/` | Redirected to login | |
| Edit review | Edit own review | Changes saved | |
| Edit someone else's review | Visit their `/edit/` URL | Access denied | |
| Delete review | Delete own review | Confirmation page, then removed | |
| Comment | Post a comment | Comment appears with message | |
| Delete comment | Delete own comment | Comment removed | |
| Like | Click like, then click again | Count goes up, then back down | |
| Filters / search / sort | Use each control | Results update correctly | |
| Draft | Save as draft | Hidden from homepage and other users | |
| Responsive | Check mobile, tablet, desktop | Layout adapts with no horizontal scroll | |

### Validators

| Tool | Result |
|---|---|
| [W3C HTML Validator](https://validator.w3.org/) | |
| [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) | |
| PEP8 ([CI Python Linter](https://pep8ci.herokuapp.com/)) | |
| Lighthouse (performance / accessibility) | |

### Bugs

| Bug | Fix |
|---|---|
| | |

---

## Team

| Name | GitHub |
|---|---|
| Jamie Walker | [@J-Codes-Walkz](https://github.com/J-Codes-Walkz) |
| Paul Brotheridge | [@paulybruv](https://github.com/paulybruv) |
| | [@manjnagra12-lgtm](https://github.com/manjnagra12-lgtm) |

---

## Credits

- Default pub image from [Unsplash](https://unsplash.com/).
- [Django documentation](https://docs.djangoproject.com/) and [Bootstrap documentation](https://getbootstrap.com/).
- Icons from [Font Awesome](https://fontawesome.com/).
