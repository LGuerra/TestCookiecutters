========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/TestCookiecutters/badge/?style=flat
    :target: https://readthedocs.org/projects/TestCookiecutters
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/testcookie.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/testcookie

.. |downloads| image:: https://img.shields.io/pypi/dm/testcookie.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/testcookie

.. |wheel| image:: https://img.shields.io/pypi/wheel/testcookie.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/testcookie

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/testcookie.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/testcookie

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/testcookie.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/testcookie


.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD license

Installation
============

::

    pip install testcookie

Documentation
=============

https://TestCookiecutters.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
