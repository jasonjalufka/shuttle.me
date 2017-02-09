DoubleMap API Client
====================


This library helps you to pull data from DoubleMap.
Included is a command line utility for determining when buses will arrive and which one to get on.


[www.doublemap.com](http://www.doublemap.com/)


Installation
------------

Via source code / GitHub:

    $ git clone https://github.com/travcunn/doublemap.git doublemap
    $ cd doublemap
    $ python setup.py install


Usage
-----
```python
>>> from doublemap import DoubleMap
>>> tracker = DoubleMap('iupui')
>>>
>>> # dict of buses. keys are bus ids.
>>> tracker.buses
>>> # retrieve info about route 23
>>> tracker.route_info(23)
```


Command Line Utility
--------------------
Included is a command line utility for accessing bus route information, which can be run after installing the package:

    $ doublemap
