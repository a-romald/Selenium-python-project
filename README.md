Selenium python project.

Selenium python project consists of two parts. The first script avito.py creates database, parses data from the site avito.ru with webdriver and Selenium-python, parses images of phones and makes their optical recognition with Tesseract-OCR. The retrived images stored in `phones` directory for further ocr-processing. The second script tripadvisorTest.py makes selenium test of pagination of the site tripadvisor.ru and parses data of hotels from each page of the selected city.

Features

    Selenium parsing and testing project that stores data in mysql database. 
    Requires Python 2.7

Init project and install necessary software in Ubuntu 16. 

Install selenium:

	sudo pip install selenium


Install webdrivers Geckodriver:

	wget https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-linux64.tar.gz
	sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.20.0-linux64.tar.gz -O > /usr/bin/geckodriver'
	sudo chmod +x /usr/bin/geckodriver
	rm geckodriver-v0.20.0-linux64.tar.gz


Install webdriver Chromedriver:

	wget https://chromedriver.storage.googleapis.com/2.36/chromedriver_linux64.zip
	unzip chromedriver_linux64.zip
	sudo chmod +x chromedriver
	sudo mv chromedriver /usr/bin/
	rm chromedriver_linux64.zip


Since we don’t have a screen to run Firefox and Chrome we are going to be using Xvfb to simulate a display and run everything in memory:

	sudo apt-get install xvfb


Install Firefox:

	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get install firefox

Test Firefox version:

	firefox -v


Install Google Chrome:

	sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
	sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb
	sudo apt-get update
	sudo apt-get install google-chrome-stable



Now we need PyVirtualDisplay which is a python wrapper for Xvfb used for easy working with virtual displays in python:

	sudo pip install pyvirtualdisplay



Install Beautiful Soap:

	sudo pip install beautifulsoup4



Install mysqlclient:

	sudo apt-get install libmysqlclient-dev
	sudo pip install mysqlclient



Install Pillow and necessary packages:

	sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
	sudo pip install pillow



Install Tesseract:

	sudo apt-get install tesseract-ocr
	sudo pip install pytesseract



Run script avito.py or Create database in Mysql:

    CREATE DATABASE selenium;



Then run script tripadvisorTest.py that takes names of manufacturers from phones.csv file.

All necessary tables given in db.sql.
