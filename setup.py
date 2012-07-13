from distutils.core import setup

setup(
    name='vote_client',
    version='0.1.0',
    author='Andrew Szymanski',
    author_email='',
    packages=['vote'],
    scripts=['bin/vote.py',],
    url='https://github.com/nws-cip/probe/tree/master/cip_client/',
    license='LICENSE.txt',
    description='Vote client libraries',
    long_description=open('README.txt').read(),
    install_requires=[
        "simplejson==2.5.2",
    ],
)