bl_info = {
    "name": "Texture Paint on Selected Cycles Image Node",
    "author": "Cezary Kopias",
    "version": (1, 0),
    "blender": (2, 72, 0),
    "location": "Cycles Material Nodes",
    "description": "LeftClick on Cycles Image Node to use it for Texture Painting Image Mode Slot",
    "warning": "It only works when in Texture Painting Image Mode with Cycles",
    "wiki_url": "",
    "category": "Paint"}

import bpy


class paint_on_node_image(bpy.types.Operator):
    bl_idname = "node.paint_on_node_image"
    bl_label = "Paint on Active Image Node"
    bl_options = {'UNDO'}

    def execute(self, context):
        if context.active_node:
            active_node = context.active_node

            if active_node.bl_idname == "ShaderNodeTexImage":
                bpy.context.scene.tool_settings.image_paint.canvas = active_node.image

        return {'FINISHED'}

addon_keymaps = []


def register():
    bpy.utils.register_class(paint_on_node_image)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new("node.paint_on_node_image", 'ACTIONMOUSE', 'CLICK')
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(paint_on_node_image)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
