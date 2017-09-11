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
#    "name": "Workstation Lattice",
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


###########################################################################################################

class Dropdown_Wkst_Lattice_Props(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.wkst_window_lattice
    """
    display_lattice_selection = bpy.props.BoolProperty(name="Selection", description="Display Selection Tools", default=False)
    display_lattice_align = bpy.props.BoolProperty(name="Align", description="Display Align Tools", default=False)
    display_lattice_orient = bpy.props.BoolProperty(name="Origin & Snap to", description="Display Origin & Snap to Tools", default=False)
    display_lattice_shading = bpy.props.BoolProperty(name="Visualization", description="Display Visualization Tools", default=False)
    display_lattice_transform = bpy.props.BoolProperty(name="Transform", description="Display Selection Tools", default=False)
    display_lattice_view = bpy.props.BoolProperty(name="View", description="Display View Tools", default=False)

bpy.utils.register_class(Dropdown_Wkst_Lattice_Props)
bpy.types.WindowManager.wkst_window_lattice = bpy.props.PointerProperty(type=Dropdown_Wkst_Lattice_Props)

###########################################################################################################


def draw_wkst_lattice_ui(self, context, layout):

    lt = context.window_manager.wkst_window_lattice
    layout = self.layout.column_flow(1)
    obj = context.object


# Title

    box = layout.box()
    row = box.row(1)
    row.alignment = "CENTER"
    row.label("LATTICE DEFORM")


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


# View

    if lt. display_lattice_view:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_view", text="", icon='TRIA_DOWN')
        row.label("View...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_view", text="", icon='TRIA_RIGHT')
        row.label("View...")

        row.operator("view3d.view_all", "", icon="ZOOM_OUT")
        row.operator("view3d.view_selected", "", icon="ZOOM_IN")
        row.operator("view3d.zoom_border", "", icon="BORDERMOVE")

    if lt. display_lattice_view:

        box = layout.box().column(1)

        row = box.column(1)
        row.operator("view3d.view_all", "All", icon="ZOOM_OUT")
        row.operator("view3d.view_center_cursor", text="Cursor", icon="ZOOM_PREVIOUS")
        row.operator("view3d.view_selected", "Selected", icon="ZOOM_IN")
        row.operator("view3d.zoom_border", "Zoom Border", icon="BORDERMOVE")

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

    if lt. display_lattice_selection:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_selection", text="", icon='TRIA_DOWN')
        row.label("Selections...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_selection", text="", icon='TRIA_RIGHT')
        row.label("Selections...")

        row.operator("view3d.select_circle", text="", icon="BORDER_LASSO")
        row.operator("view3d.select_border", text="", icon="BORDER_RECT")

    if lt. display_lattice_selection:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("view3d.select_border", text="Border", icon="BORDER_RECT")
        row.operator("view3d.select_circle", text="Circle", icon="BORDER_LASSO")

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("lattice.select_mirror", text="Mirror")
        row.operator("lattice.select_random", text="Random")

        row = box.row(1)
        row.operator("lattice.select_all").action = 'TOGGLE'
        row.operator("lattice.select_all", text="Inverse").action = 'INVERT'

        row = box.row(1)
        row.operator("lattice.select_ungrouped", text="Ungrouped Verts")


# Origin

    if lt. display_lattice_orient:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_orient", text="", icon='TRIA_DOWN')
        row.label("Pivot...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_orient", text="", icon='TRIA_RIGHT')
        row.label("Pivot...")

        row.menu("origin.setupmenu_edm", "", icon="LAYER_ACTIVE")
        row.menu("wkst.snaptocursor", "", icon="FORCE_FORCE")
        row.menu("wkst.snaptoselect", "", icon="RESTRICT_SELECT_OFF")

    if lt. display_lattice_orient:

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

    if lt. display_lattice_transform:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_transform", text="", icon='TRIA_DOWN')
        row.label("Transform...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_transform", text="", icon='TRIA_RIGHT')
        row.label("Transform...")

        row.menu("VIEW3D_MT_mirror", "", icon="ARROW_LEFTRIGHT")
        row.menu("wkst.normal_transform_menu", "", icon="AXIS_SIDE")
        row.menu("wkst.transform_menu", "", icon="MANIPUL")

    if lt. display_lattice_transform:

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
        row.operator("lattice.flip", text="FlipX").axis = "U"
        row.operator("lattice.flip", text="FlipY").axis = "V"
        row.operator("lattice.flip", text="FlipZ").axis = "W"

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

    if lt. display_lattice_align:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_align", text="", icon='TRIA_DOWN')
        row.label("Align...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_align", text="", icon='TRIA_RIGHT')

        row.label("Align...")
        sub = row.row(1)
        sub.scale_x = 0.35
        sub.operator("mesh.face_align_x", "X", icon='TRIA_RIGHT')
        sub.operator("mesh.face_align_y", "Y", icon='TRIA_UP')
        sub.operator("mesh.face_align_z", "Z", icon='SPACE3')

    if lt. display_lattice_align:

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

    box = layout.box().column(1)

    row = box.row(1)
    row.operator("lattice.make_regular", "Make Regular", icon="LATTICE_DATA")


# Visual

    if lt. display_lattice_shading:

        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_shading", text="", icon='TRIA_DOWN')
        row.label("Visual...")

    else:
        box = layout.box()
        row = box.row(1)
        row.prop(lt, "display_lattice_shading", text="", icon='TRIA_RIGHT')
        row.label("Visual...")

        row.menu("wkst.display_menu", text="", icon="UI")
        row.menu("wkst.meshdisplay_menu", text="", icon="META_CUBE")
        row.operator("object.wire_all", text="", icon='WIRE')

    if lt. display_lattice_shading:

        box = layout.box().column(1)

        row = box.row(1)
        row.operator("wm.context_toggle", text="Xray", icon='META_CUBE').data_path = "object.show_x_ray"

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
        del bpy.types.WindowManager.wkst_window_lattice
    except:
        pass


if __name__ == "__main__":
    register()
