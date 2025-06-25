import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from function_schema import get_available_functions
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

working_directory = "./calculator"

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f'Calling function: {function_call_part.name}({function_call_part.args})')
    else:
        print(f' - Calling function: {function_call_part.name}...')

    fnmap = {
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
        "get_files_info": get_files_info,
    }
    
    if function_call_part.name not in fnmap:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f'Unknown function: {function_call_part.name}'}
                )
            ]
        )

    response = fnmap[function_call_part.name](working_directory, **function_call_part.args)
    return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": response}
                )
            ]
        ) 


def main():
    verbose = False
    MAX_LOOPS = 20
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
    for _ in range(0, MAX_LOOPS):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages, 
            config=types.GenerateContentConfig(tools=[get_available_functions()], system_instruction=system_prompt),
        )

        for msg in response.candidates:
            messages.append(msg.content)
        
        fn_calls = response.function_calls
        if fn_calls is None or len(fn_calls) == 0:
            print(response.text)
            break
    
        for function_call_part in fn_calls:
            content = call_function(function_call_part, verbose)
            if content.parts[0].function_response.response is None:
                raise Exception(f'Function {function_call_part.name} returned no response')
            messages.append(content)
            if verbose:
                print(f'-> {content.parts[0].function_response.response}')
                
        if verbose:
            print("User prompt:", sys.argv[1])
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)


main()