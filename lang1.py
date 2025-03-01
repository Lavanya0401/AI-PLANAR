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
        {"mode": "Cab", "cost": 1500, "duration": "3h"},
        {"mode": "Train", "cost": 800, "duration": "2.5h"},
        {"mode": "Bus", "cost": 600, "duration": "4h"},
        {"mode": "Flight", "cost": 5000, "duration": "1h"},
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

st.set_page_config(page_title="AI Travel Planner", layout="wide")
st.title(" VoyageAI ")
st.markdown("Plan your journey with AI-powered recommendations.")

col1, col2 = st.columns([1, 1])
with col1:
    source = st.text_input("Enter Source Location:")
with col2:
    destination = st.text_input("Enter Destination Location:")
travel_date = st.date_input("Select Travel Date:")

if st.button("Get Travel Options"):
    if source and destination:
        options = get_travel_options(source, destination)
        st.subheader("Available Travel Options (₹)")
        for option in options:
            st.write(f"**Mode:** {option['mode']}")
            st.write(f"**Cost:** ₹{option['cost']}")
            st.write(f"**Duration:** {option['duration']}")
            st.markdown("---")
        
        travel_recommendation = get_travel_recommendation(source, destination, travel_date)
        st.subheader("AI-Generated Travel Recommendations")
        st.write(travel_recommendation)
    else:
        st.warning("Please enter both source and destination.")
