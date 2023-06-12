#!/usr/bin/env python3
"""
episode-renamer.py

File Renaming Script

This script is designed to aid in the renaming of files in two directories based on a matching pattern. This script is particularly useful for managing files such as TV shows or other media where season and episode information can be extracted from the filename.

This script extracts season and episode numbers from the filenames in the first directory and then matches them with the corresponding files in the second directory. If a match is found and the file types are the same, the file in the second directory will be renamed to the name of the file in the first directory. 

Here is a brief outline of how the script works:

1. The user is asked to input the paths of the two directories to be processed. If the path for the first directory is left empty, the script uses the current working directory.

2. The script previews the contents of both directories to the user, allowing them to confirm whether they want to proceed.

3. The script then iterates over each pair of files (sorted alphabetically) in the two directories. It attempts to extract season and episode numbers from each pair of filenames using a regular expression pattern (in the format 's#e#', where # represents any digit). 

4. If the season and episode numbers from both files match and the files have the same file type (e.g., both are .mp4 files), the file in the second directory is prepared to be renamed to match the filename in the first directory. 

5. The user is presented with a preview of the changes and can choose to either proceed with the renaming or cancel the operation.

6. If the user chooses to proceed, the files in the second directory are renamed, and a summary of the changes is written to a text file in the same directory.

The script is designed to handle video files and recognizes the following extensions: 'm4v', 'mp4', 'mkv', 'avi'.

Please note: the script will halt and cancel the operation if it encounters a pair of files where the season/episode numbers or file types do not match.
"""


import os
import re
from pathlib import Path

# Function to extract season and episode numbers from a string
def extract_season_episode(s):
    match = re.search(r's(\d+)e(\d+)', s.lower())
    if match:
        return match.group(1), match.group(2)
    return None, None

def rename_files():
    # Prompt user for directories
    dir1 = input("Enter the path of directory 1 (press enter for current directory): ")
    dir1 = dir1 or os.getcwd()
    dir2 = input("Enter the path of directory 2: ")

    # Preview directories
    print("Directory 1:", dir1)
    print("Directory 2:", dir2)

    # Confirm directories
    confirmation = input("Are these directories correct? (y/n): ")
    if confirmation.lower() != "y":
        print("Operation cancelled.")
        return

    # Get sorted file lists from both directories
    extensions = ['m4v', 'mp4', 'mkv', 'avi']
    files1 = sorted([f for f in Path(dir1).iterdir() if f.suffix[1:] in extensions])
    files2 = sorted([f for f in Path(dir2).iterdir() if f.suffix[1:] in extensions])
    changes = []

    # Preview files
    print("Files:")
    print(f"{dir1}: found {len(files1)} files")
    for i, video_file in enumerate(files1, start=1):
        print(f"{i}. {video_file.name}")  # Changed to print only the filename, not the full path
    print(f"{dir2}: found {len(files2)} files")
    for i, video_file in enumerate(files2, start=1):
        print(f"{i}. {video_file.name}")  # Changed to print only the filename, not the full path

    # Confirm files
    confirmation = input("Are these files correct? (y/n): ")
    if confirmation.lower() != "y":
        print("Operation cancelled.")
        return

    # Iterate over pairs of files
    for file1, file2 in zip(files1, files2):
        # Extract season and episode numbers
        s1, e1 = extract_season_episode(str(file1))
        s2, e2 = extract_season_episode(str(file2))

        # Check if extracted numbers match and files are of the same type
        if s1 == s2 and e1 == e2 and file1.suffix == file2.suffix:
            changes.append((str(Path(dir2) / file2.name), str(Path(dir2) / file1.name)))
        else:
            print(f"File mismatch: \n{file1}\n{file2}\nAborting.")
            return

    # Preview changes
    print("Preview of changes:")
    for old, new in changes:
        print(f"{old} \n-> {new}")

    # Confirm changes
    confirmation = input("Do you want to execute these changes? (y/n): ")
    if confirmation.lower() != "y":
        print("Operation cancelled.")
        return

    # Execute changes and write summary to file
    with open(Path(dir2) / 'Rename Summary.txt', 'w') as summary_file:
        for old, new in changes:
            os.rename(old, new)
            summary_file.write(f"Renamed: {os.path.basename(old)} -> {os.path.basename(new)}\n")

    print("Files renamed successfully and summary written to summary.txt.")

# Start the renaming operation
rename_files()
