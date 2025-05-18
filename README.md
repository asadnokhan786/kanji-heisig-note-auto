# kanji-heisig-note-auto

## Purpose
- Given the chapter number of a chapter from James Heisig's Remembering the Kanji, auto populate a note template for every knaji in that chapter

## Initialization
1. Run `python -m venv venv` to create virtual environemnt
2. Activate virutal environment `source venv/bin/activate` on linux/unix systems
3. Run `pip install -r requirements.txt` to install dependencies

## Usage
- Run `python3 main.py <chapter-number>` to generate auto populated kanji notes based on template file

## Template Requirements
- Fields must be encapsulated with `{}` curly braces
- Currently supported fields & corresponding naming convention
    - Heisig Number: `heisig_number`
    - Keyword: `keyword`
    - Unicode: `kanji`
    - PNG file: `png_file`

## External Credit
- PNG files are automatically generated based on svg files in this repository cloned from [kanjivig](https://github.com/KanjiVG/kanjivg)
- Unicode list, heisig number order, and keywords were extracted from the csv provided by [heisig-rtk-index](https://github.com/cyphar/heisig-rtk-index)