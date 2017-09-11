# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


#########################################################################################################
bl_info = {
    "name": "Rebool",
    "author": "Pixivore",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "View3D > CTRL + /",
    "description": "Difference and intercept between two objects",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}
#########################################################################################################


import bpy


#########################################################################################################
class ReboolPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    bpy.types.Scene.Enable_Tab_01 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_Tab_02 = bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "Enable_Tab_01", text="Info", icon="QUESTION")
        if context.scene.Enable_Tab_01:
            row = layout.row()
            layout.label(text="Rebool Operator")
            layout.label(text="Select objects to difference and intercept between them")

        layout.prop(context.scene, "Enable_Tab_02", text="URL's", icon="URL")
        if context.scene.Enable_Tab_02:
            row = layout.row()
            row.operator("wm.url_open", text="pixivores.com").url = "http://pixivores.com"
#########################################################################################################


#########################################################################################################
def main(context):
    SelObj_Name = []
    BoolObj = []

    C = bpy.context

    LastObj = C.active_object

    if(len(C.selected_objects) > 0):
        for obj in C.selected_objects:
            if(C.active_object.name != obj.name):
                BoolObj.append(obj.name)
                obj.select = False

    bpy.ops.object.select_all(action='TOGGLE')

    for obj in BoolObj:
        bpy.context.scene.objects.active = bpy.data.objects[obj]
        bpy.data.objects[obj].draw_type = "SOLID"
        bpy.data.objects[obj].select = True
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0), "constraint_axis": (False, False, False), "constraint_orientation": 'GLOBAL', "mirror": False, "proportional": 'DISABLED', "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False})
        LastObjectCreated = bpy.context.active_object.name

        for mb in LastObj.modifiers:
            if(mb.type == 'BEVEL'):
                mb.show_viewport = False

        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
        bpy.context.object.modifiers["Boolean"].object = LastObj
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")

        bpy.ops.object.select_all(action='TOGGLE')

        for mb in LastObj.modifiers:
            if(mb.type == 'BEVEL'):
                mb.show_viewport = True

    for obj in BoolObj:
        bpy.context.scene.objects.active = bpy.data.objects[LastObj.name]
        bpy.data.objects[LastObj.name].select = True
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[obj]
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
        bpy.data.objects[obj].draw_type = "WIRE"
        bpy.ops.object.select_all(action='TOGGLE')

    bpy.data.objects[LastObjectCreated].select = True

#########################################################################################################


#########################################################################################################
class ReboolOperator(bpy.types.Operator):
    bl_idname = "object.rebool"
    bl_label = "Rebool Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}
#########################################################################################################


#########################################################################################################
classes = [ReboolOperator]
addon_keymaps = []
#########################################################################################################


#########################################################################################################
def register():
    bpy.utils.register_class(ReboolPrefs)

    bpy.utils.register_class(ReboolOperator)
    # add keymap entry
    kcfg = bpy.context.window_manager.keyconfigs.addon
    if kcfg:
        km = kcfg.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new("object.rebool", 'NUMPAD_SLASH', 'PRESS', shift=False, ctrl=True)
        addon_keymaps.append((km, kmi))
#########################################################################################################


#########################################################################################################
def unregister():
    bpy.utils.unregister_class(ReboolPrefs)

   # remove keymap entry
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(ReboolOperator)
#########################################################################################################


#########################################################################################################
if __name__ == "__main__":
    register()
