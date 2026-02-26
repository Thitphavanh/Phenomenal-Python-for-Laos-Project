
from google import genai

# Use the key provided by the user in step 188 directly
api_key = "AIzaSyAIAjHC8zeunRbIwfV0bNRR8PG_pHkiBJ0"

print(f"Directly Testing Key: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents="Hello"
    )
    print("Success!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Failed: {e}")
