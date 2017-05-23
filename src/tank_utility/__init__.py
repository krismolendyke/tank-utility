"""A smart propane monitor."""

import logging
import os
from tempfile import gettempdir

from pkg_resources import resource_string

__version__ = resource_string(__name__, "VERSION").decode()

logging.getLogger(__name__).addHandler(logging.NullHandler())
