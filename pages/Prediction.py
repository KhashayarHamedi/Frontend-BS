import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# **🔹 Streamlit Page Config**
st.set_page_config(page_title="BetterSave Energy Prediction", layout="wide")

# **🔹 API URL**
API_URL = "https://bettersave-296473938693.europe-west10.run.app/predict"

# **🔹 Fetch Prediction Data**
def fetch_prediction(steps):
    params = {"steps": steps}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        try:
            data = response.json()

            # Handle missing confidence intervals
            if "confidence_interval" in data:
                data["lower"] = data["confidence_interval"]["lower Residual load"]
                data["upper"] = data["confidence_interval"]["upper Residual load"]
                data.pop("confidence_interval", None)

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # **🔹 Handle Missing 'Date' Column**
            if "Date" not in df.columns:
                # st.warning("⚠ No 'Date' column found. Creating synthetic dates...")
                df["Date"] = pd.date_range(start="2020-01-01", periods=len(df), freq="D")
            st.write(df)
            # for index, row in df:
            #     accumlated_noise = 0.001
            #     row["forecast"] = row["forecast"] + (random.randint(0,15) / 100)
            #     accumlated_noise += 0.001
            return df
        except Exception as e:
            st.error(f"Error processing data: {e}")
            return None
    else:
        st.error("Failed to fetch prediction data")
        return None

# **🔹 UI Setup**
st.markdown("<h1 style='text-align: center;'>BetterSave Energy Prediction</h1>", unsafe_allow_html=True)
st.markdown("""
### Energy Consumption & Generation Trends (2015-2020)
- **Historical Data (2015-2019):** Shown in **blue**.
- **Predicted Data (2020+):** Shown in **green** with a **shaded confidence interval**.
""")

# **🔹 User Input: Select Prediction Range**
number_of_days = st.slider("Select Prediction Range (Days)", 1, 365, 30)

# **🔹 Fetch & Display Data on Button Click**
if st.button("Predict"):
    data = fetch_prediction(number_of_days)

    if data is not None:
        # Convert 'Date' and extract Year/Month
        data["Date"] = pd.to_datetime(data["Date"], errors='coerce')
        data = data.dropna(subset=["Date"])  # Remove invalid dates
        data["Year"] = data["Date"].dt.year
        data["Month"] = data["Date"].dt.strftime('%b')

        # **🔹 Separate Historical (2015-2019) and Predicted (2020+)**
        historical_data = data[data["Year"] < 2020]
        predicted_data = data[data["Year"] >= 2020]

        # **🔹 Create Figure**
        fig = go.Figure()

        # **🔹 Historical Data (Blue Line)**
        if not historical_data.empty:
            fig.add_trace(go.Scatter(
                x=historical_data["Year"],
                y=historical_data["forecast"],
                mode="lines+markers",
                name="Historical Forecast",
                line=dict(color="blue", width=3)
            ))

        # **🔹 Predicted Data (Green Dashed Line)**
        if not predicted_data.empty:
            fig.add_trace(go.Scatter(
                x=predicted_data["Date"],
                y=predicted_data["forecast"],
                mode="lines+markers",
                name="Predicted Forecast",
                line=dict(color="green", dash="dash", width=3)
            ))

            # **🔹 Confidence Interval (Shaded Area)**
            fig.add_trace(go.Scatter(
                x=predicted_data["Date"].tolist() + predicted_data["Date"].tolist()[::-1],
                y=predicted_data["upper"].tolist() + predicted_data["lower"].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(0,255,0,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name="Confidence Interval"
            ))

        # **🔹 Custom X-Axis Formatting**
        fig.update_layout(
            title="Energy Trends: Historical vs. Predicted",
            xaxis_title="Year / Month",
            yaxis_title="MWh",
            template="plotly_white",
            xaxis=dict(
                tickmode='array',
                tickvals=data["Date"],
                ticktext=[f"{m} {y}" if y == 2020 else str(y) for y, m in zip(data["Year"], data["Month"])]
            )
        )

        col1, col2 = st.columns((3,1))
        # **🔹 Show Chart**
        with col1:
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("HOW MANY ")
