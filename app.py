import streamlit as st
import base64

# Set page config
st.set_page_config(page_title="BetterSave", layout="wide")

# ✅ Function to Set Full-Page Background Image with Dark Overlay
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Dark overlay for readability */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.4); /* Semi-transparent black */
            z-index: -1;
        }}

        /* Ensure text is readable */
        .stText, .stMarkdown, h1, h2, h3 {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            text-align: center;
        }}

        /* Center the button at the bottom */
        .explore-btn {{
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 20px;
            font-weight: bold;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# **✅ Apply Background Image**
add_bg_from_local("static/BK1.jpg")  # Path to the background image in static folder

# **Sidebar Navigation**
st.sidebar.title("Navigation")
st.sidebar.page_link("app.py", label="🏡 Home")
st.sidebar.page_link("pages/dashboard.py", label="📊 Dashboard")
st.sidebar.page_link("pages/about.py", label="ℹ️ About")

# ✅ **"EXPLORE MORE" Button at Bottom**
st.markdown(
    """
    <style>
    /* Ensure this style only applies to the button */
    .explore-btn {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 20px;
        font-weight: bold;
        color: white !important; /* Ensuring it's white */
        text-decoration: none;
        padding: 12px 25px;
        border: 2px solid white;
        border-radius: 5px;
        transition: 0.3s ease-in-out;
        animation: pulse 1.5s infinite;
    }

    /* Flashing Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    .explore-btn {
    animation: blinker 1.5s linear infinite;
}

@keyframes blinker {
    50% {
        opacity: 0;
    }
}


    <a href="./pages/dashboard.py" class="explore-btn">EXPLORE MORE</a>
    """,
    unsafe_allow_html=True
)
