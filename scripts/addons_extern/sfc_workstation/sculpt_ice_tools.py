#  ***** BEGIN GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  ***** END GPL LICENSE BLOCK *****


# bl_info = {
#    "name": "Ice Tools",
#    "author": "Ian Lloyd Dela Cruz",
#    "version": (2, 0),
#    "blender": (2, 7, 0),
#    "location": "3d View > Tool shelf",
#    "description": "Retopology support",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "Retopology"}

import bpy
import math
import bmesh
from bpy.props import *


def add_mod(mod, link, meth, offset):
    md = bpy.context.active_object.modifiers.new(mod, 'SHRINKWRAP')
    md.target = bpy.data.objects[link]
    md.wrap_method = meth
    if md.wrap_method == "PROJECT":
        md.use_negative_direction = True
    if md.wrap_method == "NEAREST_SURFACEPOINT":
        md.use_keep_above_surface = True
    md.offset = offset
    if "retopo_suppo_frozen" in bpy.context.active_object.vertex_groups:
        md.vertex_group = "retopo_suppo_thawed"
    md.show_on_cage = True
    md.show_expanded = False


def sw_Update(meshlink, wrap_offset, wrap_meth):
    activeObj = bpy.context.active_object
    wm = bpy.context.window_manager
    oldmod = activeObj.mode
    selmod = bpy.context.tool_settings.mesh_select_mode
    modnam = "shrinkwrap_apply"
    modlist = bpy.context.object.modifiers
    modops = bpy.ops.object.modifier_move_up

    if selmod[0] == True:
        oldSel = 'VERT'
    if selmod[1] == True:
        oldSel = 'EDGE'
    if selmod[2] == True:
        oldSel = 'FACE'

    bpy.context.scene.objects.active = activeObj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')

    if "shrinkwrap_apply" in bpy.context.active_object.modifiers:
        bpy.ops.object.modifier_remove(modifier="shrinkwrap_apply")

    if "retopo_suppo_thawed" in bpy.context.active_object.vertex_groups:
        tv = bpy.data.objects[activeObj.name].vertex_groups["retopo_suppo_thawed"].index
        activeObj.vertex_groups.active_index = tv
        bpy.ops.object.vertex_group_remove(all=False)

    if "retopo_suppo_frozen" in bpy.context.active_object.vertex_groups:
        fv = bpy.data.objects[activeObj.name].vertex_groups["retopo_suppo_frozen"].index
        activeObj.vertex_groups.active_index = fv
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.object.vertex_group_deselect()
        bpy.ops.object.vertex_group_add()
        bpy.data.objects[activeObj.name].vertex_groups.active.name = "retopo_suppo_thawed"
        bpy.ops.object.vertex_group_assign()

    # add sw mod
    add_mod(modnam, meshlink, wrap_meth, wrap_offset)

    # move sw mod up the stack
    for i in modlist:
        if modlist.find(modnam) == 0:
            break
        modops(modifier=modnam)

    # apply modifier
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modnam)
    bpy.ops.object.mode_set(mode='EDIT')

    if wm.sw_autoapply == False:
        # move the sw mod below the mirror or multires mod assuming this is your first
        add_mod(modnam, meshlink, wrap_meth, wrap_offset)
        for i in modlist:
            if modlist.find(modnam) == 0:
                break
            if modlist.find(modnam) == 1:
                if modlist.find("Mirror") == 0:
                    break
                if modlist.find("Multires") == 0:
                    break
            modops(modifier=modnam)

    # clipcenter
    if "Mirror" in bpy.data.objects[activeObj.name].modifiers:
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)

        for v in bm.verts:
            if wm.clipx_threshold <= 0:
                if v.co.x >= wm.clipx_threshold:
                    v.co.x = 0
            elif wm.clipx_threshold >= 0:
                if v.co.x <= wm.clipx_threshold:
                    v.co.x = 0

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type=oldSel)

    if "retopo_suppo_vgroup" in bpy.context.active_object.vertex_groups:
        vg = bpy.data.objects[activeObj.name].vertex_groups["retopo_suppo_vgroup"].index
        activeObj.vertex_groups.active_index = vg
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.vertex_group_remove(all=False)

    bpy.ops.object.mode_set(mode=oldmod)


