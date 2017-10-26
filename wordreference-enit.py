"""
  Wordreference autocompletion (enit)
"""
from albertv0 import *
import requests
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

iconPath = '/home/zxcv/projects/nglgzz/albert_plugins/icons/Wordreference.png'

def to_item(suggestion):
  return Item(
    id=str(hash(suggestion)),
    text=suggestion,
    icon=iconPath,
    subtext=suggestion,
    actions=[ProcAction('Search on Wordreference',
      ['chromium', 'http://www.wordreference.com/enit/{}'.format(suggestion)]
    )]
  )


def search(query):
  response = requests.get("http://www.wordreference.com/2012/autocomplete/autocomplete.aspx", params={
      "dict": "enit",
      "query": query,
    })
  suggestions = response.text.split('\n')
  return [to_item(suggestion.split('\t')[0]) for suggestion in suggestions if suggestion.split('\t')[0]]


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    items = search(query.string)
    items.insert(0, to_item(query.string))
    return items
  return []