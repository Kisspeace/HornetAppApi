from setuptools import setup

setup(
    name = 'HornetAppApi', 
    version = '0.1.1', 
    author='Kisspeace',
    # author_email='Kisspeace@example.com',
    url='http://github.com/Kisspeace/HornetAppApi',
    description='gethornet.com API wrapper',
    packages = ['HornetAppApi'],
    install_requires=[
        # 'uuid',
        'aiohttp'
    ]
)