import streamlit as st
import google.generativeai as genai
from datetime import datetime
import requests
import os
from dotenv import load_dotenv 

# Configure Google Gemini API with your API key
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

def get_travel_options(source, destination):
    options = [
        {"mode": "🚖 Cab", "cost": 1500, "duration": "3h", "link": "https://www.uber.com/in/en/"},
        {"mode": "🚆 Train", "cost": 800, "duration": "2.5h", "link": "https://www.irctc.co.in"},
        {"mode": "🚌 Bus", "cost": 600, "duration": "4h", "link": "https://www.redbus.in"},
        {"mode": "✈️ Flight", "cost": 5000, "duration": "1h", "link": "https://www.makemytrip.com/flights/"},
    ]
    return options

def get_travel_recommendation(source, destination, travel_date):
    prompt = f"""
    Plan a trip from {source} to {destination} on {travel_date}.
    Suggest travel options including cab, bus, train, and flights.
    Provide estimated prices for each option.
    Format the response in a structured way: Travel Mode | Duration | Estimated Cost.
    """
    response = model.generate_content(prompt)
    return response.text if response else "No recommendation available."

st.set_page_config(page_title="🧳 Explorely AI - Travel Planner", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4A90E2;
        }
        .subheader {
            font-size: 24px;
            font-weight: bold;
            color: #333333;
        }
        .travel-option {
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="title">Explorely AI🧳 - Your AI Travel Assistant </p>', unsafe_allow_html=True)
st.markdown("Plan your journey with AI-powered recommendations. ✨")

col1, col2 = st.columns([1, 1])
with col1:
    source = st.text_input("📍 Enter Source Location:")
with col2:
    destination = st.text_input("📍 Enter Destination Location:")
travel_date = st.date_input("📅 Select Travel Date:")

if st.button("🎒   Get Travel Options"):
    if not source or not destination:
        st.warning("⚠️ Please enter both source and destination.")
    elif source.lower() == destination.lower():
        st.error("⚠️ Source and Destination cannot be the same.")
    elif travel_date < datetime.today().date():
        st.error("⚠️ Please select a future travel date.")
    else:
        options = get_travel_options(source, destination)
        st.subheader("🛫 Available Travel Options (₹)")
        for option in options:
            st.markdown(
                f"<div class='travel-option'>"
                f"<b>Mode:</b> {option['mode']} - <a href='{option['link']}' target='_blank'>Book Now</a><br>"
                f"<b>Cost:</b> ₹{option['cost']}<br>"
                f"<b>Duration:</b> {option['duration']}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        travel_recommendation = get_travel_recommendation(source, destination, travel_date)
        if "Error" in travel_recommendation:
            st.error("⚠️ AI response error: Invalid data received.")
        else:
            st.subheader("🔮 AI-Generated Travel Recommendations")
            st.write(travel_recommendation)
