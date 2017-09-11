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


#######  Menus  ###################
class WKST_Subdivide(bpy.types.Menu):
    """Subdivide Menu"""
    bl_label = "Subdivide  Menu"
    bl_idname = "wkst.subdivide_menu"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("mesh.quads_convert_to_tris", text="Tris", icon="MOD_TRIANGULATE")
        layout.operator("mesh.tris_convert_to_quads", text="Quads", icon="MOD_LATTICE")

        layout.separator()

        layout.label("Subdivide Mesh", icon="MESH_ICOSPHERE")

        layout.operator("mesh.subdivide", text="1 cut").number_cuts = 1
        layout.operator("mesh.subdivide", text="2 cuts").number_cuts = 2
        layout.operator("mesh.subdivide", text="3 cuts").number_cuts = 3
        layout.operator("mesh.subdivide", text="4 cuts").number_cuts = 4
        layout.operator("mesh.subdivide", text="5 cuts").number_cuts = 5
        layout.operator("mesh.subdivide", text="6 cuts").number_cuts = 6

        layout.separator()

        layout.operator("mesh.unsubdivide", text="UnSubdivide")


class WKST_Cutting(bpy.types.Menu):
    """Cutting Menu"""
    bl_label = "Cutting Menu"
    bl_idname = "wkst.cutting_menu"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("mesh.snap_utilities_line", "SnapLine", icon="LINE_DATA")
        layout.operator("mesh.bisect", icon="SCULPTMODE_HLT")

        layout.separator()

        props = layout.operator("mesh.knife_tool", text="Knife", icon="LINE_DATA")
        props.use_occlude_geometry = True
        props.only_selected = False

        props = layout.operator("mesh.knife_tool", text="Knife Select", icon="LINE_DATA")
        props.use_occlude_geometry = False
        props.only_selected = True

        layout.operator("mesh.knife_project", icon="LINE_DATA")

        layout.separator()

        layout.operator("object_ot.fastloop", icon="GRIP")
        layout.operator("mesh.loopcut_slide", "Loop Cut", icon="COLLAPSEMENU")
        layout.operator("mesh.ext_cut_faces", text="Face Cut", icon="SNAP_EDGE")

        layout.separator()

        layout.operator("object.createhole", text="Face Hole", icon="RADIOBUT_OFF")
        layout.operator("mesh.build_corner", icon="OUTLINER_DATA_MESH")


class WKST_Axis_Cut(bpy.types.Menu):
    """Axis Cut & Delete Menu"""
    bl_label = "Axis Cut Menu"
    bl_idname = "wkst.axis_cut_menu"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        if context.mode == 'OBJECT':

            layout.operator("modifier.positiv_x_cut_obm", text="+X")
            layout.operator("modifier.positiv_y_cut_obm", text="+Y")
            layout.operator("modifier.positiv_z_cut_obm", text="+Z")

            layout.separator()

            layout.operator("modifier.negativ_x_cut_obm", text="-X")
            layout.operator("modifier.negativ_y_cut_obm", text="-Y")
            layout.operator("modifier.negativ_z_cut_obm", text="-Z")

        if context.mode == 'EDIT_MESH':

            layout.operator("modifier.positiv_x_cut", text="+X")
            layout.operator("modifier.positiv_y_cut", text="+Y")
            layout.operator("modifier.positiv_z_cut", text="+Z")

            layout.separator()

            layout.operator("modifier.negativ_x_cut", text="-X")
            layout.operator("modifier.negativ_y_cut", text="-Y")
            layout.operator("modifier.negativ_z_cut", text="-Z")


#######  Operators  ####################


class NegativXCut(bpy.types.Operator):
    """Cut Object and delete negative X"""
    bl_idname = "modifier.negativ_x_cut"
    bl_label = "Cut -X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'x'
        bpy.context.scene.AutoMirror_orientation = 'positive'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        return {'FINISHED'}


class PositivXCut(bpy.types.Operator):
    """Cut Object and delete positiv X"""
    bl_idname = "modifier.positiv_x_cut"
    bl_label = "Cut +X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'x'
        bpy.context.scene.AutoMirror_orientation = 'negative'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        return {'FINISHED'}


