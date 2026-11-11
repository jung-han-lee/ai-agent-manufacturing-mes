
import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Read the API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Send a question to the model
response = client.responses.create(
    model="gpt-4.1-mini",
    instructions="You are a manufacturing systems assistant.",
    input="Explain what MES means in manufacturing in two sentences."
)

# Print the response
print(response.output_text)
