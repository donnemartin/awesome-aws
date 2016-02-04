from awesome.__init__ import __version__
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    description='A curated list of awesome Amazon Web Services (AWS) libraries, open source repos, guides, blogs, and other resources.',
    author='Donne Martin',
    url='https://github.com/donnemartin/awesome-aws',
    download_url='https://github.com/donnemartin/awesome-aws',
    author_email='donne.martin@gmail.com',
    version=__version__,
    license='Creative Commons Attribution 4.0',
    install_requires=[
        'click>=5.1',
        'githubcli>=0.1.0',
        'colorama>=0.3.3',
    ],
    extras_require={
        'testing': [
            'mock>=1.0.1',
            'tox>=1.9.2'
        ],
    },
    entry_points={
        'console_scripts': 'awesome = awesome.awesome_cli:AwesomeCli.cli'
    },
    packages=find_packages(),
    scripts=[],
    name='awesome-aws',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
