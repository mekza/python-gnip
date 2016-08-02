python-gnip
=============


Gnip API wrapper

Installation
------------

Method with pip: if you have pip installed, just type this in a terminal
(sudo is optional on some systems)

::

    pip install python-gnip

Method by hand: download the sources, either on PyPI or (if you want the
development version) on Github, unzip everything in one folder, open a
terminal and type

::

    python setup.py install

Usage
-----


Rules
~~~~~~~~~~


.. code:: python

    from gnip import Gnip
    g = Gnip(YOUR_ACCOUNT_NAME,
            login=YOUR_EMAIL,
            password=YOUR_PASSWORD
    )
    print(g.get_rules())

Stream
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from gnip import Gnip
    g = Gnip(YOUR_ACCOUNT_NAME,
            login=YOUR_EMAIL,
            password=YOUR_PASSWORD
    )
    s = g.connect_stream()
    for line in s.iter_lines():
        print(line)
