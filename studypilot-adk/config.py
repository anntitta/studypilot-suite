import os
from google import genai
from dotenv import load_dotenv

# Load key variables from the local .env file
load_dotenv()

# Automatically initializes using GEMINI_API_KEY from environment memory
client = genai.Client()

# Core model configuration
MODEL_ID = "gemini-2.5-flash"



