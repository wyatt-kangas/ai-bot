import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a `.py` file type, other arguements can be passed through straight to the file after file_path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Python file to run, relative to the working directory",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_path_for_wd = os.path.normpath(os.path.abspath(working_directory))
        target_file = os.path.normpath(os.path.join(abs_path_for_wd, file_path))
        valid_target_file = os.path.commonpath([abs_path_for_wd, target_file]) == abs_path_for_wd

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file,]
        if args:
            command.extend(args)
        
        command_info = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30, check=False)

        return_string = ""

        if command_info.returncode != 0:
            return_string += f"Process exited with code {command_info.returncode}"

        if command_info.stderr == "" and command_info.stdout == "":
            return_string += "\nNo output produced"

        if command_info.stdout:
            return_string += f"\nSTDOUT: {command_info.stdout}"

        if command_info.stderr:
            return_string += f"\nSTDERR: {command_info.stderr}"

        return return_string

    except Exception as e:
        return f"Error: executing Python file: {e}"

