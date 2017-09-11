'''
Copyright (C) 2017 
 
Created by Rob Moore.
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
 
 
bl_info = {
    "name": "BoolCut",
    "description": "BoolCut1",
    "author": "Rob Moore",
    "version": (0, 0, 1),
    "blender": (2, 78,0 ),
    "location": "View3D > Toolshelf",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Tools" }




import bpy

class BooleanCutout(bpy.types.Operator):
    bl_idname = "object.boolean_cutout"
    bl_label = "Boolean_removal"
    bl_description = "Boolean, remove joint region"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        #First Object
        act_obj = context.active_object
        #Booleal Object
        bool_obj = bpy.context.selected_objects[0] if bpy.context.selected_objects[0] !=  act_obj else bpy.context.selected_objects[1]
        object = bpy.context.active_object
        #Create a list
        obj_bool_list = [obj for obj in context.selected_objects if obj != object and obj.type == 'MESH']

        for obj in obj_bool_list:

            #Add name to the future boolean
            bool_name = "Boolean"
            #Create the boolean with the name
            object.modifiers.new(bool_name, 'BOOLEAN')
            #Add second object as object reference
            object.modifiers[bool_name].object = obj
            #Use the Union for the Operation
            object.modifiers[bool_name].operation = 'UNION'
            #Apply the Boolean
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Boolean')
            #unselect first Object
            act_obj.select=False



            #Select Bool object and delete it
            bool_obj.select=True
            bpy.ops.object.delete(use_global=False)

            #Select Act Object and make it active object
            act_obj.select=True
            bpy.context.scene.objects.active = act_obj
            #Remove unwanted area.
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.delete(type='FACE')
        
            return {"FINISHED"}


class BooleanCutoff(bpy.types.Operator):
    bl_idname = "object.boolean_cutoff"
    bl_label = "Boolean_removal"
    bl_description = "Boolean, remove joint region"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        #First Object
        act_obj = context.active_object
        #Booleal Object
        bool_obj = bpy.context.selected_objects[0] if bpy.context.selected_objects[0] !=  act_obj else bpy.context.selected_objects[1]
        object = bpy.context.active_object
        #Create a list
        obj_bool_list = [obj for obj in context.selected_objects if obj != object and obj.type == 'MESH']

        for obj in obj_bool_list:

            #Add name to the future boolean
            bool_name = "Boolean"
            #Create the boolean with the name
            object.modifiers.new(bool_name, 'BOOLEAN')
            #Add second object as object reference
            object.modifiers[bool_name].object = obj
            #Use the Union for the Operation
            object.modifiers[bool_name].operation = 'INTERSECT'
            #Apply the Boolean
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Boolean')
            #unselect first Object
            act_obj.select=False



            #Select Bool object and delete it
            bool_obj.select=True
            bpy.ops.object.delete(use_global=False)

            #Select Act Object and make it active object
            act_obj.select=True
            bpy.context.scene.objects.active = act_obj
            #Remove unwanted area.
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.delete(type='FACE')
        
            return {"FINISHED"}
        
        
class BooleanSculptMenu(bpy.types.Panel):
    bl_idname = "boolean_Removal_menu"
    bl_label = "Boolean joint Removal"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout

        layout.operator("object.boolean_cutout", text="Boolean Cutoff", icon='MOD_BOOLEAN')
        layout.operator("object.boolean_cutoff", text="Boolean Cutout", icon='MOD_BOOLEAN')
        
def register():
    bpy.utils.register_module(__name__)
 
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()