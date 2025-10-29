"""
Premise, starting situation: There are three or more folders
in a folder that is like "Hachette FLE" or "MondesEnVF," whatever.

It's a folder of audiobooks.

Problem statement: You don't have .SRT files so you can't do interactive
immersion with these audiobooks!

Solution statement: Have a script 
1. walk through the folders,
2. Run WhisperX on every .wav file it finds,
3. producing a .srt file with exactly the same filename
4. in the same dir.

Note that 5. the intermediate files should all be cleaned up and
6. the original .wav and .mp3 must be preserved.
"""
import sys
import os

import glob
from typing import List, Dict, Tuple

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.whisperx_commands import WhisperXCommandMaker

from src.colorsPrinter import colored_print_info_type

from src.command_runner import CommandRunner

ALLOWED_EXTS = {".wav", ".srt", ".mp3"}

def find_all_subfolders(starting_dir: str) -> List[str]:
    """
    Return a list of immediate subfolders under starting_dir.
    (No recursion; exactly one level down.)
    """
    if not os.path.isdir(starting_dir):
        raise ValueError(f"Starting directory does not exist: {starting_dir}")

    subfolders = []
    with os.scandir(starting_dir) as it:
        for entry in it:
            if entry.is_dir():
                subfolders.append(entry.path)
    # Sort for stable, predictable processing order
    subfolders.sort()
    return subfolders


def make_subfolder_groupings(subfolders: List[str]) -> Dict[str, List[str]]:
    """
    Given a list of folder paths, return a mapping:
        folder_path -> sorted list of *.wav and *.mp3 files (full paths)
    Only includes folders that contain at least one .wav or .mp3.
    """
    files_by_folder: Dict[str, List[str]] = {}
    for folder in subfolders:
        wavs = glob.glob(os.path.join(folder, "*.wav"))
        mp3s = glob.glob(os.path.join(folder, "*.mp3"))
        audio_files = sorted(wavs + mp3s)
        if audio_files:  # only include folders that actually have audio files
            files_by_folder[folder] = audio_files
    return files_by_folder


def clean_intermediates(folder: str) -> int:
    """
    Delete every intermediate artifact in `folder`, preserving only:
      - *.wav
      - *.mp3
      - *.srt

    Removes any other files.
    Returns (files_deleted, dirs_deleted).
    """
    files_deleted = 0

    with os.scandir(folder) as it:
        for entry in it:
            try:
                if entry.is_file():
                    _, ext = os.path.splitext(entry.name)
                    if ext.lower() not in ALLOWED_EXTS:
                        os.remove(entry.path)
                        files_deleted += 1
            except Exception as e:
                # Non-fatal: continue cleaning the rest
                print(f"[clean_intermediates] Skipped {entry.path}: {e}")

    return files_deleted


def main():
    # =================================================================
    # CONFIGURATION - EDIT THIS SECTION
    # =================================================================

    starting_dir = ""

    """
    Remember that this walks thru the parent dir down 
    to look for .wavs and .mp3s to make into .SRTs
    """
    
    # =================================================================
    # END CONFIGURATION
    # =================================================================


    # TODO: Make the initiation tell you "Hey we found <folder list> with <count per folder>"
    all_subfolders = find_all_subfolders(starting_dir)
    if len(all_subfolders) == 0:
        raise ValueError("Expected to find folders")
    files_by_folder = make_subfolder_groupings(all_subfolders)
    total_count = sum(len(v) for v in files_by_folder.values())
                      
    # Process each episode
    successful_files = []
    failed_files = []

    for folder, wav_files in files_by_folder.items():
        print("Changing to folder: ", folder)
        os.chdir(folder)
        for wav_filename in wav_files:
            # Build command (assumes it overwrites existing .srt)
            whisperx_transcript_command = WhisperXCommandMaker.make_jnatasgrosman_whisperx_command(
                wav_filename
            )

            colored_print_info_type("[Converter] ", 1, f"Generating subtitles for: {wav_filename}")
            ok = CommandRunner.run_command(
                whisperx_transcript_command,
                "Generating subtitles with whisperx"
            )

            # Track results
            if ok:
                successful_files.append(wav_filename)
                # OPTIONAL: clean intermediates in `folder`, keeping only the .wav and .srt
                # clean_intermediates(folder, keep=set([wav_filename, os.path.splitext(wav_filename)[0] + ".srt"]))
            else:
                failed_files.append(("", wav_filename))  # ep_num unknown in this context

        f_del = clean_intermediates(folder)
        colored_print_info_type(
            "[Cleaner] ", 1, f"Cleaned {folder}: removed {f_del} files"
        )
    
    # Reset folder
    os.chdir(starting_dir)

    # Summary
    print(f"\n{'='*80}")
    print("PROCESSING SUMMARY")
    print(f"{'='*80}")
    print(f"Successful episodes: {successful_files}")
    if failed_files:
        print(f"Failed episodes:")
        for ep_num, filename in failed_files:
            print(f"  Episode {ep_num}: {filename}")
    else:
        print("All episodes processed successfully!")
    
    print(f"\nTotal processed: {len(successful_files)}/{total_count}")


if __name__ == "__main__":
    main()