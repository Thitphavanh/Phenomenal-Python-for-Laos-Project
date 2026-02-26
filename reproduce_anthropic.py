
import os
import httpx
from anthropic import Anthropic
from dotenv import load_dotenv

# Load .env
load_dotenv('/Users/hery/My-Project/Phenomenal-Python-for-Laos-Project/core/.env')

key = os.getenv('ANTHROPIC_API_KEY')
print(f"Key present: {bool(key)}")

print("Attempt 1: Standard Init")
try:
    client = Anthropic(api_key=key)
    print("Init success. Checking messages attribute...")
    print(client.messages)
except TypeError as e:
    print(f"Init failed with TypeError: {e}")
    print("Attempt 2: Fallback Init")
    client = Anthropic(api_key=key, http_client=httpx.Client())
    print("Fallback Init success. Checking messages attribute...")
    try:
        print(client.messages)
    except AttributeError as e:
        print(f"Hit AttributeError: {e}")
except Exception as e:
    print(f"Other error: {e}")

from openai import OpenAI
print("\n--- OpenAI Check ---")
key_oa = os.getenv('OPENAI_API_KEY')
try:
    client = OpenAI(api_key=key_oa)
    print("OpenAI Init success.")
except TypeError as e:
    print(f"OpenAI Init failed with TypeError: {e}")
