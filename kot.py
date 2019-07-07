import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import random

class Kot:
  LOGIN_URL = 'https://s3.kingtime.jp/admin'
  HOLIDAYS = ['Sat', 'Sun']
  HOLIDAY_CLASS = ['htBlock-scrollTable_sunday', 'htBlock-scrollTable_saturday']

  def __init__(self):
    self.id = os.environ['KOT_ID']
    self.password = os.environ['KOT_PASSWORD']
    options = Options()
    options.binary_location = os.environ['CHROME_PATH']
    options.add_argument('lang=en')
    #options.add_argument('--headless')
    self.driver = webdriver.Chrome(chrome_options=options)

  def login(self):
    self.driver.get(self.LOGIN_URL)
    self.driver.find_element_by_id('login_id').send_keys(self.id)
    self.driver.find_element_by_id('login_password').send_keys(self.password)
    self.driver.find_element_by_id('login_button').click()

  def stamp(self, day):
    target_row = self.target_row(day)
    if self.holiday(target_row): return 'Holiday: {}'.format(self.kot_date)
    url_after_login = self.driver.current_url

    # Go to target page
    Select(target_row.find_element_by_tag_name('select')).select_by_visible_text('Edit time-record')

    # Stamp attendance
    Select(self.driver.find_element_by_id('recording_type_code_1')).select_by_visible_text('Clock-in')
    self.driver.find_element_by_id('recording_timestamp_time_1').send_keys(type(self).volatile_time(830))
    Select(self.driver.find_element_by_id('recording_type_code_2')).select_by_visible_text('Clock-out')
    self.driver.find_element_by_id('recording_timestamp_time_2').send_keys(type(self).volatile_time(1900))
    self.driver.find_element_by_id('button_01').click()

    # Confirm success
    if self.driver.current_url == url_after_login:
      return 'Stamp Success: {}'.format(self.kot_date)
    return 'Something Wrong: {}'.format(self.kot_date)

  def target_row(self, day):
    table = self.driver.find_element_by_class_name('htBlock-adjastableTableF').find_element_by_tag_name('tbody')
    return table.find_elements_by_tag_name('tr')[day-1]

  def holiday(self, row):
    element = row.find_element_by_class_name('htBlock-scrollTable_day')
    self.kot_date = element.text
    if any([holiday in self.kot_date for holiday in self.HOLIDAYS]):
      return True
    element_class = element.get_attribute('class')
    if any([holiday_class == element_class for holiday_class in self.HOLIDAY_CLASS]):
      return True
    return False

  @classmethod
  def volatile_time(cls, time):
    return time + random.randrange(-20, 20)
