# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Creative Commons Attribution 4.0 International License (CC BY 4.0)
# http://creativecommons.org/licenses/by/4.0/

from githubcli.lib.github3 import null


class MockRepo(object):

    def __init__(self, name, stargazers_count):
        self.name = name
        self.stargazers_count = stargazers_count


class MockGitHubApi(object):

    def __init__(self, repos):
        self.repos = repos
        self.ratelimit_remaining = 9000

    def repository(self, _, repo_name):
        for repo in self.repos:
            if repo.name == repo_name:
                return repo
        return null.NullObject()


class MockGitHub(object):

    def __init__(self, repos):
        self.api = MockGitHubApi(repos)
