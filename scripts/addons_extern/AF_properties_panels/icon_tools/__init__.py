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
    "name": "Icon Tools 1.5.0",
    "author": "koil",
    "version": (1, 5, 0),
    "blender": (2, 66, 1),
    "location": "Editors > View 3D > Properties (N) or Tools (T)> Tools.",
    "description": "Icon Tools. set switch = 'TOOLS' to replace Tool Shelf.",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Icon_Tools",
    "tracker_url": "https://projects.blender.org/tracker/index.php?func=detail&aid=34584",
    "category": "Panel"
}


""" ---------------------------------------------------------------- """
""" header """

import bpy
from bpy.types import Header, Menu, Panel, Operator
from math import sin, cos
import bmesh
from bpy_extras import object_utils
from ..utils import AddonPreferences, SpaceProperty
""" ---------------------------------------------------------------- """
""" Replace Tool Shelf """
"""

	To replace the Tool Shelf with Icon Tools.

	Close blender.
	Open Icon_Tools.py
	Change:
		switch = 'UI'
	To:
		switch = 'TOOLS'
	Save Icon_Tools.py
	Open blender.

"""
""" ---------------------------------------------------------------- """

global switch
switch = 'UI'

bpy.types.Scene.b_label = bpy.props.BoolProperty(default=0)  # labels			d
bpy.types.Scene.b_add_set = bpy.props.BoolProperty(default=0)  # add_set			d
bpy.types.Scene.tool = bpy.props.StringProperty(default='UI')  # tool				d
bpy.types.Scene.sst = bpy.props.FloatProperty(default=0.25)  # spin screw turns		d
bpy.types.Scene.sss = bpy.props.FloatProperty(default=9.0)  # spin screw steps		d
bpy.types.Scene.sm = bpy.props.BoolProperty(default=1)		# sm # descope			d #XX00#
bpy.types.Scene.se = bpy.props.BoolProperty(default=1)		# se # descope			d #XX00#

global descope
descope = 1

""" ---------------------------------------------------------------- """


""" ---------------------------------------------------------------- """
""" task """
"""

1.5.0

poll obect mode: done
	when no object select, no menu.
	it was using active_object.type before checking if active_object

check draw_extra: done
	no scene = context.scene: done
	bpy: done
	ui rule: done
		modifiers is dynamic, global col: do later
	comment: do later

check OBJECT: done
	no scene = context.scene: done
	bpy: done
	ui rule: done
		global column, keep aligned
	comment: done

check MESH: done
	no scene = context.scene: done
	bpy: done
	ui rule: done
	comment: done

check ARMATURE: done
	no scene = context.scene: done
	bpy: done
	ui rule: done
	comment: done

check POSE: done
	no scene = context.scene: done
	bpy: done
	ui rule: done
	comment: done

bpy: done
	bpy is still used some places, like (bpy.types.Operator)
	(bpy.types.Operator): (types.Operator) dont work
	from bpy.types import Header, Menu, Panel, Operator (Operator)

move labels to panel: done
	different modes.

add set: done

orginize mesh tools: done

add bmesh: done

--------------------------------

labels:

check mod operator:

test tool:
	if tool exist:
		switch = tool
	else:
		switch = 'UI'
	make enum

	switch operator:
		add reset blender label

operator: reload and run:
	space_data context

modifer mirror, multires:

"""
""" ---------------------------------------------------------------- """


""" ---------------------------------------------------------------- """
""" object.mod_add_with_targets(mb_type='BOOLEAN') """


