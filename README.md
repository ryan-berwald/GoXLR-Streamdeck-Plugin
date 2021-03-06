# StreamDeck Emulator
A hotkey listener written in Python that sends a request to a webhook running on Node.JS that will change your GoXLR profile based on your provided configuration.

- Define hotkeys and profiles
- Press hotkey
- Watch your profile change!

## Features

- Launches a Webhook server that listens for commands
- User defined profile changes and hotkeys
- Globally listens for hotkeys, even while _gaming_

## Purpose
The purpose for this project was to allow manipulation of my GoXLR mini profiles on the fly while in a game using my MacroPad. Having to Alt-Tab out of my games while mid-match to manipulate volume on certain channels, reassign routes, or change volume on unbound channels was too time consuming, so I created this to do it all for me. 

## Languages

- Node.JS - Used for webhook server that receives a message, and transmits it through a seperate webhook server to the GoXLR
- Python
    -  Keyboard Library - Used to hook into the OS to define and listen for hotkeys
    -  WS Library - Runs the webhook client that transmits a message consisting of "changeprofile=PROFILE" to change your profile or "fetchprofiles=" to get available profiles

## Installation

- Clone repo
- Npm install
- pip install requirements.txt
- run "Python client.py" from cmd, powershell, or bash


## ToDo
Working on creating executable for future release



  
