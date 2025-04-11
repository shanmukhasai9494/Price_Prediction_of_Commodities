import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import streamlit as st
import joblib
# import streamlit as st
import requests
YOUTUBE_API_KEY = "AIzaSyDYEeSTrT7pPpVzpmaJ491gxogVxfWwpvM"

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
def info_box(yield_kg, yield_tons, price_per_kg, total_price):
    def format_number_indian(num):
        num_str = f"{num:,}"
        parts = num_str.split(",")
        if len(parts) > 2:
            return parts[0] + "," + ",".join(parts[1:]).replace(",", "_", 1).replace("_", ",")
        return num_str
    
    return f"""
        <div style="
            background-color: rgba(123, 216, 237, 0.6);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            color: black;
            font-weight: bold;
            width: 50%;
            margin: 0 auto;
        ">
            <span style='color: red;'>The crop yield is:</span> <span style='color: black;'>{format_number_indian(yield_kg)} kg</span><br>
            <span style='color: red;'>The total yield is:</span> <span style='color: black;'>{format_number_indian(yield_tons)} tons</span><br>
            <span style='color: red;'>The present price:</span> <span style='color: black;'>{format_number_indian(price_per_kg)} INR per kg</span><br>
            <span style='color: red;'>The total price:</span> <span style='color: black;'>{format_number_indian(total_price)} INR</span>
        </div>
    """