class SetUpRetopoMesh(bpy.types.Operator):
    '''Set up Retopology Mesh on Active Object'''
    bl_idname = "setup.retopo"
    bl_label = "Set Up Retopo Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'OBJECT'

    def execute(self, context):
        wm = context.window_manager
        oldObj = context.active_object.name

        bpy.ops.view3d.snap_cursor_to_active()
        bpy.ops.mesh.primitive_plane_add(enter_editmode=True)

        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.editmode_toggle()
        context.object.name = oldObj + "_retopo_mesh"
        activeObj = context.active_object

        # place mirror mod
        md = activeObj.modifiers.new("Mirror", 'MIRROR')
        md.show_on_cage = True
        md.use_clip = True

        # generate grease pencil surface draw mode on retopo mesh
        bpy.context.scene.tool_settings.grease_pencil_source = 'OBJECT'
        if context.object.grease_pencil is None:
            bpy.ops.gpencil.data_add()
        if context.object.grease_pencil.layers.active is None:
            bpy.ops.gpencil.layer_add()
        # convert to base values
        context.object.grease_pencil.draw_mode = 'SURFACE'
        context.object.grease_pencil.layers.active.line_width = 1
        context.object.grease_pencil.layers.active.show_x_ray = True
        context.object.grease_pencil.layers.active.use_onion_skinning = False
        context.object.grease_pencil.layers.active.use_volumetric_strokes = False
        context.object.grease_pencil.layers.active.use_onion_skinning = False
        bpy.data.objects[oldObj].select = True

        # further mesh toggles
        bpy.ops.object.editmode_toggle()
        context.scene.tool_settings.use_snap = True
        context.scene.tool_settings.snap_element = 'FACE'
        context.scene.tool_settings.snap_target = 'CLOSEST'
        context.scene.tool_settings.use_snap_project = True
        context.object.show_all_edges = True
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

        # establish link for shrinkwrap update function
        wm.sw_target = oldObj
        wm.sw_mesh = activeObj.name

        for SelectedObject in context.selected_objects:
            if SelectedObject != activeObj:
                SelectedObject.select = False
        activeObj.select = True
        return {'FINISHED'}


class ShrinkUpdate(bpy.types.Operator):
    '''Applies Shrinkwrap Mod on Retopo Mesh'''
    bl_idname = "shrink.update"
    bl_label = "Shrinkwrap Update"
    bl_options = {'REGISTER', 'UNDO'}

    apply_mod = bpy.props.BoolProperty(name="Auto-apply Shrinkwrap", default=True)
    sw_offset = bpy.props.FloatProperty(name="Offset:", min=-0.1, max=0.1, step=0.1, precision=3, default=0)
    sw_wrapmethod = bpy.props.EnumProperty(
        name='Wrap Method',
        items=(
            ('NEAREST_VERTEX', 'Nearest Vertex', ""),
            ('PROJECT', 'Project', ""),
            ('NEAREST_SURFACEPOINT', 'Nearest Surface Point', "")),
        default='PROJECT')

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        activeObj = context.active_object
        wm = context.window_manager

        # establish link
        if len(bpy.context.selected_objects) == 2:
            for SelectedObject in bpy.context.selected_objects:
                if SelectedObject != activeObj:
                    wm.sw_target = SelectedObject.name
                else:
                    wm.sw_mesh = activeObj.name
                if SelectedObject != activeObj:
                    SelectedObject.select = False

        if wm.sw_mesh != activeObj.name:
            self.report({'WARNING'}, "Establish Link First!")
            return {'FINISHED'}
        else:
            if self.apply_mod == True:
                wm.sw_autoapply = True
            else:
                wm.sw_autoapply = False

            if activeObj.mode == 'EDIT':
                bpy.ops.object.vertex_group_add()
                bpy.data.objects[activeObj.name].vertex_groups.active.name = "retopo_suppo_vgroup"
                bpy.ops.object.vertex_group_assign()

            sw_Update(wm.sw_target, self.sw_offset, self.sw_wrapmethod)
            activeObj.select = True

        return {'FINISHED'}


