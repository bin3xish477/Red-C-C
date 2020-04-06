#!/usr/bin/env python3

"""
AUTHORS: CHRIS KORTBAOUI, ALEXIS RODRIGUEZ
START DATE: 2020-04-06
END DATE: 2020-04
MODULE NAME: ______
"""

try:
	import socket
	from time import sleep
	from subprocess import run, PIPE
	from os import devnull, _exit
	from sys import argv, exit
except ImportError as err:
	print(f"Error: {err}")
	
"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

# COLORS-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
RESET = "\033[0m"
BOLD = "\033[01m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"

"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

# BOTNET CLASS-=-=-=-=-=-=-=-=-=-=-=-=
class BotnetCmdCtrl:
    def __init__(self):
        self.windows_count = 0
        self.linux_count = 0
        self.windows_connections = {}
        self.linux_connections = {}
        
    def create_server_socket(self):
        pass
    
    def write_reponse_output(self):
        pass
    
    def send_cmd(self):
        pass
    
"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"""

def main():
	pass

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		try:
			exit(1)
		except SystemExit:
			_exit(1)