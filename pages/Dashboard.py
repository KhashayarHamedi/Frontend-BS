import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="BetterSave Energy Dashboard", layout="wide")

# Load Data
@st.cache_data(ttl=3600)
def load_data():
    gen_file = "energy_generation_preprocessed.csv"
    cons_file = "energy_consumption_preprocessed.csv"

    energy_gen = pd.read_csv(gen_file)
    energy_cons = pd.read_csv(cons_file)

    # Convert dates
    energy_gen["Start date"] = pd.to_datetime(energy_gen["Start date"], errors="coerce")
    energy_cons["Start date"] = pd.to_datetime(energy_cons["Start date"], errors="coerce")

    return energy_gen, energy_cons

energy_generation, energy_consumption = load_data()

# Extract Key Metrics
total_consumption = energy_consumption["Total (grid load) [MWh] Calculated resolutions"].sum()
total_generation = energy_generation.iloc[:, 3:].apply(pd.to_numeric, errors='coerce').sum().sum()  # Sum of all energy sources

# Group by Year and Sum Only Numeric Columns
energy_consumption["Year"] = energy_consumption["Start date"].dt.year
energy_generation["Year"] = energy_generation["Start date"].dt.year
consumption_by_year = energy_consumption.groupby("Year").sum(numeric_only=True)
generation_by_year = energy_generation.groupby("Year").sum(numeric_only=True)

# Find the Year with Highest Consumption and Generation
highest_consumption_year = consumption_by_year["Total (grid load) [MWh] Calculated resolutions"].idxmax()
highest_generation_year = generation_by_year.sum(axis=1).idxmax()

efficiency_ratio = (total_generation / total_consumption) * 100

# Sidebar Filters
st.sidebar.header("Filters")
year_selection = st.sidebar.slider("Select Year Range:", int(energy_consumption["Year"].min()), int(energy_consumption["Year"].max()), (2015, 2019))

# Filter Data
filtered_energy_gen = energy_generation[(energy_generation["Year"] >= year_selection[0]) & (energy_generation["Year"] <= year_selection[1])]
filtered_energy_cons = energy_consumption[(energy_consumption["Year"] >= year_selection[0]) & (energy_consumption["Year"] <= year_selection[1])]

# Custom CSS for Light Theme with Dark Text
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            color: black;
        }
        .stApp {
            background-color: #ffffff;
        }
        .st-emotion-cache-t1wise {
            padding: 1.5rem 5rem 10rem !important;
        }
        .metric-container, .chart-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            margin: 10px;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 24px;
            color: black;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* Soft Shadow Effect */
            background: linear-gradient(135deg, #f0f0f0, #dcdcdc); /* Light Background */
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .metric-container:hover, .chart-container:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

# Main Dashboard
st.title("BetterSave Energy Dashboard")
st.markdown("<h2 style='text-align: center; color: black;'>Key Metrics</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

col1.markdown(f"""
    <div class="metric-container">
        <div>Total Energy Consumption</div>
        <div>{total_consumption:,.0f} MWh</div>
    </div>
""", unsafe_allow_html=True)

col2.markdown(f"""
    <div class="metric-container">
        <div>Total Energy Generation</div>
        <div>{total_generation:,.0f} MWh</div>
    </div>
""", unsafe_allow_html=True)

col3.markdown(f"""
    <div class="metric-container">
        <div>Efficiency</div>
        <div>{efficiency_ratio:.2f}%</div>
    </div>
""", unsafe_allow_html=True)


tab1, tab2 = st.tabs(["Energy Consumption vs. Generation Over Time", "Total Energy Generation by Source"])
# Consumption vs. Generation Over Time
with tab1:
    st.markdown("### Energy Consumption vs. Generation Over Time")

    filtered_trends = pd.DataFrame({
        "Year": consumption_by_year.loc[year_selection[0]:year_selection[1]].index,
        "Consumption": consumption_by_year.loc[year_selection[0]:year_selection[1], "Total (grid load) [MWh] Calculated resolutions"].values,
        "Generation": generation_by_year.loc[year_selection[0]:year_selection[1]].sum(axis=1).values
    })

    filtered_trends_melted = filtered_trends.melt(id_vars=["Year"], var_name="Type", value_name="MWh")

    fig = px.line(
        filtered_trends_melted,
        x="Year",
        y="MWh",
        color="Type",
        title="Annual Energy Trends",
        markers=True,
        template="plotly_white"
    )
    fig.update_xaxes(type='category')

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Energy Source Contribution
    st.markdown("### Energy Source Contribution")
    numeric_generation = energy_generation.drop(columns=["Start date", "End date", "Unnamed: 0", "Year"], errors='ignore').apply(pd.to_numeric, errors='coerce')
    generation_sources = numeric_generation.sum().sort_values(ascending=False)

    fig_pie = px.pie(
        names=generation_sources.index.str.replace(" \[MWh\] Calculated resolutions", ""),
        values=generation_sources.values,
        title="Total Energy Generation by Source",
        template="plotly_white"
    )

    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("---")
    st.markdown("Powered by BetterSave - Smarter Energy Decisions")
