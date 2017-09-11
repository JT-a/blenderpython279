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
    "name": "SFC Retopo",
    "description": "A collection of tools for modeling and retopology",
    "location": "3D View > Tool Shelf > SFC Retopo",
    "author": "SFC & UI: Brett Fedack / Multi Addon-Authors (see bl_infos) / SFC-Retopo_Collection & UI: Marvin.K.Breuer",
    "version": (1, 1),
    "blender": (2, 76, 0),
    "category": "Sculpting"
}


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sfc_workstation'))

if "bpy" in locals():
    import imp

    imp.reload(MeshBrush)
    imp.reload(PickSurfaceConstraint)
    imp.reload(Shrinkwrap)
    imp.reload(SmoothVertices)
    imp.reload(ResizeMeshBrush)
    imp.reload(StrokeMove)
    imp.reload(StrokeSmooth)
    imp.reload(SurfaceConstraintToolsPrefs)
    imp.reload(SurfaceConstraintToolsPanel)

    imp.reload(add_simple_curve)
    imp.reload(add_tubetool)

    imp.reload(copy_attributes)
    imp.reload(copy_mifth_cloning)
    imp.reload(copy_replicator)
    imp.reload(copy_toall)

    imp.reload(curve_action)
    imp.reload(curve_outline)
    imp.reload(curve_split)
    imp.reload(curve_beveltaper)

    imp.reload(delete_clear_all_transform)
    imp.reload(delete_orphan_slayer)

    imp.reload(edit_boolean)
    imp.reload(edit_edge_fillet)
    imp.reload(edit_edge_roundifier)
    imp.reload(edit_edger)
    imp.reload(edit_extrude_along_curve)
    imp.reload(edit_face_inset_fillet)
    imp.reload(edit_faces_along_normals)
    imp.reload(edit_fast_loop)
    imp.reload(edit_ktools)
    imp.reload(edit_mesh_bsurfaces)
    imp.reload(edit_mesh_cut_faces)
    imp.reload(edit_mesh_looptools)
    imp.reload(edit_mesh_mextrude_plus)
    imp.reload(edit_mesh_sorting_tools)
    imp.reload(edit_mesh_vertex_tools)
    imp.reload(edit_meshlint)
    imp.reload(edit_multiedit)
    imp.reload(edit_offset_edges)
    imp.reload(edit_pushpull)
    imp.reload(edit_retopo_mt)
    imp.reload(edit_rotation_constrained)
    imp.reload(edit_snap_utilities)
    imp.reload(edit_snaps_shot)
    imp.reload(edit_transfer_normals)
    imp.reload(edit_tri_faces)

    imp.reload(group_sgrouper)

    imp.reload(io_auto_backgrounds)
    imp.reload(io_export_selected)

    imp.reload(mat_material_utils)

    imp.reload(modifier_automirror)
    imp.reload(modifier_easylattice)
    imp.reload(modifier_switch)

    imp.reload(wkst_add)
    imp.reload(wkst_align)
    imp.reload(wkst_bbox)
    imp.reload(wkst_copy)
    imp.reload(wkst_curve)
    imp.reload(wkst_cutting)
    imp.reload(wkst_delete)
    imp.reload(wkst_edit)
    imp.reload(wkst_io)
    imp.reload(wkst_mirror)
    imp.reload(wkst_modifier)
    imp.reload(wkst_origin)
    imp.reload(wkst_pivot)
    imp.reload(wkst_relations)
    imp.reload(wkst_sculpt)
    imp.reload(wkst_selections)
    imp.reload(wkst_snap)
    imp.reload(wkst_specials)
    imp.reload(wkst_transform)
    imp.reload(wkst_transform_normal)
    imp.reload(wkst_vertex_group)
    imp.reload(wkst_view_camera)
    imp.reload(wkst_visual)

    imp.reload(place_advanced_align)
    imp.reload(place_align_by_faces)
    imp.reload(place_distribute_objects)
    imp.reload(place_drop_to_ground)
    imp.reload(place_simple_align)

    imp.reload(rename_tools)

    imp.reload(sculpt_brush_quickset)
    imp.reload(sculpt_geometry_tools)
    imp.reload(sculpt_ice_tools)
    imp.reload(sculpt_mask_tools)
    imp.reload(sculpt_grease_project)
    imp.reload(sculpt_tools)
    imp.reload(sculpt_zero_brush)

    imp.reload(selections_mesh_order)
    imp.reload(selections_vismaya)

    imp.reload(ui_border_lines)
    imp.reload(ui_display_tools)
    imp.reload(ui_mesh_check)

    print("Reloaded multifiles")


