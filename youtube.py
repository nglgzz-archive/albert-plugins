"""
  Get suggestions from Youtube
"""
from albertv0 import *
from os import path
import requests
import json
import re


__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Youtube Suggestions'
__version__ = '1.0'
__trigger__ = 'yt '
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
iconPath = path.dirname(__file__) + '/icons/YouTube.png'
re_videos = re.compile(r'"contents":(\[{"videoRenderer":.*}\]),"continuations"')


def search_to_item(video):
  try:
    text = video['title']['simpleText']
    subtext = '{} \t| {} | {}'.format(
      video['shortViewCountText']['simpleText'],
      video['lengthText']['simpleText'],
      video['ownerText']['runs'][0]['text'],
    )
    actions = [
      UrlAction('Watch on Youtube', 'https://youtube.com/watch?v={}'.format(video['videoId']))
    ]
  # text = suggestion.strip('\n')
  # subtext = url
  # actions = [ProcAction('Open on YouTube', ['sh', '-c', 'chromix-too rm youtube.com && chromix-too open https://youtube.com{}'.format(url)])]
  # chromix-too ls youtube.com | awk '{print $1}'
  # chromix-too raw chrome.tabs.update 441 '{ "url": "https://..." }'

    return Item(
      id=video['videoId'],
      text=text,
      icon=iconPath,
      subtext=subtext,
      actions=actions
    )
  except:
    debug(json.dumps(video))


def search(query):
  response = session.get('https://www.youtube.com/results',
    headers=REQUEST_HEADERS,
    params={
      'search_query': query,
    }
  )
  match = re_videos.search(response.text)

  if not match:
    return [Item(text='No results found')]

  videos = json.loads(match.groups()[0])
  return [search_to_item(video['videoRenderer']) for video in videos if video.get('videoRenderer')]


def completion_to_item(suggestion):
  text = suggestion
  subtext = suggestion
  actions = [ProcAction('Search on Youtube', ['sh', '-c', '/home/zxcv/projects/.albert_trigger.sh  "yt _{}"'.format(suggestion)])]

  return Item(
    id=str(hash(suggestion)),
    text=text,
    icon=iconPath,
    subtext=subtext,
    actions=actions
  )


def complete(query):
  response = session.get('https://clients1.google.com/complete/search',
    headers=REQUEST_HEADERS,
    params={
      'client': 'youtube',
      'output': 'toolbar',
      'hl': 'en',
      'q': query,
    }
  )
  response = response.text.lstrip('window.google.ac.h(').rstrip(')')
  suggestions = json.loads(response)[1]
  return [completion_to_item(suggestion[0]) for suggestion in suggestions]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    if query.string[0] == '_':
      items = search(query.string[1:])
    else:
      items = complete(query.string)
    return items
  return []
