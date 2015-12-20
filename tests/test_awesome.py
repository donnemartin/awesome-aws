# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Creative Commons Attribution 4.0 International License (CC BY 4.0)
# http://creativecommons.org/licenses/by/4.0/

import mock
import os
import unittest

from awesome.awesome import Awesome
from tests.data.readme_expected import readme_expected
from tests.mock_github import MockGitHub, MockRepo


class AwesomeTest(unittest.TestCase):

    def setUp(self):
        self.repos = self.create_repos()
        self.github = MockGitHub(self.repos)
        self.awesome = Awesome(self.github)

    def create_repos(self):
        return [
            MockRepo('foo', 10),
            MockRepo('bar', 150),
            MockRepo('baz', 270),
            MockRepo('qux', 550),
            MockRepo('foobar', 1200),
            MockRepo('bazqux', 9000),
            MockRepo('awesome-aws', 9000),
        ]

    @mock.patch('awesome.awesome.click')
    def test_rock_it(self, mock_click):
        README = os.path.join(os.path.dirname(__file__),
                              'data/README.md')
        README_RESULT = os.path.join(os.path.dirname(__file__),
                                     'data/README_RESULT.md')
        self.awesome.rock_it(README, README_RESULT)
        result = []
        with open(README_RESULT, 'r') as f:
            for line in f:
                result.append(line)
        assert result == readme_expected
        assert mock.call.secho('Broken repos:', fg='red') \
            in mock_click.mock_calls
        assert mock.call.secho('  https://github.com/user/broken', fg='red') \
            in mock_click.mock_calls
        assert mock.call.secho('Rate limit: 9000', fg='blue') \
            in mock_click.mock_calls
        assert mock.call.secho('Updated ' + README_RESULT, fg='blue') \
            in mock_click.mock_calls
