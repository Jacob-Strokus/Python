# Generate AES256 encryption key from password.
# Jacob Strokus

# imports
import pyaes, pbkdf2, binascii, os, secrets

def main():
   generate_key()

def generate_key():
     
    password = input(r'Enter a Password: ')
    passwordSalt = os.urandom(16)
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    AES_key =  binascii.hexlify(key)
    out_file = r'YOUR_OUTFILE'

    with open(out_file, 'wb') as outfile:
        outfile.write(AES_key)
    print('AES encryption key:',AES_key) # sanity check

    
# Function call to main().
main()
