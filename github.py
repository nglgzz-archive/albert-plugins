"""
  Search GitHub repos
"""
from albertv0 import *
import requests
import json

__iid__ = 'PythonInterface/v0.1'
__prettyname__ = 'GitHub Repos'
__version__ = '1.0'
__trigger__ = 'gh '
__author__ = 'Angelo Gazzola'
__dependencies__ = []

iconPath = '/home/zxcv/projects/nglgzz/albert_plugins/icons/GitHub.png'

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
      ProcAction('View on Github', ['chromium', repo['html_url']]),
      ProcAction('Clone', ['sh', '-c', 'echo git clone {} | xclip -i -selection clipboard'.format(repo['clone_url'])]),
    ]
  )


def search(query):
  response = requests.get("https://api.github.com/search/repositories", params={
    "q": query,
  })

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