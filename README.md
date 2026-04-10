# 🎬 Top 100 Movies Tracker — Streamlit App

A UI that helps the user enter their review of the top 100 movies of all time. A user can filter based on genre, user reviews, movies reviewed. They can edit their reviews and also delete them based of review ID.
movie_tracker/
├── app.py                    # Main entry point & navigation
├── db.py                     # All database logic (psycopg2)
├── requirements.txt
├── setup.sql                 # Run once to create tables & seed data
├── .streamlit/
│   └── secrets.toml.example  # Copy to secrets.toml and fill in your DB_URL
└── pages/
    ├── home.py               # Home page — movie list + ratings + info
    ├── user_ratings.py       # All user reviews with filters
    ├── enter_review.py       # Submit a new review
    ├── update_review.py      # Edit an existing review by ID
    └── delete_review.py      # Delete a review with confirmation

## Pages

| Page | Description |
|------|-------------|
| 🏠 Home | Browse movies sorted by IMDb, Letterboxd, or weighted user average. Click any movie to see director, cast, description, and user reviews. |
| ⭐ User Ratings | View all reviews with filters by movie and reviewer. |
| ✍️ Enter Review | Pick a movie from the dropdown and submit a review (name, text, rating 1–10, date). |
| ✏️ Update Review | Look up a review by ID and edit it. |
| 🗑️ Delete Review | Look up a review by ID and delete it after confirmation. |

---

## Validation Rules

- All fields are required when entering or updating a review.
- The movie must already exist in the database (selected via dropdown).
- Review text must be 100 characters or fewer.
- Rating must be between 1 and 10.
