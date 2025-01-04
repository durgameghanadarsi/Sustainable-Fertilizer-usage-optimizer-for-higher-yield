import streamlit as st

def home_page():
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
            <img src="https://media2.giphy.com/media/IfsxP5r7WmhP5P6seN/giphy.gif?cid=6c09b952o7a4fgdk41h4cbnu9cdl00zq5fyej4d5yslelutf&ep=v1_gifs_search&rid=giphy.gif&ct=g" style="max-width: 100%;">
        </div>
        """,
        unsafe_allow_html=True
    )
