from setuptools import setup

setup(
    name='jerakia',
    version='0.1.5',
    packages=['jerakia'],
    include_package_data=True,
    description='Jerakia module',
    author='Jon Ander Novella',
    install_requires=[
        'requests>=2.0',
        'mock',
        'jinja2',
        'pyaml',
        'six',
        'cryptography>=2.2.1',
        'pyOpenSSL'
    ]
)
