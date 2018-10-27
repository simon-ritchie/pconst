# coding: UTF-8

"""
This module provides const-like function on Python.
"""

import sys

NOT_SETTABLE_CONST_NAMES = [
    'ConstantError',
]


class ConstantError(Exception):
    """
    Error class that will use when invalid constant manipulation is done.

    Parameters
    ----------
    err_msg : str
        error message that will display on console.
    """

    def __init__(self, err_msg):
        super(ConstantError, self).__init__(err_msg)


class const(object):
    """
    The class that provides const-like function on Python.
    This will set as module, so you can skip initialization.

    Attributes
    ----------
    ConstantError : class
        Error class that will use when invalid constant
        manipulation is done.

    Examples
    --------
    >>> from pconst import const
    >>> const.a = 'apple'
    >>> const.a
    'apple'

    # Following code will raise ConstantError.
    >>> const.a = 'apple'
    >>> const.a = 'orange'
    ...
    ConstantError: constant value of "a" is not editable.

    Notes
    -----
    Following names are used by this class, so you can't set
    same constant names (e.g., const.ConstantError = 'apple').
    - 'ConstantError'
    - _has_key
    - _is_settable_const_name
    """

    def __init__(self):
        super(const, self).__init__()
        self.ConstantError = ConstantError

    def _has_key(self, name):
        return name in self.__dict__

    def __setattr__(self, name, value):
        if self._has_key(name):
            err_msg = 'constant value of "%s" is not editable.' % name
            raise ConstantError(err_msg)
        self.__dict__[name] = value

    def __delattr__(self, name):
        err_msg = 'constant values are not deletable.'
        raise ConstantError(err_msg)

    def __getattr__(self, name):
        if not self._has_key(name):
            err_msg = 'constant value of "%s" is not defined.' % name
            raise ConstantError(err_msg)


sys.modules[__name__] = const()
