from setuptools import setup, find_packages
from os import path
from re import search


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

with open(path.join(here, "src", "json_normalize", "__init__.py"), encoding="utf-8") as f:
    version = search(r'VERSION = "(\d+\.\d+\.\d+)"', f.read()).group(1)

setup(
    name="json-normalize",
    version=version,
    description="Recursively flattens a json-like structure into a list of dicts of depth 1.",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/funnel-io/json-normalize",
    author="Hampus Hellström",
    author_email="hampus@funnel.io",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires="~=3.7",
    project_urls={
        "Bug Reports": "https://github.com/funnel-io/json-normalize/issues",
        "Source": "https://github.com/funnel-io/json-normalize",
    },
)
