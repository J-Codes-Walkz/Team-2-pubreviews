# Graph Report - Team-2-pubreviews  (2026-11-04)

## Corpus Check
- Corpus is ~27,752 words - fits in a single context window. You may not need a graph.

## Summary
- 306 nodes · 511 edges · 18 communities (10 shown, 8 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.92)
- Token cost: 124,617 input · 0 output

## Community Hubs (Navigation)
- Pub Data Import Scripts
- Views and Django Imports
- Features, Pages and Docs
- Forms, Tests and Imports
- PubReview Model
- Database Migrations
- Upload and Price Validation
- Project Setup and Settings
- Register and Post Review
- GPS Distance Sorting
- Heroku Production Stack
- Pub Seeding Command
- Project, Sprint and Team
- App Config

## God Nodes (most connected - your core abstractions)
1. `PubReview` - 46 edges
2. `Comment` - 15 edges
3. `Category` - 13 edges
4. `SecurityAndValidationTests` - 13 edges
5. `base.html site layout` - 12 edges
6. `CommentForm` - 10 edges
7. `Pub review detail page` - 10 edges
8. `Create/edit review form page` - 10 edges
9. `PubReviewForm` - 9 edges
10. `ReviewCreateView` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Pub details auto-fill from pub_directory_json` --shares_data_with--> `birmingham_pubs.json fixture (470 verified pubs)`  [INFERRED]
  templates/reviews/review_form.html → README.md
- `Pub review detail page` --implements--> `Author-only edit/delete access control (403)`  [INFERRED]
  templates/reviews/review_detail.html → README.md
- `Pub filter form (area, style, search, sort, amenities)` --implements--> `GPS proximity sort (Closest to Me & Best Rated)`  [INFERRED]
  templates/reviews/index.html → README.md
- `Pint Passport profile page` --implements--> `My Pint Passport (district stamps, badges, wishlist)`  [INFERRED]
  templates/reviews/passport.html → README.md
- `Pub list homepage (card grid)` --shares_data_with--> `PubReview model`  [INFERRED]
  templates/reviews/index.html → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **GPS proximity sorting flow (browser geolocation to server sort)** — templates_reviews_index_pub_filter_form, templates_reviews_index_requestusergps, templates_reviews_index_applygpscoordinates, templates_reviews_index_clearusergps, templates_reviews_index_gps_session_restore, readme_gps_proximity_sort [INFERRED 0.95]
- **Heroku production stack** — readme_heroku_deployment, requirements_gunicorn, requirements_whitenoise, requirements_dj_database_url, requirements_psycopg2_binary [EXTRACTED 1.00]
- **Community engagement loop (rate, cheer, bookmark, passport)** — templates_reviews_review_detail_community_review_form, templates_reviews_review_detail_engagement_bar, templates_reviews_passport_wishlist_tab, templates_reviews_passport_district_stamps, readme_pint_passport, readme_community_averages [INFERRED 0.85]

## Communities (18 total, 8 thin omitted)

### Community 0 - "Pub Data Import Scripts"
Cohesion: 0.07
Nodes (25): build_pub_description(), classify_true_category(), Command, match_osm(), process_pub(), fetch_osm_birmingham_venues(), fetch_web_search_description(), fetch_website_meta_description() (+17 more)

### Community 1 - "Views and Django Imports"
Cohesion: 0.06
Nodes (11): CommentForm, Meta, CommentCreateView, CommentDeleteView, LikeReviewView, MyPassportRedirectView, PintPassportView, ReviewDeleteView (+3 more)

### Community 2 - "Features, Pages and Docs"
Cohesion: 0.08
Nodes (37): Automated test suite (reviews/tests.py), birmingham_pubs.json fixture (470 verified pubs), Category model (7 venue styles), Comment model (community review with ratings, pint price, photo), True Community Averages & What's on Tap price tracker, Draft/Published review status, GPS proximity sort (Closest to Me & Best Rated), My Pint Passport (district stamps, badges, wishlist) (+29 more)

### Community 3 - "Forms, Tests and Imports"
Cohesion: 0.08
Nodes (9): CategoryAdmin, CommentAdmin, CommentInline, PubReviewAdmin, Comment, Meta, FixtureSecurityTests, PintPassportAndSortingTests (+1 more)

### Community 4 - "PubReview Model"
Cohesion: 0.13
Nodes (5): PubReview, BrumArea, Meta, PricePoint, Status

### Community 5 - "Database Migrations"
Cohesion: 0.14
Nodes (7): Migration, Migration, Migration, Migration, Migration, Migration, Migration

### Community 6 - "Upload and Price Validation"
Cohesion: 0.11
Nodes (4): PubReviewForm, Meta, validate_uploaded_image_file(), SecurityAndValidationTests

### Community 8 - "Register and Post Review"
Cohesion: 0.20
Nodes (4): BrummieRegisterForm, Meta, RegisterView, ReviewCreateView

### Community 10 - "Heroku Production Stack"
Cohesion: 0.29
Nodes (6): Heroku deployment (Procfile, config vars, Postgres), dj-database-url, gunicorn, psycopg2-binary, whitenoise, Community pint & pub photo gallery

### Community 12 - "Project, Sprint and Team"
Cohesion: 0.40
Nodes (4): Sprint 1: MVP Submission (3-6 Nov 2026), Team 2 (Jamie Walker, Paul Brotheridge, manjnagra12-lgtm), The Second City Pint (Birmingham pub review site), Django>=4.2,<5.2

## Knowledge Gaps
- **13 isolated node(s):** `Team 2 (Jamie Walker, Paul Brotheridge, manjnagra12-lgtm)`, `Category model (7 venue styles)`, `True Community Averages & What's on Tap price tracker`, `Django>=4.2,<5.2`, `gunicorn` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 133 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PubReview` connect `PubReview Model` to `Pub Data Import Scripts`, `Views and Django Imports`, `Forms, Tests and Imports`, `Upload and Price Validation`, `Register and Post Review`, `GPS Distance Sorting`?**
  _High betweenness centrality (0.270) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `PubReview` (e.g. with `PubReviewForm` and `Command`) actually correct?**
  _`PubReview` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Team 2 (Jamie Walker, Paul Brotheridge, manjnagra12-lgtm)`, `Category model (7 venue styles)`, `True Community Averages & What's on Tap price tracker` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Pub Data Import Scripts` be split into smaller, more focused modules?**
  _Cohesion score 0.06610169491525424 - nodes in this community are weakly interconnected._
- **Why does `SecurityAndValidationTests` connect `Upload and Price Validation` to `Forms, Tests and Imports`, `PubReview Model`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `Comment` (e.g. with `CommentInline` and `CommentForm`) actually correct?**
  _`Comment` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Should `Views and Django Imports` be split into smaller, more focused modules?**
  _Cohesion score 0.05782312925170068 - nodes in this community are weakly interconnected._