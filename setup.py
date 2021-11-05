from os import path
from re import search
from setuptools import setup, find_packages


HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    readme = f.read()

with open(path.join(HERE, "src", "json_normalize", "__init__.py"), encoding="utf-8") as f:
    version = search(r'VERSION = "(\d+\.\d+\.\d+)"', f.read()).group(1)

setup(
    name="json-normalize",
    version=version,
    description="Recursively flattens a JSON-like structure into a list of flat dicts.",
    license="MIT",
    author="The Funnel Dev Team",
    author_email="open-source@funnel.io",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="JSON",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires="~=3.7",
    project_urls={
        "Bug Reports": "https://github.com/funnel-io/json-normalize/issues",
        "Source": "https://github.com/funnel-io/json-normalize",
    },
    url="https://github.com/funnel-io/json-normalize",
)
