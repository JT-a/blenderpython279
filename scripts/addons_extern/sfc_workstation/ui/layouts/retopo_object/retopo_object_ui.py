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
#    "name": "Workstation Object",
#    "author": "mkbreuer",
#    "version": (0, 1, 0),
#    "blender": (2, 76, 0),
#    "location": "View3D > Toolbar > Workstation ",
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


######################################################################################################

class Dropdown_Wkst_Object_Props(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.wkst_window_object
    """

    ### Objectmode ###

    display_object_geom = bpy.props.BoolProperty(name="Add", description="Display Add Geometry Tools", default=False)
    display_object_selectobm = bpy.props.BoolProperty(name="Selection", description="Display Selection Tools", default=False)
    display_object_select = bpy.props.BoolProperty(name="Selection", description="Display Selection Tools", default=False)
    display_object_modif = bpy.props.BoolProperty(name="Modifier Tools", description="Display Modifier Tools", default=False)
    display_object_mirrcut = bpy.props.BoolProperty(name="Auto Mirror Cut", description="Display Auto Mirror Cut Tools", default=False)
    display_object_normal = bpy.props.BoolProperty(name="Normals", description="Display Face & Vertex Normal Tools", default=False)
    display_object_shade = bpy.props.BoolProperty(name="Visual", description="Display Visualisation & Shading Tools", default=False)
    display_object_check = bpy.props.BoolProperty(name="Mesh Check", description="Display Mesh Check Tools", default=False)
    display_object_bsurf = bpy.props.BoolProperty(name="Bsurface", description="Display Bsurface Tools", default=False)
    display_object_setgeom = bpy.props.BoolProperty(name="Add Primitive", description="Display Add Primitive Tools", default=False)
    display_object_curvegeo = bpy.props.BoolProperty(name="Curve Shape", description="Display Curve Shape Tools", default=False)
    display_object_placegeom = bpy.props.BoolProperty(name="Copy & Rearrange Objects", description="Display Copy & Rearrange Objects Tools", default=False)
    display_object_placepivot = bpy.props.BoolProperty(name="Pivot & Origin", description="Pivot & Origin Tools", default=False)
    display_object_snapshot = bpy.props.BoolProperty(name="SnapShot Mesh", description="SnapShot Mesh Tools", default=False)
    display_object_view = bpy.props.BoolProperty(name="View", description="View Tools", default=False)

    ### Editmode ###
    display_object_editselect = bpy.props.BoolProperty(name="Selection", description="Display Selection Tools", default=False)
    display_object_editpivot = bpy.props.BoolProperty(name="Pivot & Origin", description="Pivot & Origin Tools", default=False)
    display_object_vertalign = bpy.props.BoolProperty(name="Align", description="Display Vertex Align Tools", default=False)
    display_object_vertpivot = bpy.props.BoolProperty(name="Pivot & Origin", description="Pivot & Origin Tools", default=False)
    display_object_subdiv = bpy.props.BoolProperty(name="Subdivide", description="Display Subdivide & Cutting Tools", default=False)
    display_object_vertedit = bpy.props.BoolProperty(name="Edit", description="Display Edit Tools", default=False)
    display_object_extrude = bpy.props.BoolProperty(name="Extrude", description="Display Extrusion Tools", default=False)

    display_object_bool = bpy.props.BoolProperty(name="Boolean, Join, Convert", description="Display Boolean, Join, Convert Tools", default=False)
    display_object_bool2 = bpy.props.BoolProperty(name="Boolean, Join, Convert", description="Display Boolean, Join, Convert Tools", default=False)
    display_object_sgrouper = bpy.props.BoolProperty(name="SGrouper", description="Display Group Tools", default=False)
    display_object_curveloft = bpy.props.BoolProperty(name="Curve Tools 2", description="Display Curve Tools 2", default=False)
    display_object_curveinfo = bpy.props.BoolProperty(name="Curve Tools 2", description="Display Curve Tools 2", default=False)
    display_object_rename = bpy.props.BoolProperty(name="Rename Tool", description="Display Rename Tool", default=False)
    display_object_miraedit = bpy.props.BoolProperty(name="Mira Edit Tools", description="Display Mira Edit Tools", default=False)
    display_object_miracurve = bpy.props.BoolProperty(name="Mira Edit Tools", description="Display Mira Edit Tools", default=False)
    display_object_arrayobj = bpy.props.BoolProperty(name="Array Tools", description="Display Array Tools", default=False)
    display_object_transform = bpy.props.BoolProperty(name="Transform Tools", description="Display Transform Tools", default=False)
    display_object_bboxback = bpy.props.BoolProperty(name="BBox Origin", description="Display BBox Origin Tools", default=False)
    display_object_bboxmiddle = bpy.props.BoolProperty(name="BBox Origin", description="Display BBox Origin Tools", default=False)
    display_object_bboxfront = bpy.props.BoolProperty(name="BBox Origin", description="Display BBox Origin Tools", default=False)
    display_object_imexport = bpy.props.BoolProperty(name="Import", description="Display Import Tools", default=False)

    display_object_greaseset = bpy.props.BoolProperty(name="GP Settings", description="Display Grease Pencil Settings", default=False)
    display_object_deform = bpy.props.BoolProperty(name="Deform", description="Display Deform Tools", default=False)


bpy.utils.register_class(Dropdown_Wkst_Object_Props)
bpy.types.WindowManager.wkst_window_object = bpy.props.PointerProperty(type=Dropdown_Wkst_Object_Props)


######################################################################################################


def draw_retopo_object_ui(self, context, layout):
    lt = context.window_manager.wkst_window_object

    obj = context.object
    scene = context.scene
    scn = context.scene
    rs = bpy.context.scene
    ob = context.object
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout = self.layout


# Title

    obj = context.active_object
    if obj:
        obj_type = obj.type

        if obj_type in {'MESH'}:
            box = layout.box()
            row = box.row(1)
            row.alignment = "CENTER"
            row.label("MESH EDITING")

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

# Add

    box = layout.box().column(1)
    row = box.row(1)
    row.alignment = 'CENTER'
    sub = row.row(1)
    sub.scale_x = 1
    sub.menu("INFO_MT_mesh_add", text="", icon='OUTLINER_OB_MESH')
    sub.menu("INFO_MT_curve_add", text="", icon='OUTLINER_OB_CURVE')
    sub.menu("INFO_MT_surface_add", text="", icon='OUTLINER_OB_SURFACE')
    sub.menu("INFO_MT_metaball_add", text="", icon="OUTLINER_OB_META")
    sub.operator("object.camera_add", icon='OUTLINER_OB_CAMERA', text="")
    sub.menu("INFO_MT_armature_add", text="", icon="OUTLINER_OB_ARMATURE")

    row = box.row(1)
    row.alignment = 'CENTER'
    sub = row.row(1)
    sub.scale_x = 1
    sub.operator("object.empty_add", text="", icon="OUTLINER_OB_EMPTY")
    sub.operator("object.add", text="", icon="OUTLINER_OB_LATTICE").type = "LATTICE"
    sub.operator("object.text_add", text="", icon="OUTLINER_OB_FONT")
    sub.operator("object.lamp_add", icon='OUTLINER_OB_LAMP', text="")
    sub.operator("object.speaker_add", icon='OUTLINER_OB_SPEAKER', text="")
    sub.operator_menu_enum("object.effector_add", "type", text="", icon="SOLO_ON")


# Pivot

    box = layout.box()
    row = box.row(1)
    sub = row.row(1)
    sub.scale_x = 7
    sub.operator("view3d.pivot_bounding_box", "", icon="ROTATE")
    sub.operator("view3d.pivot_3d_cursor", "", icon="CURSOR")
    sub.operator("view3d.pivot_active", "", icon="ROTACTIVE")
    sub.operator("view3d.pivot_individual", "", icon="ROTATECOLLECTION")
    sub.operator("view3d.pivot_median", "", icon="ROTATECENTER")
    row.menu("object.wkstdelete", text="", icon="PANEL_CLOSE")


# Im-Export

    if lt.display_object_imexport:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_imexport", text="", icon='TRIA_DOWN')
        row.label("Im-Export...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_imexport", text="", icon='TRIA_RIGHT')
        row.label("Im-Export...")

        row.operator("view3d.background_images_fast_import", text="", icon='IMAGE_DATA')
        row.menu("wkst.import_export", text="", icon='EXPORT')
        row.menu("wkst.link_append", text="", icon='APPEND_BLEND')

    if lt.display_object_imexport:

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("view3d.background_images_fast_import", icon='IMAGE_DATA')

        box = layout.box().column(1)

        row = box.column(1)
        row.alignment = 'CENTER'
        row.scale_x = 1.25
        row.menu("INFO_MT_file_import", text="Import", icon='EXPORT')
        row.menu("INFO_MT_file_export", text="Export", icon='IMPORT')
        row.menu("OBJECT_MT_selected_export", text="Export Selected", icon='IMPORT')

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("wm.link", text="Link", icon='LINK_BLEND')
        row.operator("wm.append", text="Append", icon='APPEND_BLEND')

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("object.proxy_make")
        row.operator("object.make_local")

        box = layout.box().column(1)

        row = box.row(1)
        pack_all = box.row()
        pack_all.operator("file.pack_all")
        pack_all.active = not bpy.data.use_autopack

        unpack_all = box.row()
        unpack_all.operator("file.unpack_all")
        unpack_all.active = not bpy.data.use_autopack

        icon = 'CHECKBOX_HLT' if bpy.data.use_autopack else 'CHECKBOX_DEHLT'
        row.operator("file.autopack_toggle", text="autom. Pack into .blend", icon=icon)

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("file.make_paths_relative")
        row.operator("file.make_paths_absolute")
        row.operator("file.report_missing_files")
        row.operator("file.find_missing_files")


# View

    if lt.display_object_view:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_view", text="", icon='TRIA_DOWN')
        row.label("3d-View...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_view", text="", icon='TRIA_RIGHT')
        row.label("3d-View...")

        row.operator("view3d.view_all", "", icon="ZOOM_OUT")
        row.operator("view3d.view_selected", "", icon="ZOOM_IN")
        row.operator("view3d.zoom_border", "", icon="BORDERMOVE")

    if lt.display_object_view:

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("view3d.view_all", "All", icon="ZOOM_OUT")
        row.operator("view3d.view_center_cursor", text="Cursor", icon="ZOOM_PREVIOUS")
        row.operator("view3d.view_selected", "Selected", icon="ZOOM_IN")
        row.operator("view3d.zoom_border", "Zoom Border", icon="BORDERMOVE")

        row = box.separator()
        row = box.row(1)
        row.operator("view3d.viewnumpad", text="Top").type = 'TOP'
        row.operator("view3d.viewnumpad", text="Front").type = 'FRONT'
        row.operator("view3d.viewnumpad", text="Left").type = 'LEFT'

        row = box.row(1)
        row.operator("view3d.viewnumpad", text="Bottom").type = 'BOTTOM'
        row.operator("view3d.viewnumpad", text="Back").type = 'BACK'
        row.operator("view3d.viewnumpad", text="Right").type = 'RIGHT'

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("view3d.localview", text="Global/Local")
        row.operator("view3d.view_persportho", text="Persp/Ortho")

        box = layout.box().column(1)

        row = box.row(1)
        row.label(text="View to Object:")

        row = box.row(1)
        row.prop(context.space_data, "lock_object", text="")


# Add

    if lt.display_object_setgeom:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_setgeom", text="", icon='TRIA_DOWN')
        row.label("Retopo...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_setgeom", text="", icon='TRIA_RIGHT')
        row.label("Retopo...")

        row.menu("origin.retopo_menu", text="", icon='RETOPO')
        row.menu("object.bbox_retopo_menu", text="", icon="BBOX")

    if lt.display_object_setgeom:

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Empty Objects")

        row = box.column(1)
        row.operator("mesh.emptyroom_cen", text="-> Center", icon='LAYER_ACTIVE')
        row.operator("mesh.emptyroom_sel", text="-> Selected", icon='LAYER_ACTIVE')
        row.operator("mesh.emptyxroom_cen", text="-> Center mirrored", icon='MOD_MIRROR')
        row.operator("mesh.emptyxroom_sel", text="-> Selected mirrored", icon='MOD_MIRROR')

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("object.bounding_box", text="Bounding Box", icon="MESH_CUBE")
        row.operator("object.bounding_boxers", text="Wire Bounding Box", icon="BBOX")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("bbox.align_vertices", text="Execute ZBox-Rectangle")

        row = box.row(1)
        row.prop(context.scene, "AutoAlign_axis", text="Align Axis", expand=True)


# Selection

    if lt.display_object_selectobm:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_selectobm", text="", icon='TRIA_DOWN')
        row.label("Select...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_selectobm", text="", icon='TRIA_RIGHT')
        row.label("Select...")

        row.menu("VIEW3D_MT_object_showhide", "", icon="VISIBLE_IPO_ON")
        row.operator("view3d.select_border", text="", icon="BORDER_RECT")
        row.operator("view3d.select_circle", text="", icon="BORDER_LASSO")

    if lt.display_object_selectobm:
        box = layout.box().column(1)

        row = box.row(1)
        row.operator("view3d.select_border", text="Border", icon="BORDER_RECT")
        row.operator("view3d.select_circle", text="Cirlce", icon="BORDER_LASSO")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.move_to_layer", text="Move to Layer")
        row.menu("VIEW3D_MT_object_showhide", "Hide / Show", icon="VISIBLE_IPO_ON")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.select_all").action = 'TOGGLE'
        row.operator("object.select_all", text="Inverse").action = 'INVERT'

        row = box.row(1)
        row.operator("object.throughselected", text="Cycle through")
        row.operator("object.select_linked", text="Single Active").type = 'OBDATA'

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.select_random", text="Random")
        row.operator("object.select_mirror", text="Mirror")

        row = box.row(1)
        row.operator("object.select_by_layer", text="All by Layer")
        row.operator("object.select_camera", text="Camera")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.select_linked", text="Linked", icon="EXPORT")
        row.operator("object.select_grouped", text="Group", icon="EXPORT")

        row = box.row(1)
        row.operator("object.select_by_type", text="Type", icon="EXPORT")
        row.operator("object.select_pattern", text="Name", icon="EXPORT")

        box = layout.box().column(1)

        row = box.row(1)
        row.menu("wkst.freezeall", text="Un-/ Freeze by Type", icon="FREEZE")

        row = box.row(1)
        row.operator("vfxtoolbox.defreeze_all_objects", text="UnFreeze all", icon="FREEZE")
        row.operator("vfxtoolbox.freeze_selected_objects", text="Freeze", icon="FREEZE")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("view3d.bbox_select", "BBox", icon="RESTRICT_SELECT_OFF")
        row.operator("view3d.bbox_select_wire", "WBox", icon="RESTRICT_SELECT_OFF")
        row.operator("view3d.bbox_select_zyl", "ZBox", icon="RESTRICT_SELECT_OFF")


# Origin

    if lt.display_object_placepivot:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_placepivot", text="", icon='TRIA_DOWN')
        row.label("Pivot...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_placepivot", text="", icon='TRIA_RIGHT')

        row.label("Pivot...")
        row.menu("origin.setupmenu_obm", text="", icon="LAYER_ACTIVE")
        row.menu("wkst.snaptocursor", "", icon="FORCE_FORCE")
        row.menu("wkst.snaptoselect", "", icon="RESTRICT_SELECT_OFF")

    if lt.display_object_placepivot:
        box = layout.box().column(1)

        row = box.row(1)
        row.operator_menu_enum("object.origin_set", "type", text="Set Origin", icon="LAYER_ACTIVE")

        row = box.row(1)
        if lt.display_object_bboxback:
            row.scale_y = 1.2
            row.prop(lt, "display_object_bboxback", text="Back +Y", icon='TRIA_DOWN')

        else:
            row.scale_y = 1
            row.prop(lt, "display_object_bboxback", text="Back +Y", icon='TRIA_RIGHT')

        if lt.display_object_bboxback:
            box = layout.box().column(1)

            # Top
            row = box.row(1)
            row.alignment = 'CENTER'
            row.scale_x = 1.55

            row.operator("object.cubeback_cornertop_minus_xy", "", icon="LAYER_ACTIVE")  # "Back- Left -Top")
            row.operator("object.cubeback_edgetop_minus_y", "", icon="LAYER_ACTIVE")  # "Back - Top")
            row.operator("object.cubeback_cornertop_plus_xy", "", icon="LAYER_ACTIVE")  # "Back- Right -Top ")

            # Middle
            row = box.row(1)
            row.alignment = 'CENTER'
            row.scale_x = 1.55
            row.operator("object.cubefront_edgemiddle_minus_x", "", icon="LAYER_ACTIVE")  # "Back- Left")
            row.operator("object.cubefront_side_plus_y", "", icon="LAYER_ACTIVE")  # "Back")
            row.operator("object.cubefront_edgemiddle_plus_x", "", icon="LAYER_ACTIVE")  # "Back- Right")

            # Bottom
            row = box.row(1)
            row.alignment = 'CENTER'
            row.scale_x = 1.55
            row.operator("object.cubeback_cornerbottom_minus_xy", "", icon="LAYER_ACTIVE")  # "Back- Left -Bottom")
            row.operator("object.cubefront_edgebottom_plus_y", "", icon="LAYER_ACTIVE")  # "Back - Bottom")
            row.operator("object.cubeback_cornerbottom_plus_xy", "", icon="LAYER_ACTIVE")  # "Back- Right -Bottom")

            box = layout.box().column(1)
            row = box.column(1)

        if lt.display_object_bboxmiddle:
            row.scale_y = 1.2
            row.prop(lt, "display_object_bboxmiddle", text="Middle", icon='TRIA_DOWN')

        else:
            row.scale_y = 1
            row.prop(lt, "display_object_bboxmiddle", text="Middle", icon='TRIA_RIGHT')

        if lt.display_object_bboxmiddle:
            box = layout.box().column(1)

            # Top
            row = box.row(1)
            row.alignment = 'CENTER'
            row.scale_x = 1.55

            row.operator("object.cubefront_edgetop_minus_x", "", icon="LAYER_ACTIVE")  # "Middle - Left Top")
            row.operator("object.cubefront_side_plus_z", "", icon="LAYER_ACTIVE")  # "Top")
            row.operator("object.cubefront_edgetop_plus_x", "", icon="LAYER_ACTIVE")  # "Middle - Right Top")

            # Middle
            row = box.row(1)
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
            row = box.row(1)
            row.alignment = 'CENTER'
            row.scale_x = 1.55

            row.operator("object.cubefront_edgebottom_minus_x", "", icon="LAYER_ACTIVE")  # "Middle - Left Bottom")
            row.operator("object.cubefront_side_minus_z", "", icon="LAYER_ACTIVE")  # "Bottom")
            row.operator("object.cubefront_edgebottom_plus_x", "", icon="LAYER_ACTIVE")  # "Middle - Right Bottom")

            box = layout.box().column(1)
            row = box.row(1)

        if lt.display_object_bboxfront:
            row.scale_y = 1.2
            row.prop(lt, "display_object_bboxfront", text="Front -Y", icon='TRIA_DOWN')

        else:
            row.scale_y = 1
            row.prop(lt, "display_object_bboxfront", text="Front -Y", icon='TRIA_RIGHT')

        if lt.display_object_bboxfront:
            box = layout.box().column(1)

            # Top
            row = box.row(1)
            row.alignment = 'CENTER'
            row.scale_x = 1.55

            row.operator("object.cubefront_cornertop_minus_xy", "", icon="LAYER_ACTIVE")  # "Front- Left -Top"
            row.operator("object.cubeback_edgetop_plus_y", "", icon="LAYER_ACTIVE")  # "Front - Top"
            row.operator("object.cubefront_cornertop_plus_xy", "", icon="LAYER_ACTIVE")  # "Front- Right -Top"

            # Middle
            row = box.row(1)
            row.alignment = 'CENTER'
            row.scale_x = 1.55

            row.operator("object.cubefront_edgemiddle_minus_y", "", icon="LAYER_ACTIVE")  # "Front- Left"
            row.operator("object.cubefront_side_minus_y", "", icon="LAYER_ACTIVE")  # "Front"
            row.operator("object.cubefront_edgemiddle_plus_y", "", icon="LAYER_ACTIVE")  # "Front- Right"

            # Bottom
            row = box.row(1)
            row.alignment = 'CENTER'
            row.scale_x = 1.55

            row.operator("object.cubefront_cornerbottom_minus_xy", "", icon="LAYER_ACTIVE")  # "Front- Left -Bottom"
            row.operator("object.cubefront_edgebottom_minus_y", "", icon="LAYER_ACTIVE")  # "Front - Bottom"
            row.operator("object.cubefront_cornerbottom_plus_xy", "", icon="LAYER_ACTIVE")  # "Front- Right -Bottom")

        box = layout.box().column(1)

        row = box.row(1)
        row.prop(context.object, "show_bounds", text="Show Bounds", icon='STICKY_UVS_LOC')

        sub = row.row(1)
        sub.scale_x = 0.5
        sub.prop(context.object, "draw_bounds_type", text="")

        box = layout.box().column(1)

        row = box.row(1)
        row.menu("wkst.snaptocursor", "Cursor to... ", icon="FORCE_FORCE")

        row = box.row(1)
        row.menu("wkst.snaptoselect", "Selection to... ", icon="RESTRICT_SELECT_OFF")


# Transform

    if lt.display_object_transform:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_transform", text="", icon='TRIA_DOWN')
        row.label("Transform...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_transform", text="", icon='TRIA_RIGHT')
        row.label("Transform...")

        row.menu("wkst.transform_menu", "", icon="MANIPUL")
        row.menu("wkst.normal_transform_menu", "", icon="AXIS_SIDE")
        row.menu("VIEW3D_MT_mirror", "", icon="ARROW_LEFTRIGHT")

        #row.operator("mesh.snap_utilities_rotate", text = "", icon="NDOF_TURN")
        #row.operator("mesh.snap_utilities_move", text = "", icon="NDOF_TRANS")

    if lt.display_object_transform:

        box = layout.box().column(1)

        row = box.row(1)
        sub = row.row(1)
        sub.scale_x = 7
        sub.operator("wm.context_toggle", text="", icon='MANIPUL').data_path = "space_data.show_manipulator"


        box = layout.box().column(1)

        row = box.row(1)
        row.operator("transform.translate", text="(G)", icon="MAN_TRANS")
        row.operator("transform.rotate", text="(R)", icon="MAN_ROT")
        row.operator("transform.resize", text="(S)", icon="MAN_SCALE")

        row = box.row(1)
        row.menu("translate.normal_menu", text="N-Move")
        row.menu("rotate.normal_menu", text="N-Rotate")
        row.menu("resize.normal_menu", text="N-Scale")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.mirror1", text="MX", icon='ARROW_LEFTRIGHT')
        row.operator("object.mirror2", text="MY", icon='ARROW_LEFTRIGHT')
        row.operator("object.mirror3", text="MZ", icon='ARROW_LEFTRIGHT')

        box = layout.box().column(1)

        row = box.row(1)
        row.menu("VIEW3D_MT_object_clear", icon="PANEL_CLOSE")
        row.menu("VIEW3D_MT_object_apply", icon="FILE_TICK")

        box = layout.box().column(1)

        row = box.row(1)
        row.label(text="", icon="MAN_TRANS")
        row.prop(context.object, 'location', text="")

        row = box.row(1)
        row.label(text="", icon="MAN_ROT")
        row.prop(context.object, 'rotation_euler', text="")

        row = box.row(1)
        row.label(text="", icon="MAN_SCALE")
        row.prop(context.object, 'scale', text="")

        row = box.row(1)
        row.label(text="", icon="MOD_MESHDEFORM")
        row.prop(context.object, 'dimensions', text="")

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("freeze_transform.selected", text="Set all to 0", icon="NDOF_DOM")
        row.operator("object.duplicate", text="Duplicate Object", icon="ZOOMIN")


# Align

    if lt.display_object_placegeom:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_placegeom", text="", icon='TRIA_DOWN')
        row.label("Obj-Align...")
    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_placegeom", text="", icon='TRIA_RIGHT')
        row.label("Obj-Align...")

        row.menu("align.scale_menu", text="", icon='MAN_SCALE')
        row.menu("align.rotation_menu", text="", icon='MAN_ROT')
        row.menu("align.location_menu", text="", icon='MAN_TRANS')

    if lt.display_object_placegeom:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.align_tools", icon="ROTATE")
        row = box.row(1)
        row.operator("object.align_by_faces", text="Active Face to Active Face", icon="SNAP_SURFACE")
        row = box.row(1)
        row.operator("object.drop_on_active", text="Drop down to Active", icon="NLA_PUSHDOWN")
        row = box.row(1)
        row.operator("object.distribute_osc", text="Distribute Objects", icon="ALIGN")

        box = layout.box().column(1)

        row = box.row(1)
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

        row = box.row(1)
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

        row = box.row(1)
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


# Sculpt

    obj = context.active_object
    if obj:
        obj_type = obj.type
        if obj_type in {'MESH', 'LATTICE'}:

            if lt.display_object_bool:
                ###space###
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_bool", text="", icon='TRIA_DOWN')
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
                row.prop(lt, "display_object_bool", text="", icon='TRIA_RIGHT')

                obj = context.active_object
                if obj:
                    obj_type = obj.type

                    if obj_type in {'MESH'}:
                        row.label("Sculpt...")

                        row.menu("object.decimatefreeze_menu", "", icon='FREEZE')
                        row.menu("draw.gpencil_menu", "", icon='SCULPTMODE_HLT')
                        row.menu("object.boolean_menu", "", icon='FULLSCREEN_EXIT')

                    if obj_type in {'LATTICE'}:

                        row.prop(context.object.data, "use_outside")
                        row.prop_search(context.object.data, "vertex_group", context.object, "vertex_groups", text="")

                        box = layout.box().column(1)

                        row = box.row(1)
                        row.prop(context.object.data, "points_u", text="X")
                        row.prop(context.object.data, "points_v", text="Y")
                        row.prop(context.object.data, "points_w", text="Z")

                        row = box.row(1)
                        row.prop(context.object.data, "interpolation_type_u", text="")
                        row.prop(context.object.data, "interpolation_type_v", text="")
                        row.prop(context.object.data, "interpolation_type_w", text="")

                else:
                    row.label("Please select an object as an active!")

            if lt.display_object_bool:

                obj = context.active_object
                if obj:
                    obj_type = obj.type

                    if obj_type in {'MESH'}:

                        box = layout.box().column(1)

                        row = box.row(1)
                        row.operator("sculpt.remesh", text='Remesh', icon='MOD_REMESH')
                        row.prop(context.window_manager, 'remeshPreserveShape', text="Preserve Shape")

                        row = box.row(1)
                        row.prop(context.window_manager, 'remeshDepthInt', text="Depth")
                        row.prop(context.window_manager, 'remeshSubdivisions', text="Subdivisions")

                        box = layout.box().column(1)

                        row = box.row(1)
                        row.operator("object.join", text="Join", icon="FULLSCREEN_EXIT")

                        union = row.operator("mesh.boolean", "Union", icon='ZOOMIN')
                        union.modOp = 'UNION'

                        row = box.row(1)
                        difference = row.operator("mesh.boolean", "Difference", icon='ZOOMOUT')
                        difference.modOp = 'DIFFERENCE'

                        intersect = row.operator("mesh.boolean", "Intersect", icon='PANEL_CLOSE')
                        intersect.modOp = 'INTERSECT'

                        box = layout.box().column(1)

                        row = box.row(1)
                        row.operator("boolean.separate", text="Separate")
                        row.operator("boolean.clone", text="Clone")

                        box = layout.box().column(1)

                        row = box.row(1)
                        row.operator("boolean.freeze", text="Freeze")
                        row.operator("boolean.unfreeze", text="Unfreeze")

                        row = box.row(1)
                        row.operator("boolean.grease_symm", text='Symmetrize')
                        row.prop(context.window_manager, "bolsymm", text="")

                        box = layout.box().column(1)

                        row = box.column(1)
                        row.operator("grease.execution", text='Grease Cut', icon="SCULPTMODE_HLT")

                        row = box.row(1)
                        row.operator("wkst_grp.purge", text='Purge/Unlink', icon="PANEL_CLOSE")
                        row.operator("boolean.purge_pencils", text='Purge Grease', icon="PANEL_CLOSE")

                        row = box.row(1)

                        row.operator("gpencil.draw", text=" ", icon="DISCLOSURE_TRI_DOWN").mode = 'ERASER'
                        row.operator("gpencil.draw", text=" ", icon="NOCURVE").mode = 'DRAW_POLY'
                        row.operator("gpencil.draw", text=" ", icon="BRUSH_DATA").mode = 'DRAW'
                        row.operator("gpencil.draw", text=" ", icon="GREASEPENCIL").mode = 'DRAW_STRAIGHT'

                        box = layout.box().column(1)

                        row = box.row(1)
                        if context.space_data.type == 'VIEW_3D':
                            row.prop(context.tool_settings, "grease_pencil_source", expand=True)

                        elif context.space_data.type == 'CLIP_EDITOR':
                            row.prop(context.space_data, "grease_pencil_source", expand=True)

                        if context.active_gpencil_layer:
                            box = layout.box().column(1)


                            row = box.row(1)
                            row.prop(context.active_gpencil_layer, "show_points", text="View Points", icon="PARTICLE_POINT")
                            row.operator("gpencil.convert", text="Convert", icon="CURVE_BEZCURVE")

                            box = layout.box().column(1)

                            row = box.row(1)
                            row.prop(context.gpencil_data, "use_stroke_edit_mode", text="Enable Editing", icon='EDIT', toggle=True)

                            if lt.display_object_greaseset:

                                box = layout.box()
                                row = box.row(1)
                                row.prop(lt, "display_object_greaseset", text="", icon='TRIA_DOWN')
                                row.label("GP Settings")

                            else:
                                box = layout.box()
                                row = box.row(1)
                                row.prop(lt, "display_object_greaseset", text="", icon='TRIA_RIGHT')
                                row.label("GP Settings")

                            if lt.display_object_greaseset:

                                box = layout.box().column(1)

                                row = box.column(1)
                                row.alignment = 'CENTER'
                                row.label("Active Layer")
                                row = box.column(1)
                                row.prop(context.active_gpencil_layer, "info", text="")

                                row = box.row(1)
                                row.prop(context.gpencil_data.layers, "active_index")

                                row = box.row(1)
                                row.operator("gpencil.layer_add", icon='ZOOMIN', text="Add Layer")
                                row.operator("gpencil.layer_remove", icon='ZOOMOUT', text="Del. Layer")

                                row = box.row(1)
                                row.prop(context.active_gpencil_layer, "lock")
                                row.prop(context.active_gpencil_layer, "hide")

                                box = layout.box().column(1)

                                row = box.column(1)
                                row.alignment = 'CENTER'
                                row.label(text="Stroke")
                                row = box.row(1)

                                row = box.column(1)
                                row.prop(context.active_gpencil_layer, "use_onion_skinning")

                            box = layout.box().column(1)

                            row = box.row(1)
                            box.prop(context.user_preferences.edit, "grease_pencil_manhattan_distance", text="Manhattan Distance")
                            box.prop(context.user_preferences.edit, "grease_pencil_euclidean_distance", text="Euclidean Distance")


                    if obj_type in {'LATTICE'}:
                        box = layout.box().column(1)

                        row = box.row(1)
                        row.prop(context.object.data, "use_outside")
                        row.prop_search(context.object.data, "vertex_group", context.object, "vertex_groups", text="")

                        box = layout.box().column(1)

                        row = box.row(1)
                        row.prop(context.object.data, "points_u", text="X")
                        row.prop(context.object.data, "points_v", text="Y")
                        row.prop(context.object.data, "points_w", text="Z")

                        row = box.row(1)
                        row.prop(context.object.data, "interpolation_type_u", text="")
                        row.prop(context.object.data, "interpolation_type_v", text="")
                        row.prop(context.object.data, "interpolation_type_w", text="")


# CurveTools

    obj = context.active_object
    if obj:
        obj_type = obj.type

        if obj_type in {'CURVE'}:

            if lt.display_object_curvegeo:
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_curvegeo", text="", icon='TRIA_DOWN')
                row.label("Curve...")

            else:
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_curvegeo", text="", icon='TRIA_RIGHT')
                row.label("Curve...")

                sub = row.row(1)
                sub.scale_x = 0.4
                sub.prop(context.object.data, "resolution_u", text="")
                row.menu("wkst.curve_edit_menu", "", icon="CURVE_BEZCIRCLE")

            if lt.display_object_curvegeo:
                box = layout.box().column(1)

                row = box.row(1)
                row.prop(context.object.data, "dimensions", expand=True)

                row = box.row(1)
                row.operator("curve.to_poly", "Poly")
                row.operator("curve.to_bezier", "Bezièr")
                row.operator("curve.to_nurbs", "Nurbs")

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("curve.open_circle", text="Open/Close", icon="MOD_CURVE")
                row.operator("curve.simplify", "Simplify", icon="IPO_EASE_IN_OUT")

                row = box.row(1)
                row.operator("object.duplicate_move_linked", text="Dupli-Linked", icon="LINKED")
                row.operator("curve.smoothspline", "Smooth", icon="SMOOTHCURVE")

                box = layout.box().column(1)

                row = box.row(1)
                row.prop(context.object.data, "fill_mode", text="")
                row.prop(context.object.data, "use_fill_deform")

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("object.wire_all", text="", icon='WIRE')
                row.prop(context.object.data, "bevel_depth", text="Bevel Depth")

                row = box.row(1)
                row.prop(context.object.data, "resolution_u", text="Rings")
                row.prop(context.object.data, "bevel_resolution", text="Loops")

                row = box.row(1)
                row.prop(context.object.data, "offset")
                row.prop(context.object.data, "extrude", "Height")

                box = layout.box().column(1)

                row = box.row(1)
                row.label(text="Bevel Length Factor:")

                row.active = (context.object.data.bevel_depth > 0 or context.object.data.bevel_object is not None)

                row = box.row(1)
                row.prop(context.object.data, "bevel_factor_start", text="Start")
                row.prop(context.object.data, "bevel_factor_end", text="End")

                row = box.row(1)
                row.prop(context.object.data, "bevel_factor_mapping_start", text="")
                row.prop(context.object.data, "bevel_factor_mapping_end", text="")

                row = box.row(1)
                sub = row.row()
                sub.active = context.object.data.taper_object is not None
                sub.prop(context.object.data, "use_map_taper")

                sub = row.row()
                sub.active = context.object.data.bevel_object is not None
                sub.prop(context.object.data, "use_fill_caps")

                box = layout.box().column(1)

                if context.mode == 'OBJECT':
                    row = box.row(1)
                    row.operator("curve.bevelcurve", "BevelCurve", icon="CURVE_BEZCIRCLE")

                row = box.row(1)
                row.label(text="Bevel Object:")
                row.prop(context.object.data, "bevel_object", text="")

                box = layout.box().column(1)

                if context.mode == 'OBJECT':
                    row = box.row(1)
                    row.operator("curve.tapercurve", "TaperCurve", icon="CURVE_BEZCURVE")

                row = box.row(1)
                row.label(text="Taper Object:")
                row.prop(context.object.data, "taper_object", text="")

                box = layout.box().column(1)

                row = box.row(1)
                row.label(text="Path / Curve-Deform:")
                row = box.row(1)
                row.prop(context.object.data, "use_radius")
                row.prop(context.object.data, "use_stretch")
                row.prop(context.object.data, "use_deform_bounds")

                row = box.row(1)
                row.label(text="Twisting:")
                row = box.row(1)
                row.active = (context.object.data.dimensions == '2D' or (context.object.data.bevel_object is None and context.object.data.dimensions == '3D'))
                row.prop(context.object.data, "twist_mode", text="")
                row.prop(context.object.data, "twist_smooth", text="Smooth")


# CurveTools2

            if lt.display_object_curveloft:

                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_curveloft", text="", icon='TRIA_DOWN')
                row.label("CurveT2...")

            else:

                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_curveloft", text="", icon='TRIA_RIGHT')
                row.label("CurveT2...")

                row.menu("wkst.splinetype_menu", "", icon="IPO_BEZIER")
                row.menu("wkst.ct2d_menu", text="", icon="DISCLOSURE_TRI_DOWN")
                row.menu("wkst.ct2_menu", text="", icon="ANIM_DATA")

            if lt.display_object_curveloft:

                box = layout.box().column(1)

                row = box.row(1)
                row.alignment = "CENTER"
                row.label("", icon="INFO")

                row = box.row(1)
                row.operator("curvetools2.operatorselectioninfo", text="Selection Info:")
                row.prop(context.scene.curvetools, "NrSelectedObjects", text="")

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("object.wire_all", text="", icon='WIRE')
                row.prop(context.object.data, "resolution_u", text="Set Resolution")

                row = box.row(1)
                row.operator("curve.open_circle", text="Open/Close", icon="MOD_CURVE")
                row.operator("curve.switch_direction_obm", "Direction", icon="ARROW_LEFTRIGHT")

                box = layout.box().column(1)

                row = box.row(1)
                row.scale_y = 1.5
                row.operator("curvetools2.operatorsweepcurves", text="Sweep")
                row.operator("curvetools2.operatorloftcurves", text="Loft")

                row = box.row(1)
                row.scale_y = 1.5
                row.operator("curvetools2.operatorbirail", text="Birail")
                row.operator("curvetools2.operatorsweepandmorph", text="Morph")

                row = box.row(1)
                row.scale_y = 1.5
                row.operator("curvetools2.operatorrevolvecurves", text="Revolver")
#                row.prop(context.scene.curvetools, "AngularResolution", text="AngRes")

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("curvetools2.operatorintersectcurves", text="Intersect Curves")
                row = box.row(1)
                row.prop(context.scene.curvetools, "LimitDistance", text="LimitDistance")

                box = layout.box().column(1)
                box = layout.box().column(1)

                row = box.row(align=0)
                row.prop(context.scene.curvetools, "IntersectCurvesAlgorithm", text="Algorithm")

                row = box.row(align=0.1)
                row.prop(context.scene.curvetools, "IntersectCurvesMode", text="Mode")

                row = box.row(align=0.1)
                row.prop(context.scene.curvetools, "IntersectCurvesAffect", text="Affect")

                box = layout.box().column(1)

                row = box.row(1)
                row.alignment = "CENTER"
                row.label("Optimize Tools for BezièrCurve", icon="LAMP")

                row = box.row(1)
                row.operator("curvetools2.operatorsplinesjoinneighbouring", text="Join neighbouring splines")

                row = box.row(1)
                row.prop(context.scene.curvetools, "SplineJoinDistance", text="Threshold join")

                box = layout.box().column(1)
                box = layout.box().column(1)

                row = box.row(1)
                row.prop(context.scene.curvetools, "SplineJoinStartEnd", text="Only at start & end")

                row = box.row(align=0.5)
                row.prop(context.scene.curvetools, "SplineJoinMode", text="Join")

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("curvetools2.operatorsplinesremovezerosegment", text="del 0-segments")
                row.operator("curvetools2.operatorsplinesremoveshort", text="del short splines")

                row = box.row(1)
                row.prop(context.scene.curvetools, "SplineRemoveLength", text="Threshold remove")


# Deform

    obj = context.active_object
    if obj:
        obj_type = obj.type

        if obj_type in {'MESH'}:

            if lt.display_object_deform:

                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_deform", text="", icon='TRIA_DOWN')
                row.label("Deform...")

            else:
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_deform", text="", icon='TRIA_RIGHT')
                row.label("Deform...")

                row.menu("wkst_menu.vertex_group", text="", icon="GROUP_VERTEX")
                row.menu("wkst.miradeform_menu", text="", icon="OUTLINER_OB_MESH")
                row.operator("object.easy_lattice", text="", icon="MOD_LATTICE")

            if lt.display_object_deform:

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("retopo.latticeapply", text="Apply Easy Lattice", icon="MOD_LATTICE")

                row = box.row(1)
                row.operator("boolean.mesh_deform", text="Mesh Deform", icon="MOD_MESHDEFORM")

                if(bpy.types.Scene.isEdgerRunning):

                    box = layout.box().column(1)

                    row = box.row(1)
                    row.operator("uv.toggle_edger", text="Stop Edger", icon="X_VEC")

                    box = layout.box().column(1)

                    row = box.row(1)

                    ic = "UNLOCKED"
                    if bpy.types.Scene.isEdgerActive:
                        ic = "LOCKED"
                    row.operator("uv.toggle_edger_locking", text="Lock", icon=ic)

                    ic = "RESTRICT_SELECT_OFF"
                    if bpy.types.Scene.deselectGroups:
                        ic = "RESTRICT_SELECT_ON"
                    row.operator("uv.toggle_edger_deselecting", text="Deselect", icon=ic)

                    row = box.row(1)
                    row.prop(context.scene, 'isEdgerDebugActive')
                    row.prop(context.scene, 'isSelectFlush')

                    row = box.row(1)
                    row.operator("wm.lock_edge_loop_idname", text="Add", icon="ZOOMIN")
                    row.operator("wm.unlock_edge_loop_idname", text="Remove", icon="ZOOMOUT")

                    row = box.row(1)
                    row.operator("wm.clear_edger_oops_idname", text="Clear Loops", icon="MOD_SOLIDIFY")

                else:
                    box = layout.box().column(1)

                    row = box.row(1)
                    row.operator("uv.toggle_edger", text="Run Edger", icon="POSE_HLT")

                box = layout.box().column(1)

                row = box.row(1)
                row.alignment = 'CENTER'
                row.label("Vertex Group", icon="GROUP_VERTEX")

                row = box.row(1)
                row.operator("object.vertex_group_add", text="Add", icon='ZOOMIN')
                row.operator("object.vertex_group_remove", text="Remove", icon='ZOOMOUT').all = False

                if context.object.vertex_groups.active:
                    row = box.row(1)
                    row.template_list("MESH_UL_vgroups", "", context.object, "vertex_groups", context.object.vertex_groups, "active_index", rows=1)

                    row = box.row(1)
                    row.prop(context.object.vertex_groups, "active_index")

                    row = box.row(1)
                    row.operator("object.vertex_group_assign", text="Assign to...", icon="DISCLOSURE_TRI_RIGHT")
                    row.operator("object.vertex_group_remove_from", text="Remove from...", icon="DISCLOSURE_TRI_DOWN")

                    row = box.row(1)
                    row.operator("object.vertex_group_select", text="Select Grp", icon="RESTRICT_SELECT_OFF")
                    row.operator("object.vertex_group_deselect", text="Deselect Grp", icon="RESTRICT_SELECT_ON")

                    box = layout.box().column(1)
                    box = layout.box().column(1)
                    box = layout.box().column(1)
                    row = box.row(1)
                    row.menu("MESH_MT_vertex_group_specials", icon='TRIA_RIGHT', text="Specials")
                    row.prop(context.tool_settings, "vertex_group_weight", text="Weight")


# Modifier

    obj = context.active_object
    if obj:
        obj_type = obj.type

        if obj_type in {'MESH', 'CURVE', 'SURFACE', 'LATTICE', 'META', 'FONT'}:
            if lt.display_object_modif:

                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_modif", text="", icon='TRIA_DOWN')
                row.label("Modifier...")

            else:
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_modif", text="", icon='TRIA_RIGHT')
                row.label("Modifier...")

                row.menu("wkst.modispace", "", icon='MODIFIER')
                row.menu("modifiers.viewport_obm", "", icon='RESTRICT_VIEW_OFF')
                row.operator("view3d.display_modifiers_delete", "", icon='X')
                row.operator("view3d.display_modifiers_apply", "", icon='FILE_TICK')

            if lt.display_object_modif:

                box = layout.box().column(1)

                row = box.row(1)
                row.operator_menu_enum("object.modifier_add", "type", icon='MODIFIER')

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("view3d.display_modifiers_viewport_off", "Off", icon='VISIBLE_IPO_OFF')
                row.operator("view3d.display_modifiers_viewport_on", "On ", icon='RESTRICT_VIEW_OFF')

                row = box.row(1)
                row.operator("view3d.display_modifiers_delete", "Delete", icon='X')
                row.operator("view3d.display_modifiers_apply", "Apply", icon='FILE_TICK')

                box = layout.box().column(1)

                row = box.row(1)
                row.alignment = 'CENTER'
                row.label("SubSurf Levels")

                row = box.row(1)
                row.operator("view3d.modifiers_subsurf_level_0")
                row.operator("view3d.modifiers_subsurf_level_1")
                row.operator("view3d.modifiers_subsurf_level_2")
                row.operator("view3d.modifiers_subsurf_level_3")
                row.operator("view3d.modifiers_subsurf_level_4")
                row.operator("view3d.modifiers_subsurf_level_5")
                row.operator("view3d.modifiers_subsurf_level_6")

                box = layout.box().column(1)

                row = box.row(1)
                row.alignment = 'CENTER'
                row.label("Mirror Modifier")

                row = box.row(1)
                row.operator("view3d.fullmirror", text="X-Clip")
                row.operator("view3d.fullmirrory", text="Y-Clip")
                row.operator("view3d.fullmirrorz", text="Z-Clip")

                box = layout.box().column(1)

                row = box.row(1)
                row.alignment = 'CENTER'
                row.label("Move over the Modifier Stack")

                row = box.row(1)
                row.operator("view3d.display_modifiers_expand", icon='DISCLOSURE_TRI_DOWN')
                row.operator("view3d.display_modifiers_collapse", icon='DISCLOSURE_TRI_RIGHT')


# MirrorCut

    obj = context.active_object
    if obj:
        obj_type = obj.type

        if obj_type in {'MESH'}:

            ###space###
            if lt.display_object_mirrcut:

                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_mirrcut", text="", icon='TRIA_DOWN')
                row.label("MirrorCut...")

            else:
                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_mirrcut", text="", icon='TRIA_RIGHT')

                row.label("MirrorCut...")

                sub = row.row(1)
                sub.scale_x = 0.3
                sub.prop(context.scene, "AutoMirror_orientation", text="")
                sub.prop(context.scene, "AutoMirror_axis", text="")
                row.menu("wkst.mirrorcut", text="", icon="MOD_WIREFRAME")

            if lt.display_object_mirrcut:
                box = layout.box().column(1)

                row = box.row(1)
                row.operator("object.automirror", text="Execute AutoMirror", icon="MOD_WIREFRAME")

                row = box.row(1)
                row.prop(context.scene, "AutoMirror_orientation", text="")
                row.prop(context.scene, "AutoMirror_axis", text="")

                row = box.row(1)
                row.prop(context.scene, "AutoMirror_threshold", text="Threshold")

                box = layout.box().column(1)
                row = box.row(1)
                row.prop(context.scene, "AutoMirror_toggle_edit", text="Stay in Editmode")
                row = box.row(1)
                row.prop(context.scene, "AutoMirror_cut", text="Cut+Mirror")
                if bpy.context.scene.AutoMirror_cut:
                    row.prop(context.scene, "AutoMirror_use_clip", text="Use Clip")
                    row = box.row(1)
                    row.prop(context.scene, "AutoMirror_show_on_cage", text="Editable")
                    row.prop(context.scene, "AutoMirror_apply_mirror", text="Apply")

                else:
                    row.label(icon="ERROR", text="No mesh selected")

                box = layout.box().column(1)

                row = box.row(1)
                row.alignment = "CENTER"
                row.label("Mesh Delete")

                row = box.row(1)
                row.operator("modifier.positiv_x_cut_obm", text="+X")
                row.operator("modifier.positiv_y_cut_obm", text="+Y")
                row.operator("modifier.positiv_z_cut_obm", text="+Z")

                row = box.row(1)
                row.operator("modifier.negativ_x_cut_obm", text="-X")
                row.operator("modifier.negativ_y_cut_obm", text="-Y")
                row.operator("modifier.negativ_z_cut_obm", text="-Z")


# SnapShot

    obj = context.active_object
    if obj:
        obj_type = obj.type

        if obj_type in {'MESH'}:

            if lt.display_object_snapshot:

                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_snapshot", text="", icon='TRIA_DOWN')
                row.label("SnapShot...")

            else:

                box = layout.box()
                row = box.row(1)
                row.prop(lt, "display_object_snapshot", text="", icon='TRIA_RIGHT')
                row.label("SnapShot...")

                row.operator("vtools.usesnapshot", icon='RECOVER_LAST', text="")
                row.operator("vtools.deletesnapshot", icon='DISCLOSURE_TRI_DOWN', text="")
                row.operator("vtools.capturesnapshot", icon='DISCLOSURE_TRI_RIGHT', text="")

            if lt.display_object_snapshot:

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("vtools.capturesnapshot", icon='DISCLOSURE_TRI_RIGHT', text="Add")
                row.operator("vtools.deletesnapshot", icon='DISCLOSURE_TRI_DOWN', text="Remove")

                box = layout.box().column(1)

                row = box.row(1)
                row.template_list('UI_UL_list', "snapShotMesh_ID", obj, "snapShotMeshes", obj, "snapShotMesh_ID_index", rows=2)

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("vtools.recalculatesnapshotfromchildren", icon='BORDERMOVE', text="Recalculate")
                row.operator("vtools.usesnapshot", icon='RECOVER_LAST', text="Set Geometry")

                box = layout.box().column(1)

                row = box.row(1)
                row.operator("vtools.deleteallsnapshot", icon='X', text="Del. All")
                row.operator("vtools.deleteunusedsnapshotlist", icon='CANCEL', text="Del. Unused")

                row = box.row(1)
                row.prop(context.scene, "mod_list", text="")
                row.operator("ba.delete_data_obs", "DelOrphan", icon="PANEL_CLOSE")


# CopyShop

    if lt.display_object_arrayobj:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_arrayobj", text="", icon='TRIA_DOWN')
        row.label("Copy...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_arrayobj", text="", icon='TRIA_RIGHT')

        row.label("Copy...")

        row.menu("wkst.copy_links_data", "", icon="CONSTRAINT")
        row.menu("wkst.copy_link", text="", icon="LINKED")
        row.menu("wkst.copy_dupli", text="", icon="MOD_ARRAY")

    if lt.display_object_arrayobj:

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("mft.radialclone", text="Radial Clone", icon="FILE_REFRESH")
        row.operator("object.simplearewo", text="Replicator", icon="TRIA_RIGHT")
        row.operator("object.cursor_array", text="Copy 2 Cursor", icon="NEXT_KEYFRAME")

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("object.make_links_data", "Set Instance", icon="LINKED").type = 'OBDATA'
        row.operator("object.makesingle", "Clear Instance", icon="UNLINKED")

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("object.select_linked", text="Select Linked", icon="RESTRICT_SELECT_OFF")
        row.operator_menu_enum("object.make_links_data", "type", " Make Links Data", icon="CONSTRAINT")

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("object.copy_selected_modifiers", text="Copy Modifier", icon="PASTEFLIPDOWN")
        row.operator("switch.mod_display", "Copy Modifier Display", icon="PASTEFLIPDOWN")

        box = layout.box().column(1)

        scene = context.scene
        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Copy Modifier")

        row = box.row(1)
        row.operator("scene.to_all", text="-> Selected").mode = "modifier, selected"
        row.operator("scene.to_all", text="-> Children").mode = "modifier, children"

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Append Modifier")

        row = box.row(1)
        row.operator("scene.to_all", text="-> Selected").mode = "modifier, selected, append"
        row.operator("scene.to_all", text="-> Children").mode = "modifier, children, append"

        row = box.row(1)
        row.prop(context.scene, "excludeMod")

        box = layout.box().column(1)

        scene = context.scene
        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Copy Material")

        row = box.row(1)
        row.operator("scene.to_all", text="-> Selected").mode = "material, selected"
        row.operator("scene.to_all", text="-> Children").mode = "material, children"

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Append Material")

        row = box.row(1)
        row.operator("scene.to_all", text="-> Selected").mode = "material, selected, append"
        row.operator("scene.to_all", text="-> Children").mode = "material, children, append"


# MeshCheck

    if lt.display_object_check:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_check", text="", icon='TRIA_DOWN')
        row.label("Check...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_check", text="", icon='TRIA_RIGHT')

        row.label("Check...")

        row.operator("view3d.rec_normals", "", icon="SNAP_NORMAL")
        row.menu("wkst.modifly", '', icon="MOD_SOFT")
        row.menu("wkst.material_menu", text="", icon='MATERIAL_DATA')
        row.menu("wkst.meshcheck_menu", text="", icon='GROUP_VCOL')

    if lt.display_object_check:

        view = context.space_data
        obj = context.object

        box = layout.box().column(1)

        row = box.row()
        row.alignment = 'CENTER'
        row.label("Mesh Check", icon='LAMP')

        row = box.row(1)
        row.operator("view3d.rec_normals", "Recalculate Normals", icon="SNAP_NORMAL")

        row = box.column(1)
        row.operator("object.add_materials", text="Display color", icon='GROUP_VCOL')
        row.operator("object.remove_materials", text="Hidde color", icon='GROUP_VERTEX')

        box = layout.box().column(1)

        row = box.row()
        row.alignment = 'CENTER'
        row.label("Object Color", icon='LAMP')

        row = box.row(1)
        row.operator("object.material_slot_remove", text="Material", icon="ZOOMOUT")
#        row.operator("object.material_add", text="Material", icon='ZOOMIN')

        row = box.row(1)
        row.prop(context.object, "color", text="")

        row = box.row(1)
        row.operator("material.remove", text="Remove all Material", icon="ZOOMOUT")

        box = layout.box().column(1)

        row = box.row()
        row.alignment = 'CENTER'
        row.label("Flymode for HighRes", icon='MOD_SOFT')

        row = box.row(1)
        row.operator("view3d.fast_navigate_operator", 'Start', icon="PLAY")
        row.operator("view3d.fast_navigate_stop_new", 'Stop', icon="PAUSE")

        row = box.row(1)
        row.prop(context.scene, "OriginalMode", "")
        row.prop(context.scene, "FastMode", "")

        row = box.row(1)
        row.prop(context.scene, "EditActive", "Edit mode")

        row = box.row(1)
        row.prop(context.scene, "Delay")
        row.prop(scene, "DelayTimeGlobal")

        row = box.row(1)
        row.prop(context.scene, "ShowParticles")
        row.prop(context.scene, "ParticlesPercentageDisplay")


# Visuals

    if lt.display_object_shade:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_shade", text="", icon='TRIA_DOWN')
        row.label("Visual...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_shade", text="", icon='TRIA_RIGHT')

        row.label("Visual...")

        row.menu("wkst.display_menu", text="", icon="UI")
        row.menu("wkst.meshdisplay_menu", text="", icon="META_CUBE")
        row.menu("wkst.shade_menu", text="", icon="SMOOTH")
        row.menu("wkst.wire_menu", text="", icon='WIRE')

    if lt.display_object_shade:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.shade_smooth", text="Smooth", icon="SMOOTH")
        row.operator("object.shade_flat", text="Flat", icon="MESH_CIRCLE")

        row = box.row(1)


        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.wire_all", text="Wire all", icon='WIRE')

        row = box.row(1)
        row.operator("view3d.display_wire_off", "Wire off", icon='MESH_PLANE')
        row.operator("view3d.display_wire_on", "Wire on", icon='MESH_GRID')

        box = layout.box().column(1)

        row = box.row(1)
        row.prop(context.object, "show_x_ray", text="X-Ray", icon="META_CUBE")
        row.prop(context.space_data, "show_backface_culling", text="Backface", icon="OUTLINER_OB_LATTICE")

        row = box.row(1)
        op = row.operator("super_grouper.change_selected_objects", text="Material Shade", icon='GHOST_DISABLED')
        op.sg_objects_changer = 'MATERIAL_SHADE'

        op = row.operator("super_grouper.change_selected_objects", text="Wire Shade", icon='GHOST_ENABLED')
        op.sg_objects_changer = 'WIRE_SHADE'

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.toggle_silhouette", icon="RADIO")

        box = layout.box().column(1)

        row = box.row(1)
        row.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="GROUP")
        row.prop(context.space_data, "use_matcap", icon="MATCAP_01")

        if context.space_data.use_matcap:
            row = box.row(1)
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


# Grouper

    if lt.display_object_sgrouper:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_sgrouper", text="", icon='TRIA_DOWN')
        row.label("Group...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_sgrouper", text="", icon='TRIA_RIGHT')
        row.label("Group...")

        row.menu('wkst.group_menu', "", icon="GROUP")
#        row.menu('group.smartjoin_menu', "", icon="LOCKVIEW_ON")

    if lt.display_object_sgrouper:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator('sjoin.join', "Smart Join", icon="LOCKVIEW_ON")
        row.operator('sjoin.separate', "Separate Join", icon="LOCKVIEW_OFF")

        row = box.row(1)
        row.operator('sjoin.expand', "Expand", icon="PASTEDOWN")
        row.operator('sjoin.collapse', "Collapse", icon="COPYDOWN")

        row = box.row(1)
        row.operator('sjoin.join_add', "Add 2 Smart", icon="PASTEFLIPUP")
        row.operator('sjoin.update_rec', "Update", icon="LOAD_FACTORY")

        box = layout.box().column(1)

        row = box.row(1)

        if context.scene.name.endswith(SCENE_SGR) is False:
            sg_settings = scene.sg_settings

            row.operator("super_grouper.super_group_add", icon='ZOOMIN', text="")
            row.operator("super_grouper.super_group_remove", icon='ZOOMOUT', text="")

            row.separator()

            op = row.operator(
                "super_grouper.change_selected_objects", text="", emboss=False, icon='BBOX')
            op.sg_objects_changer = 'BOUND_SHADE'

            op = row.operator(
                "super_grouper.change_selected_objects", text="", emboss=False, icon='WIRE')
            op.sg_objects_changer = 'WIRE_SHADE'

            op = row.operator(
                "super_grouper.change_selected_objects", text="", emboss=False, icon='MATERIAL')
            op.sg_objects_changer = 'MATERIAL_SHADE'

            op = row.operator(
                "super_grouper.change_selected_objects", text="", emboss=False, icon='RETOPO')
            op.sg_objects_changer = 'SHOW_WIRE'

            op = row.operator(
                "super_grouper.change_selected_objects", text="", emboss=False, icon='SOLID')
#            op.sg_objects_changer = 'HIDE_WIRE'

            row.separator()
            op = row.operator("super_grouper.super_group_move", icon='TRIA_UP', text="")
            op.do_move = 'UP'

            op = row.operator("super_grouper.super_group_move", icon='TRIA_DOWN', text="")
            op.do_move = 'DOWN'

            row = box.row()
            row.template_list("SG_named_super_groups", "", scene, "super_groups", scene, "super_groups_index")

            row = box.row(1)
            row.operator("super_grouper.add_to_group", text="Add")
            row.operator("super_grouper.super_remove_from_group", text="Remove")
            row.operator("super_grouper.clean_object_ids", text="Clean")

            row = box.row()
            row.prop(sg_settings, "unlock_obj", text='UnLock')
            row.prop(sg_settings, "unhide_obj", text='UnHide')

            row = box.row()
            row.prop(sg_settings, "select_all_layers", text='Select all Layers')


# Rename Settings

    if lt.display_object_rename:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_rename", text="", icon='TRIA_DOWN')
        row.label("ReName...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_object_rename", text="", icon='TRIA_RIGHT')
        row.label("ReName...")

        row.operator("object.copynametodata", "", icon="OOPS")

    if lt.display_object_rename:

        box = layout.box()
        row = box.row(1)
        sub = row.row(1)
        sub.prop(context.scene, 'rno_bool_keepOrder', text='')
        sub.enabled = False

        row.operator("object.rno_keep_selection_order", "Respect Selection")

        row = layout.row()
        box = row.box()
        rbox = box.row(1)
        rbox.prop(context.scene, "rno_str_new_name")

        rbox = box.row(1)
        rbox.prop(context.scene, "rno_bool_numbered")
        rbox.prop(context.scene, "rno_str_numFrom")

        rbox = box.column(1)
        rbox.operator("object.rno_setname", "Set new Name", icon="FONT_DATA")
        rbox.operator("object.copynametodata", "Copy to Data Name", icon="OOPS")

        row = layout.row()
        box = row.box()
        rbox = layout.box().column(1)
        rbox.prop(context.scene, "rno_str_old_string")
        rbox.prop(context.scene, "rno_str_new_string")
        box.operator("object.rno_replace_in_name", "Replace Name")

        row = layout.row()
        box = row.box()
        rbox = box.row()

        box.prop(context.scene, 'rno_bool_keepIndex', text='keep object Index')
        rbox.prop(context.scene, "rno_str_prefix")
        rbox.prop(context.scene, "rno_str_subfix")

        box.operator("object.rno_add_subfix_prefix", "Add Subfix / Prefix")


# Register

class SimpleCustomMenu(bpy.types.Menu):
    """Bsurfaces Menu"""
    bl_label = "Bsurfaces Menu"
    bl_idname = "wkst_menu.bsurfaces"

    def draw(self, context):
        layout = self.layout

        if context.mode == 'EDIT_CURVE':
            layout.operator("curve.surfsk_first_points", text="Set First Points")
            layout.operator("curve.switch_direction", text="Switch Direction")
            layout.operator("curve.surfsk_reorder_splines", text="Reorder Splines")

        if context.mode == 'EDIT_MESH':
            layout.operator("gpencil.surfsk_add_surface", text="Add Surface", icon='MOD_DYNAMICPAINT')
            layout.operator("gpencil.surfsk_edit_strokes", text="Edit Strokes", icon='MOD_DYNAMICPAINT')

            layout.separator()

            layout.prop(context.scene, "SURFSK_cyclic_cross")
            layout.prop(context.scene, "SURFSK_cyclic_follow")
            layout.prop(context.scene, "SURFSK_loops_on_strokes")
            layout.prop(context.scene, "SURFSK_automatic_join")
            layout.prop(context.scene, "SURFSK_keep_strokes")


def register():
    bpy.types.Scene.isEdgerRunning = False
    bpy.types.Scene.deselectGroups = True
    bpy.types.Scene.isSelectFlush = bpy.props.BoolProperty(name="Flush", description="If vertex is not selected deselect parent face", default=False)
    bpy.types.Scene.isEdgerActive = True
    bpy.types.Scene.isTestActive = True
    bpy.types.Scene.isEdgerDebugActive = bpy.props.BoolProperty(name="Draw", description="Toggle if edge loops should be drawn", default=True)

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_module(__name__)

    try:
        del bpy.types.WindowManager.wkst_window_object
    except:
        pass


if __name__ == "__main__":
    register()
