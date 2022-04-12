from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="StudentAssist",
    version="0.0.1",
    author="A+ Labs",
    description="StudentAssist is a Utica College CSC433 Final Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wesleyaou/CSC433",
    project_urls={
        "Bug Tracker": "https://github.com/wesleyaou/CSC433/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
    ],
    install_requires=["flask"],
    packages=["StudentAssist"],
    include_package_data=True,
    package_data={"StudentAssist": ["StudentAssist/web/*", "tests/*"]},
    python_requires=">=3.6",
)