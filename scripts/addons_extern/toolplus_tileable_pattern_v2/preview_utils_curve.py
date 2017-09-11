import bpy, os

from os import listdir
from os.path import isfile, join

from . tp_insert_curve import tp_insert_curve_geometry



######################################################




preview_collections = {}

def enum_previews_from_directory_items(self, context):
    """EnumProperty callback"""
    enum_items = []
 
    if context is None:
        return enum_items
   
    directory = join(os.path.dirname(__file__), "icons", "insert_curve_icons") #insert_icons > icons sub folder
    
    # Get the preview collection (defined in register func).
    pcoll = preview_collections["main"]
 
    if directory == pcoll.TP_Tileable_Curve_Previews_dir:
        return pcoll.TP_Tileable_Curve_Previews
 
    print("Scanning directory: %s" % directory)
  
    if directory and os.path.exists(directory):
        # Scan the directory for png files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".png"):
                image_paths.append(fn)
 
        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            thumb = pcoll.load(filepath, filepath, 'IMAGE')
            enum_items.append((name, name, "", thumb.icon_id, i))
            
    pcoll.TP_Tileable_Curve_Previews = enum_items 
    pcoll.TP_Tileable_Curve_Previews_dir = directory
 
    return pcoll.TP_Tileable_Curve_Previews
 

######################################################

 
def register_TP_Tileable_Curve_pcoll(): 
    from bpy.types import WindowManager
    from bpy.props import (EnumProperty, BoolProperty)

     
    WindowManager.TP_Tileable_Curve_Previews = EnumProperty(items=enum_previews_from_directory_items, update=tp_insert_curve_geometry)
  
    import bpy.utils.previews
    #wm = bpy.context.window_manager
    pcoll = bpy.utils.previews.new()

    pcoll.TP_Tileable_Curve_Previews_dir = ""
    pcoll.TP_Tileable_Curve_Previews = ()
 
    preview_collections["main"] = pcoll
 
 
def unregister_TP_Tileable_Curve_pcoll():    
    from bpy.types import WindowManager

 
    del WindowManager.TP_Tileable_Curve_Previews
 
    for pcoll in preview_collections.values():       
        bpy.utils.previews.remove(pcoll)
   
    preview_collections.clear()



