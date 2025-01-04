import streamlit as st
import re
from db_manager import register_user

def register_page():
    # Center the registration form container using Streamlit form layout
    with st.form(key="register_form"):
        # Title
        st.title("Register Page")

        # Form Fields
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        retype_password = st.text_input("Retype Password", type="password")

        # Submit Button inside the form
        register_button = st.form_submit_button("Register")

        # Handling form submission
        if register_button:
            # Validate email using regex
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                st.error("Invalid Email!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long!")
            elif password != retype_password:
                st.error("Passwords do not match!")
            else:
                if register_user(name, email, password):
                    st.success("Registration Successful!")
                else:
                    st.error("Email already exists!")
