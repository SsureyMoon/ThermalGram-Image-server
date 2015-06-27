# Python Thermal Image Processing Server

## Connect
```bash
chmod 400 thermal-hack.pem
ssh -i thermal-hack.pem ubuntu@ec2-52-5-124-92.compute-1.amazonaws.com
```

## Install python
```bash
sudo apt-get install build-essential
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git python-dev python-setuptools python-pip
```

## Install open-cv
```bash
sudo apt-get install python-opencv
sudo ln /dev/null /dev/raw1394
```

## Open port
```bash
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

## Run server
```bash
gunicorn app:app --timeout 20
```

git update-index --assume-unchanged settings/config.py