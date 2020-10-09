# Find all the files in a given Directory.
# Jacob Strokus
import os

# Function prints all the files in a directory.
def find(location):
    files_in_dir = []

    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(location):
       for item in f:
            files_in_dir.append(os.path.join(r, item))

    for item in files_in_dir:
       print("file in dir: ", item)
    

# Controls the program. 
def main():

    location = input('Enter the directory for which you want to find all files: ')
    find(location)

#Function call to main().
main()
