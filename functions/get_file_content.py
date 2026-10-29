import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": (
            "Reads a text file and returns its contents as a string. "
            "The file must be an existing regular file within the tool's permitted directory "
            "(paths resolving outside it via `..` or absolute paths are rejected). "
            "The file is read as UTF-8 text up to a maximum of `{MAX_CHARS}` characters; "
            "if the file exceeds this limit, it is truncated and a `[... File truncated ...]` notice is appended. "
            "Returns the raw file contents on success, or an `Error:` prefixed message on failure. "
            "Do not use this for binary files (images, PDFs, etc.) — it returns garbled text."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": (
                        "Path to the file to read, relative to the permitted directory. "
                        "Must be an existing regular file. Paths with `..`, absolute paths, or "
                        "references outside the permitted directory are rejected."
                    ),
                },
            },
            "required": ["file_path"],
        },
    },
}

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path_for_wd = os.path.normpath(os.path.abspath(working_directory))
        target_file = os.path.normpath(os.path.join(abs_path_for_wd, file_path))
        valid_target_file = os.path.commonpath([abs_path_for_wd, target_file]) == abs_path_for_wd

        if not valid_target_file:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[... File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string

    except Exception as e:
        return f"Error: {e}"

