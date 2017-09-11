# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****


bl_info = {
    "name": "Swap L.O.D.",
    "author": "Aaron Symons",
    "version": (0, 1, 4),
    "blender": (2, 63, 0),
    "api": 46461,
    "location": "View3D > Tool Shelf > Swap L.O.D.",
    "description": "Swaps low-res mesh with a defined high-res mesh at render.",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Render/Swap_LOD",
    "tracker_url": "http://projects.blender.org/tracker/?func=detail&atid=467&aid=31625&group_id=153",
    "category": "Render"
}


import bpy
from bpy.props import *


# Returns whether the current object is a Mesh object or not (not Lamp or Camera)
def is_mesh_object(obj):
    try:
        isCamera = obj.data.lens
    except:
        isCamera = -1

    try:
        isLamp = obj.data.energy
    except:
        isLamp = -1

    if isLamp == -1 and isCamera == -1:
        return True
    return False


# A check to see if an object is new
def is_new_object(obj):
    try:
        isNew = obj['swapRes_high']
    except:
        isNew = -1

    if isNew == -1:
        return True
    return False


# Adds custom properties to all objects in scene that accept Mesh Data, readying them for use
# If the objects already have those properties (we've re-opened a saved scene), it makes them visible
def update_objects(objs, scn):
    scn['updating'] = True

    for obj in objs:
        if is_mesh_object(obj):

            if is_new_object(obj):
                obj['swapRes_high'] = ""
                obj['swapRes_low'] = ""
                obj['swapRes_enable'] = False
                obj['show_lowhigh'] = False
                obj['swapRes_neverSwap'] = False
            else:
                obj['swapRes_high']
                obj['swapRes_low']
                obj['swapRes_enable']
                obj['show_lowhigh']
                obj['swapRes_neverSwap']
        else:
            continue

    scn['updating'] = False


# Custom Properties
def init_scene_props(scn):

    # Used for UI and "behind the scenes"
    bpy.types.Scene.updating = BoolProperty(
    )
    scn['updating'] = False

    bpy.types.Scene.swap_error = BoolProperty(
    )
    scn['swap_error'] = False

    bpy.types.Scene.revert_error = BoolProperty(
    )
    scn['revert_error'] = False

    bpy.types.Scene.show_swap_enabled = BoolProperty(
        name="Show Enabled",
        description="Show all objects with swap enabled"
    )
    scn['show_swap_enabled'] = False

    bpy.types.Scene.show_swap_disabled = BoolProperty(
        name="Show Disabled",
        description="Show all objects with swap disabled"
    )
    scn['show_swap_disabled'] = False

    bpy.types.Object.show_lowhigh = BoolProperty(
        name="Mesh Data",
        description="Show low and high resolution data for this object."
    )
    scn['show_lowhigh'] = False

    bpy.types.Scene.show_all_objects = BoolProperty(
        name="Show All",
        description="Show all objects."
    )
    scn['show_all_objects'] = False

    # Used by objects
    bpy.types.Scene.swap_lod_enable = BoolProperty(
        name="Enable Swap",
        description="Enable swapping."
    )
    scn['swap_lod_enable'] = False

    bpy.types.Object.swapRes_high = StringProperty(
        name="High Res",
        description="Name of the high-res Mesh Data to use."
    )

    bpy.types.Object.swapRes_low = StringProperty(
        name="Low Res",
        description="Name of the low-res Mesh Data to use."
    )

    bpy.types.Object.swapRes_enable = BoolProperty(
        name="Enable",
        description="Include this object in the swap."
    )

    bpy.types.Object.swapRes_neverSwap = BoolProperty(
        name="Never Swap",
        description="Keep this object from showing in the \"Show Disabled\" list, and out of the way."
    )

    update_objects(bpy.data.objects, scn)

# Initialise custom properties
init_scene_props(bpy.context.scene)


# Swaps low-res Mesh Data for the high-res version
def swap_lod(scn):
    oMesh = bpy.data.meshes
    objs = bpy.data.objects

    if scn['swap_lod_enable']:
        for obj in objs:
            if is_mesh_object(obj) and not is_new_object(obj):
                if obj['swapRes_enable'] and obj['swapRes_high'] != "":
                    swapped = False
                    for mData in oMesh:
                        if mData.name == obj['swapRes_high']:
                            obj.data = mData
                            swapped = True
                            scn['swap_error'] = False
                    if not swapped:
                        scn['swap_error'] = True
                        print("Could not find " + obj['swapRes_high'] + " mesh data for " + obj.name)


