import requests
import re
import os
import logging
import yaml
from scarnd.gbif import create_gbif_url
import json
from dotenv import load_dotenv
import sys


load_dotenv()
logger = logging.getLogger(__name__)

session = requests.Session()
session.headers.update({
    "User-Agent": "biodiversity-aq/scar-network-datasets",
    "Accept": "application/vnd.github.v3+json"
})

token = os.getenv("GITHUB_TOKEN")
if token:
    logger.info(f"Adding token *****{token[36:]}")
    session.headers.update({
        "Authorization": f"Bearer {token}"
    })
else:
    logger.error("No token found")


def parse_issue_body(body):
    lines = [item.strip() for item in re.split("[\r\n]+-", body)]
    props = [[re.sub("-\s+", "", s.strip()) for s in line.split(":", 1)] for line in lines]
    props_dict = {prop[0]: prop[1] for prop in props}
    if "URLs" not in props_dict:
        return None
    props_dict["URLs"] = [url.strip() for url in props_dict["URLs"].splitlines()]
    return props_dict


def get_github_issues():
    page = 1
    issues = []
    while True:
        res = session.get(url=f"https://api.github.com/repos/biodiversity-aq/scar-network-datasets/issues?state=all&labels=dataset&page={page}")
        if res.status_code != 200:
            sys.exit(f"Error: GitHub API returned status {res.status_code}")
        issues_page = res.json()
        if len(issues_page) == 0:
            break
        for issue in issues_page:
            issue["body"] = parse_issue_body(issue["body"])
        issues = issues + issues_page
        page = page + 1
    return issues


def create_github_issue(gbif_dataset, identifiers):
    url = create_gbif_url(gbif_dataset["key"])
    props = [
        {"title": gbif_dataset["title"]},
        {"GBIF": url},
        {"type": gbif_dataset["type"]},
        {"created": gbif_dataset["created"]},
        {"URLs": identifiers}
    ]
    data = {
        "title": gbif_dataset["title"],
        "body": yaml.dump(props),
        "labels": ["dataset"]
    }
    res = session.post("https://api.github.com/repos/biodiversity-aq/scar-network-datasets/issues", json.dumps(data))
    logger.info(f"Status code: {res.status_code}")
    logger.info("Created GitHub issue")
