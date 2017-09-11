
# Help Menu

import bpy
import zipfile, urllib.request, os, sys, re
import csv
import collections
import subprocess
try:
	import winreg
except:
	pass

################
# Update Function
################
class Info_MT_cookie_links(bpy.types.Menu):
    # Define the "Extras" menu
	bl_idname = "Info_MT_cookie_links"
	bl_label = "CG Cookie Links"

	def draw(self, context):
		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'

		layout.operator("wm.url_open", text="CG Cookie.com", icon='URL').url = "https://cgcookie.com/"
		layout.operator("wm.url_open", text="CG Cookie Tutorials", icon='URL').url = "https://cgcookie.com/learn-blender/"
		layout.operator("wm.url_open", text="Blender Artists Forum", icon='URL').url = "http://blenderartists.org/forum/index.php"
		layout.operator("wm.url_open", text="Blender Market", icon='URL').url = "https://cgcookiemarkets.com/blender/"

def menu_func(self, context):
	layout = self.layout
	self.layout.separator()

	self.layout.menu(Info_MT_cookie_links.bl_idname, icon="URL")


class UpdateScrambleAddon(bpy.types.Operator):
	bl_idname = "script.update_scramble_addon"
	bl_label = "Blender-Scramble-Addon Upddate"
	bl_description = "Blender-Scramble-Addon"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
#		response = urllib.request.urlopen("https://github.com/saidenka/Blender-Scramble-Addon/archive/master.zip")
		tempDir = bpy.app.tempdir
		zipPath = os.path.join(tempDir, "Blender-Scramble-Addon-master.zip")
		addonDir = os.path.dirname(__file__)
		f = open(zipPath, "wb")
		f.write(response.read())
		f.close()
		zf = zipfile.ZipFile(zipPath, "r")
		for f in zf.namelist():
			if not os.path.basename(f):
				pass
			else:
				if ("Addon_Factory" in f):
					uzf = open(os.path.join(addonDir, os.path.basename(f)), 'wb')
					uzf.write(zf.read(f))
					uzf.close()
		zf.close()
		self.report(type={"INFO"}, message="It has been updated add-on, restart the Blender")
		return {'FINISHED'}

class ToggleDisabledMenu(bpy.types.Operator):
	bl_idname = "wm.toggle_disabled_menu"
	bl_label = "Display switching of additional items of on / off"
	bl_description = "I will switch the display / non-display of additional items of on / off button at the end of the menu by ScrambleAddon"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu = not context.user_preferences.addons["Addon_Factory"].preferences.use_disabled_menu
		return {'FINISHED'}

def menu(self, context):

	layout = self.layout
	self.layout.separator()
#		self.layout.operator(UpdateScrambleAddon.bl_idname, icon="PLUGIN")
	layout.operator("wm.url_open", text="Ask Olson", icon='HELP').url = "http://www.getblended.org/"

