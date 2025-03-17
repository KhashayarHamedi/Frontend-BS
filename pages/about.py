import streamlit as st

# Set a unique background color for the About page
st.markdown("""
    <style>
        .stApp {
            background-color: #a3c1ad; /* Cambridge Blue */
        }
    </style>
""", unsafe_allow_html=True)

st.title("What is BetterSave?")

st.markdown("""
BetterSave is an **AI-powered Energy Storage-as-a-Service platform** that predicts energy surplus and optimizes its distribution.
Our technology ensures that excess energy is **not wasted** but **redirected efficiently** to where it's needed most—starting with **EV charging stations across Germany**.
BetterSave transforms energy grids into **smart, adaptive ecosystems** that balance supply and demand intelligently.

## Why BetterSave?
Germany generates significant **energy surpluses** from solar, wind, and other renewables. However, **without efficient local storage solutions**, much of this energy is wasted or sold at low prices.
Small businesses, residential buildings, and EV stations **lack access to affordable, surplus power** at the right time.
BetterSave provides a **data-driven AI solution** to bridge this gap and optimize energy flows.

## Future Vision: The Next Phase of BetterSave
- **Real-time Energy Distribution**: Automatically redirect surplus power to EV charging stations and businesses.
- **Hydrogen & Battery Storage Expansion**: Enable surplus energy storage for long-term sustainability.
- **AI-Driven Energy Marketplace**: Businesses and residential units can trade surplus energy on demand.

---

<p style='text-align: center; color: gray;'>© 2025 BetterSave - AI for Energy</p>
""", unsafe_allow_html=True)
