from setuptools import setup as _setup, find_packages as _find_packages


DESCRIPTION = """\
AwesomeGram is a framework for quickly creating and maintaining projects based on the Aiogram library.
"""


LONG_DESCRIPTION = """\
**AwesomGram** is a framework for quickly creating and maintaining projects based on the Aiogram library.

Inspired by Django, we aimed to simplify common boilerplate code with automatic generation triggered by a single or
multiple commands. We focused on making it universal and scalable, like a modular builder where you use ready-made
building blocks to construct your project—while keeping it independent from requiring all blocks to function.
"""


_setup(
    # Base:
    name="AwesomeGram",
    version="0.1",

    # Credentials:
    url="https://github.com/DriveWaveTech",
    author="DriveWaveTech",

    # Descriptions:
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",

    # Packages:
    python_requires=">=3.12",
    packages=_find_packages(),
    install_requires=[
        # Base Modules:
        'python-dotenv>=1.1.0',
        'pydantic-settings>=2.9.1',
        'argcomplete>=3.6.2',

        # Parsing Modules:
        'PyYAML>=6.0.2',
        'Jinja2>=3.1.6',

        # Database Modules:
        'asyncpg>=0.30.0',
        'SQLAlchemy>=2.0.40',
        'alembic>=1.15.2',

        # Telegram Modules:
        'aiogram>=3.20.0'
    ],

    # Run:
    entry_points={
        'console_scripts': [
            'AwesomeGram=awesomegram:main',
        ],
    },

    # Other:
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
