from setuptools import setup

setup(
    name = 'HornetAppApi',
    version = '1.0.0',
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