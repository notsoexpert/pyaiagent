import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions import get_files_info

def main():
    verbose = False
    load_dotenv("key.env")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("No prompt provided. Usage: python3 main.py [prompt]")
        exit(1)
    elif len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]
    generatedContent = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    print(generatedContent.text)
    if verbose:
        print("User prompt:", sys.argv[1])
        print("Prompt tokens:", generatedContent.usage_metadata.prompt_token_count)
        print("Response tokens:", generatedContent.usage_metadata.candidates_token_count)

main()