class OT_mod_add_with_targets(Operator):
    bl_idname = "object.mod_add_with_targets"
    bl_label = "mod_add_with_targets"
    mb_type = bpy.props.StringProperty(default='BOOLEAN')

    """ ------------------------------------------------ """
    """ mod_bool_add_with_targets """

    def execute(self, context):
        """ ------------------------------------------------ """
        """ count active_object.modifiers """

        mm_count = 0
        for i in bpy.context.active_object.modifiers:
            mm_count += 1

        """ ------------------------------------------------ """

        """ ------------------------------------------------ """
        """ if select_object!=active_object                  """
        """     add mod to active_object                     """
        """     add select_object                            """

        xxx = bpy.context.active_object

        for obs in bpy.context.selected_objects:

            if self.mb_type == 'SUBSURF':
                bpy.context.scene.objects.active = obs
                bpy.ops.object.modifier_add(type=self.mb_type)
                mm_count += 1

            if self.mb_type == 'ARMATURE':
                if obs.name != bpy.context.active_object.name:
                    bpy.ops.object.modifier_add(type=self.mb_type)
                    mm_name = bpy.context.active_object.modifiers[mm_count].name
                    bpy.context.active_object.modifiers[mm_name].object = obs             # targets armatures
                    mm_count += 1

            if self.mb_type == 'BOOLEAN':
                if obs.name != bpy.context.active_object.name:
                    bpy.ops.object.modifier_add(type=self.mb_type)
                    mm_name = bpy.context.active_object.modifiers[mm_count].name
                    bpy.context.active_object.modifiers[mm_name].object = obs             # target objects
                    bpy.context.active_object.modifiers[mm_name].operation = "INTERSECT"
                    mm_count += 1

            if self.mb_type == 'MESH_DEFORM':
                if obs.name != bpy.context.active_object.name:
                    bpy.ops.object.modifier_add(type=self.mb_type)
                    mm_name = bpy.context.active_object.modifiers[mm_count].name
                    bpy.context.active_object.modifiers[mm_name].object = obs             # target objects
                    mm_count += 1

        bpy.context.scene.objects.active = xxx

        """ ------------------------------------------------ """

        return{'FINISHED'}

    """ ------------------------------------------------ """

bpy.utils.register_class(OT_mod_add_with_targets)

""" ---------------------------------------------------------------- """


""" ---------------------------------------------------------------- """
""" object.moda_add_with_targets(mb_type='BOOLEAN') """


class OT_moda_add_with_targets(Operator):
    bl_idname = "object.moda_add_with_targets"
    bl_label = "moda_add_with_targets"
    mb_type = bpy.props.StringProperty(default='BOOLEAN')

    """ ------------------------------------------------ """
    """ mod_bool_add_with_targets """

    def execute(self, context):
        """ ------------------------------------------------ """

        if self.mb_type == 'ARMATURE':

            xxx = bpy.context.active_object

            for obs in bpy.context.selected_objects:

                bpy.context.scene.objects.active = obs

                mm_count = 0
                for i in bpy.context.active_object.modifiers:
                    mm_count += 1

                if obs.name != xxx.name:
                    bpy.ops.object.modifier_add(type=self.mb_type)
                    mm_name = bpy.context.active_object.modifiers[mm_count].name
                    bpy.context.active_object.modifiers[mm_name].object = xxx
                    mm_count += 1

            bpy.context.scene.objects.active = xxx

        """ ------------------------------------------------ """

        return{'FINISHED'}

    """ ------------------------------------------------ """

bpy.utils.register_class(OT_moda_add_with_targets)

""" ---------------------------------------------------------------- """


""" ---------------------------------------------------------------- """
""" object.mod_add_with_targets(mb_type='BOOLEAN') """


class OT_mod_add_with_targets(Operator):
    bl_idname = "object.mod_add_with_targets"
    bl_label = "mod_add_with_targets"
    mb_type = bpy.props.StringProperty(default='BOOLEAN')

    """ ------------------------------------------------ """
    """ mod_bool_add_with_targets """

    def execute(self, context):
        """ ------------------------------------------------ """
        """ count active_object.modifiers """

        mm_count = 0
        for i in bpy.context.active_object.modifiers:
            mm_count += 1

        """ ------------------------------------------------ """

        """ ------------------------------------------------ """
        """ if select_object!=active_object                  """
        """     add mod to active_object                     """
        """     add select_object                            """

        xxx = bpy.context.active_object

        for obs in bpy.context.selected_objects:

            if self.mb_type == 'SUBSURF':
                bpy.context.scene.objects.active = obs
                bpy.ops.object.modifier_add(type=self.mb_type)
                mm_count += 1

            if self.mb_type == 'ARMATURE':
                if obs.name != bpy.context.active_object.name:
                    bpy.ops.object.modifier_add(type=self.mb_type)
                    mm_name = bpy.context.active_object.modifiers[mm_count].name
                    bpy.context.active_object.modifiers[mm_name].object = obs             # targets armatures
                    mm_count += 1

            if self.mb_type == 'BOOLEAN':
                if obs.name != bpy.context.active_object.name:
                    bpy.ops.object.modifier_add(type=self.mb_type)
                    mm_name = bpy.context.active_object.modifiers[mm_count].name
                    bpy.context.active_object.modifiers[mm_name].object = obs             # target objects
                    bpy.context.active_object.modifiers[mm_name].operation = "INTERSECT"
                    mm_count += 1

            if self.mb_type == 'MESH_DEFORM':
                if obs.name != bpy.context.active_object.name:
                    bpy.ops.object.modifier_add(type=self.mb_type)
                    mm_name = bpy.context.active_object.modifiers[mm_count].name
                    bpy.context.active_object.modifiers[mm_name].object = obs             # target objects
                    mm_count += 1

        bpy.context.scene.objects.active = xxx

        """ ------------------------------------------------ """

        return{'FINISHED'}

    """ ------------------------------------------------ """

