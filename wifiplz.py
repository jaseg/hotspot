#!/usr/bin/env python3

from selenium import webdriver
#import wpa_driver

def login():
	driver = webdriver.Firefox()
	driver.get('http://clients3.google.com/generate_204')
	
	# free telekom login
	button = driver.find_element_by_class_name('dtag-button-connect')
	if button:
		button.click()
	
	del driver
	

if __name__ == '__main__':
	# TODO: MAC changing
	# TODO: Automatic network association
	login()
	# TODO: VPN setup
