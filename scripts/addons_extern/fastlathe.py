# -*- coding: utf-8 -*-

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
    "name": "lathe",
    "author": "Laurent Laget",
    "version": (0, 4),
    "blender": (2, 78, 0),
    "location": "Add > Mesh",
    "description": "Create a lathe",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy

def main(context):
    for ob in context.scene.objects:
        print(ob)

#classe lathe
class lathe(bpy.types.Operator):
    """description"""
    bl_idname = "object.lathe"
    bl_label = "Lathe"
    bl_options = {'REGISTER', 'UNDO'}
   

    def invoke(self, context, event):
        
        bpy.ops.view3d.viewnumpad(type='FRONT')
        bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.modifier_add(type='SCREW')
        bpy.context.object.modifiers["Screw"].steps = 32
        return {'FINISHED'}

#classe lathe_libre
class lathe_libre(bpy.types.Operator):
    """description"""
    bl_idname = "object.lathe_libre"
    bl_label = "Lathe_libre"
    bl_options = {'REGISTER', 'UNDO'}
   

    def invoke(self, context, event):
        bpy.ops.view3d.viewnumpad(type='FRONT')
        bpy.ops.curve.primitive_bezier_curve_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.object.modifier_add(type='SCREW')
        bpy.context.object.modifiers["Screw"].steps = 32
        return {'FINISHED'}


def menu_item(self, context):
       self.layout.operator(lathe.bl_idname, text="lathe", icon="PLUGIN")
       self.layout.operator(lathe_libre.bl_idname, text="lathe_libre", icon="PLUGIN")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)

    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