bpy.utils.register_class(OT_mod_add_with_targets)

""" ---------------------------------------------------------------- """


""" ------------------------------------------------ """
""" draw_main """


def draw_add_set(context, layout):

    if descope:

        col = layout.column(align=True)

        """ Cursor """
        row = col.row(align=True)
        row.operator("view3d.snap_cursor_to_center", text="Center")
        row.operator("view3d.snap_cursor_to_active", icon='FORCE_BOID', text="")
        row.operator("view3d.snap_cursor_to_selected", icon='FORCE_FORCE', text="")
        row.operator("view3d.snap_selected_to_cursor", icon='FORCE_LENNARDJONES', text="")
        row.operator("view3d.snap_cursor_to_grid", icon='HELP', text="")
        row.operator("view3d.snap_selected_to_grid", icon='BBOX', text="")

        """ View """
        row = col.row(align=True)
        row.operator("view3d.view_persportho", text="View")
        row.operator("mesh.primitive_plane_add", icon='MESH_PLANE', text="")
        row.operator("mesh.primitive_cube_add", icon='MESH_CUBE', text="")
        row.operator("mesh.primitive_circle_add", icon='MESH_CIRCLE', text="")
        row.operator("mesh.primitive_uv_sphere_add", icon='MESH_UVSPHERE', text="")
        row.operator("mesh.primitive_ico_sphere_add", icon='MESH_ICOSPHERE', text="")

        """ Origin """
        row = col.row(align=True)
        row.operator("object.origin_set", text="Origin")
        row.operator("mesh.primitive_grid_add", icon='MESH_GRID', text="")
        row.operator("mesh.primitive_monkey_add", icon='MESH_MONKEY', text="")
        row.operator("mesh.primitive_cylinder_add", icon='MESH_CYLINDER', text="")
        row.operator("mesh.primitive_torus_add", icon='MESH_TORUS', text="")
        row.operator("mesh.primitive_cone_add", icon='MESH_CONE', text="")

        """ Add Curve """
        row = col.row(align=True)
        row.operator("transform.translate", text="Locate")
        row.operator("curve.primitive_bezier_curve_add", icon='CURVE_BEZCURVE', text="")
        row.operator("curve.primitive_bezier_circle_add", icon='CURVE_BEZCIRCLE', text="")
        row.operator("curve.primitive_nurbs_curve_add", icon='CURVE_NCURVE', text="")
        row.operator("curve.primitive_nurbs_circle_add", icon='CURVE_NCIRCLE', text="")
        row.operator("curve.primitive_nurbs_path_add", icon='CURVE_PATH', text="")

        """ Add Surface """
        row = col.row(align=True)
        row.operator("transform.rotate")
        row.operator("surface.primitive_nurbs_surface_circle_add", icon='SURFACE_NCIRCLE', text="")
        row.operator("surface.primitive_nurbs_surface_surface_add", icon='SURFACE_NSURFACE', text="")
        row.operator("surface.primitive_nurbs_surface_cylinder_add", icon='SURFACE_NCYLINDER', text="")
        row.operator("surface.primitive_nurbs_surface_sphere_add", icon='SURFACE_NSPHERE', text="")
        row.operator("surface.primitive_nurbs_surface_torus_add", icon='SURFACE_NTORUS', text="")

        """ Add """
        row = col.row(align=True)
        row.operator("transform.resize", text="Scale")
        row.operator("object.armature_add", text="", icon="BONE_DATA")
        row.operator("object.add", text="", icon="OUTLINER_OB_LATTICE").type = "LATTICE"
        row.operator("object.speaker_add", icon='OUTLINER_OB_SPEAKER', text="")
        row.operator("object.camera_add", icon='OUTLINER_OB_CAMERA', text="")
        row.operator("object.lamp_add", icon='OUTLINER_OB_LAMP', text="")

""" ------------------------------------------------ """


