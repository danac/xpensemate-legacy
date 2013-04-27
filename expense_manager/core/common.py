#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import inspect

class Constants:
    MIN_YEAR = 2013
    INDENT = 4

class Log:

    logger = logging.getLogger(__name__)

    @classmethod
    def debug(cls, msg):
        cls.logger.debug(cls.format(msg))

    @classmethod
    def info(cls, msg):
        cls.logger.info(cls.format(msg))

    @staticmethod
    def format(msg):
        frame, filename, line_number, function_name, lines, index = inspect.getouterframes(inspect.currentframe())[1]
        line=lines[0]
        indentation_level=line.find(line.lstrip())
        return('{i} [{m}]'.format(i = '.' * (indentation_level-4), m = msg))
