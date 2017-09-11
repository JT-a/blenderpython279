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

# bl_info = {
#    "name": "SFC Retopo",
#    "author": "mkbreuer",
#    "version": (0, 1, 0),
#    "blender": (2, 76, 0),
#    "location": "View3D > Toolbar > SFC Retopo",
#    "warning": "",
#    "description": "Toolkit for the Main Panel",
#    "wiki_url": "",
#    "category": "",
#}


import bpy
from bpy import*


#########################################################################################################

class Dropdown_Wkst_Sculpt_Props(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.wkst_window_sculpt
    """

    ### Sculpt ###
    display_sculpt_brush = bpy.props.BoolProperty(name="Open", description="Open", default=False)
    display_sculpt_edit = bpy.props.BoolProperty(name="Open", description="Open", default=False)
    display_sculpt_mask = bpy.props.BoolProperty(name="Open", description="Open", default=False)
    display_sculpt_visual = bpy.props.BoolProperty(name="Open", description="Open", default=False)

bpy.utils.register_class(Dropdown_Wkst_Sculpt_Props)
bpy.types.WindowManager.wkst_window_sculpt = bpy.props.PointerProperty(type=Dropdown_Wkst_Sculpt_Props)

#########################################################################################################


def draw_wkst_sculpt_ui(self, context, layout):
    lt = context.window_manager.wkst_window_sculpt

    obj = context.object
    scene = context.scene
    scn = context.scene
    rs = bpy.context.scene
    ob = context.object
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout = self.layout.column_flow(1)


# Title

    obj = context.active_object
    if obj:
        obj_type = obj.type

        if obj_type in {'MESH'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("MESH SCULPTING")

        if obj_type in {'LATTICE'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("LATTICE DEFORM")

        if obj_type in {'CURVE'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("CURVE EDITING")

        if obj_type in {'SURFACE'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("SURFACE EDITING")

        if obj_type in {'META'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("META EDITING")

        if obj_type in {'FONT'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("FONT EDITING")

        if obj_type in {'ARMATURE'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("FONT EDITING")

        if obj_type in {'EMPTY'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("FONT EDITING")

        if obj_type in {'CAMERA'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("CAMERA EDITING")

        if obj_type in {'LAMP'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("LAMP EDITING")

        if obj_type in {'SPEAKER'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("SPEAKER EDITING")


# Brushes

        if lt.display_sculpt_brush:

            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculpt_brush", text="", icon='TRIA_DOWN')
            row.label("Brushes...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculpt_brush", text="", icon='TRIA_RIGHT')
            row.label("Brushes...")

            row.menu("wkst_menu.load_brushes", text="", icon='IMASEL')
            row.menu("wkst_menu.quick_brush", text="", icon='VPAINT_HLT')

        if lt.display_sculpt_brush:
            box = layout.box().column(1)
            row = box.row(1)

            spl = row.split()
            row = spl.column()
            row.template_ID_preview(context.tool_settings.sculpt, "brush", new="brush.add", rows=3, cols=8)

            box.separator()

            row = box.row(1)
            row.prop(context.tool_settings.sculpt, "use_symmetry_x", text="X", toggle=True)
            row.prop(context.tool_settings.sculpt, "use_symmetry_y", text="Y", toggle=True)
            row.prop(context.tool_settings.sculpt, "use_symmetry_z", text="Z", toggle=True)

            box.separator()

            ups = context.tool_settings.unified_paint_settings

            row = box.row(1)
            if ((ups.use_unified_size and ups.use_locked_size) or
                    ((not ups.use_unified_size) and brush.use_locked_size)):
                row.prop(ups, "use_locked_size", "", icon='LOCKED')
                row.prop(ups, "unprojected_radius", slider=True, text="Radius")
                row.prop(ups, "use_pressure_size", text="", toggle=True, icon_only=True)
            else:
                row.prop(ups, "use_locked_size", "", icon='UNLOCKED')
                row.prop(ups, "size", slider=True, text="Radius")
                row.prop(ups, "use_pressure_size", text="", toggle=True, icon_only=True)

            row = box.row(1)
            row.prop(context.tool_settings.sculpt.brush, "use_space_attenuation", toggle=True, text="")
            row.prop(context.tool_settings.sculpt.brush, "strength", text="Strength", slider=True)
            row.prop(context.tool_settings.sculpt.brush, "use_pressure_strength", text="", toggle=True, icon_only=True)

            row = box.row(1)
            row.prop(context.tool_settings.sculpt.brush, "use_frontface", text="", icon="SNAP_FACE")
            row.prop(context.tool_settings.sculpt.brush, "auto_smooth_factor", slider=True)
            row.prop(context.tool_settings.sculpt.brush, "use_inverse_smooth_pressure", toggle=True, text="")

            box.separator()

            row = box.row(1)
            row.prop(context.tool_settings.sculpt.brush, "direction", expand=True)

            box = layout.box().column(1)
            row = box.row(1)
            row.alignment = 'CENTER'
            row.label('QuickSet Brush')

            row = box.row(1)
            row.operator("disable.quicksetbrush", "Disable", icon='CHECKBOX_DEHLT')
            row.operator("enable.quicksetbrush", "Enable", icon='CHECKBOX_HLT')

            box = layout.box().column(1)
            row = box.row(1)
            if context.sculpt_object.use_dynamic_topology_sculpting:
                row.operator("sculpt.dynamic_topology_toggle", icon='X', text="Disable Dyntopo")
            else:
                row.operator("sculpt.dynamic_topology_toggle", icon='SCULPT_DYNTOPO', text="Enable Dyntopo")

            if context.sculpt_object.use_dynamic_topology_sculpting:

                row = box.row(1)
                row.prop(context.tool_settings.sculpt, "detail_refine_method", text="")
                row.prop(context.tool_settings.sculpt, "detail_type_method", text="")

                row = box.row(1)
                if (context.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
                    row.prop(context.tool_settings.sculpt, "constant_detail", text="const.")
                    row.operator("sculpt.sample_detail_size", text="", icon='EYEDROPPER')
                else:
                    row.prop(context.tool_settings.sculpt, "detail_size", text="detail")

                box.separator()
                row = box.row(1)
                row.prop(context.tool_settings.sculpt, "use_smooth_shading", "Smooth", icon="MATSPHERE")

                row.operator("sculpt.optimize")
                if (context.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
                    row = box.row(1)
                    row.operator("sculpt.detail_flood_fill")

                row = box.row(1)
                row.prop(context.tool_settings.sculpt, "symmetrize_direction", "")
                row.operator("sculpt.symmetrize")

            box = layout.box().column(1)
            row = box.row(1)
            row.operator('texture.load_single_brush', text='Single Brush', icon="IMAGE_COL")
            row.operator('texture.load_brushes', text='Brush Folder', icon="FILE_FOLDER")


# Tools

        if lt.display_sculpt_edit:

            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculpt_edit", text="", icon='TRIA_DOWN')
            row.label("Sculpt...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculpt_edit", text="", icon='TRIA_RIGHT')

            row.label("Sculpt...")

            row.operator("sculpt.remesh", text='', icon='MOD_REMESH')
            row.menu("sculpt.edit_menu", text='', icon='SCULPTMODE_HLT')

        if lt.display_sculpt_edit:

            box = layout.box()

            row = box.row(1)
            row.operator("sculpt.remesh", text='Remesh', icon='MOD_REMESH')
            row.prop(context.window_manager, 'remeshPreserveShape', text="Preserve Shape")

            row = box.row(1)
            row.prop(context.window_manager, 'remeshDepthInt', text="Depth")
            row.prop(context.window_manager, 'remeshSubdivisions', text="Subdivisions")

            box = layout.box().column(1)
            row = box.row(1)
            row.operator("sculpt.geometry_smooth", text="Smooth")
            row.operator("sculpt.geometry_laplacian_smooth", text="Laplacian")

            row = box.row(1)
            row.operator("sculpt.geometry_decimate", text="Decimate")
            row.operator("sculpt.geometry_displace", text="Displace")

            row = box.row(1)
            row.operator("sculpt.geometry_subdivide_faces", text="Subdiv")
            row.operator("sculpt.geometry_subdivide_faces_smooth", text="SmoothDivide")

            row = box.row(1)
            row.operator("sculpt.geometry_beautify_faces", text="Beautify")


# Mask

        if lt.display_sculpt_mask:

            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculpt_mask", text="", icon='TRIA_DOWN')
            row.label("Mask...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculpt_mask", text="", icon='TRIA_RIGHT')
            row.label("Mask...")
            row.operator("boolean.mask_extract", text="", icon='MOD_MASK')

        if lt.display_sculpt_mask:

            box = layout.box()

            row = box.row(1)
            row.operator("boolean.mask_extract", text="Extract Mask", icon='MOD_MASK')

            if context.object.vertex_groups.active:
                box = layout.box().column(1)
                row = box.row(1)
                row.template_list("MESH_UL_vgroups", "", context.object, "vertex_groups", context.object.vertex_groups, "active_index", rows=2)

                row = box.row(1)
                row.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
                row.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
                row.operator("object.vertex_group_add", icon='ZOOMIN', text="")
                row.operator("object.vertex_group_remove", icon='ZOOMOUT', text="").all = False
                row.menu("MESH_MT_vertex_group_specials", icon='DOWNARROW_HLT', text="")

            box = layout.box().column(1)
            row = box.row(1)
            row.operator("mesh.masktovgroup", text="Create Vertex Group", icon='GROUP_VERTEX')

            row = box.row(1)
            row.operator("mesh.masktovgroup_remove", text="Remove", icon='DISCLOSURE_TRI_DOWN')
            row.operator("mesh.masktovgroup_append", text="Append", icon='DISCLOSURE_TRI_RIGHT')

            box = layout.box().column(1)
            row = box.row(1)
            row.operator("mesh.vgrouptomask", text="Create Mask", icon='MOD_MASK')

            row = box.row(1)
            row.operator("mesh.vgrouptomask_remove", text="Remove", icon='DISCLOSURE_TRI_DOWN')
            row.operator("mesh.vgrouptomask_append", text="Append", icon='DISCLOSURE_TRI_RIGHT')

            box = layout.box().column(1)
            row = box.row(1)
            row.operator("mesh.mask_from_edges", text="Mask by Edges", icon='MOD_MASK')

            row = box.column(1)
            row.prop(bpy.context.window_manager, "mask_edge_angle", text="Edge Angle", icon='MOD_MASK', slider=True)
            row.prop(bpy.context.window_manager, "mask_edge_strength", text="Mask Strength", icon='MOD_MASK', slider=True)

            box = layout.box().column(1)
            row = box.row(1)
            row.operator("mesh.mask_from_cavity", text="Mask by Cavity", icon='MOD_MASK')

            row = box.column(1)
            row.prop(bpy.context.window_manager, "mask_cavity_angle", text="Cavity Angle", icon='MOD_MASK', slider=True)
            row.prop(bpy.context.window_manager, "mask_cavity_strength", text="Mask Strength", icon='MOD_MASK', slider=True)

            box = layout.box().column(1)
            row = box.row(1)
            row.operator("mesh.mask_smooth_all", text="Mask Smooth", icon='MOD_MASK')

            row = box.column(1)
            row.prop(bpy.context.window_manager, "mask_smooth_strength", text="Mask Smooth Strength", icon='MOD_MASK', slider=True)


# Visuals

        if lt.display_sculpt_visual:

            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculpt_visual", text="", icon='TRIA_DOWN')
            row.label("Visual...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculpt_visual", text="", icon='TRIA_RIGHT')

            row.label("Visual...")

            row.menu("wkst.modifly", '', icon="MOD_SOFT")
            row.menu("wkst.display_menu", text="", icon="UI")
            row.menu("wkst.meshdisplay_menu", text="", icon="META_CUBE")
            row.menu("wkst.wire_menu", text="", icon='WIRE')

        if lt.display_sculpt_visual:

            box = layout.box().column(1)

            row = box.row(1)
            row.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="GROUP")
            row.prop(context.space_data, "use_matcap", icon="MATCAP_22")
            if context.space_data.use_matcap:
                row = col_top.row(align=True)
                row.scale_y = 0.2
                row.scale_x = 0.5
                row.template_icon_view(context.space_data, "matcap_icon")

            box = layout.box().column(1)
            row = box.row(1)
            row.prop(context.space_data, "show_only_render", text="Render", icon="RESTRICT_RENDER_ON")
            row.prop(context.space_data, "show_floor", text="Grid", icon="GRID")

            row = box.row(1)
            row.prop(context.space_data, "show_world", "World", icon="WORLD")

            sub = row.row(1)
            sub.scale_x = 0.335
            sub.prop(context.space_data, "show_axis_x", text="X", toggle=True)
            sub.prop(context.space_data, "show_axis_y", text="Y", toggle=True)
            sub.prop(context.space_data, "show_axis_z", text="Z", toggle=True)


# History

        box = layout.box()
        row = box.row(1)
        row.operator('wm.path_open', text='', icon='FILESEL').filepath = "C:\\Users\Public\Documents\Blender_Dokumentation"
        row.operator("view3d.ruler", text="Ruler")
        row.operator("ed.undo_history", text="History")
        row.operator("ed.undo", text="", icon="LOOP_BACK")
        row.operator("ed.redo", text="", icon="LOOP_FORWARDS")


# Register

class Operator(bpy.types.Operator):
    bl_idname = "object.operator"
    bl_label = "Operator"

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_module(__name__)

    try:
        del bpy.types.WindowManager.wkst_window_sculpt
    except:
        pass

if __name__ == "__main__":
    register()
