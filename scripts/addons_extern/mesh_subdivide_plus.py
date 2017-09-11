# mesh_subsurf.py Copyright (C) 2012, Jordi Vall-llovera
#
# Subdivide the mesh selection with catmull-clark algorithm while in edit mode
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Subdivide Plus",
    "author": "Jordi Vall-llovera",
    "version": (0,2),
    "blender": (2, 6, 3),
    "location": "View3D > Specials > Subdivide Plus ",
    "description": "Subdivide the mesh selection with catmull-clark algorithm while in edit mode",
    "warning": "Only works well with face select mode",
    "wiki_url": "",
    "tracker_url": ""\
        "",
    "category": "Mesh"}

"""
Usage:

Launch from "W-menu" or from "Mesh -> Vertices -> Subdivide Plus"


Additional links:
    Author Site: http://jordiart3d.blogspot.com.es/
"""


import bpy
from bpy.props import IntProperty

def subdivideplus_mesh(context):

    # deselect everything for security
    for obj in context.selected_objects:
        obj.select = False

    # get active object
    obj = context.active_object

    # duplicate the object so it can be used for the subdivide surface modifier
    obj.select = True 
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.duplicate()
    target = context.active_object
    
    context.scene.objects.active = obj
    
    sw = obj.modifiers.new(type='SUBSURF', name='subdivide_target')

    # apply the modifier
    bpy.ops.object.modifier_apply(modifier='subdivide_target')
    
    # back to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # delete unwanted faces in first object
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # change context
    context.scene.objects.active = target
    
    # back to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # delete unwanted faces in second object
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # change context
    context.scene.objects.active = obj
    
    # join meshes and finish
    obj.select = True
    target.select = True
    bpy.ops.object.join()
    
    # go back to initial state
    bpy.ops.object.mode_set(mode='EDIT')
  
class Subdiv(bpy.types.Operator):
    '''Subdivide the mesh selection with catmull-clark algorithm while in edit mode'''
    bl_idname = 'mesh.subdivplus'
    bl_label = 'Subdivide Plus'
    bl_options = {'REGISTER', 'UNDO'}

    iterations = IntProperty(name="Iterations",
                default=1, min=0, max=6, soft_min=0, soft_max=6)

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH')

    def execute(self, context):
        for i in range(0,self.iterations):
            subdivideplus_mesh(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(Subdiv.bl_idname, text="Subdivide Plus")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.VIEW3D_MT_edit_mesh_specials.append(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_func)

if __name__ == "__main__":
    register()
