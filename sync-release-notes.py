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
@click.argument('notes-file')
@click.option('--token', help='Github auth token', envvar='GITHUB_TOKEN', required=True)
def main(notes_file, token):
    notes = list(open(notes_file))
    tag = notes[0].split(' ')[1]
    if 'rke2' in tag:
        repo = 'rancher/rke2'
    else:
        repo = 'k3s-io/k3s'

    print(f"Updating release notes for {tag} in {repo}")

    gh = Github(token)
    gh_repo = gh.get_repo(repo)
    gh_release = gh_repo.get_release(tag)
    gh_release.update_release(name=tag, message="".join(notes))
    print(f"Notes updated for {gh_release.html_url}")


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
