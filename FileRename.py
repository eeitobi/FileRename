import re
import os

pattern_file = '^(.*)\.(.*?)$'
replace_chars = [' ', '.', '-']

def rename_file_in_dir(absolute_path: os.path, replace_chars: list) -> None:
    # get regex match
    file_path = os.path.split(absolute_path)[0]
    file_name = os.path.split(absolute_path)[1]
    mat = re.match(pattern=pattern_file, string=file_name)

    # if match found
    if mat is not None:
        rename_string = mat.group(1)
        rename_file_ending = mat.group(2)

        for char in replace_chars:
            rename_string = rename_string.replace(char, '_')

        renamed_file = rename_string + '.' + rename_file_ending

        path_old = os.path.join(file_path, file_name)
        path_new = os.path.join(file_path, renamed_file)

        os.rename(src=path_old, dst=path_new)

def rename_folder(absolute_path: os.path) -> None:
    folder_path = os.path.split(absolute_path)[0]
    folder_name = os.path.split(absolute_path)[1]
    renamed_folder_name = folder_name
    for char in replace_chars:
        renamed_folder_name = renamed_folder_name.replace(char, '_')

    path_old = os.path.join(folder_path, folder_name)
    path_new = os.path.join(folder_path, renamed_folder_name)

    os.rename(src=path_old, dst=path_new)

def recurse_directory(path: os.path, replace_chars: list) -> None:
    # list all items in current path
    for item in os.listdir(path):
        # create path for current item
        curr_path = os.path.join(path, item)

        # decide if file or folder
        if os.path.isdir(curr_path):
            # if folder, recursively traverse
            recurse_directory(path=curr_path, replace_chars=replace_chars)
            # then rename
            rename_folder(absolute_path=curr_path)
        elif os.path.isfile(curr_path):
            # if file, rename
            rename_file_in_dir(absolute_path=curr_path, replace_chars=replace_chars)
    return


# path for renaming
path = os.path.join(os.curdir, 'Test')

# check if path exists
if not os.path.exists(path):
    os.makedirs(path)

# execute recursively
recurse_directory(path, replace_chars=replace_chars)
