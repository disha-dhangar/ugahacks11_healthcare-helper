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
location = geolocator.geocode(input)

if st.button("Search"):
    params = {
        "categories": "healthcare",
        "filter": f"circle:{location.longitude},{location.latitude},5000",
        "bias": f"proximity:{location.longitude},{location.latitude}",
        "limit": 15,
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
