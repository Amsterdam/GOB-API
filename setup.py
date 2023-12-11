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
    packages=find_packages(where="src"),
    install_requires=[
        "aniso8601==7.0.0",
        "antlr4-python3-runtime==4.7.2",
        "Flask==2.3.2",
        "Flask-Cors==3.0.10",
        "Flask-GraphQL==2.0.1",
        "geojson==2.5.0",
        "graphene==2.1.9",
        "graphene-sqlalchemy==2.1.2",
        "graphql-core==2.3.2",
        "graphql-relay==2.0.1",
        "graphql-server-core==1.2.0",
        "promise==2.3",
        "pydantic~=1.10.13",
        "PyYAML==6.0.1",
        "Rx==1.6.1",
        "singledispatch~=3.7.0",
        "gobcore @ git+https://github.com/Amsterdam/GOB-Core.git@v2.23.0"
    ]
)
