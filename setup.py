from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="quickstart_etl",
        packages=find_packages(exclude=["quickstart_etl_tests"]),
        install_requires=[
            "dagster",
            "dagster-cloud",
            "pandas",
            "matplotlib",
            "textblob",
            "tweepy",
            "wordcloud",
        ],
    )
