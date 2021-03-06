# -*- coding: utf-8 -*-
import re

commands = {}

commandregex = re.compile("(?s)^!(?P<command>\w+)\s*(?P<args>.*)?")


def command(cmd):
    """
    When you write a new command, add this decorator to it, so it's gets registered
    """

    def wrapper(wrapped):
        commands[cmd] = wrapped

        return wrapped

    return wrapper
