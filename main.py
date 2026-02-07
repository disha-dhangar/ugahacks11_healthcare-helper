import requests
import os
import sys
import streamlit as st
from geopy.geocoders import Nominatim


GEOAPIFY_API_KEY = "14a1a56e438e4c6c8324475d9fe9aa8e"
geolocator = Nominatim(user_agent="Healthcare Helper")
#url = "https://api.geoapify.com/v2/places?params"

st.title("Healthcare Helper")
st.subheader("Welcome to Healthcare Helper, an application to help you find healthcare services nearby easily and efficiently.")
st.write("Simply enter an address below to get started. You may filter out the results using the options provided.")
st.write("---")

input = st.text_input("Enter an address :")

metrics = st.slider("Distance (meters):", 0, 20000, 10000)
queries = st.number_input("Results:", min_value=1, max_value=20, value=10)
category = st.selectbox(
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

if st.button("Search"):
    if not input.strip():
        st.warning("Please enter an address.")
    else: 
        location = geolocator.geocode(input)

        if not location:
            st.warning("Address not found. Please enter a valid address.")
        else: 
            searching_placeholder = st.empty()
            searching_placeholder.success("Searching...")

            categories = { #ORIGINALLY LOWER CASE
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
                "vascular surgery": "healthcare.clinic_or_praxis.vascular surgery",
            }

            categories_param = categories.get(category.lower())

            requested_per_category = int(queries)
            total_request_limit = min(requested_per_category * max(1, len(category)), 50)

            params = {
                "categories": categories_param,
                "filter": f"circle:{location.longitude},{location.latitude},{metrics}",
                "bias": f"proximity:{location.longitude},{location.latitude}",
                "limit": int(total_request_limit), 
                "apiKey": GEOAPIFY_API_KEY
            }

            url = "https://api.geoapify.com/v2/places"
            response = requests.get(url, params=params)
            results = response.json()
            features = results.get("features", [])

            #DEBUGGING
            #st.write("Request URL:", response.url)
            #st.write("Request params (no API key shown):", {k: v for k, v in params.items() if k != "apiKey"})
            #st.write("Status code:", response.status_code)

            sorted_features = sorted(features, key=lambda x: x['properties']['distance'])
            top_results = sorted_features[:int(queries)] 

            searching_placeholder.empty()
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


# ADD CLEAR BUTTON