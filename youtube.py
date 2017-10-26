"""
  Get suggestions from Youtube
"""
from albertv0 import *
from bs4 import BeautifulSoup
import requests
import json

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Youtube Suggestions'
__version__ = '1.0'
__trigger__ = 'yt '
__author__ = 'Angelo Gazzola'
__dependencies__ = []

iconPath = '/home/zxcv/projects/nglgzz/albert_plugins/icons/YouTube.png'

def to_item(suggestion, url=''):
  if len(url) == 0:
    text = suggestion
    subtext = suggestion
    actions = [ProcAction('Search on Youtube', ['sh', '-c', '/home/zxcv/projects/.albert_trigger.sh  "yt _{}"'.format(suggestion)])]
  else :
    text = suggestion.strip('\n')
    subtext = url
    actions = [ProcAction('Open on YouTube', ['sh', '-c', 'chromix-too rm youtube.com && chromix-too open https://youtube.com{}'.format(url)])]
    # chromix-too ls youtube.com | awk '{print $1}'
    # chromix-too raw chrome.tabs.update 441 '{ "url": "https://..." }'

  return Item(
    id=str(hash(suggestion)),
    text=text,
    icon=iconPath,
    subtext=subtext,
    actions=actions
  )


def search(query):
  response = requests.get('https://www.youtube.com/results', params={
    'search_query': query,
  })
  response = BeautifulSoup(response.text, 'html5lib')
  results = response.body.find_all(lambda el: len(el.get('href', '')) > 7 and len(el.get('title', '')) > 0 and el['href'][:7] == '/watch?')
  results = [(res.text, res['href']) for res in results]
  return [to_item(res[0], res[1]) for res in results]

def complete(query):
  response = requests.get('https://clients1.google.com/complete/search', params={
    'client': 'youtube',
    'output': 'toolbar',
    'hl': 'en',
    'q': query,
  })
  response = response.text.lstrip('window.google.ac.h(').rstrip(')')
  suggestions = json.loads(response)[1]
  return [to_item(suggestion[0]) for suggestion in suggestions]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    if query.string[0] == '_':
      items = search(query.string[1:])
    else:
      items = complete(query.string)
    return items
  return []
