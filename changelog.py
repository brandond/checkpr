#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import click
import github
import subprocess
import os.path
from github import Github
from termcolor import colored


@click.command()
@click.argument('repo')
@click.argument('commit1')
@click.argument('commit2')
@click.option('--token', help='Github auth token', envvar='GITHUB_TOKEN', required=True)
@click.option('--repos', help='Path to directory containing git repos, such as $HOME/go/src/github.com', type=click.Path(exists=True, file_okay=False))
def main(repo, commit1, commit2, token, repos):
    issue_re = re.compile(f"({repo}/issues/|{repo}#|\W#)(\d+)")
    gh = Github(token)

    gh_repo = gh.get_repo(repo)
    kwargs = {}

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

    if not repo_ok:
        print("Error: must have repo available")
        exit(1)

    (exitcode, output) = subprocess.getstatusoutput(f"git --git-dir={repos}/{repo}/.git log --no-merges --format=format:%H {commit1}..{commit2}")
    if output and exitcode == 0:
        seen_prs = set()
        for commit in output.splitlines():
            gh_commit = gh_repo.get_commit(commit)
            for gh_pull in gh_commit.get_pulls():
                if gh_pull.number not in seen_prs:
                    seen_prs.add(gh_pull.number)
                    title = gh_pull.title
                    m = re.search(r'```release-note\s*(.+)\s*```', gh_pull.body)
                    if m:
                        release_note = m.group(1).strip()
                        if release_note and release_note != 'NONE':
                            title = release_note
                    print(f"* {title} ([#{gh_pull.number}]({gh_pull.html_url}))  ")
                    print("  <!---")
                    for gh_file in gh_commit.files:
                        print(f"  {gh_file.filename}")
                    print("  --->")

    else:
        print(f"Error: git log failed\n{output}")
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except github.GithubException as ex:
        print(f"Github API error {ex.status}: {ex.data['message']}")
