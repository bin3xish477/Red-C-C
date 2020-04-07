# Botnet-Command-Control
Send commands to all your bots.

### Install Docker and all the dependencies for this program.
```bash
git clone https://github.com/binexisHATT/Botnet-Command-Control.git

cd /Botnet-Command-Control/scripts/docker

chmod +x install.sh

./install.sh
```
### Downloading botnet scripts in Docker containers.
##### Repeat this step for all the containers you wish to control.
```bash
# Get interactive shell for container.
docker container run -it [Linux image]

apt install wget

wget https://raw.githubusercontent.com/binexisHATT/Botnet-Command-Control/master/scripts/cc.py

wget https://raw.githubusercontent.com/binexisHATT/Botnet-Command-Control/master/scripts/install/install.sh
```

### Download modules in Windows VM
```powershell
Use powershell for this!!
```
