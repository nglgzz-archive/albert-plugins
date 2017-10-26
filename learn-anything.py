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

iconPath = '/home/zxcv/projects/nglgzz/albert_plugins/icons/LearnAnything.png'

def to_item(suggestion):
  return Item(
    id=suggestion['id'],
    text=suggestion['key'],
    icon=iconPath,
    subtext=suggestion['key'],
    actions=[ProcAction('Search on Learn Anything',
      ['chromium', 'https://learn-anything.xyz/{}'.format(suggestion['id'])]
    )]
  )


def search(query):
  response = requests.get("https://learn-anything.xyz/api/maps", params={
    "q": query,
  })
  suggestions = json.loads(response.text)
  return [to_item(suggestion) for suggestion in suggestions]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    items = search(query.string)
    return items
  return []
