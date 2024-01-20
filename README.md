# pconst

"pconst" library provide you const-like function on Python.

# Install

Install via pip is available.

```
$ pip install pconst
```

# How to use

You can set constants to const module's attribute.

```py
from pconst import const
const.APPLE_PRICE = 100
const.APPLE_NAME = 'apple'
print(const.APPLE_PRICE)
```

```
100
```

If try to update constant value, ConstantError will be raised.

```py
const.APPLE_PRICE = 200
```

```
Constant value of "APPLE_PRICE" is not editable.
```

del operator is also disallowed.

```py
del const.APPLE_NAME
```

```
ConstantError: Constant values are not deletable.
```

You can also set dict and list value to const module, and they will be not editable (if dict or list values contains dict or list, then will be applied recursively.).

```py
const.APPLE_DATA = {
    'prince': 100,
    'name': 'apple',
    'sales_list': [12300, 25000, 8200]}
print('price:', const.APPLE_DATA['price'])
print('name:', const.APPLE_DATA['name'])
print('sales_list:', const.APPLE_DATA['sales_list'])
```

```
price: 100
name: apple
sales_list: [12300, 25000, 8200]
```

```py
const.APPLE_DATA['price'] = 200
```

```
ConstantError: Update dict value is not allowed.
```

```py
const.APPLE_DATA['sales_list'][1] = 9800
```

```
ConstantError: Constant list value is not allowed.
```

The dict or list class method that will not change the values is be able to access (e.g., len(), keys()).

```py
print(len(const.APPLE_DATA['sales_list']))
```

```
3
```

```py
print(const.APPLE_DATA.keys())
```

```
dict_keys(['price', 'name', 'sales_list'])
```

Conversely, if the method that will change the dict or list values, it will raise error.

```py
const.APPLE_DATA.update({'season': 'winter'})
```

```
ConstantError: To update dict values is not allowed.
```

If you want to allow the setting of the same constant value, calling the `accept_same_value` method will prevent errors. This setting can be convenient in situations where you are running Jupyter cells multiple times.

```py
const.accept_same_value()
const.APPLE_PRICE = 100

# Setting the same value like this will not raise an error.
const.APPLE_PRICE = 100
```

# For test

Test will be run by nose library (https://nose.readthedocs.io/en/latest/).

```
# pip install nose
```

Probably this pip command requires "Run as Administrator".

Then move to pconst directory, and run following command:

```
$ nosetests -s
```
