#coding=utf-8

from faker import Factory
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase

class HomePageViewTest(LiveServerTestCase):
    """docstring for HomePageViewTest"""
        
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

