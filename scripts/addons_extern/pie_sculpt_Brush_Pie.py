bl_info = {
    "name": "Sculpt Brush Pie Menu",
    "author": "TARDIS Maker",
    "version": (0, 0, 0),
    "blender": (2, 72, 2),
    "description": "A pie menu for selecting the sculpt brush",
    "location": "Hotkey: B",
    "category": "Pie Menu"}

import bpy
from bpy.types import Menu


# SCULPT BRUSH CUSTOM OPERATORS #


# Clay #
class Clay_Brush(bpy.types.Operator):
    bl_idname = "sculpt_brush.clay"
    bl_label = "Clay Brush"

    def execute(self, context):
        bpy.context.tool_settings.sculpt.brush = bpy.data.brushes['Clay']
        return {'FINISHED'}


# Clay Strips Brush #
class Clay_Strips_Brush(bpy.types.Operator):
    bl_idname = "sculpt_brush.clay_strips"
    bl_label = "Clay Strips Brush"

    def execute(self, context):
        bpy.context.tool_settings.sculpt.brush = bpy.data.brushes['Clay Strips']
        return {'FINISHED'}


# Snake Hook Brush #
class Snake_Hook_Brush(bpy.types.Operator):
    bl_idname = "sculpt_brush.snake_hook"
    bl_label = "Snake Hook Brush"

    def execute(self, context):
        bpy.context.tool_settings.sculpt.brush = bpy.data.brushes['Snake Hook']
        return {'FINISHED'}


# Scrape Brush #
class Scrape_Brush(bpy.types.Operator):
    bl_idname = "sculpt_brush.scrape"
    bl_label = "Scrape Brush"

    def execute(self, context):
        bpy.context.tool_settings.sculpt.brush = bpy.data.brushes['Scrape/Peaks']
        return {'FINISHED'}


# Crease Brush #
class Crease_Brush(bpy.types.Operator):
    bl_idname = "sculpt_brush.crease"
    bl_label = "Crease Brush"

    def execute(self, context):
        bpy.context.tool_settings.sculpt.brush = bpy.data.brushes['Crease']
        return {'FINISHED'}


# Smooth Brush #
class Smooth_Brush(bpy.types.Operator):
    bl_idname = "sculpt_brush.smooth"
    bl_label = "Smooth Brush"

    def execute(self, context):
        bpy.context.tool_settings.sculpt.brush = bpy.data.brushes['Smooth']
        return {'FINISHED'}


# Inflate Brush #
class Inflate_Brush(bpy.types.Operator):
    bl_idname = "sculpt_brush.inflate"
    bl_label = "Inflate Brush"

    def execute(self, context):
        bpy.context.tool_settings.sculpt.brush = bpy.data.brushes['Inflate/Deflate']
        return {'FINISHED'}


# PIE MENU DEFINITION #

# Main Pie Menu #
class VIEW3D_PIE_sculpt_brush(Menu):
    bl_idname = "sculpt.brush.main_pie"
    bl_label = "Sculpt Brush"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("sculpt_brush.clay", text="Clay", icon="BRUSH_CLAY")
        pie.operator("sculpt_brush.clay_strips", text="Clay Strips", icon="BRUSH_CLAY_STRIPS")
        pie.operator("sculpt_brush.snake_hook", text="Snake Hook", icon="BRUSH_SNAKE_HOOK")
        pie.operator("sculpt_brush.scrape", text="Scrape", icon="BRUSH_SCRAPE")
        pie.operator("sculpt_brush.crease", text="Crease", icon="BRUSH_CREASE")
        pie.operator("sculpt_brush.smooth", text="Smooth", icon="BRUSH_SMOOTH")
        pie.operator("sculpt_brush.inflate", text="Inflate", icon="BRUSH_INFLATE")
        # pie.operator("wm.call_menu_pie", text="Other", icon="PLUS").name = "sculpt.brush.other"


# REGISTER/UNREGISTER #
addon_keymaps = []


def register():
    # Pie Menu Class #
    bpy.utils.register_class(VIEW3D_PIE_sculpt_brush)
    bpy.utils.register_class(Clay_Brush)
    bpy.utils.register_class(Clay_Strips_Brush)
    bpy.utils.register_class(Snake_Hook_Brush)
    bpy.utils.register_class(Scrape_Brush)
    bpy.utils.register_class(Crease_Brush)
    bpy.utils.register_class(Inflate_Brush)
    bpy.utils.register_class(Smooth_Brush)

    # Key Map #
    wm = bpy.context.window_manager  # convienience variable

    km = wm.keyconfigs.addon.keymaps.new(name="Sculpt")
    kmi = km.keymap_items.new("wm.call_menu_pie", "B", "PRESS")
    kmi.properties.name = "sculpt.brush.main_pie"
    addon_keymaps.append(km)


def unregister():
    # Pie Menu Class #
    bpy.utils.unregister_class(VIEW3D_PIE_sculpt_brush)
    bpy.utils.unregister_class(Clay_Brush)
    bpy.utils.unregister_class(Clay_Strips_Brush)
    bpy.utils.unregister_class(Snake_Hook_Brush)
    bpy.utils.unregister_class(Scrape_Brush)
    bpy.utils.register_class(Crease_Brush)
    bpy.utils.register_class(Inflate_Brush)
    bpy.utils.register_class(Smooth_Brush)

    # Get Rid of the Key Map #
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)

    wm = bpy.context.window_manager
    wm.keyconfigs.addon.keymaps.remove(km)

    # clear the list
    del addon_keymaps[:]

if __name__ == "__main__":
    register()

    # bpy.ops.wm.call_menu_pie(name="VIEW3D_PIE_sculpt_brush")
