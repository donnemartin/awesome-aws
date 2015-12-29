# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Creative Commons Attribution 4.0 International License (CC BY 4.0)
# http://creativecommons.org/licenses/by/4.0/

import unittest

from click.testing import CliRunner

from awesome.awesome_cli import AwesomeCli


class AwesomeCliTest(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.awesome_cli = AwesomeCli()

    def test_cli(self):
        result = self.runner.invoke(self.awesome_cli.cli)
        assert result.exit_code == 0
