import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from github import Github, Auth
import argparse
from github_client import fetch_issues_and_prs
from utils import save_to_markdown

# Add argument parsing
parser = argparse.ArgumentParser(description="Fetch issues and PRs from a GitHub repo.")
parser.add_argument(
    "-d", "--days", type=int, default=7, help="Number of days to filter by."
)
args = parser.parse_args()
days = args.days

load_dotenv()  # take environment variables from .env.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get today's date
today = datetime.now().strftime("%B %d, %Y")

# Create a directory with today's date
os.makedirs(today, exist_ok=True)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
auth = Auth.Token(GITHUB_TOKEN)
OWNER = "fedimint"
REPO_NAME = "fedimint"

logger.info("Initializing Github client...")
g = Github(auth=auth)
repo = g.get_repo(f"{OWNER}/{REPO_NAME}")
logger.info("Github client initialized successfully.")


if __name__ == "__main__":
    logger.info("Starting script...")
    issues, prs = fetch_issues_and_prs(logger, today, days, repo)
    issues = sorted(issues, key=lambda i: i.updated_at, reverse=True)
    prs = sorted(prs, key=lambda p: p.updated_at, reverse=True)
    save_to_markdown(logger, today, issues, prs, graph_filename="graphs.png")
    logger.info("Data dumped to issues_and_prs.md successfully!")
    logger.info("Script finished.")
