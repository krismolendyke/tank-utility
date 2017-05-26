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
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6"
    ],
    keywords="propane monitor",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.0",
        "urllib3[secure]"
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
            "mock",
            "responses",
            "tox"
        ],
    },
    package_data={},
    include_package_data=True,
    data_files=[],
    test_suite="tests",
    entry_points={"console_scripts": ["tank-utility = tank_utility.__main__:main"]}
)
