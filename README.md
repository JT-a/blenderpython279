# blenderpython279
=============

My collection of Blender Addons and User Interface Modifications

[Prebuilt collection for Windows x86_64 (Blender 2.79)]

--

Requirements:
--
* For complete Feature set:
* Blender 2.79 Official Build ONLY!!!!
* blenderpython279 zip, unpacked.

Installation:

* Using Blender 2.79 Zip Version! https://www.blender.org/download/
* Unpack to a location of your choice!
* Browse the folder structure to the \blender-2.79-windows64\2.79 folder.
* Copy/paste the config & scripts folder from blenderpython zip into \blender-2.79-windows64\2.79
* This will overwrite only the files I have updated and add the new folders for addons.

Contents:
* This repo contains many addons and modified Blender ui files.
* All modifications are done via python.

File structure:
* New folders are added for addons:
* addons_custom; I use this folder to put all my paid for addons into.
* addons_extern; I use this folder to put all the addons i collect from the forums and github.
* I acheive access to these folders by modifying the 2.79\scripts\modules\addons_utils.py
* The addons_custom addons show up in user preferences > addons > Community category.
* The addons_extern addons show up in user preferences > addons > Testing category.
* This allows me to copy/paste addons into these folders and keep them organized and easy to keep track of.

User interface Changes:
* These are many and varied and rely heaily upon my startup files.
* There are combinations of ui changes spread across Blender interface files and with the use of addons.
* As your starting with a fresh build of Blender;
* I suggest to use the start up files in the config folder initially;
* then File > load factory settings to view the user interface without the addons enabled.
* There are also modules included here: \2.79\scripts\modules
* The start up i provide is quite busy, it can be easier to disable some addons than try to rebuild. 

# New in the interface
* shorter 3d view menus
* Tabs in the Nkey Properties shelf
* Less Tabs in the Node editor
* Shorter Tab names in the 3d View
* Grease pencil all in 1 Tab in the properties shelf
* new Header content in some editors

# new in Addons
* many small fixes and new addons from the community.
* this repo has less addons than my previous collection but it should be more refined with less duplicates.
* Many addons have been quick fixed to try to make them not error.
* Many addons have had their ui position moved to the new properties shelf tabs.
* if you are grabbing and enabling individual addons from this repo or replacing them with updated versions, you may need to edit the files to move the panel position where you need.


more information to come, Files to follow soon.


