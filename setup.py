import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="espn_fantasy_basketball_analytics",
    version="0.0.2",
    author="Justin Tran",
    author_email="justinbt21@gmail.com",
    license="MIT",
    description="To pull in data from ESPN Fantasy Basketball and do analysis on top of it.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justinbt21/espn_fantasy_basketball_analytics",
    packages=setuptools.find_packages(),
    package_data={'espn_fantasy_basketball_analytics': ['*.txt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'beautifulsoup4>=4.8.2',
        'bs4>=0.0.1',
        'lxml>=4.6.5',
        'numpy>=1.21.0',
        'pandas>=1.3.1',
        'python-dateutil==2.8.1',
        'pytz==2019.3',
        'requests==2.27.1',
        'six==1.13.0',
        'soupsieve==1.9.5',
        'unidecode==1.2.0'
    ],
    extras_require={
        'test': ['unittest'],
    },
    keywords=[
        "nba",
        "sports",
        "data mining",
        "basketball",
        "basketball reference",
        "basketball-reference.com",
        ],
)
