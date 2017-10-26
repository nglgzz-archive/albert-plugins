"""
  Search GitHub repos
"""
from albertv0 import *
from os import path
import requests
import json

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'GitHub Repos'
__version__ = '1.0'
__trigger__ = 'gh '
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

iconPath = path.dirname(__file__) + '/icons/GitHub.png'


def to_item(repo):
  description = repo["description"]

  if description and len(description) > 40:
    description = description[:40] + "..."

  subtext = "{} ({} issues - {} forks)".format(
    description,
    repo["open_issues"],
    repo["forks_count"]
  )

  return Item(
    id=str(repo['id']),
    text=repo['full_name'],
    icon=iconPath,
    subtext=subtext,
    actions=[
      UrlAction('View on Github', repo['html_url']),
      ClipAction('Copy clone url', repo['clone_url']),
    ]
  )


def search(query):
  response = session.get("https://api.github.com/search/repositories",
    headers=REQUEST_HEADERS,
    params={
      "q": query,
    }
  )

  if response.json().get('items'):
    repos = sorted(
      response.json()['items'],
      key=(lambda el: int(el["stargazers_count"]))
    )

    return [to_item(repo) for repo in repos]
  return []


def handleQuery(query):
  if query.isTriggered and len(query.string) > 0:
    items = search(query.string)
    return items
  return []