""" ------------------------------------------------ """
""" draw_extra """


def draw_extra(context, layout):
    """ -------------------------------- """
    """ active_object """

    if context.active_object:

        # global column
        # this is the gap before modifiers
        # when no modifier, makes a bigger gap
        col = layout.column(align=True)

        active_object = context.active_object

        """ -------------------------------- """
        """ OBJECT """

        if context.mode == "OBJECT":

            xx = 0
            for i in context.selected_objects:
                xx += 1

            if context.active_object.type == 'MESH':

                if xx == 1:
                    row = col.row(align=True)
                    row.operator("object.modifier_add", icon='MOD_SUBSURF', text=" Subsurf").type = "SUBSURF"
                    row.operator("object.modifier_add", icon='MOD_ARMATURE', text=" Armature").type = "ARMATURE"
                    row = col.row(align=True)
                    row.operator("object.modifier_add", icon='MOD_BOOLEAN', text=" Boolean").type = "BOOLEAN"
                    row.operator("object.modifier_add", icon='MOD_MESHDEFORM', text=" Mesh D").type = "MESH_DEFORM"
                elif xx > 1:
                    row = col.row(align=True)
                    row.operator("object.mod_add_with_targets", icon='MOD_SUBSURF', text=" Subsurf").mb_type = "SUBSURF"
                    row.operator("object.mod_add_with_targets", icon='MOD_ARMATURE', text=" Armature").mb_type = "ARMATURE"
                    row = col.row(align=True)
                    row.operator("object.mod_add_with_targets", icon='MOD_BOOLEAN', text=" Boolean").mb_type = "BOOLEAN"
                    row.operator("object.mod_add_with_targets", icon='MOD_MESHDEFORM', text=" Mesh D").mb_type = "MESH_DEFORM"

            if context.active_object.type == 'ARMATURE':

                if xx > 1:
                    row = col.row(align=True)
                    row.operator("object.moda_add_with_targets", icon='MOD_ARMATURE', text=" Armature").mb_type = "ARMATURE"

        """ -------------------------------- """
        """ OBJECT POSE """

        if context.mode == "OBJECT" or context.mode == "POSE":

            """ Keyframes """
            if context.active_object and context.active_object.type in {'MESH', 'CURVE', 'SURFACE', 'ARMATURE'}:

                col = layout.column(align=True)
                row = col.row(align=True)
                row.label(text="Keyframes (I)  Delete (Alt+I)")
                row = col.row(align=True)
                row.operator("anim.keyframe_insert_menu", icon='ZOOMIN', text="")
                row.operator("anim.keyframe_delete_v3d", icon='ZOOMOUT', text="")
                row.prop_search(context.scene.keying_sets_all, "active", context.scene, "keying_sets_all", text="")
                row.operator("anim.keyframe_insert", text="", icon='KEY_HLT')
                row.operator("anim.keyframe_delete", text="", icon='KEY_DEHLT')

        """ -------------------------------- """

    view = context.space_data

    #col = layout.column(align=True)
    split = layout.split()

    """ Grease """
    col = split.column(align=True)
    row = col.row(align=True)
#    row.prop(context.tool_settings, "use_grease_pencil_sessions",text="")
    row.label(text="Session")
    row = col.row(align=True)
    row.operator("gpencil.draw", text="", icon="GREASEPENCIL").mode = 'DRAW'
    row.operator("gpencil.draw", text="", icon="OUTLINER_OB_CURVE").mode = 'DRAW_STRAIGHT'
    row.operator("gpencil.draw", text="", icon="OUTLINER_OB_MESH").mode = 'DRAW_POLY'
    row.operator("gpencil.draw", text="", icon="PANEL_CLOSE").mode = 'ERASER'

    """ Misc """
    row = col.row(align=True)
    row.prop(view, "use_occlude_geometry", text="")
    row.prop(view, "show_textured_solid", text="", icon="TEXTURE")
    row.prop(view, "show_background_images", text="", icon="IMAGE_DATA")
    if context.active_object:
        row.prop(context.active_object, "show_x_ray", text="", icon="RADIO")
    else:
        row.operator("object.lamp_add", text="", icon="OUTLINER_OB_LAMP")

    """ Misc """
    row = col.row(align=True)
    row.prop(context.scene.tool_settings, "use_uv_select_sync", text="")
    row.prop(view, "show_manipulator", text="")
    row.operator("mesh.primitive_cube_add", text="", icon="MESH_CUBE")
    row.operator("object.armature_add", text="", icon="BONE_DATA")

    """ Motion """
    col = split.column(align=True)
    row = col.row(align=True)
    #row.prop(context.scene, "hide",text="")
    row.label(text=" ")
    row = col.row(align=True)
    row.operator("object.paths_calculate", text="", icon="ANIM_DATA")
    row.operator("object.paths_clear", text="", icon="PANEL_CLOSE")
    row.operator("screen.repeat_last", text="", icon="RECOVER_LAST")
    row.operator("screen.repeat_history", text="", icon="TIME")

    row = col.row(align=True)
    row.operator("render.render", text="", icon='RENDER_STILL')
    row.operator("render.render", text="", icon='RENDER_ANIMATION').animation = True
    row.operator("render.opengl", text="", icon='RENDER_STILL')
    row.operator("render.opengl", text="", icon='RENDER_ANIMATION').animation = True

    row = col.row(align=True)
    row.operator("wm.save_mainfile", text="", icon="FILE_TICK")
    row.operator("wm.save_as_mainfile", text="", icon="SAVE_AS")
    row.operator("wm.console_toggle", text="", icon="CONSOLE")
    row.operator("render.play_rendered_anim", text="", icon='PLAY')

