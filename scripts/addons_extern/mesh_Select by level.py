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

bl_info = {
    "name": "Select by level",
    "author": "Omar ahmed",
    "version": (1, 0),
    "blender": (2, 74, 0),
    "location": "View3D > EditMode > Select panel",
    "description": "Select vertices by level",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}

import bpy
import bmesh


class Select_by_level(bpy.types.Operator):
    """Select by level"""
    bl_idname = "mesh.select_by_level"
    bl_label = "Select by level"
    bl_options = {'REGISTER', 'UNDO'}

    # Defining the custom properties

    X_boolean = bpy.props.BoolProperty(name="X", description="Select in the X axis or not", default=False)
    Y_boolean = bpy.props.BoolProperty(name="Y", description="Select in the Y axis or not", default=False)
    Z_boolean = bpy.props.BoolProperty(name="Z", description="Select in the Z axis or not", default=True)
    Negative_threshold_x = bpy.props.FloatProperty(name="X negative threshold", description="Negative threshold to select after expanding the selection in X axis", default=0.001)
    Positive_threshold_x = bpy.props.FloatProperty(name="X Positive threshold", description="Positive threshold to select after expanding the selection in X axis", default=0.001)
    Negative_threshold_y = bpy.props.FloatProperty(name="Y negative threshold", description="Negative threshold to select after expanding the selection in Y axis", default=0.001)
    Positive_threshold_y = bpy.props.FloatProperty(name="Y Positive threshold", description="Positive threshold to select after expanding the selection in Y axis", default=0.001)
    Negative_threshold_z = bpy.props.FloatProperty(name="Z negative threshold", description="Negative threshold to select after expanding the selection in Z axis", default=0.001)
    Positive_threshold_z = bpy.props.FloatProperty(name="Z Positive threshold", description="Positive threshold to select after expanding the selection in Z axis", default=0.001)

    def execute(self, context):

        # Defining variables

        ob = bpy.context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)

        # Getting location of vertices

        location_x = [v.co.x for v in bm.verts if v.select]
        location_y = [v.co.y for v in bm.verts if v.select]
        location_z = [v.co.z for v in bm.verts if v.select]

        # See if the list is empty

        if not location_x:
            self.report({'WARNING'},
                        "No vertices selected.")
            return {'FINISHED'}

        # Getting the average of the location of vertices

        avg_x = sum(location_x) / len(location_x)
        avg_y = sum(location_y) / len(location_y)
        avg_z = sum(location_z) / len(location_z)

        # Defining the min and max values

        Min_Space_x = avg_x - self.Negative_threshold_x
        Min_Space_y = avg_y - self.Negative_threshold_y
        Min_Space_z = avg_z - self.Negative_threshold_z
        Max_Space_x = avg_x + self.Positive_threshold_x
        Max_Space_y = avg_y + self.Positive_threshold_y
        Max_Space_z = avg_z + self.Positive_threshold_z

        # Deselcting all

        bpy.ops.mesh.select_all(action='DESELECT')

        # Selecting verices with a range in X

        if self.X_boolean == True:
            for v in bm.verts:
                if v.co.x < Max_Space_x and v.co.x > Min_Space_x:
                    v.select = True
            bm.select_flush(True)

        # Selecting verices with a range in Y

        if self.Y_boolean == True:
            for v in bm.verts:
                if v.co.y < Max_Space_y and v.co.y > Min_Space_y:
                    v.select = True
            bm.select_flush(True)

        # Selecting verices with a range in Z

        if self.Z_boolean == True:
            for v in bm.verts:
                if v.co.z < Max_Space_z and v.co.z > Min_Space_z:
                    v.select = True
            bm.select_flush(True)

        return {'FINISHED'}

# Adding it to select menu


def menu_func(self, context):
    self.layout.operator(Select_by_level.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(Select_by_level)
    bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new(Select_by_level.bl_idname, 'L', 'ANY', shift=True, ctrl=True)
    # kmi.properties.my_prop = 'some'
    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.register_class(Select_by_level)
    bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)

    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
