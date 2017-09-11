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
    'name': 'Add Custom Menu Items',
    'author': 'chromoly',
    'version': (0, 4),
    'blender': (2, 78, 0),
    'location': 'View3D > Mouse > Menu',
    'category': 'Mesh'}


import bpy

from .utils import addongroup


class Mesh_OT_SharpEdge(bpy.types.Operator):
    bl_label = 'SharpEdge'
    bl_idname = 'mesh.set_sharp_edge'
    bl_options = {'REGISTER', 'UNDO'}

    crease = bpy.props.FloatProperty(
        name='Crease',
        description='Crease',
        default=0.0,
        min=-1.0,
        max=1.0,
        soft_min=-1.0,
        soft_max=1.0,
        step=1,
        precision=3)

    sharp = bpy.props.BoolProperty(
        name='Sharp',
        description='sharp',
        default=False)

    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.mode == 'EDIT'
        else:
            return False

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        me = context.active_object.data
        crease = self.properties.crease
        sharp = self.properties.sharp
        for e in me.edges:
            if e.select and not e.hide:
                e.crease = crease
                e.use_edge_sharp = sharp
        bpy.ops.object.mode_set(mode='EDIT')

        #bpy.ops.transform.edge_crease(value=crease)
        #bpy.ops.mesh.mark_sharp(clear=True if not sharp else False)

        return {'FINISHED'}


#menu_func = (lambda self, context: self.layout.operator(SharpEdge.bl_idname,
#                                        text="SharpEdge", icon='PLUGIN'))

def menu_func1(self, context):
    item = self.layout.operator(Mesh_OT_SharpEdge.bl_idname,
                                text="Mark SharpEdge", icon='PLUGIN')
    item.crease = 1.0
    item.sharp = 1


def menu_func2(self, context):
    item = self.layout.operator(Mesh_OT_SharpEdge.bl_idname,
                                text="Clear SharpEdge", icon='PLUGIN')
    item.crease = 0.0
    item.sharp = 0


def register():
    addongroup.register_module(__name__)
    #bpy.types.register(SharpEdge)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(menu_func1)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(menu_func2)


def unregister():
    addongroup.unregister_module(__name__)
    #bpy.types.unregister(SharpEdge)
    bpy.types.VIEW3D_MT_edit_mesh_edges.remove(menu_func1)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(menu_func2)


if __name__ == '__main__':
    register()
