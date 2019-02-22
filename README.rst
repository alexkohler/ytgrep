ytgrep
-----------------------

ytgrep is a CLI tool to search youtube closed captions with a grep-like interface

Requirements
===========

* Requires python >= 3.5

Installation
===========
.. code:: bash
    
    pip install ytgrep

Usage
===========

.. code:: bash



Development
===========

Run Tests
~~~~~~~~~

*Note:* Functional tests do download directly from Youtube

.. code:: bash

   ## All tests
   python -m unittest discover

   ## Unit tests
   python -m unittest discover test/unit

   ## Functional tests
   python -m unittest discover test/functional

Related projects
============
 * youtube-closed-captions - This project used this library as a starting point https://github.com/mkly/youtube-closed-captions
 * videogrep - get supercuts of video matching provided seach terms
    

TODO
============
* Supporting languages other than English
* -e '*' breaks ytgrep - appears to be applying red more than once
* Run coverage and see if any tests are missing
