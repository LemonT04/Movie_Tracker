# 🎬 Top 100 Movies Tracker — Streamlit App

A multi-page Streamlit application connected to a PostgreSQL database for tracking and reviewing the top 100 movies of all time.

---

## Project Structure

```
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
```

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection
Copy the example secrets file and fill in your PostgreSQL connection string:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Edit `.streamlit/secrets.toml`:
```toml
DB_URL = "postgresql://username:password@host:5432/your_database"
```

### 3. Create Tables & Seed Data
Run `setup.sql` against your PostgreSQL database:
```bash
psql $DATABASE_URL -f setup.sql
```

### 4. Run the App
```bash
streamlit run app.py
```

---

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
