#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Creative Commons Attribution 4.0 International License (CC BY 4.0)
# http://creativecommons.org/licenses/by/4.0/

import unittest

from test_awesome import AwesomeTest  # NOQA
from test_awesome_cli import AwesomeCliTest  # NOQA
try:
    from test_cli import CliTest  # NOQA
except:
    # pexpect import fails on Windows
    pass


if __name__ == '__main__':
    unittest.main()
