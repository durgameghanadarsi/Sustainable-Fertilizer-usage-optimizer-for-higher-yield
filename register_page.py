import streamlit as st
import re
from db_manager import register_user
import requests
from bs4 import BeautifulSoup
import pyowm
owm = pyowm.OWM('11081b639d8ada3e97fc695bcf6ddb20')

def register_page():

    st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://t4.ftcdn.net/jpg/03/11/73/01/360_F_311730118_ezoi92RU1WvSk4hRDkS4R7r4f4wg6MWb.webp');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.6);
            background-blend-mode: overlay;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Center the registration form container using Streamlit form layout
    col,col2,col3=st.columns([2,4,2])

    with col2.form(key="register_form"):
        # Title
        st.title("Sign Up🔐")

        # Form Fields
        col1,col2=st.columns(2)
        name = col1.text_input("Name")
        email = col2.text_input("Email")
        col1,col2=st.columns(2)
        location = col1.text_input("Location📍")
        language=col2.selectbox('Select Language',['English','Telugu'])
        otp=None
        col1, col2 = st.columns(2)
        password = col1.text_input("Password", type="password")
        retype_password = col2.text_input("Retype Password", type="password")

        # Submit Button inside the form
        register_button = st.form_submit_button("Register",type='primary')

        # Handling form submission
        if register_button:
            try:
                mgr = owm.weather_manager()
                observation = mgr.weather_at_place(location)
                weather = observation.weather
                temp = weather.temperature('celsius')['temp']
                humd = weather.humidity
                sky = weather.detailed_status
                rain = weather.rain.get('1h', 0)
            except:
                temp=25
                humd=50
                sky='Snow'
                rain=100
            # Validate email using regex
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                st.error("Invalid Email!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long!")
            elif password != retype_password:
                st.error("Passwords do not match!")
            else:
                if register_user(name, email,location,temp,humd,sky,rain,otp,language, password):
                    st.markdown(
                        """
                        <div style="text-align: center; padding: 1px; background-color: green; border-radius: 1px; border: 1.5px solid black; margin-bottom: 20px;">
                            <p style="color: black; font-size: 20px;"><b>Registration Successful! Please login to continue.</b></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div style="text-align: center; padding: 1px; background-color: red; border-radius: 1px; border: 1.5px solid black; margin-bottom: 20px;">
                            <p style="color: black; font-size: 20px;"><b>Registration Failed! Email already exists.</b></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
