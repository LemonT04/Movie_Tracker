import streamlit as st

st.set_page_config(
    page_title="Top 100 Movies Tracker",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Navigation
pages = {
    "🏠 Home": "pages/home.py",
    "⭐ User Ratings": "pages/user_ratings.py",
    "✍️ Enter Review": "pages/enter_review.py",
    "✏️ Update Review": "pages/update_review.py",
    "🗑️ Delete Review": "pages/delete_review.py",
}

st.sidebar.title("🎬 Movie Tracker")
st.sidebar.markdown("---")
selection = st.sidebar.radio("Navigate", list(pages.keys()))

# Route to the correct page module
if selection == "🏠 Home":
    import pages.home as page
elif selection == "⭐ User Ratings":
    import pages.user_ratings as page
elif selection == "✍️ Enter Review":
    import pages.enter_review as page
elif selection == "✏️ Update Review":
    import pages.update_review as page
elif selection == "🗑️ Delete Review":
    import pages.delete_review as page

page.show()
