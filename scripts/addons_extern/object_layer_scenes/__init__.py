bl_info = {
    "name": "SceneLayers",
    "author": "Gertjan Van den Broek",
    "version": (0, 6),
    "blender": (2, 7, 4),
    "location": "Properties, scenes",
    "description": "A CAD style layer system based on entire blender scenes instead of object visibility.",
    "wiki_url": ""
                "",
    "tracker_url": ""
                   "",
    "support": 'COMMUNITY',
    "category": "Scene"}
print("------------------")
print("Loading Scene Layers:")

if "bpy" in locals():
	print("Reloading")
	import imp
	imp.reload(layer_scene_main)
	imp.reload(layer_scene_ui)
	imp.reload(layer_scene_utils)
else:
	print("Reloading")
	from . import layer_scene_main
	from . import layer_scene_ui
	from . import layer_scene_utils

import bpy
import os



def register():
	bpy.utils.register_module(__name__);
	layer_scene_main.register()


def unregister():
    bpy.utils.unregister_module(__name__);



if __name__ == "__main__":
    register()
	
print("Finished!")
print("------------------")