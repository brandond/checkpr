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
@click.option('--token', help='Github auth token', envvar='GITHUB_TOKEN', required=True)
@click.option('--branch', help='Branch to check; default all')
@click.option('--repos', help='Path to directory containing git repos, such as $HOME/go/src/github.com', type=click.Path(exists=True, file_okay=False))
def main(repo, token, branch, repos):
    issue_re = re.compile(fr"({repo}/issues/|{repo}#|\W#)(\d+)")
    gh = Github(token)

    gh_repo = gh.get_repo(repo)
    kwargs = {}

    if branch:
        kwargs['base'] = branch

    repo_ok = False

    if not repos:
        gopath = os.getenv("GOPATH") or os.path.join(os.getenv("HOME"), "go")
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
        print(f"\n{gh_pull.base.ref:>12} | {gh_pull.title} by @{gh_pull.user.login}\t{colored(gh_pull.html_url, 'white', attrs=['underline'])}")
        padwidth = len(f"{gh_pull.title} by @{gh_pull.user.login}")

        matches = issue_re.findall(gh_pull.body or "")
        if not matches:
            print("\t     | " + colored('NO LINKED ISSUES FOUND', 'white', attrs=['bold']))

        seen_ids = set()
        for match in matches:
            try:
                gh_issue = gh_repo.get_issue(int(match[1]))
                gh_issue.__class__.get_events = get_events
            except Exception:
                print(f"\t     | Issue #{match[1]} not found")
                continue

            if gh_issue.id in seen_ids:
                continue

            seen_ids.add(gh_issue.id)
            state = gh_issue.state
            if gh_issue.pull_request and gh_issue.pull_request.html_url == gh_issue.html_url:
                state = 'pr'

            if state == 'open':
                state = colored(f"{state:>6}", 'green')
            elif state == 'closed':
                state = colored(f"{state:>6}", 'red')
            else:
                state = colored(f"{state:>6}", 'magenta')

            print(f"      {state} | {gh_issue.title:<{padwidth}}\t{colored(gh_issue.html_url, 'white', attrs=['underline'])}")

            if 'pr' in state:
                continue

            milestone = "NO MILESTONE"
            project_column = ""

            if gh_issue.milestone:
                milestone = gh_issue.milestone.title

            for gh_event in gh_issue.get_events():
                if gh_event.event == 'moved_columns_in_project':
                    project_column = gh_event.__dict__['_rawData']['project_card']['column_name']

            assignees = ' '.join(map(lambda a: '@' + a.login, gh_issue.assignees))

            if 'NO MILESTONE' in milestone:
                milestone = colored(milestone, 'white', attrs=['bold'])

            if 'Done' in project_column:
                project_column = '- ' + colored(project_column, 'red')
            elif 'Test' in project_column:
                project_column = '- ' + colored(project_column, 'yellow')
            elif project_column:
                project_column = '- ' + colored(project_column, 'green')

            print(f"\t     | Milestone: {milestone} {project_column}\t{assignees}")

            if repo_ok and gh_pull.merge_commit_sha:
                gitcmd = f"git --git-dir={repos}/{repo}/.git tag --sort=committerdate --contains={gh_pull.merge_commit_sha}"
                (exitcode, output) = subprocess.getstatusoutput(gitcmd)
                if output and exitcode == 0:
                    # show latest GA release tag if possible; otherwise just the latest alpha/beta/rc containing this commit
                    ga_tag = ''
                    for tag in output.splitlines():
                        if '-' not in tag:
                            ga_tag = tag
                    if ga_tag:
                        tag = ga_tag

                    if project_column and semver(tag) != semver(milestone):
                        tag = colored(tag, 'red', attrs=['bold'])
                    print(f"\t     | Tag:       {tag}")

            if gh_issue.state == "closed":
                print(f"\t     | Closed by: @{gh_issue.closed_by.login}")


def semver(version):
    m = re.search(r'(\d+\.\d+\.\d+)', version)
    if m:
        return m.group(0)
    return version


def get_events(self):
    return github.PaginatedList.PaginatedList(
        github.IssueEvent.IssueEvent,
        self._requester,
        f"{self.url}/events",
        None,
        headers={"Accept": "application/vnd.github.starfox-preview+json"},
    )


if __name__ == "__main__":
    try:
        main()
    except github.GithubException as ex:
        print(f"Github API error {ex.status}: {ex.data['message']}")
