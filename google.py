"""
  Get suggestions from Google
"""
from albertv0 import *
from os import path
import requests
import json


__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Google Suggestions'
__version__ = '1.0'
__trigger__ = 'gg '
__author__ = 'Angelo Gazzola'
__dependencies__ = []


REQUEST_HEADERS = {
  'User-Agent': (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/62.0.3202.62 Safari/537.36'
  )
}
session = requests.Session()
session.trust_env = False

iconPath = path.dirname(__file__) + '/icons/Google.png'


def to_item(suggestion):
  return Item(
    id=str(hash(suggestion)),
    text=suggestion,
    icon=iconPath,
    subtext=suggestion,
    actions=[
      UrlAction('Search on Google', 'https://google.com/search?q={}'.format(suggestion)),
    ]
  )


def search(query):
  response = session.get('https://clients1.google.com/complete/search',
    headers=REQUEST_HEADERS,
    params={
      'client': 'firefox',
      'output': 'toolbar',
      'hl': 'en',
      'q': query,
    }
  )
  suggestions = json.loads(response.text)[1]
  return [to_item(suggestion) for suggestion in suggestions]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    items = search(query.string)
    items.insert(0, to_item(query.string))
    return items
  return []