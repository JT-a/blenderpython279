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
#    "name": "Workstation Edit",
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


#####################################################################################################

class Dropdown_Wkst_Edit_Props(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.wkst_window_edit
    """

    ### Editmode ###
    display_edit_view = bpy.props.BoolProperty(name="View", description="View Tools", default=False)
    display_edit_editselect = bpy.props.BoolProperty(name="Selection", description="Display Selection Tools", default=False)
    display_edit_editpivot = bpy.props.BoolProperty(name="Pivot & Origin", description="Pivot & Origin Tools", default=False)
    display_edit_transform = bpy.props.BoolProperty(name="Transform Tools", description="Display Transform Tools", default=False)
    display_edit_vertalign = bpy.props.BoolProperty(name="Align", description="Display Vertex Align Tools", default=False)
    display_edit_bool = bpy.props.BoolProperty(name="Boolean, Join, Convert", description="Display Boolean, Join, Convert Tools", default=False)
    display_edit_miracurve = bpy.props.BoolProperty(name="Mira Edit Tools", description="Display Mira Edit Tools", default=False)
    display_edit_subdiv = bpy.props.BoolProperty(name="Subdivide", description="Display Subdivide & Cutting Tools", default=False)
    display_edit_extrude = bpy.props.BoolProperty(name="Extrude", description="Display Extrusion Tools", default=False)
    display_edit_vertedit = bpy.props.BoolProperty(name="Edit", description="Display Edit Tools", default=False)
    display_edit_miraedit = bpy.props.BoolProperty(name="Mira Edit Tools", description="Display Mira Edit Tools", default=False)
    display_edit_deform = bpy.props.BoolProperty(name="Deform", description="Display Deform Tools", default=False)
    display_edit_modif = bpy.props.BoolProperty(name="Modifier Tools", description="Display Modifier Tools", default=False)
    display_edit_mirrcut = bpy.props.BoolProperty(name="Auto Mirror Cut", description="Display Auto Mirror Cut Tools", default=False)
    display_edit_snapshot = bpy.props.BoolProperty(name="SnapShot Mesh", description="SnapShot Mesh Tools", default=False)
    display_edit_normal = bpy.props.BoolProperty(name="Normals", description="Display Face & Vertex Normal Tools", default=False)
    display_edit_shade = bpy.props.BoolProperty(name="Visual", description="Display Visualisation & Shading Tools", default=False)
    display_edit_check = bpy.props.BoolProperty(name="Mesh Check", description="Display Mesh Check Tools", default=False)
    display_edit_bsurf = bpy.props.BoolProperty(name="Bsurface", description="Display Bsurface Tools", default=False)
    display_edit_greaseset = bpy.props.BoolProperty(name="GP Settings", description="Display Grease Pencil Settings", default=False)


bpy.utils.register_class(Dropdown_Wkst_Edit_Props)
bpy.types.WindowManager.wkst_window_edit = bpy.props.PointerProperty(type=Dropdown_Wkst_Edit_Props)


#####################################################################################################


def draw_retopo_edit_ui(self, context, layout):
    lt = context.window_manager.wkst_window_edit

    obj = context.object
    scene = context.scene
    scn = context.scene
    rs = bpy.context.scene
    ob = context.object
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout = self.layout


# Title

    box = layout.box()
    row = box.row(1)
    row.alignment = "CENTER"
    row.label("MESH EDITING")


# Add

    box = layout.box().column_flow(1)
    row = box.row(1)
    row.alignment = 'CENTER'
    sub = row.row(1)
    sub.scale_x = 1.9
    sub.operator("mesh.primitive_plane_add", icon='MESH_PLANE', text="")
    sub.operator("mesh.primitive_cube_add", icon='MESH_CUBE', text="")
    sub.operator("mesh.primitive_circle_add", icon='MESH_CIRCLE', text="")
    sub.operator("mesh.primitive_uv_sphere_add", icon='MESH_UVSPHERE', text="")
    sub.operator("mesh.primitive_ico_sphere_add", icon='MESH_ICOSPHERE', text="")

    row = box.row(1)
    row.alignment = 'CENTER'
    sub = row.row(1)
    sub.scale_x = 1.9
    sub.operator("mesh.primitive_cylinder_add", icon='MESH_CYLINDER', text="")
    sub.operator("mesh.primitive_torus_add", icon='MESH_TORUS', text="")
    sub.operator("mesh.primitive_cone_add", icon='MESH_CONE', text="")
    sub.operator("mesh.primitive_grid_add", icon='MESH_GRID', text="")
    sub.operator("mesh.primitive_monkey_add", icon='MESH_MONKEY', text="")

    row = box.row(1)
    row.alignment = 'CENTER'
    row.scale_x = 1
    row.operator("mesh.add_curvebased_tube", text="", icon="CURVE_DATA")
    row.operator("mesh.autotubes", text="", icon="OUTLINER_DATA_EMPTY")
    row.operator("mesh.singleplane_x", text="X")
    row.operator("mesh.singleplane_y", text="Y")
    row.operator("mesh.singleplane_z", text="Z")
    row.operator("object.easy_lattice", text="", icon="OUTLINER_DATA_LATTICE")
    row.operator("mesh.singlevertex", text="", icon="STICKY_UVS_DISABLE")


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
    row.menu("mesh.cleandelete", text="", icon="PANEL_CLOSE")


# View

    if lt.display_edit_view:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_view", text="", icon='TRIA_DOWN')
        row.label("3d-View...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_view", text="", icon='TRIA_RIGHT')
        row.label("3d-View...")

        row.operator("view3d.view_all", "", icon="ZOOM_OUT")
        row.operator("view3d.view_selected", "", icon="ZOOM_IN")
        row.operator("view3d.zoom_border", "", icon="BORDERMOVE")

    if lt.display_edit_view:

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

    if lt.display_edit_editselect:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_editselect", text="", icon='TRIA_DOWN')
        row.label("Select...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_editselect", text="", icon='TRIA_RIGHT')
        row.label("Select...")

        row.menu("VIEW3D_MT_edit_mesh_showhide", "", icon="VISIBLE_IPO_ON")
        row.menu("VIEW3D_MT_edit_multi", text="", icon="UV_SYNC_SELECT")
        row.operator("view3d.select_border", text="", icon="BORDER_RECT")
        row.operator("view3d.select_circle", text="", icon="BORDER_LASSO")

    if lt.display_edit_editselect:

        #box = layout.box().column(1)

        #row = box.row(1)
        #layout.operator_context = 'INVOKE_REGION_WIN'
        #row.operator("mesh.select_mode", text="Vert", icon='VERTEXSEL').type = 'VERT'
        #row.operator("mesh.select_mode", text="Edge", icon='EDGESEL').type = 'EDGE'
        #row.operator("mesh.select_mode", text="Face", icon='FACESEL').type = 'FACE'

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("view3d.select_border", text="Border", icon="BORDER_RECT")
        row.operator("view3d.select_circle", text="Circle", icon="BORDER_LASSO")

        row = box.row(1)
        row.menu("VIEW3D_MT_edit_mesh_showhide", "Hide/Show", icon="VISIBLE_IPO_ON")
        row.menu("VIEW3D_MT_edit_multi", text="Mesh Select", icon="UV_SYNC_SELECT")

        box = layout.box().column(1)

        row = box.row(1)
        sub = row.row()
        sub.scale_x = 0.3
        sub.operator("mesh.select_more", text="+")
        sub.operator("mesh.select_all", text="All")
        sub.operator("mesh.select_less", text="-")

        row = box.row(1)
        row.operator("mesh.select_similar", text="Similar")
        row.operator("mesh.select_similar_region", text="Face Regions")

        row = box.row(1)
        row.operator("mesh.select_mirror", text="Mirror")
        row.operator("mesh.select_all", text="Inverse").action = 'INVERT'

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mesh.loop_multi_select", text="Edge Loops").ring = False
        row.operator("mesh.loop_multi_select", text="Edge Rings").ring = True

        row = box.row(1)
        row.operator("mesh.grow_loop", "Grow")
        row.operator("mesh.shrink_loop", "Shrink")

        row = box.row(1)
        row.operator("mesh.path_select_ring", "RingPath")
        row.operator("mesh.extend_loop", "Extend")

        row = box.row(1)
        row.operator("mesh.region_to_loop", "Inner-Loops")
        row.operator("mesh.loop_to_region", "Boundary-Loop")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mesh.faces_select_linked_flat", text="Linked Faces")
        row.operator("mesh.select_nth", "Checker")

        row = box.row(1)
        row.operator("mesh.select_loose", text="Loose")
        row.operator("mesh.select_linked", text="Linked")

        row = box.row(1)
        row.operator("mesh.select_axis", text="ActiveSide")
        row.operator("mesh.select_face_by_sides", text="NSide")

        row = box.row(1)
        row.operator("mesh.edges_select_sharp", text="Sharp")
        row.operator("mesh.shortest_path_select", text="Shortest")

        row = box.row(1)
        row.operator("mesh.select_ungrouped", text="Ungrouped Verts")
        row.operator("mesh.select_random", text="Random")

        box = layout.box().column(1)

        row = box.row(1)
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

        row = box.row(1)
        row.operator("data.facetype_select", text="Ngons").face_type = "5"
        row.operator("data.facetype_select", text="Quads").face_type = "4"
        row.operator("data.facetype_select", text="Tris").face_type = "3"

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.mst_sort_mesh_elements", text="MST Sort Mesh Elements")

        row = box.row(1)
        row.operator("addongen.mesh_order_research_operator", text="VertCycl").type = "Vertices"
        row.operator("addongen.mesh_order_research_operator", text="EdgeCycl").type = "Edges"
        row.operator("addongen.mesh_order_research_operator", text="PolyCycl").type = "Polygons"

        box = layout.box().column(1)

        row = box.row(1)
        if context.scene.tool_settings.mesh_select_mode[2] is False:
            row.operator("mesh.select_non_manifold", text="Non Manifold")
        row.operator("mesh.select_interior_faces", text="Interior Faces")

        row = box.row(1)
        row.operator("meshlint.select", "Meshlint > go Object Data")


# Origin

    if lt.display_edit_editpivot:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_editpivot", text="", icon='TRIA_DOWN')
        row.label("Pivot...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_editpivot", text="", icon='TRIA_RIGHT')
        row.label("Pivot...")

        row.menu("origin.setupmenu_edm", "", icon="LAYER_ACTIVE")
        row.menu("wkst.snaptocursor", "", icon="FORCE_FORCE")
        row.menu("wkst.snaptoselect", "", icon="RESTRICT_SELECT_OFF")

    if lt.display_edit_editpivot:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("origin.selected_edm", "Origin Edit", icon="EDITMODE_HLT")
        row.operator("origin.selected_obm", "Origin Object", icon="OBJECT_DATAMODE")

        box = layout.box().column(1)

        row = box.row(1)
        row.menu("wkst.snaptocursor", " > Cursor to... ", icon="FORCE_FORCE")

        row = box.row(1)
        row.menu("wkst.snaptoselect", " > Selection to... ", icon="RESTRICT_SELECT_OFF")


# Transform

    if lt.display_edit_transform:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_transform", text="", icon='TRIA_DOWN')
        row.label("Transform...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_transform", text="", icon='TRIA_RIGHT')
        row.label("Transform...")

        row.menu("wkst.transform_menu", "", icon="MANIPUL")
        row.menu("wkst.normal_transform_menu", "", icon="AXIS_SIDE")
        row.menu("VIEW3D_MT_mirror", "", icon="ARROW_LEFTRIGHT")

        #row.operator("mesh.snap_utilities_rotate", text = "", icon="NDOF_TURN")
        #row.operator("mesh.snap_utilities_move", text = "", icon="NDOF_TRANS")

    if lt.display_edit_transform:
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
        row.operator("transform.shrink_fatten", text="Shrink/Fatten")
        row.operator("transform.tosphere", "to Sphere")

        row = box.row(1)
        row.operator("transform.shear", text="Shear")
        row.operator("transform.bend", text="Bend")

        row = box.row(1)
        row.operator("transform.vertex_random", text="Randomize")
        row.operator("transform.vertex_warp", text="Warp")

        row = box.row(1)
        row.operator('mesh.rot_con', 'Face-Rotation-Constraine')

        box = layout.box().column(1)

        row = box.row(1)
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

    if lt.display_edit_vertalign:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_vertalign", text="", icon='TRIA_DOWN')
        row.label("Align...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_vertalign", text="", icon='TRIA_RIGHT')
        row.label("Align...")
        sub = row.row(1)
        sub.scale_x = 0.35
        sub.operator("mesh.face_align_x", "X", icon='TRIA_RIGHT')
        sub.operator("mesh.face_align_y", "Y", icon='TRIA_UP')
        sub.operator("mesh.face_align_z", "Z", icon='SPACE3')

    if lt.display_edit_vertalign:

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


# Sculpt

    if lt.display_edit_bool:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_bool", text="", icon='TRIA_DOWN')
        row.label("Sculpt...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_bool", text="", icon='TRIA_RIGHT')
        row.label("Sculpt...")

        row.menu("draw.gpencil_menu", "", icon='SCULPTMODE_HLT')
        row.menu("object.boolean_menu", "", icon='FULLSCREEN_EXIT')

    if lt.display_edit_bool:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("sculpt.remesh", text='Remesh', icon='MOD_REMESH')
        row.prop(context.window_manager, 'remeshPreserveShape', text="Preserve Shape")

        row = box.row(1)
        row.prop(context.window_manager, 'remeshDepthInt', text="Depth")
        row.prop(context.window_manager, 'remeshSubdivisions', text="Subdivisions")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mesh.intersect", "Intersect", icon='ZOOMIN')
        row.operator("mesh.intersect", "Intersect", icon='ZOOMOUT')

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("mesh.looptools_gstretch", "Gstretch Project", icon='SPHERECURVE')
        row.operator("boolean.purge_pencils", text='Purge Grease', icon='PANEL_CLOSE')

        row = box.row(1)
#        row.prop(context.tool_settings, "use_grease_pencil_sessions", text=" ", icon="LOCKED")
        row.operator("gpencil.draw", text=" ", icon="DISCLOSURE_TRI_DOWN").mode = 'ERASER'
        row.operator("gpencil.draw", text=" ", icon="NOCURVE").mode = 'DRAW_POLY'
        row.operator("gpencil.draw", text=" ", icon="BRUSH_DATA").mode = 'DRAW'
        row.operator("gpencil.draw", text=" ", icon="GREASEPENCIL").mode = 'DRAW_STRAIGHT'

        row = box.row(1)
        if context.space_data.type == 'VIEW_3D':
            row.prop(context.tool_settings, "grease_pencil_source", expand=True)

        elif context.space_data.type == 'CLIP_EDITOR':
            row.prop(context.space_data, "grease_pencil_source", expand=True)

        box = layout.box().column(1)

        row = box.row(1)
        box.prop(context.user_preferences.edit, "grease_pencil_manhattan_distance", text="Manhattan Distance")
        box.prop(context.user_preferences.edit, "grease_pencil_euclidean_distance", text="Euclidean Distance")



# MiraTools

    if lt.display_edit_miracurve:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_miracurve", text="", icon='TRIA_DOWN')
        row.label("MCurve...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_miracurve", text="", icon='TRIA_RIGHT')

        row.label("MCurve...")

        row.prop(context.scene.mi_settings, "surface_snap", text='', icon="SNAP_SURFACE")
        row.menu("wkst.miraextrude_menu", text="", icon="MESH_GRID")
        row.menu("wkst.miracurve_menu", text="", icon="STYLUS_PRESSURE")

    if lt.display_edit_miracurve:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mira.poly_loop", text="Poly Loop", icon="MESH_GRID")
        row.prop(context.scene.mi_settings, "surface_snap", text='', icon="SNAP_SURFACE")
        row = box.row(1)
        row.operator("mesh.retopomt", text="Retopo MT", icon="ORTHO")

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("mira.curve_stretch", text="CurveStretch", icon="STYLUS_PRESSURE")
        row.prop(context.scene.mi_cur_stretch_settings, "points_number", text='PointsNumber')

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("mira.curve_guide", text="CurveGuide", icon="RNA")
        row.prop(context.scene.mi_curguide_settings, "points_number", text='LoopSpread')

        row = box.column(1)
        row.prop(context.scene.mi_curguide_settings, "deform_type", text='Deform')

        col = layout.column(1)
        box = col.column(1).box().column()
        box = box.column(1)

        row = box.column(1)
        row.operator("mira.curve_surfaces", text="CurveSurfaces", icon="SURFACE_NCURVE")
        row.prop(context.scene.mi_cur_surfs_settings, "spread_loops_type", text='Points')

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("mira.draw_extrude", text="Draw Extrude", icon="FORCE_MAGNETIC")

        row = box.column(1)
        row.prop(context.scene.mi_extrude_settings, "extrude_step_type", text='Step')

        if context.scene.mi_extrude_settings.extrude_step_type == 'Asolute':
            row.prop(context.scene.mi_extrude_settings, "absolute_extrude_step", text='')
        else:
            row.prop(context.scene.mi_extrude_settings, "relative_extrude_step", text='')

        row = box.column(1)
        if context.scene.mi_settings.surface_snap is False:
            row.prop(context.scene.mi_extrude_settings, "do_symmetry", text='Symmetry')

            if context.scene.mi_extrude_settings.do_symmetry:
                row.prop(context.scene.mi_extrude_settings, "symmetry_axys", text='Axys')

        box = layout.box().column(1)

        row = box.row(1)
        row.label("Curve Snap Settings")

        row = box.column(1)
        row.prop(context.scene.mi_settings, "surface_snap", text='SurfaceSnapping')
        row.prop(context.scene.mi_settings, "convert_instances", text='ConvertInstances')
        row.prop(context.scene.mi_settings, "snap_objects", text='SnapObjects')

        box = layout.box().column(1)

        row = box.row(1)
        row.label("Curve Settings")

        row = box.column(1)
        row.prop(context.scene.mi_settings, "spread_mode", text='Spread')
        row.prop(context.scene.mi_settings, "curve_resolution", text='Resolution')

        row = box.row(1)
        row.prop(context.scene.mi_settings, "draw_handlers", text='Handlers')
        row.operator("mira.curve_test", text="Curve Test")


# Divide

    if lt.display_edit_subdiv:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_subdiv", text="", icon='TRIA_DOWN')
        row.label("Subdivide...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_subdiv", text="", icon='TRIA_RIGHT')
        row.label("Subdivide...")

        row.menu("wkst.subdivide_menu", text="", icon="MESH_ICOSPHERE")
        row.menu("wkst.cutting_menu", "", icon="LINE_DATA")

    if lt.display_edit_subdiv:

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Subdivide")

        row = box.row(1)
        row.operator("mesh.subdivide", text="1").number_cuts = 1
        row.operator("mesh.subdivide", text="2").number_cuts = 2
        row.operator("mesh.subdivide", text="3").number_cuts = 3
        row.operator("mesh.subdivide", text="4").number_cuts = 4
        row.operator("mesh.subdivide", text="5").number_cuts = 5
        row.operator("mesh.subdivide", text="6").number_cuts = 6

        row = box.row(1)
        row.operator("mesh.tris_convert_to_quads", text="Quads", icon="MOD_LATTICE")
        row.operator("mesh.unsubdivide", text="(Un-)Subdivide")
        row.operator("screen.redo_last", text="", icon="SCRIPTWIN")
        row.operator("mesh.quads_convert_to_tris", text="Tris", icon="MOD_TRIANGULATE")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Cutting")

        row = box.row(1)
        row.operator("mesh.snap_utilities_line", "SnapLine", icon="LINE_DATA")
        row.operator("mesh.bisect", icon="SCULPTMODE_HLT")

        row = box.row(1)
        props = row.operator("mesh.knife_tool", text="Knife", icon="LINE_DATA")
        props.use_occlude_geometry = True
        props.only_selected = False

        row.operator("object_ot.fastloop", icon="GRIP")

        row = box.row(1)

        props = row.operator("mesh.knife_tool", text="Knife Select", icon="LINE_DATA")
        props.use_occlude_geometry = False
        props.only_selected = True

        row.operator("mesh.loopcut_slide", "Loop Cut", icon="COLLAPSEMENU")

        row = box.row(1)
        row.operator("mesh.knife_project", icon="LINE_DATA")
        row.operator("mesh.ext_cut_faces", text="Face Cut", icon="SNAP_EDGE")

        row = box.row(1)
        row.operator("object.createhole", text="Face Hole", icon="RADIOBUT_OFF")
        row.operator("mesh.build_corner", icon="OUTLINER_DATA_MESH")


# Extrude

    if lt.display_edit_extrude:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_extrude", text="", icon='TRIA_DOWN')
        row.label("Extrude...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_extrude", text="", icon='TRIA_RIGHT')
        row.label("Extrude...")

        row.menu("wkst.extrude_offset_menu", text="", icon="SNAP_PEEL_OBJECT")
        row.menu("wkst.extrude_menu", text="", icon="SNAP_FACE")

    if lt.display_edit_extrude:

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Fill")

        row = box.row(1)
        row.operator("mesh.edge_face_add", "Edge/Face")
        row.operator("mesh.fill", text="Fill")

        row = box.row(1)
        row.operator("mesh.beautify_fill", text="Beautify")
        row.operator("mesh.fill_grid", "Grid Fill")

        row = box.row(1)
        row.operator("mesh.poke", text="Poke")
        row.operator("mesh.close_faces", "Close Faces")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Inset")

        row = box.row(1)
        row.operator('faceinfillet.op0_id', text='Face Fillet')
        row.operator("fillet.op0_id", text="Edge Fillet")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Extrude")

        row = box.row(1)
        row.operator("view3d.edit_mesh_extrude_move_normal", text="Region")
        row.operator("mesh.push_pull_face", "Push/Pull")

        row = box.row(1)
        row.operator("view3d.edit_mesh_extrude_individual_move", text="Individual")
        row.operator("mesh.draw_poly")

        row = box.row(1)
        row.operator('object.mextrude', text='Multi')
        row.operator_menu_enum('mesh.offset_edges', 'geometry_mode')

        row = box.row(1)
        row.operator("mesh.spin")
        row.operator("mesh.screw")

        row = box.row(1)
        row.operator("mesh.solidify", text="Solidify")
        row.operator("mesh.wireframe", text="Wire")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mesh.extrude_along_curve", text="Along Curve", icon="BLANK1")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("BBox Mirror Extrude")

        row = box.row(1)
        row.operator("bbox.circle_div", text="EvenDiv")
        row.operator("mesh.subdivide", text="< OddDiv").number_cuts = 1

        row = box.row(1)
        row.operator("bbox.mirror_extrude_x", "X")
        row.operator("bbox.mirror_extrude_y", "Y")
        row.operator("bbox.mirror_extrude_z", "Z")
        row.operator("bbox.mirror_extrude_n", "N")


# Tools

    if lt.display_edit_vertedit:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_vertedit", text="", icon='TRIA_DOWN')
        row.label("Edit...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_vertedit", text="", icon='TRIA_RIGHT')
        row.label("Edit...")

        row.menu("wkst.connect_menu", text="", icon="SOUND")
        row.menu("wkst.vertex_arrange_menu", text="", icon="PARTICLE_POINT")
        row.operator_menu_enum("mesh.merge", "type", "", icon="AUTOMERGE_ON")

    if lt.display_edit_vertedit:

        box = layout.box().column(1)

        row = box.row(1)
        row.menu("VIEW3D_MT_edit_mesh_delete")
        row.operator("mesh.remove_doubles")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mesh.duplicate_move", "Duplicate", icon="MOD_DISPLACE")

        row = box.row(1)
        row.operator("mesh.split", icon="MOD_BOOLEAN")
        row.operator("mesh.separate", text="Separate", icon="ORTHO")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Connect", icon="SOUND")

        row = box.row(1)
        row.operator("mesh.vert_connect", "Vert Connect", icon="OUTLINER_DATA_MESH")
        row.operator("mesh.vert_connect_path", "Vert Path", icon="STICKY_UVS_DISABLE")

        row = box.row(1)
        row.operator("mesh.bridge_edge_loops", "Bridge Edges", icon="SOUND")
        row.operator("mesh.edge_face_add", "Edge / Face", icon="LOOPSEL")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Arrange")

        row = box.row(1)
        row.operator("mesh.vertex_align", text="Align", icon="ALIGN")
        row.operator("mesh.vertex_distribute", text="Distribute", icon="PARTICLE_POINT")

        row = box.row(1)
        row.operator("transform.edge_slide", text="Slide Edge", icon="DISCLOSURE_TRI_RIGHT")
        row.operator("transform.vert_slide", text="Slide Vertex", icon="DISCLOSURE_TRI_RIGHT")

        row = box.row(1)
        row.operator("mesh.vertices_smooth_laplacian", "Laplacian", icon="ROOTCURVE")
        row.operator("mesh.vertices_smooth", "Smooth", icon="SPHERECURVE")

        row = box.row(1)
        row.operator("mesh.shrinkwrap_smooth", icon="BLANK1")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Merge", icon="AUTOMERGE_ON")

        row = box.row(1)
        row.operator_menu_enum("mesh.merge", "type")
        row.operator("mesh.merge", "Merge Center").type = 'CENTER'

        row = box.row(1)
        row.operator("mesh.path_select_ring", "RingPath")
        row.operator("mesh.path_collapse_select_ring")

        box = layout.box().column(1)

        row = box.row(1)
        Automerge = context.tool_settings
        row.prop(Automerge, "use_mesh_automerge", text="Auto Merge")

        row = box.row(1)
        row.operator("double.threshold01", text="TSHD 0.1")
        row.operator("double.threshold0001", text="TSHD 0.001")

        row = box.row(1)
        row.label("Double Threshold:")

        row = box.row(1)
        row.prop(context.tool_settings, "double_threshold", text="")


# CadStyle

    if lt.display_edit_miraedit:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_miraedit", text="", icon='TRIA_DOWN')
        row.label("CadStyle...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_miraedit", text="", icon='TRIA_RIGHT')
        row.label("CAD...")

        row.operator("mesh.edge_roundifier", "", icon="OUTLINER_DATA_CURVE")
        row.menu("VIEW3D_MT_edit_mesh_tinycad", "", icon="GRID")
        row.menu("VIEW3D_MT_edit_mesh_looptools", "", icon="SORTALPHA")

    if lt.display_edit_miraedit:

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("LoopTools")

        row = box.row(1)
        row.operator("mesh.looptools_circle")
        row.operator("mesh.looptools_relax")

        row = box.row(1)
        row.operator("mesh.looptools_bridge", text="Bridge").loft = False
        row.operator("mesh.looptools_flatten")

        row = box.row(1)
        row.operator("mesh.looptools_bridge", text="Loft").loft = True
        row.operator("mesh.looptools_space")

        row = box.row(1)
        row.operator("mesh.looptools_gstretch")
        row.operator("mesh.looptools_curve")

        box = layout.box().column(1)

#        row = box.row(1)
#        row.alignment = 'CENTER'
#        row.label("TinyCAD Tools")

#        row = box.row(1)
#        row.operator("view3d.autovtx", text="Auto-VTX")
#        row.operator("mesh.circlecenter", text="Circle Center")

#        row = box.row(1)
#        row.operator("mesh.vertintersect", text="V2X")
#        row.operator("mesh.intersectall", text="X-All")

#        row = box.row(1)
#        row.operator("mesh.linetobisect", text="BIX")
#        row.operator("mesh.cutonperp", text="PERP CUT")

#        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mesh.edge_roundifier", icon="OUTLINER_DATA_CURVE")


# Deform----

    if lt.display_edit_deform:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_deform", text="", icon='TRIA_DOWN')
        row.label("Deform...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_deform", text="", icon='TRIA_RIGHT')
        row.label("Deform...")

        row.menu("wkst_menu.vertex_group", text="", icon="GROUP_VERTEX")
        row.menu("wkst.miradeform_menu", text="", icon="OUTLINER_OB_MESH")
        row.operator("object.easy_lattice", text="", icon="MOD_LATTICE")

    if lt.display_edit_deform:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.easy_lattice", text="Create Easy Lattice", icon="OUTLINER_DATA_LATTICE")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mira.linear_deformer", text="LinearDeformer", icon="OUTLINER_OB_MESH")

        row = box.row(1)
        row.prop(context.scene.mi_ldeformer_settings, "manual_update", text='ManualUpdate')

        row = box.row(1)
        row.operator("mira.noise", text="NoiseDeform")
        row.operator("mira.deformer", text="Deformer")

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

            row = box.row(1)
            row.menu("MESH_MT_vertex_group_specials", icon='TRIA_RIGHT', text="Specials")
            row.prop(context.tool_settings, "vertex_group_weight", text="Weight")


# Modifier

    if lt.display_edit_modif:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_modif", text="", icon='TRIA_DOWN')
        row.label("Modifier...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_modif", text="", icon='TRIA_RIGHT')

        row.label("Modifier...")

        row.menu("wkst.modispace", "", icon='MODIFIER')
        row.menu("modifiers.viewport_edm", "", icon='RESTRICT_VIEW_OFF')
        row.operator("view3d.display_modifiers_delete", "", icon='X')
        row.operator("view3d.display_modifiers_apply_edm", "", icon='FILE_TICK')

    if lt.display_edit_modif:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator_menu_enum("object.modifier_add", "type", icon='MODIFIER')

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("view3d.display_modifiers_viewport_off", "Off", icon='VISIBLE_IPO_OFF')
        row.operator("view3d.display_modifiers_viewport_on", "On ", icon='RESTRICT_VIEW_OFF')

        row = box.row(1)
        row.operator("view3d.display_modifiers_edit_off", icon='SNAP_VERTEX')
        row.operator("view3d.display_modifiers_edit_on", icon='EDITMODE_HLT')

        row = box.row(1)
        row.operator("view3d.display_modifiers_cage_off", icon='OUTLINER_DATA_MESH')
        row.operator("view3d.display_modifiers_cage_on", icon='OUTLINER_OB_MESH')

        row = box.row(1)
        row.operator("view3d.display_modifiers_delete", "Delete", icon='X')
        row.operator("view3d.display_modifiers_apply_edm", "Apply", icon='FILE_TICK')

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


# MirrorCut

    if lt.display_edit_mirrcut:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_mirrcut", text="", icon='TRIA_DOWN')
        row.label("MirrorCut...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_mirrcut", text="", icon='TRIA_RIGHT')
        row.label("MirrorCut...")

        sub = row.row(1)
        sub.scale_x = 0.3
        sub.prop(context.scene, "AutoMirror_orientation", text="")
        sub.prop(context.scene, "AutoMirror_axis", text="")
        row.menu("wkst.mirrorcut", text="", icon="MOD_WIREFRAME")

    if lt.display_edit_mirrcut:
        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.automirror", text="Execute AutoMirror", icon="MOD_WIREFRAME")

        row = box.row(1)
        row.prop(context.scene, "AutoMirror_orientation", text="")
        row.prop(context.scene, "AutoMirror_axis", text="")

        row = box.row(1)
        row.prop(context.scene, "AutoMirror_threshold", text="Threshold")

        box = box.column(1)
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
        row.alignment = 'CENTER'
        row.label("Mesh Delete")

        row = box.row(1)
        row.operator("modifier.positiv_x_cut", text="+X")
        row.operator("modifier.positiv_y_cut", text="+Y")
        row.operator("modifier.positiv_z_cut", text="+Z")

        row = box.row(1)
        row.operator("modifier.negativ_x_cut", text="-X")
        row.operator("modifier.negativ_y_cut", text="-Y")
        row.operator("modifier.negativ_z_cut", text="-Z")


# Snapshot

    if lt.display_edit_snapshot:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_snapshot", text="", icon='TRIA_DOWN')
        row.label("SnapShot...")

    else:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_snapshot", text="", icon='TRIA_RIGHT')
        row.label("SnapShot...")

        row.operator("vtools.usesnapshot", icon='RECOVER_LAST', text="")
        row.operator("vtools.deletesnapshot", icon='DISCLOSURE_TRI_DOWN', text="")
        row.operator("vtools.capturesnapshot", icon='DISCLOSURE_TRI_RIGHT', text="")

    if lt.display_edit_snapshot:

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


# Normals

    if lt.display_edit_normal:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_normal", text="", icon='TRIA_DOWN')
        row.label("Normals...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_normal", text="", icon='TRIA_RIGHT')
        row.label("Normals...")

        row.menu("wkst.normal_menu", text="", icon='AUTO')
        row.menu("wkst.normals_menu", text="", icon='SNAP_NORMAL')

    if lt.display_edit_normal:
        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mesh.normals_make_consistent", text="Recalculate", icon='SNAP_NORMAL')
        row.operator("mesh.flip_normals", text="Flip", icon="FILE_REFRESH")

        row = box.row(1)
        row.operator("mesh.normals_make_consistent", text="Rec-Inside").inside = True
        row.operator("mesh.normals_make_consistent", text="Rec-Outside").inside = False

        row = box.row(1)
        row.prop(context.active_object.data, "show_normal_vertex", text="", icon='VERTEXSEL')
        row.prop(context.active_object.data, "show_normal_loop", text="", icon='LOOPSEL')
        row.prop(context.active_object.data, "show_normal_face", text="", icon='FACESEL')

        row.active = context.active_object.data.show_normal_vertex or context.active_object.data.show_normal_face
        row.prop(context.scene.tool_settings, "normal_size", text="Size")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.editnormals_transfer", icon='SNAP_NORMAL')


# MeshCheck

    if lt.display_edit_check:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_check", text="", icon='TRIA_DOWN')
        row.label("Check...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_check", text="", icon='TRIA_RIGHT')

        row.label("Check...")

        if context.mode == 'OBJECT':
            row.operator("view3d.rec_normals", "", icon="SNAP_NORMAL")

        row.menu("wkst.modifly", '', icon="MOD_SOFT")

        if not context.mode == 'SCULPT':
            row.menu("wkst.material_menu", text="", icon='MATERIAL_DATA')
            row.menu("wkst.meshcheck_menu", text="", icon='GROUP_VCOL')

    if lt.display_edit_check:
        view = context.space_data
        obj = context.object

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("object.add_materials", text="Display color", icon='GROUP_VCOL')
        row.operator("object.remove_materials", text="Hidde color", icon='X')

        box = layout.box().column(1)

        row = box.row(1)
        row.prop(context.window_manager.border_lines, "borderlines_use")
        row.prop(context.window_manager.border_lines, "borderlines_width")

        row = box.row(1)
        row.prop(context.window_manager.border_lines, "custom_color_use", text="Border Color")
        row.prop(context.window_manager.border_lines, "custom_color", text="")

        box = layout.box().column(1)

        row = box.row(1)
        row.alignment = 'CENTER'
        row.label("Flymode for HighRes", icon='MOD_SOFT')

        row = box.row(1)
        row.operator("view3d.fast_navigate_operator", 'Start', icon="PLAY")
        row.operator("view3d.fast_navigate_stop_new", 'Stop', icon="PAUSE")


# Visuals

    if lt.display_edit_shade:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_shade", text="", icon='TRIA_DOWN')
        row.label("Visual...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_shade", text="", icon='TRIA_RIGHT')
        row.label("Visual...")

#        row.menu("wkst.display_edit_menu", text="", icon="UI")
        row.menu("wkst.meshdisplay_menu", text="", icon="META_CUBE")
        row.menu("wkst.shade_menu", text="", icon="SMOOTH")
        row.operator("object.wire_all", text="", icon='WIRE')

    if lt.display_edit_shade:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("mesh.faces_shade_smooth", text="Smooth", icon="SMOOTH")
        row.operator("mesh.faces_shade_flat", text="Flat", icon="MESH_CIRCLE")

        row = box.row(1)
        row.prop(context.active_object.data, "show_double_sided", icon="GHOST")
        row.prop(context.active_object.data, "use_auto_smooth", icon="AUTO")

        row = box.row(1)
        row.active = context.active_object.data.use_auto_smooth
        row.prop(context.active_object.data, "auto_smooth_angle", text="Angle")

        box = layout.box().column(1)

        row = box.row(1)
        row.label(text="Mark Sharp: Edges")

        row = box.row(1)
        row.operator("mesh.mark_sharp", text="Clear").clear = True
        row.operator("mesh.mark_sharp", text="Sharp")

        row = box.row(1)
        row.label(text="Mark Sharp: Vertices")

        row = box.row(1)
        props = row.operator("mesh.mark_sharp", text="Clear")
        props.use_verts = True
        props.clear = True
        row.operator("mesh.mark_sharp", text="Sharp").use_verts = True

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("object.wire_all", text="Wire all", icon='WIRE')

        box = layout.box().column(1)

        row = box.row(1)
        row.prop(context.space_data, "use_occlude_geometry", text="Limit 2 Visible", icon='ORTHO')
        row.prop(context.object, "show_x_ray", text="X-Ray", icon="META_CUBE")

        row = box.row(1)
        row.prop(context.space_data, "show_backface_culling", text="Backface", icon="OUTLINER_OB_LATTICE")
        row.prop(context.space_data, "show_occlude_wire", text="Hidden", icon="OUTLINER_DATA_LATTICE")

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


# Besurface

    if lt.display_edit_bsurf:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_bsurf", text="", icon='TRIA_DOWN')
        row.label("Bsurfaces...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_edit_bsurf", text="", icon='TRIA_RIGHT')
        row.label("Bsurfaces...")

        row.menu("wkst_menu.bsurfaces", text="", icon='MOD_DYNAMICPAINT')

    if lt.display_edit_bsurf:

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("gpencil.surfsk_add_surface", text="Add Surface", icon='MOD_DYNAMICPAINT')
        row.operator("gpencil.surfsk_edit_strokes", text="Edit Strokes", icon='MOD_DYNAMICPAINT')
        row.prop(scn, "SURFSK_cyclic_cross")
        row.prop(scn, "SURFSK_cyclic_follow")
        row.prop(scn, "SURFSK_loops_on_strokes")
        row.prop(scn, "SURFSK_automatic_join")
        row.prop(scn, "SURFSK_keep_strokes")


# Registry

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
        del bpy.types.WindowManager.wkst_window_edit
    except:
        pass


if __name__ == "__main__":
    register()
