# -*- coding: utf-8 -*-

__version__ = "0.1.0"

__author__ = "Tom Malkin"
__copyright__ = "Tom Malkin"
__license__ = "mit"

from sqema import Sqema
import sys
import logging


_logger = logging.getLogger(__name__)


def setup_logging(loglevel):
    """
    Set up basic logging.

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


__all__ = [
    "Sqema"
]
