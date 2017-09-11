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

__bpydoc__ = """\
The DeCouple addon is really simple but useful: the selected parent object will be decoupled
temporarily from its children so youll be able to reposition the parent without influencing
the children.


Documentation

First go to User Preferences->Addons and enable the DeCouple addon in the Object category.
Select the parent object of your choice and invoke the addon (button in the Object Tools panel).

If you wish to hotkey DeCouple:
In the Input section of User Preferences at the bottom of the 3D View > Object Mode section click 'Add New' button.
In the Operator Identifier box put 'object.decouple'.
Assign a hotkey.
Save as Default (Optional).
"""


bl_info = {
    "name": "DeCouple",
    "author": "Gert De Roost",
    "version": (0, 1, 0),
    "blender": (2, 6, 5),
    "location": "View3D > Tools",
    "description": "Temporarily decouples parent and children",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

if "bpy" in locals():
    import imp


import bpy


started = 0


class DeCouple(bpy.types.Operator):
    bl_idname = "object.decouple"
    bl_label = "DeCouple"
    bl_description = "Temporarily decouples parent and children"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and context.mode == 'OBJECT')

    def invoke(self, context, event):
        self.save_global_undo = bpy.context.user_preferences.edit.use_global_undo
        bpy.context.user_preferences.edit.use_global_undo = False

        do_decouple(self)

        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def modal(self, context, event):

        global started

        if started == 2:
            started = 0
            return {"FINISHED"}

        return {"PASS_THROUGH"}


def panel_func(self, context):
    self.layout.label(text="DeCouple:")
    if started:
        self.layout.operator("object.decouple", text="Reparent")
    else:
        self.layout.operator("object.decouple", text="Unparent")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_PT_tools_objectmode.append(panel_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_PT_tools_objectmode.remove(panel_func)


if __name__ == "__main__":
    register()


def do_decouple(self):

    global started, parent, children

    if not(started):
        parent = bpy.context.active_object
        if len(parent.children) == 0:
            return
        parent.select = 0
        children = []
        for child in parent.children:
            children.append(child)
            child.select = 1
        bpy.ops.object.parent_clear(type='CLEAR')
        for child in children:
            child.select = 0
        parent.select = 1
        bpy.context.scene.objects.active = parent
        started = 1
    else:
        parent.select = 0
        for child in children:
            child.select = 1
        parent.select = 1
        bpy.context.scene.objects.active = parent
        bpy.ops.object.parent_set()
        for child in children:
            child.select = 0
        started = 2
