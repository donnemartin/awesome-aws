# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Creative Commons Attribution 4.0 International License (CC BY 4.0)
# http://creativecommons.org/licenses/by/4.0/

import pip
import pexpect
import unittest


class CliTest(unittest.TestCase):

    def test_run_cli(self):
        self.cli = None
        self.step_cli_installed()
        self.step_run_cli()
        self.step_see_prompt()
        self.step_send_ctrld()

    def step_cli_installed(self):
        """
        Make sure haxor is in installed packages.
        """
        dists = set([di.key for di in pip.get_installed_distributions()])
        assert 'haxor' in dists

    def step_run_cli(self):
        """
        Run the process using pexpect.
        """
        self.cli = pexpect.spawnu('haxor')

    def step_see_prompt(self):
        """
        Expect to see prompt.
        """
        self.cli.expect('haxor> ')

    def step_send_ctrld(self):
        """
        Send Ctrl + D to exit.
        """
        self.cli.sendcontrol('d')
        self.cli.expect(pexpect.EOF)
