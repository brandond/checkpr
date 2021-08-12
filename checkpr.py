#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import click
import github
import subprocess
import os.path
from github import Github


@click.command()
@click.argument('repo')
@click.option('--token', help='Github auth token', envvar='GITHUB_TOKEN', required=True)
@click.option('--branch', help='Branch to check; default all')
@click.option('--repos', help='Path to directory containing git repos, such as $HOME/go/src/github.com', type=click.Path(exists=True, file_okay=False))
def main(repo, token, branch, repos):
    issue_re = re.compile(f"({repo}/issues/|{repo}#|\W#)(\d+)")
    gh = Github(token)

    gh_repo = gh.get_repo(repo)
    kwargs = {}

    if branch:
        kwargs['base'] = branch

    repo_ok = False

    if not repos:
        gopath = os.getenv("GOPATH") or os.path.join(getenv("HOME"), "go")
        go_repos = os.path.join(gopath, "src", "github.com")
        if os.path.exists(go_repos):
            repos = go_repos
            print(f"Using repos from GOPATH: {repos}")

    if repos:
        print(f"Fetching tags in {repos}/{repo}...")
        (exitcode, output) = subprocess.getstatusoutput(f"git --git-dir={repos}/{repo}/.git fetch --tags")
        print(output)
        repo_ok = exitcode == 0

    for gh_pull in gh_repo.get_pulls(state='closed', **kwargs):
        if not gh_pull.merged:
            continue
        print(f"\n{gh_pull.title} by @{gh_pull.user.login}\t{gh_pull.html_url}")
        matches =  issue_re.findall(gh_pull.body or "")
        if not matches:
            print("\tNO LINKED ISSUES FOUND")
        for match in matches:
            issue = int(match[1])
            try:
                gh_issue = gh_repo.get_issue(issue)
                gh_issue.__class__.get_events = get_events
            except Exception:
                print(f"\tIssue #{issue} not found")
                continue

            if gh_issue.pull_request and gh_issue.pull_request.html_url == gh_issue.html_url:
                print(f"\t[pr]   {gh_issue.title}\t{gh_issue.html_url}")
                continue

            print(f"\t[{gh_issue.state}] {gh_issue.title}\t{gh_issue.html_url}")

            milestone = "NO MILESTONE"
            project_column= ""

            if gh_issue.milestone:
                milestone = gh_issue.milestone.title

            for gh_event in gh_issue.get_events():
                if gh_event.event == 'moved_columns_in_project':
                    project_column = "- " + gh_event.__dict__['_rawData']['project_card']['column_name']

            assignees = ' '.join(map(lambda a: '@' + a.login, gh_issue.assignees))

            print(f"\t\tMilestone: {milestone} {project_column}\t{assignees}")

            if repo_ok and gh_pull.merge_commit_sha:
                (exitcode, output) = subprocess.getstatusoutput(f"git --git-dir={repos}/{repo}/.git tag --sort=committerdate --contains={gh_pull.merge_commit_sha}")
                if output and exitcode == 0:
                    # show latest GA release tag if possible; otherwise just the latest alpha/beta/rc containing this commit
                    ga_tag = ''
                    for tag in output.splitlines():
                        if '-' not in tag:
                            ga_tag = tag
                    if ga_tag:
                        tag = ga_tag
                    print(f"\t\tTag:       {tag}")

            if gh_issue.state == "closed":
                print(f"\t\tClosed by: @{gh_issue.closed_by.login}")


def get_events(self):
            return github.PaginatedList.PaginatedList(
            github.IssueEvent.IssueEvent,
            self._requester,
            f"{self.url}/events",
            None,
            headers={"Accept": "application/vnd.github.starfox-preview+json"},
        )

if __name__ == "__main__":
    main()
