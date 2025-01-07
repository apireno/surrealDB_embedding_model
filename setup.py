# setup.py
from setuptools import setup, find_packages

setup(
    name='surrealdb_embedding_model',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'surrealdb',
        'torch',
    ],
)