#!/usr/bin/env bash

# N. Set CHANGELOG as `README.md`
scripts/set_changelog_as_readme.sh
# O. Register package with PyPi
python setup.py register -r pypi
# P. Upload to PyPi
python setup.py sdist upload -r pypi
# Q. Upload Sphinx docs to PyPi
python setup.py upload_sphinx
# R. Restore `README.md`
scripts/set_changelog_as_readme_undo.sh
