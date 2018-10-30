#!/bin/bash
set -e
set -x

echo "This is travis-build.bash..."

# remove faulty mongodb repo, we don't use it anyway
sudo rm -f /etc/apt/sources.list.d/mongodb-3.2.list
sudo add-apt-repository --remove 'http://us-central1.gce.archive.ubuntu.com/ubuntu/ main restricted'
sudo add-apt-repository --remove 'http://us-central1.gce.archive.ubuntu.com/ubuntu/ universe'
sudo add-apt-repository --remove 'http://us-central1.gce.archive.ubuntu.com/ubuntu/ multiverse'
sudo add-apt-repository -y ppa:ubuntugis/ubuntugis-testing
sudo add-apt-repository 'http://archive.ubuntu.com/ubuntu/'
sudo add-apt-repository 'http://archive.ubuntu.com/ubuntu/ universe'
sudo add-apt-repository 'http://archive.ubuntu.com/ubuntu/ multiverse'
sudo apt-get -qq --fix-missing update
sudo aptitude remove -y postgresql-9.5-postgis-2.3
sudo aptitude install -y libgdal20 python3-dev python3-pip python3-wheel
sudo apt-get install libgdal-dev


sudo apt-get install postgresql-9.5-postgis-2.3=2.3.2+dfsg-1~xenial0


# PostGIS 2.1 already installed on Travis
cd lib

pip install --upgrade pip
pip install pygdal==2.1.0 # $(gdal-config --version)
pip install -r requirements.txt
pip install -e .

# sudo aptitude install postgis
# postgresql-9.6-postgis-2.3
sudo service postgresql start

#sudo -u postgres psql -c "create role pyfulcrum superuser login password 'pyfulcrum';"
#sudo -u postgres psql -c "create database pyfulcrum_test owner pyfulcrum;"
#sudo -u postgres psql -d pyfulcrum_test -c 'create extension postgis;'

echo "travis-build.bash is done."
