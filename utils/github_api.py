# utils/github_api.py
import requests
from utils.config import GITHUB_TOKEN

class GitHubAPI:
    def __init__(self, token=None):
        self.token = token or GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_pull_request(self, owner, repo, pr_number):
        """Get pull request details."""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get PR: {response.status_code} - {response.text}")
    
    def get_pull_request_files(self, owner, repo, pr_number):
        """Get files changed in a pull request."""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get PR files: {response.status_code} - {response.text}")
    
    def create_pull_request_review(self, owner, repo, pr_number, comments):
        """Create a review comment on a pull request."""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
        response = requests.post(url, headers=self.headers, json=comments)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create review comment: {response.status_code} - {response.text}")
    
    def create_pull_request_review_comment(self, owner, repo, pr_number, commit_id, path, position, body):
        """Create a review comment on a specific line of code."""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
        data = {
            "commit_id": commit_id,
            "path": path,
            "position": position,
            "body": body
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create review comment: {response.status_code} - {response.text}")
    
    def get_repository_languages(self, owner, repo):
        """Get programming languages used in the repository."""
        url = f"{self.base_url}/repos/{owner}/{repo}/languages"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get repository languages: {response.status_code} - {response.text}")