# Installation

Red C&C has some dependencies that need to be installed prior to running it. The install.sh bash script located in this folder should help by running it on any Linux machine you're looking to issue commands to and run the client-side program (cc.py). If it utilizes a distribution not contained in the script, you can simply run the appropriate commands for your distribution located within the If/Then statements right in the terminal and it should allow you to obtain everything necessary to run cc.py on the target machine.

**For the best experience in testing, have a couple of virtual machines set up that you can uses as your "clients" or targets and one as your "server" or attacker.**

# Windows Instructions

A powershell or .bat script would only work under very specific conditions so we've listed some instructions on how to install everything so our project will work on a Windows machine as well. 

1. Download the latest version of Python for Windows directly from: https://www.python.org/downloads/. 

2. Install the pip package manager for Python to download additional modules that don't come pre-installed. This is a great guide on doing so for Windows: https://www.liquidweb.com/kb/install-pip-windows/. 

3. Once pip is installed, run the following two commands in the command line to download the additional modules needed to run cc.py:
```python
pip install pynput
pip install cryptography
```

4. Wget cc.py from the following link (https://raw.githubusercontent.com/binexisHATT/Red-C-C/master/scripts/net/cc.py)