class NegativYCut(bpy.types.Operator):
    """Cut Object and delete negative Y"""
    bl_idname = "modifier.negativ_y_cut"
    bl_label = "Cut -Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'y'
        bpy.context.scene.AutoMirror_orientation = 'positive'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        return {'FINISHED'}


class PositivYCut(bpy.types.Operator):
    """Cut Object and delete positiv Y"""
    bl_idname = "modifier.positiv_y_cut"
    bl_label = "Cut +Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'y'
        bpy.context.scene.AutoMirror_orientation = 'negative'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        return {'FINISHED'}


class NegativZCut(bpy.types.Operator):
    """Cut Object and delete negative Z"""
    bl_idname = "modifier.negativ_z_cut"
    bl_label = "Cut -Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'z'
        bpy.context.scene.AutoMirror_orientation = 'positive'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        return {'FINISHED'}


class PositivZCut(bpy.types.Operator):
    """Cut Object and delete positiv Z"""
    bl_idname = "modifier.positiv_z_cut"
    bl_label = "Cut +Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'z'
        bpy.context.scene.AutoMirror_orientation = 'negative'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        return {'FINISHED'}


##########################################

class NegativXCut_obm(bpy.types.Operator):
    """Cut Object and delete negative X"""
    bl_idname = "modifier.negativ_x_cut_obm"
    bl_label = "Cut -X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'x'
        bpy.context.scene.AutoMirror_orientation = 'positive'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class PositivXCut_obm(bpy.types.Operator):
    """Cut Object on the positiv X-Ais"""
    bl_idname = "modifier.positiv_x_cut_obm"
    bl_label = "Cut +X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'x'
        bpy.context.scene.AutoMirror_orientation = 'negative'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class NegativYCut_obm(bpy.types.Operator):
    """Cut Object and delete negative Y"""
    bl_idname = "modifier.negativ_y_cut_obm"
    bl_label = "Cut -Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'y'
        bpy.context.scene.AutoMirror_orientation = 'positive'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class PositivYCut_obm(bpy.types.Operator):
    """Cut Object and delete positiv Y"""
    bl_idname = "modifier.positiv_y_cut_obm"
    bl_label = "Cut +Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'y'
        bpy.context.scene.AutoMirror_orientation = 'negative'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class NegativZCut_obm(bpy.types.Operator):
    """Cut Object and delete negative Z"""
    bl_idname = "modifier.negativ_z_cut_obm"
    bl_label = "Cut -Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'z'
        bpy.context.scene.AutoMirror_orientation = 'positive'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class PositivZCut_obm(bpy.types.Operator):
    """Cut Object and delete positiv Z  """
    bl_idname = "modifier.positiv_z_cut_obm"
    bl_label = "Cut +Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.scene.AutoMirror_axis = 'z'
        bpy.context.scene.AutoMirror_orientation = 'negative'
        bpy.ops.object.automirror()
        bpy.ops.object.modifier_remove(modifier="Mirror")
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


# Create Hole
class CreateHole(bpy.types.Operator):
    """This Operator create a hole on a selection"""
    bl_idname = "object.createhole"
    bl_label = "Create Hole"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    divide = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=5, step=1)
    size = bpy.props.IntProperty(name="Size", description="How often?", default=1, min=1, soft_max=10, step=1)
    inset = bpy.props.IntProperty(name="Inset", description="How often?", default=1, min=1, soft_max=10, step=1)
    close = bpy.props.BoolProperty(name="Close Hole", description="close or open Hole", default=True)

    def execute(self, context):

        for i in range(self.divide):
            bpy.ops.mesh.subdivide(number_cuts=1)

        bpy.ops.mesh.extrude_region_move()

        for i in range(self.size):
            bpy.ops.transform.resize(value=(0.8, 0.8, 0.8))

        bpy.ops.mesh.looptools_circle()

        bpy.ops.mesh.extrude_region_move()

        for i in range(self.inset):
            bpy.ops.transform.resize(value=(0.8, 0.8, 0.8))

        for i in range(self.close):
            bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'}

########################################


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
