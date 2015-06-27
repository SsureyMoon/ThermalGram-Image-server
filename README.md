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
sudo apt-get install libreadline6 libreadline6-dev
```

## Install open-cv
```bash
sudo apt-get install python-opencv
sudo ln /dev/null /dev/raw1394
sudo apt-get install python-numpy libatlas-dev libatlas3gf-base
sudo apt-get build-dep python-matplotlib
sudo apt-get install python-scipy
sudo apt-get install nginx
pip install --user --install-option="--prefix=" -U scikit-learn
```

## Open port
```bash
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

# Clone git
```bash
git clone https://github.com/SsureyMoon/ThermalGram-Image-server
cd ThermalGram-Image-server
git update-index --assume-unchanged settings/config.py
pip install -r requirements.txt
```

## Run server
```bash
gunicorn -b 0.0.0.0:8000 -w 5 app:app --timeout 20
```

## Test
Send post message in CMD
or Visit ```http://ec2-52-5-124-92.compute-1.amazonaws.com:8000/image/```
```bash
curl -X POST --form "_auth_token=ASDFQWER1234" --form "rate=4" --form "justimage=@/path/to/the/image/IMG_17.JPEG" http://127.0.0.1:8000/image/
```
or

```bash
curl -X POST --form "_auth_token=ASDFQWER1234" --form "rate=4" --form "justimage=@/path/to/the/image/IMG_17.JPEG" http://ec2-52-5-124-92.compute-1.amazonaws.com:8000/image/
```
