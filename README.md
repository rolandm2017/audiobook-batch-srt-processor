# A WhisperX batch processor for audiobook content

This repo aims to help language learners process large batches of audiobook files into .SRT files.

*Be sure to read the **warning** at the bottom of the Readme before using the script. **Back up your folder before using the script.***

The .srt files will enable *interactive immersion* using LanguageReactor.

That is, with the .srt file made, you can upload the audiobook .mp3/.wav file, along with the .srt file, to LanguageReactor's media tab. Then, you can interactively read while listening to the audiobook, or interactively listen.

## How to use

### Configuring the script

- starting_dir in audiobooks.queue.py is the parent folder of all your audiobooks.

- You must modify whisperx_commands.py to contain the right configuration for your language of choice.

### Steps to run the script

The way I run it on my computer is that I change "starting_dir" in audiobooks.queue.py to point to a folder that contains my audiobook file folders.

Said another way, I expect that you keep all your audiobooks in the same folder; just a bunch of folders containing *solely, only* mp3 or .wav files.

You run this script pointed at the parent folder; it will walk through all the folders, processing them with WhisperX.

## ** WARNING ** 

1. You should BACK UP the whole folder you're going to run this on before using it.

2. *It will DELETE all files in the folders that ARE NOT .mp3, .wav, .srt after it's done!*

To modify this behavior, see the variable:

ALLOWED_EXTS = {".wav", ".srt", ".mp3"}

around line 34 of audiobooks.queue.py. To mark a file type as "safe," "to keep," you add in the extension to that list of endings.