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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****


import bpy, math, bmesh
from bpy.props import *
from bpy.types import Operator, AddonPreferences
from mathutils import Vector


class View3D_TP_Objects_To_Selected_Faces(bpy.types.Operator):
    """Copy Objects to selected Faces / press Props twice for douple, again for single"""
    bl_idname = "tp_ops.copy_to_selected_faces"
    bl_label = "Copy to Faces"
    bl_options = {"REGISTER", 'UNDO'}

    set_origin = bpy.props.BoolProperty(name="Origin to Bottom",  description="SetOrigin to Bottom", default = False)       
    dupli = bpy.props.BoolProperty(name="Duplicate",  description="Duplicate", default = False)       
    dupli_linked = bpy.props.BoolProperty(name="Duplicate Linked",  description="Duplicate Linked", default = True)      
    set_edit = bpy.props.BoolProperty(name="Target to Editmode",  description="Set Target to Editmode", default = False)   
    set_edit_linked = bpy.props.BoolProperty(name="Linked to Editmode",  description="Set Linked to Editmode", default = True)   

    def draw(self, context):
        layout = self.layout
                
        
        if self.dupli_linked == True:        
            layout.prop(self, 'dupli_linked', text="Duplicate Linked")
        else:    
            layout.prop(self, 'dupli', text="Duplicate Unlinked")   
            layout.prop(self, 'set_origin', text="Origin to Bottom") 
        
        if self.set_edit_linked == True:              
            layout.prop(self, 'set_edit_linked', text="Linked to Editmode")
        else:
            layout.prop(self, 'set_edit', text="Target to Editmode")
        
        row = layout.row()
        row.operator('wm.operator_defaults', text="Reset", icon ="RECOVER_AUTO")


    def execute(self, context):
        obj = context.active_object
   
        bpy.context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'

        bpy.ops.object.mode_set(mode='OBJECT')

        if len(bpy.context.selected_objects) > 1:

            first_obj = bpy.context.active_object

            obj_a, obj_b = context.selected_objects

            second_obj = obj_a if obj_b == first_obj else obj_b  

            bpy.data.objects[second_obj.name].select = False 

            if context.mode == 'EDIT_MESH': 

                print(self)
                self.report({'INFO'}, "Please select a source and a target object")  

            else: 
                    
                bpy.ops.object.duplicate_move()

                for i in range(self.set_origin):
                    bpy.ops.object.cubefront_side_minus_z()       
                
                bpy.context.active_object.name = "Dummy"
               
                bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')    

                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                        
                copy_cursor = bpy.context.scene.cursor_location.copy()     
         
                bm = bmesh.new()
                bm.from_mesh(obj.data)

                selected_faces = [f for f in bm.faces if f.select]
         
                for face in selected_faces:
         
                    face_location = face.calc_center_median()
         
                    loc_world_space = obj.matrix_world * Vector(face_location)
         
                    z = Vector((0,0,1))
         
                    angle = face.normal.angle(z)
         
                    axis = z.cross(face.normal)
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    
                    bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]
                    
                    bpy.data.objects[second_obj.name].select=True
                    
                    for i in range(self.dupli_linked):                                     
                        bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'})

                    for i in range(self.dupli):                    
                        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'})
                                            
                        for i in range(self.set_origin):
                            bpy.ops.tp_ops.cubefront_side_minus_z()              
                   
                    bpy.context.scene.cursor_location = loc_world_space
                    bpy.ops.view3d.snap_selected_to_cursor()
         
                    bpy.ops.transform.rotate(value=angle, axis=axis)

         
                bm.to_mesh(obj.data) 
                bm.free()
         
                bpy.context.scene.cursor_location = copy_cursor
                
                bpy.ops.object.select_all(action='DESELECT')
                
                bpy.context.scene.objects.active = bpy.data.objects["Dummy"]         
                bpy.data.objects["Dummy"].select = True

                bpy.ops.object.delete(use_global=False)
                                     
                bpy.ops.object.select_all(action='DESELECT')
                
                bpy.context.scene.objects.active = bpy.data.objects[second_obj.name]
                
                bpy.data.objects[second_obj.name].select=True


                for i in range(self.set_edit):

                    bpy.context.scene.objects.active = bpy.data.objects[first_obj.name]
                    bpy.ops.object.mode_set(mode='EDIT')        
                    
                    print(self)
                    self.report({'INFO'}, "Editmode")
      
 
        else:
            print(self)
            self.report({'INFO'}, "Please select a source and a target object")         
        
                
        return {"FINISHED"}


