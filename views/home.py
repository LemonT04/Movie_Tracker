import streamlit as st
import db


def show():
    st.title("🎬 Top 100 Movies of All Time")
    st.markdown("Browse the highest-rated movies, filter by genre, and click a movie for full details.")

    # --- Initialize DB ---
    try:
        db.init_db()
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return

    # --- Fetch movies ---
    try:
        movies = db.get_all_movies()
    except Exception as e:
        st.error(f"Could not load movies: {e}")
        return

    if not movies:
        st.info("No movies in the database yet.")
        return

    # Build display rows with user averages
    rows = []
    for m in movies:
        movie_id, title, imdb, letterboxd, rt, date_rel, genre = m
        avg = db.get_weighted_average(movie_id)
        rows.append({
            "Movie_ID": movie_id,
            "Title": title,
            "IMDb": float(imdb) if imdb else 0,
            "Letterboxd": float(letterboxd) if letterboxd else 0,
            "Rotten Tomatoes": rt,
            "User Avg": avg if avg else 0,
            "Year": date_rel.year if date_rel else "N/A",
            "Genre": genre,
        })

    # --- Filters row ---
    col_sort, col_genre = st.columns([2, 1])

    with col_sort:
        sort_option = st.radio(
            "📊 Sort By",
            ["IMDb Rating", "Letterboxd Rating", "Weighted User Average"],
            horizontal=True
        )

    with col_genre:
        all_genres = sorted(set(
            g.strip()
            for row in rows
            for g in row["Genre"].replace("/", ",").split(",")
            if g.strip()
        ))
        selected_genre = st.selectbox("🎭 Filter by Genre", ["All Genres"] + all_genres)

    # --- Apply genre filter ---
    if selected_genre != "All Genres":
        rows = [r for r in rows if selected_genre.lower() in r["Genre"].lower()]

    # --- Sort ---
    if sort_option == "IMDb Rating":
        rows.sort(key=lambda x: x["IMDb"], reverse=True)
    elif sort_option == "Letterboxd Rating":
        rows.sort(key=lambda x: x["Letterboxd"], reverse=True)
    else:
        rows.sort(key=lambda x: x["User Avg"], reverse=True)

    # --- Summary metrics ---
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🎬 Movies Shown", len(rows))
    avg_imdb = f"{sum(r['IMDb'] for r in rows) / len(rows):.2f}" if rows else "—"
    avg_lb   = f"{sum(r['Letterboxd'] for r in rows) / len(rows):.2f}" if rows else "—"
    m2.metric("⭐ Avg IMDb", avg_imdb)
    m3.metric("🍅 Avg Letterboxd", avg_lb)
    total_reviews = sum(len(db.get_user_reviews_for_movie(r["Movie_ID"])) for r in rows)
    m4.metric("💬 Total Reviews", total_reviews)

    # --- Movie list ---
    st.markdown("---")
    st.markdown("### 🎥 Movie List — Click a Movie for Details")

    if not rows:
        st.warning(f"No movies found for genre: {selected_genre}")
        return

    for i, row in enumerate(rows):
        rank = i + 1
        label = (
            f"#{rank} {row['Title']} ({row['Year']}) | "
            f"IMDb: {row['IMDb']} | Letterboxd: {row['Letterboxd']} | "
            f"RT: {row['Rotten Tomatoes']} | Genre: {row['Genre']}"
        )
        with st.expander(label):
            info = db.get_movie_info(row["Movie_ID"])
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("#### 📊 Ratings")
                st.metric("IMDb Rating", row["IMDb"])
                st.metric("Letterboxd Rating", row["Letterboxd"])
                st.metric("Rotten Tomatoes", row["Rotten Tomatoes"])
                ua = row["User Avg"]
                st.metric("User Average", f"{ua}/10" if ua else "No reviews yet")

            with col2:
                st.markdown("#### ℹ️ Movie Info")
                if info:
                    director, a1, a2, a3, description = info
                    st.markdown(f"**Director:** {director}")
                    st.markdown(f"**Cast:** {a1}, {a2}, {a3}")
                    st.markdown(f"**Genre:** {row['Genre']}")
                    st.markdown(f"**Description:** {description}")
                else:
                    st.info("No additional info available for this movie.")

                reviews = db.get_user_reviews_for_movie(row["Movie_ID"])
                if reviews:
                    st.markdown("#### 💬 User Reviews")
                    for rev in reviews:
                        uid, name, review_text, date_w, rating = rev
                        date_str = date_w.strftime("%b %d, %Y") if date_w else "Unknown"
                        st.markdown(
                            f"- **{name}** ({date_str}) — ⭐ {rating}/10: _{review_text}_"
                        )
