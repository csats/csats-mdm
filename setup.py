from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="csats-mdm",
    version="0.0.2",
    author="Adam Monsen",
    author_email="amonsen@its.jnj.com",
    url="https://git.csats.pizza/csats/devenv",
    description="C-SATS mobile device management for Ubuntu GNU/Linux workstations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
