# Perl POD for Sublime Text 2/3

[![Build Status](https://secure.travis-ci.org/vifo/SublimePerlPod.png)](http://travis-ci.org/vifo/SublimePerlPod)

This is a plugin for [Sublime Text 2](http://www.sublimetext.com/) and [Sublime Text 3](http://www.sublimetext.com/3), which allows validation and preview of [Perl POD (plain old documentation)]() in Sublime Text.

## Quick start

* Install this plugin in Sublime Text via Package Control, git or from ZIP
* Bring up the Command Palette (`Control+Shift+P` or `Command+Shift+P`), start typing "Perl POD" and choose action

Read on for detailed installation, usage, configuration and customization instructions.

## Installation

**Note**: Installation through Package Control is not available yet, since plugin has not been published yet.

* **With Sublime Package Control:** The easiest way to install Perl POD is through [Sublime Package Control](http://wbond.net/sublime_packages/package_control). If you're not using it yet, get it. Seriously.

  Once you have installed Package Control, restart Sublime Text and bring up the Command Palette (press `Control+Shift+P` on Linux/Windows, `Command+Shift+P` on OS X, or select `Tools->Command Palette...` from menu). Select *Package Control: Install Package*, wait till latest package list has been fetched, then select `Perl POD` from the list of available packages.

* **With Git:** Clone the repository in your Sublime Text *Packages* directory. Please note that the destination directory must be `PerlPod`.

        git clone https://github.com/vifo/SublimePerlPod PerlPod

The advantage of using either Package Control or git is, that the plugin will be automatically kept up-to-date with the latest version.

* **From ZIP:** Download the latest version [as a ZIP archive](https://github.com/vifo/SublimePerlPod/archive/master.zip) and copy the directory `SublimePerlPod-master` from the archive to your Sublime Text *Packages* directory. Rename directory `SublimePerlPod-master` to `PerlPod`.

The *Packages* directory locations are listed below. If using Sublime Text 3, be sure to replace "2" with "3" in directory names.  Alternatively, selecting `Preferences->Browse Packages...` from Sublime Text menu will get you to the *Packages* directory also.

| OS            | Packages location                                         |
| ------------- | --------------------------------------------------------- |
| OS X          | `~/Library/Application Support/Sublime Text 2/Packages/`  |
| Linux         | `~/.config/sublime-text-2/Packages/`                      |
| Windows       | `%APPDATA%\Sublime Text 2\Packages\`                      |

## Usage

After Perl POD installation, open a Perl file of your choice and open Command Palette. Start typing "Perl POD"", choose desired action and hit return.

## Configuration

Until a detailed explanation of all possible configuration options is available, please check comments in the default settings (select `Preferences->Package Settings->Perl POD->Settings - Default`)

### Key bindings

None by default.

## Reporting bugs

In order to make bug hunting easier, please ensure, that you always run the **latest** version of Perl POD. Apart from this, please ensure, that you've set Perl POD log level to maximum (`"log_level": "trace"` in user settings), in order to get all debugging information possible. Also please include the following information, when submitting an issue:

* Operating system name (i.e. "Windows XP SP3", **not** "Windows")

* Operating system architecture (i.e. 32-bit, 64-bit)

* Sublime Text build number (open `Help->About`)

* Output from Sublime Text console

To gather this information quickly, open ST console, type in the following Python code as-is (in one line) and include its output in your issue:

```python
from __future__ import print_function, unicode_literals;import platform, sublime, datetime;print('-' * 78);print('Date/time: {0}'.format(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000')));print('Sublime Text version: {0}'.format(sublime.version()));print('Platform: {0}'.format(sublime.platform()));print('CPU architecture: {0}'.format(sublime.arch()));print('OS info: {0}'.format(repr(platform.platform())));print('-' * 78)
```

## Changes

Only latest changes are listed here. Refer to [full change log](https://github.com/vifo/SublimePerlPod/blob/master/CHANGES.md) for all changes.

### v0.1.0 - 2013-06-27 20:00:00 +0200

* Initial release.
