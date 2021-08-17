import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="impeek",
    version="0.0.8",
    author="Nikolas Lamb",
    author_email="nikolas.lamb@gmail.com",
    description="Quickly create a collage of images using a regular expression.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nikwl/impeek",
	packages=["impeek", "imdump"],
	license='LICENSE',
	install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)