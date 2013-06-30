# -*- coding: utf-8 -*-

PLUGIN_NAME = "PerlPod"
PLUGIN_VERSION = "0.1.0"
PLUGIN_GUI_NAME = "Perl POD"

import sublime


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class PerlPod(object):
    __metaclass__ = Singleton

    """
    Helper class for accessing plugin settings and logging.
    """

    LOG_LEVELS = {
        'error': 0,
        'warning': 1,
        'notice': 2,
        'info': 3,
        'debug': 4,
        'trace': 5,
    }

    def __init__(self, **kwargs):
        self.log_level = self.get_setting('log_level')

    # Simple logging.
    def log(self, level, *messages):
        level = self.LOG_LEVELS[level]
        if level <= self.get_log_level():
            print(PLUGIN_NAME + ': ' + (' '.join(messages)))

    # Return current log level.
    def get_log_level(self):
        return self.log_level

    def get_setting(self, name, default=None):
        """
        Returns a single setting loaded from .sublime-settings, optionally
        using a default value.

        :param name:
            Name of setting to retrieve, separated with dots, e.g.
            "renderers.cpan.enabled"

        :param default:
            Default value which will be returned, if either final setting
            or any intermediate settings are None.
        """

        s = sublime.load_settings('%s.sublime-settings' % (PLUGIN_NAME))
        keys = name.split('.')

        # First element handled via .get()
        s = s.get(keys.pop(0))
        while len(keys):
            key = keys.pop(0)
            if isinstance(s, dict) and key in s:
                s = s[key]
            else:
                s = default
                break

        return s