# Reverts all low-res Objects
def revert_lod(scn):
    oMesh = bpy.data.meshes
    objs = bpy.data.objects

    if scn['swap_lod_enable']:
        for obj in objs:
            if is_mesh_object(obj) and not is_new_object(obj):
                if obj['swapRes_enable'] and obj['swapRes_low'] != "":
                    swapped = False
                    for mData in oMesh:
                        if mData.name == obj['swapRes_low']:
                            obj.data = mData
                            swapped = True
                            scn['revert_error'] = False
                    if not swapped:
                        scn['swap_error'] = True
                        print("Could not find " + obj['swapRes_low'] + " mesh data for " + obj.name)


class Swap_LOD(bpy.types.Operator):
    ''' Swaps low-res Mesh Data with high-res Mesh Data '''

    bl_idname = "swap.swap_lod"
    bl_label = "SwapLoD"
    bl_description = "Swap low-res for high-res in 3D View."

    # Used by UI button
    def execute(self, context):
        scn = bpy.context.scene
        swap_lod(scn)
        return {'FINISHED'}

    # Used at render
    def swap(unused):
        scn = bpy.context.scene
        swap_lod(scn)


class Revert_LOD(bpy.types.Operator):
    ''' Reverts Object's Mesh Data back to low-res Mesh Data '''

    bl_idname = "swap.revert_lod"
    bl_label = "RevertLoD"
    bl_description = "Revert low-res Object back to low-res Mesh Data in 3D View."

    # Used by UI button
    def execute(self, context):
        scn = bpy.context.scene
        revert_lod(scn)
        return {'FINISHED'}

    # Used at render
    def revert(unused):
        scn = bpy.context.scene
        revert_lod(scn)


class CL_Update_Objects(bpy.types.Operator):
    ''' Updates new objects in the scene - giving them the custom properties '''

    bl_idname = "swap.update_objects"
    bl_label = "updateobjs"
    bl_description = "Adds the swap properties to newly created objects."

    def execute(self, context):
        update_objects(bpy.data.objects, bpy.context.scene)
        return {'FINISHED'}


# An empty function used for disabled UI buttons - simulating a disabled button
# Currently, I don't know of another way to disable buttons while keeping them visible
class Disabled(bpy.types.Operator):
    bl_idname = "swap.nothing"
    bl_label = "Nothing"
    bl_description = "Button is disabled."

    def execute(self, context):
        return {'FINISHED'}


