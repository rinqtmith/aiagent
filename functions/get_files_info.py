import os


def get_files_info(working_directory, directory=None):
    if directory is None or not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    if os.path.abspath(directory) in os.path.abspath(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    files_info = []
    for item in os.listdir(directory):
        files_info.append(
            f"- {item}: file_size={os.path.getsize(item)} bytes, is_dir={os.path.isdir(item)}"
        )

    return "\n".join(files_info) if files_info else "No files found in the directory"
