import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def seasonal():
    st.markdown(f"<h1 style='text-align: center; color:red;'>Seasonal Trend Analysis</h1>", unsafe_allow_html=True)
    st.markdown('---')
    df=pd.read_csv("Crop_recommendation.csv")
    features = df[['N', 'P','K','temperature', 'humidity', 'ph', 'rainfall']]
    target = df['label']
    labels = df['label']
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)
    RF = RandomForestClassifier(n_estimators=25, random_state=42)
    RF.fit(Xtrain,Ytrain)
    col1, col2,col3= st.columns([5,5,5])
    with col1:
        a=st.number_input('Enter N')
    with col2:
        b=st.number_input('Enter P')
    with col3:
        c1=st.number_input('Enter K')
    col1, col2,col3,col4= st.columns([5,5,5,5])
    with col1:
        d=st.number_input('Temperature °C')
    with col2:
        e=st.number_input('Humidity %')
    with col3:
        f=st.number_input('pH')
    with col4:
        g=st.number_input('Rainfall mm')
    data = np.array([[a,b,c1,d,e,f,g]])
    prediction = RF.predict(data)
    col4, col5, col6 = st.columns([12,5,10])
    if col5.button('Predict'):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            if prediction[0]=='apple':
                st.image("images/apple.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Apple</h5>", unsafe_allow_html=True)
            if prediction[0]=='banana':
                st.image("images/banana.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Banana</h5>", unsafe_allow_html=True)
            if prediction[0]=='blackgram':
                st.image("images/blackgram.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Blackgram</h5>", unsafe_allow_html=True)
            if prediction[0]=='chickpea':
                st.image("images/chickpea.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Chickpea</h5>", unsafe_allow_html=True)
            if prediction[0]=='coconut':
                st.image("images/coconut.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Coconut</h5>", unsafe_allow_html=True)
            if prediction[0]=='coffee':
                st.image("images/coffee.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Coffee</h5>", unsafe_allow_html=True)
            if prediction[0]=='cotton':
                st.image("images/cotton.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Cotton</h5>", unsafe_allow_html=True)
            if prediction[0]=='grapes':
                st.image("images/grapes.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Grapes</h5>", unsafe_allow_html=True)
            if prediction[0]=='jute':
                st.image("images/jute.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Jute</h5>", unsafe_allow_html=True)
            if prediction[0]=='kidneybeans':
                st.image("images/kidneybeans.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Kidneybeans</h5>", unsafe_allow_html=True)
            if prediction[0]=='lentil':
                st.image("images/lentil.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Letil</h5>", unsafe_allow_html=True)
            if prediction[0]=='maize':
                st.image("images/maize.jpeg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Maize</h5>", unsafe_allow_html=True)
            if prediction[0]=='mango':
                st.image("images/mango.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Mango</h5>", unsafe_allow_html=True)
            if prediction[0]=='mothbeans':
                st.image("images/mothbeans.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Mothbeans</h5>", unsafe_allow_html=True)
            if prediction[0]=='mungbean':
                st.image("images/mungbeans.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Mungbeans</h5>", unsafe_allow_html=True)
            if prediction[0]=='muskmelon':
                st.image("images/muskmelon.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Muskmelon</h5>", unsafe_allow_html=True)
            if prediction[0]=='orange':
                st.image("images/orange.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Orange</h5>", unsafe_allow_html=True)
            if prediction[0]=='papaya':
                st.image("images/papaya.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Papaya</h5>", unsafe_allow_html=True)
            if prediction[0]=='pomegranate':
                st.image("images/pomegranate.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Ponogranate</h5>", unsafe_allow_html=True)
            if prediction[0]=='pigeonpeas':
                st.image("images/pigeonpeas.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Piegonpeas</h5>", unsafe_allow_html=True)
            if prediction[0]=='rice':
                st.image("images/rice.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Rice</h5>", unsafe_allow_html=True)
            if prediction[0]=='watermelon':
                st.image("images/watermelon.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>Watermelon</h5>", unsafe_allow_html=True)
        with col3:
            st.write(' ')
