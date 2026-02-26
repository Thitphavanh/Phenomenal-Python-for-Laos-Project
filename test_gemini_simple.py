
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
dotenv_path = '/Users/hery/My-Project/Phenomenal-Python-for-Laos-Project/core/.env'
load_dotenv(dotenv_path)

api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key present: {bool(api_key)}")
if api_key:
    # Print first few chars to verify matching
    print(f"API Key start: {api_key[:5]}...")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content("Say 'Sabaidee' to confirm connection.")
    print(f"Response: {response.text}")
    print("SUCCESS: Gemini API is working.")
except Exception as e:
    print(f"ERROR: {e}")
