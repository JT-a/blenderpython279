bl_info = {
    "name": "Move UV",
    "description": "Move the UV from 3D view",
    "author": "kgeogeo",
    "version": (1, 0),
    "blender": (2, 6, 3),
    "category": "Paint"}

import bpy
import bmesh
from bpy.app.handlers import persistent
from bpy_extras.view3d_utils import location_3d_to_region_2d as loc3d2d
from bpy.types import Operator
from bpy.props import FloatVectorProperty
import mathutils
from mathutils import *
from math import *


def find_uv(context):
    obj_data = bmesh.from_edit_mesh(context.object.data)
    l = []
    first = 0
    diff = 0
    for f, face in enumerate(obj_data.faces):
        for v, vertex in enumerate(face.verts):
            if vertex.select:
                l.append([f, v])
                if first == 0:
                    v1 = vertex.link_loops[0].vert.co
                    sv1 = loc3d2d(context.region, context.space_data.region_3d, v1)
                    v2 = vertex.link_loops[0].link_loop_next.vert.co
                    sv2 = loc3d2d(context.region, context.space_data.region_3d, v2)
                    vres = sv2 - sv1
                    va = vres.angle(Vector((0.0, 1.0)))

                    uv1 = vertex.link_loops[0][obj_data.loops.layers.uv.active].uv
                    uv2 = vertex.link_loops[0].link_loop_next[obj_data.loops.layers.uv.active].uv
                    uvres = uv2 - uv1
                    uva = uvres.angle(Vector((0.0, 1.0)))
                    diff = uva - va
                    first += 1

    return l, diff

# Oprerator Class to pan the view3D


class MoveUV(bpy.types.Operator):
    bl_idname = "view3d.move_uv"
    bl_label = "Move the UV from 3D view"

    l = []
    uva = 0
    first_mouse = FloatVectorProperty(name="OffsetUV", default=(0.0, 0.0), subtype='XYZ', size=2)
    offsetuv = FloatVectorProperty(name="OffsetUV", default=(0.0, 0.0), subtype='XYZ', size=2)
    old_offsetuv = FloatVectorProperty(name="old_OffsetUV", default=(0.0, 0.0), subtype='XYZ', size=2)
    firstuv = FloatVectorProperty(name="FirstUV", default=(0.0, 0.0), subtype='XYZ', size=2)

    @classmethod
    def poll(cls, context):
        return (context.edit_object)

    def modal(self, context, event):
        ob = context.object
        obj_data = bmesh.from_edit_mesh(ob.data)
        div = 10000
        self.offsetuv += Vector(((event.mouse_region_x - self.first_mouse.x) / div,
                                 (event.mouse_region_y - self.first_mouse.y) / div))

        o = self.offsetuv
        oo = self.old_offsetuv
        for i, j in self.l:
            d = obj_data.faces[i].loops[j][obj_data.loops.layers.uv.active]
            vec = Vector((o.x - o.y, o.x + o.y))
            d.uv = d.uv - Vector((oo.x, oo.y)) + vec

        self.old_offsetuv = vec
        self.first_mouse = Vector((event.mouse_region_x, event.mouse_region_y))
        ob.data.update()

        if context.user_preferences.inputs.select_mouse == 'LEFT':
            mb = 'LEFTMOUSE'
        else:
            mb = 'RIGHTMOUSE'

        if event.type == mb and event.value == 'RELEASE':
            return {'FINISHED'}
        if event.type == 'ESC' and event.value == 'RELEASE':
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        self.first_mouse = Vector((event.mouse_region_x, event.mouse_region_y))
        self.l, self.uva = find_uv(context)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_module(__name__)

    km = bpy.context.window_manager.keyconfigs.default.keymaps['3D View']
    kmi = km.keymap_items.new("view3d.move_uv", 'G', 'PRESS', alt=True)


def unregister():
    bpy.utils.unregister_module(__name__)

    km = bpy.context.window_manager.keyconfigs.default.keymaps['3D View']
    for kmi in (kmi for kmi in km.keymap_items if kmi.idname in {"view3d.move_uv", }):
        km.keymap_items.remove(kmi)

if __name__ == "__main__":
    register()
