import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time

# ✅ **Page Configuration**
st.set_page_config(page_title="BetterSave Energy Dashboard", layout="wide")

# ✅ **Apply Custom CSS for Background & Font Adjustments**
st.markdown("""
    <style>
        .stApp {
            background-color: black !important;  /* Keep Dashboard Background Black */
        }
        .stSubheader, .stTitle, .stText, .stMarkdown {
            color: white !important; /* Ensure Readability */
        }
        .plotly-chart {
            font-size: 16px !important; /* Ensure Larger Font */
        }
    </style>
""", unsafe_allow_html=True)

# ✅ **Title**
st.title("📊 BetterSave Energy Dashboard")

# ✅ **Load Data**
energy_consumption = pd.read_csv("energy_consumption_preprocessed.csv")
energy_generation = pd.read_csv("energy_generation_preprocessed.csv")

# ✅ **Convert Dates to Proper Format**
energy_consumption["Start date"] = pd.to_datetime(energy_consumption["Start date"], errors="coerce")
energy_generation["Start date"] = pd.to_datetime(energy_generation["Start date"], errors="coerce")

# ✅ **Define Energy Generation Columns**
generation_columns = [
    "Biomass [MWh] Calculated resolutions",
    "Hydropower [MWh] Calculated resolutions",
    "Wind offshore [MWh] Calculated resolutions",
    "Wind onshore [MWh] Calculated resolutions",
    "Photovoltaics [MWh] Calculated resolutions",
    "Other renewable [MWh] Calculated resolutions",
    "Nuclear [MWh] Calculated resolutions",
    "Lignite [MWh] Calculated resolutions",
    "Hard coal [MWh] Calculated resolutions",
    "Fossil gas [MWh] Calculated resolutions",
    "Hydro pumped storage [MWh] Calculated resolutions",
    "Other conventional [MWh] Calculated resolutions"
]

# ✅ **Create "Total Generation" Column**
energy_generation["Total Generation (MWh)"] = energy_generation[generation_columns].sum(axis=1)

# ✅ **Group Data by Year (Ensuring No Decimals)**
consumption_yearly = energy_consumption.groupby(energy_consumption["Start date"].dt.year)["Total (grid load) [MWh] Calculated resolutions"].sum().astype(int)
generation_yearly = energy_generation.groupby(energy_generation["Start date"].dt.year)["Total Generation (MWh)"].sum().astype(int)

# ✅ **Find Highest & Lowest Consumption/Generation**
highest_consumption_year = consumption_yearly.idxmax()
lowest_consumption_year = consumption_yearly.idxmin()
highest_generation_year = generation_yearly.idxmax()
lowest_generation_year = generation_yearly.idxmin()

# ✅ **Display Key Insights in a Compact Format**
st.subheader("📌 Key Energy Insights (2015-2019)")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="🟢 Highest Consumption Year", value=f"{highest_consumption_year} ({consumption_yearly.max():,.0f} MWh)")
    st.metric(label="🔻 Lowest Consumption Year", value=f"{lowest_consumption_year} ({consumption_yearly.min():,.0f} MWh)")

with col2:
    st.metric(label="🟢 Highest Generation Year", value=f"{highest_generation_year} ({generation_yearly.max():,.0f} MWh)")
    st.metric(label="🔻 Lowest Generation Year", value=f"{lowest_generation_year} ({generation_yearly.min():,.0f} MWh)")

# ✅ **Energy Consumption & Generation Trends**
st.subheader("📈 Yearly Energy Trends")
col1, col2 = st.columns(2)

with col1:
    fig_bar_consumption = px.bar(
        x=consumption_yearly.index, y=consumption_yearly.values,
        labels={"x": "Year", "y": "Total Energy Consumption (MWh)"},
        title="Total Energy Consumption (2015-2019)",
        template="plotly_dark",
        color_discrete_sequence=["#3498db"],
        text_auto=True
    )
    st.plotly_chart(fig_bar_consumption, use_container_width=True)

with col2:
    fig_bar_generation = px.bar(
        x=generation_yearly.index, y=generation_yearly.values,
        labels={"x": "Year", "y": "Total Energy Generation (MWh)"},
        title="Total Energy Generation (2015-2019)",
        template="plotly_dark",
        color_discrete_sequence=["#e74c3c"],
        text_auto=True
    )
    st.plotly_chart(fig_bar_generation, use_container_width=True)

# ✅ **Line Chart for Trends**
fig_trend = px.line(
    x=consumption_yearly.index, y=consumption_yearly.values,
    labels={"x": "Year", "y": "Energy Consumption (MWh)"},
    title="Energy Consumption Trend (2015-2019)",
    template="plotly_dark",
    color_discrete_sequence=["#2ecc71"]
)
st.plotly_chart(fig_trend, use_container_width=True)

# ✅ **Energy Balance Chart**
fig_area = px.area(
    x=generation_yearly.index, y=generation_yearly.values,
    labels={"x": "Year", "y": "Energy Generation (MWh)"},
    title="Total Energy Generation Over Years",
    template="plotly_dark",
    color_discrete_sequence=["#f1c40f"]
)
st.plotly_chart(fig_area, use_container_width=True)

# ✅ **Pie Chart for Energy Sources (with Border & Enhanced Colors)**
st.subheader("🔄 Energy Sources Breakdown (2015-2019)")
generation_totals = energy_generation[generation_columns].sum()

fig_pie = px.pie(
    values=generation_totals.values,
    names=generation_totals.index,
    title="Energy Generation by Source (2015-2019)",
    color_discrete_sequence=px.colors.qualitative.Set3,
    hole=0.3
)
fig_pie.update_traces(marker=dict(line=dict(color='black', width=2)))  # Add border to pie slices
st.plotly_chart(fig_pie, use_container_width=True)

# ✅ **Real-Time Date & Clock**
st.subheader("⏳ Real-Time Clock & Date")
clock_container = st.empty()

while True:
    now = datetime.datetime.now()
    clock_container.markdown(
        f"<h3 style='text-align:center; color:lightblue;'>🕒 {now.strftime('%H:%M:%S')}<br>📅 {now.strftime('%A, %d %B %Y')}</h3>",
        unsafe_allow_html=True
    )
    time.sleep(1)  # Update every second
