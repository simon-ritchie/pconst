# coding: UTF-8

"""
This module provides const-like function on Python.
"""

from copy import deepcopy

NOT_SETTABLE_CONST_NAMES = [
    'ConstantError',
    'ConstDict',
    'ConstList',
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


class ConstDict(dict):
    """
    The class that makes dict value not editable.

    Parameters
    ----------
    dict_val : dict
        The dict value that will be set unchangeable recursively.

    Attributes
    ----------
    _original_dict : dict
        Original dict that passed to argument.
    _is_constructor : bool
        If current timing is executing constructor,
        this bool will set to True.

    Raises
    ------
    ValueError
        If the passed value type is not dict.
    """
    _is_constructor = False

    def __init__(self, dict_val):
        self.__dict__['_is_constructor'] = True
        if not isinstance(dict_val, dict):
            err_msg = 'The type of passed value is not dict.'
            raise ValueError(err_msg)
        self._original_dict = deepcopy(dict_val)
        dict_val = self._replace_dict_val_to_const(dict_val=dict_val)
        super(ConstDict, self).__init__(dict_val)

        self._is_constructor = False

    def _replace_dict_val_to_const(self, dict_val):
        """
        Replace values in dict to ConstDict or ConstList.

        Parameters
        ----------
        dict_val : dict
            All values that this dict has will replace to ConstDict
            or CostList if values are dict or list.

        Returns
        -------
        dict_val : dict
            Replaced dict.
        """
        for key, value in dict_val.items():
            if (not isinstance(value, dict)
                    and not isinstance(value, list)):
                continue

            if isinstance(value, dict):
                dict_val[key] = ConstDict(dict_val=value)
                continue

            if isinstance(value, list):
                dict_val[key] = ConstList(list_value=value)
                continue
        return dict_val

    def __setitem__(self, key, item):
        """
        This method will always raise error except during executing
        constructor in order to prevent the dict value update.
        e.g., const.yourdict['a'] = 100 will raise ConstantError.

        Parameters
        ----------
        key : str
            Dict key.
        item : *
            Dict Value

        Raises
        ------
        ConstantError
            This method will always raise error except during
            executing constructor.
        """
        if not self._is_constructor:
            err_msg = "Update dict value is not allowed."
            raise ConstantError(err_msg)
        self.__dict__[key] = item

    def __repr__(self):
        """
        This method will be called when ConstDict object will
        pass to print function. Output will skip class attributes,
        like _is_constructor.

        Returns
        -------
        output_str : str
            The text that display to console or output cell.

        Examples
        --------
        >>> from pconst import const
        >>> const_dict = const.ConstDict({'a': 100})
        >>> print(const_dict)
        {'a': 100}
        """
        return str(self._original_dict)

    def __delitem__(self, key):
        """
        This method will always raise error to disallow dict
        value deletion.

        Parameters
        ----------
        key : str
            Key of the dict.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'Deletion of dict value is not allowed.'
        raise ConstantError(err_msg)

    def clear(self):
        """
        This method will always raise error to disallow dict
        value deletion.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'To reset dict values is not allowed.'
        raise ConstantError(err_msg)

    def update(self, *args, **kwargs):
        """
        This method will always raise error to disallow dict
        value update.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'To update dict values is not allowed.'
        raise ConstantError(err_msg)

    def pop(self, *args):
        """
        This method will always raise error to disallow dict
        value update.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'pop method is disallowed to not update dict value.'
        raise ConstantError(err_msg)


class ConstList(object):
    """
    The class that makes list value not editable.

    Parameters
    ----------
    list_value : list
        The list value that will be set unchangeable recursively.

    Attributes
    ----------
    _original_list : list
        Original list that passed to argument.

    Raises
    ------
    ValueError
        If the passed value is not list.
    """

    def __init__(self, list_value):
        super(ConstList, self).__init__()
        if not isinstance(list_value, list):
            err_msg = 'The type of passed value is not list.'
            raise ValueError(err_msg)
        self._original_list = list_value


class Const(object):
    """
    The class that provides const-like function on Python.
    This will set as module, so you can skip initialization.

    Attributes
    ----------
    ConstantError : class
        Error class that will use when invalid constant
        manipulation is done.
    ConstDict : class
        The class that makes dict value not editable.
    ConstList : class
        The class that makes list value not editable.
    _is_constructor : bool
        If current timing is executing constructor,
        this bool will set to True.

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
    ConstantError: Constant value of "a" is not editable.

    Notes
    -----
    Following names are used by this class, so you can't set the
    same constant names (e.g., const.ConstantError = 'apple').
    - 'ConstantError'
    - 'ConstDict'
    - 'ConstList'
    - '_has_key'
    - '_is_settable_const_name'
    - '_is_constructor'
    """

    _is_constructor = True

    def __init__(self):
        super(Const, self).__init__()
        self.ConstantError = ConstantError
        self.ConstDict = ConstDict
        self.ConstList = ConstList
        self._is_constructor = False

    def _has_key(self, name):
        """
        Return True if this class has the attribute of specified name.

        Parameters
        ----------
        name : str
            Attribute name.

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
            Constant name.

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
        Set value to class attribute. When property will updated,
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
        e.g., del const.a will raise ConstantError.

        Raises
        ------
        ConstantError
            When attempt to delete attribute, error will
            always be raised.

        Parameters
        ----------
        name : str
            Constant name.
        """
        err_msg = 'Constant values are not deletable.'
        raise ConstantError(err_msg)

    def __getattr__(self, name):
        """
        Get the attribute value of specified constant name. When
        accessed const property, this method will be called
        (e.g., a = const.a).

        Parameters
        ----------
        name : str
            Constant name.

        Returns
        -------
        Constant value.

        Raises
        ------
        ConstantError
            If the specified constant is not defined.
        """
        if not self._has_key(name):
            err_msg = 'Constant value of "%s" is not defined.' % name
            raise ConstantError(err_msg)
