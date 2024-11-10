import requests
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

def get_weather_data(latitude, longitude, start_date, end_date):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "T2M,RH2M,PRECTOTCORR,WS2M,GWETTOP,GWETROOT,GWETPROF",
        # "parameters": "T2M,RH2M,PS,WS2M",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        parameter_data = data['properties']['parameter']
        df = pd.DataFrame()
        for key, value in parameter_data.items():
            df[key] = list(value.values())
        df['Date'] = list(parameter_data['T2M'].keys())
        return df
    else:
        print("Failed to retrieve data")
        return None

def main():
    geolocator = Nominatim(user_agent="weather_app")
    location = input("Enter Location (e.g. Lahore, Islamabad, etc.): ") or "Lahore"
    location_query = geolocator.geocode(location)
    if location_query:
        latitude = location_query.latitude
        longitude = location_query.longitude
        print(f"Selected Coordinates: Latitude = {latitude}, Longitude = {longitude}")
        start_date = input("Enter Start Date (YYYYMMDD): ") or "20140101"
        end_date = input("Enter End Date (YYYYMMDD): ") or "20240101"
        weather_df = get_weather_data(latitude, longitude, start_date, end_date)
        if weather_df is not None:
            weather_df.to_csv(f"{location}_{start_date}_{end_date}.csv", index=False)
            print(f"Data saved to {location}_{start_date}_{end_date}.csv")
        else:
            print("Please select a location to proceed.")
    else:
        print("Invalid location")

if __name__ == "__main__":
    main()

