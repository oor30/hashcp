from setuptools import setup, find_packages

def requirements_from_file(file_name: str) -> list[str]:
    return open(file_name).read().splitlines()

setup(
    name='hashcpa',
    version='0.1.0',
    description='hashcp package',
    author='kazuki wakamatsu',
    packages=find_packages(),
    install_requires=['natsort'],
    license='MIT',
)