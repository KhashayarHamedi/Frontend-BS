import streamlit as st
import requests
import plotly.express as px

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# Fetch data from the backend
def fetch_data():
    response = requests.get(f"{BACKEND_URL}/")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Streamlit App
st.set_page_config(page_title="BetterSave Dashboard", layout="wide")

# Add a background color
st.markdown("""
    <style>
    .main {
        background-color: #f4f4f4;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 BetterSave Energy Dashboard")

# Fetch and Display Data
data = 

if data:
    st.subheader("Energy Mix Overview")
    fig = px.pie(names=data["labels"], values=data["values"], title="Energy Source Distribution", color_discrete_sequence=data["colors"])
    st.plotly_chart(fig)

    # Prediction Button
    if st.button("Click for Prediction"):
        st.write("Predictions will be displayed here soon!")
else:
    st.error("Failed to fetch data from backend.")
