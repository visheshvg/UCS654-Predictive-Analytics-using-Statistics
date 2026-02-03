from setuptools import setup, find_packages

setup(
    name="Topsis-Vishesh-102303961",
    version="0.1",
    author="Vishesh",
    author_email="vishesh@example.com",
    description="A Python package implementing TOPSIS method",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    packages=find_packages(),   # will detect topsis_package

    install_requires=[
        "pandas",
        "numpy"
    ],

    entry_points={
        "console_scripts": [
            "topsis=topsis_package.topsis:main"
        ]
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires=">=3.6",
)
