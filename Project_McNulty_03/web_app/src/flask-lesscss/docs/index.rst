Welcome to flask-lesscss's documentation!
=========================================

If you use `LessCSS`_ to stay sane while writing CSS, you probably know it can
be a pain to run ``lessc --watch static/style.less`` every time you want to
work on your styles. It gets even worse when you have more than one ``.less``
file.

flask-lesscss is a small `Flask`_ extension that will automatically re-render
your ``.less`` files into CSS before each request if they've changed.

**NOTE:** You need to have the LessCSS gem installed for this to work.

.. _LessCSS: http://lesscss.org/
.. _Flask: http://flask.pocoo.org/

Installation
------------

Install flask-lesscss with `pip`_::

    pip install -e 'hg+http://bitbucket.org/sjl/flask-lesscss@v0.9.1#egg=flask-lesscss'

Prefer `git`_ to `Mercurial`_?

::

    pip install -e 'git+http://github.com/sjl/flask-lesscss.git@v0.9.1#egg=flask-lesscss'

.. _pip: http://pip.openplans.org/
.. _git: http://git-scm.com/
.. _Mercurial: http://hg-scm.org/

Usage
-----

You can activate it by calling the ``lesscss`` function with your Flask app as
a parameter::

    from flaskext.lesscss import lesscss
    lesscss(app)

This will watch your app's static media directory and automatically render
``.less`` files into ``.css`` files in the same (sub)directory.

When you deploy your app you might not want to accept the overhead of checking
the modification time of your ``.less`` and ``.css`` files on each request.
A simple way to avoid this is wrapping the ``lesscss`` call in an ``if``
statement::

    if app.debug:
        from flaskext.lesscss import lesscss
        lesscss(app)

If you do this *you'll* be responsible for rendering the ``.less`` files into
CSS when you deploy in non-debug mode to your production server.

Contribute
----------

If you want to contribute feel free to fork the `Mercurial repository`_ or `git
repository`_ and send a pull request.

.. _Mercurial repository: http://bitbucket.org/sjl/flask-lesscss/
.. _git repository: http://github.com/sjl/flask-lesscss/
