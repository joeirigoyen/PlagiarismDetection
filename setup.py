from setuptools import setup, find_packages

setup(
    name="plagiarism-detector-v1",
    version="1.0.0",
    description="Simple plagiarism detector that uses cosine similarity to compare files.",
    url="https://github.com/joeirigoyen/PlagiarismDetection",
    author="Youthan Irigoyen, Eduardo Rodríguez, Rebeca Rojas",
    license="MIT",
    classifiers=['Development Status :: 2 - Beta', 'Intended Audience :: Developers', 'Topic :: Plagiarism Detection', 'Programming Language :: Python :: 3.10'],
    keywords="plagiarism detection",
    packages=find_packages(include=['src', 'src.*', 'test', 'test.*']),
    python_requires='>=3.10'
    )
