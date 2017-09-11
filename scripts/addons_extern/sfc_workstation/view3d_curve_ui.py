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
#    "name": "Workstation Curve",
#    "author": "mkbreuer",
#    "version": (0, 1, 0),
#    "blender": (2, 76, 0),
#    "location": "View3D > Toolbar > Workstation",
#    "warning": "",
#    "description": "Toolkit for the Main Panel",
#    "wiki_url": "",
#    "category": "",
#}


import bpy
from bpy import*


########################################################################################################

class Dropdown_Wkst_Curve_Props(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.wkst_window_curve
    """
    display_curve_modifier = bpy.props.BoolProperty(name="Modifier Tools", description="Display Modifier Tools", default=False)
    display_curve_align = bpy.props.BoolProperty(name="Align", description="Display Align Tools", default=False)
    display_curve_edit = bpy.props.BoolProperty(name="Editing", description="Display Editing Tools", default=False)
    display_curve_tools = bpy.props.BoolProperty(name="Curve", description="Display Curve Tools", default=False)
    display_curve_visual = bpy.props.BoolProperty(name="Shading", description="Display Shading Tools", default=False)
    display_curve_select = bpy.props.BoolProperty(name="Selection", description="Display Selection Tools", default=False)
    display_curve_transform = bpy.props.BoolProperty(name="Transform", description="Display Transform Tools", default=False)
    display_curve_pivot = bpy.props.BoolProperty(name="Pivot & Origin", description="Display Pivot & Origin Tools", default=False)
    display_curve_geo = bpy.props.BoolProperty(name="Shape Geometry", description="Display Shape Geometry Tools", default=False)
    display_curve_view = bpy.props.BoolProperty(name="View", description="Display View Tools", default=False)
    display_curve_bsurf = bpy.props.BoolProperty(name="Bsurface", description="Display Bsurface Tools", default=False)

bpy.utils.register_class(Dropdown_Wkst_Curve_Props)
bpy.types.WindowManager.wkst_window_curve = bpy.props.PointerProperty(type=Dropdown_Wkst_Curve_Props)

########################################################################################################


def draw_wkst_curve_ui(self, context, layout):
    lt = context.window_manager.wkst_window_curve
    obj = context.object
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout = self.layout.column_flow(1)


# Title

    box = layout.box()
    row = box.row(1)
    row.alignment = "CENTER"
    row.label("CURVE EDITING")


# Add

    box = layout.box()
    row = box.row(1)
    row.alignment = 'CENTER'

    sub = row.row(1)
    sub.scale_x = 1.2
    sub.operator("curve.primitive_bezier_curve_add", icon='CURVE_BEZCURVE', text="")
    sub.operator("curve.primitive_bezier_circle_add", icon='CURVE_BEZCIRCLE', text="")
    sub.operator("curve.primitive_nurbs_curve_add", icon='CURVE_NCURVE', text="")
    sub.operator("curve.primitive_nurbs_circle_add", icon='CURVE_NCIRCLE', text="")
    sub.operator("curve.primitive_nurbs_path_add", icon='CURVE_PATH', text="")
    row.operator("object.curv_to_2d", text="2d")
    row.operator("object.curv_to_3d", text="3d")


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
    row.operator("curve.delete", "", icon="PANEL_CLOSE")


# View

    if lt.display_curve_view:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_view", text="", icon='TRIA_DOWN')
        row.label("View...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_view", text="", icon='TRIA_RIGHT')
        row.label("View...")

        row.operator("view3d.view_all", "", icon="ZOOM_OUT")
        row.operator("view3d.view_selected", "", icon="ZOOM_IN")
        row.operator("view3d.zoom_border", "", icon="BORDERMOVE")

    if lt.display_curve_view:

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


# Selection

    if lt.display_curve_select:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_select", text="", icon='TRIA_DOWN')
        row.label("Select...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_select", text="", icon='TRIA_RIGHT')
        row.label("Select...")

        row.menu("VIEW3D_MT_edit_curve_showhide", "", icon="VISIBLE_IPO_ON")
        row.operator("view3d.select_circle", text="", icon="BORDER_LASSO")
        row.operator("view3d.select_border", text="", icon="BORDER_RECT")

    if lt.display_curve_select:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("view3d.select_border", text="Border", icon="BORDER_RECT")
        row.operator("view3d.select_circle", text="Circle", icon="BORDER_LASSO")

        box = layout.box().column(1)

        row = box.row(1)
        row.menu("VIEW3D_MT_edit_curve_showhide", icon="VISIBLE_IPO_ON")

        row = box.separator()
        row = box.row(1)
        row.operator("curve.select_all", text="Inverse").action = 'INVERT'
        row.operator("curve.select_random", text="Random")

        row = box.row(1)
        row.operator("curve.select_linked", text="Linked")
        row.operator("curve.select_nth", text="Checker")

        row = box.row(1)
        row.operator("curve.de_select_first", text="First")
        row.operator("curve.de_select_last", text="Last")

        row = box.row(1)
        row.operator("curve.select_next", text="Next")
        row.operator("curve.select_previous", text="Previous")


# Origin

    if lt.display_curve_pivot:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_pivot", text="", icon='TRIA_DOWN')
        row.label("Pivot...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_pivot", text="", icon='TRIA_RIGHT')
        row.label("Pivot...")

        row.menu("origin.setupmenu_edm", "", icon="LAYER_ACTIVE")
        row.menu("wkst.snaptocursor", "", icon="FORCE_FORCE")
        row.menu("wkst.snaptoselect", "", icon="RESTRICT_SELECT_OFF")

    if lt.display_curve_pivot:
        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.origin_obm", "Origin Object", icon="OBJECT_DATAMODE")
        row.operator("object.origin_edm", "Origin Edit", icon="EDITMODE_HLT")

        box = layout.box().column(1)

        row = box.row(1)
        row.menu("wkst.snaptocursor", "Cursor to... ", icon="FORCE_FORCE")

        row = box.row(1)
        row.menu("wkst.snaptoselect", "Selection to... ", icon="RESTRICT_SELECT_OFF")


# Transform

    if lt.display_curve_transform:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_transform", text="", icon='TRIA_DOWN')
        row.label("Transform...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_transform", text="", icon='TRIA_RIGHT')
        row.label("Transform...")

        row.menu("VIEW3D_MT_mirror", "", icon="ARROW_LEFTRIGHT")
        row.menu("wkst.normal_transform_menu", "", icon="AXIS_SIDE")
        row.menu("wkst.transform_menu", "", icon="MANIPUL")

    if lt.display_curve_transform:
        box = layout.box().column(1)

        row = box.row(1)
        sub = row.row(1)
        sub.scale_x = 7
        sub.operator("wm.context_toggle", text="", icon='MANIPUL').data_path = "space_data.show_manipulator"
        sub.operator("object.pie_move", "", icon="MAN_TRANS")
        sub.operator("object.pie_rotate", "", icon="MAN_ROT")
        sub.operator("object.pie_scale", "", icon="MAN_SCALE")
        sub.operator("object.pie_all_manipulators", text="", icon='NDOF_DOM')

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
        row.operator("transform.push_pull", text="Push/Pull")
        row.operator("transform.vertex_warp", text="Warp")

        row = box.row(1)
        row.operator("transform.vertex_random", text="Randomize")
        row.operator("transform.tosphere", "to Sphere")

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("transform.translate", text="Move Texture Space").texture_space = True
        row.operator("transform.resize", text="Scale Texture Space").texture_space = True

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


# Align

    if lt.display_curve_align:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_align", text="", icon='TRIA_DOWN')
        row.label("Align...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_align", text="", icon='TRIA_RIGHT')
        row.label("Align...")

        sub = row.row(1)
        sub.scale_x = 0.35
        sub.operator("mesh.face_align_x", "X", icon='TRIA_RIGHT')
        sub.operator("mesh.face_align_y", "Y", icon='TRIA_UP')
        sub.operator("mesh.face_align_z", "Z", icon='SPACE3')

    if lt.display_curve_align:

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


# Tools

    if lt.display_curve_geo:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_geo", text="", icon='TRIA_DOWN')
        row.label("Curve...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_geo", text="", icon='TRIA_RIGHT')
        row.label("Curve...")

        sub = row.row(1)
        sub.scale_x = 0.4
        sub.prop(context.object.data, "resolution_u", text="")
        row.menu("wkst.curve_edit_menu", "", icon="CURVE_BEZCIRCLE")

    if lt.display_curve_geo:

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("curve.spline_type_set", "Set Spline Type", icon="IPO_BEZIER")
        row.operator("curve.switch_direction", text="Switch Direction", icon="ARROW_LEFTRIGHT")
        row.operator("curve.cyclic_toggle", "Open / Close Curve", icon="MOD_CURVE")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Handles")

        row = box.row(1)
        row.operator("curve.handle_to_free", "Free")
        row.operator("curve.handle_to_automatic", "Auto")

        row = box.row(1)
        row.operator("curve.handle_to_vector", "Vector")
        row.operator("curve.handle_to_aligned", "Aligned")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Subdivide")

        row = box.row(1)
        row.operator("curve.subdivide", text="1").number_cuts = 1
        row.operator("curve.subdivide", text="2").number_cuts = 2
        row.operator("curve.subdivide", text="3").number_cuts = 3
        row.operator("curve.subdivide", text="4").number_cuts = 4
        row.operator("curve.subdivide", text="5").number_cuts = 5
        row.operator("curve.subdivide", text="6").number_cuts = 6

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("curve.extrude_move", text="Extrude")
        row.operator("curve.make_segment", text="Weld")

        row = box.row(1)
        row.operator("curve.split", text="Split")
        row.operator("curve.bezier_spline_divide", text='Divide')

        row = box.row(1)
        row.operator("curve.separate", text="Separate")
        row.operator("curve.bezier_points_fillet", text='Fillet')

        row = box.row(1)
        row.operator("transform.vertex_random")
        row.operator("object._curve_outline", text="Outline")

        row = box.row(1)
        row.operator("transform.tilt", text="Tilt")
        row.operator("curve.radius_set", "Radius")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("curve.smooth", icon="SMOOTHCURVE")
        row.operator("curve.normals_make_consistent", icon="SNAP_NORMAL")

        row = box.row(1)
        row.prop(context.active_object.data, "show_handles", text="Handles")
        row.prop(context.active_object.data, "show_normal_face", text="Normals")

        row = box.row(1)
        row.prop(context.scene.tool_settings, "normal_size", text="Normal Size")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Bevel Curve")

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
        row.label(text="Bevel Factor:")

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

        row = box.row(1)
        row.label(text="Taper Object:")
        row.prop(context.object.data, "taper_object", text="")

        row = box.row(1)
        row.label(text="Bevel Object:")
        row.prop(context.object.data, "bevel_object", text="")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label(text="Path / Curve-Deform")

        row = box.row(1)
        row.prop(context.object.data, "use_radius")
        row.prop(context.object.data, "use_stretch")
        row.prop(context.object.data, "use_deform_bounds")

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label(text="Twisting")

        row = box.row(1)
        row.active = (context.object.data.dimensions == '2D' or (context.object.data.bevel_object is None and context.object.data.dimensions == '3D'))
        row.prop(context.object.data, "twist_mode", text="")
        row.prop(context.object.data, "twist_smooth", text="Smooth")


# CurveTool2

    if lt.display_curve_tools:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_tools", text="", icon='TRIA_DOWN')
        row.label("CurveT2...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_tools", text="", icon='TRIA_RIGHT')
        row.label("CurveT2...")

        row.operator("curve.spline_type_set", "", icon="IPO_BEZIER")
        row.menu("wkst.ct2d_menu", text="", icon="DISCLOSURE_TRI_DOWN")
        row.menu("wkst.ct2_menu", text="", icon="ANIM_DATA")

    if lt.display_curve_tools:
        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = "CENTER"
        row.label("", icon="INFO")

        row = box.row(1)
        row.operator("curvetools2.operatorcurveinfo", text="Curve")
        row.operator("curvetools2.operatorsplinesinfo", text="Splines")
        row.operator("curvetools2.operatorsegmentsinfo", text="Segments")

        row = box.row(1)
        row.operator("curvetools2.operatorselectioninfo", text="Selection Info:")
        row.prop(context.scene.curvetools, "NrSelectedObjects", text="")

        row = box.row(1)
        row.operator("curvetools2.operatorcurvelength", text="Calc Length")
        row.prop(context.scene.curvetools, "CurveLength", text="")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.wire_all", text="", icon='WIRE')
        row.prop(context.object.data, "resolution_u", text="Set Resolution")

        row = box.row(1)
        row.operator("curve.open_circle", text="Open/Close", icon="MOD_CURVE")
        row.operator("curve.switch_direction_obm", "Direction", icon="ARROW_LEFTRIGHT")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = "CENTER"
        row.label("Optimize Tools for BezièrCurve", icon="LAMP")

        row = box.row(1)
        row.operator("curvetools2.operatorsplinesjoinneighbouring", text="Join neighbouring splines", icon="AUTOMERGE_ON")

        row = box.row(1)
        row.prop(context.scene.curvetools, "SplineJoinDistance", text="Threshold join")

        row = box.row(1)
        row.prop(context.scene.curvetools, "SplineJoinStartEnd", text="Only at start & end")

        row = box.row(align=0.5)
        row.prop(context.scene.curvetools, "SplineJoinMode", text="Join")

        row = box.row(1)
        row.operator("curvetools2.operatorsplinesremovezerosegment", text="del 0-segments", icon="DISCLOSURE_TRI_DOWN")
        row.operator("curvetools2.operatorsplinesremoveshort", text="del short splines", icon="DISCLOSURE_TRI_DOWN")

        row = box.row(1)
        row.prop(context.scene.curvetools, "SplineRemoveLength", text="Threshold remove")


# Modifier

    if lt.display_curve_modifier:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_modifier", text="", icon='TRIA_DOWN')
        row.label("Modifier...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_modifier", text="", icon='TRIA_RIGHT')
        row.label("Modifier...")

        row.operator_menu_enum("object.modifier_add", "type", "", icon='MODIFIER')
        row.menu("modifiers.viewport_edm", "", icon='RESTRICT_VIEW_OFF')
        row.operator("view3d.display_modifiers_delete", "", icon='X')

    if lt.display_curve_modifier:

        box = layout.box().column(1)

        row = box.row(1)

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
        row.label("Mirror Modifier / all enabled")

        row = box.row(1)
        row.operator("view3d.fullmirror", text="X-Clip")
        row.operator("view3d.fullmirrory", text="Y-Clip")
        row.operator("view3d.fullmirrorz", text="Z-Clip")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("view3d.display_modifiers_viewport_on", icon='RESTRICT_VIEW_OFF')
        row.operator("view3d.display_modifiers_edit_on", icon='EDITMODE_HLT')
        row.operator("view3d.display_modifiers_cage_on", icon='OUTLINER_OB_MESH')

        row = box.row(1)
        row.operator("view3d.display_modifiers_viewport_off", icon='VISIBLE_IPO_OFF')
        row.operator("view3d.display_modifiers_edit_off", icon='SNAP_VERTEX')
        row.operator("view3d.display_modifiers_cage_off", icon='OUTLINER_DATA_MESH')

        box = layout.box().column(1)

        row = box.row(1)
        row.label("Move over the Modifier Stack")

        row = box.row(1)
        row.operator("view3d.display_modifiers_expand", icon='DISCLOSURE_TRI_DOWN_VEC')
        row.operator("view3d.display_modifiers_collapse", icon='DISCLOSURE_TRI_RIGHT_VEC')


# Visuals

    if lt.display_curve_visual:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_visual", text="", icon='TRIA_DOWN')

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_visual", text="", icon='TRIA_RIGHT')
        row.label("Visual...")

        row.menu("wkst.display_menu", text="", icon="UI")
        row.menu("wkst.meshdisplay_menu", text="", icon="META_CUBE")
        row.operator("object.wire_all", text="", icon='WIRE')

    if lt.display_curve_visual:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("wm.context_toggle", text="Xray", icon='META_CUBE').data_path = "object.show_x_ray"
        row.operator("object.wire_all", text="Wire all", icon='WIRE')

        box = layout.box().column(1)

        row = box.row(1)
        row.prop(context.space_data.fx_settings, "use_ssao", text="AOccl", icon="GROUP")
        row.prop(context.space_data, "use_matcap", icon="MATCAP_22")
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


# Bsurface

    if lt.display_curve_bsurf:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_bsurf", text="", icon='TRIA_DOWN')
        row.label("Bsurfaces...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_curve_bsurf", text="", icon='TRIA_RIGHT')
        row.label("Bsurfaces...")

        row.menu("wkst_menu.bsurfaces", text="", icon='MOD_DYNAMICPAINT')

    if lt.display_curve_bsurf:

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("curve.surfsk_reorder_splines", text="Reorder Splines", icon="MOD_DYNAMICPAINT")
        row.operator("curve.surfsk_first_points", text="Set First Points")
        row.operator("curve.switch_direction", text="Switch Direction")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("wkst_grp.purge", text='Purge/Unlink', icon="PANEL_CLOSE")
        row.operator("boolean.purge_pencils", text='Purge Grease', icon="PANEL_CLOSE")

        row = box.row(1)

        lock = context.tool_settings.use_grease_pencil_sessions
        if lock:
            row.prop(context.tool_settings, "use_grease_pencil_sessions", text=" ", icon="LOCKED")
        else:
            row.prop(context.tool_settings, "use_grease_pencil_sessions", text=" ", icon="UNLOCKED")

        row.operator("gpencil.draw", text=" ", icon="DISCLOSURE_TRI_DOWN").mode = 'ERASER'
        row.operator("gpencil.draw", text=" ", icon="NOCURVE").mode = 'DRAW_POLY'
        row.operator("gpencil.draw", text=" ", icon="BRUSH_DATA").mode = 'DRAW'
        row.operator("gpencil.draw", text=" ", icon="GREASEPENCIL").mode = 'DRAW_STRAIGHT'

        if context.active_gpencil_layer:

            box = layout.box().column(1)

            row = box.row(1)
            if context.space_data.type == 'VIEW_3D':
                row.prop(context.tool_settings, "grease_pencil_source", expand=True)

            elif context.space_data.type == 'CLIP_EDITOR':
                row.prop(context.space_data, "grease_pencil_source", expand=True)

            row = box.row(1)
            row.prop_enum(context.gpencil_data, "draw_mode", 'VIEW')
            row.prop_enum(context.gpencil_data, "draw_mode", 'CURSOR')

            row = box.row(1)
            row.prop_enum(context.gpencil_data, "draw_mode", 'SURFACE')
            row.prop_enum(context.gpencil_data, "draw_mode", 'STROKE')

            row = box.row(1)
            row.active = context.gpencil_data.draw_mode in {'SURFACE', 'STROKE'}
            row.prop(context.gpencil_data, "use_stroke_endpoints")

            row = box.row(1)
            row.prop(context.active_gpencil_layer, "show_points", text="View Points", icon="PARTICLE_POINT")
            row.operator("gpencil.convert", text="Convert", icon="CURVE_BEZCURVE")

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
            row.prop(context.active_gpencil_layer, "color", text="")
            row.prop(context.active_gpencil_layer, "alpha", "Opac", slider=True)

            row = box.column(1)
            row.prop(context.active_gpencil_layer, "line_width", slider=True)

            row = box.column(1)
            row.alignment = 'CENTER'
            row.label(text="Fill")

            row = box.row(1)
            row.prop(context.active_gpencil_layer, "fill_color", text="")
            row.prop(context.active_gpencil_layer, "fill_alpha", "Opac", slider=True)

            row = box.column(1)
            row.prop(context.active_gpencil_layer, "use_onion_skinning")

        else:
            box = layout.box().column(1)

            row = box.row(1)
            if context.space_data.type == 'VIEW_3D':
                row.prop(context.tool_settings, "grease_pencil_source", expand=True)

            elif context.space_data.type == 'CLIP_EDITOR':
                row.prop(context.space_data, "grease_pencil_source", expand=True)

        box = layout.box().column(1)

        row = box.row(1)
        box.prop(context.user_preferences.edit, "grease_pencil_manhattan_distance", text="Manhattan Distance")
        box.prop(context.user_preferences.edit, "grease_pencil_euclidean_distance", text="Euclidean Distance")

        boxrow = box.row(1)
        boxrow.prop(context.user_preferences.edit, "use_grease_pencil_smooth_stroke", text="Smooth")
        boxrow.prop(context.user_preferences.edit, "use_grease_pencil_simplify_stroke", text="Simplify")

    box = layout.box().column(1)

    row = box.row(1)
    row.prop(context.object.data, "dimensions", expand=True)


# History

    box = layout.box()
    row = box.row(1)
    row.operator('wm.path_open', text='', icon='FILESEL').filepath = "C:\\Users\Public\Documents"
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
        del bpy.types.WindowManager.wkst_window_curve
    except:
        pass


if __name__ == "__main__":
    register()
