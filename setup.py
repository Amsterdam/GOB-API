from setuptools import setup, find_packages

setup(
    name="GOB-API",
    version="0.1",
    url="https://github.com/Amsterdam/GOB-API.git",
    license="MPL2",
    author="Amsterdam",
    author_email="datapunt@amsterdam.nl",
    description="GOB-API",
    package_dir={"": "src"},
    packages=find_packages(exclude=["tests"]),
)
