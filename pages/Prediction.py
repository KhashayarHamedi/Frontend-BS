import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# **🔹 Streamlit Page Config**
st.set_page_config(page_title="BetterSave Energy Prediction", layout="wide")

# **🔹 API URL**
API_URL = "https://bettersave-296473938693.europe-west10.run.app/predict"

# **🔹 Fetch Prediction Data**
@st.cache_data(ttl=3600)
def fetch_prediction(steps):
    params = {"steps": steps}
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        try:
            data = response.json()

            if "confidence_interval" in data:
                data["lower"] = data["confidence_interval"]["lower Residual load"]
                data["upper"] = data["confidence_interval"]["upper Residual load"]
                data.pop("confidence_interval", None)

            df = pd.DataFrame(data)

            if "Date" not in df.columns:
                df["Date"] = pd.date_range(start="2020-01-01", periods=len(df), freq="D")

            return df
        except Exception as e:
            st.error(f"Error processing data: {e}")
            return None
    else:
        st.error("Failed to fetch prediction data")
        return None

# **🔹 Custom CSS for Blinking Glow Text & Fixing Alignment**
st.markdown("""
    <style>
        @keyframes blink-glow {
            0% { opacity: 1; text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; }
            50% { opacity: 0.5; text-shadow: 0 0 15px #ff00ff, 0 0 30px #ff00ff; }
            100% { opacity: 1; text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; }
        }

        .blinking-glow-text {
            font-size: 30px;
            font-weight: bold;
            text-align: center;
            color: black;
            animation: blink-glow 2s infinite alternate;
        }

        /* Centering the Audi text properly */
        .center-text {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-top: -10px;
        }

        /* Remove the blue line that appears */
        div[data-baseweb="input"] > div {
            border: none !important;
        }

    </style>
""", unsafe_allow_html=True)

# **🔹 UI Setup**
st.markdown("<h1 style='text-align: center;'>BetterSave Energy Prediction</h1>", unsafe_allow_html=True)
st.markdown("### Energy Consumption & Generation Trend (2020)")

# **🔹 User Input: Select Prediction Range**
number_of_days = st.slider("Select Prediction Range (Days)", 1, 365, 30)

# **🔹 Fetch Data Only Once**
if "data" not in st.session_state:
    if st.button("Predict"):
        st.session_state.data = fetch_prediction(number_of_days)

# **🔹 Display Prediction Data**
if "data" in st.session_state:
    data = st.session_state.data

    data["Date"] = pd.to_datetime(data["Date"], errors='coerce')
    data = data.dropna(subset=["Date"])
    data["Year"] = data["Date"].dt.year
    data["Month"] = data["Date"].dt.strftime('%b')

    historical_data = data[data["Year"] < 2020]
    predicted_data = data[data["Year"] >= 2020]

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

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    # **🔹 Audi EV Charging Calculation**
    with col2:
        st.subheader("🔋 How Many EVs Can Be Charged?")

        total_surplus_mwh = 334.47  # MWh for 1 month
        battery_capacity_kwh = 95  # kWh for Audi e-tron 55 quattro
        total_charges = int((total_surplus_mwh * 1000) / battery_capacity_kwh)  # Convert MWh to kWh

        st.markdown(f"""
            <p class='blinking-glow-text'>
            With <b>{total_surplus_mwh:.2f} MWh</b> of surplus energy in just one month, we could fully charge approximately:
            </p>
        """, unsafe_allow_html=True)

        st.markdown(f"<h1 style='text-align: center; color: #000000; font-size: 42px;'>{total_charges}</h1>", unsafe_allow_html=True)

        st.markdown("<p class='center-text'>Audi e-tron 55 quattro EVs! 🚗⚡</p>", unsafe_allow_html=True)

    # **🔹 Separate Section for Powering Homes**
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>🏠 How Many Homes Can We Power in Germany?</h2>", unsafe_allow_html=True)

    # **Dynamic Slider (1-12 Months)**
    months = st.slider("Select Months of Surplus Energy", 1, 12, 1, key="surplus_months")

    avg_home_annual_consumption_mwh = 3.5  # Average German household yearly consumption in MWh
    total_energy_mwh = total_surplus_mwh * months
    homes_powered = int(total_energy_mwh / avg_home_annual_consumption_mwh)

    st.markdown(f"""
        <p class='blinking-glow-text'>
        With <b>{months} month(s)</b> of surplus energy, we could fully power:
        </p>
    """, unsafe_allow_html=True)

    st.markdown(f"<h1 style='text-align: center; color: #000000; font-size: 42px;'>{homes_powered} Homes</h1>", unsafe_allow_html=True)

    st.progress(min(1.0, homes_powered / 5000))

    # **🔹 Forecast Table**
    st.markdown("### 📊 Forecast Data Table")
    st.dataframe(data[["Date", "forecast", "lower", "upper"]].head(30), use_container_width=True)
