# Python Thermal Image Processing Server
Image processing server for ThermalGram(thermalgram.com).
ThermalGram is an Android and web application which uses FLIR One camera to take and share thermal selfies with social media. This sever recognizes thermal temperature of the picture in the request, returns a response with the calculated temperature rating.

## Main dependencies
### Software
- [Python](https://www.python.org/) version 2.7.x or higher
- [Flask](http://flask.pocoo.org/) version 0.10.x or higher
- [Gunicorn](http://gunicorn.org/) 19.3.x or higher
- [Nginx](http://nginx.org/en/) 1.4.6 or higher
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
ssh -i thermal-hack.pem ubuntu@ec2-54-208-206-110.compute-1.amazonaws.com
```

## Setting the basic environment (Ubuntu 14.04)
### Creat and change to a new user
```bash
adduser new-user-name
sudo adduser new-user-name sudo
su - new-user-name
```

### Install packages
```bash
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get upgrade
sudo apt-get install git ufw libreadline6 libreadline6-dev
sudo apt-get install cmake libatlas-dev libatlas3gf-base build-dep
```

### Configure the Firewall
```bash
sudo ufw enable
sudo ufw default deny
sudo ufw allow ssh
sudo ufw allow 123
sudo ufw allow 80/tcp
sudo ufw enable
```

## Setting Python environment

### Set up source folder and enable virtual environment
```bash
sudo mkdir -p /var/www/
sudo chown thermal /var/www/
cd /var/www
mkdir virtual_env & cd virtual_env
sudo apt-get install python-virtualenv
virtualenv . --system-site-packages
```

Run ```source bin/activate``` to enable the virtual environment.

python-setuptools python-pip
### Install python
```bash
sudo apt-get install python-dev
```

### Install OpenCV
In your virtual env:
```bash
sudo ln /dev/null /dev/raw1394
sudo apt-get install python-numpy libatlas-dev libatlas3gf-base
sudo apt-get install python-numpy python-scipy
sudo apt-get build-dep python-matplotlib
sudo apt-get install python-opencv
pip install --user --install-option="--prefix=" -U scikit-learn
```

Test if opencv is installed properly.
```bash
$ python
import cv2
cv2.__version__
```

You should see the proper version.

### Clone git
```bash
cd /var/www
git clone https://github.com/SsureyMoon/ThermalGram-Image-server
mv ThermalGram-Image-server thermal_app
cd thermal_app
mkdir data/model
git update-index --assume-unchanged settings/config.py
```

### Install more dependencies
```bash
pip install -r requirements.txt
```

### Setup your own authorization token
In ```settings/config.py```:
```bash
AUTH_TOKEN = "<replace this>"
```

### Setup front end javascript(Optional)
In ```static/upload.js```:
```bash
var publicDNS = "<repalce this to the public DNS of your server>";
```

## Web server setting
We are going to use [Nginx](http://nginx.org/en/) and [Gunicorn](http://gunicorn.org/) to server our application.

### Run Gunicorn server
Gnuicorn server only serve local requests.
Nginx will work as a proxy server to pass remote request to local gunicorn server.
```bash
gunicorn -b 127.0.0.1:8080 -w 3 app:app --name thermal_app --timeout 20 --log-file logs.log --log-level debug &
```

### Config Nginx
```bash
sudo apt-get install nginx
sudo service nginx start
sudo nano /etc/nginx/sites-available/thermal_app
```

Copy and paste following lines in ```/etc/nginx/sites-available/thermal_app```:
```bash
server {
    listen   80;
    server_name ec2-54-208-206-110.compute-1.amazonaws.com;
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /static {
        alias  /var/www/thermal_app/static/;
    }
}
```

Enable user configuration and disable default configuration:
```bash
sudo unlink /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/thermal_app /etc/nginx/sites-enabled/thermal_app
```

### Run Nginx
```bash
sudo service nginx relaod
sudo service nginx restart
```

## API endpoints
  * GET /:
      * Response (JSON):
        * result: "success"
  * GET /image
      * Response (HTML):
        * form for upload image file.
  * POST /image
      * Form Data:
        * _auth_token: String
        * rate: Int
        * justimage: String
      * Response(JSON):
        * image_file: original image file link, same as 'justimage'
        * rate: user rating (1 to 5)
        * result (Property):
          * how_other_user_say:3
          * images (Property):
              * orig:original image file url in this image server
              * base : Area with temperatures above threshold,
              * point1: Area with middle temperature
              * point2: Area with higher temperature

## Test
Use ```_auth_token```, which you set.
Send post message in CMD to local server.
```bash
curl -X POST --form "_auth_token=<replace this>" --form "rate=4" --form "justimage=@/path/to/the/image/IMG_17.JPEG" http://127.0.0.1:8080/image/
curl -X POST --form "_auth_token=<replace this>" --form "rate=4" --form "justimage=http://thermalgram.com/julia.jpg" http://127.0.0.1:8080/image/
```
or post message in CMD to amazon server.
```bash
curl -X POST --form "_auth_token=<replace this>" --form "rate=4" --form "justimage=@/path/to/the/image/IMG_17.JPEG" http://ec2-54-208-206-110.compute-1.amazonaws.com/image/
curl -X POST --form "_auth_token=<replace this>" --form "rate=4" --form "justimage=http://thermalgram.com/julia.jpg" http://ec2-54-208-206-110.compute-1.amazonaws.com/image/
```
or Visit ```http://ec2-54-208-206-110.compute-1.amazonaws.com/image/```
