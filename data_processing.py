import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def generate_graphs_and_statistics(logger, today, issues, prs):
    logger.info("Generating graphs and statistics for issues and pull requests...")

    # Convert issues and prs to pandas DataFrames
    issues_df = pd.DataFrame(
        [
            {
                "number": issue.number,
                "title": issue.title,
                "user": issue.user.login,
                "state": issue.state,
                "created_at": issue.created_at,
                "updated_at": issue.updated_at,
                "comments": issue.comments,
                "labels": ", ".join([label.name for label in issue.labels]),
            }
            for issue in issues
        ]
    )

    prs_df = pd.DataFrame(
        [
            {
                "number": pr.number,
                "title": pr.title,
                "user": pr.user.login,
                "state": pr.state,
                "created_at": pr.created_at,
                "updated_at": pr.updated_at,
                "comments": pr.comments,
                "labels": ", ".join([label.name for label in pr.labels]),
            }
            for pr in prs
        ]
    )

    # issues_df.to_csv(f"{today}/issues_df.csv", index=False)
    # prs_df.to_csv(f"{today}/prs_df.csv", index=False)

    # Generate statistics
    issues_by_user = issues_df["user"].value_counts()
    prs_by_user = prs_df["user"].value_counts()
    comments_by_user = issues_df.groupby("user")["comments"].sum()

    # Ensure all series have the same index
    all_users = issues_by_user.index.union(prs_by_user.index).union(
        comments_by_user.index
    )
    issues_by_user = issues_by_user.reindex(all_users, fill_value=0)
    prs_by_user = prs_by_user.reindex(all_users, fill_value=0)
    comments_by_user = comments_by_user.reindex(all_users, fill_value=0)

    # Generate graphs
    fig, ax = plt.subplots()
    width = 0.2  # width of the bars
    x = np.arange(len(issues_by_user))  # label locations

    rects1 = ax.bar(x - width, issues_by_user.values, width, label="Issues")
    rects2 = ax.bar(x, prs_by_user.values, width, label="PRs")
    rects3 = ax.bar(x + width, comments_by_user.values, width, label="Comments")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Counts")
    ax.set_title("Issues, PRs and Comments by User")
    ax.set_xticks(x)
    ax.set_xticklabels(issues_by_user.keys(), rotation=90)
    ax.legend()

    autolabel(ax, rects1)
    autolabel(ax, rects2)
    autolabel(ax, rects3)

    fig.tight_layout()

    plt.savefig(f"{today}/graphs.png")

    logger.info("Generated graphs and statistics successfully.")
    return f"graphs.png"


def autolabel(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            "{}".format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
        )
