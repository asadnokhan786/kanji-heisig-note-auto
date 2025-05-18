import pandas as pd
import os

# Function to read the template from a file
def read_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def populate_template(row):
    """
    Populates the template with values from the DataFrame row.
    
    Parameters:
    template (str): The template string with placeholders.
    row (pandas.Series): A row of the DataFrame containing data for a single kanji.
    
    Returns:
    str: A populated template string.
    """
    # Assuming read_template reads the template file into a string
    template = read_template("template.md")
    
    # Populate the template using str.format
    populated_template = template.format(
        png_file=f"{row['unicode_code_point']}.png",  # Ensures correct png filename format
        keyword=row['keyword'].title(),
        kanji=row['kanji'],
        heisig_number=row['heisig_number']
    )
    
    return populated_template


