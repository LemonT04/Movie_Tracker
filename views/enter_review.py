import streamlit as st

from datetime import date

import db
def show():
    st.title("✍️ Enter a Review")
    st.markdown("Select a movie from the list and share your thoughts.")

    try:
        movie_options = db.get_movie_titles()
    except Exception as e:
        st.error(f"Could not load movies: {e}")
        return

    if not movie_options:
        st.warning("No movies are available in the system yet.")
        return

    movie_map = {title: mid for mid, title in movie_options}
    movie_titles = list(movie_map.keys())

    with st.form("enter_review_form", clear_on_submit=True):
        st.markdown("### 📝 New Review")

        selected_title = st.selectbox("Movie *", movie_titles)
        name = st.text_input("Your Name *", max_chars=100)
        review = st.text_area("Review * (max 100 characters)", max_chars=100, height=100)
        rating_val = st.slider("Your Rating * (1–10)", min_value=1, max_value=10, value=7)
        date_watched = st.date_input("Date Watched *", value=date.today())

        submitted = st.form_submit_button("Submit Review")

    if submitted:
        # Validation
        errors = []
        if not name.strip():
            errors.append("Name is required.")
        if not review.strip():
            errors.append("Review is required.")
        if len(review.strip()) > 100:
            errors.append("Review must be under 100 characters.")
        if not (1 <= rating_val <= 10):
            errors.append("Rating must be between 1 and 10.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            try:
                movie_id = movie_map[selected_title]
                db.insert_review(
                    movie_id=movie_id,
                    name=name.strip(),
                    review=review.strip(),
                    date_watched=date_watched,
                    rating=str(rating_val)
                )
                st.success(f"✅ Review for **{selected_title}** submitted successfully!")
            except Exception as e:
                st.error(f"Failed to submit review: {e}")
