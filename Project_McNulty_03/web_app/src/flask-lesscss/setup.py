"""
flask-lesscss
----------

A small Flask extension that makes it easy to use LessCSS with your Flask
application.

Links
`````

* `documentation <http://sjl.bitbucket.org/flask-lesscss/>`_
* `development version
  <http://bitbucket.org/sjl/flask-lesscss/get/tip.gz#egg=flask-lesscss-dev`_


"""
from setuptools import setup


setup(
    name='flask-lesscss',
    version='0.9.1',
    url='http://sjl.bitbucket.org/flask-lesscss/',
    license='MIT',
    author='Steve Losh',
    author_email='steve@stevelosh.com',
    description='A small Flask extension that adds LessCSS support to Flask.',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