###################################################
###################################################

else:

    from .operators import MeshBrush
    from .operators import PickSurfaceConstraint
    from .operators import Shrinkwrap
    from .operators import SmoothVertices
    from .operators.internal import ResizeMeshBrush
    from .operators.internal import StrokeMove
    from .operators.internal import StrokeSmooth
    from .preferences import SurfaceConstraintToolsPrefs
    from .ui.panels import SurfaceConstraintToolsPanel

    from . import add_simple_curve
    from . import add_tubetool

    from . import copy_attributes
    from . import copy_mifth_cloning
    from . import copy_replicator
    from . import copy_toall

    from . import curve_action
    from . import curve_outline
    from . import curve_split
    from . import curve_beveltaper

    from . import delete_clear_all_transform
    from . import delete_orphan_slayer

    from . import edit_boolean
    from . import edit_edge_fillet
    from . import edit_edge_roundifier
    from . import edit_edger
    from . import edit_extrude_along_curve
    from . import edit_face_inset_fillet
    from . import edit_faces_along_normals
    from . import edit_fast_loop
    from . import edit_ktools
    from . import edit_mesh_bsurfaces
    from . import edit_mesh_cut_faces
    from . import edit_mesh_looptools
    from . import edit_mesh_mextrude_plus
    from . import edit_mesh_sorting_tools
    from . import edit_mesh_vertex_tools
    from . import edit_meshlint
    from . import edit_multiedit
    from . import edit_offset_edges
    from . import edit_pushpull
    from . import edit_retopo_mt
    from . import edit_rotation_constrained
    from . import edit_snap_utilities
    from . import edit_snaps_shot
    from . import edit_transfer_normals
    from . import edit_tri_faces

    from . import group_sgrouper

    from . import io_auto_backgrounds
    from . import io_export_selected

    from . import mat_material_utils

    from . import modifier_automirror
    from . import modifier_easylattice
    from . import modifier_switch

    from . import wkst_add
    from . import wkst_align
    from . import wkst_bbox
    from . import wkst_copy
    from . import wkst_curve
    from . import wkst_cutting
    from . import wkst_delete
    from . import wkst_edit
    from . import wkst_io
    from . import wkst_mirror
    from . import wkst_modifier
    from . import wkst_origin
    from . import wkst_pivot
    from . import wkst_relations
    from . import wkst_sculpt
    from . import wkst_selections
    from . import wkst_snap
    from . import wkst_specials
    from . import wkst_transform
    from . import wkst_transform_normal
    from . import wkst_vertex_group
    from . import wkst_view_camera
    from . import wkst_visual

    from . import place_advanced_align
    from . import place_align_by_faces
    from . import place_distribute_objects
    from . import place_drop_to_ground
    from . import place_simple_align

    from . import rename_tools

    from . import sculpt_brush_quickset
    from . import sculpt_geometry_tools
    from . import sculpt_ice_tools
    from . import sculpt_mask_tools
    from . import sculpt_grease_project
    from . import sculpt_tools
    from . import sculpt_zero_brush

    from . import selections_mesh_order
    from . import selections_vismaya

    from . import ui_border_lines
    from . import ui_display_tools
    from . import ui_mesh_check

    print("Imported multifiles")


###################################################
###################################################


import add_simple_curve
import add_tubetool

import copy_attributes
import copy_mifth_cloning
import copy_replicator
import copy_toall

