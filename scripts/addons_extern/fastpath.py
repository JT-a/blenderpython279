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
    "name": "fast_path",
    "author": "Laurent Laget",
    "version": (0, 1),
    "blender": (2, 78, 5),
    "location": "Add",
    "description": "Create fast_path",
    "warning": "",
    "wiki_url": "",
    "category": "Add Curve",
    }

import bpy

def main(context):
    for ob in context.scene.objects:
        print(ob)

#Classe fastpath
class fastpath(bpy.types.Operator):
    """Create a path for the selected object"""
    bl_idname = "object.fastpath"
    bl_label = "fastpath"
    bl_options = {'REGISTER', 'UNDO'}
   

    def invoke(self, context, event):
        
        #Get the name of the selected object and add a follow path constrain to it
        objectname = bpy.context.active_object
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        #bpy.ops.view3d.snap_cursor_to_selected()

        
        # Add a curve object , name it, delete vertices and make it ready for shift + right click draw
        bpy.ops.curve.primitive_bezier_curve_add()
        bpy.context.object.name = "Path"
        pathname= bpy.context.active_object
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.delete(type='VERT')
        
        #print (pathname)
        #print (objectname)
        
        #Go back to object mode , reselect the selected object , push the name of the path in the follow path constraint and animate it 
        bpy.ops.object.editmode_toggle()
        bpy.context.scene.objects.active = objectname
        bpy.context.object.constraints["Follow Path"].target = pathname
        bpy.context.object.constraints["Follow Path"].use_curve_follow = True
        bpy.context.object.constraints["Follow Path"].forward_axis = 'TRACK_NEGATIVE_Y'
        
        override={'constraint':objectname.constraints["Follow Path"]}
        bpy.ops.constraint.followpath_path_animate(override,constraint='Follow Path')
        
        #reselect the path
        bpy.context.scene.objects.active = pathname
        bpy.ops.object.editmode_toggle()        

        return {'FINISHED'}


def menu_item(self, context):
       self.layout.operator(fastpath.bl_idname, text="fastpath", icon="CURVE_DATA")
       
       
def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_curve_add.append(menu_item)

    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_curve_add.remove(menu_item)

if __name__ == "__main__":
    register()
