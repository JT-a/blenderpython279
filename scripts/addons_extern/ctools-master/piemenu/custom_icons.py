import os

import bpy

preview_collections = {}


def register():
    pcoll = bpy.utils.previews.new()

    dirname = os.path.join(os.path.dirname(__file__), "icons")
    for i in range(16):
        pcoll.load(str(i), os.path.join(dirname, str(i) + ".png"), 'IMAGE')
    pcoll.load("empty", os.path.join(dirname, "empty.png"), 'IMAGE')

    preview_collections["main"] = pcoll


def unregister():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
