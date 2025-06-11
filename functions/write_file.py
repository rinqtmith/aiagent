import os


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(abs_file_path)
        except Exception as e:
            return f"Error creating file: {e}"

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error writing to file "{file_path}": {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
