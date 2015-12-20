# coding: utf-8

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Creative Commons Attribution 4.0 International License (CC BY 4.0)
# http://creativecommons.org/licenses/by/4.0/

readme_expected = [
    '## The Fiery Meter of AWSome\n',
    '* [user/foo](https://github.com/user/foo) - desc\n',
    '* [user/bar :fire:](https://github.com/user/bar) - desc\n',
    '* [user/baz :fire::fire:](https://github.com/user/baz) - desc\n',
    '* [user/qux :fire::fire::fire:](https://github.com/user/qux) - desc\n',
    '* [user/foobar :fire::fire::fire::fire:](https://github.com/user/foobar) - desc\n',
    '* [user/bazqux :fire::fire::fire::fire::fire:](https://github.com/user/bazqux) - desc\n',
    '* [user/exclude](https://github.com/donnemartin) - desc\n',
    '* [user/exclude](https://github.com/donnemartin/awesome-aws) - desc\n',
    '* [user/exclude](https://github.com/sindresorhus/awesome) - desc\n',
    '* [user/exclude](https://github.com/kilimchoi/engineering-blogs) - desc\n',
    '* [user/exclude](https://github.com/user/foo#)\n',
]
