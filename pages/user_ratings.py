import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import db


def show():
    st.title("⭐ User Ratings")
    st.markdown("See all reviews submitted by users across every movie.")

    try:
        reviews = db.get_all_user_reviews()
    except Exception as e:
        st.error(f"Could not load reviews: {e}")
        return

    if not reviews:
        st.info("No user reviews yet. Be the first to submit one!")
        return

    # Filter by movie
    movie_titles = sorted(set(r[1] for r in reviews))
    filter_movie = st.selectbox("Filter by Movie (optional)", ["All Movies"] + movie_titles)

    # Filter by name
    names = sorted(set(r[2] for r in reviews))
    filter_name = st.selectbox("Filter by Reviewer (optional)", ["All Reviewers"] + names)

    filtered = reviews
    if filter_movie != "All Movies":
        filtered = [r for r in filtered if r[1] == filter_movie]
    if filter_name != "All Reviewers":
        filtered = [r for r in filtered if r[2] == filter_name]

    st.markdown(f"**{len(filtered)} review(s) found.**")
    st.markdown("---")

    for r in filtered:
        user_id, title, name, review_text, date_watched, rating = r
        date_str = date_watched.strftime("%B %d, %Y") if date_watched else "Unknown date"

        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**🎬 {title}**")
                st.markdown(f"_{review_text}_")
            with col2:
                st.markdown(f"👤 **{name}**")
                st.markdown(f"📅 Watched: {date_str}")
            with col3:
                st.metric("Rating", f"{rating}/10")
            st.markdown("---")
