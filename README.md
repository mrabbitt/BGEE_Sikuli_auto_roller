# BGEE Sikuli Auto Roller

## About

## Prerequisites
To run this script, you need [Sikuli IDE](http://www.sikuli.org).  See  [sikuli.org/download.html](http://www.sikuli.org/download.html) for information and downloads.  This script was developed and tested using *Sikuli X-1.0rc3 (r930)* on Mac OS X 10.8, but will likely work on other platforms.

## Running

### Game Setup
For best results, run *Baldur's Gate: Enhanced Edition* in a window 1024x768.  You can edit the `Baldur.ini` file to set the size explicitly.  `Baldur.ini` is found:

* `~/Documents/Baldur's Gate - Enhanced Edition/Baldur.ini`
* `%USERPROFILE%\MY DOCUMENTS\Baldur's Gate - Enhanced Edition\Baldur.ini` ***(unverified)***

Within the `INSERT INTO options ROWS(...)` section, add or replace the following settings:

    	'Window',	'Full Screen',	'0',
    	'Window',	'w',	'1024',
    	'Window',	'h',	'768',

See [the baldursgate.com forums for more information on customizing your game](http://forum.baldursgate.com/discussion/8317/how-to-manually-customize-your-game).

### Script configuration
* **TODO** Describe `max_interations` and `target_value`.
* **TODO** Describe logging configuration, and make logging easier to configure?