import curve_action
import curve_outline
import curve_split
import curve_beveltaper

import delete_clear_all_transform
import delete_orphan_slayer

import edit_boolean
import edit_edge_fillet
import edit_edge_roundifier
import edit_edger
import edit_extrude_along_curve
import edit_face_inset_fillet
import edit_faces_along_normals
import edit_fast_loop
import edit_ktools
import edit_mesh_bsurfaces
import edit_mesh_cut_faces
import edit_mesh_looptools
import edit_mesh_mextrude_plus
import edit_mesh_sorting_tools
import edit_mesh_vertex_tools
import edit_meshlint
import edit_multiedit
import edit_offset_edges
import edit_pushpull
import edit_retopo_mt
import edit_rotation_constrained
import edit_snap_utilities
import edit_snaps_shot
import edit_transfer_normals
import edit_tri_faces

import group_sgrouper

import io_auto_backgrounds
import io_export_selected

import mat_material_utils

import modifier_automirror
import modifier_easylattice
import modifier_switch

import wkst_add
import wkst_align
import wkst_bbox
import wkst_copy
import wkst_curve
import wkst_cutting
import wkst_delete
import wkst_edit
import wkst_io
import wkst_mirror
import wkst_modifier
import wkst_origin
import wkst_pivot
import wkst_relations
import wkst_sculpt
import wkst_selections
import wkst_snap
import wkst_specials
import wkst_transform
import wkst_transform_normal
import wkst_vertex_group
import wkst_view_camera
import wkst_visual

import place_advanced_align
import place_align_by_faces
import place_distribute_objects
import place_drop_to_ground
import place_simple_align

import rename_tools

import sculpt_brush_quickset
import sculpt_geometry_tools
import sculpt_ice_tools
import sculpt_mask_tools
import sculpt_grease_project
import sculpt_tools
import sculpt_zero_brush

import selections_mesh_order
import selections_vismaya

import ui_border_lines
import ui_display_tools
import ui_mesh_check


import bpy


###################################################
###################################################


def register():

    add_simple_curve.register()
    add_tubetool.register()

    copy_attributes.register()
    copy_mifth_cloning.register()
    copy_replicator.register()
    copy_toall.register()

    curve_action.register()
    curve_outline.register()
    curve_split.register()
    curve_beveltaper.register()

    delete_clear_all_transform.register()
    delete_orphan_slayer.register()

    edit_boolean.register()
    edit_edge_fillet.register()
    edit_edge_roundifier.register()
    edit_edger.register()
    edit_extrude_along_curve.register()
    edit_face_inset_fillet.register()
    edit_faces_along_normals.register()
    edit_fast_loop.register()
    edit_ktools.register()
    edit_mesh_bsurfaces.register()
    edit_mesh_cut_faces.register()
    edit_mesh_looptools.register()
    edit_mesh_mextrude_plus.register()
    edit_mesh_sorting_tools.register()
    edit_mesh_vertex_tools.register()
    edit_meshlint.register()
    edit_multiedit.register()
    edit_offset_edges.register()
    edit_pushpull.register()
    edit_retopo_mt.register()
    edit_rotation_constrained.register()
    edit_snap_utilities.register()
    edit_snaps_shot.register()
    edit_transfer_normals.register()
    edit_tri_faces.register()

    group_sgrouper.register()

    io_auto_backgrounds.register()
    io_export_selected.register()

    mat_material_utils.register()

    modifier_automirror.register()
    modifier_easylattice.register()
    modifier_switch.register()

    wkst_add.register()
    wkst_align.register()
    wkst_bbox.register()
    wkst_copy.register()
    wkst_curve.register()
    wkst_cutting.register()
    wkst_delete.register()
    wkst_edit.register()
    wkst_io.register()
    wkst_mirror.register()
    wkst_modifier.register()
    wkst_origin.register()
    wkst_pivot.register()
    wkst_relations.register()
    wkst_sculpt.register()
    wkst_selections.register()
    wkst_snap.register()
    wkst_specials.register()
    wkst_transform.register()
    wkst_transform_normal.register()
    wkst_vertex_group.register()
    wkst_view_camera.register()
    wkst_visual.register()

    place_advanced_align.register()
    place_align_by_faces.register()
    place_distribute_objects.register()
    place_drop_to_ground.register()
    place_simple_align.register()

    rename_tools.register()

    sculpt_brush_quickset.register()
    sculpt_geometry_tools.register()
    sculpt_ice_tools.register()
    sculpt_mask_tools.register()
    sculpt_grease_project.register()
    sculpt_tools.register()
    sculpt_zero_brush.register()

    selections_mesh_order.register()
    selections_vismaya.register()

    ui_border_lines.register()
    ui_display_tools.register()
    ui_mesh_check.register()

    bpy.utils.register_module(__name__)


