import os
import bpy
import bpy.utils.previews

tptp_preview_icon_collections = {}
tptp_ops_icons_loaded = False

def load_icons():
    global tptp_preview_icon_collections
    global tptp_ops_icons_loaded

    if tptp_ops_icons_loaded: return tptp_preview_icon_collections["main"]

    custom_icons = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__))

    #icons for the panels
    custom_icons.load("Cone_icon", os.path.join(icons_dir, "PL_Cone.png"), 'IMAGE')
    custom_icons.load("Icosphere_icon", os.path.join(icons_dir, "PL_Icosphere.png"), 'IMAGE')
    custom_icons.load("Torus_icon", os.path.join(icons_dir, "PL_Torus.png"), 'IMAGE')

    tptp_preview_icon_collections["main"] = custom_icons
    tptp_ops_icons_loaded = True

    return tptp_preview_icon_collections["main"]

def clear_icons():
	global tptp_icons_loaded

	for icon in tptp_preview_icon_collections.values():
		bpy.utils.previews.remove(icon)

	tptp_preview_icon_collections.clear()
	tptp_ops_icons_loaded = False