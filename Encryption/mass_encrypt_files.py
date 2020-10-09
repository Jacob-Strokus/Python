# Encrypt computer files.
# Jacob Strokus

# Import statements
import shutil, os, errno

# encrypt the files.
def encrypt(item):
    #replace print statement with encryption of your choice. I reccommend AES 256 :) will need to import necessary dependencies.
    print('')

# Launch the Script.
def main():

    files_in_dir = []
    source = input(r'Where should I start: ')
    
    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(source):
        for item in f:
            files_in_dir.append(os.path.join(r, item))

        print('Encrypting: \n ')
        for dirs in d:
            print('\' + dirs + '\n')
            

    for item in files_in_dir:
            encrypt(item);
        

# Function call to main().
main()
