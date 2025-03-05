import streamlit as st
import pandas as pd
from db_manager import validate_user,update_password

email=st.text_input('Email')
password=st.text_input('Password',type='password')
confirm_password=st.text_input('Confirm Password',type='password')

if st.button('Change Password'):
    if validate_user(email,password):
        if password==confirm_password:
            update_password(email,password)
            st.success('Password Changed Successfully')
        else:
            st.error('Password and Confirm Password should be same')
    else:
        st.error('Invalid Email or Password')