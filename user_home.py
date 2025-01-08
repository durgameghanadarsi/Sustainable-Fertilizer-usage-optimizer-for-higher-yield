import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import requests
from bs4 import BeautifulSoup
user=st.session_state['user']
city=user[3]
url = "https://www.google.com/search?q=" + "weather" + city
html = requests.get(url).content
soup = BeautifulSoup(html, 'html.parser')
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
str_ = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
data = str_.split('\n')
time = data[0]
sky = data[1]
listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
strd = listdiv[5].text
pos = strd.find('Wind')
other_data = strd[pos:]
def seasonal():
    st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://static.vecteezy.com/system/resources/thumbnails/036/226/390/small_2x/ai-generated-nature-landscapes-background-free-photo.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-height: 100vh;  /* Ensure the background covers the whole screen */
            background-color: rgba(255, 255, 255, 0.7); /* Add a semi-transparent overlay */
            background-blend-mode: overlay; /* Blend the image with the overlay */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f"<h1 style='text-align: center; color:red;'>Seasonal Trend Analysis</h1>", unsafe_allow_html=True)
    st.markdown('---')
    df=pd.read_csv("Crop_recommendation.csv")
    col1, col2 = st.columns([5,5])
    district=col1.selectbox('Select District',df['District'].unique())
    season=col2.selectbox('Select Season',df['Season'].unique())   
    k=season.split('(')[0]
    df=df[(df['District']==district) & (df['Season']==k)]
    crops=df['Crop'].unique()
    k=str(k)
    crop_images=pd.read_csv('Crops.csv')
    crop_images=crop_images.set_index('Crop')
    col1, col2, col3=st.columns([10,5,10])
    if col2.button('Submit',type='primary'):
        st.markdown('---')
        col1,col2,col3=st.columns([5,5,5])
        try:
            for i in range(0,len(crops),3):
                with col1:
                    if i<len(crops):
                        st.image(crop_images.loc[crops[i],'Image'],use_column_width=True)
                        st.markdown(f"<h5 style='text-align: center; color:black;'>{crops[i]}</h5>", unsafe_allow_html=True)
                with col2:
                    if i+1<len(crops):
                        st.image(crop_images.loc[crops[i+1],'Image'],use_column_width=True)
                        st.markdown(f"<h5 style='text-align: center; color:black;'>{crops[i+1]}</h5>", unsafe_allow_html=True)
                with col3:
                    if i+2<len(crops):
                        st.image(crop_images.loc[crops[i+2],'Image'],use_column_width=True)
                        st.markdown(f"<h5 style='text-align: center; color:black;'>{crops[i+2]}</h5>", unsafe_allow_html=True)
        except:
            pass

def fertilizer():
    try:
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area */
            .main {
                background-image: url('https://eos.com/wp-content/uploads/2023/11/components-of-different-types-of-fertilizers.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                min-height: 100vh;  /* Ensure the background covers the whole screen */
                background-color: rgba(255, 255, 255, 0.8); /* Add a semi-transparent overlay */
                background-blend-mode: overlay; /* Blend the image with the overlay */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(f"<h1 style='text-align: center; color:blue;'>Fertilizer Recommendation System</h1>", unsafe_allow_html=True)
        st.markdown('---')
        fertilizer=['10-10-10','10-26-26','14-14-14','14-35-14','15-15-15','17-17-17','20-20','28-28','DAP','Potassium chloride','Potassium sulfate.','Superphosphate','TSP','Urea']
        soil=['Black','Clayey','Loamy','Red','Sandy']
        crop=['Barley','Cotton','Ground Nuts','Maize','Millets','Oil seeds','Paddy','Pulses','Sugarcane','Tobacco','Wheat','coffee','kidneybeans','orange','pomegranate','rice','watermelon']
        col1, col2,col3= st.columns([5,5,5])
        user=st.session_state['user']
        location=user[3]
        a=temp.split('°')[0]
        humd=other_data.find('°')
        b=other_data[humd-3:humd]
        if b=='':
            b=float(64.98)
        col1,col2,col3= st.columns([5,5,5])
        with col1:
            c=st.number_input('Moisture',min_value=10,max_value=100.0,value=42.8)
        with col2:
            d=st.selectbox('Soil Type',('Black','Clayey','Loamy','Red','Sandy'))
        with col3:
            e=st.selectbox('Crop Type',('Barley','Cotton','Ground Nuts','Maize','Millets','Oil seeds','Paddy','Pulses','Sugarcane','Tobacco','Wheat','coffee','kidneybeans','orange','pomegranate','rice','watermelon'))
        col1, col2,col3= st.columns([5,5,5])
        with col1:
            f=st.number_input('Enter N',min_value=0,max_value=126,value=10)
        with col2:
            g=st.number_input('Enter P',min_value=0,max_value=54,value=7)
        with col3:
            h=st.number_input('Enter K',min_value=0,max_value=59,value=8)
        
        col4, col5, col6 = st.columns([12,5,10])
        if col5.button('Predict',type='primary'):
            col1, col2, col3 = st.columns(3)
            data = np.array([[a,b,c,soil.index(d),crop.index(e),f,g,h]])
            model=pickle.load(open('classifier.pkl','rb'))
            res=model.predict(data)
            d1=pd.read_csv('fertilizer.csv')
            #get the image of the fertilizer
            d1=d1.set_index('fertilizer')
            col1,col2,col3=st.columns([5,5,5])
            col2.image(d1.loc[fertilizer[res[0]],'image'],width=300)
    except:
        pass
def user_home_page():
    # Navigation menu for user dashboard

    with st.sidebar:
        st.markdown(f"<h1 style='text-align: center; color: black;'><b>🏡Dashboard</b></h1>", unsafe_allow_html=True)

        selected_tab = option_menu(
            menu_title=None,
            options=["Seasonal Based Crops", "Fertilizers",'Logout'],
            icons=['apple','bucket','file-lock2'], menu_icon="cast", default_index=0,
        styles={
        "nav-link-selected": {"background-color": "green", "color": "white", "border-radius": "5px"},
        }
        )
        user=st.session_state['user']
        location=user[3]
        col1,col2=st.columns([1,1])
        col1.markdown(f"<h1 style='text-align: center; color:black;'>{temp}🌞</h1>", unsafe_allow_html=True)
        col2.markdown(f"<h1 style='text-align: center; color:black;'>{sky}🌥️</h1>", unsafe_allow_html=True)

    if selected_tab == "Seasonal Based Crops":
        seasonal()
    elif selected_tab == "Fertilizers":
        fertilizer()
    elif selected_tab=='Logout':
        # Logout functionality
        st.session_state.clear()  # Clear session state to "log out"
        st.experimental_rerun()
