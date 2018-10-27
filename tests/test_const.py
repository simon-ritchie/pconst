"""
The test module of const.py.
"""

from __future__ import print_function
from importlib import reload
import sys
sys.path.append('../')

from unittest import TestCase
from nose.tools import assert_equal, assert_true, assert_false, \
    assert_raises

from pconst import const


def assert_raises_if_const_added(const_name, const_value):
    """
    Check the ConstantError will raise if arguments condition
    will passed.

    Parameters
    ----------
    const_name : str
        Specified target constant name.
    const_value : *
        Specified target constant value.

    Raises
    ------
    AssertionError
        If the ConstantError will not raised.
    """
    try:
        setattr(const, const_name, const_value)
    except const.ConstantError:
        return
    err_msg = 'The ConstantError not raised.'
    err_msg += '\nconst name: %s' % const_name
    raise AssertionError(err_msg)


class TestConst(TestCase):

    def test__has_key(self):
        result_bool = const._has_key('a')
        assert_false(result_bool)

        const.a = 'a'
        result_bool = const._has_key('a')
        assert_true(result_bool)

    def test__is_settable_const_name(self):
        result_bool = const._is_settable_const_name(
            const_name='ConstantError')
        assert_false(result_bool)

        result_bool = const._is_settable_const_name(
            const_name='apple')
        assert_true(result_bool)

    def test___setattr__(self):
        const.b = 'apple'
        assert_equal(const.b, 'apple')

        assert_raises_if_const_added(
            const_name='b', const_value='orange')

        assert_raises_if_const_added(
            const_name='ConstantError', const_value='orange')

    def test___delattr__(self):
        try:
            del const.a
        except const.ConstantError:
            return
        err_msg = 'Not raised when constant deleted.'
        raise AssertionError(err_msg)
