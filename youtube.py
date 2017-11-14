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
__icon__ = path.dirname(__file__) + '/icons/YouTube.png'


REQUEST_HEADERS = {
  'User-Agent': (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/62.0.3202.62 Safari/537.36'
  )
}
session = requests.Session()
session.trust_env = False
re_videos = re.compile(r'"contents":(\[{"videoRenderer":.*}\]),"continuations"')


class SuggestionItem(Item):
  def __init__(self, suggestion):
    super().__init__(
      id=str(hash(suggestion)),
      icon=__icon__,
      text=suggestion,
      completion=__trigger__ + suggestion + '_',
      actions=[
        UrlAction(
          'Search on YouTube',
          'https://youtube.com/search?q={}'.format(suggestion)
        )
      ]
    )

class ResultItem(Item):
  def __init__(self, video, query):
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

      super().__init__(
        id=video['videoId'],
        text=text,
        icon=__icon__,
        completion=__trigger__ + query + '_',
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
    debug(query)
    return [Item(text='No results found')]

  videos = json.loads(match.groups()[0])
  return [ResultItem(video['videoRenderer'], query) for video in videos if video.get('videoRenderer')]


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
  return [SuggestionItem(suggestion[0]) for suggestion in suggestions]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    if query.string[-1] == '_':
      items = search(query.string[:-1])
    else:
      items = complete(query.string)
      items.insert(0, SuggestionItem(query.string))
    return items

  return [Item(icon=__icon__, text='YouTube')]

