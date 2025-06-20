import os

G_MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    absPath = ""
    try:
        absPath = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: could not get absolute path from {working_directory}'
    
    if not os.path.exists(absPath):
        return f'Error: working directory "{absPath}" does not exist'
    if not os.path.isdir(absPath):
        return f'Error: "{absPath}" is not a directory'
    
    file = ""
    try:
        file = os.path.abspath(os.path.join(absPath, file_path))
    except Exception as e:
        return f'Error: could not get absolute path from {os.path.join(absPath, file_path)}'
    
    if not os.path.exists(file):
        return f'Error: file "{file_path}" does not exist'
    if not os.path.isfile(file):
        return f'Error: "{file_path}" is not a file'
    
    if not file.startswith(absPath):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(file, "r") as f:
            file_content = f.read()
            if len(file_content) > G_MAX_CHARS:
                file_content = file_content[:G_MAX_CHARS] + f'\n[...File "{file_path}" truncated at 10000 characters]'
            return file_content
    except Exception as e:
        return f'Error: Failed to open "{file_path}"'