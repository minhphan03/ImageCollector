from importlib.metadata import requires
from setuptools import setup, find_packages

rerquires = [
    'tornado',
    'motor'
]

setup(
    name='image-uploader',
    version='1.0',
    description='A local image uploader backed by a local MongoDB instance',
    author='Minh Phan',
    email='vuanhminhphan@gmail.com',
    packages=find_packages(),
    requires=requires
)