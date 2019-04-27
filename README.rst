ytgrep
-----------------------

ytgrep is a CLI tool to search youtube closed captions with a grep-like interface.


Requirements
=============

* Requires python >= 3.5

Installation
=============

.. code:: bash
    
    pip install ytgrep

Purpose
=============
ytgrep is particularly useful whilst looking for particular topic or keywords mentioned in a video.

    For example, searching for the word 'topoloigcal sort' in `MIT's Open Courseware Lecture on DFS and topological sort <https://www.youtube.com/watch?v=AfSk24UTFS8>`__:

|image0|

.. |image0| image:: https://asciinema.org/a/SjG0XTmIPzDfNgx2SxwhCdXwt.svg
   :target: https://asciinema.org/a/SjG0XTmIPzDfNgx2SxwhCdXwt
   

Usage
==============

.. code:: bash

    usage: ytgrep.py [-h] [-e] [-v] [-links] pattern urls [urls ...]

Flags
=============
* -e <PATTERN> - specify a regular expression to match
* -v - verbose, print debug information
* -links - include the time shortcut link with each match (see example below) 


More examples
=============

Include shortcut links to times where keywords were mentioned

.. code:: bash
    
    $ ytgrep -links 'potassium' https://www.youtube.com/watch?v=OIYOshsEqmQ

Search with regular expression

.. code:: bash

    ytgrep -e 'banana|potassium' https://www.youtube.com/watch?v=OIYOshsEqmQ
    

Search multiple urls

.. code:: bash

    ytgrep 'banana' https://www.youtube.com/watch?v=LH5ay10RTGY https://www.youtube.com/watch?v=zFQWVN4xip0
    

    


Development
=============

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
==================
 * youtube-closed-captions - This project used this library as a starting point https://github.com/mkly/youtube-closed-captions
 * videogrep - get supercuts of video matching provided seach terms
