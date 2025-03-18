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
consumption_by_year = energy_consumption.groupby(energy_consumption["Start date"].dt.year).sum(numeric_only=True)
generation_by_year = energy_generation.groupby(energy_generation["Start date"].dt.year).sum(numeric_only=True)

# Find the Year with Highest Consumption and Generation
highest_consumption_year = consumption_by_year["Total (grid load) [MWh] Calculated resolutions"].idxmax()
highest_generation_year = generation_by_year.sum(axis=1).idxmax()

efficiency_ratio = (total_generation / total_consumption) * 100

# Sidebar Filters
st.sidebar.header("Filters")
year_selection = st.sidebar.slider("Select Year Range:", int(energy_consumption["Start date"].dt.year.min()), int(energy_consumption["Start date"].dt.year.max()), (2015, 2019))

# Filter Data
filtered_energy_gen = energy_generation[(energy_generation["Start date"].dt.year >= year_selection[0]) & (energy_generation["Start date"].dt.year <= year_selection[1])]
filtered_energy_cons = energy_consumption[(energy_consumption["Start date"].dt.year >= year_selection[0]) & (energy_consumption["Start date"].dt.year <= year_selection[1])]

# Custom CSS for Dark Theme with Neon Glow
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #121212;
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
            color: white;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.8); /* Neon Glow Effect */
            background: linear-gradient(135deg, #1f1c2c, #928DAB); /* Dark Futuristic Background */
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .metric-container:hover, .chart-container:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px rgba(0, 255, 255, 1);
        }
    </style>
""", unsafe_allow_html=True)

# Main Dashboard
st.title("BetterSave Energy Dashboard")
st.markdown("<h2 style='text-align: center; color: white ;'>Key Metrics</h2>", unsafe_allow_html=True)
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
        <div>Efficiency (%)</div>
        <div>{efficiency_ratio:.2f}%</div>
    </div>
""", unsafe_allow_html=True)

# Consumption vs. Generation Over Time
st.markdown("### Energy Consumption vs. Generation Over Time")

df_trends = pd.DataFrame({
    "Year": consumption_by_year.index,
    "Consumption": consumption_by_year["Total (grid load) [MWh] Calculated resolutions"].values,
    "Generation": generation_by_year.sum(axis=1).values
})

df_trends_melted = df_trends.melt(id_vars=["Year"], var_name="Type", value_name="MWh")

fig = px.line(
    df_trends_melted,
    x="Year",
    y="MWh",
    color="Type",
    title="Annual Energy Trends",
    markers=True,
    template="plotly_dark"
)

st.markdown("""
    <div class="chart-container">
""", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""</div>""", unsafe_allow_html=True)

# Energy Source Contribution
st.markdown("### Energy Source Contribution")
# Ensure only numeric columns are summed
numeric_generation = energy_generation.drop(columns=["Start date", "End date", "Unnamed: 0", "Year"], errors='ignore').apply(pd.to_numeric, errors='coerce')

generation_sources = numeric_generation.sum().sort_values(ascending=False)
fig_pie = px.pie(
    names=generation_sources.index,
    values=generation_sources.values,
    title="Total Energy Generation by Source",
    template="plotly_dark"
)

st.markdown("""
    <div class="chart-container">
""", unsafe_allow_html=True)
st.plotly_chart(fig_pie, use_container_width=True)
st.markdown("""</div>""", unsafe_allow_html=True)

# Data Download
st.sidebar.markdown("### Download Data")
st.sidebar.download_button("Download Consumption Data", data=filtered_energy_cons.to_csv(index=False), file_name="filtered_consumption.csv", mime="text/csv")
st.sidebar.download_button("Download Generation Data", data=filtered_energy_gen.to_csv(index=False), file_name="filtered_generation.csv", mime="text/csv")

st.markdown("---")
st.markdown("Powered by BetterSave - Smarter Energy Decisions")
