#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyvirtualdisplay import Display
from selenium import webdriver
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytesseract import image_to_string
from PIL import Image
from base64 import decodestring
import MySQLdb
 

      
display = Display(visible=0, size=(1366, 768))
display.start()
driver = webdriver.Firefox()
driver.get('https://www.avito.ru/sankt-peterburg')
driver.maximize_window()

#conn = MySQLdb.connect('localhost', 'root', '', 'selenium', charset="utf8", use_unicode=True)
conn = MySQLdb.connect(host="localhost", user="root", passwd="", charset="utf8", use_unicode=True)
cursor = conn.cursor()

cursor.execute("SET sql_notes = 0; ")
sql = "CREATE DATABASE IF NOT EXISTS selenium"
cursor.execute(sql)
# use selenium
sql = "USE selenium"
cursor.execute(sql)
# create table
cursor.execute("SET sql_notes = 0; ")
sql = """
  CREATE TABLE IF NOT EXISTS phones (
  id int(11) NOT NULL AUTO_INCREMENT,
  title varchar(255) DEFAULT NULL,
  price varchar(100) DEFAULT NULL,
  image varchar(255) DEFAULT NULL,
  phone varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
cursor.execute(sql)
cursor.execute("SET sql_notes = 1; ")

with open('phones.csv', "r") as f_obj:
    reader = csv.reader(f_obj)
    for row in reader:
        search = row[0]
        element = driver.find_element_by_id("search")
        driver.find_element_by_id("search").send_keys(search)
        element.submit()
        wait = WebDriverWait(driver, 3)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.catalog-list')))
        print "The keyword [" + search + "] is searched"
        # GET PAGE WITH RESULTS OF SEARCH FORM
        driver.switch_to.window(driver.window_handles[-1])
        print driver.title
        items = driver.find_elements_by_css_selector('div.js-catalog_before-ads div.item_table')
        i = 0
        for item in items :
            i = i + 1
            print i
            # Title
            title = item.find_element_by_css_selector('h3.item-description-title a')
            title = title.text
            print title
            # Price
            price = item.find_element_by_css_selector('div.about')
            price = price.text
            print price
            # Image
            try :
              image = item.find_element_by_css_selector('div.large-picture')
              style = image.get_attribute('style')
              start = '('
              end = ')'
              s = style
              img = s[s.find(start)+len(start):s.rfind(end)]
              start = '"'
              end = '"'
              s = img
              im = s[s.find(start)+len(start):s.rfind(end)]
              print im
            except :
              im = None
            # Phone
            try :
              show = item.find_element_by_css_selector('div.item_table-extended-contacts button')
              show.click()
              phone = item.find_element_by_css_selector('div.item_table-extended-contacts img')
              src = phone.get_attribute('src')
              imagestr = src.split(',', 1) # split() only once
              imagestr = imagestr[1]
              j = str(i)
              with open("phones/" + search + j + ".png","wb") as f:
                  f.write(decodestring(imagestr))
              
              phonenum = image_to_string(Image.open("phones/" + search + j + ".png"))
              print phonenum
            except :
              phonenum = None

            try:
                cursor.execute("""INSERT INTO phones (title, price, image, phone)
                          VALUES (%s, %s, %s, %s)""", 
                         (title.encode('utf-8'), 
                          price.encode('utf-8'),
                          im,
                          phonenum))

                conn.commit()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])

        # GET BACK TO MAIN PAGE
        driver.back()                  
        WebDriverWait(driver, 3)
        driver.switch_to.window(driver.window_handles[0])
        print "---------------------------------------------"             

                     
driver.close()
