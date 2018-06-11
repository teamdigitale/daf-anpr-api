# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Core Vocabularies API ",
    author_email="robipolli@gmail.com",
    url="",
    keywords=["Swagger", "Core Vocabularies API "],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    Dictionaries are versioned key-value store that you can   retrieve via API. For each dictionary you can:   - get metadata infos   - retrieve a paged subset   - get a single entry via an unique key   - find entries by a given key (which could not be unique)    Dictionary structure is the following:   - Dictionary: has a single name and many versions     - Table: it&#39;s a specific version of a dictionary. May         expire         - Entry: it&#39;s the actual data contained in a table.  Despite http://zalando.github.io/restful-api-guidelines/index.html#160     we use pagination as it&#39;s more intuitive for this use case. 
    """
)

