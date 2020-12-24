"""Module containing entrypoint definitions."""
from . import data

def show_data_folder():
    """Return the path to the data folder."""
    print(data.__package__.replace(".", "/"))
