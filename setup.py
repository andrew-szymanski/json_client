from distutils.core import setup

setup(
    name='vote_client',
    version='1.0',
    author='Andrew Szymanski',
    author_email='',
    packages=['vote'],
    scripts=['vote/vote.py',],
    url='https://github.com/andrew-szymanski/json_client',
    license='LICENSE.txt',
    description='Vote client libraries',
    long_description=open('README.txt').read(),
    install_requires=[
        "simplejson>=2.5.2",
    ],
)