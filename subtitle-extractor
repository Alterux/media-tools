#!/usr/bin/env python3
"""
subtitle-extractor.py

Subtitle Extraction Script

This script extracts subtitle streams from video files in a specified directory. This utility is particularly useful when dealing with multimedia files such as movies or TV series that contain multiple language subtitles. It extracts the desired subtitle languages into separate .srt files for each input video file.

Here is a brief outline of how the script works:

1. The user is prompted to input the path to the directory containing the video files. If the path is left empty, the script uses the current working directory.

2. The script previews the media files found in the specified directory. It handles video files with the following extensions: 'm4v', 'mp4', 'mkv', 'avi'.

3. The user is asked to confirm whether the fetched media files are correct. If not, the script aborts the operation.

4. The script then fetches the available subtitle languages from the video files using ffprobe, which is part of the ffmpeg package. It displays the available languages to the user.

5. The user is asked to input the languages they want to extract. They can either input the language names or their corresponding numbers from the displayed list.

6. The script creates a directory named "Extracted Subtitles" in the specified directory to store the extracted subtitle files.

7. For each video file and selected language, the script extracts the respective subtitle stream using ffmpeg and saves it as an .srt file in the "Extracted Subtitles" directory. The output files are named in the format "basename.language.srt", where "basename" is the name of the original video file and "language" is the ISO 639-1 language code.

8. Upon completion, the script prints a summary of the extracted subtitles, indicating the language, original video file, and output .srt filename for each extracted subtitle.

Note: The script requires ffmpeg to be installed and accessible in the system's PATH. It also uses a mapping from ISO 639-2 to ISO 639-1 language codes for the naming of the output files. If a language is not included in this mapping, the script defaults to using the first two characters of the ISO 639-2 code.
"""


import os
import json
import subprocess
from pathlib import Path

# ISO 639-2 to ISO 639-1 language codes mapping
iso639_mapping = {'eng': 'en', 'jpn': 'ja', 'spa': 'es', 'fre': 'fr', 'deu': 'de', 'ita': 'it', 'dut': 'nl', 'por': 'pt', 'rus': 'ru', 'kor': 'ko', 'chi': 'zh'}

def get_subtitle_streams(filename):
    result = subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', '-select_streams', 's', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return json.loads(result.stdout)

def extract_subtitle(stream, filename, output_filename):
    mapping = stream['index']
    command = ['ffmpeg', '-i', filename, '-map', f'0:{mapping}', '-y', '-nostats', '-loglevel', '0', output_filename]
    subprocess.run(command)

def ask_languages(lang_title_list):
    while True:
        lang_input = input("Enter languages to extract (numbers or names, separated by spaces): ").split()
        languages = [lang_title_list[int(i)-1] if i.isdigit() else i for i in lang_input]
        invalid_inputs = [lang_title for lang_title in languages if lang_title not in lang_title_list]
        if invalid_inputs:
            print(f"Error: {', '.join(invalid_inputs)} is not a valid language. Please try again.")
        else:
            return languages

def extract_subtitles():
    # Ask for directory
    folder_path = input("Enter the path to your folder (enter: current directory): ")
    if not folder_path:
        folder_path = os.getcwd()

    extensions = ['m4v', 'mp4', 'mkv', 'avi']
    video_files = [f for f in Path(folder_path).iterdir() if f.suffix[1:] in extensions]

    # Preview of found media files
    print(f"\nPath: {folder_path}\n")
    print(f"Media files found: {len(video_files)}")
    for i, video_file in enumerate(sorted(video_files), start=1):
        print(f"{i}. {video_file.name}")  # Changed to print only the filename, not the full path

    confirmation = input("\nAre these the correct media files? (y/n): ")
    if confirmation.lower() != 'y':
        print("Aborted.")
        return

    # Fetch subtitle languages
    lang_title_set = set()
    for video_file in video_files:
        streams = get_subtitle_streams(str(video_file))
        for stream in streams['streams']:
            if 'language' in stream['tags']:
                lang = stream['tags']['language']
                title = stream['tags'].get('title', '')
                lang_title_set.add(f"{lang}-{title}" if title else lang)

    print("\nThe following languages were found:")
    lang_title_list = sorted(lang_title_set)
    for i, lang_title in enumerate(lang_title_list, start=1):
        print(f"{i}. Language: {lang_title}")

    languages = ask_languages(lang_title_list)

    output_dir = Path(folder_path) / "Extracted Subtitles"
    output_dir.mkdir(exist_ok=True)

    summary = []

    for video_file in video_files:
        streams = get_subtitle_streams(str(video_file))
        base_name = video_file.stem
        for stream in streams['streams']:
            if 'language' in stream['tags']:
                lang = stream['tags']['language']
                title = stream['tags'].get('title', '')
                lang_title = f"{lang}-{title}" if title else lang
                if lang_title in languages:
                    output_lang = iso639_mapping.get(lang, lang[:2])
                    output_filename = f"{base_name}.{output_lang}.srt"
                    extract_subtitle(stream, str(video_file), str(output_dir / output_filename))
                    summary.append((lang_title, base_name, output_filename))

    print("\nSubtitle extraction complete.\n")
    print(f"Saved {len(summary)} subtitles to {output_dir}/.\n")
    print("Summary:")
    for lang_title, base_name, output_filename in summary:
        print(f"Subtitle '{lang_title}' from '{base_name}'")
        print(f"    -> '{output_filename}'")


if __name__ == "__main__":
    extract_subtitles()
