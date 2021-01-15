from simplecrypt import encrypt, decrypt
import json
import getpass

username = input('Username: ')
password = getpass.getpass()

#---This builds the dictionary that contains the username and passwords ---#
creds = {
    'username': username,
    'password': password
}

encryptedCredsFile = input('File name for encrypted credentials file (encryptedCreds) ') or 'encryptedCreds'
key = getpass.getpass('Encryption Key: ')

print('\n\n...Encrypting...\n\n')

with open(encryptedCredsFile, 'wb') as encrypt_out:
    encrypt_out.write(encrypt(key, json.dumps(creds)))

with open(encryptedCredsFile, 'rb') as encrypt_in:
    encryptedCreds = json.loads(decrypt(key, encrypt_in.read()))

print(encryptedCredsFile + ' is encrypted with this key')
print(key)
print('and contains these credentials')
print(encryptedCreds)
