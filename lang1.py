import streamlit as st
import google.generativeai as genai
import json
import numpy as np
import pandas as pd
from datetime import datetime
import requests
import os
from dotenv import load_dotenv 

# Load environment variables
load_dotenv()

# Configure Google Gemini API with your API key
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
SYSTEM_PROMPT = "Provide only the booking links for travel options."
model = genai.GenerativeModel("gemini-2.0-flash-exp", system_instruction=SYSTEM_PROMPT)

def get_travel_recommendation(source, destination, travel_date):
    prompt = f"""
    Plan a trip from {source} to {destination} on {travel_date}.
    Suggest travel options including cab, bus, train, and flights.
    Provide estimated prices for each option.
    Format the response in a structured way.
    Only provide the booking links for each option without listing travel details again.
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

st.markdown('<p class="title">Explorely AI🧳 - Your AI Travel Assistant 🚀</p>', unsafe_allow_html=True)
st.markdown("Plan your journey with AI-powered recommendations. ✨")

col1, col2 = st.columns([1, 1])
with col1:
    source = st.text_input("📍 Enter Source Location:")
with col2:
    destination = st.text_input("📍 Enter Destination Location:")
travel_date = st.date_input("📅 Select Travel Date:")

if st.button("🎒 Get Travel Options"):
    if not source or not destination:
        st.warning("⚠️ Please enter both source and destination.")
    elif source.lower() == destination.lower():
        st.error("⚠️ Source and Destination cannot be the same.")
    elif travel_date < datetime.today().date():
        st.error("⚠️ Please select a future travel date.")
    else:
        travel_recommendation = get_travel_recommendation(source, destination, travel_date)
        if not travel_recommendation or "Invalid" in travel_recommendation:
            st.error("⚠️ AI response error: Invalid data received.")
        else:
            st.subheader("🔮 AI-Generated Travel Recommendations")
            st.write(travel_recommendation)
