# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from nose.tools import assert_equal, assert_regexp_matches, assert_true, assert_false, assert_raises, assert_is_none
from lib.utils import TestCaseWindows, TestCaseNonWindows, TestCase


class TestPerlPodUtils(TestCase):

    pass


class TestPerlPodUtilsWindows(TestCaseWindows):

    pass


class TestPerlPodUtilsNonWindows(TestCaseNonWindows):

    pass
