"""The Tank Utility CLI."""

import argparse
import json
import os

from . import __version__
from . import auth
from . import device


def _get_parser():
    """Get a command line argument parser.

    :param list argv: A list of command line arguments.
    :rtype: :py:class:`argparse.ArgumentParser`

    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--username", "-u", help="Username", default=os.environ.get("TANK_UTILITY_USERNAME", ""))
    parser.add_argument("--password", "-p", help="Password", default=os.environ.get("TANK_UTILITY_PASSWORD", ""))
    parser.add_argument("--verbose", "-v", help="Print debugging information", action="store_true")
    parser.add_argument("--pretty", help="Pretty print data", action="store_true")
    return parser


def main():
    """CLI entry point."""
    args = _get_parser().parse_args()
    if args.verbose:
        import logging
        logging.getLogger("").setLevel(logging.DEBUG)
    data = device.get_data(args.username, args.password)
    if args.pretty:
        import pprint
        pprint.pprint(data)
    else:
        print(json.dumps(data))
