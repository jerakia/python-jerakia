from setuptools import setup,find_packages

setup(
    name='jerakia',
    version='0.4.0',
    packages=find_packages(),
    include_package_data=True,
    description='Jerakia',
    author='Jon Ander Novella',
    install_requires=[
        'requests>=2.0',
        'msgpack',
        'mock',
        'jinja2',
        'pyaml',
        'six',
        'cryptography>=2.2.1',
        'pyOpenSSL'
    ]
)
