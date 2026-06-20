import os
from google import genai
from dotenv import load_dotenv

# Load key variables from the local .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")      
client = genai.Client(api_key=API_KEY)  # Initialize the Gemini API client with the API key


# Core model configuration
MODEL_ID = "gemini-2.5-flash"



