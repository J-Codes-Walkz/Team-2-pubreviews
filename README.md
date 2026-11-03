# The Second City Pint — Birmingham, UK Pub Review Blog

A collaborative Birmingham pub review web application built with **Django**, **Bootstrap 5**, and **FontAwesome 6**.

## 3-Developer Team Split
1. **Base Shell, Auth & UI Framework (`second_city_pint/`, `templates/base.html`, `templates/registration/`)**
   - Project settings, authentication routes, heritage pub UI theme, sticky responsive navbar, and dismissible Bootstrap 5 toast notifications.
2. **Core Pub Review CRUD Engine (`reviews/models.py`, `reviews/forms.py`, `reviews/views.py`, `reviews/admin.py`)**
   - `Category` and `PubReview` models, star ratings (`pint_quality_rating`, `atmosphere_rating`, `value_rating`), author-protected `CreateView` / `UpdateView` / `DeleteView`.
3. **Community Engagement & Discovery (`reviews/views.py`, `templates/reviews/index.html`, `populate_birmingham_pubs.py`)**
   - Dynamic filtering by Birmingham district (`brum_area`), pub category, search query, and multi-amenity checkboxes (`serves_cask_ale`, `serves_cobs_or_food`, `has_beer_garden`, `is_dog_friendly`, `shows_live_sports`), plus `LikeReviewView` and `Comment` threads.

## Quick Start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations reviews
python manage.py migrate
python manage.py populate_birmingham_pubs
python manage.py runserver
```

### Seeded Demo Accounts
- **Usernames:** `brummie_pete`, `jq_hannah`, `digbeth_dan`, `harborne_helen`
- **Password:** `BrumPint2025!`
