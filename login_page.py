import streamlit as st
from db_manager import validate_user

def login_page():
    st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L3Vwd2s2MTg0MDYxNC13aWtpbWVkaWEtaW1hZ2Uta293YzJxMmMuanBn.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-height: 100vh;  /* Ensure the background covers the whole screen */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Center the login form using Streamlit form layout
    with st.form(key="login_form"):
        # Title
        st.title("Login🔓")

        # Email and Password inputs
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # Submit button inside the form
        login_button = st.form_submit_button("Login",type='primary')

        # Handling form submission
        if login_button:
            user = validate_user(email, password)
            if user:
                # Set session state to user_home and store user details
                st.session_state["page"] = "user_home"
                st.session_state["user"] = user  # Store user info (e.g., name, email)
                st.session_state["user_tab"] = "Loan Page"  # Default tab after login
                st.experimental_rerun()
            else:
                st.error("Invalid Email or Password!")
