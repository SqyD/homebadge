# HomeBadge
A Home Assistant client for the series of event badges supported by the badge.team firmware, which is based on MicroPython. Initial development targets the MCH2022 badge but it can likely be made to work on the others like the HackerHotel badge or the SHA2017 one.

This project relies on the generic Home Assistant client for MicroPython HAPy I publish here: https://github.com/SqyD/hapy

## Current state
This project is at a very early Proof Of Concept stage.

### What it is
* A very rudimentary Home Assistant client for IoT hobby projects.
* A cool demo of what these badges can do.
* Very feature incomplete. Pull requests are very much welcomed.


### What is it NOT
* Secure: There is no security what so ever. No HTTPS, no Oauth. Just a HA access token that's stored plain text. Don't use it to IoT-enable your bank vault just yet.
* An easy to use replacement for the wonderful esphome.io project. This is meant for tinker projects. People using this better like messing with (micro)python code.
* Done. Again: Pull requests are welcome!

## Installing
Easypeasy: Just use the badge installer to install the "HomeBadge" egg from the Hatchery.
Hack: Take the .py and .json files from this project, add the upyhome.py from it's project and place all of the files on the badge using mpftool in /lib/homebadge/ on the badge.

This project as an Egg in the badge.team Hatchery: https://badge.team/projects/homebadge
This project on Github: https://github.com/SqyD/homebadge
The generic Home Assistant client for MicroPython: https://github.com/SqyD/hapy
Home Assistant: https://www.home-assistant.io/
