"""
  Get suggestions from Google
"""
from albertv0 import *
import requests
import json

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Google Suggestions'
__version__ = '1.0'
__trigger__ = 'gg '
__author__ = 'Angelo Gazzola'
__dependencies__ = []

iconPath = '/home/zxcv/projects/nglgzz/albert_plugins/icons/Google.png'

def to_item(suggestion):
  return Item(
    id=str(hash(suggestion)),
    text=suggestion,
    icon=iconPath,
    subtext=suggestion,
    actions=[ProcAction('Search on Google',
      ['chromium', 'https://google.com/search?q={}'.format(suggestion)]
    )]
  )


def search(query):
  response = requests.get('https://clients1.google.com/complete/search', params={
    'client': 'firefox',
    'output': 'toolbar',
    'hl': 'en',
    'q': query,
  })
  suggestions = json.loads(response.text)[1]
  return [to_item(suggestion) for suggestion in suggestions]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    items = search(query.string)
    items.insert(0, to_item(query.string))
    return items
  return []