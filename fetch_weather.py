import requests
import json
from math import exp

# --- Functions to calculate feels like --- #

def wind_chill(T, V_kmh):
    """Wind Chill formula (for Ta <= 10°C)"""
    return 13.12 + 0.6215*T - 11.37*V_kmh**0.16 + 0.3965*T*V_kmh**0.16

def heat_index(T, RH):
    """Heat Index formula (for Ta >= 20°C and RH >= 40%)"""
    HI = (-8.784695 + 1.61139411*T + 2.338549*RH 
          - 0.14611605*T*RH - 0.012308094*T**2 
          - 0.016424828*RH**2 + 0.002211732*T**2*RH 
          + 0.00072546*T*RH**2 - 0.000003582*T**2*RH**2)
    return HI

def apparent_temperature(T, RH, V_ms):
    """Australian Apparent Temperature"""
    # water vapor pressure
    rho = (RH / 100) * 6.105 * exp((17.27*T) / (237.7 + T))
    AT = T + 0.33*rho - 0.7*V_ms - 4
    return AT

# --- Fetch data --- #

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
Ta = current['temperature']             # Ambient temp °C
V_kmh = current['windspeed']            # Wind km/h
V_ms = V_kmh / 3.6                      # Convert to m/s

# Find matching RH for current_weather time
current_time = current['time']
hour_index = data['hourly']['time'].index(current_time)
RH = data['hourly']['relativehumidity_2m'][hour_index]

# --- Decide which formula to use --- #
if Ta <= 10:
    feels_like = round(wind_chill(Ta, V_kmh), 1)
elif Ta >= 20 and RH >= 40:
    feels_like = round(heat_index(Ta, RH), 1)
else:
    feels_like = round(apparent_temperature(Ta, RH, V_ms), 1)

# --- Build JSON --- #
weather_data = {
    "city": city_name,
    "current_temp": Ta,
    "current_windspeed": V_kmh,
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

# --- Write JSON --- #
with open(f"data/{city_name.lower().replace(' ','_')}.json", "w") as f:
    json.dump(weather_data, f, indent=2)

print(f"Weather data for {city_name} updated with correct 'feels like'.")
