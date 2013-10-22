from distutils.core import setup

import vyky

setup(
    name='vyky',

    version=vyky.__version__,
    description='A Genetic Algorithm to run TSPLib instances',
    long_description=vyky.__doc__,
    license=vyky.__license__,
    url='https://github.com/vyscond/vyky',

    author=vyky.__author__,
    author_email='vyscond@gmail.com',


    py_modules=['vyky'],
    scripts=['vyky.py']
)
