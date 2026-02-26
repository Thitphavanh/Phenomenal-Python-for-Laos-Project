
import os
import sys
from openai import OpenAI
from anthropic import Anthropic

# Print env vars related to proxies
print("Environment Variables:")
for key in os.environ:
    if 'PROXY' in key.upper():
        print(f"{key}: {os.environ[key]}")

print("\n--- Testing OpenAI Init ---")
try:
    client = OpenAI(api_key="sk-test-dummy")
    print("OpenAI Init Success")
except TypeError as e:
    print(f"OpenAI Init Failed: {e}")
except Exception as e:
    print(f"OpenAI Init Error: {e}")

print("\n--- Testing Anthropic Init ---")
try:
    client = Anthropic(api_key="sk-ant-test-dummy")
    print("Anthropic Init Success")
except TypeError as e:
    print(f"Anthropic Init Failed: {e}")
except Exception as e:
    print(f"Anthropic Init Error: {e}")
