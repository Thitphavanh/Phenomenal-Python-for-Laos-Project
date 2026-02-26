
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
dotenv_path = '/Users/hery/My-Project/Phenomenal-Python-for-Laos-Project/core/.env'
load_dotenv(dotenv_path)

api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

print("Listing available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

print("\nTrying 'gemini-1.5-flash'...")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Sabaidee'")
    print(f"Response: {response.text}")
    print("SUCCESS with gemini-1.5-flash")
except Exception as e:
    print(f"ERROR with gemini-1.5-flash: {e}")

print("\nTrying 'gemini-pro'...")
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'Sabaidee'")
    print(f"Response: {response.text}")
    print("SUCCESS with gemini-pro")
except Exception as e:
    print(f"ERROR with gemini-pro: {e}")
