# coding: UTF-8

"""
This module provides const-like function on Python.
"""

import sys

NOT_SETTABLE_CONST_NAMES = [
    'ConstantError',
    '_has_key',
    '_is_settable_const_name',
    '_is_constructor',
]
ERR_MSG_NOT_SETTABLE_CONST_NAME = 'Specified constant name is not settable. Please set constant name except following list: %s' % NOT_SETTABLE_CONST_NAMES


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
    - _is_constructor
    """

    _is_constructor = True

    def __init__(self):
        super(const, self).__init__()
        self.ConstantError = ConstantError
        self._is_constructor = False

    def _has_key(self, name):
        """
        Return True if this class has the attribute of specified name.

        Parameters
        ----------
        name : str
            Target attribute name.

        Returns
        -------
        result : bool
            Return True if this class has the attribute of
            specified name.
        """
        return name in self.__dict__

    def _is_settable_const_name(self, const_name):
        """
        Return True if specified const_name is not in
        NOT_SETTABLE_CONST_NAMES list.

        Parameters
        ----------
        const_name : str
            Target constant name.

        Notes
        -----
        Only when constructor method, result will always be True.

        Returns
        -------
        result : bool
            Return True if specified const_name is not in
            NOT_SETTABLE_CONST_NAMES list.
            e.g., If const_name is 'ConstantError', then
            result will be False.
        """
        if self._is_constructor:
            return True
        is_in = const_name in NOT_SETTABLE_CONST_NAMES
        if is_in:
            return False
        return True

    def __setattr__(self, name, value):
        """
        Aet value to class attribute. When property will updated,
        this method will be called (e.g., const.a = 100).

        Parameters
        ----------
        name : str
            Constant name.
        value : *
            Constant value.

        Raises
        ------
        ConstantError
            - If the same constant name attibute already exists.
            - If the constant name is not acceptable because of
                used by class (e.g., name='ConstantError').
        """
        if self._has_key(name):
            err_msg = 'Constant value of "%s" is not editable.' % name
            raise ConstantError(err_msg)
        is_settable = self._is_settable_const_name(
            const_name=name)
        if not is_settable:
            raise ConstantError(ERR_MSG_NOT_SETTABLE_CONST_NAME)
        self.__dict__[name] = value

    def __delattr__(self, name):
        """
        This method will raise error in order to prevent the
        constants deletion.
        i.e., del const.a will raise ConstantError.

        Parameters
        ----------
        name : str
            Constant name.
        """
        err_msg = 'Constant values are not deletable.'
        raise ConstantError(err_msg)

    def __getattr__(self, name):
        if not self._has_key(name):
            err_msg = 'Constant value of "%s" is not defined.' % name
            raise ConstantError(err_msg)


sys.modules[__name__] = const()
