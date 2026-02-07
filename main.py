import requests
import os
import sys
import streamlit as st
from geopy.geocoders import Nominatim

GEOAPIFY_API_KEY = "14a1a56e438e4c6c8324475d9fe9aa8e"
geolocator = Nominatim(user_agent="Healthcare Helper")
#url = "https://api.geoapify.com/v2/places?params"

st.title("Healthcare Helper")
st.subheader("Welcome to Healthcare Helper, an application to help you find healthcare services nearby.")

input = st.text_input("Enter an address :")

metrics = st.slider("Distance (meters):", 0, 5000)
queries = st.number_input("Results:", min_value=1, max_value=20, value=1)
category = st.multiselect("Healthcare services:", ["Hospital", "Dentist", "Pharmacy", "Orthodontics"])

if st.button("Search"):
    location = geolocator.geocode(input)

    categories = {  
        "hospital": "healthcare.hospital",
        "dentist": "healthcare.dentist",
        "pharmacy": "healthcare.pharmacy",
        "orthodontics": "healthcare.orthodontics"
    }

    if not category:
        categories_param = "healthcare"
    else:
        categories_param = ",".join([categories[c.lower()] for c in category])

    params = {
        "categories": categories_param,
        "filter": f"circle:{location.longitude},{location.latitude},{metrics}",
        "bias": f"proximity:{location.longitude},{location.latitude}",
        "limit": int(queries),
        "apiKey": GEOAPIFY_API_KEY
    }

    url = "https://api.geoapify.com/v2/places"
    response = requests.get(url, params=params)
    results = response.json()
    features = results.get("features", [])

    st.subheader("Nearby Healthcare Services")
    st.write("---")
    for feature in features:
        st.write(f"**Name**: {feature['properties']['name']}")
        st.write(f"**Address**: {feature['properties']['formatted']}")
        st.write(f"**Distance**: {feature['properties']['distance']} meters")
        st.write("---")
