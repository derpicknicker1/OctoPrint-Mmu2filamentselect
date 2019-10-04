# OctoPrint-Mmu2filamentselect

<img src="https://raw.githubusercontent.com/derpicknicker1/OctoPrint-Mmu2filamentselect/pics/octoprusa.png" width="25%" align="left"> 

This plugin shows a dialog to select the filament when a print on a Prusa printer with MMU2 is startet in single mode.

You can select the filament which should be used in this dialog. So you don't have to go over to your printer to select the filament in the printers menu.

The dialog will timeout after a given time (see [Configuration](configuration), default 30 seconds). Then everything will work as usual and you have to select the filament at your printers menu.

<img src="https://raw.githubusercontent.com/derpicknicker1/OctoPrint-Mmu2filamentselect/pics/dialog.png"> 

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/derPicknicker1/OctoPrint-Mmu2filamentselect/archive/master.zip

## Configuration

In the settings of this plugin you can set the timeout. If this timeout runs out after the dialog pops up, it will close the dialog automatically. 

<img src="https://raw.githubusercontent.com/derpicknicker1/OctoPrint-Mmu2filamentselect/pics/settings2.png"> 
