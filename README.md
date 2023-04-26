Folder Synchronizer

This project is a Python script that synchronizes two folders from source to copy only, keeping them identical.

Requirements:

+ Python 3.x
+ For the used modules only schedule had to be pip installed

Usage:

- Clone repository into your local machine with the command git clone
- Open the root folder on console
- The command to execute the file "sync_folders.py" is at follows:
- python .\sync_folders.py -s source -c copy -t time
- Where the flags represent:
  - -s absolute path of the source folder to be synchronized, must be given
  - -c absolute path of the copy folder to be synchronized, must be given
  - -t time in seconds for the period of iteration, must be given
- An example of arguments could be:
  - python .\sync_folders.py -s 'C:\Users\Public' -c 'C:\Users\Public2' -t 30
- For more help use the command: python .\sync_folders.py --help