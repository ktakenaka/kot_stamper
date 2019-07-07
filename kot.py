import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import random

class Kot:
  LOGIN_URL = 'https://s3.kingtime.jp/admin'

  def __init__(self):
    self.id = os.environ['KOT_ID']
    self.password = os.environ['KOT_PASSWORD']
    options = Options()
    options.binary_location = os.environ['CHROME_PATH']
    options.add_argument('lang=en')
    options.add_argument('--headless')
    self.driver = webdriver.Chrome(chrome_options=options)

  def login(self):
    self.driver.get(self.LOGIN_URL)
    self.driver.find_element_by_id('login_id').send_keys(self.id)
    self.driver.find_element_by_id('login_password').send_keys(self.password)
    self.driver.find_element_by_id('login_button').click()

  def stamp(self, day):
    menus = self.driver.find_elements_by_class_name('htBlock-selectOther')
    Select(menus[day-1]).select_by_visible_text('Edit time-record')
    Select(self.driver.find_element_by_id('recording_type_code_1')).select_by_visible_text('Clock-in')
    self.driver.find_element_by_id('recording_timestamp_time_1').send_keys(type(self).volatile_time(830))
    Select(self.driver.find_element_by_id('recording_type_code_2')).select_by_visible_text('Clock-out')
    self.driver.find_element_by_id('recording_timestamp_time_2').send_keys(type(self).volatile_time(1900))
    self.driver.find_element_by_id('button_01').click()

  @classmethod
  def volatile_time(cls, time):
    return time + random.randrange(-20, 20)
