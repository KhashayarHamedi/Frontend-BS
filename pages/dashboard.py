import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time

# Set page title
st.title("BetterSave Energy Dashboard")

# Load Data
energy_consumption = pd.read_csv("energy_consumption_preprocessed.csv")
energy_generation = pd.read_csv("energy_generation_preprocessed.csv")

# Convert "Start date" column to datetime format
energy_consumption["Start date"] = pd.to_datetime(energy_consumption["Start date"], errors="coerce")
energy_generation["Start date"] = pd.to_datetime(energy_generation["Start date"], errors="coerce")

# Define Energy Generation Columns
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

# Create "Total Generation" Column
energy_generation["Total Generation (MWh)"] = energy_generation[generation_columns].sum(axis=1)

# Group Data by Year
consumption_yearly = energy_consumption.groupby(energy_consumption["Start date"].dt.year)["Total (grid load) [MWh] Calculated resolutions"].sum()
generation_yearly = energy_generation.groupby(energy_generation["Start date"].dt.year)["Total Generation (MWh)"].sum()

# Find Highest & Lowest Consumption/Generation
highest_consumption_year = consumption_yearly.idxmax()
lowest_consumption_year = consumption_yearly.idxmin()
highest_generation_year = generation_yearly.idxmax()
lowest_generation_year = generation_yearly.idxmin()

# **Display Key Insights in a Table**
st.subheader("📌 Key Energy Insights (2015-2019)")

data_table = pd.DataFrame({
    "Metric": [
        "🟢 Highest Consumption Year",
        "🔻 Lowest Consumption Year",
        "🟢 Highest Generation Year",
        "🔻 Lowest Generation Year"
    ],
    "Year": [
        highest_consumption_year,
        lowest_consumption_year,
        highest_generation_year,
        lowest_generation_year
    ],
    "Value (MWh)": [
        f"{consumption_yearly.max():,.0f}",
        f"{consumption_yearly.min():,.0f}",
        f"{generation_yearly.max():,.0f}",
        f"{generation_yearly.min():,.0f}"
    ]
})

st.dataframe(data_table.style.set_properties(**{
    'background-color': '#2C3E50',
    'color': 'white',
    'border': '1px solid white',
    'font-size': '16px',
    'text-align': 'center'
}))

# **📊 Visualizing Key Metrics**
st.subheader("📈 Yearly Energy Insights")

# **Bar Chart for Key Metrics**
key_metrics_data = pd.DataFrame({
    "Metric": [
        "Highest Consumption",
        "Lowest Consumption",
        "Highest Generation",
        "Lowest Generation"
    ],
    "Year": [
        highest_consumption_year,
        lowest_consumption_year,
        highest_generation_year,
        lowest_generation_year
    ],
    "Value (MWh)": [
        consumption_yearly.max(),
        consumption_yearly.min(),
        generation_yearly.max(),
        generation_yearly.min()
    ]
})

fig_bar_metrics = px.bar(
    key_metrics_data,
    x="Metric",
    y="Value (MWh)",
    text="Year",
    color="Metric",
    title="Energy Consumption & Generation Peaks (2015-2019)",
    color_discrete_map={
        "Highest Consumption": "#3498db",
        "Lowest Consumption": "#e74c3c",
        "Highest Generation": "#2ecc71",
        "Lowest Generation": "#f1c40f"
    },
    template="plotly_dark"
)
st.plotly_chart(fig_bar_metrics, use_container_width=True)

# 📊 **Visualizations of Consumption & Generation Trends**
st.subheader("📉 Energy Consumption & Generation Trends")

# **Bar Chart for Consumption**
fig_bar_consumption = px.bar(
    x=consumption_yearly.index,
    y=consumption_yearly.values,
    labels={"x": "Year", "y": "Total Energy Consumption (MWh)"},
    title="Total Energy Consumption (2015-2019)",
    template="plotly_dark",
    color_discrete_sequence=["#3498db"]
)
st.plotly_chart(fig_bar_consumption, use_container_width=True)

# **Bar Chart for Generation**
fig_bar_generation = px.bar(
    x=generation_yearly.index,
    y=generation_yearly.values,
    labels={"x": "Year", "y": "Total Energy Generation (MWh)"},
    title="Total Energy Generation (2015-2019)",
    template="plotly_dark",
    color_discrete_sequence=["#e74c3c"]
)
st.plotly_chart(fig_bar_generation, use_container_width=True)

# **Line Chart for Trends**
fig_trend = px.line(
    x=consumption_yearly.index,
    y=consumption_yearly.values,
    labels={"x": "Year", "y": "Energy Consumption (MWh)"},
    title="Energy Consumption Trend",
    template="plotly_dark",
    color_discrete_sequence=["#2ecc71"]
)
st.plotly_chart(fig_trend, use_container_width=True)

# **Area Chart for Energy Balance**
fig_area = px.area(
    x=generation_yearly.index,
    y=generation_yearly.values,
    labels={"x": "Year", "y": "Energy Generation (MWh)"},
    title="Total Energy Generation Over Years",
    template="plotly_dark",
    color_discrete_sequence=["#f1c40f"]
)
st.plotly_chart(fig_area, use_container_width=True)

# **Pie Chart for Energy Sources**
st.subheader("🔄 Energy Sources Breakdown (2015-2019)")
generation_totals = energy_generation[generation_columns].sum()

fig_pie = px.pie(
    values=generation_totals.values,
    names=generation_totals.index,
    title="Energy Generation by Source (2015-2019)",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_pie, use_container_width=True)

# **📅 Real-Time Date & Clock**
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("⏳ Real-Time Clock & Date")

# Create a container for live updating clock
clock_container = st.empty()

while True:
    now = datetime.datetime.now()
    clock_container.markdown(
        f"<h3 style='text-align:center; color:lightblue;'>🕒 {now.strftime('%H:%M:%S')} | 📅 {now.strftime('%A, %d %B %Y')}</h3>",
        unsafe_allow_html=True
    )
    time.sleep(1)  # Update every second
