from distutils.core import setup

setup(
    name='Compost',
    version='0.1.0',
    author='Maxi Weß',
    author_email='maxwess@googlemail.com',
    packages=['compost'],
    scripts=['bin/compost.py'],
    url='http://pypi.python.org/pypi/Compost/',
    license='LICENSE.txt',
    description='Useful for comparative analysis of POS-Taggers.',
    long_description=open('README.txt').read(),
    install_requires=[],
    extra_requires=[
        "nltk >= 3.7.0",
        "dill >= 0.2.8.2",
    ],
)
