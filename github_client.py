from datetime import datetime, timedelta
import pandas as pd


def fetch_issues_and_prs(logger, today, days, repo):
    logger.info("Fetching all issues and pull requests...")
    all_issues = repo.get_issues(state="all")

    days_ago = datetime.now() - timedelta(days=days)

    issues = [
        issue
        for issue in all_issues
        if issue.updated_at >= days_ago and not issue.pull_request
    ]
    prs = [
        issue
        for issue in all_issues
        if issue.updated_at >= days_ago and issue.pull_request
    ]

    logger.info(f"Fetched {len(issues)} issues and {len(prs)} pull requests.")
    all_data = issues + prs
    all_data_df = pd.DataFrame(all_data)
    all_data_df.to_csv(f"{today}/data.csv", index=False)
    return issues, prs
