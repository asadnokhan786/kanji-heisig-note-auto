import os
import shutil
import zipfile
import pandas as pd
from AyDictionary import AyDictionary


# Read the existing CSV
df = pd.read_csv('KANJI_INDEX.csv')

# Sort by 'id_6th_ed' column in ascending order, in place
df.sort_values(by='id_6th_ed', ascending=True, inplace=True)

# Rename the column 'id_6th_ed' to 'heisig_number', in place
df.rename(columns={'id_6th_ed': 'heisig_number'}, inplace=True)

# Rename the column 'keyword_6th_ed' to 'keyword', in place
df.rename(columns={'keyword_6th_ed': 'keyword'}, inplace=True)

# Convert the 'heisig_number' column to integers
df['heisig_number'] = df['heisig_number'].fillna(0).astype(int)

# Drop unnecessary columns, in place
df.drop(columns=['id_5th_ed', 'keyword_5th_ed', 'on_reading', 'kun_reading', 'components'], inplace=True)

# Initialize the Dictionary object
dictionary = AyDictionary()

# List to store core meanings of the keywords
core_meaning = []

# Following is still experimental, doesn't work well enough yet
# # Iterate over each row in the 'keyword' column to fetch definitions
# for keyword in df['keyword']:
#     try:
#         # Check if the keyword contains more than one word
#         if len(keyword.split()) > 1:
#             print(f"Invalid, keyword '{keyword}' has more than one word")
#             core_meaning.append('Invalid')
#             continue  # Skip this iteration and move to the next keyword
        
#         # Fetch the meaning of the keyword from the dictionary
#         meaning = dictionary.meaning(keyword)
        
#         # If a meaning is found, append it to the core_meaning list
#         if meaning:
#             core_meaning.append(meaning)
#         else:
#             core_meaning.append('Core meaning not found')

#     except Exception as e:  # Catching all errors
#         print(f"An error occurred with keyword '{keyword}': {e}")
#         core_meaning.append('Core meaning not found')

# # Add the 'core_meaning' list as a new column to the DataFrame
# df['core_meaning'] = core_meaning



# List to store unicode code point equivalents of the unicode of the kanji
unicode_code_point = []

for unicode in df['kanji']:
        # Get the Unicode code point using ord()
    code_point = ord(unicode)

    # Convert the code point to hexadecimal and omit the '0x' part
    hex_code = hex(code_point)[2:].zfill(5)

    unicode_code_point.append(hex_code)


# Add unicode code poinnts list as new column to data frame
df['unicode_code_point'] = unicode_code_point


# Array with the number of kanji for each chapter
heisig_kanji_per_chap = [15, 19, 20, 20, 24, 11, 24, 51, 22, 43, 15, 30, 26, 25, 
                         31, 19, 27, 92, 33, 6, 66, 67, 142, 30, 99, 65, 81, 20, 
                         43, 39, 62, 37, 32, 53, 41, 66, 37, 62, 55, 60, 32, 34, 
                         36, 33, 48, 20, 32, 24, 27, 28, 28, 24, 55, 30, 20, 19]

# Initialize the starting index for slicing
start_index = 0

# Define the base paths for the SVG files and the target lesson folders
kanji_svg_dir = 'kanjivg-20250422-all/kanji/'
target_base_dir = 'chapters/'

# Iterate through the array of kanji counts for each chapter
for chapter_num, number_of_kanji in enumerate(heisig_kanji_per_chap, start=1):
    # Slice the DataFrame to get the first 'number_of_kanji' rows for this chapter
    df_chapter = df.iloc[start_index:start_index + number_of_kanji]

    # Create the directory for the chapter, if it doesn't already exist
    target_chapter_dir = os.path.join(target_base_dir, f'lesson_{chapter_num}')
    os.makedirs(target_chapter_dir, exist_ok=True)

    # Save this subset of the dataframe to a new CSV file
    df_chapter.to_csv(os.path.join(target_chapter_dir, 'kanji_data.csv'), index=False)

    # For each kanji in the current chapter, move the corresponding SVG file
    for unicode_code in df_chapter['unicode_code_point']:
        # Construct the SVG file name using the unicode code point
        svg_file_name = f'{unicode_code}.svg'
        svg_file_path = os.path.join(kanji_svg_dir, svg_file_name)

        target_svg_dir = target_chapter_dir+"/svg_files"
        os.makedirs(target_svg_dir, exist_ok=True)

        if os.path.exists(svg_file_path):
            # Move the SVG file to the chapter's directory
            shutil.move(svg_file_path, os.path.join(target_svg_dir, svg_file_name))
            print(f'Moved: {svg_file_name} to {target_svg_dir}')
        else:
            print(f'Warning: SVG file for code point {svg_file_path} not found.')

    # Update the starting index for the next slice
    start_index += number_of_kanji

    # Zip the 'svg_files' folder
    zip_file_path = os.path.join(target_chapter_dir, f'lesson_{chapter_num}_svgs.zip')
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the svg_files folder and add all files to the zip archive
        for root, _, files in os.walk(target_svg_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), target_svg_dir))
    shutil.rmtree(target_svg_dir)

    # Print confirmation for the chapter's CSV creation
    print(f'Created: {os.path.join(target_chapter_dir, "kanji_data.csv")} with {number_of_kanji} kanji')

print("CSV files and SVG files for each chapter have been successfully created and moved.")