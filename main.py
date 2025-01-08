import streamlit as st
from login_page import login_page
from register_page import register_page
from db_manager import init_db
from streamlit_option_menu import option_menu
from home_page import home_page

# Initialize the database
init_db()

# Streamlit Page Config
st.set_page_config(page_title = 'Agriculture', layout='wide', page_icon="🌾")

# Add background image to the main page



# Session State Initialization
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

if st.session_state["page"] == "Home":
    # Horizontal navigation for non-logged-in users
    with st.sidebar:
        selected_page = option_menu(
            menu_title=None,
            options=["Home", "Login", "Register"],
            icons=["house", "box-arrow-in-right", "person-plus"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "nav-link-selected": {
                    "background-color": "green",  # Background color of the selected item
                    "color": "white",
                },
                "nav-link": {
                    "background-color": "#d6fca7",  # Background color of unselected items
                    "color": "black",  # Text color of unselected items
                },
            },
        )
        st.image('https://www.freeiconspng.com/uploads/garden-flowers-png-12.png')

    # Render the selected page
    if selected_page == "Home":
        home_page()
    elif selected_page == "Login":
        login_page()
    elif selected_page == "Register":
        register_page()

elif st.session_state["page"] == "user_home":
    # Redirect to the user dashboard after login
    from user_home import user_home_page
    user_home_page()
