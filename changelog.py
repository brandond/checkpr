#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import click
import github
import os.path
from yaml import load, SafeLoader
from github import Github


@click.command()
@click.argument('repo')
@click.argument('base')
@click.argument('head')
@click.option('--token', help='Github auth token', envvar='GITHUB_TOKEN', required=True)
@click.option('--list-files', help='List changed files', is_flag=True)
def main(repo, base, head, token, list_files):
    gh = Github(token)
    gh_repo = gh.get_repo(repo)

    text = ''
    seen_prs = set()
    changelog = list()
    compare = gh_repo.compare(base, head)
    changelog.append(f"<!-- {compare.html_url} -->\n")
    for gh_commit in compare.commits:
        if len(gh_commit.parents) > 1:
            print("!", file=sys.stderr, end="", flush=True)
            continue

        for gh_pull in gh_commit.get_pulls():
            if gh_pull.number in seen_prs:
                print(",", file=sys.stderr, end="", flush=True)
                continue

            if text:
                changelog.append(text)
            seen_prs.add(gh_pull.number)
            title = gh_pull.title.capitalize()
            search = re.search(r'```release-note\s*(.+)\s*```', gh_pull.body or '')
            if search:
                release_note = search.group(1).strip()
                if release_note.lower() == 'none':
                    print("-", file=sys.stderr, end="", flush=True)
                    text = f"<!-- {title} ([#{gh_pull.number}]({gh_pull.html_url})) -->\n"
                    continue
                elif release_note:
                    title = release_note
            title = re.sub(r'^\[.*\] ?', r'', title).capitalize()
            text = f"* {title} ([#{gh_pull.number}]({gh_pull.html_url}))\n"
            print(".", file=sys.stderr, end="", flush=True)

        if list_files:
            text += "  <!--\n"
            text += f"  {gh_commit.commit.message.splitlines()[0]}\n"
            vendor_files = 0
            for gh_file in gh_commit.files:
                if gh_file.filename.startswith("vendor/"):
                    vendor_files += 1
                else:
                    text += f"    {gh_file.filename}\n"
            if vendor_files:
                text += f"    vendor/...  ({vendor_files} files not listed)\n"
            text += "  -->\n"

    if text:
        changelog.append(text)

    print("\n\n", file=sys.stderr, end="", flush=True)

    for text in reversed(changelog):  #sorted(changelog, key=lambda t: t.splitlines()[0].lower()):
        print(text, end="")


def load_config():
    hosts = os.path.expanduser("~/.config/gh/hosts.yml")
    if os.path.exists(hosts):
        hosts = load(open(hosts), Loader=SafeLoader)
        os.environ['GITHUB_TOKEN'] = hosts.get("github.com", {}).get("oauth_token", "")


if __name__ == "__main__":
    try:
        load_config()
        main()
    except github.GithubException as ex:
        print(f"Github API error {ex.status}: {ex.data['message']}")
