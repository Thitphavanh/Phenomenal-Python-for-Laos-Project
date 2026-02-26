
import os

from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
dotenv_path = '/Users/hery/My-Project/Phenomenal-Python-for-Laos-Project/core/.env'
load_dotenv(dotenv_path)

def test_openai():
    print("\n--- Testing OpenAI ---")
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        print("No OpenAI Key found.")
        return
    
    try:
        client = OpenAI(api_key=key)
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print("✅ OpenAI: Valid")
    except Exception as e:
        print(f"❌ OpenAI: Invalid/Error ({e})")

def test_anthropic():
    print("\n--- Testing Anthropic ---")
    key = os.getenv('ANTHROPIC_API_KEY')
    if not key:
        print("No Anthropic Key found.")
        return
    
    try:
        client = Anthropic(api_key=key)
        client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print("✅ Anthropic: Valid")
    except Exception as e:
        print(f"❌ Anthropic: Invalid/Error ({e})")

def test_gemini():
    print("\n--- Testing Gemini ---")
    key = os.getenv('GOOGLE_API_KEY')
    if not key:
        print("No Gemini Key found.")
        return
    
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        model.generate_content("Hi")
        print("✅ Gemini: Valid")
    except Exception as e:
        print(f"❌ Gemini: Invalid/Error ({e})")

if __name__ == "__main__":
    print("Starting diagnostics...")
    try:
        test_openai()
    except Exception as e:
        print(f"OpenAI test crashed: {e}")
        
    try:
        test_anthropic()
    except Exception as e:
        print(f"Anthropic test crashed: {e}")
        
    try:
        test_gemini()
    except Exception as e:
        print(f"Gemini test crashed: {e}")
        
    print("Diagnostics complete.")
