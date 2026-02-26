
from django.core.management.base import BaseCommand
from openai import OpenAI
from anthropic import Anthropic
import os
import httpx

class Command(BaseCommand):
    help = 'Diagnose AI init in Django'

    def handle(self, *args, **options):
        self.stdout.write("Checking Environment for PROXY...")
        for key in os.environ:
            if 'PROXY' in key.upper():
                self.stdout.write(f"{key}: {os.environ[key]}")

        self.stdout.write("\nChecking httpx version...")
        self.stdout.write(httpx.__version__)

        self.stdout.write("\nAttempting OpenAI Init...")
        try:
            client = OpenAI(api_key="test")
            self.stdout.write(self.style.SUCCESS("OpenAI Init Success"))
        except TypeError as e:
            self.stdout.write(self.style.ERROR(f"OpenAI Init TypeError: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"OpenAI Init Error: {e}"))

        self.stdout.write("\nAttempting Anthropic Init...")
        try:
            client = Anthropic(api_key="test")
            self.stdout.write(self.style.SUCCESS("Anthropic Init Success"))
        except TypeError as e:
            self.stdout.write(self.style.ERROR(f"Anthropic Init TypeError: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Anthropic Init Error: {e}"))
        
        self.stdout.write("\nAttempting Direct httpx Client Init...")
        try:
            client = httpx.Client(proxies={"http://": "http://10.10.1.10:3128"})
            self.stdout.write("httpx.Client(proxies=...) Success")
        except TypeError as e:
             self.stdout.write(self.style.ERROR(f"httpx.Client(proxies=...) Failed: {e}"))
