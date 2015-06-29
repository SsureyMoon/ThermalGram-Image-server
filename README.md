# Python Thermal Image Processing Server
Image processing server for ThermalGram(thermalgram.com).
ThermalGram is an Android and web application which uses FLIR One camera to take and share thermal selfies with social media. This sever recognizes thermal temperature of the picture in the request, returns a response with the calculated temperature rating.

## Main dependencies
### Software
- [Python](https://www.python.org/) version 2.7.x or higher
- [Flask](http://flask.pocoo.org/) version 0.10.x or higher
- [Gunicorn](http://gunicorn.org/) 19.3.x or higher
- [httplib2](https://pypi.python.org/pypi/httplib2) 0.8 or higher
- [numpy](http://www.numpy.org/) 1.8.x or higher
- [scipy](http://www.scipy.org/) 0.13.x or higher
- [scikit-learn](http://scikit-learn.org/) 4.x or higher
- [OpenCV](http://opencv.org/) 2.4.8 or higher

### Hardware
- [FLIRONE](http://flir.com/flirone/) Thermal accessory for Android Smartphone

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
gunicorn -b 0.0.0.0:8000 -w 3 app:app --timeout 20 --log-file logs.log --log-level debug &
```

## Test

Use ```_auth_token```, which you set.
Send post message in CMD to local server.
```bash
curl -X POST --form "_auth_token=<replace this>" --form "rate=4" --form "justimage=@/path/to/the/image/IMG_17.JPEG" http://127.0.0.1:8000/image/
curl -X POST --form "_auth_token=<replace this>" --form "rate=4" --form "justimage=http://thermalgram.com/julia.jpg" http://127.0.0.1:8000/image/
```
or post message in CMD to amazon server.
```bash
curl -X POST --form "_auth_token=<replace this>" --form "rate=4" --form "justimage=@/path/to/the/image/IMG_17.JPEG" http://ec2-52-5-124-92.compute-1.amazonaws.com:8000/image/
curl -X POST --form "_auth_token=<replace this>" --form "rate=4" --form "justimage=http://thermalgram.com/julia.jpg" http://ec2-52-5-124-92.compute-1.amazonaws.com:8000/image/
```
or Visit ```http://ec2-52-5-124-92.compute-1.amazonaws.com:8000/image/```
