from datetime import date
from kot import Kot
from slackclient import SlackClient
import os

target_day = date.today().day
client = SlackClient(os.environ['SLACK_TOKEN'])

stamper = Kot()
try:
  stamper.login()
  result = stamper.stamp(target_day)
  client.api_call('chat.postMessage', channel='general', username='Stamp Attendance', text=result)
except:
  client.api_call('chat.postMessage', channel='general', username='Stamp Attendance', text='Failed: {}'.format(target_day))
