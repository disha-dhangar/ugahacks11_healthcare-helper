import os
from geopy.geocoders import Nominatim
import requests
from dotenv import load_dotenv
import streamlit as st


# Geoapify Api Key and GeoPy API used
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
geolocator = Nominatim(user_agent="Healthcare Helper")

# Check if API key is set
if not GEOAPIFY_API_KEY:
    st.error("API key not set. Please set GEOAPIFY_API_KEY in your environment. Refer to Geoapify documentation as needed.")

# Loads CSS for styling
with open("display.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Personalizes page title and icon
st.set_page_config(
    page_title="Healthcare Helper", 
    page_icon="🏥", 
)


# Title and description
st.title("°✧˖ Healthcare Helper ˖✧°")
st.subheader("Welcome to Healthcare Helper, an application to help you find healthcare services nearby easily and efficiently.")
st.write("Simply enter an address below to get started. You may filter out the results using the options provided.")
st.write("---")

# User input of location
location_input = st.text_input("Enter a city, zip code, or address :", key="address")

# User input for search parameters
distance = st.slider("Distance (meters):", 0, 20000, 10000)
results_amount = st.number_input("Results:", min_value=1, max_value=20, value=10)
categories = st.selectbox(
    "Healthcare services:", 
    ["Show All",
    "Allergology",
    "Cardiology",
    "Dentist",
    "Dermatology",
    "Endocrinology",
    "Gastroenterology",
    "General",
    "Gynaecology",
    "Hospital",
    "Occupational",
    "Ophthalmology",
    "Orthodontics",
    "Orthopaedics",
    "Otolaryngology",
    "Paediatrics",
    "Pharmacy",
    "Psychiatry",
    "Pulmonology",
    "Radiology",
    "Rheumatology",
    "Trauma",
    "Urology",
    "Vascular Surgery",
    ]
)


# Search button logic and API request
if st.button("Search"):
    # Displays warning if location input is empty, otherwise proceeds with geocoding
    if not location_input.strip():
        st.warning("Please enter an address.")
    else: 
        location = geolocator.geocode(location_input)

        # Displays warning if geocoding fails, otherwise proceeds with API request
        if not location:
            st.warning("Address not found. Please enter a valid address.")
        else: 
            searching_placeholder = st.empty()
            searching_placeholder.success("Searching...")


            # Maps user-friendly category names to Geoapify API categories
            api_categories = { 
                "show all": "healthcare",
                "allergology": "healthcare.clinic_or_praxis.allergology",
                "cardiology": "healthcare.clinic_or_praxis.cardiology",
                "dentist": "healthcare.dentist",
                "dermatology": "healthcare.clinic_or_praxis.dermatology",
                "endocrinology": "healthcare.clinic_or_praxis.endocrinology",
                "gastroenterology": "healthcare.clinic_or_praxis.gastroenterology",
                "general": "healthcare.clinic_or_praxis.general",
                "gynaecology": "healthcare.clinic_or_praxis.gynaecology",
                "hospital": "healthcare.hospital",
                "occupational": "healthcare.clinic_or_praxis.occupational",
                "ophthalmology": "healthcare.clinic_or_praxis.ophthalmology",
                "orthodontics": "healthcare.dentist.orthodontics",
                "orthopaedics": "healthcare.clinic_or_praxis.orthopaedics",
                "otolaryngology": "healthcare.clinic_or_praxis.otolaryngology",
                "paediatrics": "healthcare.clinic_or_praxis.paediatrics",
                "pharmacy": "healthcare.clinic_or_praxis.pharmacy",
                "psychiatry": "healthcare.clinic_or_praxis.psychiatry",
                "pulmonology": "healthcare.clinic_or_praxis.pulmonology",
                "radiology": "healthcare.clinic_or_praxis.radiology",
                "rheumatology": "healthcare.clinic_or_praxis.rheumatology",
                "trauma": "healthcare.clinic_or_praxis.trauma",
                "urology": "healthcare.clinic_or_praxis.urology",
                "vascular surgery": "healthcare.clinic_or_praxis.vascular_surgery",
            }


            # Gets the API category for the selected service
            categories_param = api_categories.get(categories.lower())

            # Calculates total number of results to request from the API
            total_request_limit = int(results_amount)


            # Prepares API request parameters
            params = {
                "categories": categories_param,
                "filter": f"circle:{location.longitude},{location.latitude},{distance}",
                "bias": f"proximity:{location.longitude},{location.latitude}",
                "limit": int(total_request_limit), 
                "apiKey": GEOAPIFY_API_KEY
            }

            # Sends request to Geoapify API
            url = "https://api.geoapify.com/v2/places"
            response = requests.get(url, params=params)
            results = response.json()
            features = results.get("features", [])


            # Sorts features by distance
            sorted_features = sorted(features, key=lambda x: x['properties']['distance'])
            top_results = sorted_features[:int(results_amount)] 

            # Clears the searching placeholder 
            searching_placeholder.empty()

            # Displays results (nearby places), or a message if no results are found
            if not top_results:
                st.subheader("No healthcare services found.")
                st.write("Please try a different location or adjust your search criteria.")
            else: 
                searching_placeholder.empty()
                st.subheader("Nearby Healthcare Services")
                st.write("---")
                for feature in top_results: 
                    st.write(f"**Name**: {feature['properties'].get('name', 'N/A')}")
                    st.write(f"**Address**: {feature['properties'].get('formatted', 'N/A')}")
                    st.write(f"**Distance**: {feature['properties'].get('distance', 'N/A')} meters")
                    st.write("---")
