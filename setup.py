"""setuptools entry point."""

from os import path
from setuptools import find_packages, setup
import codecs

HERE = path.abspath(path.dirname(__file__))

with codecs.open(path.join(HERE, "README.rst"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

with codecs.open(path.join(HERE, "src", "tank_utility", "VERSION")) as version_file:
    VERSION = version_file.read().strip()

setup(
    name="tank_utility",
    version=VERSION,
    description="A smart propane tank monitor.",
    long_description=LONG_DESCRIPTION,
    author="Kris Molendyke",
    author_email="kris@k20e.com",
    url="https://git.io/k20e",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    project_urls={
        "Source": "https://github.com/krismolendyke/tank-utility",
        "Bug Tracker": "https://github.com/krismolendyke/tank-utility/issues",
    },
    keywords="propane monitor",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.0",
        "urllib3"
    ],
    extras_require={
        "dev": [
            "bumpversion",
            "pylint",
            "pre-commit",
            "yapf"
        ],
        "test": [
            "coverage",
            "responses",
            "tox"
        ],
    },
    package_data={"tank_utility": ["VERSION"]},
    include_package_data=True,
    data_files=[],
    entry_points={"console_scripts": ["tank-utility = tank_utility.__main__:main"]}
)