model=joblib.load('crop_price_model.pkl')
st.markdown(
    """
    <style>
    /* Apply background image to the main content area with transparency */
    .main {
        background-image: url('https://img.freepik.com/free-photo/agriculture-iot-with-rice-field-background_53876-124635.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255, 255, 255, 0.6); /* Add a semi-transparent overlay */
        background-blend-mode: overlay; /* Blend the image with the overlay */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(f"<h1 style='text-align: center; color:green;'>Crop Yield Prediction</h1>", unsafe_allow_html=True)
with st.form(key='my_form'):
    col1,col2,col3=st.columns(3)
    input=col1.selectbox("Select State",('Andaman and Nicobar Islands', 'Andhra Pradesh',
    'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh',
    'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
    'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala',
    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
    'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh'))
    crop_name=col2.selectbox("Select Crop",('Arecanut', 'Arhar/Tur', 'Bajra', 'Banana', 'Barley', 'Bean', 'Black pepper', 'Blackgram', 'Bottle Gourd', 'Brinjal', 'Cabbage', 'Cardamom', 'Carrot', 'Cashewnut', 'Castor seed', 'Cauliflower', 'Citrus Fruit', 'Coconut', 'Coffee', 'Coriander', 'Cotton', 'Cowpea', 'Drum Stick', 'Dry chillies', 'Dry ginger', 'Garlic', 'Ginger', 'Gram', 'Grapes', 'Groundnut', 'Guar seed', 'Horse-gram', 'Jack Fruit', 'Jowar', 'Jute', 'Khesari', 'Korra', 'Lemon', 'Lentil', 'Linseed', 'Maize', 'Mango', 'Masoor', 'Mesta', 'Moong(Green Gram)', 'Moth', 'Niger seed', 'Oilseeds total', 'Onion', 'Orange', 'Other  Rabi pulses', 'Other Cereals & Millets', 'Other Citrus Fruit', 'Other Dry Fruit', 'Other Fresh Fruits', 'Other Kharif pulses', 'Other Vegetables', 'Papaya', 'Peach', 'Pear', 'Peas & beans (Pulses)', 'Pineapple', 'Plums', 'Pome Fruit', 'Pome Granet', 'Potato', 'Pulses total', 'Pump Kin', 'Ragi', 'Rajmash Kholar', 'Rapeseed &Mustard', 'Redish', 'Ribed Guard', 'Rice', 'Rubber', 'Safflower', 'Samai', 'Sannhamp', 'Sapota', 'Sesamum', 'Small millets', 'Soyabean', 'Sugarcane', 'Sunflower', 'Sweet potato', 'Tapioca', 'Tea', 'Tobacco', 'Tomato', 'Total foodgrain', 'Turmeric', 'Turnip', 'Urad', 'Varagu', 'Water Melon', 'Wheat', 'Yam', 'other oilseeds', 'other misc. pulses', 'other fibres', 'other cereals', 'other vegetables', 'Total Pulses', 'Total foodgrain', 'Total fruits', 'Total vegetables'))


    acres=col3.number_input('Enter Acres')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        a=st.number_input('Enter N')
    with col2:
        b=st.number_input('Enter P')
    with col3:
        c1=st.number_input('Enter K')
    with col4:
        d=st.number_input('Temperature °C')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        e=st.number_input('Humidity %')
    with col2:
        f=st.number_input('pH')
    with col3:
        g=st.number_input('Rainfall mm')
    with col4:
        soil_type=st.selectbox("Select Soil Type",('Alluvial', 'Black', 'Clayey', 'Loamy', 'Red', 'Sandy', 'Silt'))
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
    data = pd.read_csv('crop_data.csv') 
    X = data.drop(['CROP_PRICE', 'CROP'], axis=1)  # Features
    X = pd.get_dummies(X)

    model_columns = list(X.columns)
    # Convert input data to dataframe
    input_data = pd.DataFrame(new_data, index=[0])
    input_data = pd.get_dummies(input_data)

    # Ensure the input data is in the same format as the training data
    input_data = input_data.reindex(columns=model_columns, fill_value=0)

    # Make prediction
    prediction = model.predict(input_data)
    col1,col2,col3=st.columns([2,2,1])
    if col2.form_submit_button('Predict',type='primary') and crop_name:
        pri=pd.read_csv('crop_prices.csv')
        price=pri[pri['Crop Name']==crop_name]['Price 2025 (INR per kg)'].values[0]
        p_tons=prediction[0]*acres/1000
        if p_tons:
            st.markdown(info_box(prediction[0]*acres,int(p_tons),price,round(prediction[0]*acres*price)),unsafe_allow_html=True)
        #show previous price vs predicted price
        pri=pd.read_csv('crop_prices.csv')
        prediction = [1.2]  # Example multiplier (replace with actual prediction logic)
        st.write('----')
        # Get price
        st.markdown(f"<h4 style='text-align: center; color:blue;'>Price Trend</h4>", unsafe_allow_html=True)
        price = pri[pri['Crop Name'] == crop_name]['Price 2025 (INR per kg)'].values[0]
        prev_price = pri[pri['Crop Name'] == crop_name]['Price 2020'].values[0]

        price_2020 = pri[pri['Crop Name'] == crop_name]['Price 2020'].values[0]
        price_2025 = pri[pri['Crop Name'] == crop_name]['Price 2025 (INR per kg)'].values[0]
        years = np.arange(2020, 2026)
        prices = np.linspace(price_2020, price_2025, num=len(years)) + np.random.uniform(-1, 1, size=len(years))
        col1,col2=st.columns(2)
        # Plot the line chart
        fig, ax = plt.subplots()
        ax.plot(years, prices, marker='o', linestyle='-', color='red')
        ax.set_xticks([])  # Remove year labels
        ax.set_title(f'Price Trend for {crop_name} (2020-2025)')
        ax.set_ylabel('Price (INR per kg)')
        col1.pyplot(fig)

        #show plot for next 5 years
        price_2020 = pri[pri['Crop Name'] == crop_name]['Price 2020'].values[0]
        price_2025 = pri[pri['Crop Name'] == crop_name]['Price 2025 (INR per kg)'].values[0]

        # Generate price trend from 2020 to 2025
        years_past = np.arange(2020, 2026)
        prices_past = np.linspace(price_2020, price_2025, num=len(years_past)) + np.random.uniform(-1, 1, size=len(years_past))

        # Forecast next 5 years (2026-2030) using a simple linear growth model
        slope = (price_2025 - price_2020) / (2025 - 2020)
        years_future = np.arange(2026, 2031)
        prices_future = [price_2025 + slope * (year - 2025) + np.random.uniform(-1, 1) for year in years_future]

        # Combine past and forecasted data
        all_years = np.concatenate((years_past, years_future))
        all_prices = np.concatenate((prices_past, prices_future))

        # Plot the price trend with forecast
        fig, ax = plt.subplots()
        ax.plot(all_years, all_prices, marker='o', linestyle='-', color='blue', label='Price Trend')
        ax.axvline(x=2025, color='red', linestyle='--', label='Forecast Start')  # Indicate forecast start
        ax.set_title(f'Price Forecast for {crop_name} (2020-2030)')
        ax.set_xlabel('Year')
        ax.set_ylabel('Price (INR per kg)')
        ax.legend()
        col2.pyplot(fig)
        st.write('----')
        st.markdown(f"<h4 style='text-align: center; color:red;'>Plant Care Videos</h4>", unsafe_allow_html=True)
        query = f"{crop_name} crop care"
        videos = fetch_youtube_videos(query, max_results=2)

        # Display videos in rows of 3
        for i in range(0, len(videos), 2):
            cols = st.columns(2)  # Create 3 columns
            for j, video in enumerate(videos[i:i+2]):  # Iterate over videos for the current row
                with cols[j]:
                    st.video(f"https://www.youtube.com/watch?v={video['video_id']}")
        fert=f'Fertilizer for {crop_name}'
        videos=fetch_youtube_videos(fert,max_results=2)
        for i in range(0, len(videos), 2):
            cols = st.columns(2)  # Create 3 columns
            for j, video in enumerate(videos[i:i+2]):  # Iterate over videos for the current row
                with cols[j]:
                    st.video(f"https://www.youtube.com/watch?v={video['video_id']}")