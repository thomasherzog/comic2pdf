from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

with open("requirements.txt", "r") as file:
    requirements = []
    for line in file:
        requirements.append(line.split("#")[0])

setup(
    name="comic2pdf",
    version="1.0",
    description="comic2pdf converts comic book format to pdf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Thomas Herzog",
    scripts=["src/comic2pdf.py"],
    license="MIT",
    install_requires=requirements
)
