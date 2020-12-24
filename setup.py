from setuptools import setup, find_packages

setup(
    name="word-of-the-day-bot",
    version="0.1",
    packages=find_packages(include=["wotdb", "wotdb.*"]),
    package_data={"wotdb": ["templates/*.html"]},
    entry_points={
        "console_scripts": [
            "generate_image=wotdb.main:generate_image",
            "generate_and_open=wotdb.main:generate_and_open",
            "generate_and_post=wotdb.main:generate_and_post",
        ]
    },
)
