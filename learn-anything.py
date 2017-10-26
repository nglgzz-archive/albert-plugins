"""
  Get suggestions for Learn Anything
"""
from albertv0 import *
import requests
import json

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Learn Anything Suggestions'
__version__ = '1.0'
__trigger__ = 'la '
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

iconPath = '/home/zxcv/projects/nglgzz/albert-plugins/icons/LearnAnything.png'


def to_item(suggestion):
  return Item(
    id=suggestion['id'],
    text=suggestion['key'],
    icon=iconPath,
    subtext=suggestion['key'],
    actions=[
      UrlAction('Search on Learn Anything', 'https://learn-anything.xyz/{}'.format(suggestion['id'])),
    ]
  )


def search(query):
  response = session.get("https://learn-anything.xyz/api/maps", params={
    "q": query,
  })
  suggestions = json.loads(response.text)
  return [to_item(suggestion) for suggestion in suggestions]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    items = search(query.string)
    return items
  return []
