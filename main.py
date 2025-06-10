import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


if len(sys.argv) < 2:
    print("Please provide a prompt as an argument.")
    sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("prompt", type=str)
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

user_prompt = args.prompt
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

print(response.text)
if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