def fertilizer():
    st.markdown(f"<h1 style='text-align: center; color:blue;'>Fertilizer Recommendation System</h1>", unsafe_allow_html=True)
    st.markdown('---')
    data = pd.read_csv('Fertilizer Prediction.csv')
    data.rename(columns={'Humidity ':'Humidity','Soil Type':'Soil_Type','Crop Type':'Crop_Type','Fertilizer Name':'Fertilizer'},inplace=True)
    from sklearn.preprocessing import LabelEncoder
    encode_soil = LabelEncoder()
    data.Soil_Type = encode_soil.fit_transform(data.Soil_Type)
    Soil_Type = pd.DataFrame(zip(encode_soil.classes_,encode_soil.transform(encode_soil.classes_)),columns=['Original','Encoded'])
    Soil_Type = Soil_Type.set_index('Original')
    encode_crop = LabelEncoder()
    data.Crop_Type = encode_crop.fit_transform(data.Crop_Type)
    Crop_Type = pd.DataFrame(zip(encode_crop.classes_,encode_crop.transform(encode_crop.classes_)),columns=['Original','Encoded'])
    Crop_Type = Crop_Type.set_index('Original')
    encode_ferti = LabelEncoder()
    data.Fertilizer = encode_ferti.fit_transform(data.Fertilizer)
    Fertilizer = pd.DataFrame(zip(encode_ferti.classes_,encode_ferti.transform(encode_ferti.classes_)),columns=['Original','Encoded'])
    Fertilizer = Fertilizer.set_index('Original')
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(data.drop('Fertilizer',axis=1),data.Fertilizer,test_size=0.2,random_state=1)
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    from sklearn.ensemble import RandomForestClassifier
    soil=['Black','Clayey','Loamy','Red','Sandy']
    crop=['Barley','Cotton','Ground Nuts','Maize','Millets','Oil seeds','Paddy','Pulses','Sugarcane','Tobacco','Wheat']
    fert=['10-26-26','14-35-14','17-17-17','20-20','28-28','DAP','Urea']
    rand = RandomForestClassifier(n_estimators=30,random_state=42)
    pred_rand = rand.fit(x_train,y_train).predict(x_test)
    col1, col2,col3= st.columns([5,5,5])
    with col1:
        a=st.number_input('Temperature °C')
    with col2:
        b=st.number_input('Humidity %')
    with col3:
        c=st.number_input('Moisture')
    col1,col2= st.columns([5,5])
    with col1:
        d=st.selectbox('Soil Type',('Black','Clayey','Loamy','Red','Sandy'))
    with col2:
        e=st.selectbox('Crop Type',('Barley','Cotton','Ground Nuts','Maize','Millets','Oil seeds','Paddy','Pulses','Sugarcane','Tobacco','Wheat'))
    col1, col2,col3= st.columns([5,5,5])
    with col1:
        f=st.number_input('Enter N')
    with col2:
        g=st.number_input('Enter P')
    with col3:
        h=st.number_input('Enter K')
    data = np.array([[a,b,c,soil.index(d),crop.index(e),f,g,h]])
    prediction = rand.predict(data)
    res=fert[prediction[0]]
    col4, col5, col6 = st.columns([12,5,10])
    if col5.button('Predict'):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            if res=='10-26-26':
                st.image("images/10-26-26.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>10-26-26</h5>", unsafe_allow_html=True)
            if res=='14-35-14':
                st.image("images/14-35-14.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>14-35-14</h5>", unsafe_allow_html=True)
            if res=='17-17-17':
                st.image("images/17-17-17.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>17-17-17</h5>", unsafe_allow_html=True)
            if res=='20-20':
                st.image("images/20-20.jpg")
                st.markdown(f"<h5 style='text-align: center; color:black;'>20-20</h5>", unsafe_allow_html=True)
            if res=='28-28':
                st.image("images/28-28.jpg")
                st.write('28-28')
                st.markdown(f"<h5 style='text-align: center; color:black;'>28-28</h5>", unsafe_allow_html=True)
            if res=='DAP':
                st.image("images/DAP.jpg")
                st.write('DAP')
                st.markdown(f"<h5 style='text-align: center; color:black;'>DAP</h5>", unsafe_allow_html=True)
            if res=='Urea':
                st.image("images/Urea.jpg")
                st.write('Urea')
                st.markdown(f"<h5 style='text-align: center; color:black;'>Urea</h5>", unsafe_allow_html=True)
        with col3:
            st.write(' ')
def user_home_page():
    # Navigation menu for user dashboard
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-image: url('');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        min-height: 100vh;  /* Ensure the background covers the whole screen */
    }
    </style>
    """,
    unsafe_allow_html=True
)

    with st.sidebar:
        selected_tab = option_menu(
            menu_title=None,
            options=["Seasonal Based Crops", "Fertilizers",'Logout'],
            icons=['apple','bucket','file-lock2'], menu_icon="cast", default_index=0,
        styles={
        "nav-link-selected": {"background-color": "green", "color": "white", "border-radius": "5px"},
        }
        )
    if selected_tab == "Seasonal Based Crops":
        seasonal()
    elif selected_tab == "Fertilizers":
        fertilizer()
    elif selected_tab=='Logout':
        # Logout functionality
        st.session_state.clear()  # Clear session state to "log out"
        st.experimental_rerun()