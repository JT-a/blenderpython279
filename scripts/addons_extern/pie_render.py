bl_info = {
    "name": "Render Pie menu",
    "author": "TARDIS Maker",
    "version": (0, 0, 0),
    "blender": (2, 72, 2),
    "description": "A pie menu for render. It gives the options between Render still, Render Animation, OpenGL Render Still, OpenGL Render Animation.",
    "location": "Hotkey: F12",
    "category": "Pie Menu"}

import bpy
from bpy.types import Menu


##################
# Pie Menu Class #
##################
class RenderPieMenu(Menu):
    bl_idname = "pie.render"
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("render.render", text="Render", icon="RENDER_STILL")
        pie.operator("render.render", text="Render Animation", icon="RENDER_ANIMATION").animation = True
        pie.operator("render.opengl", text="OpenGL Render", icon="RENDER_STILL")
        pie.operator("render.opengl", text="OpenGL Render Animation", icon="RENDER_ANIMATION").animation = True


########################
# REGISTER/UNREGISTER  #
########################
addon_keymaps = []


def register():
    bpy.utils.register_class(RenderPieMenu)

    # Keymap #
    wm = bpy.context.window_manager  # convienience variable

    km = wm.keyconfigs.addon.keymaps.new(name="Screen")
    kmi = km.keymap_items.new("wm.call_menu_pie", "F12", "PRESS")
    kmi.properties.name = "pie.render"
    addon_keymaps.append(km)


def unregister():
    bpy.utils.unregister_class(RenderPieMenu)
    wm = bpy.context.window_manager

    # Keymap #
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)

    wm.keyconfigs.addon.keymaps.remove(km)

    # clear the list
    del addon_keymaps[:]

if __name__ == "__main__":
    register()