class View3D_Tp_Origin_CubeFront_Side_Minus_Z(bpy.types.Operator):  
    bl_idname = "tp_ops.cubefront_side_minus_z"  
    bl_label = "Origin to -Z Edge / Bottom of Cubefront"  
  
    def execute(self, context):
        if context.mode == 'OBJECT':         
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.z
                     init=1
                 elif x.co.z<a:
                     a=x.co.z
                     
            for x in o.data.vertices:
                 x.co.z-=a
                             
            o.location.z+=a                   
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o=bpy.context.active_object
            init=0
            for x in o.data.vertices:
                 if init==0:
                     a=x.co.z
                     init=1
                 elif x.co.z<a:
                     a=x.co.z
                     
            for x in o.data.vertices:
                 x.co.z-=a
                             
            o.location.z+=a                   
            bpy.ops.object.mode_set(mode = 'EDIT')
        
            
        return {'FINISHED'}




class View3D_TP_Copy_2_Cursor_Panel(bpy.types.Operator):
    """Copy selected object to cursor direction"""
    bl_idname = "tp_ops.copy_to_cursor_panel"
    bl_label = "Copy 2 Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    bpy.types.Scene.ctc_total = bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)

    ctc_unlink = bpy.props.BoolProperty(name="Unlink Copies", description ="Unlink Copies" , default = False)
    ctc_join = bpy.props.BoolProperty(name="Join Copies", description ="Join Copies" , default = False)


    def draw(self, context):
        layout = self.layout.column(1)

        box = layout.box().column(1)
        
        row = box.column(1)        
        row.prop(self, 'ctc_join', text="Join")
        row.label("or")
        row.prop(self, 'ctc_unlink', text="Unlink")


    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor_location
        obj = scene.objects.active

        for i in range(context.scene.ctc_total):
            obj_new = obj.copy()
            scene.objects.link(obj_new)

            factor = i / scene.ctc_total
            obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

        if self.ctc_join == True:
            bpy.ops.object.select_linked(type='OBDATA') 
            bpy.ops.object.join()

        if self.ctc_unlink == True: 
            bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)

        return {'FINISHED'}

class View3D_TP_Copy_2_Cursor(bpy.types.Operator):
    """Copy selected object to cursor direction"""
    bl_idname = "tp_ops.copy_to_cursor"
    bl_label = "Copy 2 Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    total = bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)
    unlink = bpy.props.BoolProperty(name="Unlink Copies", description ="Unlink Copies" , default = False)
    join = bpy.props.BoolProperty(name="Join Copies", description ="Join Copies" , default = False)

    def draw(self, context):
        layout = self.layout.column(1)

        box = layout.box().column(1)
        
        row = box.column(1)        
        row.prop(self, 'total', text="Steps")

        row = box.row(1) 
        row.prop(self, 'join', text="Join")
        row.label("or")
        row.prop(self, 'unlink', text="Unlink")


    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor_location
        obj = scene.objects.active

        for i in range(self.total):
            obj_new = obj.copy()
            scene.objects.link(obj_new)

            factor = i / self.total
            obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

        if self.join == True:
            bpy.ops.object.select_linked(type='OBDATA') 
            bpy.ops.object.join()

        if self.unlink == True: 
            bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)





