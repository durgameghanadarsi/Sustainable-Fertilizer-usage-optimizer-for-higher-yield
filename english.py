import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import joblib
import gdown
import pyowm
import tensorflow as tf
owm = pyowm.OWM('11081b639d8ada3e97fc695bcf6ddb20')
from sklearn.ensemble import RandomForestRegressor
from db_manager import change_location, fetch_details,add_fertilizer,fetch_fertilizer  
# Load the trained model
# Load the trained model
def download_and_load_model():
    try:
        file_id = '1y_epR8Az7lEzsbjJa0HELNFCmauBvsVU'  # Replace with your file ID
        url = f'https://drive.google.com/uc?id={file_id}'
        output = 'model.h5'
        gdown.download(url, output, quiet=False)

        # Load the model from the file
        SoilNet = tf.keras.models.load_model('model.h5')
        return SoilNet
    except Exception as e:
        return None

SoilNet = download_and_load_model()
import requests
YOUTUBE_API_KEY = "AIzaSyCAvohp0JoAHgOy7ec_gdSISpzImyMFpUo"

def fetch_youtube_videos(query, max_results=6):
    url = f"https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'key': YOUTUBE_API_KEY,
        'maxResults': max_results
    }
    response = requests.get(url, params=params)
    videos = []
    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            videos.append({'video_id': video_id, 'title': video_title})
    return videos

yield_model = 'yield_prediction_model.pkl'
model_yield = joblib.load(yield_model)
user=st.session_state['user']
user=fetch_details(user[2])
city=user[3]
temp=user[4]
humd=user[5]
sky=user[6]
rain=user[7]
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
        user=fetch_details(user[2])
        location=user[3]
        mail=user[2]
        a=temp
        b=humd

        col1,col2,col3= st.columns([5,5,5])
        with col1:
            c=st.number_input('Moisture',min_value=1,max_value=100,value=42)
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
            model_1=pickle.load(open('classifier.pkl','rb'))
            res=model_1.predict(data)
            d1=pd.read_csv('fertilizer.csv')
            #get the image of the fertilizer
            d1=d1.set_index('fertilizer')
            col1,col2,col3=st.columns([5,5,5])
            add_fertilizer(mail,fertilizer[res[0]])
            col2.image(d1.loc[fertilizer[res[0]],'image'],width=300,caption=fertilizer[res[0]])
    except Exception as e:
        st.write(e)
