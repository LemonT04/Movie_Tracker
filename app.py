import streamlit as st

st.set_page_config(
    page_title="Top 100 Movies Tracker",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🎬 Movie Tracker")
st.sidebar.markdown("---")

selection = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "⭐ User Ratings",
    "✍️ Enter Review",
    "✏️ Update Review",
    "🗑️ Delete Review",
])

if selection == "🏠 Home":
    from views import home as page
elif selection == "⭐ User Ratings":
    from views import user_ratings as page
elif selection == "✍️ Enter Review":
    from views import enter_review as page
elif selection == "✏️ Update Review":
    from views import update_review as page
elif selection == "🗑️ Delete Review":
    from views import delete_review as page

page.show()
