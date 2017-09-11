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


####### Material Menu ###################

class WKST_Material_Menu(bpy.types.Menu):
    """Material / Object Color"""
    bl_label = "Material Display"
    bl_idname = "wkst.material_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.material_add", text="Material", icon='ZOOMIN')
        layout.operator("object.material_slot_remove", text="Material", icon="ZOOMOUT")

        layout.separator()

        layout.label("Object Color", icon="TRIA_DOWN")
        layout.prop(context.object, "color", text="")

        layout.separator()

        layout.operator("material.remove", text="Remove All", icon="ZOOMOUT")


####### Wire Menu ###################

class WKST_WIRE_Menu(bpy.types.Menu):
    """Wire Display"""
    bl_label = "Wire Display"
    bl_idname = "wkst.wire_menu"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        layout.operator("object.wire_all", text="Wire all", icon='WIRE')

        if context.mode == 'OBJECT':
            layout.separator()

            layout.operator("view3d.display_wire_on", "Wire Single on", icon='MESH_GRID')
            layout.operator("view3d.display_wire_off", "Wire Single off", icon='MESH_PLANE')

            layout.separator()

            op = layout.operator("super_grouper.change_selected_objects", text="Wire Shade", icon='GHOST_ENABLED')
            op.sg_objects_changer = 'WIRE_SHADE'

            op = layout.operator("super_grouper.change_selected_objects", text="Material Shade", icon='GHOST_DISABLED')
            op.sg_objects_changer = 'MATERIAL_SHADE'


####### Shading Menu ###################

class WKST_SHADE_Menu(bpy.types.Menu):
    """Shading Menu"""
    bl_label = "Shading Menu"
    bl_idname = "wkst.shade_menu"

    def draw(self, context):
        layout = self.layout

        if context.mode == 'OBJECT':
            layout.operator("object.shade_flat", text="Flat", icon="MESH_CIRCLE")
            layout.operator("object.shade_smooth", text="Smooth", icon="SMOOTH")

        else:
            layout.operator("mesh.faces_shade_flat", text="Flat", icon="MESH_CIRCLE")
            layout.operator("mesh.faces_shade_smooth", text="Smooth", icon="SMOOTH")

            layout.separator()

            layout.operator("mesh.mark_seam", icon="UV_EDGESEL").clear = False
            layout.operator("mesh.mark_seam", text="Clear Seam").clear = True

            layout.separator()

            layout.operator("mesh.mark_sharp", icon="SNAP_EDGE").clear = False
            layout.operator("mesh.mark_sharp", text="Clear Sharp").clear = True

            layout.separator()

            layout.operator("transform.edge_crease")
            layout.operator("transform.edge_bevelweight")

            layout.separator()

            if bpy.app.build_options.freestyle and not context.scene.render.use_shading_nodes:
                layout.operator("mesh.mark_freestyle_edge").clear = False
                layout.operator("mesh.mark_freestyle_edge", text="Clear Freestyle Edge").clear = True


####### Normal Menu ###################

class WKST_Normals_Menu(bpy.types.Menu):
    """Normals Menu"""
    bl_label = "Normals Menu"
    bl_idname = "wkst.normals_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("mesh.flip_normals", text="Flip Normals", icon="FILE_REFRESH")
        layout.operator("mesh.normals_make_consistent", text="Recalculate Normals", icon='SNAP_NORMAL')

        layout.separator()

        layout.operator("mesh.normals_make_consistent", text="Rec-Inside").inside = True
        layout.operator("mesh.normals_make_consistent", text="Rec-Outside").inside = False


class WKST_Normal_Menu(bpy.types.Menu):
    """Douple Side / AutoSmooth"""
    bl_label = "Normals Menu"
    bl_idname = "wkst.normal_menu"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.active_object.data, "show_double_sided", icon="GHOST")

        layout.separator()

        layout.prop(context.active_object.data, "use_auto_smooth", icon="AUTO")
       # layout.active = context.active_object.data.use_auto_smooth
        layout.prop(context.active_object.data, "auto_smooth_angle", text="Angle")


####### Mesh Check Menu ###################

