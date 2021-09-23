#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import click
import github
from github import Github


@click.command()
@click.argument('repo')
@click.argument('base')
@click.argument('head')
@click.option('--token', help='Github auth token', envvar='GITHUB_TOKEN', required=True)
def main(repo, base, head, token):
    gh = Github(token)
    gh_repo = gh.get_repo(repo)

    seen_prs = set()
    for gh_commit in gh_repo.compare(base, head).commits:
        if len(gh_commit.parents) > 1:
            continue
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
        print(f"  {gh_commit.commit.message.splitlines()[0]}")
        vendor_files = 0
        for gh_file in gh_commit.files:
            if gh_file.filename.startswith("vendor/"):
                vendor_files += 1
            else:
                print(f"    {gh_file.filename}")
        if vendor_files:
            print(f"    vendor/...  ({vendor_files} files not listed)")
        print("  --->")


if __name__ == "__main__":
    try:
        main()
    except github.GithubException as ex:
        print(f"Github API error {ex.status}: {ex.data['message']}")
