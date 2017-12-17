"""
  Get suggestions for Learn Anything
"""
from albertv0 import *
from os import path
import requests
import json
import re


__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Cheat.sh'
__version__ = '1.0'
__trigger__ = 'ch '
__author__ = 'Angelo Gazzola'
__dependencies__ = []
__icon__ = path.dirname(__file__) + '/icons/python.svg'


COLORS_PATTERN = re.compile(r'\[[\d;]*m');
REQUEST_HEADERS = {
  'User-Agent': (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/62.0.3202.62 Safari/537.36'
  )
}
session = requests.Session()
session.trust_env = False


def to_item(text, id):
  return Item(
    id=id,
    text=text,
    icon=__icon__,
    actions=[
      ClipAction("Copy result to clipboard", text)
    ]
  )

def search(query):
  response = session.get("http://cheat.sh/{}".format(query))
  text = COLORS_PATTERN.sub('', response.text)
  return [to_item(chunk, query + str(index))
    for index, chunk in enumerate(text.split('\n\n'))]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    return search(query.string)
  return [Item(icon=__icon__, text='Cheat')]
