import streamlit as st
import requests
from datetime import datetime

api_key = st.secrets[""API_KEY""]

current_url = "https://api.openweathermap.org/data/2.5/weather"
forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

st.set_page_config(page_title="Advanced Weather App", page_icon="🌦️", layout="wide")

st.title("🌦️ Advanced Weather Dashboard")
st.caption("Live weather data powered by OpenWeather")

if "history" not in st.session_state:
    st.session_state.history = []

city = st.text_input("Enter City Name")

if st.button("Get Weather"):

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        # Current weather
        response = requests.get(current_url, params=params)
        data = response.json()

        if response.status_code == 200:

            if city not in st.session_state.history:
                st.session_state.history.append(city)

            st.success("Weather Loaded Successfully ✅")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🌡️ Temperature", f"{data['main']['temp']} °C")

            with col2:
                st.metric("💧 Humidity", f"{data['main']['humidity']} %")

            with col3:
                st.metric("💨 Wind Speed", f"{data['wind']['speed']} m/s")

            st.subheader(f"📍 {data['name']}, {data['sys']['country']}")
            st.write(f"🌥️ Condition: {data['weather'][0]['description']}")
            st.write(f"🥵 Feels Like: {data['main']['feels_like']} °C")
            st.write(f"🧭 Pressure: {data['main']['pressure']} hPa")

            sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset = datetime.fromtimestamp(data["sys"]["sunset"])

            st.write(f"🌅 Sunrise: {sunrise.strftime('%I:%M %p')}")
            st.write(f"🌇 Sunset: {sunset.strftime('%I:%M %p')}")

            # Forecast
            st.subheader("📅 Forecast Preview")

            f_response = requests.get(forecast_url, params=params)
            f_data = f_response.json()

            for item in f_data["list"][:5]:
                time = item["dt_txt"]
                temp = item["main"]["temp"]
                condition = item["weather"][0]["description"]

                st.write(f"🕒 {time} | 🌡️ {temp}°C | 🌥️ {condition}")

        else:
            st.error(data["message"])

    except Exception as e:
        st.error(f"Network Error: {e}")

# Sidebar history
st.sidebar.title("🔍 Search History")

for item in st.session_state.history:
    st.sidebar.write(item)