# The UI jazz
class Swap_LOD_UIPanel(bpy.types.Panel):
    ''' Class for UI Panel '''

    bl_label = "Swap L.O.D."
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        # If an error has occured, lets tell the user
        if scn['revert_error'] or scn['swap_error']:
            layout.label("oops! Some mesh data wasn't found.", icon="ERROR")
            layout.label("Look in the Console for details:")
            layout.label("Help > Toggle System Console", icon="INFO")
            layout.separator()

        box = layout.box()
        row1 = box.row()
        row2 = box.row(align=True)
        row3 = box.row(align=True)

        swapEnableIcon = "RESTRICT_RENDER_OFF"
        if not scn['swap_lod_enable']:
            swapEnableIcon = "RESTRICT_RENDER_ON"
        row1.prop(scn, 'swap_lod_enable', icon=swapEnableIcon)

        row1.operator("swap.update_objects", text="Update", icon="FILE_REFRESH")

        revert = "swap.revert_lod"
        swap = "swap.swap_lod"
        if scn['swap_lod_enable']:
            row2.active = True
        else:
            revert = "swap.nothing"
            swap = "swap.nothing"
            row2.active = False
        row2.operator(swap, text="Swap to High", icon="MESH_DATA")
        row2.operator(revert, text="Swap to Low", icon="MESH_DATA")

        showEnabledIcon = "RESTRICT_VIEW_ON"
        showDisabledIcon = "RESTRICT_VIEW_ON"
        if scn['show_swap_enabled']:
            showEnabledIcon = "RESTRICT_VIEW_OFF"
        if scn['show_swap_disabled']:
            showDisabledIcon = "RESTRICT_VIEW_OFF"
        row3.prop(scn, 'show_swap_enabled', text="Enabled", icon=showEnabledIcon)
        row3.prop(scn, 'show_swap_disabled', text="Disabled", icon=showDisabledIcon)

        showAllObjs = "RESTRICT_VIEW_ON"
        if scn['show_all_objects']:
            showAllObjs = "RESTRICT_VIEW_OFF"
        row3.prop(scn, 'show_all_objects', icon=showAllObjs)

        objs = bpy.data.objects

        # Display enabled objects
        enabledObjs = 0
        if not scn['updating'] and scn['show_swap_enabled']:
            for obj in objs:
                if is_mesh_object(obj) and not is_new_object(obj):
                    if obj['swapRes_enable']:
                        enabledObjs += 1

                        box = layout.box()
                        row0 = box.row()
                        row1 = box.row()
                        row0.label(obj.name + ":")

                        if obj['swapRes_neverSwap']:
                            row0.prop(obj, 'swapRes_neverSwap')
                        row1.prop(obj, 'swapRes_enable', text="Swap")

                        showMeshData = "RESTRICT_VIEW_ON"
                        if obj['show_lowhigh']:
                            showMeshData = "RESTRICT_VIEW_OFF"
                        row1.prop(obj, 'show_lowhigh', text="Mesh Data", icon=showMeshData)

                        if obj['show_lowhigh']:
                            box.prop(obj, 'swapRes_high', icon="MESH_DATA")
                            box.prop(obj, 'swapRes_low', icon="MESH_DATA")
            if enabledObjs == 0:
                box = layout.box()
                row = box.row()
                row.label("No enabled objects to display.")

        # Display disabled objects
        disabledObjs = 0
        if not scn['updating'] and scn['show_swap_disabled']:
            for obj in objs:
                if is_mesh_object(obj) and not is_new_object(obj):
                    if not obj['swapRes_enable'] and not obj['swapRes_neverSwap']:
                        disabledObjs += 1

                        box = layout.box()
                        row0 = box.row()
                        row1 = box.row()
                        row0.label(obj.name + ":")

                        row0.prop(obj, 'swapRes_neverSwap')
                        row1.prop(obj, 'swapRes_enable', text="Swap")

                        showMeshData = "RESTRICT_VIEW_ON"
                        if obj['show_lowhigh']:
                            showMeshData = "RESTRICT_VIEW_OFF"
                        row1.prop(obj, 'show_lowhigh', text="Mesh Data", icon=showMeshData)

                        if obj['show_lowhigh']:
                            box.prop(obj, 'swapRes_high', icon="MESH_DATA")
                            box.prop(obj, 'swapRes_low', icon="MESH_DATA")
            if disabledObjs == 0:
                box = layout.box()
                row = box.row()
                row.label("No disabled objects to display.")

        # Display all objects
        numObjs = 0
        if not scn['updating'] and scn['show_all_objects']:
            for obj in objs:
                if is_mesh_object(obj) and not is_new_object(obj):
                    numObjs += 1
                    box = layout.box()
                    row0 = box.row()
                    row1 = box.row()
                    row0.label(obj.name + ":")

                    row0.prop(obj, 'swapRes_neverSwap')
                    row1.prop(obj, 'swapRes_enable', text="Swap")

                    showMeshData = "RESTRICT_VIEW_ON"
                    if obj['show_lowhigh']:
                        showMeshData = "RESTRICT_VIEW_OFF"
                    row1.prop(obj, 'show_lowhigh', text="Mesh Data", icon=showMeshData)

                    if obj['show_lowhigh']:
                        box.prop(obj, 'swapRes_high', icon="MESH_DATA")
                        box.prop(obj, 'swapRes_low', icon="MESH_DATA")
            if numObjs == 0:
                box = layout.box()
                row = box.row()
                row.label("No objects to display.")

# Registration


def register():
    bpy.utils.register_module(__name__)

    bpy.app.handlers.render_pre.append(Swap_LOD.swap)
    bpy.app.handlers.render_cancel.append(Revert_LOD.revert)
    bpy.app.handlers.render_complete.append(Revert_LOD.revert)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.app.handlers.render_pre.remove(Swap_LOD.swap)
    bpy.app.handlers.render_cancel.remove(Revert_LOD.revert)
    bpy.app.handlers.render_complete.remove(Revert_LOD.revert)

if __name__ == '__main__':
    register()
