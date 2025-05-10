import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# List all available models
models = genai.list_models()
for model in models:
    print(f"🔹 {model.name} | Supported Methods: {model.supported_generation_methods}")