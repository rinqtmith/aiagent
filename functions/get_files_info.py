import os


def get_files_info(working_directory, directory=None):
    if directory == ".":
        directory = ""
    directory = (
        os.path.join(working_directory, directory or "")
        if directory != "../"
        else directory
    )
    if directory is None or not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    if working_directory not in directory or directory == "..":
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    files_info = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        files_info.append(
            f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
        )

    return "\n".join(files_info) if files_info else "No files found in the directory"
