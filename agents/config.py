import os
from dotenv import load_dotenv

load_dotenv()

# We use litellm formatting for AutoGen to speak with Gemini
llm_config = {
    "config_list": [{
        "model": "gemini-2.5-flash",
        "api_key": os.getenv("GOOGLE_API_KEY"),
        "api_type": "google"
    }],
    "temperature": 0.2
}