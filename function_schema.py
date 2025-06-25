from google import genai
from google.genai import types

def get_available_functions():
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                        type=types.Type.STRING,
                        description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                    ),
                },
            ),
        )
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Retrieves the content of the specified file, constrained to the working directory. Limits the characters returned to 10000.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path to the file, relative to the working directory."
                    ),
                },
            ),
        )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to the specified file, constrained to the working directory. Creates the file if it does not exist and overwrites it if it does.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "content": types.Schema(
                        type=types.Type.STRING,
                        description="The content to write to the file. If the file already exists, it will be overwritten."
                    ),
                "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path to the file, relative to the working directory."
                    ),
                },
            ),
        )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes the specified Python file, constrained to the working directory. Outputs the result of the execution.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path to the Python file, relative to the working directory."
                    ),
                },
            ),
        )
    return types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )