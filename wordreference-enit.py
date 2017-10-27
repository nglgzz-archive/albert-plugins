"""
  Wordreference autocompletion (enit)
"""
from albertv0 import *
from os import path
import requests
import lxml.html
import json

"""
res = []

rows = document.querySelectorAll('tr')
rows.forEach((row) => {
  const FrWord = row.querySelector('.FrWrd strong');
  const desc = row.querySelector('.FrWrd+td');
  const ToWord = row.querySelector('.ToWrd');

  if (FrWord && desc && ToWord) {
    const r = {
      from: FrWord.textContent,
      desc: desc.textContent,
      to: ToWord.textContent,
    };

    if (r.from && r.desc && r.to) {
      res.push(r);
    }
  }
})
"""

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'Wordreference autocompletion (enit)'
__version__ = '1.0'
__trigger__ = 'enit '
__author__ = 'Angelo Gazzola'
__dependencies__ = []
__icon__ = path.dirname(__file__) + '/icons/Wordreference.png'
__lang__ = 'enit'

REQUEST_HEADERS = {
  'User-Agent': (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    ' Chrome/62.0.3202.62 Safari/537.36'
  )
}
session = requests.Session()
session.trust_env = False

iconPath = path.dirname(__file__) + '/icons/Wordreference.png'


class SuggestionItem(Item):
  def __init__(self, suggestion):
    super().__init__(
      id=str(hash(suggestion)),
      icon=__icon__,
      text=suggestion,
      completion=__trigger__ + suggestion,
      actions=[
        UrlAction(
          'Search on Wordreference',
          'http://www.wordreference.com/{}/{}'.format(__lang__, suggestion)
        )
      ]
    )


class ResultItem(Item):
  def __init__(self, result):
    super().__init__(
      id=str(hash(str(result[0]) + str(result[1]) + str(result[2]))),
      icon=__icon__,
      text=result[2],
      subtext='{} | {} | {}'.format(result[0], result[1], result[2])
    )


def search(query):
  response = session.get(
    "http://www.wordreference.com/{}/{}".format(__lang__, query),
    headers=REQUEST_HEADERS
  )
  html = lxml.html.fromstring(response.text)
  selections = html.cssselect('tr[id^="{}"]'.format(__lang__))
  results = []

  for sel in selections:
    sel = sel.getchildren()
    results.append((
      sel[0].find('strong').text,
      sel[1].text,
      sel[2].text
    ))

  return [ResultItem(r) for r in results]


def suggest(query):
  response = session.get("http://www.wordreference.com/2012/autocomplete/autocomplete.aspx",
    headers=REQUEST_HEADERS,
    params={
      "dict": __lang__,
      "query": query,
    }
  )
  suggestions = response.text.split('\n')
  return [SuggestionItem(suggestion.split('\t')[0]) for suggestion in suggestions if suggestion.split('\t')[0]]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    if query.string[-1] == '_':
      items = search(query.string[:-1])
    else:
      items = suggest(query.string)
      items.insert(0, SuggestionItem(query.string))
    return items
  return []