import streamlit as st

def home_page():
    st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvdjkzOS1udW5ueS0wMi5qcGc.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-height: 100vh;  /* Ensure the background covers the whole screen */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Sustainable Fertilizer Usage Optimizer for Higher Yield</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Center the image
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://assets-v2.lottiefiles.com/a/43aff328-ee85-11ee-b1b3-43aa48f22991/Kk6fZSgixc.png", width="500">
        </div>
        """,
        unsafe_allow_html=True
    )
