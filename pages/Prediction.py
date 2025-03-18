import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="BetterSave Energy Prediction", layout="wide")

# API URL
API_URL = "https://bettersave-296473938693.europe-west10.run.app/predict"


# Fetch Prediction Data
# @st.cache_data(ttl=3600)
def fetch_prediction():
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        try:
            data = response.json()
            data["lower"] = data["confidence_interval"]["lower Residual load"]
            data["upper"] = data["confidence_interval"]["upper Residual load"]
            data.pop("confidence_interval")
            # st.write(data)
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame.from_dict(data, orient='index').transpose()
            else:
                st.error("Unexpected API response format")
                return None

            return df
        except Exception as e:
            st.error(f"Error processing data: {e}")
            return None
    else:
        st.error("Failed to fetch prediction data")
        return None

# Load Data
st.title("BetterSave Energy Prediction Dashboard")
st.markdown("""
### Energy Consumption & Generation Trends (2015-2020)
Historical data from 2015-2019 is shown in blue, while predicted data from 2020 is highlighted in green.
""")

number_of_days = st.slider("number of days", 1, 365)
params={"steps": number_of_days}

if st.button("Predict"):
    data = fetch_prediction()
    st.write(data)
# st.write(data)
# if data is not None:
#     try:
#         data["Date"] = pd.to_datetime(data["Date"], errors='coerce')
#         data = data.dropna(subset=["Date"])  # Drop rows where 'Date' is NaT
#         data["Year"] = data["Date"].dt.year
#         data["Month"] = data["Date"].dt.strftime('%b')

#         # Separate Historical and Predicted Data
#         historical_data = data[data["Year"] < 2020]
#         predicted_data = data[data["Year"] >= 2020]

#         # Aggregate Historical Data by Year
#         historical_grouped = historical_data.groupby("Year")[["Consumption", "Generation"]].sum().reset_index()
#         predicted_grouped = predicted_data.groupby(["Year", "Month"])[["Consumption", "Generation"]].sum().reset_index()

#         # Melt Data for Plotly
#         historical_melted = historical_grouped.melt(id_vars=["Year"], var_name="Type", value_name="MWh")
#         predicted_melted = predicted_grouped.melt(id_vars=["Year", "Month"], var_name="Type", value_name="MWh")

#         # Plot Historical Data
#         fig = px.line(
#             historical_melted,
#             x="Year", y="MWh", color="Type",
#             title="Energy Trends: Historical & Predicted",
#             markers=True, template="plotly_dark"
#         )

#         # Add Predicted Data for 2020
#         for type_ in predicted_melted["Type"].unique():
#             filtered_pred = predicted_melted[predicted_melted["Type"] == type_]
#             fig.add_scatter(
#                 x=filtered_pred["Month"], y=filtered_pred["MWh"],
#                 mode="lines+markers", name=f"{type_} (Predicted)",
#                 line=dict(color="green", dash="dash")
#             )

#         st.plotly_chart(fig, use_container_width=True)
#     except Exception as e:
#         st.error(f"Error processing visualization: {e}")
# else:
#     st.error("No prediction data available")
