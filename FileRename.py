import re
import os
import logging
from logging import handlers

VERSION = '1.0.0'

def rename_safely(old_file_path: os.path, new_file_path: os.path) -> None:
    # check if target file name already exists
    if not os.path.exists(new_file_path):
        os.rename(src=old_file_path, dst=new_file_path)
        log.info(f"Renaming without conflict; SourcePath; '{old_file_path}'; RenamedPath; '{new_file_path}';")
    else:
        # if target file name exists, append "_2"
        path, ext = os.path.splitext(new_file_path)
        path = path + '_2'
        new_file_path = path + ext
        # try renaming again
        rename_safely(old_file_path, new_file_path)
        log.warn(f"Renaming with conflict; Added '_2' to path; SourcePath; '{old_file_path}'; RenamedPath; '{new_file_path}';")


def rename_file_in_dir(absolute_path: os.path, replace_chars: list) -> None:
    # get regex match
    file_path = os.path.split(absolute_path)[0]
    file_name = os.path.split(absolute_path)[1]
    mat = re.match(pattern=pattern_file, string=file_name)

    # exclude hidden files
    if file_name.startswith('.'):
        log.debug(f"Hidden file ignored; File name; '{file_name}';")
        return

    # if match found
    if mat is not None:
        rename_string = mat.group(1)
        rename_file_ending = mat.group(2)

        for char in replace_chars:
            rename_string = rename_string.replace(char, '_')

        renamed_file = rename_string + '.' + rename_file_ending

        path_old = os.path.join(file_path, file_name)
        path_new = os.path.join(file_path, renamed_file)

        # check if renaming is necessary
        if not path_old == path_new:
            log.info(f"Found file to rename; Old file name; '{file_name}'; New file name; '{renamed_file}';")
            # rename with check of target path
            rename_safely(old_file_path=path_old, new_file_path=path_new)
            return
        
        # if renaming not necessary, log debug
        log.debug(f"Renaming not necessary for file; File name; '{file_name}';")

def rename_folder(absolute_path: os.path) -> None:
    folder_path = os.path.split(absolute_path)[0]
    folder_name = os.path.split(absolute_path)[1]
    renamed_folder_name = folder_name

    # exclude hidden folders
    if folder_name.startswith('.'):
        log.debug(f"Hidden folder ignored; Folder name; '{folder_name}';")
        return
    
    for char in replace_chars:
        renamed_folder_name = renamed_folder_name.replace(char, '_')

    # rename safely
    path_old = os.path.join(folder_path, folder_name)
    path_new = os.path.join(folder_path, renamed_folder_name)

    # check if renaming is necessary
    if not path_old == path_new:
        log.info(f"Found folder to rename; Old folder name; '{folder_name}'; New folder name; '{renamed_folder_name}';")
        rename_safely(old_file_path=path_old, new_file_path=path_new)
        return
    
    # if renaming not necessary, log debug
    log.debug(f"Renaming not necessary for folder; Folder name; '{folder_name}';")

def recurse_directory(path: os.path, replace_chars: list) -> None:
    # list all items in current path
    for item in os.listdir(path):
        # create path for current item
        curr_path = os.path.join(path, item)
        log.debug(f"Analyzing item; Path; '{os.path.realpath(curr_path)}';")

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

pattern_file = '^(.*)\.(.*?)$'
replace_chars = [' ', '.', '-']

# set and create log dir if it does not exist
log_dir = os.path.join(os.curdir, 'FileRenameLog.log')
if not os.path.exists(os.path.split(log_dir)[0]):
    os.makedirs(os.path.split(log_dir)[0])

# logger
log = logging.getLogger('main')
log.setLevel(logging.DEBUG)

# handler
loghandler = handlers.RotatingFileHandler(log_dir, maxBytes=52428800, backupCount=3, encoding='utf-8')
loghandler.setLevel(logging.DEBUG)

# formatter
logformatter = logging.Formatter(fmt='{asctime}; {levelname:8s}; {funcName:20s}; {message}', datefmt='%Y-%m-%d %H:%M:%S', style='{')
loghandler.setFormatter(logformatter)
log.addHandler(loghandler)

log.info(f"****************************************************")
log.info(f"FileRename v{VERSION}")
log.info(f"****************************************************")
log.info(f"Configured symbols to be replaced; {replace_chars};")

# path for renaming
# TODO: remove Test subdir
path = os.path.join(os.curdir, 'Test')
log.info(f"Root path to rename set; Path; '{os.path.realpath(path)}';")

# check if path exists
if not os.path.exists(path):
    os.makedirs(path)
    log.warn(f"Root path did not exist; Path created; '{os.path.realpath(path)}';")

# execute recursively
recurse_directory(path, replace_chars=replace_chars)
log.info(f"Execution finished;")