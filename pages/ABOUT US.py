import streamlit as st

# Set Animated Gradient Background with a Futuristic Twist
st.markdown("""
    <style>
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stApp {
            background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #533483);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: white;
        }

        /* Title - Solid Neon Green */
        .futuristic-title {
            color: #1eff00;
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            padding: 20px;
            font-family: 'Orbitron', sans-serif;
        }

        /* Subheading - Solid Yellow (No Glow) */
        .plain-yellow-subtitle {
            color: #fbff00;
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            padding-top: 15px;
            font-family: 'Orbitron', sans-serif;
        }

        /* Paragraph Styling */
        .paragraph {
            font-size: 18px;
            line-height: 1.8;
            text-align: justify;
            padding: 10px 20px;
            color: white;
        }

        /* Glitch Effect Keyframes for the Button Only */
        @keyframes glitch {
            0% { text-shadow: 2px 2px 0px #ff00ff, -2px -2px 0px #00ffff; }
            25% { text-shadow: -2px -2px 0px #ff00ff, 2px 2px 0px #00ffff; }
            50% { text-shadow: 2px -2px 0px #ff00ff, -2px 2px 0px #00ffff; }
            75% { text-shadow: -2px 2px 0px #ff00ff, 2px -2px 0px #00ffff; }
            100% { text-shadow: 2px 2px 0px #ff00ff, -2px -2px 0px #00ffff; }
        }

        /* Glitch Button Effect */
        .glitch-button {
            display: block;
            width: 280px;
            margin: 20px auto;
            padding: 15px 25px;
            font-size: 20px;
            text-align: center;
            font-weight: bold;
            text-decoration: none;
            color: white;
            background-color: #4afff9;
            border: none;
            border-radius: 8px;
            transition: 0.3s;
            font-family: 'Orbitron', sans-serif;
            animation: glitch 0.7s infinite alternate;
        }

        .glitch-button:hover {
            background-color: #ff0080;
            box-shadow: 0px 0px 20px rgba(255, 0, 128, 1);
            transform: scale(1.1);
        }

        /* Footer with Futuristic Design */
        .futuristic-footer {
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            padding-top: 20px;
            font-family: 'Orbitron', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Title - Solid Neon Green
st.markdown("<div class='futuristic-title'>WHAT is BetterSave?</div>", unsafe_allow_html=True)

# Introduction (Plain Text, No Box)
st.markdown("""
    <p class='paragraph'>
        BetterSave is an <b>AI-powered Energy Storage-as-a-Service platform</b> that predicts energy surplus and optimizes its distribution.
        Our technology ensures that excess energy is <b>not wasted</b> but <b>redirected efficiently</b> to where it's needed most—starting with <b>EV charging stations across Germany</b>.
        BetterSave transforms energy grids into <b>smart, adaptive ecosystems</b> that balance supply and demand intelligently.
    </p>
""", unsafe_allow_html=True)

# Why BetterSave? Section (Solid Yellow, No Glow)
st.markdown("<div class='plain-yellow-subtitle'>WHY BetterSave?</div>", unsafe_allow_html=True)
st.markdown("""
    <p class='paragraph'>
        Germany generates significant <b>energy surpluses</b> from solar, wind, and other renewables. However, <b>without efficient local storage solutions</b>, much of this energy is wasted or sold at low prices.
        Small businesses, residential buildings, and EV stations <b>lack access to affordable, surplus power</b> at the right time.
        BetterSave provides a <b>data-driven AI solution</b> to bridge this gap and optimize energy flows.
    </p>
""", unsafe_allow_html=True)

# Future Vision Section (Solid Yellow, No Glow)
st.markdown("<div class='plain-yellow-subtitle'>THE FUTURE VISION OF BetterSave</div>", unsafe_allow_html=True)
st.markdown("""
    <p class='paragraph'>
        At BetterSave, we envision a world where energy is <b>intelligently managed</b> and <b>dynamically optimized</b>.
        Our goal is to create a <b>seamless ecosystem</b> where surplus energy is not just stored but <b>strategically distributed</b>
        to where it’s needed most. By integrating <b>AI-driven forecasting</b>, <b>real-time energy redistribution</b>, and <b>next-generation storage solutions</b>
        such as <b>hydrogen</b> and <b>advanced battery technologies</b>, we are reshaping the energy landscape. <br><br>Our vision is to empower businesses, communities, and individuals to <b>access cleaner, more affordable energy</b>, reducing waste and
        paving the way for a <b>truly sustainable future</b>. <br><br> Through <b>AI-powered energy trading</b>, BetterSave aims to transform every household and business into an active participant
        in the <b>energy revolution</b>—where power is not just consumed, but intelligently optimized, shared, and traded.
    </p>
""", unsafe_allow_html=True)

# Call-to-Action Button with Glitch Effect
st.markdown("""
    <a class='glitch-button' href="https://www.bettersave.com" target="_blank">
        COMING SOON
    </a>
""", unsafe_allow_html=True)

# Footer with Futuristic Design
st.markdown("<div class='futuristic-footer'>© 2025 BetterSave - AI for Energy</div>", unsafe_allow_html=True)
