from setuptools import setup, find_packages
setup(
    name="word-of-the-day-bot",
    version="0.1",
    packages=find_packages(include=["wotdb", "wotdb.*"]),
    package_data={"wotdb": ["templates/*.html"]},
    entry_points={
        "console_scripts": ["generate_image=wotdb.main:run"]
    },
)
