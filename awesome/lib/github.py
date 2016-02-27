# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from getpass import getpass
import os
try:
    # Python 3
    import configparser
except ImportError:
    # Python 2
    import ConfigParser as configparser

import click
from githubcli.lib.github3 import authorize, login
from githubcli.lib.github3.exceptions import UnprocessableEntity


class GitHub(object):
    """Provides integration with the GitHub API.

    Attributes:
        * api: An instance of github3 to interact with the GitHub API.
        * CONFIG: A string representing the config file name.
        * CONFIG_SECTION: A string representing the main config file section.
        * CONFIG_USER_LOGIN: A string representing the user login config.
        * CONFIG_USER_PASS: A string representing the user pass config.
        * CONFIG_USER_TOKEN: A string representing the user token config.
        * CONFIG_URL: A string representing the jump to url config file name.
        * CONFIG_URL_SECTION: A string representing the jump to url config
            file section.
        * GITHUB_ISSUES: A string representing the GitHub issues url portion.
        * GITHUB_URL: A string representing the GitHub main url.
        * user_login: A string that represents the user's login in
            ~/.githubconfig
        * user_pass: A string that represents the user's pass in
            ~/.githubconfig
        * user_token: A string that represents the user's token in
            ~/.githubconfig
    """

    CONFIG = '.githubconfig'
    CONFIG_SECTION = 'github'
    CONFIG_USER_LOGIN = 'user_login'
    CONFIG_USER_PASS = 'user_pass'
    CONFIG_USER_TOKEN = 'user_token'
    CONFIG_URL = '.githubconfigurl'
    CONFIG_URL_SECTION = 'url'
    CONFIG_AVATAR = '.githubconfigavatar.png'
    GITHUB_ISSUES = 'issues/'
    GITHUB_URL = 'https://github.com/'

    def __init__(self):
        """Inits GitHub.

        Args:
            * None.

        Returns:
            None.
        """
        self.api = None
        self.user_login = None
        self.user_pass = None
        self.user_token = None
        self._login()

    def _github_config(self, config_file_name):
        """Attempts to find the github config file.

        Adapted from https://github.com/sigmavirus24/github-cli.

        Args:
            * config_file_name: A String that represents the config file name.

        Returns:
            A string that represents the github config file path.
        """
        home = os.path.abspath(os.environ.get('HOME', ''))
        config_file_path = os.path.join(home, config_file_name)
        return config_file_path

    def _login(self):
        """Logs into GitHub.

        Adapted from https://github.com/sigmavirus24/github-cli.

        TODO: Two factor authentication does not seem to be triggering the
            SMS code: https://github.com/sigmavirus24/github3.py/issues/387

        Args:
            * None.

        Returns:
            None.
        """
        # Get the full path to the configuration file
        config = self._github_config(self.CONFIG)
        parser = configparser.RawConfigParser()
        # Check to make sure the file exists and we are allowed to read it
        if os.path.isfile(config) and os.access(config, os.R_OK | os.W_OK):
            parser.readfp(open(config))
            self.user_login = parser.get(self.CONFIG_SECTION,
                                         self.CONFIG_USER_LOGIN)
            self.api = login(token=parser.get(self.CONFIG_SECTION,
                                              self.CONFIG_USER_TOKEN),
                             two_factor_callback=self._two_factor_code)
        else:
            # Either the file didn't exist or we didn't have the correct
            # permissions
            user_login = ''
            while not user_login:
                user_login = input('User Login: ')
            user_pass = ''
            while not user_pass:
                user_pass = getpass('Password: ')
            auth = None
            try:
                # Get an authorization for this
                auth = authorize(
                    user_login,
                    user_pass,
                    scopes=['user', 'repo', 'gist'],
                    note='githubcli',
                    note_url='https://github.com/donnemartin/github-cli'
                )
            except UnprocessableEntity:
                click.secho('Error creating token.\nVisit the following '
                            'page and verify you do not have an existing '
                            'token named "githubcli":\n'
                            'See https://github.com/settings/tokens\n'
                            'If a token already exists update your ' +
                            self.githubconfig + ' file with your user_token.',
                            fg='red')
            parser.add_section(self.CONFIG_SECTION)
            parser.set(self.CONFIG_SECTION, self.CONFIG_USER_LOGIN, user_login)
            parser.set(self.CONFIG_SECTION, self.CONFIG_USER_PASS, user_pass)
            parser.set(self.CONFIG_SECTION, self.CONFIG_USER_TOKEN, auth.token)
            self.api = login(token=auth.token,
                             two_factor_callback=self._two_factor_code)
            # Create the file if it doesn't exist. Otherwise completely blank
            # out what was there before. Kind of dangerous and destructive but
            # somewhat necessary
            parser.write(open(config, 'w+'))

    def _two_factor_code(self):
        """Callback if two factor authentication is requested.

        Args:
            * None.

        Returns:
            A string that represents the user input two factor
                authentication code.
        """
        code = ''
        while not code:
            code = input('Enter 2FA code: ')
        return code
