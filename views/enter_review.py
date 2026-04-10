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

    with st.form("enter_review_form", clear_on_submit=False):
        st.markdown("### 📝 New Review")
        selected_title = st.selectbox("Movie *", movie_titles)
        name = st.text_input("Your Name *", max_chars=100)
        review = st.text_area("Review * (max 100 characters)", max_chars=100, height=100)
        rating_val = st.slider("Your Rating * (1–10)", min_value=1, max_value=10, value=7)
        date_watched = st.date_input("Date Watched *", value=date.today())
        submitted = st.form_submit_button("Preview & Confirm")

    if submitted:
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
            # Store pending submission in session state
            st.session_state["pending_review"] = {
                "movie_id": movie_map[selected_title],
                "title": selected_title,
                "name": name.strip(),
                "review": review.strip(),
                "rating": rating_val,
                "date_watched": date_watched,
            }

    # --- Confirmation step ---
    if "pending_review" in st.session_state:
        p = st.session_state["pending_review"]
        st.markdown("---")
        st.markdown("### ✅ Confirm Your Review")
        st.markdown(f"**Movie:** {p['title']}")
        st.markdown(f"**Name:** {p['name']}")
        st.markdown(f"**Review:** {p['review']}")
        st.markdown(f"**Rating:** {p['rating']}/10")
        st.markdown(f"**Date Watched:** {p['date_watched']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Submit", type="primary"):
                try:
                    db.insert_review(
                        movie_id=p["movie_id"],
                        name=p["name"],
                        review=p["review"],
                        date_watched=p["date_watched"],
                        rating=str(p["rating"])
                    )
                    st.success(f"✅ Review for **{p['title']}** submitted successfully!")
                    st.session_state.pop("pending_review", None)
                except Exception as e:
                    st.error(f"Failed to submit review: {e}")
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.pop("pending_review", None)
                st.info("Submission cancelled.")
                st.rerun()
