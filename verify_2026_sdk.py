
import os
import sys

print("Checking Google Genai...")
try:
    from google import genai
    print(f"Google Genai Import Success. Client available? {hasattr(genai, 'Client')}")
except Exception as e:
    print(f"Google Genai Failed: {e}")

print("\nChecking OpenAI...")
try:
    from openai import OpenAI
    import httpx
    client = OpenAI(api_key="test", http_client=httpx.Client())
    print("OpenAI Init Success")
except Exception as e:
    print(f"OpenAI Failed: {e}")

print("\nChecking Anthropic...")
try:
    from anthropic import Anthropic
    import httpx
    client = Anthropic(api_key="test", http_client=httpx.Client())
    print("Anthropic Init Success")
except Exception as e:
    print(f"Anthropic Failed: {e}")
