import streamlit as st
import random
from db_manager import validate_user, fetch_otp, update_otp
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_alert_email(to_email, subject, message, from_email, from_password):
    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        # Connect to the server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        pass
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
    col, col2, col3 = st.columns([2, 4, 2])
    with col2:
        if "otp_sent" not in st.session_state:
            st.session_state["otp_sent"] = False
        if "email" not in st.session_state:
            st.session_state["email"] = None
        if "otp_verified" not in st.session_state:
            st.session_state["otp_verified"] = False

        if not st.session_state["otp_sent"]:  # Login Form
            with st.form(key="login_form"):
                st.title("Login🔓")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Login", type='primary')

                if login_button:
                    user = validate_user(email, password)
                    if user:
                        otp = random.randint(1000, 9999)
                        to_email=email
                        subject = "OTP for Sustainable Fertilizer Usage"
                        body = f"Hello,\n\nYour OTP is {otp}. Please enter this OTP to login.\n\nRegards,\nTeam Sustainable Fertilizer Usage"
                        from_email = 'dont.reply.mail.mail@gmail.com'
                        from_password = 'ekdbgizfyaiycmkv'  
                        # Send the alert email
                        send_alert_email(to_email, subject, body, from_email, from_password)
                        update_otp(email, otp)
                        st.success("OTP Sent to your email. Please enter the OTP to login.")
                        st.session_state["otp_sent"] = True
                        st.session_state["email"] = email
                        st.session_state["user"] = user
                        st.experimental_rerun()  # Rerun script to show OTP form
                    else:
                        st.error("Invalid Email or Password!")

        else:  # OTP Verification Form
            with st.form(key="otp_form"): 
                st.title("Enter OTP")
                otp_input = st.text_input("Enter OTP")
                submit_button = st.form_submit_button("Submit", type='primary')
                stored_otp = fetch_otp(st.session_state["email"])[0]
                if submit_button and otp_input:
                    if otp_input:
                        st.success("Login Successful!")
                        st.session_state["otp_verified"] = True
                        st.session_state["page"] = "user_home"
                        st.experimental_rerun()
                    else:
                        st.error("Invalid OTP! Try again.")

        # Redirect after OTP verification
        if st.session_state.get("otp_verified"):
            st.experimental_rerun()
