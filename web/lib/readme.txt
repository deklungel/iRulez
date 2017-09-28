libraries and components to reuse

Install mosquitto for PHP:

this information to install mosquittolib with php in raspberry

wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key
cd /etc/apt/sources.list.d/
sudo wget http://repo.mosquitto.org/debian/mosquitto-jessie.list
sudo apt-get update
apt-get install mosquitto
sudo apt-get install mosquitto-clients
sudo apt-get install php5-dev
sudo apt-get install libmosquitto-dev


sudo pecl install Mosquitto-alpha
and in /etc/php5/mods-available/mosquitto.ini

add this code

extension=mosquitto.so