class FreezeVerts(bpy.types.Operator):
    '''Immunize verts from shrinkwrap update'''
    bl_idname = "freeze_verts.retopo"
    bl_label = "Freeze Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'EDIT'

    def execute(self, context):
        activeObj = bpy.context.active_object

        if "retopo_suppo_frozen" in bpy.context.active_object.vertex_groups:
            fv = bpy.data.objects[activeObj.name].vertex_groups["retopo_suppo_frozen"].index
            activeObj.vertex_groups.active_index = fv
            bpy.ops.object.vertex_group_assign()
        else:
            bpy.ops.object.vertex_group_add()
            bpy.data.objects[activeObj.name].vertex_groups.active.name = "retopo_suppo_frozen"
            bpy.ops.object.vertex_group_assign()

        return {'FINISHED'}


class ThawFrozenVerts(bpy.types.Operator):
    '''Remove frozen verts'''
    bl_idname = "thaw_freeze_verts.retopo"
    bl_label = "Thaw Frozen Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'EDIT'

    def execute(self, context):
        activeObj = bpy.context.active_object

        if "retopo_suppo_frozen" in bpy.context.active_object.vertex_groups:
            tv = bpy.data.objects[activeObj.name].vertex_groups["retopo_suppo_frozen"].index
            activeObj.vertex_groups.active_index = tv
            bpy.ops.object.vertex_group_remove_from()

        return {'FINISHED'}


class ShowFrozenVerts(bpy.types.Operator):
    '''Show frozen verts'''
    bl_idname = "show_freeze_verts.retopo"
    bl_label = "Show Frozen Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'EDIT'

    def execute(self, context):
        activeObj = bpy.context.active_object

        if "retopo_suppo_frozen" in bpy.context.active_object.vertex_groups:
            bpy.ops.mesh.select_mode(type='VERT')
            fv = bpy.data.objects[activeObj.name].vertex_groups["retopo_suppo_frozen"].index
            activeObj.vertex_groups.active_index = fv
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.vertex_group_select()

        return {'FINISHED'}


class PolySculpt(bpy.types.Operator):
    '''Polysculpt retopology mesh'''
    bl_idname = "polysculpt.retopo"
    bl_label = "Sculpts Retopo Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        activeObj = context.active_object
        wm = context.window_manager

        if wm.sw_mesh != activeObj.name:
            self.report({'WARNING'}, "Establish Link First!")
        else:
            context.space_data.show_only_render = False
            context.object.show_wire = True
            bpy.ops.object.mode_set(mode='SCULPT')

        return {'FINISHED'}

"""    
class RetopoSupport(bpy.types.Panel):
    Retopology Support Functions
    bl_label = "Ice Tools"
    bl_idname = "OBJECT_PT_retosuppo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Retopology'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row_sw = layout.row(align=True)
        row_sw.alignment = 'EXPAND'
        row_sw.operator("setup.retopo", "Set Up Retopo Mesh")
        row_sw = layout.row(align=True)
        row_sw.alignment = 'EXPAND'
        row_sw.operator("shrink.update", "Shrinkwrap Update")
        row_sw.operator("polysculpt.retopo", "", icon = "SCULPTMODE_HLT")
        row_sw = layout.row(align=True)
        row_sw.prop(wm, "clipx_threshold", "Clip X Threshold")
        
        row_fv = layout.row(align=True)
        row_fv.alignment = 'EXPAND'
        row_fv.operator("freeze_verts.retopo", "Freeze")
        row_fv.operator("thaw_freeze_verts.retopo", "Thaw")
        row_fv.operator("show_freeze_verts.retopo", "Show") 
        
        if context.active_object is not None:
            row_view = layout.row(align=True)
            row_sw.alignment = 'EXPAND'
            row_view.prop(context.object, "show_wire", toggle =False)
            row_view.prop(context.object, "show_x_ray", toggle =False)
            row_view.prop(context.space_data, "show_occlude_wire", toggle =False)              

"""


def register():
    bpy.utils.register_module(__name__)

    bpy.types.WindowManager.sw_mesh = StringProperty()
    bpy.types.WindowManager.sw_target = StringProperty()
    bpy.types.WindowManager.sw_use_onlythawed = BoolProperty(default=False)
    bpy.types.WindowManager.sw_autoapply = BoolProperty(default=True)
    bpy.types.WindowManager.clipx_threshold = FloatProperty(min=-0.1, max=0.1, step=0.1, precision=3, default=0)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
