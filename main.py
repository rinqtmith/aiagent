import sys
import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from prompts import system_prompt
from call_function import available_functions


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        result = call_function(function_call_part, verbose)
        if not result.parts:
            raise Exception(f"Error calling function {function_call_part.name}")
        if verbose and result.parts:
            print(
                f"-> {result.parts[0].function_response.response if result.parts[0].function_response else ''}"
            )


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    functions = {
        "get_file_content": get_file_content(
            "./calculator", function_call_part.args.get("file_path", "")
        ),
        "get_files_info": get_files_info(
            "./calculator", function_call_part.args.get("directory", "")
        ),
        "run_python_file": run_python_file(
            "./calculator", function_call_part.args.get("file_path", "")
        ),
        "write_file": write_file(
            "./calculator",
            function_call_part.args.get("file_path", ""),
            function_call_part.args.get("content", ""),
        ),
    }

    if function_call_part.name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    result = functions[function_call_part.name]

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )


if __name__ == "__main__":
    main()
