import os
from distutils.core import setup

setup(
    name='swiftlink',
    version='1.0',
    packages=['src'],
    package_dir={'': 'src'},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'swiftlink-server=src.swiftlink_server:swiftlink_server',
            'swiftlink-client=src.swiftlink_client:swiftlink_client',
        ],
    },
)
