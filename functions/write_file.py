import os

def write_file(working_directory, file_path, content):
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
        
    if not file.startswith(absPath):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
   
    try:
        with open(file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Failed to write to file "{file}"'
