Contributing
============
All contributions to this project are welcome via pull request (PR) on the `Github repository <https://github.com/anvilistas/anvil-extras>`_

Guidelines
----------
#. Issues

   Please open an `Issue <https://github.com/anvilistas/anvil-extras/issues>`_ and describe the contribution you'd like to make before submitting any code. This prevents duplication of effort and makes reviewing the eventual PR much easier for the maintainers.

   If you could start the name of the branch you work on with the number of the issue you create, that would be very helpful as github will automatically link the two together.
#. Commits

   Please try to use commit messages that give a meaningful history for anyone using git's log features. Try to use messages that complete the sentence, "This commit will..." There is some excellent guidance on the subject from `Chris Beams <https://chris.beams.io/posts/git-commit/>`_
#. Components

   All the components in the library are intended to work from the anvil toolbox as soon as the dependency has been added to an application, without any further setup. This means that they cannot use any of the features within the library's theme.

   If you are thinking of submitting a new component, please ensure that it is entirely standalone and does not required any css or javascript from within a theme element or native library.
#. Python Code

   * Please try, as far as possible, to follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_
   * Use the `Black formatter <https://github.com/ambv/black>`_ to format all code and the `isort utility <https://github.com/timothycrosley/isort>`_ to sort import statements.
#. Documentation

   Please include documentation for your contribution as part of your PR. Our documents are written in `reStructuredText <https://en.wikipedia.org/wiki/ReStructuredText>`_ and hosted at `Read The Docs <https://anvil-extras.readthedocs.io/en/latest/>`_

   Our docs are built using `Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_ which you can install locally and use to view your work before submission. To build a local copy of the docs in a 'build' directory:

   .. code-block::

       sphinx-build docs build

   You can then open 'index.html' from within the build directory using your favourite browser.
#. Testing

   The project uses the `Pytest <https://docs.pytest.org/en/stable/>`_ library and its test suite can be run with:

   .. code-block::

       python -m pytest

   We appreciate the difficulty of writing unit tests for Anvil applications but, if you are submitting pure Python code with no dependency on any of the Anvil framework, we'll expect to see some additions to the test suite for that code.
#. Merging

   We require both maintainers to have reviewed and accepted a PR before it is merged.
   
   If you would like feedback on your contribution before it's ready to merge, please create a draft PR and request a review.
#. Copyright

   By submitting a PR, you agree that your work may be distributed under the terms of the project's `licence <https://github.com/anvilistas/anvil-extras/blob/master/LICENSE>`_ and that you will become one of the project's `joint copyright holders <https://github.com/anvilistas/anvil-extras/graphs/contributors>`_.
