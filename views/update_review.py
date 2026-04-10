import streamlit as st
from datetime import date
import db


def show():
    st.title("✏️ Update a Review")
    st.markdown("Enter your Review ID to load and edit your existing review.")

    user_id_input = st.number_input("Review ID", min_value=1, step=1, value=1)
    load_btn = st.button("Load Review")

    if load_btn or "edit_review" in st.session_state:
        try:
            review_row = db.get_review_by_id(int(user_id_input))
        except Exception as e:
            st.error(f"Could not fetch review: {e}")
            return

        if not review_row:
            st.warning(f"No review found with ID {int(user_id_input)}.")
            st.session_state.pop("edit_review", None)
            return

        user_id, title, name, review_text, date_watched, rating = review_row
        st.session_state["edit_review"] = review_row
        st.info(f"Editing review for: **{title}** by **{name}**")

        with st.form("update_review_form"):
            st.markdown("### ✏️ Edit Your Review")
            new_review = st.text_area(
                "Review * (max 100 characters)",
                value=review_text,
                max_chars=100,
                height=100
            )
            new_rating = st.slider(
                "Your Rating * (1–10)",
                min_value=1, max_value=10,
                value=int(float(rating)) if rating else 5
            )
            current_date = date_watched.date() if date_watched else date.today()
            new_date = st.date_input("Date Watched *", value=current_date)
            update_btn = st.form_submit_button("Preview & Confirm")

        if update_btn:
            errors = []
            if not new_review.strip():
                errors.append("Review cannot be empty.")
            if len(new_review.strip()) > 100:
                errors.append("Review must be under 100 characters.")
            if not (1 <= new_rating <= 10):
                errors.append("Rating must be between 1 and 10.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                st.session_state["pending_update"] = {
                    "user_id": user_id,
                    "title": title,
                    "name": name,
                    "review": new_review.strip(),
                    "rating": new_rating,
                    "date_watched": new_date,
                }

    # --- Confirmation step ---
    if "pending_update" in st.session_state:
        p = st.session_state["pending_update"]
        st.markdown("---")
        st.markdown("### ✅ Confirm Your Update")
        st.markdown(f"**Movie:** {p['title']}")
        st.markdown(f"**Name:** {p['name']}")
        st.markdown(f"**Updated Review:** {p['review']}")
        st.markdown(f"**Updated Rating:** {p['rating']}/10")
        st.markdown(f"**Updated Date Watched:** {p['date_watched']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Update", type="primary"):
                try:
                    db.update_review(
                        user_id=p["user_id"],
                        review=p["review"],
                        date_watched=p["date_watched"],
                        rating=str(p["rating"])
                    )
                    st.success("✅ Review updated successfully!")
                    st.session_state.pop("pending_update", None)
                    st.session_state.pop("edit_review", None)
                except Exception as e:
                    st.error(f"Failed to update review: {e}")
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.pop("pending_update", None)
                st.info("Update cancelled.")
                st.rerun()
