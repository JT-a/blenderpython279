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


import bpy
from bpy import*


# Multi Select  #######-------------------------------------------------------

class VIEW3D_MT_edit_multi(bpy.types.Menu):
    """Multi Selection"""
    bl_label = "Multi Selection"
    bl_label = "wkst.multi_selection"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        prop = layout.operator("wm.context_set_value", text="Vertex Select", icon='VERTEXSEL')
        prop.value = "(True, False, False)"
        prop.data_path = "tool_settings.mesh_select_mode"

        prop = layout.operator("wm.context_set_value", text="Edge Select", icon='EDGESEL')
        prop.value = "(False, True, False)"
        prop.data_path = "tool_settings.mesh_select_mode"

        prop = layout.operator("wm.context_set_value", text="Face Select", icon='FACESEL')
        prop.value = "(False, False, True)"
        prop.data_path = "tool_settings.mesh_select_mode"

        layout.separator()

        prop = layout.operator("wm.context_set_value", text="Vertex & Edge Select", icon='EDITMODE_HLT')
        prop.value = "(True, True, False)"
        prop.data_path = "tool_settings.mesh_select_mode"

        prop = layout.operator("wm.context_set_value", text="Vertex & Face Select", icon='ORTHO')
        prop.value = "(True, False, True)"
        prop.data_path = "tool_settings.mesh_select_mode"

        prop = layout.operator("wm.context_set_value", text="Edge & Face Select", icon='SNAP_FACE')
        prop.value = "(False, True, True)"
        prop.data_path = "tool_settings.mesh_select_mode"
        layout.separator()

        prop = layout.operator("wm.context_set_value", text="Vertex & Edge & Face Select", icon='SNAP_VOLUME')
        prop.value = "(True, True, True)"
        prop.data_path = "tool_settings.mesh_select_mode"


# Cycle through Selected  #######-------------------------------------------------------

###Mr. Stan_Pancake
class ThroughSelected(bpy.types.Operator):
    """cycle through selected objects"""
    bl_idname = "object.throughselected"
    bl_label = "Cycle through Selected"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selection = bpy.context.selected_objects

        if not bpy.context.active_object.select:
            if len(selection):
                bpy.context.scene.objects.active = selection[0]
        else:
            for i, o in enumerate(selection):
                if o == bpy.context.active_object:
                    bpy.context.scene.objects.active = selection[(i + 1) % len(selection)]
                    break

        return {'FINISHED'}


import bpy
import re
import math
from mathutils import Vector
from math import pi

# ------------------------------------------------------------------------
#    freeze selection button
# ------------------------------------------------------------------------


def get_AllObjectsInSelection():
    return bpy.context.selected_objects


def get_hideSelectObjects(object_list):
    for i in object_list:
        i.hide_select = True
    bpy.ops.object.select_all(action='DESELECT')
    return True


class FreezeObjectsButton(bpy.types.Operator):
    bl_idname = "vfxtoolbox.freeze_selected_objects"
    bl_label = "Freeze Selection"
    bl_description = "Disables the viewport selection of current objects."

    def execute(self, context):
        selection = get_AllObjectsInSelection()
        n = len(selection)
        if n > 0:
            get_hideSelectObjects(selection)
            self.report({'INFO'}, "%d Object%s frozen." % (n, "s"[n == 1:]))
        else:
            self.report({'INFO'}, 'Nothing selected.')
        return{'FINISHED'}


# ------------------------------------------------------------------------
#    unfreeze all button
# ------------------------------------------------------------------------

def get_AllObjectsInScene():
    return bpy.data.objects


def get_dehideSelectObjects(object_list):
    hidedObjs = []
    for i in object_list:
        if i.hide_select == True:
            i.hide_select = False
            hidedObjs.append(i)
    return hidedObjs


def get_highlightObjects(selection_list):

    for i in selection_list:
        bpy.data.objects[i.name].select = True


class UnfreezeButton(bpy.types.Operator):
    bl_idname = "vfxtoolbox.defreeze_all_objects"
    bl_label = "Unfreeze All"
    bl_description = "Enables viewport selection of all objects in scene."

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        selection = get_AllObjectsInScene()
        n = len(selection)

        if n > 0:
            freezed_array = get_dehideSelectObjects(selection)
            get_highlightObjects(freezed_array)
            self.report({'INFO'}, "%d Object%s released." % (n, "s"[n == 1:]))
        else:
            self.report({'INFO'}, 'Nothing selected.')

        return{'FINISHED'}

############------------############
############  REGISTER  ############


def register():
    # bpy.utils.register_class()
    bpy.utils.register_module(__name__)


def unregister():
    # bpy.utils.unregister_class()
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
