import requests
import json
from math import exp

# Replace with your city
city_name = "Melbourne"
lat = "-37.8136"
lon = "144.9631"

url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}"
    "&current_weather=true"
    "&hourly=temperature_2m,weathercode,precipitation,uv_index,windspeed_10m,relativehumidity_2m"
    "&daily=sunset"
    "&forecast_hours=12"
    "&timezone=auto"
)

response = requests.get(url)
data = response.json()

current = data['current_weather']
Ta = current['temperature']           # Ambient temp °C
omega = current['windspeed'] / 3.6    # Convert km/h to m/s (if Open-Meteo gives km/h)
RH = data['hourly']['relativehumidity_2m'][0]  # Use current hour

# Water vapor pressure (hPa)
rho = (RH / 100) * 6.105 * exp((17.27 * Ta) / (237.7 + Ta))

# Apparent temperature (feels like)
feels_like = round(Ta + 0.33*rho - 0.7*omega - 4, 1)

# Build JSON
weather_data = {
    "city": city_name,
    "current_temp": Ta,
    "current_windspeed": current['windspeed'],
    "current_condition": current['weathercode'],
    "feels_like": feels_like,
    "today_sunset": data['daily']['sunset'][0],
    "forecast_12h": [
        {
            "time": t,
            "temperature": temp,
            "precipitation_mm": prec,
            "uv_index": uv
        }
        for t, temp, prec, uv in zip(
            data['hourly']['time'],
            data['hourly']['temperature_2m'],
            data['hourly']['precipitation'],
            data['hourly']['uv_index']
        )
    ]
}

# Write JSON
with open(f"data/{city_name.lower().replace(' ','_')}.json", "w") as f:
    json.dump(weather_data, f, indent=2)

print(f"Weather data for {city_name} updated with Apparent Temperature.")
