import argparse
import pandas as pd
import os
import shutil
import zipfile
from generate_png import svg_to_png  # Assuming svg_to_png function is in svg_converter.py
from populate_template import populate_template  # Assuming populate_template function is in populate_template.py

def process_chapter(chapter_num):
    # Ensure chapter number is within the valid range
    if chapter_num < 1 or chapter_num > 56:
        print(f"Error: Chapter number {chapter_num} is out of range. Please enter a number between 1 and 56.")
        return

    # Path to the CSV file for the chapter
    csv_file_path = f"chapters/lesson_{chapter_num}/kanji_data.csv"
    
    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file for chapter {chapter_num} not found at {csv_file_path}.")
        return

    # Load the CSV into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Path to the zip file of SVGs for the chapter
    zip_file_path = f"chapters/lesson_{chapter_num}/lesson_{chapter_num}_svgs.zip"
    
    # Check if the zip file exists
    if not os.path.exists(zip_file_path):
        print(f"Error: Zip file for chapter {chapter_num} not found at {zip_file_path}.")
        return
    
    # Create a directory to unzip the SVG files
    unzip_dir = f"chapters/lesson_{chapter_num}/svgs"
    os.makedirs(unzip_dir, exist_ok=True)
    
    # Unzip the SVG files
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_dir)
    
    # Create the output directories
    output_png_dir = os.path.join(os.getcwd(), f"output/lesson_{chapter_num}/png_files")
    os.makedirs(output_png_dir, exist_ok=True)
    
    output_templates_dir = os.path.join(os.getcwd(), f"output/lesson_{chapter_num}/kanji-templates")
    os.makedirs(output_templates_dir, exist_ok=True)

    # Iterate through the DataFrame and process each kanji
    for index, row in df.iterrows():
        # Populating the template
        populated_template = populate_template(row)

        # Save the populated template to a file named by the keyword of the kanji
        template_filename = os.path.join(output_templates_dir, f"{row['keyword']}.md")
        with open(template_filename, 'w') as f:
            f.write(populated_template)

        # Call svg_to_png to generate the PNG for the kanji
        svg_filename = os.path.join(unzip_dir, f"{row['unicode_code_point']}.svg")
        if os.path.exists(svg_filename):
            output_png_filename = os.path.join(output_png_dir, f"{row['unicode_code_point']}.png")
            svg_to_png(svg_filename, output_png_filename)
        else:
            print(f"Warning: SVG file for {row['unicode_code_point']} not found.")

    # Delete the unzipped folder after processing
    # shutil.rmtree(unzip_dir)
    print(f"Finished processing chapter {chapter_num}. All files are saved.")

# Set up argparse to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Process a specific chapter based on the chapter number.")
    
    # Add the chapter argument (expects an integer between 1 and 56)
    parser.add_argument('chapter', type=int, help="Chapter number (1 through 56)")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the function with the provided chapter number
    process_chapter(args.chapter)

if __name__ == '__main__':
    main()
