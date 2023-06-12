#!/usr/bin/env python3
"""
subtitle-combiner.py

Subtitle Combination Script

This Python script is intended for combining two sets of subtitles from the same video into a single file. It is particularly useful for language learning purposes, where the user might want to see subtitles in two different languages simultaneously (for example, their native language and the language they are trying to learn).

The main functionality of this script is:

1. User is prompted to input the path to the directory containing the subtitle files. If the path is left empty, the script uses the current working directory.

2. The script will then group all the subtitle files in the directory by their base name and language, assuming that the filename format is 'basename.language.srt'.

3. If only one language is found, the script will notify the user and terminate as there are no multiple languages to combine.

4. If exactly two languages are found, these will automatically be selected for combination.

5. If more than two languages are found, the user is prompted to input the two languages they want to combine.

6. Next, the user is asked to choose which language subtitles should be displayed at the top of the video frame.

7. A preview of the changes to be made is displayed, with the format of the combined subtitle file names being 'basename.language1-language2.ass'.

8. After confirmation from the user, the script will combine the subtitles, placing the top language subtitles at the top center of the frame, and the other at the bottom center. Subtitle styling (color, outline, and size) is handled automatically.

9. The combined subtitle files are saved in a subfolder named 'Combined Subtitles' in the specified directory, with the extension '.ass'.

Note: This script requires the Python library pysubs2 to be installed. It is used to load, manipulate, and save the subtitle files. It supports various subtitle formats including .srt and .ass.
"""


import os
import pysubs2
from pysubs2 import Alignment, Color, SSAFile, SSAStyle
from collections import defaultdict

def create_style(lang, position):
    return SSAStyle(alignment=position,
                    primarycolor=Color(255, 255, 255),
                    outlinecolor=Color(0, 0, 0),
                    shadow=0,
                    outline=1,
                    fontsize=22 if lang == "JP" else 20)

def combine_subtitles():
    # Ask for directory
    folder_path = input("Enter the path to your folder (default: current directory): ")
    if not folder_path:
        folder_path = os.getcwd()

    # Group files by base name and language
    subtitles = defaultdict(dict)
    languages = set()
    for filename in os.listdir(folder_path):
        if filename.endswith('.srt'):
            base_name, lang = '.'.join(filename.split('.')[:-2]), filename.split('.')[-2]
            subtitles[base_name][lang] = filename
            languages.add(lang)

    # If only one language is found
    if len(languages) == 1:
        print("\nLanguage found:", ', '.join(sorted(languages)))
        print("No more languages can be combined.")
        return

    # If only two languages are found
    elif len(languages) == 2:
        lang1, lang2 = languages
        print("\nLanguages found:", ', '.join(sorted(languages)))
        print("Automatically combining these two languages.")

    # If more than two languages are found
    else:
        print("\nLanguages found:", ', '.join(sorted(languages)))
        lang1 = input("Enter the first language to combine: ")
        lang2 = input("Enter the second language to combine: ")

        if lang1 not in languages or lang2 not in languages:
            print("One or both languages not found.")
            return

    # Ask for language positions
    top_lang = input(f"Which language should be on top ({lang1}/{lang2}): ")

    if top_lang not in {lang1, lang2}:
        print("Invalid input.")
        return

    bottom_lang = lang2 if top_lang == lang1 else lang1

    # Preview changes
    print("\nPreview of changes:")
    for base_name, languages in sorted(subtitles.items()):
        if lang1 in languages and lang2 in languages:
            print(f"Combining\t{languages[lang1]}\nwith\t\t{languages[lang2]}\n" + "\033[1m" + f"into\t\t{base_name}.{bottom_lang}-{top_lang}.ass" + "\033[0m" + "\n")

    # Confirm changes
    confirm = input("\nAre these changes correct? (y/n) ")
    if confirm.lower() != 'y':
        print("Aborted.")
        return

    # Process each episode
    output_folder = os.path.join(folder_path, "Combined Subtitles")
    os.makedirs(output_folder, exist_ok=True)  # Create the output directory if it doesn't exist

    for base_name, languages in sorted(subtitles.items()):
        if lang1 in languages and lang2 in languages:
            subs1 = pysubs2.load(os.path.join(folder_path, languages[lang1]))
            subs2 = pysubs2.load(os.path.join(folder_path, languages[lang2]))

            subs = SSAFile()
            subs.styles = {
                top_lang: create_style(top_lang, Alignment.TOP_CENTER),
                bottom_lang: create_style(bottom_lang, Alignment.BOTTOM_CENTER)
            }
            for e in (subs1 if top_lang == lang1 else subs2):
                e.style = top_lang
                subs.append(e)
            for e in (subs1 if top_lang == lang2 else subs2):
                e.style = bottom_lang
                subs.append(e)

            subs.save(os.path.join(output_folder, f"{base_name}.{bottom_lang}-{top_lang}.ass"))
    print("All changes made successfully.")

if __name__ == "__main__":
    combine_subtitles()
