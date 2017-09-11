"""Use pie menus for proportional editing and falloff selection."""

bl_info = {
    "name": "Proportional Edit Pies",
    "author": "italic",
    "version": (1, 0, 0),
    "blender": (2, 77, 0),
    "description": "Uses pie menus for proportional edit toggling and falloff selection.",
    "location": "Hotkey: O, SHIFT + O (\"Oh,\" not zero)",
    "category": "Pie Menu"}


import bpy
from bpy.types import Menu, Operator


class ContextPollMode(Operator):
    bl_idname = "context.mode"
    bl_label = "Proportional Edit Poll"
    bl_options = {'INTERNAL'}

    mode = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.scene.tool_settings.proportional_edit = self.mode
        return {'FINISHED'}


class ContextPollFalloff(Operator):
    bl_idname = "context.fo"
    bl_label = "Proportional Edit Poll"
    bl_options = {'INTERNAL'}

    falloff = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.scene.tool_settings.proportional_edit_falloff = self.falloff
        return {'FINISHED'}


class ProportionalEditPie(Menu):
    bl_label = "Proportional Edit"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("context.mode", text="Disabled", icon='PROP_OFF').mode = 'DISABLED'
        pie.operator("context.mode", text="Enabled", icon='PROP_ON').mode = 'ENABLED'
        pie.operator("context.mode", text="Connected", icon='PROP_CON').mode = 'CONNECTED'
        pie.operator("context.mode", text="Projected (2D)", icon='PROP_ON').mode = 'PROJECTED'


class FalloffPie(Menu):
    bl_label = "Proportional Falloff"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # XXX: Rearrange to a logical order
        pie.operator("context.fo", text="Sharp", icon='SHARPCURVE').falloff = 'SHARP'
        pie.operator("context.fo", text="Sphere", icon='SPHERECURVE').falloff = 'SPHERE'
        pie.operator("context.fo", text="Random", icon='RNDCURVE').falloff = 'RANDOM'
        pie.operator("context.fo", text="Root", icon='ROOTCURVE').falloff = 'ROOT'
        pie.operator("context.fo", text="Linear", icon='LINCURVE').falloff = 'LINEAR'
        pie.operator("context.fo", text="Inverse Square", icon='ROOTCURVE').falloff = 'INVERSE_SQUARE'
        pie.operator("context.fo", text="Constant", icon='NOCURVE').falloff = 'CONSTANT'
        pie.operator("context.fo", text="Smooth", icon='SMOOTHCURVE').falloff = 'SMOOTH'


addon_keymaps = []

classes = [
    ContextPollMode,
    ContextPollFalloff,
    ProportionalEditPie,
    FalloffPie
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Grease Pencil Stroke Edit Mode')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
    kmi.properties.name = "ProportionalEditPie"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS', shift=True)
    kmi.properties.name = "FalloffPie"
    addon_keymaps.append(km)

    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
    kmi.properties.name = "ProportionalEditPie"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS', shift=True)
    kmi.properties.name = "FalloffPie"
    addon_keymaps.append(km)

    km = wm.keyconfigs.addon.keymaps.new(name='Curve')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
    kmi.properties.name = "ProportionalEditPie"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS', shift=True)
    kmi.properties.name = "FalloffPie"
    addon_keymaps.append(km)

    km = wm.keyconfigs.addon.keymaps.new(name='Mesh')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
    kmi.properties.name = "ProportionalEditPie"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS', shift=True)
    kmi.properties.name = "FalloffPie"
    addon_keymaps.append(km)

    km = wm.keyconfigs.addon.keymaps.new(name='Metaball')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
    kmi.properties.name = "ProportionalEditPie"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS', shift=True)
    kmi.properties.name = "FalloffPie"
    addon_keymaps.append(km)

    km = wm.keyconfigs.addon.keymaps.new(name='Lattice')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
    kmi.properties.name = "ProportionalEditPie"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS', shift=True)
    kmi.properties.name = "FalloffPie"
    addon_keymaps.append(km)

    km = wm.keyconfigs.addon.keymaps.new(name='Particle')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
    kmi.properties.name = "ProportionalEditPie"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS', shift=True)
    kmi.properties.name = "FalloffPie"
    addon_keymaps.append(km)

    km = wm.keyconfigs.addon.keymaps.new(name='Mask Editing')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS')
    kmi.properties.name = "ProportionalEditPie"
    kmi = km.keymap_items.new('wm.call_menu_pie', 'O', 'PRESS', shift=True)
    kmi.properties.name = "FalloffPie"
    addon_keymaps.append(km)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)

            # wm.keyconfigs.addon.keymaps.remove(km)

    addon_keymaps.clear()

if __name__ == "__main__":
    register()
