import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="frotaintegra",
    version="0.0.1",
    author="Roberto Neves",
    author_email="robertonsilva@gmail.com",
    description=("Integraçao simplificada com FrotaSaas Guberman"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robertons/frotaintegra",
    project_urls={
        "Bug Tracker": "https://github.com/robertons/frotaintegra/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "beautifulsoup4==4.11.1",
        "blessed==1.19.1",
        "certifi==2022.12.7",
        "charset-normalizer==3.0.1",
        "idna==3.4",
        "inquirer==3.1.2",
        "install==1.3.5",
        "python-editor==1.0.4",
        "readchar==4.0.3",
        "requests==2.28.2",
        "requests-toolbelt==0.10.1",
        "six==1.16.0",
        "soupsieve==2.3.2.post1",
        "Unidecode==1.3.6",
        "urllib3==1.26.14",
        "wcwidth==0.2.6"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "frotaintegra = frotaintegra.cli:main",
        ]
    }
)
