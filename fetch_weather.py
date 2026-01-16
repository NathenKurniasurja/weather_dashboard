import requests
import json
from datetime import datetime, timedelta

# Replace with your city
city_name = "Melbourne"
lat = "-37.8136"  
lon = "144.9631"  

# Open-Meteo API request
url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    "&current_weather=true"
    "&hourly=temperature_2m,weathercode,precipitation,uv_index"
    "&daily=sunset"
    "&forecast_hours=12"
    "&timezone=auto"
)

response = requests.get(url)
data = response.json()

# Build 12-hour forecast entries
forecast_12h = []
hourly = data["hourly"]

for i in range(12):
    forecast_12h.append({
        "time": hourly["time"][i],
        "temperature": hourly["temperature_2m"][i],
        "weather_code": hourly["weathercode"][i],
        "precipitation_mm": hourly["precipitation"][i],
        "uv_index": hourly["uv_index"][i]
    })

current_temp = data["current_weather"]["temperature"]
current_windspeed = data["current_weather"]["windspeed"]
current_condition = data["current_weather"]["weathercode"]
today_sunset = data["daily"]["sunset"][0]

# Final weather object
weather_data = {
    "city": city_name,
    "current_temp": current_temp,
    "current_windspeed": current_windspeed,
    "current_condition": current_condition,
    "today_sunset": today_sunset,
    "forecast_12h": forecast_12h
}

# Write JSON to GitHub Pages data folder
filename = city_name.lower().replace(" ", "_")
with open(f"data/{filename}.json", "w") as f:
    json.dump(weather_data, f, indent=2)

print(f"Weather data for {city_name} updated.")
