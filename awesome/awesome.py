# coding: utf-8

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Creative Commons Attribution 4.0 International License (CC BY 4.0)
# http://creativecommons.org/licenses/by/4.0/

import re

import click
from githubcli.lib.github3 import null

from awesome.lib.github import GitHub


class Awesome(object):
    """Awesomeness.

    :type github: :class:`awesome.lib.GitHub`
    :param github: Provides integration with the GitHub API.

    :type output: list
    :param output: The updated README content.

    :type repos_broken: list
    :param repos_broken: Dead repos found during parsing.

    :type repos_exclude_score: list
    :param repos_exclude_score: Repos to exclude in calculating the
        Fiery Meter of AWSome score.

    """

    def __init__(self, github=None):
        self.github = github if github else GitHub()
        self.output = []
        self.repos_broken = []
        self.repos_exclude_score = [
            'https://github.com/donnemartin',
            'https://github.com/donnemartin/awesome-aws',
            'https://github.com/sindresorhus/awesome',
            'https://github.com/kilimchoi/engineering-blogs',
            'https://github.com/aws/aws-sdk-go/wiki',
            '#',
        ]

    def extract_repo_params(self, url):
        """Extracts the user login and repo name from a repo url.

        Expects the url to be valid of the form:
        https://github.com/user/repo/...

        :type regex_match: :class:`sre.SRE_Match`
        :param regex_match:
        """
        tokens = url.split('/')
        POS_USER_ID = 3
        POS_REPO_NAME = 4
        return tokens[POS_USER_ID], tokens[POS_REPO_NAME]

    def print_repos_broken(self):
        """Prints out any broken repos."""
        if self.repos_broken:
            click.secho('Broken repos:', fg='red')
            for repo in self.repos_broken:
                click.secho('  ' + repo, fg='red')

    def process_line(self, line):
        """Processes each line in the README.

        :type line: str
        :param line: The current line in the README.
        """
        match = re.search(r'(https://github.com/[^)]*)', line)
        # If we're not processing a repo, just output the line
        if match is None:
            self.output.append(line)
            return
        # If the repo is in the score exclude list, just output the line
        if any(substr in match.group(0) for substr in self.repos_exclude_score):
            self.output.append(line)
            return
        user_login, repo_name = self.extract_repo_params(match.group(0))
        repo = self.github.api.repository(user_login, repo_name)
        # Tag any broken repos
        if type(repo) is null.NullObject:
            self.repos_broken.append(match.group(0))
            return
        line = self.update_repo_score(repo, line)
        self.output.append(line)

    def rock_it(self, readme_path, result_path=None):
        """Processes the README.

        :type readme_path: str
        :param readme_path: The README file path.

        :type result_path: str
        :param result_path: The file path of where to output the results.
        """
        with open(readme_path, 'r') as f:
            for line in f:
                line = line.strip('\n')
                self.process_line(line)
        if result_path is None:
            result_path = readme_path
        self.write_output(result_path)
        self.print_repos_broken()
        click.secho('Rate limit: ' + str(self.github.api.ratelimit_remaining),
                    fg='blue')
        click.secho('Updated ' + result_path, fg='blue')

    def score_repo(self, stars, cached_score):
        """Assigns the Fiery Meter of AWSome score.

        :type stars: int
        :param stars: The number of repo stars.

        :type cached_score: int
        :param cached_score: The previouslya assigned score.
        """
        score = cached_score
        if stars < 100:
            score = 0 if score != 0 else cached_score
        elif stars < 200:
            score = 1 if score != 1 else cached_score
        elif stars < 500:
            score = 2 if score != 2 else cached_score
        elif stars < 1000:
            score = 3 if score != 3 else cached_score
        elif stars < 2000:
            score = 4 if score != 4 else cached_score
        else:
            score = 5 if score != 5 else cached_score
        return score

    def update_repo_score(self, repo, line):
        """Updates the repo's markdown, given its new score.

        :type repo: :class:`github3.repos.repo.Repository`
        :param repo: Contains repo information.

        :type line: str
        :param line: The current line of the README.
        """
        stars = repo.stargazers_count
        cached_score = line.count(':fire:')
        score = self.score_repo(stars, cached_score)
        if score != cached_score:
            prefix = ''
            if cached_score == 0:
                prefix = ' '
            cached_fires = ':fire:' * cached_score
            fires = ':fire:' * score
            line = line.replace(cached_fires + ']', prefix + fires + ']')
        return line

    def write_output(self, result_path):
        """Writes the results to the result_path.

        :type result_path: str
        :param result_path: The file path specifying where to write the output.
        """
        with open(result_path, 'w') as f:
            for output in self.output:
                f.write(output + '\n')
