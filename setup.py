import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

REPO_NAME = "text-summarizer"
AUTHOR_USER_NAME = "SuryaKTiwari11"
AUTHOR_EMAIL = "jamcocobutter@gmail.com"
SRC_REPO = "textSummarizer"

setuptools.setup(
    name=REPO_NAME,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Python package for text summarization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SuryaKTiwari11/Text-Summarizer",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add your dependencies here, e.g.:
        # "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
