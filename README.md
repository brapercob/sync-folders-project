TODO:
1. Obtain command line arguments for:
   - Source folder path
   - Copy folder path
   - Time for interval of synchronization

2. Begging with iteration on the source folder:
   - Copy the folders that does not exist on copy folder
   - Copy the files that does not exist (Equal hash to another file)
     + Function to compare the hash of two files (md5)
   - Cases for comparing files:
     1. New, file on source but not on copy -> copy file to copy folder
     2. Deleted, file on copy but not on source -> delete from copy folder
     3. Modified, file exists on both but hash is different -> replace on folder copy
     4. Unchanged, file exists and same hash -> no action

3. Log for every action taken on the folders after they are performed on a logfile and on console

4. Establish the time interval for iteration on the folder with a schedule.
    