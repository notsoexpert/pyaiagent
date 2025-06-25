import subprocess
import os

def run_python_file(working_directory, file_path):
    absPath = ""
    try:
        absPath = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: Could not get absolute path from {working_directory}'
    
    if not os.path.exists(absPath):
        return f'Error: Working directory "{absPath}" does not exist'
    if not os.path.isdir(absPath):
        return f'Error: "{absPath}" is not a directory'
    
    file = ""
    try:
        file = os.path.abspath(os.path.join(absPath, file_path))
    except Exception as e:
        return f'Error: Could not get absolute path from {os.path.join(absPath, file_path)}'
    
    if not os.path.exists(file):
        return f'Error: File "{file_path}" not found'
    if not os.path.isfile(file) or not file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    if not file.startswith(absPath):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    output = ""
    try:
        completed = subprocess.run(['python', file_path], cwd=absPath, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not completed.stdout.decode('utf-8').strip() and not completed.stderr.decode('utf-8').strip():
            output = f'No output produced.'
        else:
            output = f'STDOUT:\n{completed.stdout.decode('utf-8').strip()}\nSTDERR:\n{completed.stderr.decode('utf-8')}'

        if completed.returncode != 0:
            output = f'{output}\nProcess exited with code {completed.returncode}\n'
        return output
    except Exception as e:
        return f'Error: Executing Python file: {e}'