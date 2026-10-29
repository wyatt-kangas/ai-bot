import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": (
            "Executes a Python (.py) script with the system `python` interpreter and returns its combined console output as a string. "
            "The script must live inside `working_directory`; paths that resolve outside it (e.g. via `..`) are rejected. "
            "Any extra positional arguments are appended verbatim to the command line, so they arrive in the script's sys.argv[1:] exactly as given "
            "(no shell is used, so quoting/globbing/expansion is NOT performed by this tool). "
            "Runs synchronously with a 30 second timeout; if the script exceeds it, or raises an exception, the failure is reported in the returned string rather than raised. "
            "Returns a human-readable result string containing the exit code on non-zero exit, `STDOUT:` / `STDERR:` prefixed sections when there is output, "
            "and `No output produced` when the script succeeds silently. Never use this for files other than `.py`, and do not expect return values from the script - only printed output is captured."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the Python script to execute, relative to `working_directory` (must end in `.py`). "
                        "Must be an existing regular file inside `working_directory`."
                    ),
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Optional list of command-line arguments forwarded to the script in order (each list item becomes one argv entry). "
                        "Omit or leave empty if the script takes no arguments. Pass flags as separate items, e.g. [\"--verbose\", \"--count\", \"3\"] "
                        "not [\"--verbose --count 3\"]. No shell interpretation is applied."
                    ),
                },
            },
            "required": ["working_directory", "file_path"],
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