""" ------------------------------------------------ """


""" ------------------------------------------------ """
""" Object Mode """


class VIEW3D_PT_tools_objectmode(Panel):
    bl_category = "Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = switch
    # bl_region_type = context.scene.tool	# check if exist, set
    bl_context = "objectmode"
    bl_label = "Icon Tools"
    # bl_options = {'HIDE_HEADER'}		# check if top default

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'OBJECT'))

    def draw(self, context):

        layout = self.layout

        if context.active_object:
            if context.scene.b_add_set:
                draw_add_set(context, layout)
        else:
            draw_add_set(context, layout)

        """ -------------------------------- """
        """ Object """

        col = layout.column(align=True)		# global column, keep aligned

        if context.active_object and context.active_object.type in {'MESH', 'CURVE', 'SURFACE'}:
            row = col.row(align=True)
            row.operator("object.shade_smooth", text="Smooth")
            row.operator("object.shade_flat", text="Flat")
        if context.active_object:
            row = col.row(align=True)
            row.operator("object.join", text="Join")
            row = col.row(align=True)
            row.operator("object.origin_set", text="Origin")

        """ -------------------------------- """

        draw_extra(context, layout)

""" ------------------------------------------------ """


""" ------------------------------------------------ """
""" Edit Mode Mesh """


class VIEW3D_PT_tools_meshedit(Panel):
    bl_category = "Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = switch
    bl_context = "mesh_edit"
    bl_label = "Icon Tools"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_MESH'))

    def draw(self, context):

        layout = self.layout

        if context.active_object:
            if context.scene.b_add_set:
                draw_add_set(context, layout)

        """ -------------------------------- """
        """ Mesh """

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.faces_shade_smooth", text="Smooth")
        row.operator("mesh.faces_shade_flat", text="Flat")
        row = col.row(align=True)
        row.operator("mesh.merge")
        row.operator("mesh.edge_face_add", text="Make Face")
        row = col.row(align=True)
        row.operator("mesh.subdivide")
        row.operator("mesh.unsubdivide")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.loop_multi_select", text="Edge Loop").ring = False
        row.operator("mesh.loop_multi_select", text="Edge Ring").ring = True
        row = col.row(align=True)
        row.operator("mesh.edge_split")
        row.operator("mesh.bridge_edge_loops", text="Edge Bridge")
        row = col.row(align=True)
        row.operator("transform.edge_slide")
        row.operator("transform.vert_slide")
        row = col.row(align=True)
        row.operator("mesh.edge_rotate", text="RE CW").use_ccw = False
        row.operator("mesh.edge_rotate", text="RE CCW").use_ccw = True

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.loopcut_slide", text="Loop Cut")
        row.operator("mesh.inset")
        row = col.row(align=True)
        props = row.operator("mesh.knife_tool", text="Knife All")
        props.use_occlude_geometry = True
        props.only_selected = False
        props = row.operator("mesh.knife_tool", text="Knife Sel")
        props.use_occlude_geometry = False
        props.only_selected = True
        row = col.row(align=True)
        row.operator("mesh.split")
        row.operator("mesh.separate")
        row = col.row(align=True)
        row.operator("mesh.rip_move")
        row.operator("mesh.rip_move_fill")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.normals_make_consistent", text="N Recalc")
        row.operator("mesh.flip_normals", text="N Flip")
        row = col.row(align=True)
        row.operator("mesh.noise", text="VT Noise")
        row.operator("mesh.vertices_smooth", text="V Smooth")
        row = col.row(align=True)
        row.operator("mesh.remove_doubles", text="Rem Doubles")
        row.operator("mesh.symmetrize")
        row = col.row(align=True)
        row.operator("mesh.quads_convert_to_tris", text="Quad to Tri")
        row.operator("mesh.tris_convert_to_quads", text="Tri to Quad")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("wm.call_menu", text="UV Unwrap").name = "VIEW3D_MT_uv_map"
        row = col.row(align=True)
        row.operator("mesh.mark_seam", text="Mark Seam").clear = False
        row.operator("mesh.mark_seam", text="Clear Seam").clear = True

        col = layout.column(align=True)
        row = col.row(align=True)
        OPSP = row.operator("mesh.spin", text="Spin")
        OPSC = row.operator("mesh.screw", text="Screw")
        row = col.row(align=True)
        row.prop(context.scene, "sst", text="Turns")
        row.prop(context.scene, "sss", text="Steps")
        OPSP.steps = context.scene.sss
        OPSP.angle = (context.scene.sst * 6.283185307179586476925286766559)
        OPSC.steps = context.scene.sss
        OPSC.turns = context.scene.sst

        """ -------------------------------- """

        draw_extra(context, layout)

