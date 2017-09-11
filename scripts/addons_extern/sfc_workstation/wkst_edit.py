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


#######  Menus  ####################

class WKST_Connect(bpy.types.Menu):
    """Connect / Split / Separate"""
    bl_label = "Connect Menu"
    bl_idname = "wkst.connect_menu"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("mesh.vert_connect_path", "Vert Path", icon="STICKY_UVS_DISABLE")
        #layout.operator("mesh.vert_connect", "Vert Connect", icon="OUTLINER_DATA_MESH")

        layout.separator()

        layout.operator("mesh.bridge_edge_loops", "Bridge Edges", icon="ALIGN")
        layout.operator("mesh.edge_face_add", "Edge / Face", icon="EDITMODE_VEC_HLT")

        layout.separator()

        layout.operator("mesh.split", icon="MOD_BOOLEAN")
        layout.operator("mesh.separate", text="Separate", icon="ORTHO")


class WKST_Vertex_Arrange(bpy.types.Menu):
    """Vertex Arrange Menu"""
    bl_label = "Vertex Arrange Menu"
    bl_idname = "wkst.vertex_arrange_menu"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("mesh.vertex_align", text="Vertex Align", icon="ALIGN")
        layout.operator("mesh.vertex_distribute", text="Vertex Distribute", icon="PARTICLE_POINT")

        layout.separator()

        layout.operator("mesh.vertices_smooth", "Smooth", icon="SPHERECURVE")
        layout.operator("mesh.vertices_smooth_laplacian", "Laplacian")

        layout.separator()

        layout.operator("transform.edge_slide", text="Slide Edge", icon="FRAME_NEXT")
        layout.operator("transform.vert_slide", text="Slide Vertex")


class WKST_Extrude(bpy.types.Menu):
    """Extrude Menu"""
    bl_label = "Extrude Menu"
    bl_idname = "wkst.extrude_menu"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("mesh.push_pull_face", text="PushPull")

        layout.separator()

        layout.operator("view3d.edit_mesh_extrude_move_normal", text="Region")
        layout.operator("view3d.edit_mesh_extrude_individual_move", text="Individual")

        layout.separator()

        layout.operator("mesh.fill_grid", "Grid Fill")

        layout.separator()

        layout.operator("mesh.fill", text="Fill")
        layout.operator("mesh.beautify_fill", text="Beautify")

        layout.separator()

        layout.operator("mesh.fill_holes", text="Fill Holes")
        layout.operator("mesh.close_faces", "Close Faces")

        layout.separator()

        layout.operator('faceinfillet.op0_id', text='Face Fillet')
        layout.operator("fillet.op0_id", text="Edge Fillet")

        layout.separator()
        layout.operator("mesh.poke", text="Poke")
        layout.operator("mesh.beautify_fill", text="Beautify")


class WKST_Extrude_Offset(bpy.types.Menu):
    """Extrude Offset Menu"""
    bl_label = "Extrude Offset Menu"
    bl_idname = "wkst.extrude_offset_menu"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        mov = layout.operator('mesh.offset_edges', text='Edge Move')
        mov.geometry_mode = 'move'

        off = layout.operator('mesh.offset_edges', text='Edge Offset')
        off.geometry_mode = 'offset'

        ext = layout.operator('mesh.offset_edges', text='Edge Extrude')
        ext.geometry_mode = 'extrude'

        layout.separator()

        layout.operator("mesh.spin")
        layout.operator("mesh.screw")
        layout.operator('object.mextrude', text='Multi')

        layout.separator()

        layout.operator("mesh.wireframe", text="Wire")
        layout.operator("mesh.solidify", text="Solidify")

        layout.separator()

        layout.operator("mesh.extrude_along_curve", text="Along Curve")


#######  Operators  ##################


class ShrinkApply(bpy.types.Operator):
    """Apply Shrinkwrap"""
    bl_idname = "retopo.shrinkapply"
    bl_label = "Apply Shrinkwrap"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class MirrorApply(bpy.types.Operator):
    """Apply Mirror"""
    bl_idname = "retopo.mirrorapply"
    bl_label = "Apply Mirror"

    def execute(self, context):

        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class LatticeApply(bpy.types.Operator):
    """Apply E-Lattice and delete it"""
    bl_idname = "retopo.latticeapply"
    bl_label = "Apply E-Lattice and delete it"

    def execute(self, context):

        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="latticeeasytemp")
        bpy.ops.object.select_pattern(pattern="LatticeEasytTemp", extend=False)
        bpy.ops.object.delete(use_global=False)

        return {'FINISHED'}


class Freeze(bpy.types.Operator):
    """Freeze from Selection"""
    bl_idname = "retopo.freeze"
    bl_label = "Freeze from Selection"

    def execute(self, context):
        bpy.context.object.hide_select = True
        return {'FINISHED'}


class Wire_All(bpy.types.Operator):
    """Wire on All Objects"""
    bl_idname = "object.wire_all"
    bl_label = "Wire on All Objects"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        for obj in bpy.data.objects:
            if obj.show_wire:
                obj.show_all_edges = False
                obj.show_wire = False
            else:
                obj.show_all_edges = True
                obj.show_wire = True

        return {'FINISHED'}


# Double Threshold 0.001
class DoubleThreshold0001(bpy.types.Operator):
    """Double Threshold 0001"""
    bl_idname = "double.threshold0001"
    bl_label = "Double Threshold 0001"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.scene.tool_settings.double_threshold = 0.001
        return {'FINISHED'}


# Double Threshold 0.1
class DoubleThreshold01(bpy.types.Operator):
    """Double Threshold 01"""
    bl_idname = "double.threshold01"
    bl_label = "Double Threshold 01"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.scene.tool_settings.double_threshold = 0.1
        return {'FINISHED'}


# Albertofx
class removedoubles(bpy.types.Operator):
    """Removes doubles on selected objects."""
    bl_idname = "mesh.removedouble"
    bl_label = "Remove Doubles off Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.join()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        return {'FINISHED'}


class CloseFaces(bpy.types.Operator):
    """Close Faces"""
    bl_idname = "mesh.close_faces"
    bl_label = "Close Faces"
    bl_options = {'REGISTER', 'UNDO'}

    inset = bpy.props.IntProperty(name="Inset", description="How often?", default=0, min=0, soft_max=100, step=1)

    def execute(self, context):

        bpy.ops.mesh.edge_face_add()
        for i in range(self.inset):
            bpy.ops.mesh.inset(thickness=0.025)
        bpy.ops.mesh.poke()
        return {'FINISHED'}


############------------################
############  REGISTER  ################

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
