bl_info = {
    "name": "Mask Extract",
    "author": "Ian Lloyd Dela Cruz",
    "version": (1, 0),
    "blender": (2, 7, 5),
    "location": "3d View > Tool shelf",
    "description": "Dyntopo Mask Extraction",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sculpting"}

import bpy
import math
import bmesh
from bpy.props import *


def mask_to_vertex_group(obj, name, pull):
    wm = bpy.context.window_manager
    maskcount = 0

    vgroup = obj.vertex_groups.new(name)
    bpy.ops.object.vertex_group_set_active(group=vgroup.name)

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    deform_layer = bm.verts.layers.deform.active
    if deform_layer is None:
        deform_layer = bm.verts.layers.deform.new()
    mask = bm.verts.layers.paint_mask.active
    if mask is not None:
        wm.mask_detect_layer = True
        for v in bm.verts:
            if v[mask] == 1:
                maskcount += 1
                v.select = True
                v[deform_layer][vgroup.index] = 1.0
                n = (v.normal) * pull
                v.co += n
            else:
                v.select = False
    else:
        wm.mask_detect_layer = False

    if maskcount == 0:
        wm.mask_detect_layer = False

    bm.to_mesh(obj.data)
    bm.free()
    pass
    return vgroup


def duplicateObject(scene, name, copyobj):

    # Create new mesh
    mesh = bpy.data.meshes.new(name)

    # Create new object associated with the mesh
    ob_new = bpy.data.objects.new(name, mesh)

    # Copy data block from the old object into the new object
    ob_new.data = copyobj.data.copy()
    ob_new.scale = copyobj.scale
    ob_new.location = copyobj.location

    # Link new object to the given scene and select it
    bpy.context.scene.objects.link(ob_new)
    ob_new.select = True
    bpy.context.scene.objects.active = bpy.data.objects[ob_new.name]

    return ob_new


def smoothextracted():
    wm = bpy.context.window_manager
    for i in range(wm.mask_smooth_normals):
        md = bpy.context.active_object.modifiers.new('smooth_extract', 'SMOOTH')
        md.iterations = 5

        bpy.ops.object.modifier_apply(apply_as='DATA', modifier='smooth_extract')


def isolate(obj):
    for SelectedObject in bpy.context.selected_objects:
        if SelectedObject != obj:
            SelectedObject.select = False

    obj.select = True


class MaskExtract(bpy.types.Operator):
    '''Decimate Masked Areas'''
    bl_idname = "mask.extraction"
    bl_label = "Extract masked areas"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):
        wm = context.window_manager
        activeObj = context.active_object
        modnam = "Mask Extract"
        vname = "mask extraction vgroup"

        if context.sculpt_object.use_dynamic_topology_sculpting:
            self.report({'WARNING'}, "Exit Dyntopo First!")
            return {'FINISHED'}

        # isolate target mesh
        isolate(activeObj)

        # convert mask to vgroup
        duplicateObject(context.scene.name, activeObj.name, activeObj)

        mask_to_vertex_group(context.active_object, vname, wm.mask_extract_offset)

        if wm.mask_detect_layer == True:
            self.report({'WARNING'}, "Masked Areas Present!")
        else:
            self.report({'WARNING'}, "No Masked Areas!")
            activeObj.select = False
            bpy.ops.object.delete()
            activeObj.select = True
            bpy.context.scene.objects.active = bpy.data.objects[activeObj.name]
            return {'FINISHED'}

        # place/apply mask modifier
        md = bpy.context.active_object.modifiers.new(modnam, 'MASK')
        md.vertex_group = vname

        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modnam)

        # place/apply smooth modifier
        smoothextracted()

        # place/apply solidify modifier
        md = bpy.context.active_object.modifiers.new(modnam + "solid", 'SOLIDIFY')
        md.use_rim = True
        md.thickness = wm.mask_extract_thickness

        if wm.mask_solid_apply == True:
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modnam + "solid")

            # place/apply smooth modifier
            smoothextracted()

        # remove vgroup
        if vname in bpy.context.active_object.vertex_groups:
            bpy.ops.object.vertex_group_set_active(group=vname)
            bpy.ops.object.vertex_group_remove(all=False)

        # select target mesh
        isolate(activeObj)
        bpy.context.scene.objects.active = bpy.data.objects[activeObj.name]

        return {'FINISHED'}


class MaskDecimationPanel(bpy.types.Panel):
    """Mask Extract Function"""
    bl_label = "Mask Extract"
    bl_idname = "OBJECT_PT_maskextraction"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Sculpt'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row_sw = layout.row(align=True)
        row_sw.alignment = 'EXPAND'
        row_sw.operator("mask.extraction", "Extract")
        row_sw = layout.row(align=False)
        row_sw.prop(wm, "mask_extract_offset", "Offset")
        row_sw = layout.row(align=False)
        row_sw.prop(wm, "mask_extract_thickness", "Thickness")
        row_sw = layout.row(align=False)
        row_sw.prop(wm, "mask_smooth_normals", "Smooth")
        row_sw = layout.row(align=False)
        row_sw.prop(wm, "mask_solid_apply", "Apply Solidify")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.WindowManager.mask_extract_offset = FloatProperty(min=0, max=1, step=0.1, precision=3, default=.01)
    bpy.types.WindowManager.mask_extract_thickness = FloatProperty(min=0, max=1, step=0.1, precision=3, default=.025)
    bpy.types.WindowManager.mask_smooth_normals = IntProperty(min=0, max=10, default=1)
    bpy.types.WindowManager.mask_solid_apply = BoolProperty(default=True)
    bpy.types.WindowManager.mask_detect_layer = BoolProperty(default=False)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
