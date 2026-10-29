import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Writes text content to a file, returning a confirmation message as a string. "
            "Creates any missing parent directories automatically so intermediate folders don't need to exist beforehand. "
            "Overwrites the file entirely if it already exists — contents are not appended. "
            "Returns a success message in the format `Successfully wrote to \"<path>\" (<N> characters written)` or an `Error:` prefixed message on failure. "
            "Only files inside the tool's permitted root can be written; paths resolving outside it via `..` or absolute paths are rejected. "
            "The `file_path` must not point to an existing directory (use `get_files_info` to list directories instead). "
            "This tool writes raw text only — it does not encode or interpret the content, so include any newlines, formatting, or markup in the `content` string yourself."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path for the file to write, relative to the permitted root. "
                        "Can include intermediate directories (e.g. `src/utils/helpers.py`); they are created automatically if they don't exist. "
                        "Must not point to an existing directory. Paths with `..`, absolute paths, or references outside the permitted root are rejected."
                    ),
                },
                "content": {
                    "type": "string",
                    "description": (
                        "The full text content to write into the file. "
                        "Includes newlines, indentation, and any markup/encoding the file format requires — this tool writes exactly what is given, nothing more."
                    ),
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path_for_wd = os.path.normpath(os.path.abspath(working_directory))
        target_file = os.path.normpath(os.path.join(abs_path_for_wd, file_path))
        valid_target_file = os.path.commonpath([abs_path_for_wd, target_file]) == abs_path_for_wd

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