class WKST_MESH_CHECK_Menu(bpy.types.Menu):
    """Mesh Check Tools"""
    bl_label = "Mesh Check"
    bl_idname = "wkst.meshcheck_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.add_materials", text="Display color", icon='GROUP_VCOL')
        layout.operator("object.remove_materials", text="Hidde color", icon='GROUP_VERTEX')

        if context.mode == 'EDIT_MESH':

            layout.separator()

            layout.prop(context.window_manager.border_lines, "borderlines_use")
            layout.prop(context.window_manager.border_lines, "custom_color_use", text="Border Color")

            layout.separator()

            layout.prop(context.window_manager.preselect, "preselect_use")
            layout.prop(context.window_manager.preselect, "depth_test")


####### Mesh Display Menu ##################

class WKST_EXT_Meshdisplay_Menu(bpy.types.Menu):
    """Mesh Display"""
    bl_label = "Mesh Display"
    bl_idname = "wkst_ext_menu.meshdisplay"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.object, "show_x_ray", text="X-Ray", icon="META_CUBE")
        layout.prop(context.space_data, "show_backface_culling", text="Backface", icon="OUTLINER_OB_LATTICE")

        if context.mode == 'EDIT_MESH':

            layout.prop(context.space_data, "show_occlude_wire", text="Hidden", icon="OUTLINER_DATA_LATTICE")
            layout.prop(context.space_data, "use_occlude_geometry", text="Limit 2 Visible", icon='ORTHO')


class WKST_Meshdisplay_Menu(bpy.types.Menu):
    """Mesh Display"""
    bl_label = "Mesh Display"
    bl_idname = "wkst.meshdisplay_menu"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        obj_type = obj.type
        is_geometry = (obj_type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'})
        is_wire = (obj_type in {'CAMERA', 'EMPTY'})
        is_empty_image = (obj_type == 'EMPTY' and obj.empty_draw_type == 'IMAGE')
        is_dupli = (obj.dupli_type != 'NONE')

        layout.prop(context.object, "show_x_ray", text="X-Ray", icon="META_CUBE")
        layout.prop(context.space_data, "show_backface_culling", text="Backface", icon="OUTLINER_OB_LATTICE")

        if context.mode == 'EDIT_MESH':
            layout.prop(context.space_data, "show_occlude_wire", text="Hidden", icon="OUTLINER_DATA_LATTICE")
            layout.prop(context.space_data, "use_occlude_geometry", text="Limit 2 Visible", icon='ORTHO')

        layout.separator()

        if context.space_data.viewport_shade == 'SOLID':
            layout.prop(context.space_data, "use_matcap", emboss=False)
            if context.space_data.use_matcap:
                layout.template_icon_view(context.space_data, "matcap_icon")

        layout.separator()

        if obj and obj.mode == 'OBJECT':
            if obj_type == 'MESH' or is_empty_image:
                layout.prop(obj, "show_transparent", text="Transparency", emboss=False)

        layout.separator()

        if obj and obj.mode == 'OBJECT':
            layout.prop(obj, "show_bounds", text="Bounds", emboss=False)
            layout.prop(obj, "draw_bounds_type", text="", icon="BBOX", emboss=False)

            layout.separator()

        if is_geometry:
            layout.prop(obj, "show_texture_space", text="Texture Space", emboss=False)

        if is_wire:
            # wire objects only use the max. draw type for duplis
            layout.active = is_dupli
            layout.label(text="Maximum Dupli Draw Type:")
        else:
            layout.label(text="Maximum Draw Type:")
        layout.prop(obj, "draw_type", text="", icon="BRUSH_DATA", emboss=False)

        layout.separator()

        layout.menu("wkst.mesh_overlays", text="Mesh Overlays", icon="PREFERENCES")


####### Display Menu ##################

class WKST_Display_Menu(bpy.types.Menu):
    """Display Menu"""
    bl_label = "Display Menu"
    bl_idname = "wkst.display_menu"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.object, "show_axis", text="Axis")
        layout.prop(context.object, "show_name", text="Name")

        layout.separator()

        layout.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="GROUP")
        layout.prop(context.space_data, "show_only_render", text="Render", icon="RESTRICT_RENDER_ON")
        layout.prop(context.space_data, "show_world", "World", icon="WORLD")

        layout.separator()

        layout.prop(context.space_data, "show_floor", text="Grid", icon="GRID")
        layout.menu("wkst.gridaxis_menu", text="Axis XYZ")

        layout.separator()

        layout.prop(context.space_data, "show_outline_selected")
        layout.prop(context.space_data, "show_all_objects_origin")
        layout.prop(context.space_data, "show_relationship_lines")


