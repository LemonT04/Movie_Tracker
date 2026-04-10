import streamlit as st
import db
def show():
    st.title("🎬 Top 100 Movies of All Time")
    st.markdown("Browse the highest-rated movies, explore ratings, and click a movie for full details.")

    # --- Initialize DB ---
    try:
        db.init_db()
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return

    # --- Sort selector ---
    st.markdown("### 📊 Sort By")
    sort_option = st.radio(
        "Choose how to rank movies:",
        ["IMDb Rating", "Letterboxd Rating", "Weighted User Average"],
        horizontal=True
    )

    # --- Fetch movies ---
    try:
        movies = db.get_all_movies()
    except Exception as e:
        st.error(f"Could not load movies: {e}")
        return

    if not movies:
        st.info("No movies in the database yet. Ask your administrator to seed the movie list.")
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

    # Sort
    if sort_option == "IMDb Rating":
        rows.sort(key=lambda x: x["IMDb"], reverse=True)
    elif sort_option == "Letterboxd Rating":
        rows.sort(key=lambda x: x["Letterboxd"], reverse=True)
    else:
        rows.sort(key=lambda x: x["User Avg"], reverse=True)

    # --- Movie info expander ---
    st.markdown("---")
    st.markdown("### 🎥 Movie List — Click a Movie for Details")

    for i, row in enumerate(rows):
        rank = i + 1
        label = (
            f"**#{rank} {row['Title']}** ({row['Year']}) | "
            f"IMDb: {row['IMDb']} | Letterboxd: {row['Letterboxd']} | "
            f"RT: {row['Rotten Tomatoes']} | User Avg: {row['User Avg'] if row['User Avg'] else '—'} | "
            f"Genre: {row['Genre']}"
        )
        with st.expander(label):
            info = db.get_movie_info(row["Movie_ID"])
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("#### 🎬 Ratings")
                st.metric("IMDb", row["IMDb"])
                st.metric("Letterboxd", row["Letterboxd"])
                st.metric("Rotten Tomatoes", row["Rotten Tomatoes"])
                ua = row["User Avg"]
                st.metric("User Average", f"{ua}/10" if ua else "No reviews yet")

            with col2:
                st.markdown("#### ℹ️ Movie Info")
                if info:
                    director, a1, a2, a3, description = info
                    st.markdown(f"**Director:** {director}")
                    st.markdown(f"**Cast:** {a1}, {a2}, {a3}")
                    st.markdown(f"**Description:** {description}")
                else:
                    st.info("No additional info available for this movie.")

            # Show user reviews for this movie
            reviews = db.get_user_reviews_for_movie(row["Movie_ID"])
            if reviews:
                st.markdown("#### 💬 User Reviews")
                for rev in reviews:
                    uid, name, review_text, date_w, rating = rev
                    date_str = date_w.strftime("%b %d, %Y") if date_w else "Unknown"
                    st.markdown(
                        f"- **{name}** ({date_str}) — ⭐ {rating}/10: _{review_text}_"
                    )
