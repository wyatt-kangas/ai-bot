import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": (
            "Lists the immediate contents of a directory and returns a plain-text listing as a string. "
            "For each entry it reports the name, its size in bytes, and whether it is a directory, one per line, e.g. `- notes.md: file_size=1024, is_dir=False`. "
            "The first line is a status line (`Success! <dir> is a valid directory`) or an `Error:` prefixed message on failure. "
            "The listing is NOT recursive — subdirectory contents are not expanded; call again with that path to descend. "
            "Hidden files (dotfiles) are included. Entries are returned in arbitrary OS order, not sorted. "
            "Only directories inside the tool's permitted root can be listed; paths resolving outside it via `..` or absolute paths are rejected."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": (
                        "Path to the directory to list, relative to the permitted root. Defaults to `.` (the root itself) when omitted. "
                        "Must be an existing directory. Paths with `..`, absolute paths, or references outside the permitted root are rejected. "
                        "Passing a file path here returns an error — use the file-reading tool instead."
                    ),
                },
            },
            "required": [],
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path_for_wd = os.path.normpath(os.path.abspath(working_directory))
        target_dir = os.path.normpath(os.path.join(abs_path_for_wd, directory))
        valid_target_dir = os.path.commonpath([abs_path_for_wd, target_dir]) == abs_path_for_wd

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        output = [f"Success! {directory} is a valid directory"]
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            output.append(f"- {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: {e}"

