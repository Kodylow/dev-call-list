from data_processing import generate_graphs_and_statistics


def write_to_file(f, items, state, item_type):
    f.write(f"\n\n# {state} {item_type}\n\n")
    for item in items:
        f.write(
            f"- {item.number}: [{item.title}]({item.html_url}) - ({item.updated_at})\n"
        )

        # labels = ", ".join([label.name for label in item.labels])
        # f.write(f"<details>\n")
        # f.write(f"<summary>{item.number}: [{item.title}]({item.html_url})</summary>\n")
        # f.write(f"<ul>\n")
        # f.write(f"  <li>User: {item.user.login}</li>\n")
        # f.write(f"  <li>State: {item.state}</li>\n")
        # f.write(f"  <li>Created At: {item.created_at}</li>\n")
        # f.write(f"  <li>Updated At: {item.updated_at}</li>\n")
        # f.write(f"  <li>Comments: {item.comments}</li>\n")
        # f.write(f"  <li>Labels: {labels}</li>\n")
        # f.write(f"</ul>\n")
        # f.write(f"</details>\n\n")

    # f.write(f"\n\n# {state} {item_type}\n\n")
    # f.write(
    #     "| Number | Title | User | State | Created At | Updated At | Comments | Labels |\n"
    # )
    # f.write(
    #     "|--------|-------|------|-------|------------|------------|----------|--------|\n"
    # )
    # for item in items:
    #     labels = ", ".join([label.name for label in item.labels])
    #     f.write(
    #         f"| #{item.number} | [{item.title}]({item.html_url}) | {item.user.login} | {item.state} | {item.created_at} | {item.updated_at} | {item.comments} | {labels} |\n"
    #     )

    # Add more useful information to the markdown
    # f.write(f"\n\n## Statistics for {state} {item_type}\n\n")
    # f.write(f"Total number: {len(items)}\n\n")

    # users = [item.user.login for item in items]
    # user_counts = {user: users.count(user) for user in set(users)}
    # f.write("Number of items per user:\n\n")
    # for user, count in user_counts.items():
    #     f.write(f"- {user}: {count}\n")


def save_to_markdown(logger, today, issues, prs, graph_filename):
    logger.info("Saving issues and pull requests to markdown...")
    with open(f"{today}/{today}.md", "w") as f:
        # generate_graphs_and_statistics(logger, today, issues, prs)

        # f.write("\n\n## Graphs\n\n")
        # f.write(f"![Issues and PRs by User](./{graph_filename})\n\n")

        for state in ["Open", "Closed"]:
            write_to_file(
                f,
                [i for i in issues if i.state.lower() == state.lower()],
                state,
                "Issues",
            )
            write_to_file(
                f,
                [p for p in prs if p.state.lower() == state.lower()],
                state,
                "Pull Requests",
            )

    logger.info("Saved issues and pull requests to markdown successfully.")
