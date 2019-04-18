from setuptools import setup

setup(
    name='snapper',
    version='0.1',
    author='Rex',
    author_email='rex@hacktrader.com',
    description='Snapshot maker for EC2 instance volumes',
    license="GPLv3+",
    packages=['snapper_ec2'],
    url='https://github.com/rexblein/snapper',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
       [console_scripts]
       snapper_ec2=snapper_ec2.snapper_ec2:cli
    ''',

)
