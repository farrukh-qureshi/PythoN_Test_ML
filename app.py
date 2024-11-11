import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

def get_weather_data(latitude, longitude, start_date, end_date):
    url = f"https://power.larc.nasa.gov/api/temporal/hourly/point"
    params = {
        "parameters": "T2M",
        "community": "SB",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_data = data['properties']['parameter']['T2M']
        df = pd.DataFrame(weather_data.items(), columns=['Date', 'Temperature'])
        return df
    else:
        st.error("Failed to retrieve data")
        return None

# Streamlit UI
st.title("Weather Data Viewer")

# Map of Pakistan to select latitude and longitude
st.subheader("Select Location on Map")
m = folium.Map(location=[30.3753, 69.3451], zoom_start=5, dragging=True, zoom_control=True)

# Adding a click-for-marker function
m.add_child(folium.LatLngPopup())

# Displaying the map
map_data = st_folium(m, width=350, height=500)

latitude = [30.3753]
longitude = [69.3451]

# Search bar for location
location = st.text_input("Enter Location (e.g. Lahore, Islamabad, etc.)")
geolocator = Nominatim(user_agent="weather_app")
if st.button("Search Location"):
    location_query = geolocator.geocode(location)
    if location_query:
        latitude = location_query.latitude
        longitude = location_query.longitude
        m.loc = [latitude, longitude]
        m.zoom_start = 12
        st.write(f"Selected Coordinates: Latitude = {latitude}, Longitude = {longitude}")

# Button to fetch and display weather data
start_date = st.text_input("Enter Start Date (YYYYMMDD)", value="20230101")
end_date = st.text_input("Enter End Date (YYYYMMDD)", value="20231231")

if st.button("Get Weather Data") and latitude is not None and longitude is not None:
    weather_df = get_weather_data(latitude, longitude, start_date, end_date)
    if weather_df is not None:
        fig = px.line(weather_df, x='Date', y='Temperature', title='Temperature Over Time')
        st.plotly_chart(fig)
else:
    st.warning("Please select a location on the map or search for a location to proceed.")

