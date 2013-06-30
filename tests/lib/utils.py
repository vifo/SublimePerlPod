# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import sys
from nose.plugins.skip import SkipTest


def is_windows():
    return sys.platform.startswith('win32')


class TestCase(object):

    """
    Test case.
    """

    skip_reason = None

    def skip_if_have_reason(self):
        if self.skip_reason:
            raise SkipTest(self.skip_reason)


class TestCaseWindows(TestCase):

    """
    Test case, which will be run on Windows platform only.
    """

    def setUp(self):
        if not is_windows():
            self.skip_reason = "Not running on Windows"


class TestCaseNonWindows(TestCase):

    """
    Test case, which will be run on Non-Windows platforms only.
    """

    def setUp(self):
        if is_windows():
            self.skip_reason = "Running on Windows"
