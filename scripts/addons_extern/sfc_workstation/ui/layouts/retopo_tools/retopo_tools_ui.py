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


NUM_LAYERS = 20
SCENE_SGR = '#SGR'
UNIQUE_ID_NAME = 'sg_belong_id'


############----------------------############
############  Props for DROPDOWN  ############
############----------------------############

class DropdownRetopoToolProps(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.retopowindow
    """

    ### Objectmode ###

    display_geom = bpy.props.BoolProperty(name="Add", description="Display Add Geometry Tools", default=False)
    display_selectobm = bpy.props.BoolProperty(name="Selection", description="Display Selection Tools", default=False)
    display_select = bpy.props.BoolProperty(name="Selection", description="Display Selection Tools", default=False)
    display_modif = bpy.props.BoolProperty(name="Modifier Tools", description="Display Modifier Tools", default=False)
    display_mirrcut = bpy.props.BoolProperty(name="Auto Mirror Cut", description="Display Auto Mirror Cut Tools", default=False)
    display_normal = bpy.props.BoolProperty(name="Normals", description="Display Face & Vertex Normal Tools", default=False)
    display_shade = bpy.props.BoolProperty(name="Visual", description="Display Visualisation & Shading Tools", default=False)
    display_check = bpy.props.BoolProperty(name="Mesh Check", description="Display Mesh Check Tools", default=False)
    display_bsurf = bpy.props.BoolProperty(name="Bsurface", description="Display Bsurface Tools", default=False)
    display_setgeom = bpy.props.BoolProperty(name="Add Primitive", description="Display Add Primitive Tools", default=False)
    display_curvegeo = bpy.props.BoolProperty(name="Curve Shape", description="Display Curve Shape Tools", default=False)
    display_placegeom = bpy.props.BoolProperty(name="Copy & Rearrange Objects", description="Display Copy & Rearrange Objects Tools", default=False)
    display_placepivot = bpy.props.BoolProperty(name="Pivot & Origin", description="Pivot & Origin Tools", default=False)
    display_snapshot = bpy.props.BoolProperty(name="SnapShot Mesh", description="SnapShot Mesh Tools", default=False)
    display_view = bpy.props.BoolProperty(name="View", description="View Tools", default=False)

    ### Editmode ###
    display_editselect = bpy.props.BoolProperty(name="Selection", description="Display Selection Tools", default=False)
    display_editpivot = bpy.props.BoolProperty(name="Pivot & Origin", description="Pivot & Origin Tools", default=False)
    display_vertalign = bpy.props.BoolProperty(name="Align", description="Display Vertex Align Tools", default=False)
    display_vertpivot = bpy.props.BoolProperty(name="Pivot & Origin", description="Pivot & Origin Tools", default=False)
    display_subdiv = bpy.props.BoolProperty(name="Subdivide", description="Display Subdivide & Cutting Tools", default=False)
    display_vertedit = bpy.props.BoolProperty(name="Edit", description="Display Edit Tools", default=False)
    display_extrude = bpy.props.BoolProperty(name="Extrude", description="Display Extrusion Tools", default=False)

    display_bool = bpy.props.BoolProperty(name="Boolean, Join, Convert", description="Display Boolean, Join, Convert Tools", default=False)
    display_bool2 = bpy.props.BoolProperty(name="Boolean, Join, Convert", description="Display Boolean, Join, Convert Tools", default=False)
    display_sgrouper = bpy.props.BoolProperty(name="SGrouper", description="Display Group Tools", default=False)
    display_curveloft = bpy.props.BoolProperty(name="Curve Tools 2", description="Display Curve Tools 2", default=False)
    display_curveinfo = bpy.props.BoolProperty(name="Curve Tools 2", description="Display Curve Tools 2", default=False)
    display_rename = bpy.props.BoolProperty(name="Rename Tool", description="Display Rename Tool", default=False)
    display_miraedit = bpy.props.BoolProperty(name="Mira Edit Tools", description="Display Mira Edit Tools", default=False)
    display_miracurve = bpy.props.BoolProperty(name="Mira Edit Tools", description="Display Mira Edit Tools", default=False)
    display_arrayobj = bpy.props.BoolProperty(name="Array Tools", description="Display Array Tools", default=False)
    display_transform = bpy.props.BoolProperty(name="Transform Tools", description="Display Transform Tools", default=False)
    display_bboxback = bpy.props.BoolProperty(name="BBox Origin", description="Display BBox Origin Tools", default=False)
    display_bboxmiddle = bpy.props.BoolProperty(name="BBox Origin", description="Display BBox Origin Tools", default=False)
    display_bboxfront = bpy.props.BoolProperty(name="BBox Origin", description="Display BBox Origin Tools", default=False)
    display_imexport = bpy.props.BoolProperty(name="Import", description="Display Import Tools", default=False)

    ### Sculpt ###
    display_sculptmask = bpy.props.BoolProperty(name="Mask", description="Display Sculpt Mask Tools", default=False)
    display_sculptbrush = bpy.props.BoolProperty(name="Sculpt Brushes", description="Display Sculpt Brushes", default=False)
    display_deform = bpy.props.BoolProperty(name="Deform", description="Display Deform Tools", default=False)


bpy.utils.register_class(DropdownRetopoToolProps)
bpy.types.WindowManager.retopowindow = bpy.props.PointerProperty(type=DropdownRetopoToolProps)


############-----------------------------############
############  DROPDOWN Layout for PANEL  ############
############-----------------------------############


def draw_retopo_tools_ui(self, context, layout):
    lt = context.window_manager.retopowindow

    obj = context.object
    scene = context.scene
    scn = context.scene
    rs = bpy.context.scene
    ob = context.object
    layout.operator_context = 'INVOKE_REGION_WIN'
    col = layout.column(align=True)

    if context.mode == 'OBJECT':
        box = layout.box().column(True)
        row = box.row(align=True)
        row.alignment = 'CENTER'
        sub = row.row(1)
        sub.scale_x = 1
        sub.menu("INFO_MT_mesh_add", text="", icon='OUTLINER_OB_MESH')
        sub.menu("INFO_MT_curve_add", text="", icon='OUTLINER_OB_CURVE')
        sub.menu("INFO_MT_surface_add", text="", icon='OUTLINER_OB_SURFACE')
        sub.menu("INFO_MT_metaball_add", text="", icon="OUTLINER_OB_META")
        sub.operator("object.camera_add", icon='OUTLINER_OB_CAMERA', text="")
        sub.menu("INFO_MT_armature_add", text="", icon="OUTLINER_OB_ARMATURE")

        row = box.row(align=True)
        row.alignment = 'CENTER'
        sub = row.row(1)
        sub.scale_x = 1
        sub.operator("object.empty_add", text="", icon="OUTLINER_OB_EMPTY")
        sub.operator("object.add", text="", icon="OUTLINER_OB_LATTICE").type = "LATTICE"
        sub.operator("object.text_add", text="", icon="OUTLINER_OB_FONT")
        sub.operator("object.lamp_add", icon='OUTLINER_OB_LAMP', text="")
        sub.operator("object.speaker_add", icon='OUTLINER_OB_SPEAKER', text="")
        sub.operator_menu_enum("object.effector_add", "type", text="", icon="SOLO_ON")

    if context.mode == 'EDIT_MESH':
        box = layout.box().column(True)
        row = box.row(align=True)
        row.alignment = 'CENTER'
        sub = row.row(1)
        sub.scale_x = 1.9
        sub.operator("mesh.primitive_plane_add", icon='MESH_PLANE', text="")
        sub.operator("mesh.primitive_cube_add", icon='MESH_CUBE', text="")
        sub.operator("mesh.primitive_circle_add", icon='MESH_CIRCLE', text="")
        sub.operator("mesh.primitive_uv_sphere_add", icon='MESH_UVSPHERE', text="")
        sub.operator("mesh.primitive_ico_sphere_add", icon='MESH_ICOSPHERE', text="")

        row = box.row(align=True)
        row.alignment = 'CENTER'
        sub = row.row(1)
        sub.scale_x = 1.9
        sub.operator("mesh.primitive_cylinder_add", icon='MESH_CYLINDER', text="")
        sub.operator("mesh.primitive_torus_add", icon='MESH_TORUS', text="")
        sub.operator("mesh.primitive_cone_add", icon='MESH_CONE', text="")
        sub.operator("mesh.primitive_grid_add", icon='MESH_GRID', text="")
        sub.operator("mesh.primitive_monkey_add", icon='MESH_MONKEY', text="")

        row = box.row(align=True)
        row.alignment = 'CENTER'
        row.scale_x = 1
        row.operator("mesh.add_curvebased_tube", text="", icon="CURVE_DATA")
        row.operator("mesh.autotubes", text="", icon="OUTLINER_DATA_EMPTY")
        row.operator("mesh.singleplane_x", text="X")
        row.operator("mesh.singleplane_y", text="Y")
        row.operator("mesh.singleplane_z", text="Z")
        row.operator("object.easy_lattice", text="", icon="OUTLINER_DATA_LATTICE")
        row.operator("mesh.singlevertex", text="", icon="STICKY_UVS_DISABLE")


##################
### Edit Pivot ###
##################

    ###space###
    box = layout.box()
    row = box.row(1)
    sub = row.row(1)
    sub.scale_x = 7
    sub.operator("view3d.pivot_bounding_box", "", icon="ROTATE")
    sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
    sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
    sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")
    sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
    if context.mode == 'OBJECT':
        row.menu("object.wkstdelete", text="", icon="PANEL_CLOSE")
    else:
        row.menu("mesh.cleandelete", text="", icon="PANEL_CLOSE")

########################
### Object Im-Export ###
########################

    ###space###
    if context.mode == 'OBJECT':

        ###space###
        if lt.display_imexport:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_imexport", text="", icon='TRIA_DOWN')
            row.label("Im-Export...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_imexport", text="", icon='TRIA_RIGHT')
            row.label("Im-Export...")

            row.operator("view3d.background_images_fast_import", text="", icon='IMAGE_DATA')
            row.menu("wkst.import_export", text="", icon='EXPORT')
            row.menu("wkst.link_append", text="", icon='APPEND_BLEND')

        ###space###
        if lt.display_imexport:
            ###space###
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(1)
            row.operator("view3d.background_images_fast_import", icon='IMAGE_DATA')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(1)
            row.alignment = 'CENTER'
            row.scale_x = 1.25
            row.menu("INFO_MT_file_import", text="Import", icon='EXPORT')
            row.menu("INFO_MT_file_export", text="Export", icon='IMPORT')
            row.menu("OBJECT_MT_selected_export", text="Export Selected", icon='IMPORT')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(1)
            row.operator("wm.link", text="Link", icon='LINK_BLEND')
            row.operator("wm.append", text="Append", icon='APPEND_BLEND')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.proxy_make")
            row.operator("object.make_local")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            pack_all = box.row()
            pack_all.operator("file.pack_all")
            pack_all.active = not bpy.data.use_autopack

            unpack_all = box.row()
            unpack_all.operator("file.unpack_all")
            unpack_all.active = not bpy.data.use_autopack

            icon = 'CHECKBOX_HLT' if bpy.data.use_autopack else 'CHECKBOX_DEHLT'
            row.operator("file.autopack_toggle", text="autom. Pack into .blend", icon=icon)

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("file.make_paths_relative")

            row = col_top.row(align=True)
            row.operator("file.make_paths_absolute")

            row = col_top.row(align=True)
            row.operator("file.report_missing_files")

            row = col_top.row(align=True)
            row.operator("file.find_missing_files")


##############
### Sculpt ###
##############

    if context.mode == 'SCULPT':
        ###space###
        if lt.display_sculptbrush:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculptbrush", text="", icon='TRIA_DOWN')
            row.label("Brushes...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculptbrush", text="", icon='TRIA_RIGHT')
            row.label("Brushes...")

            row.menu("wkst_menu.load_brushes", text="", icon='IMASEL')
            row.menu("wkst_menu.quick_brush", text="", icon='VPAINT_HLT')

        ###space###
        if lt.display_sculptbrush:
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


############
### View ###
############

    ###space###
    if lt.display_view:
        ###space###
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_view", text="", icon='TRIA_DOWN')
        row.label("3d-View...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_view", text="", icon='TRIA_RIGHT')
        row.label("3d-View...")

        row.operator("view3d.view_all", "", icon="ZOOM_OUT")
        row.operator("view3d.view_selected", "", icon="ZOOM_IN")
        row.operator("view3d.zoom_border", "", icon="BORDERMOVE")

    ###space###
    if lt.display_view:

        col = layout.column(align=True)
        box = col.column(align=True).box().column()
        col_top = box.column(align=True)

        row = col_top.column(align=True)
        row.operator("view3d.view_all", "All", icon="ZOOM_OUT")
        row.operator("view3d.view_center_cursor", text="Cursor", icon="ZOOM_PREVIOUS")
        row.operator("view3d.view_selected", "Selected", icon="ZOOM_IN")
        row.operator("view3d.zoom_border", "Zoom Border", icon="BORDERMOVE")

        col = layout.column(align=True)
        box = col.column(align=True).box().column()
        col_top = box.column(align=True)

        row = col_top.row(align=True)
        row.operator("view3d.localview", text="Global/Local")
        row.operator("view3d.view_persportho", text="Persp/Ortho")

        col = layout.column(align=True)
        box = col.column(align=True).box().column()
        col_top = box.column(align=True)

        row = col_top.row(align=True)
        row.label(text="View to Object:")
        row = col_top.row(align=True)
        row.prop(context.space_data, "lock_object", text="")


###################
### Retopo Geom ###
###################

    ###space###
    if context.mode == 'OBJECT':
        ###space###
        if lt.display_setgeom:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_setgeom", text="", icon='TRIA_DOWN')
            row.label("Retopo...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_setgeom", text="", icon='TRIA_RIGHT')
            row.label("Retopo...")

            row.menu("origin.retopo_menu", text="", icon='RETOPO')
            row.menu("object.bbox_retopo_menu", text="", icon="BBOX")

        ###space###
        if lt.display_setgeom:
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Object Origin")

            row = col_top.row(align=True)
            row.operator("mesh.emptyroom_cen", text="-> Center", icon='LAYER_ACTIVE')
            row = col_top.row(align=True)
            row.operator("mesh.emptyroom_sel", text="-> Selected", icon='LAYER_ACTIVE')

            row = col_top.row(align=True)
            row.operator("mesh.emptyxroom_cen", text="-> Center mirrored", icon='MOD_MIRROR')
            row = col_top.row(align=True)
            row.operator("mesh.emptyxroom_sel", text="-> Selected mirrored", icon='MOD_MIRROR')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(align=True)
            row.operator("object.bounding_box", text="Bounding Box", icon="MESH_CUBE")
            row.operator("object.bounding_boxers", text="Wire Bounding Box", icon="BBOX")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.scene, "AutoAlign_axis", text="Align Axis", expand=True)
            row = col_top.row(align=True)
            row.operator("bbox.align_vertices", text="Execute ZBox-Rectangle")


#################
### Selection ###
#################

    ###space###
    if context.mode == 'OBJECT':

        ###space###
        if lt.display_selectobm:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_selectobm", text="", icon='TRIA_DOWN')
            row.label("Select...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_selectobm", text="", icon='TRIA_RIGHT')
            row.label("Select...")

            row.menu("VIEW3D_MT_object_showhide", "", icon="VISIBLE_IPO_ON")
            row.operator("view3d.select_border", text="", icon="BORDER_RECT")
            row.operator("view3d.select_circle", text="", icon="BORDER_LASSO")

        ###space###
        if lt.display_selectobm:
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("view3d.select_border", text="Border", icon="BORDER_RECT")
            row.operator("view3d.select_circle", text="Cirlce", icon="BORDER_LASSO")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.move_to_layer", text="Move to Layer")
            row.menu("VIEW3D_MT_object_showhide", "Hide / Show", icon="VISIBLE_IPO_ON")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.select_all").action = 'TOGGLE'
            row.operator("object.select_all", text="Inverse").action = 'INVERT'

            row = col_top.row(align=True)
            row.operator("object.throughselected", text="Cycle through")
            row.operator("object.select_linked", text="Single Active").type = 'OBDATA'

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.select_random", text="Random")
            row.operator("object.select_mirror", text="Mirror")

            row = col_top.row(align=True)
            row.operator("object.select_by_layer", text="All by Layer")
            row.operator("object.select_camera", text="Camera")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.select_linked", text="Linked", icon="EXPORT")
            row.operator("object.select_grouped", text="Group", icon="EXPORT")

            row = col_top.row(align=True)
            row.operator("object.select_by_type", text="Type", icon="EXPORT")
            row.operator("object.select_pattern", text="Name", icon="EXPORT")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.menu("wkst.freezeall", text="Un-/ Freeze by Type", icon="FREEZE")

            row = col_top.row(align=True)
            row.operator("vfxtoolbox.defreeze_all_objects", text="UnFreeze all")
            row.operator("vfxtoolbox.freeze_selected_objects", text="Freeze")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("view3d.bbox_select", "BBox", icon="RESTRICT_SELECT_OFF")
            row.operator("view3d.bbox_select_wire", "WBox", icon="RESTRICT_SELECT_OFF")
            row.operator("view3d.bbox_select_zyl", "ZBox", icon="RESTRICT_SELECT_OFF")


######################
### Place Geometry ###
######################

    ###space###
    if context.mode == 'OBJECT':

        ###space###
        if lt.display_placepivot:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_placepivot", text="", icon='TRIA_DOWN')
            row.label("Pivot...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_placepivot", text="", icon='TRIA_RIGHT')

            row.label("Pivot...")
            #row.operator_menu_enum("object.origin_set", "type","", icon="LAYER_ACTIVE")
            row.menu("origin.setupmenu_obm", text="", icon="LAYER_ACTIVE")
            row.menu("wkst.snaptocursor", "", icon="FORCE_FORCE")
            row.menu("wkst.snaptoselect", "", icon="RESTRICT_SELECT_OFF")

        ###space###
        if lt.display_placepivot:
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator_menu_enum("object.origin_set", "type", text="Set Origin", icon="LAYER_ACTIVE")

            row = col_top.row(align=True)
            if lt.display_bboxback:
                row.scale_y = 1.2
                row.prop(lt, "display_bboxback", text="Back +Y", icon='TRIA_DOWN')

            else:
                row.scale_y = 1
                row.prop(lt, "display_bboxback", text="Back +Y", icon='TRIA_RIGHT')

            ###space###
            if lt.display_bboxback:
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                # Top
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubeback_cornertop_minus_xy", "", icon="LAYER_ACTIVE")  # "Back- Left -Top")
                row.operator("object.cubeback_edgetop_minus_y", "", icon="LAYER_ACTIVE")  # "Back - Top")
                row.operator("object.cubeback_cornertop_plus_xy", "", icon="LAYER_ACTIVE")  # "Back- Right -Top ")

                # Middle
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55
                row.operator("object.cubefront_edgemiddle_minus_x", "", icon="LAYER_ACTIVE")  # "Back- Left")
                row.operator("object.cubefront_side_plus_y", "", icon="LAYER_ACTIVE")  # "Back")
                row.operator("object.cubefront_edgemiddle_plus_x", "", icon="LAYER_ACTIVE")  # "Back- Right")

                # Bottom
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55
                row.operator("object.cubeback_cornerbottom_minus_xy", "", icon="LAYER_ACTIVE")  # "Back- Left -Bottom")
                row.operator("object.cubefront_edgebottom_plus_y", "", icon="LAYER_ACTIVE")  # "Back - Bottom")
                row.operator("object.cubeback_cornerbottom_plus_xy", "", icon="LAYER_ACTIVE")  # "Back- Right -Bottom")

                ###space###
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = box.column(1)

            ###space###
            if lt.display_bboxmiddle:
                row.scale_y = 1.2
                row.prop(lt, "display_bboxmiddle", text="Middle", icon='TRIA_DOWN')

            else:
                row.scale_y = 1
                row.prop(lt, "display_bboxmiddle", text="Middle", icon='TRIA_RIGHT')

            ###space1###
            if lt.display_bboxmiddle:
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                # Top
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_edgetop_minus_x", "", icon="LAYER_ACTIVE")  # "Middle - Left Top")
                row.operator("object.cubefront_side_plus_z", "", icon="LAYER_ACTIVE")  # "Top")
                row.operator("object.cubefront_edgetop_plus_x", "", icon="LAYER_ACTIVE")  # "Middle - Right Top")

                # Middle
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_side_minus_x", "", icon="LAYER_ACTIVE")  # "Left")
                obj = context.object
                if obj and obj.mode == 'EDIT':
                    row.operator("mesh.origincenter", text="", icon="LAYER_ACTIVE")
                else:
                    row.operator("object.origin_set", text="", icon="LAYER_ACTIVE").type = 'ORIGIN_GEOMETRY'

                row.operator("object.cubefront_side_plus_x", "", icon="LAYER_ACTIVE")  # "Right")

                # Bottom
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_edgebottom_minus_x", "", icon="LAYER_ACTIVE")  # "Middle - Left Bottom")
                row.operator("object.cubefront_side_minus_z", "", icon="LAYER_ACTIVE")  # "Bottom")
                row.operator("object.cubefront_edgebottom_plus_x", "", icon="LAYER_ACTIVE")  # "Middle - Right Bottom")

                ##############################
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)

            ###space1###

            if lt.display_bboxfront:
                row.scale_y = 1.2
                row.prop(lt, "display_bboxfront", text="Front -Y", icon='TRIA_DOWN')

            else:
                row.scale_y = 1
                row.prop(lt, "display_bboxfront", text="Front -Y", icon='TRIA_RIGHT')

            ###space1###
            if lt.display_bboxfront:
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                # Top
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_cornertop_minus_xy", "", icon="LAYER_ACTIVE")  # "Front- Left -Top"
                row.operator("object.cubeback_edgetop_plus_y", "", icon="LAYER_ACTIVE")  # "Front - Top"
                row.operator("object.cubefront_cornertop_plus_xy", "", icon="LAYER_ACTIVE")  # "Front- Right -Top"

                # Middle
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_edgemiddle_minus_y", "", icon="LAYER_ACTIVE")  # "Front- Left"
                row.operator("object.cubefront_side_minus_y", "", icon="LAYER_ACTIVE")  # "Front"
                row.operator("object.cubefront_edgemiddle_plus_y", "", icon="LAYER_ACTIVE")  # "Front- Right"

                # Bottom
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_cornerbottom_minus_xy", "", icon="LAYER_ACTIVE")  # "Front- Left -Bottom"
                row.operator("object.cubefront_edgebottom_minus_y", "", icon="LAYER_ACTIVE")  # "Front - Bottom"
                row.operator("object.cubefront_cornerbottom_plus_xy", "", icon="LAYER_ACTIVE")  # "Front- Right -Bottom")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.object, "show_bounds", text="Show Bounds", icon='STICKY_UVS_LOC')
            sub = row.row(1)
            sub.scale_x = 0.5
            sub.prop(context.object, "draw_bounds_type", text="")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.menu("wkst.snaptocursor", "Cursor to... ", icon="FORCE_FORCE")

            row = col_top.row(align=True)
            row.menu("wkst.snaptoselect", "Selection to... ", icon="RESTRICT_SELECT_OFF")


######################
### Edit Selection ###
######################

    ###space###
    if context.mode == 'EDIT_MESH':

        ###space###
        if lt.display_editselect:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_editselect", text="", icon='TRIA_DOWN')
            row.label("Select...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_editselect", text="", icon='TRIA_RIGHT')
            row.label("Select...")

            row.menu("VIEW3D_MT_edit_mesh_showhide", "", icon="VISIBLE_IPO_ON")
            row.menu("VIEW3D_MT_edit_multi", text="", icon="UV_SYNC_SELECT")
            row.operator("view3d.select_border", text="", icon="BORDER_RECT")
            row.operator("view3d.select_circle", text="", icon="BORDER_LASSO")

        ###space###
        if lt.display_editselect:
            ###space###
            #col = layout.column(align=True)
            #box = col.column(align=True).box().column()
            #col_top = box.column(align=True)

            #row = col_top.row(align=True)
            #row.alignment = "CENTER"

            #row = col_top.row(align=True)
            #layout.operator_context = 'INVOKE_REGION_WIN'
            #row.operator("mesh.select_mode", text="Vert", icon='VERTEXSEL').type = 'VERT'
            #row.operator("mesh.select_mode", text="Edge", icon='EDGESEL').type = 'EDGE'
            #row.operator("mesh.select_mode", text="Face", icon='FACESEL').type = 'FACE'

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)

            row.operator("view3d.select_border", text="Border", icon="BORDER_RECT")
            row.operator("view3d.select_circle", text="Circle", icon="BORDER_LASSO")

            row = col_top.row(align=True)
            row.menu("VIEW3D_MT_edit_mesh_showhide", "Hide/Show", icon="VISIBLE_IPO_ON")
            row.menu("VIEW3D_MT_edit_multi", text="Mesh Select", icon="UV_SYNC_SELECT")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            sub = row.row()
            sub.scale_x = 0.3
            sub.operator("mesh.select_more", text="+")
            sub.operator("mesh.select_all", text="All")
            sub.operator("mesh.select_less", text="-")

            row = col_top.row(align=True)
            row.operator("mesh.select_similar", text="Similar")
            row.operator("mesh.select_similar_region", text="Face Regions")

            row = col_top.row(align=True)
            row.operator("mesh.select_mirror", text="Mirror")
            row.operator("mesh.select_all", text="Inverse").action = 'INVERT'

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("mesh.loop_multi_select", text="Edge Loops").ring = False
            row.operator("mesh.loop_multi_select", text="Edge Rings").ring = True

            row = col_top.row(align=True)
            row.operator("mesh.grow_loop", "Grow")
            row.operator("mesh.shrink_loop", "Shrink")
            row.operator("mesh.extend_loop", "Extend")

            row = col_top.row(align=True)
            row.operator("mesh.region_to_loop", "Inner-Loops")
            row.operator("mesh.loop_to_region", "Boundary-Loop")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("mesh.faces_select_linked_flat", text="Linked Faces")
            row.operator("mesh.select_nth", "Checker")

            row = col_top.row(align=True)
            row.operator("mesh.select_loose", text="Loose")
            row.operator("mesh.select_linked", text="Linked")

            row = col_top.row(align=True)
            row.operator("mesh.select_axis", text="ActiveSide")
            row.operator("mesh.select_face_by_sides", text="NSide")

            row = col_top.row(align=True)
            row.operator("mesh.edges_select_sharp", text="Sharp")
            row.operator("mesh.shortest_path_select", text="Shortest")

            row = col_top.row(align=True)
            row.operator("mesh.select_ungrouped", text="Ungrouped Verts")
            row.operator("mesh.select_random", text="Random")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            # by CoDEmanX
            ob = context.active_object
            info_str = ""
            tris = quads = ngons = 0

            for p in ob.data.polygons:
                count = p.loop_total
                if count == 3:
                    tris += 1
                elif count == 4:
                    quads += 1
                else:
                    ngons += 1

            info_str = "  Ngons: %i  Quads: %i  Tris: %i" % (ngons, quads, tris)
            row.label(info_str, icon='INFO')

            row = col_top.row(align=True)
            row.operator("data.facetype_select", text="Ngons").face_type = "5"
            row.operator("data.facetype_select", text="Quads").face_type = "4"
            row.operator("data.facetype_select", text="Tris").face_type = "3"

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.mst_sort_mesh_elements", text="MST Sort Mesh Elements")

            row = col_top.row(align=True)
            row.operator("addongen.mesh_order_research_operator", text="VertCycl").type = "Vertices"
            row.operator("addongen.mesh_order_research_operator", text="EdgeCycl").type = "Edges"
            row.operator("addongen.mesh_order_research_operator", text="PolyCycl").type = "Polygons"

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            if context.scene.tool_settings.mesh_select_mode[2] is False:
                row.operator("mesh.select_non_manifold", text="Non Manifold")
            row.operator("mesh.select_interior_faces", text="Interior Faces")

            row = col_top.row(align=True)
            row.operator("meshlint.select", "Meshlint > go Object Data")


##################
### Edit Pivot ###
##################

    ###space###
    if context.mode == 'EDIT_MESH':
        mesh = context.active_object.data

        ###space###
        if lt.display_editpivot:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_editpivot", text="", icon='TRIA_DOWN')
            row.label("Pivot...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_editpivot", text="", icon='TRIA_RIGHT')
            row.label("Pivot...")

            row.menu("origin.setupmenu_edm", "", icon="LAYER_ACTIVE")
            row.menu("wkst.snaptocursor", "", icon="FORCE_FORCE")
            row.menu("wkst.snaptoselect", "", icon="RESTRICT_SELECT_OFF")

        ###space###
        if lt.display_editpivot:
            ###space###
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("origin.selected_edm", "Origin Edit", icon="EDITMODE_HLT")
            row.operator("origin.selected_obm", "Origin Object", icon="OBJECT_DATAMODE")

            row = col_top.row(align=True)
            if lt.display_bboxback:
                row.scale_y = 1.2
                row.prop(lt, "display_bboxback", text="Back +Y", icon='TRIA_DOWN')

            else:
                row.scale_y = 1
                row.prop(lt, "display_bboxback", text="Back +Y", icon='TRIA_RIGHT')

            ###space###
            if lt.display_bboxback:
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                # Top
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubeback_cornertop_minus_xy", "", icon="LAYER_ACTIVE")  # "Back- Left -Top")
                row.operator("object.cubeback_edgetop_minus_y", "", icon="LAYER_ACTIVE")  # "Back - Top")
                row.operator("object.cubeback_cornertop_plus_xy", "", icon="LAYER_ACTIVE")  # "Back- Right -Top ")

                # Middle
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55
                row.operator("object.cubefront_edgemiddle_minus_x", "", icon="LAYER_ACTIVE")  # "Back- Left")
                row.operator("object.cubefront_side_plus_y", "", icon="LAYER_ACTIVE")  # "Back")
                row.operator("object.cubefront_edgemiddle_plus_x", "", icon="LAYER_ACTIVE")  # "Back- Right")

                # Bottom
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55
                row.operator("object.cubeback_cornerbottom_minus_xy", "", icon="LAYER_ACTIVE")  # "Back- Left -Bottom")
                row.operator("object.cubefront_edgebottom_plus_y", "", icon="LAYER_ACTIVE")  # "Back - Bottom")
                row.operator("object.cubeback_cornerbottom_plus_xy", "", icon="LAYER_ACTIVE")  # "Back- Right -Bottom")

                ###space###
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = box.column(1)

            ###space###
            if lt.display_bboxmiddle:
                row.scale_y = 1.2
                row.prop(lt, "display_bboxmiddle", text="Middle", icon='TRIA_DOWN')

            else:
                row.scale_y = 1
                row.prop(lt, "display_bboxmiddle", text="Middle", icon='TRIA_RIGHT')

            ###space###
            if lt.display_bboxmiddle:
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                # Top
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_edgetop_minus_x", "", icon="LAYER_ACTIVE")  # "Middle - Left Top")
                row.operator("object.cubefront_side_plus_z", "", icon="LAYER_ACTIVE")  # "Top")
                row.operator("object.cubefront_edgetop_plus_x", "", icon="LAYER_ACTIVE")  # "Middle - Right Top")

                # Middle
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_side_minus_x", "", icon="LAYER_ACTIVE")  # "Left")
                obj = context.object
                if obj and obj.mode == 'EDIT':
                    row.operator("mesh.origincenter", text="", icon="LAYER_ACTIVE")
                else:
                    row.operator("object.origin_set", text="", icon="LAYER_ACTIVE").type = 'ORIGIN_GEOMETRY'

                row.operator("object.cubefront_side_plus_x", "", icon="LAYER_ACTIVE")  # "Right")

                # Bottom
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_edgebottom_minus_x", "", icon="LAYER_ACTIVE")  # "Middle - Left Bottom")
                row.operator("object.cubefront_side_minus_z", "", icon="LAYER_ACTIVE")  # "Bottom")
                row.operator("object.cubefront_edgebottom_plus_x", "", icon="LAYER_ACTIVE")  # "Middle - Right Bottom")

                ###space###
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)
                row = col_top.row(align=True)

            ###space###
            if lt.display_bboxfront:
                row.scale_y = 1.2
                row.prop(lt, "display_bboxfront", text="Front -Y", icon='TRIA_DOWN')

            else:
                row.scale_y = 1
                row.prop(lt, "display_bboxfront", text="Front -Y", icon='TRIA_RIGHT')

            ###space###
            if lt.display_bboxfront:
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                # Top
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_cornertop_minus_xy", "", icon="LAYER_ACTIVE")  # "Front- Left -Top"
                row.operator("object.cubeback_edgetop_plus_y", "", icon="LAYER_ACTIVE")  # "Front - Top"
                row.operator("object.cubefront_cornertop_plus_xy", "", icon="LAYER_ACTIVE")  # "Front- Right -Top"

                # Middle
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_edgemiddle_minus_y", "", icon="LAYER_ACTIVE")  # "Front- Left"
                row.operator("object.cubefront_side_minus_y", "", icon="LAYER_ACTIVE")  # "Front"
                row.operator("object.cubefront_edgemiddle_plus_y", "", icon="LAYER_ACTIVE")  # "Front- Right"

                # Bottom
                row = col_top.row(align=True)
                row.alignment = 'CENTER'
                row.scale_x = 1.55

                row.operator("object.cubefront_cornerbottom_minus_xy", "", icon="LAYER_ACTIVE")  # "Front- Left -Bottom"
                row.operator("object.cubefront_edgebottom_minus_y", "", icon="LAYER_ACTIVE")  # "Front - Bottom"
                row.operator("object.cubefront_cornerbottom_plus_xy", "", icon="LAYER_ACTIVE")  # "Front- Right -Bottom")

            ###space###
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)

            row = col_top.row(align=True)
            row.menu("wkst.snaptocursor", " > Cursor to... ", icon="FORCE_FORCE")

            row = col_top.row(align=True)
            row.menu("wkst.snaptoselect", " > Selection to... ", icon="RESTRICT_SELECT_OFF")


#################
### Transform ###
#################
    if context.mode not in 'SCULPT':
        ###space###
        if lt.display_transform:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_transform", text="", icon='TRIA_DOWN')
            row.label("Transform...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_transform", text="", icon='TRIA_RIGHT')
            row.label("Transform...")

            row.menu("wkst.transform_menu", "", icon="MANIPUL")
            row.menu("wkst.normal_transform_menu", "", icon="AXIS_SIDE")
            row.menu("VIEW3D_MT_mirror", "", icon="ARROW_LEFTRIGHT")

            #row.operator("mesh.snap_utilities_rotate", text = "", icon="NDOF_TURN")
            #row.operator("mesh.snap_utilities_move", text = "", icon="NDOF_TRANS")

        if lt.display_transform:

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("transform.translate", text="(G)", icon="MAN_TRANS")
            row.operator("transform.rotate", text="(R)", icon="MAN_ROT")
            row.operator("transform.resize", text="(S)", icon="MAN_SCALE")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(align=True)
            row.menu("translate.normal_menu", text="N-Translate")
            row.menu("rotate.normal_menu", text="N-Rotate")
            row.menu("resize.normal_menu", text="N-Scale")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.mirror1", text="MX", icon='ARROW_LEFTRIGHT')
            row.operator("object.mirror2", text="MY", icon='ARROW_LEFTRIGHT')
            row.operator("object.mirror3", text="MZ", icon='ARROW_LEFTRIGHT')

            ###space###
            if context.mode == 'OBJECT':

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.row(align=True)
                row.menu("VIEW3D_MT_object_clear", icon="PANEL_CLOSE")
                row.menu("VIEW3D_MT_object_apply", icon="FILE_TICK")

            ###space###
            if context.mode == 'EDIT_MESH':

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.row(align=True)
                row.operator("transform.shrink_fatten", text="Shrink/Fatten")
                row.operator("transform.tosphere", "to Sphere")

                row = col_top.row(align=True)
                row.operator("transform.shear", text="Shear")
                row.operator("transform.bend", text="Bend")

                row = col_top.row(align=True)
                row.operator("transform.vertex_random", text="Randomize")
                row.operator("transform.vertex_warp", text="Warp")

                row = col_top.row(align=True)
                row.operator('mesh.rot_con', 'Face-Rotation-Constraine')

                # ----------------------------------------------------------------------------------

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.row(align=True)
                row.operator("transform.translate", text="Move Texture Space").texture_space = True
                row.operator("transform.resize", text="Scale Texture Space").texture_space = True

            ###space###
            if context.mode == 'OBJECT':
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                if context.object:

                    row = col_top.row(align=True)
                    row.label(text="", icon="MAN_TRANS")
                    row.prop(context.object, 'location', text="")

                    row = col_top.row(align=True)
                    row.label(text="", icon="MAN_ROT")
                    row.prop(context.object, 'rotation_euler', text="")

                    row = col_top.row(align=True)
                    row.label(text="", icon="MAN_SCALE")
                    row.prop(context.object, 'scale', text="")

                    row = col_top.row(align=True)
                    row.label(text="", icon="MOD_MESHDEFORM")
                    row.prop(context.object, 'dimensions', text="")

                col_top = box.column(align=True)
                col_top = box.column(align=True)
                row = col_top.column(align=True)
                row.operator("freeze_transform.selected", text="Set all to 0", icon="NDOF_DOM")
                row.operator("object.duplicate", text="Duplicate Object", icon="ZOOMIN")


#######################
### Place Geometry  ###
#######################

    ###space###
    if context.mode == 'OBJECT':

        ###space###
        if lt.display_placegeom:
            ###space2###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_placegeom", text="", icon='TRIA_DOWN')
            row.label("Obj-Align...")
        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_placegeom", text="", icon='TRIA_RIGHT')
            row.label("Obj-Align...")

            row.menu("align.scale_menu", text="", icon='MAN_SCALE')
            row.menu("align.rotation_menu", text="", icon='MAN_ROT')
            row.menu("align.location_menu", text="", icon='MAN_TRANS')

        ###space###
        if lt.display_placegeom:

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.align_tools", icon="ROTATE")
            row = col_top.row(align=True)
            row.operator("object.align_by_faces", text="Active Face to Active Face", icon="SNAP_SURFACE")
            row = col_top.row(align=True)
            row.operator("object.drop_on_active", text="Drop down to Active", icon="NLA_PUSHDOWN")
            row = col_top.row(align=True)
            row.operator("object.distribute_osc", text="Distribute Objects", icon="ALIGN")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.align_location_all", text=" ", icon='MAN_TRANS')
            row.operator("object.align_location_x", text="X")
            row.operator("object.align_location_y", text="Y")
            row.operator("object.align_location_z", text="Z")

            sub = row.row(1)
            sub.scale_x = 2.0
            sub.operator("object.location_clear", text="", icon="X")

            props = row.operator("object.transform_apply", text="", icon="FILE_TICK")
            props.location = True
            props.rotation = False
            props.scale = False

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("object.align_rotation_all", text=" ", icon='MAN_ROT')
            row.operator("object.align_rotation_x", text="X")
            row.operator("object.align_rotation_y", text="Y")
            row.operator("object.align_rotation_z", text="Z")

            sub = row.row(1)
            sub.scale_x = 2.0
            sub.operator("object.rotation_clear", text="", icon="X")
            props = row.operator("object.transform_apply", text="", icon="FILE_TICK")
            props.location = False
            props.rotation = True
            props.scale = False

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("object.align_objects_scale_all", text=" ", icon='MAN_SCALE')
            row.operator("object.align_objects_scale_x", text="X")
            row.operator("object.align_objects_scale_y", text="Y")
            row.operator("object.align_objects_scale_z", text="Z")

            sub = row.row(1)
            sub.scale_x = 2.0
            sub.operator("object.scale_clear", text="", icon="X")

            props = row.operator("object.transform_apply", text="", icon="FILE_TICK")
            props.location = False
            props.rotation = False
            props.scale = True


###############
###  Align  ###
###############

    ###space###
    if context.mode == 'EDIT_MESH':
        mesh = context.active_object.data

        ###space###
        if lt.display_vertalign:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_vertalign", text="", icon='TRIA_DOWN')
            row.label("Align...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_vertalign", text="", icon='TRIA_RIGHT')
            row.label("Align...")
            sub = row.row(1)
            sub.scale_x = 0.35
            sub.operator("mesh.face_align_x", "X", icon='TRIA_RIGHT')
            sub.operator("mesh.face_align_y", "Y", icon='TRIA_UP')
            sub.operator("mesh.face_align_z", "Z", icon='SPACE3')

        ###space###
        if lt.display_vertalign:
            ###space###

            box = layout.box().row()
            row = box.column(1)
            row.label("Align")
            row.label("to")
            row.label("Axis")

            row = box.column(1)
            row.operator("mesh.face_align_xy", "Xy", icon='TRIA_RIGHT_BAR')
            row.operator("mesh.face_align_yz", "Zy", icon='TRIA_UP_BAR')
            row.operator("mesh.face_align_xz", "Zx", icon='TRIA_LEFT_BAR')

            row = box.column(1)
            row.operator("mesh.face_align_x", "X", icon='TRIA_RIGHT')
            row.operator("mesh.face_align_y", "Y", icon='TRIA_UP')
            row.operator("mesh.face_align_z", "Z", icon='SPACE3')

            box = layout.box().column(1)
            row = box.row(1)
            row.operator("mesh.face_make_planar", "Planar Faces")
            row.operator("mesh.align_normal", "Align 2 Normal")


########################
### Convert / Sculpt ###
########################

    ###space###
    obj = context.active_object
    if obj:
        obj_type = obj.type
        if obj_type in {'MESH', 'LATTICE'}:

            if lt.display_bool:
                ###space###
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_bool", text="", icon='TRIA_DOWN')
                obj = context.active_object
                if obj:
                    obj_type = obj.type

                    if obj_type in {'MESH'}:
                        row.label("Sculpt...")

                    if obj_type in {'LATTICE'}:
                        row.label("Lattice...")

            else:
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_bool", text="", icon='TRIA_RIGHT')

                obj = context.active_object
                if obj:
                    obj_type = obj.type

                    if obj_type in {'MESH'}:
                        row.label("Sculpt...")

                        if context.mode == 'OBJECT':
                            row.menu("object.decimatefreeze_menu", "", icon='FREEZE')
                            row.menu("draw.gpencil_menu", "", icon='SCULPTMODE_HLT')
                            #row.operator("sculpt.remesh", text='', icon='MOD_REMESH')
                            row.menu("object.boolean_menu", "", icon='FULLSCREEN_EXIT')

                        if context.mode == 'EDIT_MESH':
                            row.menu("draw.gpencil_menu", "", icon='SCULPTMODE_HLT')
                            #row.operator("sculpt.remesh", text='', icon='MOD_REMESH')
                            row.menu("object.boolean_menu", "", icon='FULLSCREEN_EXIT')

                    if obj_type in {'LATTICE'}:

                        row.prop(context.object.data, "use_outside")
                        row.prop_search(context.object.data, "vertex_group", context.object, "vertex_groups", text="")

                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.prop(context.object.data, "points_u", text="X")
                        row.prop(context.object.data, "points_v", text="Y")
                        row.prop(context.object.data, "points_w", text="Z")

                        row = col_top.row(align=True)
                        row.prop(context.object.data, "interpolation_type_u", text="")
                        row.prop(context.object.data, "interpolation_type_v", text="")
                        row.prop(context.object.data, "interpolation_type_w", text="")

                    if context.mode == 'SCULPT':
                        row.operator("sculpt.remesh", text='', icon='MOD_REMESH')
                        row.menu("sculpt.edit_menu", text='', icon='SCULPTMODE_HLT')

                else:
                    row.label("Please select an object as an active!")

            ###space###
            if lt.display_bool:
                ###space###
                obj = context.active_object
                if obj:
                    obj_type = obj.type
                    ###space###
                    if obj_type in {'MESH'}:

                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.operator("sculpt.remesh", text='Remesh', icon='MOD_REMESH')
                        row.prop(context.window_manager, 'remeshPreserveShape', text="Preserve Shape")

                        row = col_top.row(align=True)
                        row.prop(context.window_manager, 'remeshDepthInt', text="Depth")
                        row.prop(context.window_manager, 'remeshSubdivisions', text="Subdivisions")

                        if context.mode == 'OBJECT':

                            col = layout.column(align=True)
                            box = col.column(align=True).box().column()
                            col_top = box.column(align=True)

                            row = col_top.row(align=True)
                            row.operator("object.join", text="Join", icon="FULLSCREEN_EXIT")

                            union = row.operator("mesh.boolean", "Union", icon='ZOOMIN')
                            union.modOp = 'UNION'

                            row = col_top.row(align=True)
                            difference = row.operator("mesh.boolean", "Difference", icon='ZOOMOUT')
                            difference.modOp = 'DIFFERENCE'

                            intersect = row.operator("mesh.boolean", "Intersect", icon='PANEL_CLOSE')
                            intersect.modOp = 'INTERSECT'

                            col = layout.column(align=True)
                            box = col.column(align=True).box().column()
                            col_top = box.column(align=True)

                            row = col_top.row(align=True)
                            row.operator("boolean.separate", text="Separate")
                            row.operator("boolean.clone", text="Clone")

                            col = layout.column(align=True)
                            box = col.column(align=True).box().column()
                            col_top = box.column(align=True)

                            row = col_top.row(align=True)
                            row.operator("boolean.freeze", text="Freeze")
                            row.operator("boolean.unfreeze", text="Unfreeze")

                            row = col_top.row(align=True)
                            row.operator("boolean.grease_symm", text='Symmetrize')
                            row.prop(context.window_manager, "bolsymm", text="")

                        if context.mode == 'EDIT_MESH':
                            col = layout.column(align=True)
                            box = col.column(align=True).box().column()
                            col_top = box.column(align=True)

                            row = col_top.row(align=True)
                            row.operator("mesh.intersect", "Intersect", icon='ZOOMIN').use_separate = False
                            row.operator("mesh.intersect", "Intersect", icon='ZOOMOUT').use_separate = True

                            col = layout.column(align=True)
                            box = col.column(align=True).box().column()
                            col_top = box.column(align=True)

                            row = col_top.column(align=True)
                            row.operator("mesh.looptools_gstretch", "Gstretch Project", icon='SPHERECURVE')
                            row.operator("boolean.purge_pencils", text='Purge Grease', icon='PANEL_CLOSE')

                            row = col_top.row(align=True)
                            row.prop(context.tool_settings, "use_grease_pencil_sessions", text=" ", icon="LOCKED")
                            row.operator("gpencil.draw", text=" ", icon="DISCLOSURE_TRI_DOWN").mode = 'ERASER'
                            row.operator("gpencil.draw", text=" ", icon="NOCURVE").mode = 'DRAW_POLY'
                            row.operator("gpencil.draw", text=" ", icon="BRUSH_DATA").mode = 'DRAW'
                            row.operator("gpencil.draw", text=" ", icon="GREASEPENCIL").mode = 'DRAW_STRAIGHT'

                            row = col_top.row(align=True)
                            if context.space_data.type == 'VIEW_3D':
                                row.prop(context.tool_settings, "grease_pencil_source", expand=True)
                            elif context.space_data.type == 'CLIP_EDITOR':
                                row.prop(context.space_data, "grease_pencil_source", expand=True)

                        if context.mode == 'OBJECT':
                            col = layout.column(align=True)
                            box = col.column(align=True).box().column()
                            col_top = box.column(align=True)

                            row = col_top.column(align=True)
                            row.operator("grease.execution", text='Grease Cut', icon="SCULPTMODE_HLT")

                            row = col_top.row(align=True)
                            row.operator("wkst_grp.purge", text='Purge/Unlink', icon="PANEL_CLOSE")
                            row.operator("boolean.purge_pencils", text='Purge Grease', icon="PANEL_CLOSE")

                            row = col_top.row(align=True)
                            row.prop(context.tool_settings, "use_grease_pencil_sessions", text=" ", icon="LOCKED")
                            row.operator("gpencil.draw", text=" ", icon="DISCLOSURE_TRI_DOWN").mode = 'ERASER'
                            row.operator("gpencil.draw", text=" ", icon="NOCURVE").mode = 'DRAW_POLY'
                            row.operator("gpencil.draw", text=" ", icon="BRUSH_DATA").mode = 'DRAW'
                            row.operator("gpencil.draw", text=" ", icon="GREASEPENCIL").mode = 'DRAW_STRAIGHT'

                            if context.active_gpencil_layer:
                                col = layout.column(align=True)
                                box = col.column(align=True).box().column()
                                col_top = box.column(align=True)

                                row = col_top.row(align=True)
                                if context.space_data.type == 'VIEW_3D':
                                    row.prop(context.tool_settings, "grease_pencil_source", expand=True)

                                elif context.space_data.type == 'CLIP_EDITOR':
                                    row.prop(context.space_data, "grease_pencil_source", expand=True)

                                row = col_top.row(align=True)
                                row.prop_enum(context.gpencil_data, "draw_mode", 'VIEW')
                                row.prop_enum(context.gpencil_data, "draw_mode", 'CURSOR')

                                row = col_top.row(align=True)
                                row.prop_enum(context.gpencil_data, "draw_mode", 'SURFACE')
                                row.prop_enum(context.gpencil_data, "draw_mode", 'STROKE')

                                row = col_top.row(align=True)
                                row.active = context.gpencil_data.draw_mode in {'SURFACE', 'STROKE'}
                                row.prop(context.gpencil_data, "use_stroke_endpoints")

                                row = col_top.row(align=True)
                                row.prop(context.active_gpencil_layer, "show_points", text="View Points", icon="PARTICLE_POINT")
                                row.operator("gpencil.convert", text="Convert", icon="CURVE_BEZCURVE")

                                col = layout.column(align=True)
                                box = col.column(align=True).box().column()
                                col_top = box.column(align=True)

                                row = col_top.column(align=True)
                                row.alignment = 'CENTER'
                                row.label("Active Layer")
                                row = col_top.column(align=True)
                                row.prop(context.active_gpencil_layer, "info", text="")

                                row = col_top.row(align=True)
                                row.prop(context.gpencil_data.layers, "active_index")

                                row = col_top.row(align=True)
                                row.operator("gpencil.layer_add", icon='ZOOMIN', text="Add Layer")
                                row.operator("gpencil.layer_remove", icon='ZOOMOUT', text="Del. Layer")

                                row = col_top.row(align=True)
                                row.prop(context.active_gpencil_layer, "lock")
                                row.prop(context.active_gpencil_layer, "hide")

                                col = layout.column(align=True)
                                box = col.column(align=True).box().column()
                                col_top = box.column(align=True)

                                row = col_top.column(align=True)
                                row.alignment = 'CENTER'
                                row.label(text="Stroke")
                                row = col_top.row(align=True)
                                row.prop(context.active_gpencil_layer, "color", text="")
                                row.prop(context.active_gpencil_layer, "alpha", "Opac", slider=True)
                                row = col_top.column(align=True)
                                row.prop(context.active_gpencil_layer, "line_width", slider=True)

                                row = col_top.column(align=True)
                                row.alignment = 'CENTER'
                                row.label(text="Fill")
                                row = col_top.row(align=True)
                                row.prop(context.active_gpencil_layer, "fill_color", text="")
                                row.prop(context.active_gpencil_layer, "fill_alpha", "Opac", slider=True)

                                row = col_top.column(align=True)
                                row.prop(context.active_gpencil_layer, "use_onion_skinning")

                            else:
                                col = layout.column(align=True)
                                box = col.column(align=True).box().column()
                                col_top = box.column(align=True)

                                row = col_top.row(align=True)
                                if context.space_data.type == 'VIEW_3D':
                                    row.prop(context.tool_settings, "grease_pencil_source", expand=True)

                                elif context.space_data.type == 'CLIP_EDITOR':
                                    row.prop(context.space_data, "grease_pencil_source", expand=True)

                            col = layout.column(align=True)
                            box = col.column(align=True).box().column()
                            col_top = box.column(align=True)

                            row = col_top.row(align=True)
                            box.prop(context.user_preferences.edit, "grease_pencil_manhattan_distance", text="Manhattan Distance")
                            box.prop(context.user_preferences.edit, "grease_pencil_euclidean_distance", text="Euclidean Distance")
                            boxrow = box.row(align=True)
                            boxrow.prop(context.user_preferences.edit, "use_grease_pencil_smooth_stroke", text="Smooth")
                            boxrow.prop(context.user_preferences.edit, "use_grease_pencil_simplify_stroke", text="Simplify")

                        if context.mode == 'SCULPT':
                            col = layout.column(align=True)
                            box = col.column(align=True).box().column()
                            col_top = box.column(align=True)

                            row = col_top.row(align=True)
                            row.operator("sculpt.geometry_smooth", text="Smooth")
                            row.operator("sculpt.geometry_laplacian_smooth", text="Laplacian")

                            row = col_top.row(align=True)
                            row.operator("sculpt.geometry_decimate", text="Decimate")
                            row.operator("sculpt.geometry_displace", text="Displace")

                            row = col_top.row(align=True)
                            row.operator("sculpt.geometry_subdivide_faces", text="Subdiv")
                            row.operator("sculpt.geometry_subdivide_faces_smooth", text="SmoothDivide")

                            row = col_top.row(align=True)
                            row.operator("sculpt.geometry_beautify_faces", text="Beautify")

                    ###space###

                    if obj_type in {'LATTICE'}:
                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.prop(context.object.data, "use_outside")
                        row.prop_search(context.object.data, "vertex_group", context.object, "vertex_groups", text="")

                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.prop(context.object.data, "points_u", text="X")
                        row.prop(context.object.data, "points_v", text="Y")
                        row.prop(context.object.data, "points_w", text="Z")

                        row = col_top.row(align=True)
                        row.prop(context.object.data, "interpolation_type_u", text="")
                        row.prop(context.object.data, "interpolation_type_v", text="")
                        row.prop(context.object.data, "interpolation_type_w", text="")


###################
### Sculpt Mask ###
###################

    ###space###
    if context.mode == 'SCULPT':

        ###space###
        if lt.display_sculptmask:

            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculptmask", text="", icon='TRIA_DOWN')
            row.label("Mask...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sculptmask", text="", icon='TRIA_RIGHT')
            row.label("Mask...")
            row.operator("boolean.mask_extract", text="", icon='MOD_MASK')

        ###space###
        if lt.display_sculptmask:
            ###space###

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("boolean.mask_extract", text="Extract Mask", icon='MOD_MASK')

            if context.object.vertex_groups.active:
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.row(align=True)
                row.template_list("MESH_UL_vgroups", "", context.object, "vertex_groups", context.object.vertex_groups, "active_index", rows=2)

                row = col_top.row(align=True)
                row.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
                row.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
                row.operator("object.vertex_group_add", icon='ZOOMIN', text="")
                row.operator("object.vertex_group_remove", icon='ZOOMOUT', text="").all = False
                row.menu("MESH_MT_vertex_group_specials", icon='DOWNARROW_HLT', text="")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(1)
            row.operator("mesh.masktovgroup", text="Create Vertex Group", icon='GROUP_VERTEX')
            row = col_top.row(1)
            row.operator("mesh.masktovgroup_remove", text="Remove", icon='DISCLOSURE_TRI_DOWN')
            row.operator("mesh.masktovgroup_append", text="Append", icon='DISCLOSURE_TRI_RIGHT')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(1)
            row.operator("mesh.vgrouptomask", text="Create Mask", icon='MOD_MASK')
            row = col_top.row(1)
            row.operator("mesh.vgrouptomask_remove", text="Remove", icon='DISCLOSURE_TRI_DOWN')
            row.operator("mesh.vgrouptomask_append", text="Append", icon='DISCLOSURE_TRI_RIGHT')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(1)
            row.operator("mesh.mask_from_edges", text="Mask by Edges", icon='MOD_MASK')

            row = col_top.column(1)
            row.prop(bpy.context.window_manager, "mask_edge_angle", text="Edge Angle", icon='MOD_MASK', slider=True)
            row.prop(bpy.context.window_manager, "mask_edge_strength", text="Mask Strength", icon='MOD_MASK', slider=True)

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(1)
            row.operator("mesh.mask_from_cavity", text="Mask by Cavity", icon='MOD_MASK')

            row = col_top.column(1)
            row.prop(bpy.context.window_manager, "mask_cavity_angle", text="Cavity Angle", icon='MOD_MASK', slider=True)
            row.prop(bpy.context.window_manager, "mask_cavity_strength", text="Mask Strength", icon='MOD_MASK', slider=True)

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(1)
            row.operator("mesh.mask_smooth_all", text="Mask Smooth", icon='MOD_MASK')

            row = col_top.column(1)
            row.prop(bpy.context.window_manager, "mask_smooth_strength", text="Mask Smooth Strength", icon='MOD_MASK', slider=True)


##################
### Mira Tools ###
##################

    ###space###
    if context.mode == 'EDIT_MESH':

        ###space###
        if lt.display_miracurve:

            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_miracurve", text="", icon='TRIA_DOWN')
            row.label("MCurve...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_miracurve", text="", icon='TRIA_RIGHT')

            row.label("MCurve...")

            row.prop(context.scene.mi_settings, "surface_snap", text='', icon="SNAP_SURFACE")
            row.menu("wkst.miraextrude_menu", text="", icon="MESH_GRID")
            row.menu("wkst.miracurve_menu", text="", icon="STYLUS_PRESSURE")

        ###space###
        if lt.display_miracurve:
            ###space###
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(1)
            row.operator("mira.poly_loop", text="Poly Loop", icon="MESH_GRID")
            row.prop(context.scene.mi_settings, "surface_snap", text='', icon="SNAP_SURFACE")
            row = col_top.row(1)
            row.operator("mesh.retopomt", text="Retopo MT", icon="ORTHO")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(align=True)
            row.operator("mira.curve_stretch", text="CurveStretch", icon="STYLUS_PRESSURE")
            row.prop(context.scene.mi_cur_stretch_settings, "points_number", text='PointsNumber')

            row = col_top.column(align=True)
            row.prop(context.scene.mi_cur_stretch_settings, "spread_mode", text='Spread')

            # ----------------------------------------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(align=True)
            row.operator("mira.curve_guide", text="CurveGuide", icon="RNA")
            row.prop(context.scene.mi_curguide_settings, "points_number", text='LoopSpread')

            row = col_top.column(align=True)
            row.prop(context.scene.mi_curguide_settings, "deform_type", text='Deform')

            # ----------------------------------------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(1)
            row.operator("mira.curve_surfaces", text="CurveSurfaces", icon="SURFACE_NCURVE")
            row.prop(context.scene.mi_cur_surfs_settings, "spread_loops_type", text='Points')

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(align=True)
            row.operator("mira.draw_extrude", text="Draw Extrude", icon="FORCE_MAGNETIC")
            #row.prop(context.scene.mi_extrude_settings, "extrude_mode", text='Mode')

            row = col_top.column(1)
            row.prop(context.scene.mi_extrude_settings, "extrude_step_type", text='Step')

            if context.scene.mi_extrude_settings.extrude_step_type == 'Asolute':
                row.prop(context.scene.mi_extrude_settings, "absolute_extrude_step", text='')
            else:
                row.prop(context.scene.mi_extrude_settings, "relative_extrude_step", text='')

            row = col_top.column(1)
            if context.scene.mi_settings.surface_snap is False:
                row.prop(context.scene.mi_extrude_settings, "do_symmetry", text='Symmetry')

                if context.scene.mi_extrude_settings.do_symmetry:
                    row.prop(context.scene.mi_extrude_settings, "symmetry_axys", text='Axys')

            # ----------------------------------------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.label("Curve Snap Settings")

            row = col_top.column(align=True)
            row.prop(context.scene.mi_settings, "surface_snap", text='SurfaceSnapping')
            row.prop(context.scene.mi_settings, "convert_instances", text='ConvertInstances')
            row.prop(context.scene.mi_settings, "snap_objects", text='SnapObjects')

            # ----------------------------------------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.label("Curve Settings")

            row = col_top.column(align=True)
            row.prop(context.scene.mi_settings, "spread_mode", text='Spread')
            row.prop(context.scene.mi_settings, "curve_resolution", text='Resolution')

            row = col_top.row(align=True)
            row.prop(context.scene.mi_settings, "draw_handlers", text='Handlers')
            row.operator("mira.curve_test", text="Curve Test")


################
###  Subdiv  ###
################

    ###space###
    if context.mode == 'EDIT_MESH':

        ###space###
        if lt.display_subdiv:

            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_subdiv", text="", icon='TRIA_DOWN')
            row.label("Subdivide...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_subdiv", text="", icon='TRIA_RIGHT')
            row.label("Subdivide...")

            row.menu("wkst.subdivide_menu", text="", icon="MESH_ICOSPHERE")
            row.menu("wkst.cutting_menu", "", icon="LINE_DATA")

        ###space###
        if lt.display_subdiv:
            ###space###

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Subdivide")

            row = col_top.row(align=True)
            row.operator("mesh.subdivide", text="1").number_cuts = 1
            row.operator("mesh.subdivide", text="2").number_cuts = 2
            row.operator("mesh.subdivide", text="3").number_cuts = 3
            row.operator("mesh.subdivide", text="4").number_cuts = 4
            row.operator("mesh.subdivide", text="5").number_cuts = 5
            row.operator("mesh.subdivide", text="6").number_cuts = 6

            row = col_top.row(align=True)
            row.operator("mesh.tris_convert_to_quads", text="Quads", icon="MOD_LATTICE")
            row.operator("mesh.unsubdivide", text="(Un-)Subdivide")
            row.operator("screen.redo_last", text="", icon="SCRIPTWIN")
            row.operator("mesh.quads_convert_to_tris", text="Tris", icon="MOD_TRIANGULATE")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Cutting")

            row = col_top.row(align=True)
            row.operator("mesh.snap_utilities_line", "SnapLine", icon="LINE_DATA")
            row.operator("mesh.bisect", icon="SCULPTMODE_HLT")

            row = col_top.row(align=True)
            props = row.operator("mesh.knife_tool", text="Knife", icon="LINE_DATA")
            props.use_occlude_geometry = True
            props.only_selected = False

            row.operator("object_ot.fastloop", icon="GRIP")

            row = col_top.row(align=True)

            props = row.operator("mesh.knife_tool", text="Knife Select", icon="LINE_DATA")
            props.use_occlude_geometry = False
            props.only_selected = True

            row.operator("mesh.loopcut_slide", "Loop Cut", icon="COLLAPSEMENU")

            row = col_top.row(align=True)
            row.operator("mesh.knife_project", icon="LINE_DATA")
            row.operator("mesh.ext_cut_faces", text="Face Cut", icon="SNAP_EDGE")

            row = col_top.row(align=True)
            row.operator("object.createhole", text="Face Hole", icon="RADIOBUT_OFF")
            row.operator("mesh.build_corner", icon="OUTLINER_DATA_MESH")


####################
###  Extrusions  ###
####################

    ###space###
    if context.mode == 'EDIT_MESH':

        ###space###
        if lt.display_extrude:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_extrude", text="", icon='TRIA_DOWN')
            row.label("Extrude...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_extrude", text="", icon='TRIA_RIGHT')
            row.label("Extrude...")

            row.menu("wkst.extrude_offset_menu", text="", icon="SNAP_PEEL_OBJECT")
            row.menu("wkst.extrude_menu", text="", icon="SNAP_FACE")

        ###space###
        if lt.display_extrude:
            ###space###

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Fill")

            row = col_top.row(align=True)
            row.operator("mesh.edge_face_add", "Edge/Face")
            row.operator("mesh.fill", text="Fill")

            row = col_top.row(align=True)
            row.operator("mesh.beautify_fill", text="Beautify")
            row.operator("mesh.fill_grid", "Grid Fill")

            row = col_top.row(align=True)
            row.operator("mesh.fill_holes", text="Fill Holes")
            row.operator("mesh.close_faces", "Close Faces")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Inset")

            row = col_top.row(align=True)
            row.operator('faceinfillet.op0_id', text='Face Fillet')
            row.operator("fillet.op0_id", text="Edge Fillet")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Extrude")

            row = col_top.row(align=True)
            row.operator("view3d.edit_mesh_extrude_move_normal", text="Region")
            row.operator("mesh.push_pull_face", "Push/Pull")

            row = col_top.row(align=True)
            row.operator("view3d.edit_mesh_extrude_individual_move", text="Individual")
            row.operator_menu_enum('mesh.offset_edges', 'geometry_mode')

            row = col_top.row(align=True)
            row.operator("mesh.poke", text="Poke")
            row.operator('object.mextrude', text='Multi Extrude')

            row = col_top.row(align=True)
            row.operator("mesh.spin")
            row.operator("mesh.screw")

            row = col_top.row(align=True)
            row.operator("mesh.solidify", text="Solidify")
            row.operator("mesh.wireframe", text="Wire")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("mesh.extrude_along_curve", text="Along Curve")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("BBox Mirror Extrude")

            row = col_top.row(align=True)
            row.operator("bbox.circle_div", text="EvenDiv")
            row.operator("mesh.subdivide", text="< OddDiv").number_cuts = 1

            row = col_top.row(align=True)
            row.operator("bbox.mirror_extrude_x", "X")
            row.operator("bbox.mirror_extrude_y", "Y")
            row.operator("bbox.mirror_extrude_z", "Z")
            row.operator("bbox.mirror_extrude_n", "N")


##############
###  Edit  ###
##############

    ###space###
    if context.mode == 'EDIT_MESH':

        ###space###
        if lt.display_vertedit:

            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_vertedit", text="", icon='TRIA_DOWN')
            row.label("Edit...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_vertedit", text="", icon='TRIA_RIGHT')
            row.label("Edit...")

            row.menu("wkst.connect_menu", text="", icon="SOUND")
            row.menu("wkst.vertex_arrange_menu", text="", icon="PARTICLE_POINT")
            row.operator_menu_enum("mesh.merge", "type", "", icon="AUTOMERGE_ON")

        ###space###
        if lt.display_vertedit:
            ###space###

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.menu("VIEW3D_MT_edit_mesh_delete")
            row.operator("mesh.remove_doubles")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("mesh.duplicate_move", "Duplicate", icon="MOD_DISPLACE")

            row = col_top.row(align=True)
            row.operator("mesh.split", icon="MOD_BOOLEAN")
            row.operator("mesh.separate", text="Separate", icon="ORTHO")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Connect", icon="SOUND")

            row = col_top.row(align=True)
            row.operator("mesh.vert_connect", "Vert Connect", icon="OUTLINER_DATA_MESH")
            row.operator("mesh.vert_connect_path", "Vert Path", icon="STICKY_UVS_DISABLE")

            row = col_top.row(align=True)
            row.operator("mesh.bridge_edge_loops", "Bridge Edges", icon="SOUND")
            row.operator("mesh.edge_face_add", "Edge / Face", icon="EDITMODE_VEC_HLT")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Arrange")

            row = col_top.row(align=True)
            row.operator("mesh.vertex_align", text="Align", icon="ALIGN")
            row.operator("mesh.vertex_distribute", text="Distribute", icon="PARTICLE_POINT")

            row = col_top.row(align=True)
            row.operator("mesh.vertices_smooth_laplacian", "Laplacian", icon="ROOTCURVE")
            row.operator("mesh.vertices_smooth", "Smooth", icon="SPHERECURVE")

            row = col_top.row(align=True)
            row.operator("transform.edge_slide", text="Slide Edge", icon="DISCLOSURE_TRI_RIGHT_VEC")
            row.operator("transform.vert_slide", text="Slide Vertex", icon="DISCLOSURE_TRI_RIGHT_VEC")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Merge", icon="AUTOMERGE_ON")

            row = col_top.row(align=True)
            row.operator_menu_enum("mesh.merge", "type")
            row.operator("mesh.merge", "Merge Center").type = 'CENTER'

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            Automerge = context.tool_settings
            row.prop(Automerge, "use_mesh_automerge", text="Auto Merge")

            row = col_top.row(align=True)
            row.operator("double.threshold01", text="TSHD 0.1")
            row.operator("double.threshold0001", text="TSHD 0.001")

            tool_settings = context.tool_settings
            row = col_top.row(align=True)
            row.label("Double Threshold:")
            row = col_top.row(align=True)
            row.prop(tool_settings, "double_threshold", text="")


###################
### Curve Tools ###
###################

    ###space###
    if context.mode == 'OBJECT':
        obj = context.active_object
        if obj:
            obj_type = obj.type

            if obj_type in {'CURVE'}:

                    ######################
                    ### Curve Geometry ###
                    ######################

                    ###space###
                if lt.display_curvegeo:
                    box = layout.box()
                    row = box.row(1)
                    row.prop(lt, "display_curvegeo", text="", icon='TRIA_DOWN')
                    row.label("Curve...")

                else:
                    box = layout.box()
                    row = box.row(1)
                    row.prop(lt, "display_curvegeo", text="", icon='TRIA_RIGHT')
                    row.label("Curve...")

                    sub = row.row(1)
                    sub.scale_x = 0.4
                    sub.prop(context.object.data, "resolution_u", text="")
                    row.menu("wkst.curve_edit_menu", "", icon="CURVE_BEZCIRCLE")

                if lt.display_curvegeo:
                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.prop(context.object.data, "dimensions", expand=True)

                    row = col_top.row(align=True)
                    row.operator("curve.to_poly", "Poly")
                    row.operator("curve.to_bezier", "Bezièr")
                    row.operator("curve.to_nurbs", "Nurbs")

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.operator("curve.open_circle", text="Open/Close", icon="MOD_CURVE")
                    row.operator("curve.simplify", "Simplify", icon="IPO_EASE_IN_OUT")

                    row = col_top.row(align=True)
                    row.operator("object.duplicate_move_linked", text="Dupli-Linked", icon="LINKED")
                    row.operator("curve.smoothspline", "Smooth", icon="SMOOTHCURVE")

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.prop(context.object.data, "fill_mode", text="")
                    row.prop(context.object.data, "use_fill_deform")

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.operator("object.wire_all", text="", icon='WIRE')
                    row.prop(context.object.data, "bevel_depth", text="Bevel Depth")

                    row = col_top.row(align=True)
                    row.prop(context.object.data, "resolution_u", text="Rings")
                    row.prop(context.object.data, "bevel_resolution", text="Loops")

                    row = col_top.row(align=True)
                    row.prop(context.object.data, "offset")
                    row.prop(context.object.data, "extrude", "Height")

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.label(text="Bevel Length Factor:")

                    row.active = (context.object.data.bevel_depth > 0 or context.object.data.bevel_object is not None)

                    row = col_top.row(align=True)
                    row.prop(context.object.data, "bevel_factor_start", text="Start")
                    row.prop(context.object.data, "bevel_factor_end", text="End")

                    row = col_top.row(align=True)
                    row.prop(context.object.data, "bevel_factor_mapping_start", text="")
                    row.prop(context.object.data, "bevel_factor_mapping_end", text="")

                    row = col_top.row(align=True)
                    sub = row.row()
                    sub.active = context.object.data.taper_object is not None
                    sub.prop(context.object.data, "use_map_taper")

                    sub = row.row()
                    sub.active = context.object.data.bevel_object is not None
                    sub.prop(context.object.data, "use_fill_caps")

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    if context.mode == 'OBJECT':
                        row = col_top.row(align=True)
                        row.operator("curve.bevelcurve", "BevelCurve", icon="CURVE_BEZCIRCLE")

                    row = col_top.row(align=True)
                    row.label(text="Bevel Object:")
                    row.prop(context.object.data, "bevel_object", text="")

                    col_top = box.column(align=True)

                    if context.mode == 'OBJECT':
                        row = col_top.row(align=True)
                        row.operator("curve.tapercurve", "TaperCurve", icon="CURVE_BEZCURVE")

                    row = col_top.row(align=True)
                    row.label(text="Taper Object:")
                    row.prop(context.object.data, "taper_object", text="")

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.label(text="Path / Curve-Deform:")
                    row = col_top.row(align=True)
                    row.prop(context.object.data, "use_radius")
                    row.prop(context.object.data, "use_stretch")
                    row.prop(context.object.data, "use_deform_bounds")

                    row = col_top.row(align=True)
                    row.label(text="Twisting:")
                    row = col_top.row(align=True)
                    row.active = (context.object.data.dimensions == '2D' or (context.object.data.bevel_object is None and context.object.data.dimensions == '3D'))
                    row.prop(context.object.data, "twist_mode", text="")
                    row.prop(context.object.data, "twist_smooth", text="Smooth")

                #####################
                ### Curve Tools 2 ###
                #####################

                ###space###
                if lt.display_curveloft:
                    ###space###
                    box = layout.box()
                    row = box.row(1)
                    row.prop(lt, "display_curveloft", text="", icon='TRIA_DOWN')
                    row.label("CurveT2...")

                else:
                    ###space###
                    box = layout.box()
                    row = box.row(1)
                    row.prop(lt, "display_curveloft", text="", icon='TRIA_RIGHT')
                    row.label("CurveT2...")

                    row.menu("wkst.splinetype_menu", "", icon="IPO_BEZIER")
                    row.menu("wkst.ct2d_menu", text="", icon="DISCLOSURE_TRI_DOWN")
                    row.menu("wkst.ct2_menu", text="", icon="ANIM_DATA")

                ###space###
                if lt.display_curveloft:
                    ###space###

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.alignment = "CENTER"
                    row.label("", icon="INFO")

                    row = col_top.row(align=True)
                    row.operator("curvetools2.operatorselectioninfo", text="Selection Info:")
                    row.prop(context.scene.curvetools, "NrSelectedObjects", text="")

                    # --------------------------

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.operator("object.wire_all", text="", icon='WIRE')
                    row.prop(context.object.data, "resolution_u", text="Set Resolution")
                    #row.operator("curvetools2.operatorsplinessetresolution", text = "Set resolution")
                    #row.prop(context.scene.curvetools, "SplineResolution", text = "")

                    row = col_top.row(align=True)
                    row.operator("curve.open_circle", text="Open/Close", icon="MOD_CURVE")
                    #row.operator("curvetools2.operatororigintospline0start", text = "Origin 2 Start" ,icon = "PARTICLE_TIP")
                    row.operator("curve.switch_direction_obm", "Direction", icon="ARROW_LEFTRIGHT")

                    # --------------------------

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)
                    row = col_top.row(align=True)
                    row.scale_y = 1.5
                    row.operator("curvetools2.operatorsweepcurves", text="Sweep")
                    row.operator("curvetools2.operatorloftcurves", text="Loft")

                    row = col_top.row(align=True)
                    row.scale_y = 1.5
                    row.operator("curvetools2.operatorbirail", text="Birail")
                    row.operator("curvetools2.operatorsweepandmorph", text="Morph")

                    row = col_top.row(align=True)
                    row.scale_y = 1.5
                    row.operator("curvetools2.operatorrevolvecurves", text="Revolver")
                    row.prop(context.scene.curvetools, "AngularResolution", text="AngRes")

                    # --------------------------

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.operator("curvetools2.operatorintersectcurves", text="Intersect Curves")
                    row = col_top.row(align=True)
                    row.prop(context.scene.curvetools, "LimitDistance", text="LimitDistance")
                    #row.active = (context.scene.curvetools.IntersectCurvesAlgorithm == '3D')

                    col_top = box.column(align=True)
                    col_top = box.column(align=True)

                    row = col_top.row(align=0)
                    row.prop(context.scene.curvetools, "IntersectCurvesAlgorithm", text="Algorithm")

                    row = col_top.row(align=0.1)
                    row.prop(context.scene.curvetools, "IntersectCurvesMode", text="Mode")

                    row = col_top.row(align=0.1)
                    row.prop(context.scene.curvetools, "IntersectCurvesAffect", text="Affect")

                    # --------------------------

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.alignment = "CENTER"
                    row.label("Optimize Tools for BezièrCurve", icon="LAMP")

                    row = col_top.row(align=True)
                    row.operator("curvetools2.operatorsplinesjoinneighbouring", text="Join neighbouring splines")

                    row = col_top.row(align=True)
                    row.prop(context.scene.curvetools, "SplineJoinDistance", text="Threshold join")

                    col_top = box.column(align=True)
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.prop(context.scene.curvetools, "SplineJoinStartEnd", text="Only at start & end")

                    row = col_top.row(align=0.5)
                    row.prop(context.scene.curvetools, "SplineJoinMode", text="Join")

                    # --------------------------

                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.operator("curvetools2.operatorsplinesremovezerosegment", text="del 0-segments")
                    row.operator("curvetools2.operatorsplinesremoveshort", text="del short splines")

                    row = col_top.row(align=True)
                    row.prop(context.scene.curvetools, "SplineRemoveLength", text="Threshold remove")


#######################
### Edit Mira Tools ###
#######################

    ###space###
    if context.mode == 'EDIT_MESH':

        ###space###
        if lt.display_miraedit:

            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_miraedit", text="", icon='TRIA_DOWN')
            row.label("CadStyle...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_miraedit", text="", icon='TRIA_RIGHT')
            row.label("CAD...")

            row.operator("mesh.edge_roundifier", "", icon="OUTLINER_DATA_CURVE")
            row.menu("VIEW3D_MT_edit_mesh_tinycad", "", icon="GRID")
            row.menu("VIEW3D_MT_edit_mesh_looptools", "", icon="SORTALPHA")

        ###space###
        if lt.display_miraedit:
            ###space###

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("LoopTools")

            row = col_top.row(align=True)
            row.operator("mesh.looptools_circle")
            row.operator("mesh.looptools_relax")

            row = col_top.row(align=True)
            row.operator("mesh.looptools_bridge", text="Bridge").loft = False
            row.operator("mesh.looptools_flatten")

            row = col_top.row(align=True)
            row.operator("mesh.looptools_bridge", text="Loft").loft = True
            row.operator("mesh.looptools_space")

            row = col_top.row(align=True)
            row.operator("mesh.looptools_gstretch")
            row.operator("mesh.looptools_curve")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("TinyCAD Tools")

            row = col_top.row(align=True)
            row.operator("view3d.autovtx", text="Auto-VTX")
            row.operator("mesh.circlecenter", text="Circle Center")

            row = col_top.row(align=True)
            row.operator("mesh.vertintersect", text="V2X")
            row.operator("mesh.intersectall", text="X-All")

            row = col_top.row(align=True)
            row.operator("mesh.linetobisect", text="BIX")
            row.operator("mesh.cutonperp", text="PERP CUT")

            # --------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("mesh.edge_roundifier", icon="OUTLINER_DATA_CURVE")


###################
### Deform ###
###################

    ###space###
    if context.mode == 'OBJECT' or context.mode == 'EDIT_MESH':

        obj = context.active_object
        if obj:
            obj_type = obj.type

            if obj_type in {'MESH'}:
                ###space###

                if lt.display_deform:
                    ###space###
                    box = layout.box()
                    row = box.row(1)
                    row.prop(lt, "display_deform", text="", icon='TRIA_DOWN')
                    row.label("Deform...")

                else:
                    box = layout.box()
                    row = box.row(1)
                    row.prop(lt, "display_deform", text="", icon='TRIA_RIGHT')
                    row.label("Deform...")

                    if context.mode == 'OBJECT':
                        row.menu("wkst_menu.vertex_group", text="", icon="GROUP_VERTEX")
                        row.operator("boolean.mesh_deform", text="", icon="MOD_MESHDEFORM")
                        row.operator("retopo.latticeapply", text="", icon="MOD_LATTICE")

                    if context.mode == 'EDIT_MESH':
                        row.menu("wkst_menu.vertex_group", text="", icon="GROUP_VERTEX")
                        row.menu("wkst.miradeform_menu", text="", icon="OUTLINER_OB_MESH")
                        row.operator("object.easy_lattice", text="", icon="MOD_LATTICE")

                ###space###
                if lt.display_deform:

                    if context.mode == 'OBJECT':
                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.operator("retopo.latticeapply", text="Apply Easy Lattice", icon="MOD_LATTICE")

                        row = col_top.row(align=True)
                        row.operator("boolean.mesh_deform", text="Mesh Deform", icon="MOD_MESHDEFORM")

                    if context.mode == 'EDIT_MESH':

                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.operator("object.easy_lattice", text="Create Easy Lattice", icon="OUTLINER_DATA_LATTICE")

                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.operator("mira.linear_deformer", text="LinearDeformer", icon="OUTLINER_OB_MESH")

                        row = col_top.row(align=True)
                        row.prop(context.scene.mi_ldeformer_settings, "manual_update", text='ManualUpdate')

                        row = col_top.row(align=True)
                        row.operator("mira.noise", text="NoiseDeform")
                        row.operator("mira.deformer", text="Deformer")

                    ###space###
                    if(bpy.types.Scene.isEdgerRunning):

                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.operator("uv.toggle_edger", text="Stop Edger", icon="X_VEC")

                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)

                        ic = "UNLOCKED"
                        if bpy.types.Scene.isEdgerActive:
                            ic = "LOCKED"
                        row.operator("uv.toggle_edger_locking", text="Lock", icon=ic)

                        ic = "RESTRICT_SELECT_OFF"
                        if bpy.types.Scene.deselectGroups:
                            ic = "RESTRICT_SELECT_ON"
                        row.operator("uv.toggle_edger_deselecting", text="Deselect", icon=ic)

                        row = col_top.row(align=True)
                        row.prop(context.scene, 'isEdgerDebugActive')
                        row.prop(context.scene, 'isSelectFlush')

                        row = col_top.row(align=True)
                        row.operator("wm.lock_edge_loop_idname", text="Add", icon="ZOOMIN")
                        row.operator("wm.unlock_edge_loop_idname", text="Remove", icon="ZOOMOUT")

                        row = col_top.row(align=True)
                        row.operator("wm.clear_edger_oops_idname", text="Clear Loops", icon="MOD_SOLIDIFY")

                    ###space###
                    else:

                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.operator("uv.toggle_edger", text="Run Edger", icon="POSE_HLT")

                    if context.mode == 'OBJECT' or context.mode == 'EDIT_MESH':

                        col = layout.column(align=True)
                        box = col.column(align=True).box().column()
                        col_top = box.column(align=True)

                        row = col_top.row(align=True)
                        row.alignment = 'CENTER'
                        row.label("Vertex Group", icon="GROUP_VERTEX")

                        row = col_top.row(align=True)
                        row.operator("object.vertex_group_add", text="Add", icon='ZOOMIN')
                        row.operator("object.vertex_group_remove", text="Remove", icon='ZOOMOUT').all = False

                        if context.object.vertex_groups.active:
                            row = col_top.row(align=True)
                            row.template_list("MESH_UL_vgroups", "", context.object, "vertex_groups", context.object.vertex_groups, "active_index", rows=1)
                            row = col_top.row(align=True)
                            row.prop(context.object.vertex_groups, "active_index")

                            if context.mode == 'EDIT_MESH':
                                row = col_top.row(align=True)
                                row.operator("object.vertex_group_assign", text="Assign to...", icon="DISCLOSURE_TRI_RIGHT")
                                row.operator("object.vertex_group_remove_from", text="Remove from...", icon="DISCLOSURE_TRI_DOWN")

                                row = col_top.row(align=True)
                                row.operator("object.vertex_group_select", text="Select Grp", icon="RESTRICT_SELECT_OFF")
                                row.operator("object.vertex_group_deselect", text="Deselect Grp", icon="RESTRICT_SELECT_ON")

                            col_top = box.column(align=True)
                            col_top = box.column(align=True)
                            col_top = box.column(align=True)
                            row = col_top.row(align=True)
                            row.menu("MESH_MT_vertex_group_specials", icon='TRIA_RIGHT', text="Specials")

                            if context.mode == 'EDIT_MESH':
                                row.prop(context.tool_settings, "vertex_group_weight", text="Weight")


#################
### Modifier  ###
#################

    ###space###
    if lt.display_modif:
        ###space###
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_modif", text="", icon='TRIA_DOWN')
        row.label("Modifier...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_modif", text="", icon='TRIA_RIGHT')

        row.label("Modifier...")

        row.menu("wkst.modispace", "", icon='MODIFIER')

        ###space###
        if context.mode == 'OBJECT':

            row.menu("modifiers.viewport_obm", "", icon='RESTRICT_VIEW_OFF')

            row.operator("view3d.display_modifiers_delete", "", icon='X')
            row.operator("view3d.display_modifiers_apply", "", icon='FILE_TICK')

        if context.mode == 'SCULPT':
            row.menu("modifiers.viewport_edm", "", icon='RESTRICT_VIEW_OFF')

            row.operator("view3d.display_modifiers_delete", "", icon='X')
            row.operator("view3d.display_modifiers_apply", "", icon='FILE_TICK')

        if context.mode == 'EDIT_MESH':
            row.menu("modifiers.viewport_edm", "", icon='RESTRICT_VIEW_OFF')

            row.operator("view3d.display_modifiers_delete", "", icon='X')
            row.operator("view3d.display_modifiers_apply_edm", "", icon='FILE_TICK')

    ###space###
    if lt.display_modif:
        ###space###

        col = layout.column(align=True)
        box = col.column(align=True).box().column()
        col_top = box.column(align=True)

        row = col_top.row(align=True)
        row.operator_menu_enum("object.modifier_add", "type", icon='MODIFIER')

        col = layout.column(align=True)
        box = col.column(align=True).box().column()
        col_top = box.column(align=True)

        row = col_top.row(align=True)
        row.operator("view3d.display_modifiers_delete", "Delete", icon='X')

        if context.mode == 'OBJECT':
            row.operator("view3d.display_modifiers_apply", "Apply", icon='FILE_TICK')

        if context.mode == 'SCULPT':
            row.operator("view3d.display_modifiers_apply", "Apply", icon='FILE_TICK')

        if context.mode == 'EDIT_MESH':
            row.operator("view3d.display_modifiers_apply_edm", "Apply", icon='FILE_TICK')

        col = layout.column(align=True)
        box = col.column(align=True).box().column()
        col_top = box.column(align=True)

        row = col_top.row(align=True)
        row.operator("view3d.display_modifiers_viewport_off", "Off", icon='VISIBLE_IPO_OFF')
        row.operator("view3d.display_modifiers_viewport_on", "On ", icon='RESTRICT_VIEW_OFF')

        if context.mode == 'EDIT_MESH':
            row = col_top.row(align=True)
            row.operator("view3d.display_modifiers_edit_off", icon='SNAP_VERTEX')
            row.operator("view3d.display_modifiers_edit_on", icon='EDITMODE_HLT')

            row = col_top.row(align=True)
            row.operator("view3d.display_modifiers_cage_off", icon='OUTLINER_DATA_MESH')
            row.operator("view3d.display_modifiers_cage_on", icon='OUTLINER_OB_MESH')

        col = layout.column(align=True)
        box = col.column(align=True).box().column()
        col_top = box.column(align=True)

        row = col_top.row(align=True)
        row.alignment = 'CENTER'
        row.label("SubSurf Levels")

        row = col_top.row(align=True)
        row.operator("view3d.modifiers_subsurf_level_0")
        row.operator("view3d.modifiers_subsurf_level_1")
        row.operator("view3d.modifiers_subsurf_level_2")
        row.operator("view3d.modifiers_subsurf_level_3")
        row.operator("view3d.modifiers_subsurf_level_4")
        row.operator("view3d.modifiers_subsurf_level_5")
        row.operator("view3d.modifiers_subsurf_level_6")

        if context.mode not in 'SCULPT':
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Mirror Modifier")

            row = col_top.row(align=True)
            row.operator("view3d.fullmirror", text="X-Clip")
            row.operator("view3d.fullmirrory", text="Y-Clip")
            row.operator("view3d.fullmirrorz", text="Z-Clip")

        ###space###
        if context.mode == 'OBJECT':

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Move over the Modifier Stack")

            row = col_top.row(align=True)
            row.operator("view3d.display_modifiers_expand", icon='DISCLOSURE_TRI_DOWN_VEC')
            row.operator("view3d.display_modifiers_collapse", icon='DISCLOSURE_TRI_RIGHT_VEC')


###################
### Auto Mirror ###
###################

    ###space###
    obj = context.active_object
    if obj:
        obj_type = obj.type

        if obj_type in {'MESH'}:

            ###space###
            if lt.display_mirrcut:
                ###space###
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_mirrcut", text="", icon='TRIA_DOWN')
                row.label("MirrorCut...")

            else:
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_mirrcut", text="", icon='TRIA_RIGHT')

                row.label("MirrorCut...")

                # if context.mode == 'OBJECT' or context.mode == 'EDIT_MESH':
                #row.menu("wkst.axis_cut_menu", text="", icon="MOD_DECIM")

                sub = row.row(1)
                sub.scale_x = 0.3
                sub.prop(context.scene, "AutoMirror_orientation", text="")
                sub.prop(context.scene, "AutoMirror_axis", text="")
                row.menu("wkst.mirrorcut", text="", icon="MOD_WIREFRAME")

            ###space###
            if lt.display_mirrcut:
                col = layout.column(align=True)
                ###space###
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.row(align=True)
                row.operator("object.automirror", text="Execute AutoMirror", icon="MOD_WIREFRAME")

                row = col_top.row(align=True)
                row.prop(context.scene, "AutoMirror_orientation", text="")
                row.prop(context.scene, "AutoMirror_axis", text="")

                row = col_top.row(align=True)
                row.prop(context.scene, "AutoMirror_threshold", text="Threshold")

                col_top = box.column(align=True)
                row = col_top.row(align=True)
                row.prop(context.scene, "AutoMirror_toggle_edit", text="Stay in Editmode")
                row = col_top.row(align=True)
                row.prop(context.scene, "AutoMirror_cut", text="Cut+Mirror")
                if bpy.context.scene.AutoMirror_cut:
                    row.prop(context.scene, "AutoMirror_use_clip", text="Use Clip")
                    row = col_top.row(align=True)
                    row.prop(context.scene, "AutoMirror_show_on_cage", text="Editable")
                    row.prop(context.scene, "AutoMirror_apply_mirror", text="Apply")

                else:
                    row.label(icon="ERROR", text="No mesh selected")

                ###space###
                if context.mode == 'OBJECT':
                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.label("Mesh Cut")

                    row = col_top.row(align=True)
                    row.operator("modifier.positiv_x_cut_obm", text="+X")
                    row.operator("modifier.positiv_y_cut_obm", text="+Y")
                    row.operator("modifier.positiv_z_cut_obm", text="+Z")

                    row = col_top.row(align=True)
                    row.operator("modifier.negativ_x_cut_obm", text="-X")
                    row.operator("modifier.negativ_y_cut_obm", text="-Y")
                    row.operator("modifier.negativ_z_cut_obm", text="-Z")

                ###space###
                if context.mode == 'EDIT_MESH':
                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)

                    row = col_top.row(align=True)
                    row.alignment = 'CENTER'
                    row.label("Mesh Cut")

                    row = col_top.row(align=True)
                    row.operator("modifier.positiv_x_cut", text="+X")
                    row.operator("modifier.positiv_y_cut", text="+Y")
                    row.operator("modifier.positiv_z_cut", text="+Z")

                    row = col_top.row(align=True)
                    row.operator("modifier.negativ_x_cut", text="-X")
                    row.operator("modifier.negativ_y_cut", text="-Y")
                    row.operator("modifier.negativ_z_cut", text="-Z")


####################
### SnapShot ###
####################

    ###space###
    obj = context.active_object
    if obj:
        obj_type = obj.type

        if obj_type in {'MESH'}:
            ###space###
            if lt.display_snapshot:
                ###space###
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_snapshot", text="", icon='TRIA_DOWN')
                row.label("SnapShot...")

            else:
                ###space###
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_snapshot", text="", icon='TRIA_RIGHT')
                row.label("SnapShot...")

                row.operator("vtools.usesnapshot", icon='RECOVER_LAST', text="")
                row.operator("vtools.deletesnapshot", icon='DISCLOSURE_TRI_DOWN', text="")
                row.operator("vtools.capturesnapshot", icon='DISCLOSURE_TRI_RIGHT', text="")

            ###space###
            if lt.display_snapshot:
                ###space###
                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.row(align=True)
                row.operator("vtools.capturesnapshot", icon='DISCLOSURE_TRI_RIGHT', text="Add")
                row.operator("vtools.deletesnapshot", icon='DISCLOSURE_TRI_DOWN', text="Remove")

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.row(align=True)
                row.template_list('UI_UL_list', "snapShotMesh_ID", obj, "snapShotMeshes", obj, "snapShotMesh_ID_index", rows=2)

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.row(align=True)
                row.operator("vtools.recalculatesnapshotfromchildren", icon='BORDERMOVE', text="Recalculate")
                row.operator("vtools.usesnapshot", icon='RECOVER_LAST', text="Set Geometry")

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.row(align=True)
                row.operator("vtools.deleteallsnapshot", icon='X', text="Del. All")
                row.operator("vtools.deleteunusedsnapshotlist", icon='CANCEL', text="Del. Unused")

                row = col_top.row(align=True)
                row.prop(context.scene, "mod_list", text="")
                row.operator("ba.delete_data_obs", "DelOrphan", icon="PANEL_CLOSE")


#############
### Array ###
#############

    ###space###
    if context.mode == 'OBJECT':

        ###space###
        if lt.display_arrayobj:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_arrayobj", text="", icon='TRIA_DOWN')
            row.label("Copy...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_arrayobj", text="", icon='TRIA_RIGHT')

            row.label("Copy...")

            row.menu("wkst.copy_links_data", "", icon="CONSTRAINT")
            row.menu("wkst.copy_link", text="", icon="LINKED")
            row.menu("wkst.copy_dupli", text="", icon="MOD_ARRAY")

        ###space###
        if lt.display_arrayobj:

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(align=True)
            if context.mode == 'OBJECT':
                row.operator("mft.radialclone", text="Radial Clone", icon="FILE_REFRESH")
                row.operator("object.simplearewo", text="Replicator", icon="TRIA_RIGHT")
            row.operator("object.cursor_array", text="Copy 2 Cursor", icon="NEXT_KEYFRAME")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(align=True)
            row.operator("object.make_links_data", "Set Instance", icon="LINKED").type = 'OBDATA'
            if context.mode == 'OBJECT':
                row.operator("object.makesingle", "Clear Instance", icon="UNLINKED")

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.column(align=True)
                row.operator("object.select_linked", text="Select Linked", icon="RESTRICT_SELECT_OFF")
                row.operator_menu_enum("object.make_links_data", "type", " Make Links Data", icon="CONSTRAINT")

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)

                row = col_top.column(align=True)
                row.operator("object.copy_selected_modifiers", text="Copy Modifier", icon="PASTEFLIPDOWN")
                row.operator("switch.mod_display", "Copy Modifier Display", icon="PASTEFLIPDOWN")


####################
### Edit Normals ###
####################

    ###space###
    if context.mode == 'EDIT_MESH':

        ###space###
        if lt.display_normal:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_normal", text="", icon='TRIA_DOWN')
            row.label("Normals...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_normal", text="", icon='TRIA_RIGHT')
            row.label("Normals...")

            row.menu("wkst.normal_menu", text="", icon='AUTO')
            row.menu("wkst.normals_menu", text="", icon='SNAP_NORMAL')

        ###space###
        if lt.display_normal:
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("mesh.normals_make_consistent", text="Recalculate", icon='SNAP_NORMAL')
            row.operator("mesh.flip_normals", text="Flip", icon="FILE_REFRESH")

            row = col_top.row(align=True)
            row.operator("mesh.normals_make_consistent", text="Rec-Inside").inside = True
            row.operator("mesh.normals_make_consistent", text="Rec-Outside").inside = False

            row = col_top.row(align=True)
            row.prop(mesh, "show_normal_vertex", text="", icon='VERTEXSEL')
            row.prop(mesh, "show_normal_loop", text="", icon='LOOPSEL')
            row.prop(mesh, "show_normal_face", text="", icon='FACESEL')

            row.active = mesh.show_normal_vertex or mesh.show_normal_face
            row.prop(context.scene.tool_settings, "normal_size", text="Size")

            row = col_top.row(align=True)
            row.prop(mesh, "show_double_sided", icon="GHOST")

            row = col_top.row(align=True)
            row.prop(context.active_object.data, "use_auto_smooth", icon="AUTO")

            row = col_top.row(align=True)
            row.active = context.active_object.data.use_auto_smooth
            row.prop(context.active_object.data, "auto_smooth_angle", text="Angle")


#####################
### Mesh Check ###
#####################

    ###space###
    if lt.display_check:
        ###space###
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_check", text="", icon='TRIA_DOWN')
        row.label("Check...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_check", text="", icon='TRIA_RIGHT')

        row.label("Check...")

        if context.mode == 'OBJECT':
            row.operator("view3d.rec_normals", "", icon="SNAP_NORMAL")

        row.menu("wkst.modifly", '', icon="MOD_SOFT")

        if not context.mode == 'SCULPT':
            row.menu("wkst.material_menu", text="", icon='MATERIAL_DATA')
            row.menu("wkst.meshcheck_menu", text="", icon='GROUP_VCOL')

    ###space###
    if lt.display_check:
        ###space###
        if context.mode == 'OBJECT':
            view = context.space_data
            obj = context.object
            ###space###

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row()
            row.alignment = 'CENTER'
            row.label("Mesh Check", icon='LAMP')

            row = col_top.row(align=True)
            row.operator("view3d.rec_normals", "Recalculate Normals", icon="SNAP_NORMAL")

            row = col_top.column(align=True)
            row.operator("object.add_materials", text="Display color", icon='GROUP_VCOL')
            row.operator("object.remove_materials", text="Hidde color", icon='GROUP_VERTEX')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row()
            row.alignment = 'CENTER'
            row.label("Object Color", icon='LAMP')

            row = col_top.row(align=True)
            row.operator("object.material_slot_remove", text="Material", icon="ZOOMOUT")
            row.operator("object.material_add", text="Material", icon='ZOOMIN')
            row = col_top.row(align=True)
            row.prop(context.object, "color", text="")
            row = col_top.row(align=True)
            #row.prop(context.material, "use_object_color", text="Obj-Color", icon="COLOR")
            row.operator("material.remove", text="Remove all Material", icon="ZOOMOUT")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row()
            row.alignment = 'CENTER'
            row.label("Flymode for HighRes", icon='MOD_SOFT')

            row = col_top.row(align=True)
            row = col_top.row(align=True)
            row.operator("view3d.fast_navigate_operator", 'Start', icon="PLAY")
            row.operator("view3d.fast_navigate_stop_new", 'Stop', icon="PAUSE")

            row = col_top.row(align=True)
            row.prop(context.scene, "OriginalMode", "")
            row.prop(context.scene, "FastMode", "")

            row = col_top.row(align=True)
            row.prop(context.scene, "EditActive", "Edit mode")

            row = col_top.row(align=True)
            row.prop(context.scene, "Delay")
            row.prop(scene, "DelayTimeGlobal")

            row = col_top.row(align=True)
            row.prop(context.scene, "ShowParticles")
            row.prop(context.scene, "ParticlesPercentageDisplay")

        ###space###
        if context.mode == 'EDIT_MESH':
            view = context.space_data
            obj = context.object

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(1)
            row.operator("object.add_materials", text="Display color", icon='GROUP_VCOL')
            row.operator("object.remove_materials", text="Hidde color", icon='X')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.window_manager.border_lines, "borderlines_use")
            row.prop(context.window_manager.border_lines, "borderlines_width")

            row = col_top.row(align=True)
            row.prop(context.window_manager.border_lines, "custom_color_use", text="Border Color")
            row.prop(context.window_manager.border_lines, "custom_color", text="")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.column(1)
            row.prop(context.window_manager.preselect, "preselect_use")
            row.prop(context.window_manager.preselect, "depth_test")

            row = col_top.column(1)
            row.prop(context.window_manager.preselect, "preselect_radius")
            row.prop(context.window_manager.preselect, "preselect_width")
            row.prop(context.window_manager.preselect, "opacity_vertices")
            row.prop(context.window_manager.preselect, "opacity_edges")
            row.prop(context.window_manager.preselect, "opacity_face")
            row.prop(context.window_manager.preselect, "custom_color", text="")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.alignment = 'CENTER'
            row.label("Flymode for HighRes", icon='MOD_SOFT')

            row = col_top.row(align=True)
            row.operator("view3d.fast_navigate_operator", 'Start', icon="PLAY")
            row.operator("view3d.fast_navigate_stop_new", 'Stop', icon="PAUSE")


#####################
### Visualization ###
#####################

    ###space###
    if lt.display_shade:
        ###space###
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_shade", text="", icon='TRIA_DOWN')
        row.label("Visual...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_shade", text="", icon='TRIA_RIGHT')

        row.label("Visual...")

        row.menu("wkst.display_menu", text="", icon="UI")

        if context.mode == 'OBJECT' or context.mode == 'SCULPT':
            row.menu("wkst.meshdisplay_menu", text="", icon="META_CUBE")
            if context.mode == 'OBJECT':
                row.menu("wkst.shade_menu", text="", icon="SMOOTH")
            row.menu("wkst.wire_menu", text="", icon='WIRE')

        else:
            row.menu("wkst.meshdisplay_menu", text="", icon="META_CUBE")
            if context.mode == 'EDIT_MESH':
                row.menu("wkst.shade_menu", text="", icon="SMOOTH")
            row.operator("object.wire_all", text="", icon='WIRE')

    ###space###
    if lt.display_shade:
        ###space###

        if context.mode == 'OBJECT':

            ###space###
            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.shade_smooth", text="Smooth", icon="SMOOTH")
            row.operator("object.shade_flat", text="Flat", icon="MESH_CIRCLE")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.wire_all", text="Wire all", icon='WIRE')

            row = col_top.row(align=True)
            row.operator("view3d.display_wire_off", "Wire off", icon='MESH_PLANE')
            row.operator("view3d.display_wire_on", "Wire on", icon='MESH_GRID')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.object, "show_x_ray", text="X-Ray", icon="META_CUBE")
            row.prop(context.space_data, "show_backface_culling", text="Backface", icon="OUTLINER_OB_LATTICE")

            row = col_top.row(align=True)
            op = row.operator("super_grouper.change_selected_objects", text="Material Shade", icon='GHOST_DISABLED')
            op.sg_objects_changer = 'MATERIAL_SHADE'

            op = row.operator("super_grouper.change_selected_objects", text="Wire Shade", icon='GHOST_ENABLED')
            op.sg_objects_changer = 'WIRE_SHADE'

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="GROUP")
            row.prop(context.space_data, "use_matcap", icon="MATCAP_01")

            if context.space_data.use_matcap:
                row = col_top.row(align=True)
                row.scale_y = 0.2
                row.scale_x = 0.5
                row.template_icon_view(context.space_data, "matcap_icon")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.space_data, "show_only_render", text="Render", icon="RESTRICT_RENDER_ON")
            row.prop(context.space_data, "show_floor", text="Grid", icon="GRID")

            row = col_top.row(align=True)
            row.prop(context.space_data, "show_world", "World", icon="WORLD")

            sub = row.row(1)
            sub.scale_x = 0.335
            sub.prop(context.space_data, "show_axis_x", text="X", toggle=True)
            sub.prop(context.space_data, "show_axis_y", text="Y", toggle=True)
            sub.prop(context.space_data, "show_axis_z", text="Z", toggle=True)

        ###space###
        if context.mode == 'EDIT_MESH':

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("mesh.faces_shade_smooth", text="Smooth", icon="SMOOTH")
            row.operator("mesh.faces_shade_flat", text="Flat", icon="MESH_CIRCLE")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("object.wire_all", text="Wire all", icon='WIRE')
            row.operator("object.editnormals_transfer", icon='SNAP_NORMAL')

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.space_data, "use_occlude_geometry", text="Limit 2 Visible", icon='ORTHO')
            row.prop(context.object, "show_x_ray", text="X-Ray", icon="META_CUBE")

            row = col_top.row(align=True)
            row.prop(context.space_data, "show_backface_culling", text="Backface", icon="OUTLINER_OB_LATTICE")
            row.prop(context.space_data, "show_occlude_wire", text="Hidden", icon="OUTLINER_DATA_LATTICE")

            row = col_top.row(align=True)
            row.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="GROUP")
            row.prop(context.space_data, "use_matcap", icon="MATCAP_22")
            if context.space_data.use_matcap:
                row = col_top.row(align=True)
                row.scale_y = 0.2
                row.scale_x = 0.5
                row.template_icon_view(context.space_data, "matcap_icon")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.space_data, "show_only_render", text="Render", icon="RESTRICT_RENDER_ON")
            row.prop(context.space_data, "show_floor", text="Grid", icon="GRID")

            row = col_top.row(align=True)
            row.prop(context.space_data, "show_world", "World", icon="WORLD")

            sub = row.row(1)
            sub.scale_x = 0.335
            sub.prop(context.space_data, "show_axis_x", text="X", toggle=True)
            sub.prop(context.space_data, "show_axis_y", text="Y", toggle=True)
            sub.prop(context.space_data, "show_axis_z", text="Z", toggle=True)

        ###space###
        if context.mode == 'SCULPT':

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="GROUP")
            row.prop(context.space_data, "use_matcap", icon="MATCAP_22")
            if context.space_data.use_matcap:
                row = col_top.row(align=True)
                row.scale_y = 0.2
                row.scale_x = 0.5
                row.template_icon_view(context.space_data, "matcap_icon")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.prop(context.space_data, "show_only_render", text="Render", icon="RESTRICT_RENDER_ON")
            row.prop(context.space_data, "show_floor", text="Grid", icon="GRID")

            row = col_top.row(align=True)
            row.prop(context.space_data, "show_world", "World", icon="WORLD")

            sub = row.row(1)
            sub.scale_x = 0.335
            sub.prop(context.space_data, "show_axis_x", text="X", toggle=True)
            sub.prop(context.space_data, "show_axis_y", text="Y", toggle=True)
            sub.prop(context.space_data, "show_axis_z", text="Z", toggle=True)


################
### SGrouper ###
################

    ###space###
    if context.mode == 'OBJECT':

        ###space###
        if lt.display_sgrouper:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sgrouper", text="", icon='TRIA_DOWN')
            row.label("Group...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_sgrouper", text="", icon='TRIA_RIGHT')
            row.label("Group...")

            row.menu('wkst.group_menu', "", icon="GROUP")
            row.menu('group.smartjoin_menu', "", icon="LOCKVIEW_ON")

        ###space###
        if lt.display_sgrouper:
            ###space###

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator('sjoin.join', "Smart Join", icon="LOCKVIEW_ON")
            row.operator('sjoin.separate', "Separate Join", icon="LOCKVIEW_OFF")

            row = col_top.row(align=True)
            row.operator('sjoin.expand', "Expand", icon="PASTEDOWN")
            row.operator('sjoin.collapse', "Collapse", icon="COPYDOWN")

            row = col_top.row(align=True)
            row.operator('sjoin.join_add', "Add 2 Smart", icon="PASTEFLIPUP")
            row.operator('sjoin.update_rec', "Update", icon="LOAD_FACTORY")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)

            if context.scene.name.endswith(SCENE_SGR) is False:
                sg_settings = scene.sg_settings

                row.operator("super_grouper.super_group_add", icon='ZOOMIN', text="")
                row.operator("super_grouper.super_group_remove", icon='ZOOMOUT', text="")

                row.label()
                op = row.operator("super_grouper.change_selected_objects", text="", emboss=False, icon='BBOX')
                op.sg_objects_changer = 'BOUND_SHADE'

                row.label()
                op = row.operator("super_grouper.super_group_move", icon='TRIA_UP', text="")
                op.do_move = 'UP'

                op = row.operator("super_grouper.super_group_move", icon='TRIA_DOWN', text="")
                op.do_move = 'DOWN'

                """
                 row = col_top.row(align=True)
                 if scene.super_groups and scene.super_groups[scene.super_groups_index].use_toggle:

                     op = row.operator("super_grouper.change_grouped_objects", text="", emboss=False, icon='COLOR_GREEN')
                     op.sg_group_changer = 'COLOR_WIRE'

                     op = row.operator("super_grouper.change_grouped_objects", text="", emboss=False, icon='COLOR_RED')
                     op.sg_group_changer = 'DEFAULT_COLOR_WIRE'

                 if scene.super_groups:
                     row.prop(scene.super_groups[scene.super_groups_index], "wire_color", text='')

                 """

                row = col_top.row()
                row.template_list("SG_named_super_groups", "", scene, "super_groups", scene, "super_groups_index")

                row = col_top.row(1)
                row.operator("super_grouper.add_to_group", text="Add")
                row.operator("super_grouper.super_remove_from_group", text="Remove")
                row.operator("super_grouper.clean_object_ids", text="Clean")

                #layout.label(text="Selection Settings:")
                row = col_top.row()
                row.prop(sg_settings, "select_all_layers", text='L')
                row.prop(sg_settings, "unlock_obj", text='L')
                row.prop(sg_settings, "unhide_obj", text='H')


##############
### Rename ###
##############

    ###space###
    if context.mode == 'OBJECT':

        # Rename Settings
        #--------------------#
        #scn = context.scene
        #rs = bpy.context.scene
        #--------------------#

        ###space###
        if lt.display_rename:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_rename", text="", icon='TRIA_DOWN')
            row.label("ReName...")

        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_rename", text="", icon='TRIA_RIGHT')
            row.label("ReName...")

            row.operator("object.copynametodata", "", icon="OOPS")

        ###space###
        if lt.display_rename:
            ###space###
            col_top = box.column(align=True)
            row = layout.row(align=True)
            row.alignment = 'EXPAND'

            # ----------- RESPECT ORDER ------------------ #

            col = row.column()
            subrow = col.row()
            subrow.prop(context.scene, 'rno_bool_keepOrder', text='')
            subrow.enabled = False
            col = row.column()
            subrow = col.row()
            subrow.operator("object.rno_keep_selection_order", "Respect Selection")

            # ----------- NEW NAME ------------------ #

            row = layout.row()
            box = row.box()
            rbox = box.row(align=True)
            rbox.prop(context.scene, "rno_str_new_name")
            rbox = box.row(align=True)
            rbox.prop(context.scene, "rno_bool_numbered")
            rbox.prop(context.scene, "rno_str_numFrom")
            rbox = box.column(1)
            rbox.operator("object.rno_setname", "Set new Name", icon="FONT_DATA")
            rbox.operator("object.copynametodata", "Copy to Data Name", icon="OOPS")

            # ----------- REPLACE NAME ------------------ #

            row = layout.row()
            box = row.box()
            rbox = box.column(align=True)
            rbox.prop(context.scene, "rno_str_old_string")
            rbox.prop(context.scene, "rno_str_new_string")
            box.operator("object.rno_replace_in_name", "Replace Name")

            # ----------- ADD SUBFIX / PREFIX NAME ------------------ #
            row = layout.row()
            box = row.box()
            rbox = box.row()

            box.prop(context.scene, 'rno_bool_keepIndex', text='keep object Index')
            rbox.prop(context.scene, "rno_str_prefix")
            rbox.prop(context.scene, "rno_str_subfix")

            box.operator("object.rno_add_subfix_prefix", "Add Subfix / Prefix")


#############
### Bsurf ###
### Bsurf ###
#############

    ###space###
    if context.mode == 'EDIT_MESH':

        ###space###
        if lt.display_bsurf:
            ###space###
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_bsurf", text="", icon='TRIA_DOWN')
            row.label("Bsurfaces...")
        else:
            box = layout.box()
            row = box.row(1)
            row.prop(lt, "display_bsurf", text="", icon='TRIA_RIGHT')

            row.label("Bsurfaces...")
            op = row.operator("gpencil.surfsk_add_surface", text="", icon='MOD_DYNAMICPAINT')

        ###space###
        if lt.display_bsurf:
            ###space###

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("gpencil.surfsk_edit_strokes", text="Edit Strokes", icon='MOD_DYNAMICPAINT')

            row = col_top.row(align=True)
            row.prop(scn, "SURFSK_cyclic_cross")
            row = col_top.row(align=True)
            row.prop(scn, "SURFSK_cyclic_follow")
            row = col_top.row(align=True)
            row.prop(scn, "SURFSK_loops_on_strokes")
            row = col_top.row(align=True)
            row.prop(scn, "SURFSK_automatic_join")
            row = col_top.row(align=True)
            row.prop(scn, "SURFSK_keep_strokes")


# ---------------------------------------------------------------------

class alignz(bpy.types.Operator):
    """align selected to Z-axis / depend by pivot"""
    bl_label = "align z"
    bl_idname = "mesh.face_align_z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}


######################################################################################################################################################
############------------############
############  REGISTER  ############
############------------############
######################################################################################################################################################


# registering and menu integration
def register():
    bpy.types.Scene.isEdgerRunning = False
    bpy.types.Scene.deselectGroups = True
    bpy.types.Scene.isSelectFlush = bpy.props.BoolProperty(name="Flush", description="If vertex is not selected deselect parent face", default=False)
    bpy.types.Scene.isEdgerActive = True
    bpy.types.Scene.isTestActive = True
    bpy.types.Scene.isEdgerDebugActive = bpy.props.BoolProperty(name="Draw", description="Toggle if edge loops should be drawn", default=True)

    bpy.utils.register_module(__name__)


# unregistering and removing menus
def unregister():

    bpy.utils.unregister_module(__name__)

    try:
        del bpy.types.WindowManager.retopowindowtool
    except:
        pass


if __name__ == "__main__":
    register()
