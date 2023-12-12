'''
python approvePr.py
  -pull_request_number=PR NUMBER
  -github_token=TOKEN
'''

import requests
import argparse
parser = argparse.ArgumentParser()

def merge_pull_request(repo_owner, repo_name, pull_request_number, github_token):
  url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_request_number}/merge'

  headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
  }

  merge_data = {
    'commit_title': 'merge pull request',
    'commit_message': 'automatically merged by Jenkins'
  }

  response = requests.put(url, headers=headers, json=merge_data)

  if response.status_code == 200:
    print(f'merged pull request #{pull_request_number}.')
  else:
    print(f'failed merge pull request. status code: {response.status_code}')
    print(response.json())

parser.add_argument("-pull_request_number", "--pull_request_number", help="pull request number")
parser.add_argument("-github_token", "--github_token", help="github token")
args = parser.parse_args()

pull_request_number = args.pull_request_number
github_token = args.github_token
repo_owner = "danilo-lopes"
repo_name = "recursive"

merge_pull_request(repo_owner, repo_name, pull_request_number, github_token)