""" ------------------------------------------------ """


""" ------------------------------------------------ """
""" Edit Mode Armature """


class VIEW3D_PT_tools_armatureedit(Panel):
    bl_category = "Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = switch
    bl_context = "armature_edit"
    bl_label = "Icon Tools"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_ARMATURE'))

    def draw(self, context):

        layout = self.layout

        if context.active_object:
            if context.scene.b_add_set:
                draw_add_set(context, layout)

        """ -------------------------------- """
        """ Armature """

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("armature.bone_primitive_add", text="Add")
        row = col.row(align=True)
        row.operator("armature.merge")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("armature.subdivide", text="Subdivide").number_cuts = 1
        row.operator("armature.subdivide", text="Subdivide 2").number_cuts = 2
        row = col.row(align=True)
        row.operator("armature.select_hierarchy", text="Select Parent").direction = "PARENT"
        row.operator("armature.select_hierarchy", text="Select Child").direction = "CHILD"
        row = col.row(align=True)
        row.operator("armature.fill", text="Fill Between")
        row.operator("armature.switch_direction")
        row = col.row(align=True)
        row.operator("armature.parent_set")
        row.operator("armature.parent_clear")
        #row = col.row(align=True)
        # row.operator("armature.calculate_roll")
        # row.operator("armature.switch_direction")

        """ -------------------------------- """

        draw_extra(context, layout)

""" ------------------------------------------------ """


""" ------------------------------------------------ """
""" Pose Mode Armature """


class VIEW3D_PT_tools_posemode(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = switch
    bl_context = "posemode"
    bl_label = "Icon Tools"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'POSE'))

    def draw(self, context):

        layout = self.layout

        if context.active_object:
            if context.scene.b_add_set:
                draw_add_set(context, layout)

        """ -------------------------------- """
        """ Pose """

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("poselib.pose_add", text="Add To Library")

        row = col.row(align=True)
        row.operator("pose.copy")
        row.operator("pose.paste")
        row = col.row(align=True)
        row.operator("pose.loc_clear", text="Clear Loc")
        row.operator("pose.rot_clear", text="Clear Rot")
        row = col.row(align=True)
        row.operator("pose.scale_clear", text="Clear Scale")
        row.operator("pose.transforms_clear", text="Clear All")

        """ -------------------------------- """

        draw_extra(context, layout)

""" ------------------------------------------------ """


""" ---------------------------------------------------------------- """
""" OBJECT_OT_primitive_custom_add """


class OBJECT_OT_primitive_custom_tri_add(Operator):
    bl_idname = "mesh.primitive_custom_tri_add"
    bl_label = "Add Triangle"

    def execute(self, context):

        A = 6.283185307179586476925286766559 / 3

        verts = [(sin(A * 1), 0.0, cos(A * 1)),
                 (sin(A * 2), 0.0, cos(A * 2)),
                 (sin(A * 3), 0.0, cos(A * 3)),
                 ]

        faces = [(0, 1, 2)]

        mesh = bpy.data.meshes.new("Cube")

        bm = bmesh.new()

        for v_co in verts:
            bm.verts.new(v_co)

        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()

        object_utils.object_data_add(context, mesh)

        return{'FINISHED'}

