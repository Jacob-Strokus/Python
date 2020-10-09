# Copy computer files.
# Jacob Strokus

# Import statements
import shutil, os, errno



# copy the files.
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else: raise

# Launch the Script.
def main():

    files_in_dir = []
    source = input(r'Where should I start: ')
    destination = os.mkdir(r'E:\System_Copy') # Makes new folder where everything will be copied -- this can be anything
    target = r'E:\System_Copy' # target should be the same String of destination
    
    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(source):
       for item in f:
            files_in_dir.append(os.path.join(r, item)) # collect all files

    for item in files_in_dir:
        print('copying: '+ item)
        copy(item, target) # copy

# Function call to main().
main()
