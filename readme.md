# Rhus Keeti Discord Bot

One of my best friends asked me to help him build a bot to authenticate the members of his camp. They're using discord to separate all the members and their roles, and have specific announcement channels for communication.

## Pre-requisites

python 3.9

probably a dedicated/virtual host, unless you want to host it permanently locally. The client must be active in CMD for the bot to work.

## Installation

You are more than welcome to set up a python virtual environment.

`pip3 install discord`

`pip3 install openpyxl`

## Usage

`py -3 main.py`

This will open the client in CMD, and communciate with the bot until the client is closed.

## How it works

Currently the bot is configured to only work on the one server, so it makes things easier. We also know which channels are currnetly available, and we have a set up list of roles.
Once the bot connects to the server, it does some configuration, then listens for webhook requests, such as when a member joins/leaves and when a message is sent/received.

Thus when a member joins, a welcome message is sent privately to the new member. If they reply incorrectly, they're asked again. If they reply correctly, they're welcomed, and their roles on the server are added.

Info is sent to the system channel (a channel that only administrators/IT Support can see)

the command `$whois` will give a list of people who have no roles on the server yet.