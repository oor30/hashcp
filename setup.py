from setuptools import setup, find_packages

def requirements_from_file(file_name: str) -> list[str]:
    return open(file_name).read().splitlines()

setup(
    name='hashcp_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements_from_file('requirements.txt'),
)