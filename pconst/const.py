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
        This method will be called when ConstDict object will be
        passed to print function. Output will skip class attributes,
        like _is_constructor attribute.

        Returns
        -------
        output_str : str
            The text that display to console or output cell.

        Examples
        --------
        >>> from pconst import const
        >>> const_dict = const.ConstDict({'a': 100})
        >>> print(const_dict)
        [Out] {'a': 100}
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


class ConstList(list):
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
    _is_constructor : bool
        If current timing is executing constructor,
        this bool will set to True.

    Raises
    ------
    ValueError
        If the passed value is not list.
    """

    _is_constructor = False

    def __init__(self, list_value):
        self.__dict__['_is_constructor'] = True
        if not isinstance(list_value, list):
            err_msg = 'The type of passed value is not list.'
            raise ValueError(err_msg)
        self._original_list = deepcopy(list_value)
        for i, value in enumerate(list_value):
            if isinstance(value, dict):
                list_value[i] = ConstDict(dict_val=value)
                continue
            if isinstance(value, list):
                list_value[i] = ConstList(list_value=value)
                continue
        super(ConstList, self).__init__(list_value)
        self._is_constructor = False

    def append(self, object):
        """
        This method will always raise error to disallow list
        value update.

        Parameters
        ----------
        object : *
            Object that append to list.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'append method is disallowed to not update list value.'
        raise ConstantError(err_msg)

    def clear(self):
        """
        This method will always raise error to disallow list
        value update.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'clear method is disallowed to not update list value.'
        raise ConstantError(err_msg)

    def extend(self, iterable):
        """
        This method will always raise error to disallow list
        value update.

        Parameters
        ----------
        iterable : array-like
            The iterable object that will be appended to list.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'extend method is disallowed to not update list value.'
        raise ConstantError(err_msg)

    def insert(self, index, object):
        """
        This method will always raise error to disallow list
        value update.

        Parameters
        ----------
        index : int
            Index position that object will be inserted.
        object : *
            The object that will be inserted.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'insert method is disallowed to not update list value.'
        raise ConstantError(err_msg)

    def pop(self, index):
        """
        This method will always raise error to disallow list
        value update.

        Parameters
        ----------
        index : int
            Index position that object will be taken out.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'pop method is disallowed to not update list value.'
        raise ConstantError(err_msg)

    def remove(self, value):
        """
        This method will always raise error to disallow list
        value update.

        Parameters
        ----------
        value : *
            The value that will be removed from list.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'remove method is disallowed to not update list value.'
        raise ConstantError(err_msg)

    def reverse(self):
        """
        This method will always raise error to disallow list
        value update.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'reverse method is disallowed to not update list value.'
        raise ConstantError(err_msg)

    def sort(key=None, reverse=False):
        """
        This method will always raise error to disallow list
        value update.

        Parameter
        ---------
        key : function or None, default None
            The function that will be applied to each elements before
            sorting.
        reverse : bool, default False
            If True, sorted result will be reversed order.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'sort method is disallowed to not update list value.'
        raise ConstantError(err_msg)

    def __delitem__(self, index):
        """
        This method will always raise error to disallow list
        value update.

        The same is true of writing del operator
        (e.g., del const_list[0]).

        Parameter
        ---------
        index : int
            The index that will be deleted.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = '__delitem__ method and del operator are disallowed to not update list value.'
        raise ConstantError(err_msg)

    def __reversed__(self):
        """
        This method will always raise error to disallow list
        value update.

        Raises
        ------
        ConstantError
            This method will always raise error.
        """
        err_msg = 'sort method is disallowed to not update list value.'
        raise ConstantError(err_msg)

    def __setitem__(self, index, value):
        """
        Update list value at specified index location.
        Except the timing of constructor method is executing,
        this method will raise error to disallow list value update
        (e.g., const_list.a[0] = 1 will raise error).

        Parameters
        ----------
        index : int
            The index location that update list value.
        value : *
            The value that apply to specified index.

        Raises
        ------
        ConstantError
            If the case that try to update list value except
            the timing of constructor method is executing.
        """
        if not self._is_constructor:
            err_msg = 'Constant list value is not allowed.'
            raise ConstantError(err_msg)
        self.__dict__[index] = value

    def __repr__(self):
        """
        This method will be called when ConstList object will be
        passed to print function. Output will skip class
        attributes, like _is_constructor attribute.

        Returns
        -------
        output_str : str
            The text that display to console or output cell.

        Examples
        --------
        >>> from pconst import const
        >>> const_list = const.ConstList(list_value=[100, 200])
        >>> print(const_list)
        [Out] [100, 200]
        """
        return str(self._original_list)


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
    [Out] 'apple'

    # Following code will raise ConstantError.
    >>> const.a = 'apple'
    >>> const.a = 'orange'
    [Out] ConstantError: Constant value of "a" is not editable.

    # Also can use dict or list.
    >>> const.fruit = {'apple': 100}
    >>> const.fruit['apple']
    [Out] 100

    # Following code will raise ConstantError.
    >>> const.fruit['apple'] = 200
    [Out] ConstantError: Update dict value is not allowed.

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
        if isinstance(value, dict):
            value = ConstDict(dict_val=value)
        if isinstance(value, list):
            value = ConstList(list_value=value)
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
