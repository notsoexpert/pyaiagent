import subprocess
import os

def run_python_file(working_directory, file_path):
    absPath = ""
    try:
        absPath = os.path.abspath(working_directory)
    catch Exception as e:
        
