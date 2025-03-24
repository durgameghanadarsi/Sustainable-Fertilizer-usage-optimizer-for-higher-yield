from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import streamlit as st
import os
import tensorflow as tf
import gdown

# Function to download the model from Google Drive
@st.cache_data(show_spinner = "Getting Things Ready................")
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
              4: "Red Soil:{ Cotton,Wheat,Pilses,Millets,OilSeeds,Potatoes }"}

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
            body { margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-image: url('https://m.media-amazon.com/images/I/61A+ysVsqgL.AC_UF1000,1000_QL80.jpg'); }
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

# Streamlit UI setup
st.markdown(
    """
    <div style="text-align: center; padding: 1px; background-color: #fc986a ; border-radius: 60px; border: 2px solid black;">
        <p style="color: black; font-size: 48px;"><b>Soil Surface Texture Detection</b></p>
    </div>
    """,
    unsafe_allow_html=True
)

# File uploader in Streamlit
file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if file is not None:
    pred, output_html = model_predict(file, SoilNet)
    col1,col2,col3=st.columns([1,100,1])
    # Display the prediction result and the HTML page
    col2.markdown(output_html, unsafe_allow_html=True)