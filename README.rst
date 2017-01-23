===============================
FlowGen
===============================


.. image:: https://img.shields.io/pypi/v/flowgen.svg
        :target: https://pypi.python.org/pypi/flowgen

.. image:: https://img.shields.io/travis/ad-m/flowgen.svg
        :target: https://travis-ci.org/ad-m/flowgen

.. image:: https://readthedocs.org/projects/flowgen/badge/?version=latest
        :target: https://flowgen.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ad-m/flowgen/shield.svg
     :target: https://pyup.io/repos/github/ad-m/flowgen/
     :alt: Updates


code to flowchart converter.


* Free software: MIT license
* Documentation: https://flowgen.readthedocs.io.


Features
--------

* draw flowchart from pseudocode

Example
--------

It's simple to draw diagram based on simple pseudocode like::

    Hello Smith;
    Ask Smith about coffee;
    if(Smith want coffee){
        Make coffee;
        // Warning, it might be hot!
    }
    // Be nice
    Let's party!;
    Good night Smith!;

It was rendered as:

.. image:: https://raw.githubusercontent.com/ad-m/flowgen/master/examples/basic_code.png
     :alt: Rendered diagram



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

