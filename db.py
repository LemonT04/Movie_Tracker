import psycopg2
import streamlit as st
from contextlib import contextmanager


@st.cache_resource
def get_connection():
    """Create a cached database connection."""
    return psycopg2.connect(st.secrets["DB_URL"])


@contextmanager
def get_cursor():
    """Context manager for database cursor with auto-commit."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def init_db():
    """Initialize database tables if they don't exist."""
    with get_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Top_100_Movies (
                Movie_ID SERIAL PRIMARY KEY,
                Title VARCHAR(100) NOT NULL,
                IMDB VARCHAR(20) NOT NULL,
                Letterboxd VARCHAR(20) NOT NULL,
                Rotten_Tomatoes VARCHAR(20) NOT NULL,
                Date_Released TIMESTAMP NOT NULL,
                Genre VARCHAR(100) NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Movie_Info (
                Info_ID SERIAL PRIMARY KEY,
                Movie_ID INTEGER NOT NULL REFERENCES Top_100_Movies(Movie_ID) ON DELETE CASCADE,
                Director VARCHAR(100) NOT NULL,
                Actor1 VARCHAR(100) NOT NULL,
                Actor2 VARCHAR(100) NOT NULL,
                Actor3 VARCHAR(100) NOT NULL,
                Description VARCHAR(500) NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS User_Info (
                User_ID SERIAL PRIMARY KEY,
                Movie_ID INTEGER NOT NULL REFERENCES Top_100_Movies(Movie_ID) ON DELETE CASCADE,
                Name VARCHAR(100) NOT NULL,
                Review VARCHAR(100) NOT NULL,
                Date_Watched TIMESTAMP DEFAULT NOW(),
                Rating VARCHAR(20) NOT NULL
            );
        """)


def get_all_movies():
    """Fetch all movies ordered by IMDB rating descending."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT Movie_ID, Title, IMDB, Letterboxd, Rotten_Tomatoes,
                   Date_Released, Genre
            FROM Top_100_Movies
            ORDER BY CAST(IMDB AS FLOAT) DESC NULLS LAST;
        """)
        return cur.fetchall()


def get_movie_titles():
    """Return list of (Movie_ID, Title) tuples for dropdowns."""
    with get_cursor() as cur:
        cur.execute("SELECT Movie_ID, Title FROM Top_100_Movies ORDER BY Title;")
        return cur.fetchall()


def get_movie_info(movie_id):
    """Fetch info record for a given movie."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT Director, Actor1, Actor2, Actor3, Description
            FROM Movie_Info WHERE Movie_ID = %s;
        """, (movie_id,))
        return cur.fetchone()


def get_all_user_reviews():
    """Fetch all user reviews joined with movie titles."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT u.User_ID, m.Title, u.Name, u.Review,
                   u.Date_Watched, u.Rating
            FROM User_Info u
            JOIN Top_100_Movies m ON u.Movie_ID = m.Movie_ID
            ORDER BY u.Date_Watched DESC;
        """)
        return cur.fetchall()


def get_user_reviews_for_movie(movie_id):
    """Fetch all user reviews for a specific movie."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT User_ID, Name, Review, Date_Watched, Rating
            FROM User_Info WHERE Movie_ID = %s
            ORDER BY Date_Watched DESC;
        """, (movie_id,))
        return cur.fetchall()


def get_weighted_average(movie_id):
    """Calculate weighted average of user ratings for a movie."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT AVG(CAST(Rating AS FLOAT))
            FROM User_Info
            WHERE Movie_ID = %s
              AND Rating ~ '^[0-9]+(\\.[0-9]+)?$';
        """, (movie_id,))
        result = cur.fetchone()
        return round(result[0], 2) if result and result[0] else None


def insert_review(movie_id, name, review, date_watched, rating):
    """Insert a new user review."""
    with get_cursor() as cur:
        cur.execute("""
            INSERT INTO User_Info (Movie_ID, Name, Review, Date_Watched, Rating)
            VALUES (%s, %s, %s, %s, %s);
        """, (movie_id, name, review, date_watched, rating))


def update_review(user_id, review, date_watched, rating):
    """Update an existing user review."""
    with get_cursor() as cur:
        cur.execute("""
            UPDATE User_Info
            SET Review = %s, Date_Watched = %s, Rating = %s
            WHERE User_ID = %s;
        """, (review, date_watched, rating, user_id))


def delete_review(user_id):
    """Delete a user review by ID."""
    with get_cursor() as cur:
        cur.execute("DELETE FROM User_Info WHERE User_ID = %s;", (user_id,))


def get_review_by_id(user_id):
    """Fetch a single review by User_ID."""
    with get_cursor() as cur:
        cur.execute("""
            SELECT u.User_ID, m.Title, u.Name, u.Review,
                   u.Date_Watched, u.Rating
            FROM User_Info u
            JOIN Top_100_Movies m ON u.Movie_ID = m.Movie_ID
            WHERE u.User_ID = %s;
        """, (user_id,))
        return cur.fetchone()
