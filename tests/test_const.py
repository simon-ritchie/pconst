"""
The test module of const.py.
"""

from __future__ import print_function
import sys
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

    def test__is_settable_const_name(self):
        from pconst import const
        result_bool = const._is_settable_const_name(
            const_name='ConstantError')
        assert_false(result_bool)

        result_bool = const._is_settable_const_name(
            const_name='apple')
        assert_true(result_bool)
