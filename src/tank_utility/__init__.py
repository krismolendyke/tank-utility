"""A smart propane monitor."""

from importlib.resources import files
import logging

try:
    __version__ = files(__package__).joinpath("VERSION").read_text().strip()
except Exception:  # pylint: disable=broad-except
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("tank-utility")
    except PackageNotFoundError:
        __version__ = "unknown"

logging.getLogger(__name__).addHandler(logging.NullHandler())

