#
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#
# ***** END GPL LICENCE BLOCK *****


import bpy
from bpy import*


#######  Add Geometry   #################

class SINGLEVERTEX(bpy.types.Operator):
    """Add a single Vertex in Editmode"""
    bl_idname = "mesh.singlevertex"
    bl_label = "Single Vertex"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.mesh.merge(type='CENTER')
        return {'FINISHED'}


class SINGLELINE_X(bpy.types.Operator):
    """Add a single Line in Editmode"""
    bl_idname = "mesh.singleline_x"
    bl_label = "Single Line"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror": False}, TRANSFORM_OT_translate={"value": (2, 0, 0), "constraint_axis": (True, False, False), "constraint_orientation": 'GLOBAL', "mirror": False, "proportional": 'DISABLED', "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "texture_space": False, "remove_on_cancel": False, "release_confirm": False})
        bpy.ops.mesh.select_linked(limit=False)
        return {'FINISHED'}


class SINGLELINE_Y(bpy.types.Operator):
    """Add a single Line in Editmode"""
    bl_idname = "mesh.singleline_y"
    bl_label = "Single Line"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror": False}, TRANSFORM_OT_translate={"value": (0, 2, 0), "constraint_axis": (False, True, False), "constraint_orientation": 'GLOBAL', "mirror": False, "proportional": 'DISABLED', "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "texture_space": False, "remove_on_cancel": False, "release_confirm": False})
        bpy.ops.mesh.select_linked(limit=False)
        return {'FINISHED'}


class SINGLELINE_Z(bpy.types.Operator):
    """Add a single Line in Editmode"""
    bl_idname = "mesh.singleline_z"
    bl_label = "Single Line"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror": False}, TRANSFORM_OT_translate={"value": (0, 0, 2), "constraint_axis": (False, False, True), "constraint_orientation": 'GLOBAL', "mirror": False, "proportional": 'DISABLED', "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "texture_space": False, "remove_on_cancel": False, "release_confirm": False})
        bpy.ops.mesh.select_linked(limit=False)
        return {'FINISHED'}


class SINGLEPLANE_X(bpy.types.Operator):
    """Add a vertical Plane in Editmode"""
    bl_idname = "mesh.singleplane_x"
    bl_label = "Single Plane"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {'FINISHED'}


class SINGLEPLANE_Y(bpy.types.Operator):
    """Add a vertical Plane in Editmode"""
    bl_idname = "mesh.singleplane_y"
    bl_label = "Single Plane"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {'FINISHED'}


class SINGLEPLANE_Z(bpy.types.Operator):
    """Add a vertical Plane in Editmode"""
    bl_idname = "mesh.singleplane_z"
    bl_label = "Single Plane"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}


class EMPTYROOMCEN(bpy.types.Operator):
    """Add a object without a mesh in editmode to center"""
    bl_idname = "mesh.emptyroom_cen"
    bl_label = "Retopo CenterRoom"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.delete(type='VERT')
        bpy.context.object.name = "Retopo"
        bpy.ops.object.copynametodata()
        return {'FINISHED'}


class EMPTYXROOMCEN(bpy.types.Operator):
    """Add a object without a mesh in editmode and add a x mirror modifier to center"""
    bl_idname = "mesh.emptyxroom_cen"
    bl_label = "Retopo X-CenterRoom"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.view3d.fullmirror()
        bpy.context.object.name = "Retopo"
        bpy.ops.object.copynametodata()
        return {'FINISHED'}


class EMPTYROOM(bpy.types.Operator):
    """Add a object without a mesh in editmode to selected"""
    bl_idname = "mesh.emptyroom_sel"
    bl_label = "Retopo SelectRoom"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.delete(type='VERT')
        bpy.context.object.name = "Retopo"
        bpy.ops.object.copynametodata()
        return {'FINISHED'}


class EMPTYXROOM(bpy.types.Operator):
    """Add a object without a mesh in editmode and add a x mirror modifier to selected"""
    bl_idname = "mesh.emptyxroom_sel"
    bl_label = "Retopo X-SelectRoom"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.view3d.fullmirror()
        bpy.context.object.name = "Retopo"
        bpy.ops.object.copynametodata()
        return {'FINISHED'}


class FullCurve(bpy.types.Operator):
    """Add A full Bevel Curve"""
    bl_idname = "view3d.fullcurve"
    bl_label = "A full Bevel Curve"

    def execute(self, context):

        bpy.ops.curve.primitive_bezier_curve_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        bpy.ops.transform.resize(value=(5, 5, 5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.bevel_resolution = 8
        bpy.context.object.data.resolution_u = 10
        bpy.context.object.data.bevel_depth = 0.2
        bpy.context.object.name = "Bevel Curve"
        bpy.ops.object.copynametodata()
        return {'FINISHED'}


class FullCircleCurve(bpy.types.Operator):
    """Add A full Bevel CircleCurve"""
    bl_idname = "view3d.fullcirlcecurve"
    bl_label = "A full Bevel CircleCurve"

    def execute(self, context):

        bpy.ops.curve.primitive_bezier_circle_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        bpy.ops.transform.resize(value=(5, 5, 5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.bevel_resolution = 8
        bpy.context.object.data.resolution_u = 10
        bpy.context.object.data.bevel_depth = 0.2
        bpy.context.object.name = "Bevel Circle"
        bpy.ops.object.copynametodata()
        return {'FINISHED'}


############  REGISTER  ############

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
