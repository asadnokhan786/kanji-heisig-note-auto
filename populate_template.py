import pandas as pd
import os

# Function to read the template from a file
def read_template(template_path):
    """
    Reads the template from the specified file.
    
    Parameters:
    template_path (str): Path to the template file.
    
    Returns:
    str: The template content as a string.
    """
    with open(template_path, 'r') as template_file:
        template = template_file.read()
    return template

# Function to populate the template for each row in the DataFrame
def populate_template(row):
    """
    Populates the template with values from the DataFrame row.
    
    Parameters:
    template (str): The template string with placeholders.
    row (pandas.Series): A row of the DataFrame containing data for a single kanji.
    
    Returns:
    str: A populated template string.
    """
    template = read_template("template.md")
    populated_template = template.format(
        png_file=(row['unicode_code_point']+".png"),
        keyword=row['keyword'],
        kanji=row['kanji'],
        heisig_number=row['heisig_number']
    )
    return populated_template

