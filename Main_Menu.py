import streamlit as st

st.set_page_config(page_title="NovaHealth", layout="wide")

st.markdown("""
    <style>
        /* Global Styles */
        html, body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f5f9f8;
            color: #2c3e50;
        }

        /* Title Styling */
        .title {
            font-size: 60px;
            font-weight: 700;
            color: #1abc9c;
            text-align: center;
            margin-top: 0;
            margin-bottom: 10px;
        }

        /* Subtitle Styling */
        .subtitle {
            font-size: 24px;
            font-weight: 500;
            color: #34495e;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Description Styling */
        .description {
            font-size: 20px;
            text-align: center;
            color: #555;
            margin: 0 auto;
            max-width: 800px;
            margin-bottom: 40px;
        }

        /* Section Headings */
        .section-header {
            font-size: 28px;
            font-weight: 600;
            text-align: center;
            color: #2c3e50;
            margin-bottom: 20px;
            margin-top: 40px;
        }

        /* Service List Styling */
        .service-list {
            font-size: 18px;
            color: #2c3e50;
            margin: 0 auto;
            max-width: 800px;
            padding-left: 0;
            list-style-type: none;
        }

        .service-list li {
            background-color: #eafaf1;
            border: 1px solid #d1f0dd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        /* Sidebar Styling */
        .sidebar-title {
            font-size: 20px;
            font-weight: 600;
            color: #1abc9c;
            margin-top: 20px;
        }

        /* Disclaimer Styling */
        .disclaimer {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
            border-radius: 8px;
            padding: 20px;
            font-size: 16px;
            font-weight: 500;
            text-align: center;
            margin-top: 40px;
        }

        .disclaimer h4 {
            font-size: 20px;
            margin-bottom: 10px;
        }
        
        /*efforts*/
        .efforts{
            background-color: #fff3cd;
            color: lightgreen;
            border: 1px solid #ffeeba;
            border-radius: 8px;
            padding: 20px;
            font-size: 16px;
            font-weight: 500;
            text-align: center;
            margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown('<div class="title">NovaHealth 🧘‍♀️🌱🔆</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A Smart Health Diagnosis and Lifestyle System</div>', unsafe_allow_html=True)

# Description
st.markdown('<div class="description">Welcome to your one-stop platform for health and wellness. We provide smart tools to help you stay informed, eat better, and make healthier lifestyle choices.</div>', unsafe_allow_html=True)

# Our Services
st.markdown('<div class="section-header">Our Services</div>', unsafe_allow_html=True)
st.markdown("""
    <ul class="service-list">
        <li><strong>🏥 Disease Detection & Assistance</strong><br>Use ML models to get insights into possible health conditions and guidance on next steps.</li>
        <li><strong>🥗 Personalized Diet & Workout Plan</strong><br>Receive customized health plans tailored to your goals, body type, and lifestyle.</li>
        <li><strong>🤖 MediBot – Your Wellness Chatbot</strong><br>A friendly assistant that answers your health-related questions using smart, encylopedia-sourced information.</li>
    </ul>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
st.sidebar.info("Use this sidebar to explore all NovaHealth services.")

# Call to action
st.markdown("---")
st.info("👉 Ready to begin? Use the sidebar to access each feature.")

# Disclaimer
st.markdown("""
    <div class="disclaimer">
        <h4>⚠️ Disclaimer</h4>
        This platform is currently in the <strong>prototyping phase</strong> and is intended for informational use only. 
        The content and recommendations are sourced from online data and may not be fully accurate. 
        <br><br><strong>Always consult a qualified healthcare provider</strong> before making any medical decisions.
        <br><br><h6 style= "color:black">Efforts by: Maitreyee Purohit (21130252) and Shubhangam Tripathi (21103099)</h6>
        
    </div>
""", unsafe_allow_html=True)

