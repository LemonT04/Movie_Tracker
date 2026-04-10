import streamlit as st
import db
def show():
    st.title("🗑️ Delete a Review")
    st.markdown("Enter your Review ID to remove it. You will be asked to confirm before deletion.")

    user_id_input = st.number_input("Review ID", min_value=1, step=1, value=1)
    find_btn = st.button("Find Review")

    if find_btn:
        st.session_state.pop("delete_target", None)
        st.session_state.pop("delete_confirmed", None)
        try:
            row = db.get_review_by_id(int(user_id_input))
        except Exception as e:
            st.error(f"Database error: {e}")
            return

        if not row:
            st.warning(f"No review found with ID {int(user_id_input)}.")
            return

        st.session_state["delete_target"] = row

    # Show review details and confirmation
    if "delete_target" in st.session_state:
        row = st.session_state["delete_target"]
        user_id, title, name, review_text, date_watched, rating = row
        date_str = date_watched.strftime("%B %d, %Y") if date_watched else "Unknown"

        st.markdown("---")
        st.markdown("### ⚠️ Review to Delete")

        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"**🎬 {title}**")
            st.markdown(f"_{review_text}_")
        with col2:
            st.markdown(f"👤 **{name}**")
            st.markdown(f"📅 {date_str}")
        with col3:
            st.metric("Rating", f"{rating}/10")

        st.markdown("---")
        st.warning("⚠️ This action cannot be undone. Are you sure you want to delete this review?")

        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("✅ Yes, Delete It", type="primary"):
                try:
                    db.delete_review(user_id)
                    st.success(f"Review ID {user_id} has been deleted.")
                    st.session_state.pop("delete_target", None)
                except Exception as e:
                    st.error(f"Failed to delete review: {e}")
        with col_no:
            if st.button("❌ Cancel"):
                st.session_state.pop("delete_target", None)
                st.info("Deletion cancelled.")
                st.rerun()
