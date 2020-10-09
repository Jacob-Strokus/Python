# Encrypt computer files.
# Jacob Strokus

# Import statements
import shutil, os, errno, time, pyfiglet


# banner
ascii_banner = pyfiglet.figlet_format("Pixxlated")
print(ascii_banner)

# encrypt the files.
def encrypt(item):
    #replace print statement with encryption of your choice. I reccommend AEs 256 :)
    print('')

# Launch the Script.
def main():

    files_in_dir = []
    dirs = []
    source = input(r'Where should I start: ')
    
    # r=>root, d=>directories, f=>files
    for r, d, f in os.walk(source):

        for item in d:
            dirs.append(os.path.join(r, item))
        for item in f:
            files_in_dir.append(os.path.join(r, item))
            

    #   THIS BLOCK OF CODE IS FOR VISUAL PURPOSES ONLY
    print('Encrypting:\n')
    for d in dirs:
        time.sleep(2)
        print(d + '\n')
            
    # actual encryption
    for item in files_in_dir:
            encrypt(item);
        

# Function call to main().
main()
