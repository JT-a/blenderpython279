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
    'name': 'Vertex Slide',
    'author': 'chromoly',
    'version': (0, 1, 2),
    'blender': (2, 78, 0),
    'location': 'View3D > Mouse',
    'description': '',
    'warning': '',
    'category': 'Mesh'}


import math
import bpy
from mathutils import Vector
import bgl
import bmesh

from .utils import addongroup

from .utils import vagl as vagl
from .utils import vaview3d as vav
from .utils import modalmouse_old as modalmouse


class MESH_OT_vertext_slide(bpy.types.Operator):
    bl_description = ''
    bl_idname = 'mesh.vertex_slide'
    bl_label = 'Vertex Slide'
    bl_options = {'REGISTER', 'UNDO'}

    value = bpy.props.FloatProperty(
        name='Value',
        default=0.0,
        step=1)
    mode = bpy.props.EnumProperty(
        name='Mode',
        items=(('DISTANCE', 'Distance', ''),
               ('FACTOR', 'Factor', '')),
        default='DISTANCE')
    flip = bpy.props.IntProperty(
        name='Flip',
        description='Direction. 0:center, -1or1:side',
        default=0,
        min=-1,
        max=1)
    use_local_coords = bpy.props.BoolProperty(
        name='Use Local Coords')

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'EDIT_MESH'

    def execute(self, context):
        threshold = 1e-6

        region = context.region
        rv3d = context.region_data
        actob = context.active_object
        mat = actob.matrix_world
        imat = actob.matrix_world.inverted()

        bm = bmesh.from_edit_mesh(actob.data)

        edgelines = self.edgelines  # 描画用
        translines = self.translines  # 描画用

        edgelines[:] = []  # Clear
        translines[:] = []  # Clear

#         mm_relative = self.modal_mouse.relative.to_3d()
#         if mm_relative.length < threshold:
#             mm_relative = Vector((1, 0))
        if self.modal_mouse.lock:
            lock_relative = self.modal_mouse.lock - self.modal_mouse.origin
        else:
            lock_relative = self.modal_mouse.relative
        if lock_relative.length < threshold:
            lock_relative = Vector((1, 0))

        # 座標初期化
        for src, dst in zip(self.bm.verts, bm.verts):
            dst.co = src.co

        new_coordinates = {}  # index: Vector

        for i, eve in enumerate(bm.verts):
            if not eve.select or eve.hide:
                continue

            # 頂点に接続する頂点を求める
            connected_vertices = []
            for eed in (e for e in eve.link_edges if not e.hide):
                connected_vertices.append(eed.other_vert(eve))
            if not connected_vertices:
                continue

            # 辺の長さが0なら、更にその先にある頂点を追加する
            verts = []
            for eve2 in connected_vertices:
                if (eve2.co - eve.co).length < threshold:
                    for eed in (e for e in eve2.link_edges if not e.hide):
                        verts.append(eed.other_vert(eve2))
            connected_vertices.extend(verts)

            # 移動先の頂点を求める
            angles = []
            v1 = eve.co
            v1W = mat * v1
            v1R = vav.project(region, rv3d, v1W).to_2d()
            for eve2 in connected_vertices:
                v2W = mat * eve2.co
                v2R = vav.project(region, rv3d, v2W).to_2d()
                v = v2R - v1R
                if v.length >= threshold:
                    angles.append(lock_relative.angle(v))
                else:
                    angles.append(math.pi * 2)  # 優先度最低
            eve_target = connected_vertices[angles.index(min(angles))]
            v2 = eve_target.co
            v2W = mat * v2
            if self.use_local_coords:
                transvec = v2 - v1
            else:
                transvec = v2W - v1W
            if transvec.length < threshold:
                continue
            
            if self.modal_mouse.lock:
                value = self.value
            else:
                if self.mode == 'DISTANCE':
                    value = min(max(0, self.value), transvec.length)
                else:
                    value = min(max(0.0, self.value), 1.0)
            
            if self.mode == 'DISTANCE':
                transvec.normalize()
            if self.use_local_coords:
                if self.flip:
                    newco = v2 - transvec * value
                else:
                    newco = v1 + transvec * value
            else:
                if self.flip:
                    newco = v2W - transvec * value
                else:
                    newco = v1W + transvec * value
            # edgelines
            for eve2 in connected_vertices:
                vW = mat * eve2.co
                if eve2 == eve_target:
                    translines.append((v1W, vW))
                else:
                    edgelines.append((v1W, vW))
            
            if self.use_local_coords:
                new_coordinates[i] = newco
            else:
                new_coordinates[i] = imat * newco

        # apply
        bm.verts.ensure_lookup_table()
        for i, vec in new_coordinates.items():
            bm.verts[i].co = vec

        bm.normal_update()
        bmesh.update_edit_mesh(actob.data, True, True)

        return {'FINISHED'}

    def draw_callback_px(self, context):
        glsettings = vagl.GLSettings(context)
        glsettings.push()
        cm = glsettings.region_view3d_space()
        cm.__enter__()

        # draw edgelines
        bgl.glColor4f(0.8, 0.8, 0.8, 1.0)
        bgl.glBegin(bgl.GL_LINES)
        for p1, p2 in self.edgelines:
            bgl.glVertex3f(*p1)
            bgl.glVertex3f(*p2)
        if self.modal_mouse.lock:
            bgl.glColor4f(0.0, 0.0, 1.0, 1.0)
        else:
            bgl.glColor4f(1.0, 1.0, .0, 1.0)
        for p1, p2 in self.translines:
            bgl.glVertex3f(*p1)
            bgl.glVertex3f(*p2)
        bgl.glEnd()

        cm.__exit__(None, None, None)
        glsettings.pop()

    def modal(self, context, event):
        if event.type == 'INBETWEEN_MOUSEMOVE':
            return {'RUNNING_MODAL'}

        context.space_data.transform_orientation = 'LOCAL'
        
        bm = bmesh.from_edit_mesh(context.active_object.data)
        
        retval = self.modal_mouse.modal(context, event)
        if retval & {'PASS_THROUGH', 'RUNNING_MODAL'}:
            if retval & {'PASS_THROUGH'}:
                if event.type == 'I' and event.value == 'PRESS':
                    self.flip ^= True
            # Reset vert coords
            for dst, src in zip(bm.verts, self.bm.verts):
                dst.co = src.co
            
            self.execute(context)
            context.area.tag_redraw()
            retval = {'RUNNING_MODAL'}
        
        context.space_data.transform_orientation = self._orientation
        
        if retval & {'FINISHED', 'CANCELLED'}:
            if retval & {'CANCELLED'}:
                # Reset vert coords
                for dst, src in zip(bm.verts, self.bm.verts):
                    dst.co = src.co
                bm.normal_update()
