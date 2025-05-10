import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import pdfkit
import tempfile
import shutil

# Load environment variables
load_dotenv()

# Configure API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in environment variables.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Load model safely
try:
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
except Exception as e:
    st.error(f"❌ Failed to load Gemini model: {e}")
    st.stop()


def generate_recommendation(gender, age, height, weight, dietary_preferences, fitness_goals, lifestyle_factors, dietary_restrictions,
                            health_conditions, user_query):
    prompt = f"""
You are a smart fitness and nutrition assistant.

User Profile:
- Gender: {gender}
- Age: {age}
- Height: {height}
- Weight: {weight}
- Dietary Preferences: {dietary_preferences}
- Fitness Goals: {fitness_goals}
- Lifestyle Factors: {lifestyle_factors}
- Dietary Restrictions: {dietary_restrictions}
- Health Conditions: {health_conditions}
- Specific Query: {user_query}

Please return a structured recommendation plan with the following sections:

💡 Diet Recommendations:
- List 5 personalized diet types that match the user's profile.

🏋️ Workout Options:
- List 5 workout suggestions tailored to their fitness goals and lifestyle.


- 5 breakfast ideas.
- 5 dinner options.

🧠 Additional Recommendations:
- List useful tips including snacks, supplements, or hydration tailored to the user.
"""
    try:
        response = model.generate_content(prompt)
        return response.text if response else "⚠️ No response from Gemini."
    except Exception as e:
        return f"❌ Error generating content: {e}"


def parse_recommendation(text):
    sections = {
        "diet_types": [],
        "workouts": [],
        "breakfasts": [],
        "dinners": [],
        "additional_tips": []
    }

    current = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "Diet Recommendations" in line:
            current = "diet_types"
        elif "Workout Options" in line:
            current = "workouts"
        elif "breakfast" in line.lower():
            current = "breakfasts"
        elif "dinner" in line.lower():
            current = "dinners"
        elif "Additional Recommendations" in line:
            current = "additional_tips"
        elif current:
            sections[current].append(line.strip("-• "))
    return sections


def generate_html(plan):
    html = "<h1>Personalized Diet & Workout Plan</h1>"

    html += "<h2>💡 Diet Recommendations</h2><ul>"
    html += "".join(f"<li>{item}</li>" for item in plan["diet_types"])
    html += "</ul>"

    html += "<h2>🏋️ Workout Options</h2><ul>"
    html += "".join(f"<li>{item}</li>" for item in plan["workouts"])
    html += "</ul>"

    html += "<h2>🍳 Breakfast Ideas</h2><ul>"
    html += "".join(f"<li>{item}</li>" for item in plan["breakfasts"])
    html += "</ul><h2>🍽️ Dinner Options</h2><ul>"
    html += "".join(f"<li>{item}</li>" for item in plan["dinners"])
    html += "</ul>"

    html += "<h2>🧠 Additional Tips</h2><ul>"
    html += "".join(f"<li>{item}</li>" for item in plan["additional_tips"])
    html += "</ul>"

    return html


def main():
    st.title("🥗 Personalized Diet & Workout Plan")

    with st.form("user_input_form"):
        gender = st.selectbox("🧑 Gender", ["Male", "Female", "Other"])
        age = st.number_input("🎂 Age", min_value=0, max_value=120, step=1)
        height = st.number_input("📏 Height (cm)", min_value=50, max_value=250, step=1)
        weight = st.number_input("⚖️ Weight (kg)", min_value=10, max_value=300, step=1)
        dietary_preferences = st.text_input("🍴 Dietary Preferences", placeholder="e.g., vegetarian, keto")
        fitness_goals = st.text_input("💪 Fitness Goals", placeholder="e.g., muscle gain, weight loss")
        lifestyle_factors = st.text_input("🏃 Lifestyle Factors", placeholder="e.g., sedentary, active, traveler")
        dietary_restrictions = st.text_input("🚫 Dietary Restrictions", placeholder="e.g., gluten-free, dairy-free")
        health_conditions = st.text_input("🩺 Health Conditions", placeholder="e.g., diabetes, hypertension")
        user_query = st.text_input("🤔 Specific Question (Optional)", placeholder="e.g., meals for evening workouts")

        submitted = st.form_submit_button("Generate Plan")

    if submitted:
        with st.spinner("Generating your personalized plan..."):
            result_text = generate_recommendation(
                gender,
                age,
                height,
                weight,
                dietary_preferences,
                fitness_goals,
                lifestyle_factors,
                dietary_restrictions,
                health_conditions,
                user_query
            )

            if result_text.startswith("❌") or result_text.startswith("⚠️"):
                st.error(result_text)
                return

            plan = parse_recommendation(result_text)

        st.markdown("### 💡 Diet Recommendations")
        for item in plan["diet_types"]:
            st.write(item)

        st.markdown("### 🏋️ Workout Options")
        for item in plan["workouts"]:
            st.write(item)

        st.markdown("### 🍳 Breakfast Ideas")
        for item in plan["breakfasts"]:
            st.write(item)

        st.markdown("### 🍽️ Dinner Options")
        for item in plan["dinners"]:
            st.write(item)

        st.markdown("### 🧠 Additional Tips")
        for item in plan["additional_tips"]:
            st.write(item)


        # PDF download
        html_content = generate_html(plan)
        wkhtmltopdf_path = shutil.which("wkhtmltopdf")

        if wkhtmltopdf_path:
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                try:
                    pdfkit.from_string(html_content, tmp_file.name, configuration=config)
                    with open(tmp_file.name, "rb") as f:
                        st.download_button("📄 Download Plan as PDF", f, file_name="personalized_plan.pdf", mime="application/pdf")
                except Exception as e:
                    st.error(f"❌ Failed to generate PDF: {e}")
        else:
            st.warning("⚠️ wkhtmltopdf not found. Please install it to enable PDF download.")


if __name__ == "__main__":
    main()
