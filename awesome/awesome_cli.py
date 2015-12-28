#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Creative Commons Attribution 4.0 International License (CC BY 4.0)
# http://creativecommons.org/licenses/by/4.0/

import click

from awesome.awesome import Awesome


pass_awesome = click.make_pass_decorator(Awesome)


class AwesomeCli(object):
    """Awesomeness in CLI form."""

    @click.group()
    @click.pass_context
    def cli(ctx):
        """Main entry point for AwesomeCli.

        :type ctx: :class:`click.core.Context`
        :param ctx: Stores an instance of Awesome used to update the README.
        """
        # Create a GitHub object and remember it as as the context object.
        # From this point onwards other commands can refer to it by using the
        # @pass_github decorator.
        ctx.obj = Awesome()

    @cli.command()
    @click.argument('readme_path')
    @pass_awesome
    def rock_it(awesome, readme_path):
        """Updates the README.

        :type awesome: :class:`Awesome`
        :param awesome: Stores an instance of Awesome used to update the README.

        :type readme_path: str
        :param readme_path: The README path
        """
        awesome.rock_it(readme_path)
