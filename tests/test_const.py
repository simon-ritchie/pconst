"""
The test module of const.py.
"""

from __future__ import print_function
import sys
try:
    from importlib import reload
except Exception:
    pass
sys.path.append('../')

from unittest import TestCase
from nose.tools import assert_equal, assert_true, assert_false, \
    assert_raises


class TestConst(TestCase):

    def test__has_key(self):
        from pconst import const
        result_bool = const._has_key('a')
        assert_false(result_bool)

        const.a = 'a'
        result_bool = const._has_key('a')
        assert_true(result_bool)


