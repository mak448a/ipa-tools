# IPA tools for Godot Engine

A multipurpose IPA editor/builder for people who don't own Macs!

Ever wanted to stop hopping between your Mac and Windows/Linux PCs when developing an iOS Project? This is the project for you!

Features:
- Editor to update IPA without rebuilding!
- Builder that pushes to GitHub actions for building!


> [!WARNING]  
> I am not responsible for data loss, but I try my best to keep the script safe.
> This is currently under construction!! Do not expect stability!


## Requirements
- gh CLI
- git

## Usage
Do the standard `python3 -m venv venv`
`source venv/bin/activate`
`python3 main.py`.

Check the tutorial directory out for screenshots of getting your Dropbox API key.
Visit https://www.dropbox.com/developers/apps to get your key.

I should probably put this in the readme, but I'm trying to get this out quickly.

## Privacy Policy
I don't collect any data.
This project uses GitHub and Dropbox. See the privacy policies for these services for more information.

If you get an `AuthError('expired_access_token', None))`, that means that you need to get a new OAuth token from Dropbox.


Started work on this project ~11/2024.