#                 context.active_object.update_tag({'OBJECT', 'DATA'})  # Modifierを更新
                bmesh.update_edit_mesh(context.active_object.data, True, False)
            context.space_data.draw_handler_remove(self._handle, 'WINDOW')
            context.area.tag_redraw()

        return retval

    def invoke(self, context=None, event=None):
        v3d = context.space_data
        actob = context.active_object

        bm = bmesh.from_edit_mesh(actob.data)
        bm.verts.index_update()
        bm.edges.index_update()
        bm.faces.index_update()
        self.bm = bm.copy()

        class ModalMouse(modalmouse.ModalMouse):
            mode = 'DISTANCE'
            medes = modes=('DISTANCE', 'FACTOR')
            def header_text(self, context):
                text = 'Flip (I): {}, Use Local Coords (D): {}'
                text = text.format(self.master.flip,
                                   self.master.use_local_coords)
                return text
                 
        self.modal_mouse = ModalMouse(context, event, self,
                                      use_normalized_orientation=False)

        # init
        self.translines = []  # 描画用。移動中のedge
        self.edgelines = []  # 描画用。移動可能なedge

        self.region_id = context.region.id
        self._handle = context.space_data.draw_handler_add(
                                            self.draw_callback_px, (context,),
                                            'WINDOW', 'POST_PIXEL')
        
        self._orientation = v3d.transform_orientation
        return {'RUNNING_MODAL'}


def menu_func(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.operator(MESH_OT_vertext_slide.bl_idname, text='Vertex Slide')


addon_keymaps = []


def register():
    addongroup.AddonGroup.register_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)

    km = addongroup.AddonGroup.get_keymap('Mesh')
    if km:
        kmi = km.keymap_items.new('mesh.vertex_slide', 'V', 'PRESS',
                                  shift=True, head=True)
        addon_keymaps.append((km, kmi))


def unregister():
    addongroup.AddonGroup.unregister_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_func)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == '__main__':
    register()
