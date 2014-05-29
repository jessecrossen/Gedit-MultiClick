Gedit-MultiClick
================

A plugin for gedit 3+ that improves the functionality of double and triple clicks such that useful keywords and chains of keywords can be selected. It's fairly similar to [gedit-click-config](https://code.google.com/p/gedit-click-config/), except that it's simpler, has less features, and can't be configured. Without plugins, double-clicking in gedit will select the word but will not select across an underscore ("\_") and triple-clicking has no effect. This fixes that and adds a bit more as well, allowing triple-clicks to select keyword chains like "Gdk.EventType.\_3BUTTON\_PRESS".

Installing
==========

By cloning the repo:

    $ git clone https://github.com/jessecrossen/Gedit-MultiClick.git
    $ cd Gedit-MultiClick
    $ ./install.sh
    
Or by unpacking a snapshot if don't want to use git:

    $ wget https://github.com/jessecrossen/Gedit-MultiClick/archive/master.zip
    $ unzip master.zip
    $ cd Gedit-MultiClick-master
    $ ./install.sh

Then restart gedit from the console and enable the MultiClick plugin in the preferences dialog. If you see something like this in your console output:

    (gedit:4579): libpeas-WARNING **: Could not find loader 'python3' for plugin 'multiclick'
    
...then you're probably running a version of gedit earlier than 3.12 that only supports Python 3.  Edit the second line of multicursor.plugin to read as follows:

    Loader=python
    
Then re-run install.sh and try again from there.

Usage
=====

Double-click a keyword to select it. A keyword is defined as any contiguous run of alphanumeric characters and underscores, potentially containing internal dashes as well to support CSS class names and such. Triple clicking will select a chain of keywords, defined as any contiguous run of keywords separated by the common operators "->", "::", and "." as well as forward and backward slashes for paths and "@" for emails. I didn't put a whole lot of thought into these definitions, so feel free to suggest improvements. Good matching of URLs would be handy, for instance.
