'''
python createPr.py
  -github_token=TOKEN
  -origin_branch="release/3.0.19+250"
  -destination_branch="master"
  -tag_name="3.0.19+250"
'''

import requests
import argparse
import os

parser = argparse.ArgumentParser()

def create_tag_and_release(repo_owner, repo_name, tag_name, branch_name, github_token):
  api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"

  headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github.v3+json"
  }

  data = {
    "tag_name": tag_name,
    "target_commitish": f"{branch_name}",
    "name": f"{tag_name} - Produção",
    "body": tag_name,
    "draft": False,
    "prerelease": False
  }

  response = requests.post(api_url, headers=headers, json=data)

  if response.status_code == 201:
    print(f"release {tag_name} created successfully!")
  else:
    print(f"failed to create release. status code: {response.status_code}")
    print(response.text)

def create_pull_request(repo_owner, repo_name, base_branch, head_branch, title, body, token):
  url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"

  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
  }

  data = {
    "title": title,
    "body": body,
    "head": head_branch,
    "base": base_branch
  }

  response = requests.post(url, headers=headers, json=data)

  if response.status_code == 201:
    print("pull request created successfully.")
    return response.json()
  else:
    print(f"failed to create pull request. status code: {response.status_code}.")
    print(response.text)
    return None
  
def delete_branch(repo_owner, repo_name, branch_name, token):
  url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/{branch_name}"

  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
  }

  response = requests.delete(url, headers=headers)

  if response.status_code == 204:
    print(f"branch '{branch_name}' deleted successfully.")
  elif response.status_code == 404:
    print(f"branch '{branch_name}' not found.")
  else:
    print(f"failed to delete branch '{branch_name}'. status code: {response.status_code}")
    print(response.text)

parser.add_argument("-origin_branch", "--origin_branch", help="origin branch")
parser.add_argument("-destination_branch", "--destination_branch", help="destination branch")
parser.add_argument("-github_token", "--github_token", help="github token")
parser.add_argument("-tag_name", "--tag_name", help="tag name")
args = parser.parse_args()

github_token = args.github_token
destination_branch = args.destination_branch
origin_branch = args.origin_branch
tag_name = args.tag_name

title = "Jenkins Pull Request"
body = "pull request aberto automaticamente pelo Jenkins"
repo_owner = "danilo-lopes"
repo_name = "recursive"

pull_request = create_pull_request(repo_owner, repo_name, destination_branch, origin_branch, title, body, github_token)

if pull_request:
  pull_request_number = pull_request['number']
  os.system(f"python mergePr.py -pull_request_number={pull_request_number} -github_token={github_token}")

  create_tag_and_release(repo_owner, repo_name, tag_name, destination_branch, github_token)
  delete_branch(repo_owner, repo_name, origin_branch, github_token)
