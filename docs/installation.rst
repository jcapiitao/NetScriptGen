NetScriptGen Installation and Python Basics
=============================================

A note about Python
-------------------

What sort of language is Python ? Well, the naïve view of computer languages is that they come as either compiled languages or interpreted languages. Python is one of those interpreted languages. It does not have to be explicitly compiled but behind the scenes there is a system that compiles Python (.py) into an intermediate code (.pyc) which is stashed away to make things faster in future.
But it does'nt matter for you, the machine does this without you having to do anything explicit yourself. You can treat Python as a purely interpreted language like the Shell or JavaScript.

The core philosophy of the language is summarized by the document `PEP 20 (The Zen of Python)`_, which includes aphorisms such as:

- Beautiful is better than ugly
- Explicit is better than implicit
- Simple is better than complex
- Complex is better than complicated
- Readability counts


If you want to dive yourself deeper in Python history, see the `Nick Coghlan's Python Notes`_ documentation.


Installing NetScriptGen
------------------------
NetScripGen needs Python version 3.4+, the OS should not matter.
I had to make a choice between Python 2.x and Python 3.x version. Personally, at this time, I think that it really depends on what third-party 
libraries yo rely on. But in the future, when all the Python 2.x libraries will be ported to Python 3.x, it will be the most widely used version.

Furthermore, Python 3.4 and 3.5 are gathering all the cool new stuff that make life easier for developers. So, as all my third-parties are supported in Python3.4, I decided to go ahead with this Python version.

You can check your python version with the ``-V`` switch...

.. code-block:: none

   jcapitao@SanJose:~$ python -V
   Python 3.4.0
   jcapitao@SanJose:~$ $


Install from the source
~~~~~~~~~~~~~~~~~~~~~~~

1. Download the `NetScripGen compressed tarball`_
2. Extract it
3. Run the ``setup.py`` script in the tarball: ::

      python setup.py install


Github
~~~~~~~~~~~~~~~~~~~~

If you're interested in the source, you can always pull from the `Github repository`_:

   ::

      git clone https://github.com/JoelCapitao/NetScriptGen.git


Using NetScriptGen
------------------

Once you have installed NetScriptGen on your system, it's time to run it.

.. code-block:: shell

   jcapitao@SanJose:~$ python netscriptgen
   netscriptgen -e <excelFile> -t <scriptTemplate> -o <directory>


.. _`Nick Coghlan's Python Notes`: http://python-notes.curiousefficiency.org/en/latest/python3/questions_and_answers.html

.. _`PEP 20 (The Zen of Python)`: https://www.python.org/dev/peps/pep-0020/

.. _`NetScripGen compressed tarball`: http://trystram.net/dl/netscriptgen.tar.gz

.. _`Github repository`: https://github.com/JoelCapitao/NetScriptGen
