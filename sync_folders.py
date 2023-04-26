import os
import hashlib
import inspect
import logging
import argparse
import shutil
import schedule
import time


# Parser to obtain the arguments from command line
parser = argparse.ArgumentParser(description='Configuration arguments for folder synchronization processor')
# Arguments with the path to source folder
parser.add_argument('-s', '--source', required=True, type=str, help="Path to the source folder")
# Arguments with the path to copy folder
parser.add_argument('-c', '--copy', required=True, type=str, help="Path to the copy folder")
# Arguments with the time for iteration
parser.add_argument('-t', '--time', help='time for iteration in seconds', type=int)


# Get the arguments from the parser for the paths and time period
arguments = parser.parse_args()
source_path = arguments.source
copy_path = arguments.copy
time_period = arguments.time


# Function to create the logger for log file and console
def get_logger():
    # Refers to function name
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)
    fileHandler = logging.FileHandler('logfile.log')
    formatter = logging.Formatter('%(asctime)s :%(levelname)s :%(message)s')
    fileHandler.setFormatter(formatter)
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    logger.addHandler(fileHandler)
    logger.setLevel(logging.INFO)
    return logger


# Function that return the sha256 hash digest of a file parameter
def generate_hash(file):
    with open(file, 'rb') as f:
        content = f.read()
    sha256 = hashlib.sha256()
    sha256.update(content)
    return sha256.hexdigest()


# Function to get the hashes of contents from a folder on a dictionary
def folder_hasher(folder_path):
    # Dictionary for path,hash
    folder_hash = {}

    # Start going over the source folder having path, subdir and files
    for path, subdir, files in os.walk(folder_path):

        # Subdirectories inside the folder
        for s in subdir:
            # For folders inside the folder they will be inside the dictionary with key relative path and value "folder"
            relative_dir = os.path.relpath(path, folder_path)
            relative_folder = os.path.join(relative_dir, s)
            if ".\\" in relative_folder:
                relative_folder = relative_folder.replace('.\\', '')
            folder_hash[relative_folder] = "folder"

        # Files inside every folder
        for f in files:
            # The files will be represented with key=relative_path and value=hash
            rel_dir = os.path.relpath(path, folder_path)
            rel_file = os.path.join(rel_dir, f)
            if ".\\" in rel_file:
                rel_file = rel_file.replace('.\\', '\\')
            if '\\\\' in rel_file:
                rel_file = rel_file.replace('\\\\', '\\')
            folder_hash[rel_file] = generate_hash(os.path.join(path, f))

    return folder_hash


# Declare the logger outside the function so the logs are not repeting on logfile
logger = get_logger()


# Function to compare two folders content according to their hash digest
def folder_updater():
    # Obtain the hashes of both folders
    source_files = folder_hasher(source_path)
    copy_files = folder_hasher(copy_path)

    # Loop through the files (paths) on the source folder
    for f in source_files.items():

        # If it is a folder
        if f[1] == "folder":
            # Check if the folder is contained in the copy folder add it to it
            if f[0] not in copy_files:
                os.makedirs(copy_path + '\\' + f[0])
                logger.info(' Added folder: ' + f[0])

        # File not in copy according to name, the file is not in copy, or it was renamed
        if f[0] not in copy_files and f[1] != 'folder':
            shutil.copy(source_path+'\\'+f[0], copy_path+'\\'+f[0])
            logger.info(' Added file: ' + f[0])

        # Same name but different hash, not updated
        elif f[0] in copy_files and f[1] != copy_files.get(f[0]) and f[1] != 'folder':
            shutil.copy(source_path+'\\'+f[0], copy_path+'\\'+f[0])
            logger.info(' Updated file: ' + f[0])

    # Put into the deleted set the files that are only on copy folder
    copy_files_updated = folder_hasher(copy_path)
    deleted_files = find_deleted_items(source_files, copy_files_updated)

    # For the hash of the files that are only on copy delete them
    for d in copy_files_updated.items():
        if d in deleted_files and d[1] != 'folder':
            os.remove(copy_path+'\\'+d[0])
            logger.info(' Deleted file: ' + d[0])
    # Perform the same for deleting folders in reversed order
    for d in reversed(copy_files_updated.items()):
        if d in deleted_files and d[1] == 'folder':
            os.rmdir(copy_path+'\\'+d[0])
            logger.info(' Deleted folder: ' + d[0])


# Function to find the files that were deleted from source
def find_deleted_items(source, copy):

    deleted_set = set()
    source_set = set(source.items())
    copy_set = set(copy.items())
    deleted_items = copy_set - source_set
    for d in deleted_items:
        deleted_set.add(d)

    return deleted_set


# Schedule for the function folder_updater() to run periodically based on time_period
schedule.every(time_period).seconds.do(folder_updater)

# Time between executions
while True:
    schedule.run_pending()
    time.sleep(5)