def yield_prediction():
    # Load the dataset
        data = pd.read_csv('crop_data.csv') 
        X = data.drop(['CROP_PRICE', 'CROP'], axis=1)  # Features
        y = data['CROP_PRICE']  # Target variable

        # One-hot encoding for categorical variables
        X = pd.get_dummies(X)
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area with transparency */
            .main {
                background-image: url('https://img.freepik.com/free-photo/detail-rice-plant-sunset-valencia-with-plantation-out-focus-rice-grains-plant-seed_181624-25838.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-color: rgba(255, 255, 255, 0.8); /* Add a semi-transparent overlay */
                background-blend-mode: overlay; /* Blend the image with the overlay */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f"<h1 style='text-align: center; color:green;'>Crop Yield Prediction</h1>", unsafe_allow_html=True)
        input=st.selectbox("Select State",('Andaman and Nicobar Islands', 'Andhra Pradesh',
        'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
        'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
        'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala',
        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
        'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
        'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            a=st.number_input('Enter N',min_value=0,max_value=126,value=10)
        with col2:
            b=st.number_input('Enter P',min_value=0,max_value=54,value=7)
        with col3:
            c1=st.number_input('Enter K',min_value=0,max_value=59,value=8)
        with col4:
            soil_type=st.selectbox("Select Soil Type",('Alluvial', 'Black', 'Clayey', 'Loamy', 'Red', 'Sandy', 'Silt'))

        d=temp
        e=humd
        col1, col2, col3, col4 = st.columns(4)
        f=7
        g=rain
        col1,col2=st.columns([1,1])
        area=col1.number_input('Enter Area in Hectares',min_value=0.1,max_value=100.0,value=1.0)
        crop_name=col2.selectbox('Crop',['Barley','Cotton','Ground Nuts','Maize','Millets','Oil seeds','Paddy','Pulses','Sugarcane','Tobacco','Wheat','coffee','kidneybeans','orange','pomegranate','rice','watermelon'])
        new_data = pd.DataFrame({
        'STATE': [input],
        'SOIL_TYPE': [soil_type],
        'N_SOIL': [a],
        'P_SOIL': [b],
        'K_SOIL': [c1],
        'TEMPERATURE': [d],
        'HUMIDITY': [e],
        'ph': [f],
        'RAINFALL': [g],
        })
        new_data_encoded = pd.get_dummies(new_data)
        new_data_encoded = new_data_encoded.reindex(columns=X.columns, fill_value=0)  # Ensure same set of dummy variables
        predicted_price = model_yield.predict(new_data_encoded)
        col1,col2,col3 = st.columns([4,6,1])
        #get crop yield= profit+total cost/predicted price
        profit=0.3*predicted_price
        total_cost=0.7*predicted_price
        yi=profit+total_cost/predicted_price[0]
        yid=yi/100
        yid=yid*area

        if col2.button('Predict Crop Yield',type='primary'):
            output=f"The predicted {crop_name} yield is: {int(yid)} quintals/ha."
            st.success(output)
def englih_page():
    # Navigation menu for user dashboard

    with st.sidebar:
        st.markdown(f"<h1 style='text-align: center; color: black;'><b>🏡Dashboard</b></h1>", unsafe_allow_html=True)

        selected_tab = option_menu(
            menu_title=None,
            options=["Seasonal Crops","Fertilizers", 'Crop Recommendation','Yield Prediction','Fertilizer Usage','Fertilizer History','Visualizations',"Edit Page" ,'Logout'],
        styles={
        "nav-link-selected": {"background-color": "green", "color": "white", "border-radius": "5px"},
        }
        )
        user=st.session_state['user']
        user=fetch_details(user[2])
        col1,col2=st.columns([1,1])
        temp=user[4]
        sky=user[6]
        col1.markdown(f"<h1 style='text-align: center; color:black;'>{temp}🌞</h1>", unsafe_allow_html=True)
        col2.markdown(f"<h1 style='text-align: center; color:black;'>{sky}🌥️</h1>", unsafe_allow_html=True)

    if selected_tab == "Seasonal Crops":
        seasonal()
    elif selected_tab == "Fertilizers":
        fertilizer()
    elif selected_tab == "Yield Prediction":
        yield_prediction()
    elif selected_tab == "Crop Recommendation":
        st.markdown(
                """
                <style>
                /* Apply background image to the main content area */
                .main {
                    background-image: url('https://dailycivil.com/wp-content/uploads/2023/08/TYPES-OF-SOIL-3.jpg');
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    min-height: 100vh;  /* Ensure the background covers the whole screen */
                    background-color: rgba(255, 255, 255, 0.6); /* Add a semi-transparent overlay */
                    background-blend-mode: overlay; /* Blend the image with the overlay */
                }
                </style>
                """,
                unsafe_allow_html=True
            )
        # Class definitions
        classes = {0: "Alluvial Soil:-{ Rice,Wheat,Sugarcane,Maize,Cotton,Soyabean,Jute }", 
                1: "Black Soil:-{ Virginia, Wheat , Jowar,Millets,Linseed,Castor,Sunflower} ",
                2: "Clay Soil:-{ Rice,Lettuce,Chard,Broccoli,Cabbage,Snap Beans }", 
                3: "Red Soil:{ Cotton,Wheat,Pilses,Millets,OilSeeds,Potatoes }",
                4: "Red Soil:{ Cotton,Wheat,Pilses,Millets,OilSeeds,Potatoes }"
                }

        # HTML content for each soil type
        html_content = {
            "Alluvial": """
            <!DOCTYPE HTML>
            <html>
            <head>
                <title>Alluvial Soil</title>
                <link rel="shortcut icon" type="image" href="https://hi-static.z-dn.net/files/d73/28374f9395f783f022566793228cbf71.jpg">
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
                <style>
                    body { margin: 0; padding: 0; background-image: url('https://hi-static.z-dn.net/files/d73/28374f9395f783f022566793228cbf71.jpg'); font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; }
                    #wrapper { max-width: 1200px; width: 90%; text-align: center; background-image: url('https://cdn.pixabay.com/photo/2023/02/01/21/40/pink-7761356_640.png'); background-repeat: no-repeat; background-size: cover; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); padding: 20px; }
                    header h1 { font-size: 2em; margin-bottom: 20px; color: #333; }
                    header p { font-size: 1.2em; color: #555; }
                    .crop-gallery { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 20px; margin-top: 20px; }
                    .crop-item { text-align: center; width: calc(33% - 20px); box-sizing: border-box; }
                    .crop-item img { width: 100%; height: auto; max-height: 150px; border: 2px solid #ccc; border-radius: 8px; object-fit: cover; }
                    .crop-item p { margin-top: 10px; font-size: 1em; font-weight: bold; color: #333; }
                </style>
            </head>
            <body>
                <div id="wrapper">
                    <header id="header">
                        <h1>Soil Type: Alluvial Soil</h1>
                        <p>You can Plant below crops:</p>
                        <div class="crop-gallery">
                            <div class="crop-item"><img src="https://organicboosting.bio/wp-content/uploads/2024/04/organic-rice.jpg" alt="Rice"><p>Rice</p></div>
                            <div class="crop-item"><img src="https://foodrevolution.org/wp-content/uploads/iStock-1400295675.jpg" alt="Wheat"><p>Wheat</p></div>
                            <div class="crop-item"><img src="https://www.mahagro.com/cdn/shop/articles/iStock_000063947343_Medium_4e1c882b-faf0-4487-b45b-c2b557d32442.jpg?v=1541408129" alt="Sugarcane"><p>Sugarcane</p></div>
                            <div class="crop-item"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZoHK8hyR9XPMyPyH1X35brHDxO8dvRADu7A&s" alt="Maize"><p>Maize</p></div>
                            <div class="crop-item"><img src="https://m.media-amazon.com/images/I/61WWhptbnEL.jpg" alt="Cotton"><p>Cotton</p></div>
                            <div class="crop-item"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSs2CkDWauAijpsx1TbHPMkuw7ptduFMyK0Ng&s" alt="Soyabean"><p>Soyabean</p></div>
                        </div>
                    </header>
                </div>
            </body>
            </html>
            """,
            "Black": """
            <!DOCTYPE HTML>
            <html>
            <head>
                <title>Black Soil</title>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
                <style>
                    body { margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-image: url('https://www.vedantu.com/question-sets/d95b6135-bb2d-4012-9202-09783f9814905747391973605676716.png'); }
                    #wrapper { max-width: 1200px; width: 90%; text-align: center; background-image: url('https://cdn.pixabay.com/photo/2023/02/01/21/40/pink-7761356_640.png'); background-repeat: no-repeat; background-size: cover; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); padding: 20px; }
                    header h1 { font-size: 2em; margin-bottom: 20px; color: #333; }
                    header p { font-size: 1.2em; color: #555; }
                    .crop-gallery { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 20px; margin-top: 20px; }
                    .crop-item { text-align: center; width: calc(33% - 20px); box-sizing: border-box; }
                    .crop-item img { width: 100%; height: auto; max-height: 150px; border: 2px solid #ccc; border-radius: 8px; object-fit: cover; }
                </style>
            </head>
            <body>
                <div id="wrapper">
                    <header id="header">
                        <h1>Soil Type: Black Soil</h1>
                        <p>You can Plant below crops:</p>
                        <div class="crop-gallery">
                            <div class="crop-item"><img src="https://www.world-grain.com/ext/resources/2023/07/28/wheat-ears-field_NITR---STOCK.ADOBE.COM_e.jpg?height=667&t=1724852636&width=1080" alt="Wheat"><p>Wheat</p></div>
                            <div class="crop-item"><img src="https://pmfias.b-cdn.net/wp-content/uploads/2024/05/Picture-1-39.png" alt="Jowar"><p>Jowar</p></div>
                            <div class="crop-item"><img src="https://indocert.org/wp-content/uploads/2024/10/2.png" alt="Millets"><p>Millets</p></div>
                            <div class="crop-item"><img src="https://img.feedstrategy.com/files/base/wattglobalmedia/all/image/2019/10/fs.linseed-in-animal-feed.png?auto=format%2Ccompress&fit=max&q=70&w=1200" alt="Linseed"><p>Linseed</p></div>
                            <div class="crop-item"><img src="https://media.istockphoto.com/id/486714852/photo/green-buds-of-castor-oil-plant-ricinus-communis.jpg?s=612x612&w=0&k=20&c=mms9HvHbF-gkUJrwHnNSkRg2Z_xSwcGUeuN-CypxohQ=" alt="Castor"><p>Castor</p></div>
                            <div class="crop-item"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMnfGVe2KqjpZ4q7Z2IJjmSqj5nsmoLl8T3g&s" alt="Sunflower"><p>Sunflower</p></div>
                        </div>
                    </header>
                </div>
            </body>
            </html>
            """,
            "Clay": """
            <!DOCTYPE HTML>
            <html>
            <head>
                <title>Clay Soil</title>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
                <style>
                    body { margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-image: url('https://www.shutterstock.com/image-photo/rich-hue-red-soilred-soil-600nw-2472615905.jpg'); }
                    #wrapper { max-width: 1200px; width: 90%; text-align: center; background-image: url('https://cdn.pixabay.com/photo/2023/02/01/21/40/pink-7761356_640.png'); background-repeat: no-repeat; background-size: cover; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); padding: 20px; }
                    header h1 { font-size: 2em; margin-bottom: 20px; color: #333; }
                    header p { font-size: 1.2em; color: #555; }
                    .crop-gallery { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 20px; margin-top: 20px; }
                    .crop-item { text-align: center; width: calc(33% - 20px); box-sizing: border-box; }
                    .crop-item img { width: 100%; height: auto; max-height: 150px; border: 2px solid #ccc; border-radius: 8px; object-fit: cover; }
                    .crop-item p { margin-top: 10px; font-size: 1em; font-weight: bold; color: #333; }
                </style>
            </head>
            <body>
                <div id="wrapper">
                    <header id="header">
                        <h1>Soil Type: Clay Soil</h1>
                        <p>You can Plant below crops:</p>
                        <div class="crop-gallery">
                            <div class="crop-item"><img src="https://www.world-grain.com/ext/resources/Article-Images/2021/09/Rice_AdobeStock_64819529_E.jpg?height=667&t=1632316472&width=1080" alt="Rice"><p>Rice</p></div>
                            <div class="crop-item"><img src="https://i0.wp.com/images-prod.healthline.com/hlcmsresource/images/AN_images/red-leaf-lettuce-1296x728-feature.jpg?w=1155&h=1528" alt="Lettuce"><p>Lettuce</p></div>
                            <div class="crop-item"><img src="https://www.health.com/thmb/m6gcOGCKNjLCv5mnk8zV_MqDX9U=/2121x0/filters:no_upscale():max_bytes(150000):strip_icc()/SwissChard-6193e3b4941b4479979f5df338ae6ea3.jpg" alt="Chard"><p>Chard</p></div>
                            <div class="crop-item"><img src="https://www.health.com/thmb/Rmc7904DESkPtLdsuVB49yGBZNo=/3950x0/filters:no_upscale():max_bytes(150000):strip_icc()/Health-Stocksy_txp48915e00jrw300_Medium_5965806-1b7dc08bfcbc4b748e5f1f27f67894a5.jpg" alt="Broccoli"><p>Broccoli</p></div>
                            <div class="crop-item"><img src="https://assets.clevelandclinic.org/transform/871f96ae-a852-4801-8675-683191ce372d/Benefits-Of-Cabbage-589153824-770x533-1_jpg" alt="Cabbage"><p>Cabbage</p></div>
                            <div class="crop-item"><img src="https://www.shutterstock.com/image-photo/healthy-benefits-bush-beansgreen-beans-260nw-751391686.jpg" alt="Snap Beans"><p>Snap Beans</p></div>
                        </div>
                    </header>
                </div>
            </body>
            </html>
            """,
            
            "Red": """
            <!DOCTYPE HTML>
            <html>
            <head>
                <title>Red Soil</title>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
                <style>
                    body { margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-image: url('https://m.media-amazon.com/images/I/61A+ysVsqgL._AC_UF1000,1000_QL80_.jpg'); }
                    #wrapper { max-width: 1200px; width: 90%; text-align: center; background-image: url('https://cdn.pixabay.com/photo/2023/02/01/21/40/pink-7761356_640.png'); background-repeat: no-repeat; background-size: cover; border-radius: 10px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); padding: 20px; }
                    header h1 { font-size: 2em; margin-bottom: 20px; color: #333; }
                    header p { font-size: 1.2em; color: #555; }
                    .crop-gallery { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 20px; margin-top: 20px; }
                    .crop-item { text-align: center; width: calc(33% - 20px); box-sizing: border-box; }
                    .crop-item img { width: 100%; height: auto; max-height: 150px; border: 2px solid #ccc; border-radius: 8px; object-fit: cover; }
                    .crop-item p { margin-top: 10px; font-size: 1em; font-weight: bold; color: #333; }
                </style>
            </head>
            <body>
                <div id="wrapper">
                    <header id="header">
                        <h1>Soil Type: Red Soil</h1>
                        <p>You can Plant below crops:</p>
                        <div class="crop-gallery">
                            <div class="crop-item"><img src="https://textileengineering.net/wp-content/uploads/2023/01/Cotton-Fibre.jpg" alt="Cotton"><p>Cotton</p></div>
                            <div class="crop-item"><img src="https://www.epicgardening.com/wp-content/uploads/2022/01/wheat-vs-barley-1.jpg" alt="Wheat"><p>Wheat</p></div>
                            <div class="crop-item"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5FnsC4oOq5c6HebsREvIJMep7GpHaCK3MpA&s" alt="Pulses"><p>Pulses</p></div>
                            <div class="crop-item"><img src="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTZBMl-oxSQ-8G5gEoSmSxNi1Z2S6NTYCaFRC2d0Nfg-ifrXLoO4d4jBBaN9WUBYzYCGxmt3oaTomnmu0gHn8XPjQ" alt="Millets"><p>Millets</p></div>
                            <div class="crop-item"><img src="https://static.toiimg.com/photo/88435060.cms" alt="Oil Seeds"><p>Oil Seeds</p></div>
                            <div class="crop-item"><img src="https://plantix.net/en/library/assets/custom/crop-images/potato.jpeg" alt="Potatoes"><p>Potatoes</p></div>
                        </div>
                    </header>
                </div>
            </body>
            </html>
            """   
        }
        def model_predict(image_path, model):
            try:
                print("Predicted")
                image = load_img(image_path, target_size=(224, 224))
                image = img_to_array(image)
                image = image / 255
                image = np.expand_dims(image, axis=0)
                result = np.argmax(model.predict(image))
                prediction = classes[result]
                if result == 0:
                    return "Alluvial", html_content["Alluvial"]
                elif result == 1:
                    return "Black", html_content["Black"]
                elif result == 2:
                    return "Clay", html_content["Clay"]
                elif result == 3:
                    return "Red", html_content["Red"]
                elif result == 4:
                    return "Red", html_content["Red"]
            except Exception as e:
                return 'Red',html_content["Red"]

        # Streamlit UI setup
        st.markdown(f"<h2 style='text-align: center; color:indigo;'>Crop Recommendations Based on Soil Surface</h2>", unsafe_allow_html=True)
        # File uploader in Streamlit
        # Custom styling for the file uploader
        st.markdown(
            """
            <style>
            div[data-testid="stFileUploader"] {
                border: 2px dashed black !important; /* Indigo border */
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                font-size: 18px;
                color: black;
                background-color: #F8F9FA;
                margin-bottom: 20px;
            }
            div[data-testid="stFileUploader"]:hover {
                border-color: #4338CA; /* Darker indigo on hover */
                background-color: #EDEDF0;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # File uploader inside the styled box
        col1,col2,col3=st.columns([1,6,1])
        img_file = col2.file_uploader("UPLOAD SOIL IMAGES HERE", type=["jpg", "jpeg", "png"])

        col1,col2,col3=st.columns([3,3,1])
        button = col2.button("Predict", type="primary")
        if img_file is not None and button:
            pred, output_html = model_predict(img_file, SoilNet)
            col1,col2,col3=st.columns([1,100,1])
            # Display the prediction result and the HTML page
            col2.markdown(output_html, unsafe_allow_html=True)

    elif selected_tab=='Logout':
        # Logout functionality
        st.session_state.clear()  # Clear session state to "log out"
        st.experimental_rerun()
    elif selected_tab=='Edit Page':
        st.markdown('<h1 style="text-align: center; color:blue;">Edit Profile</h1>', unsafe_allow_html=True)
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://static.vecteezy.com/system/resources/previews/010/171/047/non_2x/colorful-watercolor-world-map-on-transparent-background-free-png.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-height: 100vh;  /* Ensure the background covers the whole screen */
            background-color: rgba(255, 255, 255, 0.6); /* Add a semi-transparent overlay */
            background-blend-mode: overlay; /* Blend the image with the overlay */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
        user=fetch_details(user[2])
        email=user[2]
        location=user[3]
        col1,col2,col3=st.columns([1,3,1])
        loc=col2.text_input('Enter Location',value=location)
        language=col2.selectbox('Select Language',['English','Telugu'])
        st.write("")
        col1,col2,col3=st.columns([3,3,1])
        if col2.button('Update',type='primary'):
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
            change_location(email,loc,temp,humd,sky,rain,language)
            col1,col2,col3=st.columns([1,3,1])
            col2.success('Updated Successfully')
    elif selected_tab=='Fertilizer Usage':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://kisanvedika.bighaat.com/wp-content/uploads/2024/08/efficient-fertilizer-use.jpg');
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
        st.markdown(f"<h1 style='text-align: center; color:green;'>Fertilizer Usage</h1>", unsafe_allow_html=True)
        data=pd.read_csv('fertilizer_dataset_50_crops.csv')
        #unique column names
        crops = data['Crop Name'].unique()
        crops=crops.tolist()
        col1,col2=st.columns([1,1])
        selected_crop=col1.selectbox('Select Crop',crops)
        acres=col2.number_input('No of Acres',value=1)
        col1,col2,col3=st.columns([2,2,1])
        button=col2.button('Predict',type='primary')
        if button:
            filtered_data = data[data['Crop Name'] == selected_crop]
            # Display filtered data
            if not filtered_data.empty:
                crop_details = filtered_data.iloc[0]  # Get first matching row

                # HTML and CSS for styling
                html_content = f"""
                <style>
                    .crop-card {{
                        background-image:url(https://www.icl-group.com/wp-content/uploads/2022/07/fetilizers-101-1-1.jpg);
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                        background-color: rgba(255, 255, 255, 0.7); /* Add a semi-transparent overlay */
                        background-blend-mode: overlay; /* Blend the image with the overlay */
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
                        font-family: Arial, sans-serif;
                    }}
                    .title {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #2c3e50;
                    }}
                    .info {{
                        font-size: 18px;
                        margin: 5px 0;
                        color: #34495e;
                    }}
                    .icon {{
                        font-size: 22px;
                        margin-right: 10px;
                    }}
                </style>

                <div class="crop-card">
                    <div class="title">🌿 {crop_details['Crop Name']} -Usage Details</div>
                    <p class="info">💰 <b>Cost (INR):</b> {crop_details['Cost (INR)']*acres}</p>
                    <p class="info">🔄 <b>No of Times Need to Use:</b> {crop_details['Application Frequency']}</p>
                    <p class="info">🌱 <b>When to Use:</b> {crop_details['Application Stage']}</p>
                    <p class="info">💊 <b>Dosage per Acre:</b> {crop_details['Dosage per Acre']}</p>
                    <p class="info">💧 <b>Water to Mix (Liters):</b> {crop_details['Water to Mix (Liters for 50 crops)']} lts</p>
                </div>
                """
                # Render HTML
                st.markdown(html_content, unsafe_allow_html=True)
                query=crop_details['Crop Name']+'cultivation farming in english'
                st.write('')
                st.write('')
                videos = fetch_youtube_videos(query)
                for i in range(0, len(videos), 2):
                    cols = st.columns(2)  # Create 3 columns
                    for j, video in enumerate(videos[i:i+2]):  # Iterate over videos for the current row
                        with cols[j]:
                            st.video(f"https://www.youtube.com/watch?v={video['video_id']}")
            else:
                st.write("No data found for the selected crop.")
    elif selected_tab=='Fertilizer History':
        st.markdown('<h1 style="text-align: center; color:maroon;">Usage History of Fertilizers</h1>', unsafe_allow_html=True)
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url('https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTA2L3BkbWlzYzktYmctZGlnaXRhbGN3Y29tbW9ud2VhbHRocTUyNG41OTlzLWltYWdlLTA0LmpwZw.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            min-height: 100vh;  /* Ensure the background covers the whole screen */
            background-color: rgba(255, 255, 255, 0.4); /* Add a semi-transparent overlay */
            background-blend-mode: overlay; /* Blend the image with the overlay */
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        user=fetch_details(user[2])
        email=user[2]
        user_fertilizers = fetch_fertilizer(email)  # Fetch fertilizers specific to the user
        
        if user_fertilizers:
            # Convert the user’s fertilizers to a DataFrame
            user_fertilizers_df = pd.DataFrame(user_fertilizers, columns=['fertilizer'])

            # Read the CSV file containing all fertilizers
            d1 = pd.read_csv('fertilizer.csv')

            # Merge to get only user-related fertilizers (Ensures only those fertilizers present in the CSV are displayed)
            filtered_fertilizers = d1[d1['fertilizer'].isin(user_fertilizers_df['fertilizer'])]

            # Remove duplicates
            unique_fertilizers = filtered_fertilizers.drop_duplicates(subset=['fertilizer'])

            # Streamlit Layout - Display in 3 columns
            cols = st.columns(3)

            for index, row in enumerate(unique_fertilizers.itertuples()):
                with cols[index % 3]:  # Distribute across 3 columns
                    st.markdown(
                        f"""
                        <div style="border: 2px solid pink; padding: 10px; text-align: center; background-image:url(https://marketplace.canva.com/EAGPIDVZ0-A/1/0/1131w/canva-peach-aesthetic-background-flyer-IqGDJ_simvM.jpg); background-size: cover; background-position: center; background-repeat: no-repeat; border-radius: 10px;">
                            <img src="{row.image}" width="150px" height="150px" style="border-radius: 10px;"><br>
                            <b style="font-size: 18px; color: red;">{row.fertilizer}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.write("No data found")
    elif selected_tab=='Visualizations':
        st.markdown('<h1 style="text-align: center; color:red;">Data Visualizations</h1>', unsafe_allow_html=True)
        data1=pd.read_csv('Crop_recommendation.csv')
        col1,col2,col3=st.columns([1,3,2])
        option=col3.selectbox('Select Feature',['Seasonal Crops','Fertilizer Recommendation','Crop Yield Prediction','Fertilizer Usage'])
        if option=='Seasonal Crops':
            df = pd.DataFrame(data1)
            crop_counts = df.groupby("District")["Crop"].count().reset_index()
            crop_counts.columns = ["District", "Number of Crops"]
            fig_bar = px.bar(
                crop_counts, 
                x="District", 
                y="Number of Crops", 
                text="Number of Crops",
                labels={"Number of Crops": "Total Crops"},
                title="Number of Crops in Each District",
                color="District"
            )
            fig_bar.update_traces(textposition="outside", marker=dict(line=dict(color="black", width=1)))
            st.plotly_chart(fig_bar)
            seasonal_counts = df.groupby("Season")["Crop"].count().reset_index()
            seasonal_counts.columns = ["Season", "Number of Crops"]
            fig_bar = px.bar(
                seasonal_counts, 
                x="Season", 
                y="Number of Crops", 
                text="Number of Crops",
                labels={"Number of Crops": "Total Crops"},
                title="Number of Crops in Each Season",
                color="Season"
            )
            fig_bar.update_traces(textposition="outside", marker=dict(line=dict(color="black", width=1)))
            st.plotly_chart(fig_bar)
        elif option=='Fertilizer Recommendation':
            data2=pd.read_csv('f2.csv')
            df2 = pd.DataFrame(data2)
            fertilizer_counts = df2["Fertilizer"].value_counts().reset_index()
            fertilizer_counts.columns = ["Fertilizer", "Count"]

            fig_fertilizer = px.bar(
                fertilizer_counts, 
                x="Fertilizer", 
                y="Count", 
                text="Count",
                title="Count of Fertilizers",
                color="Fertilizer"
            )
            fig_fertilizer.update_traces(textposition="outside", marker=dict(line=dict(color="black", width=1)))
            st.plotly_chart(fig_fertilizer)

            # **2️⃣ Count of Crops**
            crop_counts = df2["Crop_Type"].value_counts().reset_index()
            crop_counts.columns = ["Crop_Type", "Count"]

            fig_crop = px.bar(
                crop_counts, 
                x="Crop_Type", 
                y="Count", 
                text="Count",
                title="Count of Crops",
                color="Crop_Type"
            )
            fig_crop.update_traces(textposition="outside", marker=dict(line=dict(color="black", width=1)))
            st.plotly_chart(fig_crop)

            # **3️⃣ Soil Type vs Crop Type**
            fig_soil_crop = px.histogram(
                df2, 
                x="Soil_Type", 
                color="Crop_Type", 
                title="Soil Type vs Crop Type Distribution",
                barmode="group"
            )
            st.plotly_chart(fig_soil_crop)
        elif option=='Crop Yield Prediction':
            data3=pd.read_csv('crop_yield.csv')
            df3 = pd.DataFrame(data3)
            fig_state_crop = px.bar(
                df3, 
                x="State", 
                color="Crop", 
                title="State vs Crops",
                barmode="group"
            )
            st.plotly_chart(fig_state_crop)

        elif option=='Fertilizer Usage':
            data4=pd.read_csv('fertilizer_dataset_50_crops.csv')
            df4 = pd.DataFrame(data4)
            crop_counts = df4["Crop Name"].value_counts().reset_index()
            crop_counts.columns = ["Crop Name", "Count"]

            # **3️⃣ Unique Fertilizer vs Cost**
            unique_fertilizers = df4[["Fertilizer Used", "Cost (INR)"]].drop_duplicates()

            fig_fertilizer_cost = px.bar(
                unique_fertilizers, 
                x="Fertilizer Used", 
                y="Cost (INR)", 
                text="Cost (INR)",
                title="Unique Fertilizer vs Cost",
                color="Fertilizer Used"
            )
            fig_fertilizer_cost.update_traces(textposition="outside", marker=dict(line=dict(color="black", width=1)))
            st.plotly_chart(fig_fertilizer_cost)

            