# Mifth Tools > Author: Paul Geraskin > Version (2, 71, 0)
class View3D_TP_Curve_Radial_Clone(bpy.types.Operator):
    """Radial Clone"""
    bl_idname = "curve_mft.radialclone"
    bl_label = "Radial Clone"
    bl_description = "Radial Clone"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    radialClonesAngle = FloatProperty(default = 360.0, min = -360.0, max = 360.0)
    clonez = IntProperty(default = 8, min = 2, max = 300)
    single = bpy.props.BoolProperty(name="Unlink",  description="Unlink Clones", default=False)    
    join = bpy.props.BoolProperty(name="Join",  description="Join Clones", default=False)    
    edit = bpy.props.BoolProperty(name="Edit",  description="Editmode", default=False)    

    def draw(self, context):
        layout = self.layout
        box = layout.box().column(1)   

        row = box.column(1) 
        row.prop(self, "radialClonesAngle")
        row.prop(self, "clonez")
        
        row = box.row(1)         
        row.prop(self, "single")
        row.prop(self, "join")
        row.prop(self, "edit")

    def execute(self, context):

        if len(bpy.context.selected_objects) > 0:
            activeObj = bpy.context.scene.objects.active
            selObjects = bpy.context.selected_objects
            mifthTools = bpy.context.scene.mifthTools
            activeObjMatrix = activeObj.matrix_world

            for i in range(self.clonez - 1):
                bpy.ops.object.duplicate(linked=True, mode='DUMMY')
                theAxis = None

                if mifthTools.radialClonesAxis == 'X':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][0], activeObjMatrix[1][0], activeObjMatrix[2][0])
                    else:
                        theAxis = (1, 0, 0)

                elif mifthTools.radialClonesAxis == 'Y':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][1], activeObjMatrix[1][1], activeObjMatrix[2][1])
                    else:
                        theAxis = (0, 1, 0)

                elif mifthTools.radialClonesAxis == 'Z':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][2], activeObjMatrix[1][2], activeObjMatrix[2][2])
                    else:
                        theAxis = (0, 0, 1)
                
                rotateValue = (math.radians(self.radialClonesAngle)/float(self.clonez))
                bpy.ops.transform.rotate(value=rotateValue, axis=theAxis)

            bpy.ops.object.select_all(action='DESELECT')

            for obj in selObjects:
                obj.select = True
            selObjects = None
            bpy.context.scene.objects.active = activeObj
        else:
            self.report({'INFO'}, "Select Objects!")

        for i in range(self.single):
            bpy.ops.object.select_linked(type='OBDATA')
            bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)

        for i in range(self.join):
            bpy.ops.object.select_linked(type='OBDATA')
            bpy.ops.object.join()
            
        for i in range(self.edit):
            bpy.ops.object.editmode_toggle()
               
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)



# Mifth Tools > Author: Paul Geraskin > Version (2, 71, 0)
class Curve_Radial_Clone_Panel(bpy.types.Operator):
    """Radial Clone"""
    bl_idname = "curve_mft.radialclone_panel"
    bl_label = "Radial Clone"
    bl_description = "Radial Clone"
    bl_options = {'REGISTER', 'UNDO'}

    bpy.types.Scene.radialClonesAngle = FloatProperty(default = 360.0, min = -360.0, max = 360.0)
    bpy.types.Scene.clonez = IntProperty(default = 2, min = 2, max = 300)

    rz_unlink = bpy.props.BoolProperty(name="Unlink",  description="Unlink Clones", default=False)  
    rz_join = bpy.props.BoolProperty(name="Join",  description="Join Clones", default=False)       
  

    def draw(self, context):
        layout = self.layout.column(1)

        box = layout.box().column(1)
        
        row = box.column(1)        
        row.prop(self, 'rz_join', text="Join")
        row.label("or")
        row.prop(self, 'rz_unlink', text="Unlink")
        

    def execute(self, context):
        scene = context.scene

        if len(bpy.context.selected_objects) > 0:
            activeObj = bpy.context.scene.objects.active
            selObjects = bpy.context.selected_objects
            mifthTools = bpy.context.scene.mifthTools
            activeObjMatrix = activeObj.matrix_world

            for i in range(scene.clonez - 1):
                bpy.ops.object.duplicate(linked=True, mode='DUMMY')
                theAxis = None

                if mifthTools.radialClonesAxis == 'X':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][0], activeObjMatrix[1][0], activeObjMatrix[2][0])
                    else:
                        theAxis = (1, 0, 0)

                elif mifthTools.radialClonesAxis == 'Y':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][1], activeObjMatrix[1][1], activeObjMatrix[2][1])
                    else:
                        theAxis = (0, 1, 0)

                elif mifthTools.radialClonesAxis == 'Z':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][2], activeObjMatrix[1][2], activeObjMatrix[2][2])
                    else:
                        theAxis = (0, 0, 1)
                
                rotateValue = (math.radians(scene.radialClonesAngle)/float(scene.clonez))
                bpy.ops.transform.rotate(value=rotateValue, axis=theAxis)

            bpy.ops.object.select_all(action='DESELECT')

            for obj in selObjects:
                obj.select = True
            selObjects = None
            bpy.context.scene.objects.active = activeObj
        else:
            self.report({'INFO'}, "Select Objects!")

        for i in range(self.rz_unlink):
            bpy.ops.object.select_linked(type='OBDATA')
            bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True)

        for i in range(self.rz_join):
            bpy.ops.object.select_linked(type='OBDATA')
            bpy.ops.object.join()

               
        return {'FINISHED'}




class MFTProperties(bpy.types.PropertyGroup):

    radialClonesAxis = EnumProperty(items = (('X', 'X', ''), ('Y', 'Y', ''), ('Z', 'Z', '')), default = 'Z')

    radialClonesAxisType = EnumProperty(items = (('Global', 'Global', ''),('Local', 'Local', '')), default = 'Global')



