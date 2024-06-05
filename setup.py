from setuptools import setup

setup(
    name = 'HornetAppApi',
    version = '1.1.0',
    author='Kisspeace',
    url='http://github.com/Kisspeace/HornetAppApi',
    description='gethornet.com API wrapper',
    packages = ['HornetAppApi', 'HornetAppApi.aiohttp', 'HornetAppApi.requests'],
    install_requires=[
        # 'uuid',
        'aiohttp',
        'requests'
    ]
)
