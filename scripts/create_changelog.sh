#!/usr/bin/env bash

gitchangelog > CHANGELOG_DRAFT
pandoc --from=markdown --to=rst --output=CHANGELOG.rst CHANGELOG.md
