from setuptools import setup, find_packages

with open("requirements.txt") as requirements:
    dependencies = requirements.read().strip().split("\n")

package = "utopia-audio-processor"
version = "1.0.0"

setup(
    name=package,
    version=version,
    install_requires=dependencies,
    packages=find_packages()
)