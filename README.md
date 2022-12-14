# HomeBadge
A Home Assistant client for the series of event badges supported by the badge.team firmware, which is based on MicroPython. Initial development targets the MCH2022 badge but it can likely be made to work on the others like the HackerHotel badge or the SHA2017 one.

This project relies on the generic Home Assistant client for MicroPython HAPy I publish here: https://github.com/SqyD/hapy

## Current state
This project is at a very early Proof Of Concept stage.

### What it is
* A very rudimentary Home Assistant client for IoT hobby projects .
* A hopefully cool demo of what these badges can do.
* Very feature incomplete. Pull requests are very much welcomed.


### What is it NOT
* Secure: There is no security what so ever. Limited https, no Oauth. Just a HA access token that's stored plain text. Don't use it to IoT-enable your bank vault just yet.
* An easy to use replacement for the wonderful esphome.io project. This is meant for tinker projects. People using this better like messing with (micro)python code.
* Done. Again: Pull requests are welcome!

### What is actually is
Perhaps you could consider this a social experiment to see how many skilled people that should know better will trust the control of their automated homes to a malware and bug infested hardware and software platform that is the event badge universe. In that ecosystem, consider this the bate that other egg developers can leverage for fun and/or profits.

## Installing
Easy: Just use the badge installer to install the "HomeBadge" egg from the Hatchery.
Hack: Take the .py and .json files from this project, add the hapy.py from it's project and place all of the files on the badge using the badge tools.

## Icons
Home Assistant uses the icons from the MaterialDesign project. As the original source has SVG images, I have generated a collection of png files using the icons2png bash file in the tools directory. It relies on Inkscape for the format conversion.

## Authentication
You will need to create and configure a so called "Long-Lived Access Token".
* Log into your Home Assistance instance.
* Go to your Profile page, at /profile or at the bottom of your sidebar.
* Click the "Create Token" at the bottom.
* Copy the key to your clipboard.
* Connect to the builtin python shell.
* Insert your Home Assistant url ("http://192.168.1.23") and token to these commands:
```
import nvs, ujson
secrets = {"url": "your_home_assistant_url", "access_token": "AABBCC112233"}
nvs.nvs_setstr('homebadge', 'secrets', ujson.dumps(secrets))
```

* This project as an Egg in the badge.team Hatchery: https://mch2022.badge.team/projects/homebadge
* This project on Github: https://github.com/SqyD/homebadge
* The generic Home Assistant client for MicroPython: https://github.com/SqyD/hapy
* The MaterialDesign icon set: https://materialdesignicons.com/
* Home Assistant: https://www.home-assistant.io/
