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
    "name": "Transform Normal Constraint",
    "author": "marvin.k.breuer",
    "version": (0, 1),
    "blender": (2, 7, 5),
    "location": "View3D > Tools > Transform > Transform with Normal Axis Contraint",
    "description": "Transform Objects with Normal Axis Contraint",
    "warning": "",
    "url": "http://www.blenderartists.org/forum/showthread.php?380673-Transform-with-Normal-Axis-Contraint&p=2932621#post2932621",
    "url": "https://plus.google.com/u/0/+MarvinKBreuer/posts",
    "category": "User Interface"
}


import bpy


###########  Menu  #######################


class WKST_N_Transform_Menu(bpy.types.Menu):
    """Normal Transform Menu"""
    bl_label = "Normal Transform Menu"
    bl_idname = "wkst.normal_transform_menu"

    def draw(self, context):
        layout = self.layout

        layout.menu("translate.normal_menu", text="N-Translate")
        layout.menu("rotate.normal_menu", text="N-Rotate")
        layout.menu("resize.normal_menu", text="N-Scale")

        ###space###
        if context.mode == 'EDIT_MESH':

            layout.separator()

            layout.operator('mesh.rot_con', 'Face-Rotation')


class Translate_Normal_Menu(bpy.types.Menu):
    """Translate Normal Constraint"""
    bl_label = "Translate Normal Constraint"
    bl_idname = "translate.normal_menu"

    def draw(self, context):
        layout = self.layout

        # layout.label("___Move___")

        props = layout.operator("transform.transform", text="X-Axis")
        props.mode = 'TRANSLATION'
        props.constraint_axis = (True, False, False)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'

        props = layout.operator("transform.transform", text="Y-Axis")
        props.mode = 'TRANSLATION'
        props.constraint_axis = (False, True, False)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'

        props = layout.operator("transform.transform", text="Z-Axis")
        props.mode = 'TRANSLATION'
        props.constraint_axis = (False, False, True)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'


class Resize_Normal_Menu(bpy.types.Menu):
    """Resize Normal Constraint"""
    bl_label = "Resize Normal Constraint"
    bl_idname = "resize.normal_menu"

    def draw(self, context):
        layout = self.layout

        # layout.label("___Scale___")

        props = layout.operator("transform.resize", text="X-Axis")
        props.constraint_axis = (True, False, False)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'

        props = layout.operator("transform.resize", text="Y-Axis")
        props.constraint_axis = (False, True, False)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'

        props = layout.operator("transform.resize", text="Z-Axis")
        props.constraint_axis = (False, False, True)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'

        props = layout.operator("transform.resize", text="XY-Axis")
        props.constraint_axis = (True, True, False)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'


class Rotate_Normal_Menu(bpy.types.Menu):
    """Rotate Normal Constraint"""
    bl_label = "Rotate Normal Constraint"
    bl_idname = "rotate.normal_menu"

    def draw(self, context):
        layout = self.layout

        # layout.label("___Rotate___")

        props = layout.operator("transform.rotate", text="X-Axis")
        props.constraint_axis = (True, False, False)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'

        props = layout.operator("transform.rotate", text="Y-Axis")
        props.constraint_axis = (False, True, False)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'

        props = layout.operator("transform.rotate", text="Z-Axis")
        props.constraint_axis = (False, False, True)
        props.constraint_orientation = 'NORMAL'
        props.snap_target = 'ACTIVE'


class AlignNormal(bpy.types.Operator):
    """Align selected Mesh to active Face in Normal Z Direction"""
    bl_idname = "mesh.align_normal"
    bl_label = "Align to Normal"
    bl_options = {'REGISTER', 'UNDO'}

    manipul = bpy.props.BoolProperty(name="Set Normal Orientation", description="Orientation", default=False)

    def execute(self, context):
        bpy.ops.view3d.pivot_active()
        bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(self.manipul):
            bpy.ops.space.normal()

        return {'FINISHED'}


# -------------------------------------------------


def transform_normal_draw(self, context):
    layout = self.layout
    col = layout.column(align=True)
    #col.label("Transform with Normal Axis Constraint")
    col.menu("translate.normal_menu", text="N-Translate")
    col.menu("rotate.normal_menu", text="N-Rotate")
    col.menu("resize.normal_menu", text="N-Scale")
    if context.mode == 'EDIT_MESH':
        col.operator("mesh.align_normal", text="N-Align")

    col.separator()


######------------################################################################
######  Registry  ################################################################


def register():
    bpy.utils.register_class(Translate_Normal_Menu)
    bpy.utils.register_class(Resize_Normal_Menu)
    bpy.utils.register_class(Rotate_Normal_Menu)
    bpy.utils.register_class(AlignNormal)

    bpy.types.VIEW3D_PT_tools_transform.append(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_transform_mesh.append(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_transform_curve.append(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_transform_surface.append(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_mballedit.append(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_armatureedit_transform.append(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_latticeedit.append(transform_normal_draw)
    bpy.types.VIEW3D_MT_transform_object.prepend(transform_normal_draw)
    bpy.types.VIEW3D_MT_transform.prepend(transform_normal_draw)


def unregister():

    bpy.utils.unregister_class(Translate_Normal_Menu)
    bpy.utils.unregister_class(Resize_Normal_Menu)
    bpy.utils.unregister_class(Rotate_Normal_Menu)
    bpy.utils.unregister_class(AlignNormal)

    bpy.types.VIEW3D_PT_tools_transform.remove(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_transform_mesh.remove(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_transform_curve.remove(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_transform_surface.remove(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_mballedit.remove(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_armatureedit_transform.remove(transform_normal_draw)
    bpy.types.VIEW3D_PT_tools_latticeedit.remove(transform_normal_draw)
    bpy.types.VIEW3D_MT_transform_object.remove(transform_normal_draw)
    bpy.types.VIEW3D_MT_transform.remove(transform_normal_draw)


if __name__ == "__main__":
    register()
