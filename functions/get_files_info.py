import os

def get_files_info(working_directory, directory=None):
    absPath = ""
    try:
        absPath = os.path.abspath(working_directory)
    except Exception as e:
        return f'Error: could not get absolute path from {working_directory}'
    
    if not os.path.exists(absPath):
        return f'Error: working directory "{absPath}" does not exist'
    if not os.path.isdir(absPath):
        return f'Error: "{absPath}" is not a directory'
    
    dir = ""
    if directory is None:
        dir = absPath
    else:
        try:
            dir = os.path.abspath(os.path.join(absPath, directory))
        except Exception as e:
            return f'Error: could not get absolute path from {os.path.join(absPath, directory)}'
    
    if not os.path.exists(dir):
        return f'Error: directory "{dir}" does not exist'
    if not os.path.isdir(dir):
        return f'Error: "{dir}" is not a directory'
    
    if not dir.startswith(absPath):
        return f'Error: Cannot list "{dir}" as it is outside the permitted working directory'
    
    contents = ""
    for file in os.listdir(dir):
        fileDir = os.path.join(dir, file)
        contents = contents + f'- {file}: file_size={os.path.getsize(fileDir)} bytes, is_dir={os.path.isdir(fileDir)}\n'
    return contents