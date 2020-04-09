#!/usr/bin/env python3

try:
	import os
	from cryptography.fernet import Fernet
except ImportError as e:
    print(f"Import error: {e}")

key = Fernet.generate_key() #generate key
fernet = Fernet(key)
keyfile = open('key.key' , 'wb')
keyfile.write(key) #write it to a file to save it
keyfile.close()


def encrypt_a_file():
	with open('test.txt', 'wb') as output_f:
		data = open('test.txt', 'rb').read() # read data from a file
		encrypted = fernet.encrypt(data) #encrypt it
		print(encrypted)
		output_f.write(encrypted) # write encrypted data to the file


def decrypt_a_file():
	with open('test.txt', 'wb') as decrypted_f:
		data = open('test.txt','rb').read() # read data from the file
		print(data)
		#data = encrypted_f.read() # read data from the file
		decrypted = fernet.decrypt(data) #decrypt it
		decrypted_f.write(decrypted) # write decrypted data back to the file
			

def main():
	encrypt_a_file()
	decrypt_a_file()

main()
