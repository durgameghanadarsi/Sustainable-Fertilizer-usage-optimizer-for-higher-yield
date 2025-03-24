import streamlit as st
from streamlit_option_menu import option_menu
from db_manager import change_location, fetch_details
from english import englih_page
from telugu import telugu_page
def user_home_page():
    # Navigation menu for user dashboard
    user=st.session_state['user']
    user=fetch_details(user[2])
    if user[9]=='English':
        englih_page()
    if user[9]=='Telugu':
        telugu_page()



