ytgrep
-----------------------

ytgrep is a CLI tool to search youtube closed captions with a grep-like interface.


Purpose
=============
ytgrep is particularly useful whilst looking for particular topic or keywords in a video. For example, suppose you are 
interested in learning more about Breadth First Search. Rather than watching MIT Open Courseware's entire 50 minute video,
you can do the following with ytgrep:


.. code:: bash

    python ytgrep.py 'bfs' https://www.youtube.com/watch?v=s-CYnVz-uh4
    [00:46:22.109 --> 00:46:24.170] compute this shortest we compute this path out of bfs which is follow a parent
    [00:46:24.170 --> 00:46:24.180] path out of bfs which is follow a parent
    [00:46:24.180 --> 00:46:26.450] path out of bfs which is follow a parent of v is c prime of c is x parent of x is
    [00:47:25.799 --> 00:47:28.459] the shortest path thats the cool thing about bfs yeah bfs explores of vertices"


Requirements
=============

* Requires python >= 3.5

Installation
=============
.. code:: bash
    
    pip install ytgrep

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
    

TODO
============
* Supporting languages other than English
* -e '*' breaks ytgrep - appears to be applying red more than once
* Run coverage and see if any tests are missing
