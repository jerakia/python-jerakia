from setuptools import setup

setup(
    name='jerakia',
    version='0.1.0',
    description='Jerakia module',
    author='Jon Ander Novella',
    install_requires=[
        'requests',
        'jinja2',
        'pyaml',
        'six',
        'cryptography>=2.2.1',
        'pyOpenSSL'
    ],
    packages=['jerakia']
)
