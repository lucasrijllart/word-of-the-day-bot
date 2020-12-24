from setuptools import setup, find_packages

setup(
    name="word-of-the-day-bot",
    version="0.1",
    packages=find_packages(include=["wotdb", "wotdb.*"]),
    package_data={"wotdb": ["templates/*.html"]},
    entry_points={
        "console_scripts": [
            "show_data_folder=wotdb.entrypoints:show_data_folder",
            "generate_image=wotdb.entrypoints:generate_image",
            "generate_and_open=wotdb.entrypoints:generate_and_open",
            "generate_and_post=wotdb.entrypoints:generate_and_post",
        ]
    },
)
