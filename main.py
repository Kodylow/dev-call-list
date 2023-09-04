import logging
from github import Github, Auth
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Github token (make sure you have the correct permissions for the repo in your token)
GITHUB_TOKEN= os.environ.get('GITHUB_TOKEN')
auth = Auth.Token(GITHUB_TOKEN)
# Repo details
OWNER = 'fedimint'
REPO_NAME = 'fedimint'

logger.info('Initializing Github client...')
g = Github(auth=auth)
repo = g.get_repo(f"{OWNER}/{REPO_NAME}")
logger.info('Github client initialized successfully.')

def fetch_issues_and_prs():
    logger.info('Fetching all issues and pull requests...')
    # Fetch all issues (this will include pull requests too because in GitHub, PRs are also considered as issues)
    all_issues = repo.get_issues(state='all')

    issues = []
    prs = []

    for issue in all_issues:
        if issue.pull_request:
            prs.append(issue)
        else:
            issues.append(issue)

    logger.info(f'Fetched {len(issues)} issues and {len(prs)} pull requests.')
    return issues, prs

def save_to_markdown(issues, prs):
    logger.info('Saving issues and pull requests to markdown...')
    with open("issues_and_prs.md", "w") as f:
        # Dump issues
        f.write("# Issues\n\n")
        f.write("| Number | Title | User | State | Created At |\n")
        f.write("|--------|-------|------|-------|------------|\n")
        for issue in issues:
            f.write(f"| #{issue.number} | [{issue.title}]({issue.html_url}) | {issue.user.login} | {issue.state} | {issue.created_at} |\n")

        f.write("\n\n# Pull Requests\n\n")
        f.write("| Number | Title | User | State | Created At |\n")
        f.write("|--------|-------|------|-------|------------|\n")
        for pr in prs:
            f.write(f"| #{pr.number} | [{pr.title}]({pr.html_url}) | {pr.user.login} | {pr.state} | {pr.created_at} |\n")
    logger.info('Saved issues and pull requests to markdown successfully.')

if __name__ == "__main__":
    logger.info('Starting script...')
    issues, prs = fetch_issues_and_prs()
    save_to_markdown(issues, prs)
    logger.info('Data dumped to issues_and_prs.md successfully!')
    logger.info('Script finished.')
