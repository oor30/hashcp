from setuptools import find_packages, setup

setup(
    name='hashcp',
    version='1.0.0',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'natsort~=8.4.0'
    ],
    entry_points={
        'console_scripts': [
            'hashcp=hashcp.core:cli'
        ]
    },
    
    author='kazuki wakamatsu',
    author_email='kazuki.w.0920+oor30@gmail.com',
    url='https://github.com/oor30/hashcp',
)