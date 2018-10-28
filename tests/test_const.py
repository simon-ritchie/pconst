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


def assert_class_constructor_will_raise_error(
        target_class, error_class, args):
    """
    Check the specified class constructor will raise exception.

    Parameters
    ----------
    target_class : class
        The class that will be checked.
    error_class : class
        The expected error class.
    args : list
        The arguments that will be passed to constructor.

    Raises
    ------
    AssertionError
        If specified error not raised.
    """
    try:
        _ = target_class(*args)
    except error_class:
        return
    err_msg = 'Specified error not raised on constructor.'
    err_msg += '\ntarget class: %s' % target_class
    err_msg += '\n error class: %s' % error_class


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

        const.d = {'apple': 100}
        assert_true(isinstance(const.d, const.ConstDict))
        assert_equal(const.d['apple'], 100)

        const.e = ['100']
        assert_true(isinstance(const.e, const.ConstList))
        assert_equal(const.e[0], '100')

    def test___delattr__(self):
        try:
            del const.a
        except const.ConstantError:
            return
        err_msg = 'Not raised when constant deleted.'
        raise AssertionError(err_msg)

    def test___getattr__(self):
        const.c = 100
        c = const.c

        try:
            d = const.d
        except const.ConstantError:
            return
        raise AssertionError('ConstantError is not raised.')


class TestConstDict(TestCase):

    def test___init__(self):

        args = [100]
        assert_class_constructor_will_raise_error(
            target_class=const.ConstDict,
            error_class=ValueError,
            args=args)

        const_dict = const.ConstDict(dict_val={'apple': 100})
        assert_false(const_dict._is_constructor)
        assert_equal(
            const_dict._original_dict,
            {'apple': 100})
        assert_equal(const_dict['apple'], 100)

    def test___setitem__(self):
        const_dict =  const.ConstDict(dict_val={'a': 100})
        try:
            const_dict['a'] = 200
        except const.ConstantError:
            return
        err_msg = 'Update of dict value is not raise error.'
        raise AssertionError(err_msg)

    def test___repr__(self):
        const_dict = const.ConstDict(dict_val={'a': 200})
        output_str = const_dict.__repr__()
        assert_equal(output_str, "{'a': 200}")

    def test___delitem__(self):
        const_dict = const.ConstDict(dict_val={'a': 300})
        try:
            del const_dict['a']
        except const.ConstantError:
            return
        err_msg = 'Error not raised when delete dict value.'
        raise AssertionError(err_msg)

    def test_clear(self):
        const_dict = const.ConstDict(dict_val={'a': 100})
        try:
            const_dict.clear()
        except const.ConstantError:
            return
        err_msg = 'Error not raised when clear dict values.'
        raise AssertionError(err_msg)

    def test_update(self):
        const_dict = const.ConstDict(dict_val={'a': 100})
        try:
            const_dict.update({'b': 200})
        except const.ConstantError:
            return
        err_msg = 'Error nor raised when update dict values.'
        raise AssertionError(err_msg)

    def test_pop(self):
        const_dict = const.ConstDict(dict_val={'a': 100})
        try:
            _ = const_dict.pop('a')
        except const.ConstantError:
            return
        err_msg = 'Error not raised when pop method is called.'
        raise AssertionError(err_msg)

    def test__replace_dict_val_to_const(self):
        dict_val = {'a': {'b': 100}, 'c': 200, 'd': [100]}
        const_dict = const.ConstDict(dict_val=dict_val)
        assert_true(isinstance(const_dict['a'], const.ConstDict))
        assert_equal(const_dict['a']['b'], 100)
        assert_equal(const_dict['c'], 200)
        assert_true(isinstance(const_dict['d'], const.ConstList))
        assert_equal(const_dict['d'][0], 100)


class TestConstList(TestCase):

    def test___init__(self):
        args = [100]
        assert_class_constructor_will_raise_error(
            target_class=const.ConstList,
            error_class=ValueError,
            args=args)

        const_list = const.ConstList(list_value=[100, 200])
        assert_equal(
            const_list._original_list,
            [100, 200])
        assert_equal(const_list[0], 100)
        assert_equal(const_list[1], 200)
        assert_equal(len(const_list), 2)

        const_list = const.ConstList(
            list_value=[
                {'a': 100, 'b': {'c': 200}},
                [300, 400],
                500])
        assert_true(
            isinstance(const_list[0], const.ConstDict))
        assert_equal(const_list[0]['a'], 100)
        assert_true(
            isinstance(const_list[0]['b'], const.ConstDict))
        assert_equal(const_list[0]['b']['c'], 200)
        assert_true(
            isinstance(const_list[1], const.ConstList))
        assert_equal(const_list[1][0], 300)
        assert_equal(const_list[1][1], 400)
        assert_equal(const_list[2], 500)

    def test_append(self):
        const_list = const.ConstList(list_value=[100])
        try:
            const_list.append(200)
        except const.ConstantError:
            return
        err_msg = 'Error not raised when append method is called.'
        raise AssertionError(err_msg)