def unregister():

    add_simple_curve.unregister()
    add_tubetool.unregister()

    copy_attributes.unregister()
    copy_mifth_cloning.unregister()
    copy_replicator.unregister()
    copy_toall.unregister()

    curve_action.unregister()
    curve_outline.unregister()
    curve_split.unregister()
    curve_beveltaper.unregister()

    delete_clear_all_transform.unregister()
    delete_orphan_slayer.unregister()

    edit_boolean.unregister()
    edit_edge_fillet.unregister()
    edit_edge_roundifier.unregister()
    edit_edger.unregister()
    edit_extrude_along_curve.unregister()
    edit_face_inset_fillet.unregister()
    edit_faces_along_normals.unregister()
    edit_fast_loop.unregister()
    edit_ktools.unregister()
    edit_mesh_bsurfaces.unregister()
    edit_mesh_cut_faces.unregister()
    edit_mesh_looptools.unregister()
    edit_mesh_mextrude_plus.unregister()
    edit_mesh_sorting_tools.unregister()
    edit_mesh_vertex_tools.unregister()
    edit_meshlint.unregister()
    edit_multiedit.unregister()
    edit_offset_edges.unregister()
    edit_pushpull.unregister()
    edit_retopo_mt.unregister()
    edit_rotation_constrained.unregister()
    edit_snap_utilities.unregister()
    edit_snaps_shot.unregister()
    edit_transfer_normals.unregister()
    edit_tri_faces.unregister()

    group_sgrouper.unregister()

    io_auto_backgrounds.unregister()
    io_export_selected.unregister()

    mat_material_utils.unregister()

    modifier_automirror.unregister()
    modifier_easylattice.unregister()
    modifier_switch.unregister()

    wkst_add.unregister()
    wkst_align.unregister()
    wkst_bbox.unregister()
    wkst_copy.unregister()
    wkst_curve.unregister()
    wkst_cutting.unregister()
    wkst_delete.unregister()
    wkst_edit.unregister()
    wkst_io.unregister()
    wkst_mirror.unregister()
    wkst_modifier.unregister()
    wkst_origin.unregister()
    wkst_pivot.unregister()
    wkst_relations.unregister()
    wkst_sculpt.unregister()
    wkst_selections.unregister()
    wkst_snap.unregister()
    wkst_specials.unregister()
    wkst_transform.unregister()
    wkst_transform_normal.unregister()
    wkst_vertex_group.unregister()
    wkst_view_camera.unregister()
    wkst_visual.unregister()

    place_advanced_align.unregister()
    place_align_by_faces.unregister()
    place_distribute_objects.unregister()
    place_drop_to_ground.unregister()
    place_simple_align.unregister()

    rename_tools.unregister()

    sculpt_brush_quickset.unregister()
    sculpt_geometry_tools.unregister()
    sculpt_ice_tools.unregister()
    sculpt_mask_tools.unregister()
    sculpt_grease_project.unregister()
    sculpt_tools.unregister()
    sculpt_zero_brush.unregister()

    selections_mesh_order.unregister()
    selections_vismaya.unregister()

    ui_border_lines.unregister()
    ui_display_tools.unregister()
    ui_mesh_check.unregister()

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