bpy.utils.register_class(OBJECT_OT_primitive_custom_tri_add)

""" ---------------------------------------------------------------- """


""" ------------------------------------------------ """
""" Add """

bpy.types.Scene.add_p_c_vertices = bpy.props.IntProperty(default=32, soft_min=3, soft_max=250)
bpy.types.Scene.add_p_c_radius = bpy.props.FloatProperty(default=1, soft_min=-50.0, soft_max=50.0)

bpy.types.Scene.add_p_uvs_segments = bpy.props.IntProperty(default=32, soft_min=3, soft_max=250)
bpy.types.Scene.add_p_uvs_rings = bpy.props.IntProperty(default=16, soft_min=3, soft_max=250)


class VIEW3D_PT_Add(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Add"

    def draw(self, context):

        layout = self.layout

        # Circle
        col = layout.column(align=True)
        row = col.row(align=True)
        p = row.operator("mesh.primitive_circle_add")
        row = col.row(align=True)
        row.prop(context.scene, "add_p_c_vertices", text="vertices")
        row = col.row(align=True)
        p.vertices = context.scene.add_p_c_vertices

        # UV Sphere
        col = layout.column(align=True)
        row = col.row(align=True)
        p = row.operator("mesh.primitive_uv_sphere_add")
        row = col.row(align=True)
        row.prop(context.scene, "add_p_uvs_segments", text="segments")
        row = col.row(align=True)
        row.prop(context.scene, "add_p_uvs_rings", text="rings")
        row = col.row(align=True)
        p.segments = context.scene.add_p_uvs_segments
        p.ring_count = context.scene.add_p_uvs_rings

        # Triangle
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.primitive_custom_tri_add")

        """

        # ---------------------------------------------------------------- #
        # rule: make col + row when you want to draw

        check = 0

        # ---------------------------------------------------------------- #

        # ---------------------------------------------------------------- #

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label("--------------------------------")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.primitive_custom_add",text="test")

        if check==1:
            row = col.row(align=True)
            row.operator("mesh.primitive_custom_add",text="test")

        row = col.row(align=True)
        row.operator("mesh.primitive_custom_add",text="test")

        # ---------------------------------------------------------------- #

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label("--------------------------------")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.primitive_custom_add",text="test")

        if check==1:
            col = layout.column(align=True)
            row = col.row(align=True)
            row.operator("mesh.primitive_custom_add",text="test")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.primitive_custom_add",text="test")
        

        # ---------------------------------------------------------------- #

        col = layout.column(align=True)
        row = col.row(align=True)
        row.label("--------------------------------")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.primitive_custom_add",text="test")

        if check==1:
            row.operator("mesh.primitive_custom_add",text="test")

        row.operator("mesh.primitive_custom_add",text="test")

        # ---------------------------------------------------------------- #


        """

""" ------------------------------------------------ """


""" ---------------------------------------------------------------- """
""" UI_OT_dere_add """


class UI_OT_dere_add(Operator):
    bl_idname = "ui.dere_add"
    bl_label = "De Register Add"

    def execute(self, context):

        bpy.utils.unregister_class(VIEW3D_PT_Add)

        return{'FINISHED'}


bpy.utils.register_class(UI_OT_dere_add)

""" ---------------------------------------------------------------- """


""" ---------------------------------------------------------------- """
""" UI_OT_regi_add """


class UI_OT_regi_add(Operator):
    bl_idname = "ui.regi_add"
    bl_label = "Register Add"

    def execute(self, context):

        bpy.utils.register_class(VIEW3D_PT_Add)

        return{'FINISHED'}


bpy.utils.register_class(UI_OT_regi_add)

""" ---------------------------------------------------------------- """


""" ---------------------------------------------------------------- """
""" Icon Tools """


class SCENE_PT_Icon_Tools(Panel):
    bl_label = "Icon Tools"
    bl_idname = "SCENE_PT_Icon_Tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        """ column split """
        split = layout.split()

        """ column one """
        col = split.column(align=False)
        row = col.row(align=False)
        row.prop(context.scene, "b_label", text="Labels", toggle=True)

        row = col.row(align=False)
        row.prop(context.scene, "b_add_set", text="Add Set", toggle=True)

        row = col.row(align=False)
        row.operator("ui.regi_add")

        row = col.row(align=False)
        row.operator("ui.dere_add")

        """ column two """

        """
        col = split.column(align=False)
        col.context_pointer_set("bpy.data.screens['Scripting']", context.space_data)
        row = col.row(align=False)
        row.context_pointer_set("bpy.data.screens['Scripting']", context.space_data)

        col = split.column(align=False)
        col.context_pointer_set("Scripting", context.space_data)
        row = col.row(align=False)
        row.context_pointer_set("Scripting", context.space_data)

        col = split.column(align=False)
        col.context_pointer_set("SpaceTextEditor", context.space_data)
        row = col.row(align=False)
        row.context_pointer_set("SpaceTextEditor", context.space_data)

        p=row.operator("text.reload")
        row = col.row(align=False)
        row.operator("text.run_script")
        """

        """ -------------------------------- """
        """ Labels """

        if context.scene.b_label == 1:

            if context.mode == 'OBJECT':

                col = layout.column(align=True)
                row = col.row(align=True)
                row.label("Object")

                row = col.row(align=True)
                row.label("Select All: A")
                row.label("Locate: G")

                row = col.row(align=True)
                row.label("Rotate: R")
                row.label("Scale: S")

                row = col.row(align=True)
                row.label("Mode: TAB")
                row.label("Snap Menu: Shift + S")

                row = col.row(align=True)
                row.label("Box Select: B")
                row.label("Circle Select: C")

                row = col.row(align=True)
                row.label("Add: Shift + A")
                row.label("Delete: X")

                row = col.row(align=True)
                row.label("Duplcate: Shift + D")
                row.label("Join: Ctrl + J")

                row = col.row(align=True)
                row.label("Pan: Shift + LMB")
                row.label("View: NUMPAD 5")

            if context.mode == 'EDIT_MESH':

                col = layout.column(align=True)
                row = col.row(align=True)
                row.label("Mesh")

                row = col.row(align=True)
                row.label("Select All: A")
                row.label("Locate: G")

                row = col.row(align=True)
                row.label("Rotate: R")
                row.label("Scale: S")

                row = col.row(align=True)
                row.label("Mode: TAB")
                row.label("Snap Menu: Shift + S")

                row = col.row(align=True)
                row.label("Box Select: B")
                row.label("Circle Select: C")

                row = col.row(align=True)
                row.label("Add: Shift + A")
                row.label("Delete: X")

                row = col.row(align=True)
                row.label("Duplcate: Shift + D")
                row.label("Merge: Alt + M")

                row = col.row(align=True)
                row.label("Extrude: E")
                row.label("Knife: K")

                row = col.row(align=True)
                row.label("Edge Loop: Alt + RMB")
                row.label("Edge Ring: Ctrl + Alt + RMB")

                row = col.row(align=True)
                row.label("Pan: Shift + LMB")
                row.label("View: NUMPAD 5")

        """ -------------------------------- """


class PT_xxxx(Panel):
    bl_label = "Test"
    bl_idname = "xxxxxx"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        col.context_pointer_set("SpaceTextEditor", context.space_data)
        row = col.row(align=False)
        row.context_pointer_set("SpaceTextEditor", context.space_data)

        p = row.operator("text.reload")
        row = col.row(align=False)
        row.operator("text.run_script")
        row = col.row(align=False)
        row.label(str(context.space_data))


""" ---------------------------------------------------------------- """


""" ------------------------------------------------ """
""" Register """


def register():
    bpy.utils.register_class(VIEW3D_PT_tools_objectmode)
    bpy.utils.register_class(VIEW3D_PT_tools_meshedit)
    bpy.utils.register_class(VIEW3D_PT_tools_armatureedit)
    bpy.utils.register_class(VIEW3D_PT_tools_posemode)
    bpy.utils.register_class(SCENE_PT_Icon_Tools)

    # bpy.utils.register_class(PT_xxxx)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_tools_objectmode)
    bpy.utils.unregister_class(VIEW3D_PT_tools_meshedit)
    bpy.utils.unregister_class(VIEW3D_PT_tools_armatureedit)
    bpy.utils.unregister_class(VIEW3D_PT_tools_posemode)
    bpy.utils.unregister_class(SCENE_PT_Icon_Tools)

    # bpy.utils.unregister_class(PT_xxxx)

if __name__ == "__main__":
    register()

""" ------------------------------------------------ """
