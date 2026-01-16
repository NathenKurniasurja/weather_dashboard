import requests
import json
from datetime import datetime, timedelta

# Replace with your city
city_name = "Melbourne"
lat = "-37.8136"  
lon = "144.9631"  

# Open-Meteo example (free, no API key)
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,weathercode&current_weather=true&forecast_hours=12"

response = requests.get(url)
data = response.json()

# Combine current + 12-hour forecast
weather_data = {
    "city": city_name,
    "current": data.get("current_weather"),
    "forecast_12h": data.get("hourly")  # 12-hour hourly forecast
}

# Write to JSON
with open(f"data/{city_name.lower().replace(' ','_')}.json", "w") as f:
    json.dump(weather_data, f, indent=2)

print(f"Weather data for {city_name} updated.")
