#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import unittest
from random import randint
import MySQLdb



class DbSettings(unittest.TestCase):
	  db = None

	  @classmethod	  
	  def setUpClass(cls):
		  cls.db = MySQLdb.connect('localhost', 'root', '', 'selenium', charset="utf8", use_unicode=True)
		  


	  @classmethod
	  def tearDownClass(cls):
		  cls.db.close( )
		  print "------test is over------"




class tripadvisorTest(DbSettings):

	  def setUp(self):
		  display = Display(visible=0, size=(1366, 768))
		  display.start()
		  self.driver = webdriver.Firefox()
		  
 
 
	  def test_pagination(self):
		  driver=self.driver
		  driver.get('https://www.tripadvisor.ru/Hotels-g187497-Barcelona_Catalonia-Hotels.html')
		  driver.maximize_window()
		  
		  # DATABASE
		  conn = self.db
		  cursor = conn.cursor()		  
		  # create table
		  cursor.execute("SET sql_notes = 0; ")
		  sql = """
			  CREATE TABLE IF NOT EXISTS hotels (
				  id int(11) NOT NULL AUTO_INCREMENT,
				  title varchar(255) DEFAULT NULL,
				  city varchar(100) DEFAULT NULL,
				  price varchar(100) DEFAULT NULL,
				  link varchar(512) NOT NULL,
				  PRIMARY KEY (id),
				  UNIQUE KEY link (link)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;
		  """
		  cursor.execute(sql)
		  cursor.execute("SET sql_notes = 1; ")
		  
		  # DATA
		  breadcrumb = driver.find_element_by_xpath('//div[@id="taplc_trip_planner_breadcrumbs_0"]/ul/li[5]')
		  city = breadcrumb.find_element_by_css_selector('a span').text
		  print city
		  
		  #pages = driver.find_elements_by_xpath('//div[@class="pageNumbers"]/a')
		  divPages = driver.find_element_by_class_name('standard_pagination')
		  m = divPages.get_attribute('data-numpages')		  
		  numPages = "Number of pages: " + m
		  print numPages
		  print "----------------------------------------------"
		  m = int(m)
		  m = m + 1
		  pages = range(1, m)
		  #print pages
		  
		  for num in pages :
		  
			  try :				
				j = 0 #count items per 1 page

				blks = driver.find_elements(By.XPATH, '//div[@data-prwidget-name="meta_hsx_responsive_listing"]')
				for blk in blks :	
					  l = blk.find_element_by_class_name('prw_meta_hsx_listing_name')
					  lnk = l.find_element_by_tag_name('a')
					  title = lnk.text
					  href = lnk.get_attribute("href")
					  price = blk.find_element_by_class_name('price').text
					  print title + ": " + price

					  # DATABASE
					  if j < 100 : # to avoid bulk data errors
						  try:
							  cursor.execute("""INSERT INTO hotels (title, city, price, link)
									  VALUES (%s, %s, %s, %s)""", 
									 (title.encode('utf-8'),
									  city.encode('utf-8'),
									  price.encode('utf-8'),
									  href.encode('utf-8')))
						  
							  conn.commit()
						  except MySQLdb.Error, e:
							  print "Error %d: %s" % (e.args[0], e.args[1])

						  j = j+1
					  else :
						self.tearDown()

				  				
				# TEST CURRENT PAGE
				span = driver.find_element_by_css_selector('div.pageNumbers span.current')
				pnum = int(span.text)
				self.assertEqual(num, pnum)

				curnum = num
				print "------"				
				curPage = "Current page is: " + str(curnum)
				print curPage
				itemsInPage = "Items in page: " + str(j)
				print itemsInPage
				print "---------------------------------------------------------------"				

				# CLICK NEXT PAGE
				nextnum = curnum + 1
				nextnum = str(nextnum)
				alink = driver.find_element_by_xpath('//div[@class="pageNumbers"]/a[@data-page-number="' + nextnum + '"]')
				if alink :
				  alink.click()
				  rand = randint(4, 10)
				  time.sleep(rand)
				  WebDriverWait(driver, rand).until(EC.presence_of_element_located((By.ID, "taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"))) 
				  

			  except :
				pass	  
		  
		  
				 

	  def tearDown(self):
		   self.driver.quit()
		   



  
if __name__ == "__main__":
	unittest.main()