####### Grid Menu ##################

class WKST_Grid_Axis_Menu(bpy.types.Menu):
    """Axis Menu"""
    bl_label = "Axis"
    bl_idname = "wkst.gridaxis_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("wkst.grid_axis_on", icon="MANIPUL")
        layout.operator("wkst.grid_axis_off")

        layout.separator()

        layout.prop(context.space_data, "show_axis_x", text="X", toggle=True)
        layout.prop(context.space_data, "show_axis_y", text="Y", toggle=True)
        layout.prop(context.space_data, "show_axis_z", text="Z", toggle=True)


class WKST_Grid_OFF(bpy.types.Operator):
    """All Axis off"""
    bl_idname = "wkst.grid_axis_off"
    bl_label = "All Axis off"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.context.space_data.show_axis_x = False
        bpy.context.space_data.show_axis_y = False
        bpy.context.space_data.show_axis_z = False

        return {'FINISHED'}


class WKST_Grid_ON(bpy.types.Operator):
    """"All Axis on"""
    bl_idname = "wkst.grid_axis_on"
    bl_label = "All Axis on"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.context.space_data.show_axis_x = True
        bpy.context.space_data.show_axis_y = True
        bpy.context.space_data.show_axis_z = True

        return {'FINISHED'}


#######  Mesh Overlay Menu ##################

class WKST_MeshOverlays_Menu(bpy.types.Menu):
    """Mesh Overlays"""
    bl_label = "Mesh Overlays"
    bl_idname = "wkst.mesh_overlays"

    def draw(self, context):
        layout = self.layout

        with_freestyle = bpy.app.build_options.freestyle

        mesh = context.active_object.data
        scene = context.scene

        layout.prop(mesh, "show_faces", text="Faces")
        layout.prop(mesh, "show_edges", text="Edges")
        layout.prop(mesh, "show_edge_crease", text="Creases")
        layout.prop(mesh, "show_weight", text="Weights")

        if with_freestyle:
            layout.prop(mesh, "show_edge_seams", text="Seams")

        if not with_freestyle:
            layout.prop(mesh, "show_edge_seams", text="Seams")

        layout.prop(mesh, "show_edge_sharp", text="Sharp")
        layout.prop(mesh, "show_edge_bevel_weight", text="Bevel")

        if with_freestyle:
            layout.prop(mesh, "show_freestyle_edge_marks", text="Edge Marks")
            layout.prop(mesh, "show_freestyle_face_marks", text="Face Marks")

        if bpy.app.debug:
            layout.prop(mesh, "show_extra_indices")


######  Flymode  #####################

class Navigatestop(bpy.types.Operator):
    """Navigate Stop"""
    bl_idname = "view3d.fast_navigate_stop_new"
    bl_label = "Navigate Stop"

    def execute(self, context):
        bpy.ops.view3d.fast_navigate_stop()
        bpy.context.space_data.viewport_shade = 'SOLID'

        return {'FINISHED'}

bpy.utils.register_class(Navigatestop)


class View3D_Modifly(bpy.types.Menu):
    """Fast Navigate"""
    bl_label = "Fast Navigate"
    bl_idname = "wkst.modifly"

    def draw(self, context):
        active_obj = context.active_object
        layout = self.layout

        scene = context.scene

        layout.operator("view3d.fast_navigate_operator", icon="MOD_SOFT")
        layout.operator("view3d.fast_navigate_stop_new")

        layout.separator()

        layout.prop(scene, "OriginalMode", "")

        layout.prop(scene, "FastMode", "")

        layout.separator()

        layout.prop(scene, "EditActive", "Edit mode")

        layout.separator()

        layout.prop(scene, "Delay")
        layout.prop(scene, "DelayTimeGlobal")

        layout.separator()

        layout.prop(scene, "ShowParticles")
        layout.prop(scene, "ParticlesPercentageDisplay")

bpy.utils.register_class(View3D_Modifly)


######------------##############################
######  Registry  ##############################

def register():

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
