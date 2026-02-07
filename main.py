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

metrics = st.slider("Distance (meters):", 1, 20000, 10000)
queries = st.number_input("Results:", min_value=1, max_value=20, value=10)
category = st.multiselect(
    "Healthcare services:", 
    ["Hospital", 
     "Dentist", 
     "Pharmacy", 
     "Orthodontics",
     "Allergology",
     "Cardiology",
     "Dermatology",
     "Endocrinology",
     "Gastroenterology",
     "General",
     "Gynaecology",
     "Occupational",
     "Ophthalmology",
     "Orthopaedics",
     "Otolaryngology",
     "Paediatrics",
     "Psychiatry",
     "Pulmonology",
     "Radiology",
     "Rheumatology",
     "Trauma",
     "Urology",
     "Vascular Surgery"
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

            categories = { 
                "hospital": "healthcare.hospital",
                "dentist": "healthcare.dentist",
                "pharmacy": "healthcare.pharmacy",
                "orthodontics": "healthcare.orthodontics",
                "allergology": "healthcare.allergology",
                "cardiology": "healthcare.cardiology",
                "dermatology": "healthcare.dermatology",
                "endocrinology": "healthcare.endocrinology",
                "gastroenterology": "healthcare.gastroenterology",
                "general": "healthcare.general",
                "gynaecology": "healthcare.gynaecology",
                "occupational": "healthcare.occupational",
                "ophthalmology": "healthcare.ophthalmology",
                "orthopaedics": "healthcare.orthopaedics",
                "otolaryngology": "healthcare.otolaryngology",
                "paediatrics": "healthcare.paediatrics",
                "psychiatry": "healthcare.psychiatry",
                "pulmonology": "healthcare.pulmonology",
                "radiology": "healthcare.radiology",
                "rheumatology": "healthcare.rheumatology",
                "trauma": "healthcare.trauma",
                "urology": "healthcare.urology",
                "vascular_surgery": "healthcare.vascular_surgery"
            }

            if not category:
                categories_param = "healthcare"
            else:
                categories_param = ",".join([categories[c.lower()] for c in category])

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
