
import os
from google import genai
from dotenv import load_dotenv

load_dotenv('core/.env')
api_key = os.getenv('GOOGLE_API_KEY')

print(f"Testing Gemini Key: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash', # Use a known stable model for testing
        contents="Hello, are you working?"
    )
    print("Success!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Failed: {e}")
