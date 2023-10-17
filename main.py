import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from github import Github, Auth
from git import Repo
from flask import Flask, request, render_template, send_file
from github_client import fetch_issues_and_prs
from utils import save_to_markdown
import tempfile
import time

load_dotenv()  # take environment variables from .env.

# Get environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get today's date
today = datetime.now().strftime("%B %d, %Y")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        repo_link = request.form.get("repo_link")
        days = int(request.form.get("days"))
        logger.info("Starting script...")

        # Parse owner and repo name from the repo_link
        OWNER, REPO_NAME = repo_link.split("/")[-2:]

        # Initialize Github client and get the repo
        start_time = time.time()
        auth = Auth.Token(GITHUB_TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(f"{OWNER}/{REPO_NAME}")
        end_time = time.time()
        print(
            f"Time taken for Github client and repo initialization: {end_time - start_time} seconds"
        )

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Perform your operations on the repo
            start_time = time.time()
            issues, prs = fetch_issues_and_prs(logger, today, days, repo)
            end_time = time.time()
            print(
                f"Time taken for fetch_issues_and_prs: {end_time - start_time} seconds"
            )

            issues = sorted(issues, key=lambda i: i.updated_at, reverse=True)
            prs = sorted(prs, key=lambda p: p.updated_at, reverse=True)

            # Save to markdown
            start_time = time.time()
            markdown_content = save_to_markdown(
                logger,
                today,
                issues,
                prs,
                graph_filename="graphs.png",
                directory=tmpdirname,
            )
            end_time = time.time()
            print(f"Time taken for save_to_markdown: {end_time - start_time} seconds")

            # Return the markdown content as a response
            return markdown_content

        # The temporary directory and its contents are automatically deleted here

        return response

    return render_template("index.html")  # render a form for input


if __name__ == "__main__":
    app.run(debug=True)
