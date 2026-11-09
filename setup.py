from setuptools import setup, find_packages

setup(
    name="aeroengineer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A clean and practical Python package for aeronautical engineering calculations",
    packages=find_packages(include=["aeroengineer", "aeroengineer.*"]),
    install_requires=["numpy"],
    python_requires='>=3.7',
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
