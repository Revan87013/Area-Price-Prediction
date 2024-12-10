import streamlit as st
import pickle
from PIL import Image
import requests
from io import BytesIO
import warnings

# Suppress warnings related to LinearRegression
warnings.filterwarnings('ignore', message=".*LinearRegression.*fitted with feature names.*")

# Streamlit page configuration
st.set_page_config(page_title="Area-Price Predictor", layout="wide", page_icon="🏠")

# Custom CSS for UI Styling
st.markdown("""
    <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
            padding: 10px 20px;
        }
        .stButton > button:hover {
            background-color: #45a049;
            color: white;
        }
        .header-style {
            font-size: 50px;
            color: #4CAF50;
            text-align: center;
            font-weight: bold;
        }
        .subheader-style {
            font-size: 20px;
            color: #333333;
            text-align: center;
            font-weight: 300;
            margin-top: -10px;
        }
        .footer-style {
            text-align: center;
            font-size: 14px;
            color: grey;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section with Custom Style
st.markdown('<div class="header-style">🏡 Area-Price Prediction App</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader-style">Powered by Machine Learning | Indian Property Market</div>', unsafe_allow_html=True)

# Add a decorative banner image
image_url = "https://wallpapercave.com/wp/wp10389741.jpg"
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))
st.image(img, caption="Property Price Prediction", use_container_width=True)

# Sidebar Section with Icons and Info
st.sidebar.header("📋 *App Features*")
st.sidebar.markdown("""
- Predict property prices based on area.
- Adjust prices dynamically based on location.
- Interactive and user-friendly interface.
""")
st.sidebar.header("📊 *Model Info*")
st.sidebar.markdown("""
- Linear Regression Model.
- Location-based price adjustments.
- Predefined Indian city multipliers.
""")

# Dropdown for Indian locations with descriptions
locations = {
    "Mumbai": {"factor": 1.5, "info": "Financial hub with high property prices."},
    "Delhi": {"factor": 1.3, "info": "Capital city with high demand."},
    "Bangalore": {"factor": 1.2, "info": "IT hub with growing property value."},
    "Hyderabad": {"factor": 1.1, "info": "Emerging market with steady growth."},
    "Chennai": {"factor": 1.0, "info": "Steady property prices."},
    "Kolkata": {"factor": 0.9, "info": "Affordable property market."},
    "Ahmedabad": {"factor": 0.8, "info": "Developing market with lower costs."},
    "Pune": {"factor": 0.85, "info": "Affordable IT city with growth potential."}
}

st.sidebar.subheader("📍 Select a Location")
selected_location = st.sidebar.radio(
    "Choose a city:",
    list(locations.keys()),
    help="Select a city to adjust prices based on location-specific factors."
)
st.sidebar.info(locations[selected_location]["info"])

# Area input with both slider and manual input
st.subheader("📏 Enter the Area (in square feet)")
area_slider = st.slider(
    "Move the slider to specify the area of the property (sqft):",
    min_value=500, max_value=10000, step=50, value=1000
)

area_manual = st.number_input(
    "Or enter the area manually:",
    min_value=500, max_value=10000, step=50, value=1000,
    help="Enter the area in square feet."
)

# Allow the user to choose between slider or manual input (defaults to slider)
area = area_slider if area_slider == area_manual else area_manual

# Load the pre-trained model
try:
    with open('area_price_model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
except Exception as e:
    st.error(f"Model loading failed: {e}")

# Function to predict price
def predict_price(area, location):
    # Predict price using the model
    base_price = loaded_model.predict([[area]])[0]
    # Apply location multiplier
    location_factor = locations[location]["factor"]
    adjusted_price = base_price * location_factor
    return adjusted_price

# Stylish Prediction Button
st.markdown("---")
st.subheader("🔮 Predict the Property Price")
button = st.button("💰 Show Predicted Price")

if button:
    if area > 0:
        try:
            predicted_price = predict_price(area, selected_location)
            st.success(f"✨ *Predicted Price*: ₹{predicted_price:.2f} for {area} sqft in {selected_location}")
        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)}")
    else:
        st.warning("Please enter a valid area (greater than 0).")

st.markdown("---")
# Footer with Created by and Copyright info
st.markdown("""
    ---
    <div style="text-align: center; font-size: 14px; color: grey; margin-top: 20px;">
        <p>Created by <a href="https://www.linkedin.com/in/revangunaganti" target="_blank">🔗LinkedIn</a> | 
        <a href="https://github.com/Revan87013" target="_blank">🐱GitHub</a></p>
        <p>&copy; 2024 All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)
