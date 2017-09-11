'''
Copyright (C) 2016 Cedric Lepiller
pitiwazou@hotmail.com

Created by Cedric Lepiller

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
    "name": "Booleans Sculpt",
    "description": "",
    "author": "Cedric Lepiller",
    "version": (0, 0, 2),
    "blender": (2, 77, 1),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Tools" }
    

import bpy
from bpy.props import (StringProperty, 
                       BoolProperty, 
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty)

##------------------------------------------------------  
#
# Preferences
#
##------------------------------------------------------  

## Addons Preferences Update Panel
def update_panel(self, context):
    try:
        bpy.utils.unregister_class(BooleanSculptMenu)
    except:
        pass
    BooleanSculptMenu.bl_category = context.user_preferences.addons[__name__].preferences.category
    bpy.utils.register_class(BooleanSculptMenu)   
    
    
class BooleanAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
        
    prefs_tabs = EnumProperty(
        items=(('info', "Info", "Info"),
               ('links', "Links", "Links")),
               default='info'
               )
               
    category = bpy.props.StringProperty(
            name="Category",
            description="Choose a name for the category of the panel",
            default="Tools",
            update=update_panel) 
                      
    def draw(self, context):
            layout = self.layout
            wm = bpy.context.window_manager
            
            
            row= layout.row(align=True)
            row.prop(self, "prefs_tabs", expand=True)
            if self.prefs_tabs == 'info':
                layout = self.layout
                
                box = layout.box()
                split = box.split()
                col = split.column()
                col.label(text="Change Category:")
                col = split.column(align=True)
                col.prop(self, "category", text="") 
                
                layout.separator() 
                
                layout.label("This addon is usefull to work with Dyntopo Objects")   
                layout.label("You can make booleans, adjust the Detail Size etc") 
                layout.label("You don't need any other addon to use this one") 
                
            if self.prefs_tabs == 'links':  
                layout.operator("wm.url_open", text="Booleans Sculpt on BlenderArtist Forum ").url = "https://blenderartists.org/forum/showthread.php?402842-Addon-Booleans-Sculpt"  
                layout.operator("wm.url_open", text="Booleans Sculpt on BlenderLounge Forum ").url = "http://blenderlounge.fr/forum/viewtopic.php?f=26&t=1652"  
                layout.separator() 
                layout.operator("wm.url_open", text="Asset Management").url = "https://gumroad.com/l/kANV"
                layout.operator("wm.url_open", text="Speedflow").url = "https://gumroad.com/l/speedflow"
                layout.separator() 
                layout.operator("wm.url_open", text="Pitiwazou.com").url = "http://www.pitiwazou.com/"
                layout.operator("wm.url_open", text="Wazou's Ghitub").url = "https://github.com/pitiwazou/Scripts-Blender"
                layout.operator("wm.url_open", text="BlenderLounge Forum").url = "http://blenderlounge.fr/forum/"      
##------------------------------------------------------  
#
# Funtions
#
##------------------------------------------------------  
bpy.types.WindowManager.smooth_mesh = BoolProperty(
    name="Smooth Update",
    description="Smooth mesh after boolean or prepare for Dyntopo",
    default=True)


bpy.types.WindowManager.subdivide_mesh = BoolProperty(
    name="Subdiv Update",
    description="Subdiv mesh after boolean or prepare for Dyntopo",
    default=True)

bpy.types.WindowManager.use_sharps = BoolProperty(
    name="Add Sharps",
    description="Add sharps Edge to the mesh",
    default=False)    
    
bpy.types.WindowManager.update_detail_flood_fill = BoolProperty(
    name="Update Detail Flood Fill",
    description="Add Detail Flood Fill to the whole mesh",
    default=True)    
    
bpy.types.WindowManager.detail_size = bpy.props.FloatProperty(min = 0.01, max = 300, default = 20)

backup_obj = {} 


##------------------------------------------------------  
#
# Enable Dyntopo
#
##------------------------------------------------------  
class EnableDyntopo(bpy.types.Operator):  
    bl_idname = "enable.dyntopo"  
    bl_label = "Enable Dyntopo" 
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.sculpt.dynamic_topology_toggle()
        bpy.context.scene.tool_settings.sculpt.detail_refine_method = 'SUBDIVIDE_COLLAPSE'
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
        bpy.context.scene.tool_settings.sculpt.use_smooth_shading = True
        return {'FINISHED'} 

##------------------------------------------------------  
#
# Update Dyntopo
#
##------------------------------------------------------ 
class UpdateDyntopo(bpy.types.Operator):
    bl_idname = "object.update_dyntopo"
    bl_label = "Update Dyntopo"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        Detailsize = bpy.context.window_manager.detail_size
        WM = context.window_manager
        
        if bpy.context.object.mode == "SCULPT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.object.mode_set(mode = 'SCULPT')
            
            #Check Dyntopo
            if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
                pass
            else :
                bpy.ops.enable.dyntopo()
                
            #Update Detail size
            if WM.update_detail_flood_fill :  
                bpy.context.scene.tool_settings.sculpt.constant_detail = Detailsize       
                bpy.ops.sculpt.detail_flood_fill()
            else :
                pass
            
            #Smooth Mesh
            if WM.smooth_mesh :
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.modifier_add(type='SMOOTH')
                bpy.context.object.modifiers["Smooth"].factor = 1
                bpy.context.object.modifiers["Smooth"].iterations = 2
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")
                bpy.ops.object.mode_set(mode = 'SCULPT')
            
            #Check Dyntopo
            if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
                pass
            else :
                bpy.ops.enable.dyntopo()
            bpy.ops.sculpt.optimize()
        
        elif bpy.context.object.mode == "OBJECT":
            sel=bpy.context.selected_objects
            for x in sel:
                bpy.ops.object.select_all(action='DESELECT') #deselect all objects
            
                #select current object
                bpy.context.scene.objects.active=x
                x.select=True
                
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                #Add Sharps
                if WM.use_sharps:
                    bpy.ops.object.mode_set(mode = 'OBJECT') 
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.mesh.edges_select_sharp(sharpness=0.523599)
                    bpy.ops.transform.edge_crease(value=1)
                    bpy.ops.object.mode_set(mode = 'SCULPT')
                
                #Subdiv Mesh
                if WM.subdivide_mesh :
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.ops.object.modifier_add(type='SUBSURF')
                    bpy.context.object.modifiers["Subsurf"].levels = 2
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
                    bpy.ops.object.mode_set(mode = 'SCULPT')
                
                #Check Dyntopo
                bpy.ops.object.mode_set(mode = 'SCULPT')
                if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
                    pass
                else :
                    bpy.ops.enable.dyntopo()
                  
                #Update Detail Flood fill
                if WM.update_detail_flood_fill :  
                    bpy.context.scene.tool_settings.sculpt.constant_detail = Detailsize       
                    bpy.ops.sculpt.detail_flood_fill()
                else :
                    pass
                
                bpy.ops.sculpt.optimize()
                #Smooth Mesh
                if WM.smooth_mesh :
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.ops.object.modifier_add(type='SMOOTH')
                    bpy.context.object.modifiers["Smooth"].factor = 1
                    bpy.context.object.modifiers["Smooth"].iterations = 2
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")
                    bpy.ops.object.mode_set(mode = 'SCULPT')
                    
                 
                #Comme back to Object mode
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.mode_set(mode='EDIT') 
                bpy.ops.object.mode_set(mode = 'OBJECT')      

            for x in sel:    
                x.select=True

        return {"FINISHED"}
        

##------------------------------------------------------  
#
# Symmetrize
#
##------------------------------------------------------   
class Symmetrize(bpy.types.Operator):
    bl_idname = "object.symmetrize_x"
    bl_label = "Symmetrize X"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        Detailsize = bpy.context.window_manager.detail_size
        WM = context.window_manager
        toolsettings = context.tool_settings
        sculpt = toolsettings.sculpt
        
        #Sculpt
        if bpy.context.object.mode == "SCULPT":
            bpy.ops.sculpt.symmetrize()
            
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.mode_set(mode = 'SCULPT')
            
            #Update Detail Flood fill
            if WM.update_detail_flood_fill :  
                bpy.context.scene.tool_settings.sculpt.constant_detail = Detailsize       
                bpy.ops.sculpt.detail_flood_fill()
            else :
                pass
            
            bpy.ops.sculpt.optimize()
            
            #Smooth Mesh
            if WM.smooth_mesh :
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.modifier_add(type='SMOOTH')
                bpy.context.object.modifiers["Smooth"].factor = 1
                bpy.context.object.modifiers["Smooth"].iterations = 2
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")
                bpy.ops.object.mode_set(mode = 'SCULPT')
            
        #Object    
        elif bpy.context.object.mode == "OBJECT":
            sel=bpy.context.selected_objects
            for x in sel:
                bpy.ops.object.select_all(action='DESELECT') #deselect all objects
            
                #select current object
                bpy.context.scene.objects.active=x
                x.select=True
                
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_all(action='TOGGLE')
                bpy.ops.mesh.symmetrize(direction='POSITIVE_X')
                bpy.ops.object.mode_set(mode = 'OBJECT')
                
                
                    
                #Update Detail Flood fill
                if WM.update_detail_flood_fill :  
                    bpy.ops.object.mode_set(mode = 'SCULPT')
                    #Check Dyntopo
                    if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
                        pass
                    else :
                        bpy.ops.enable.dyntopo()
                        
                    bpy.context.scene.tool_settings.sculpt.constant_detail = Detailsize       
                    bpy.ops.sculpt.detail_flood_fill()
                    bpy.ops.sculpt.optimize()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                else :
                    pass
                
                #Smooth Mesh
                if WM.smooth_mesh :
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    bpy.ops.object.modifier_add(type='SMOOTH')
                    bpy.context.object.modifiers["Smooth"].factor = 1
                    bpy.context.object.modifiers["Smooth"].iterations = 2
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")
                
            for x in sel:    
                x.select=True
                
        return {"FINISHED"}


##------------------------------------------------------  
#
# Boolean Union
#
##------------------------------------------------------      
class BooleanSculptUnion(bpy.types.Operator):
    bl_idname = "object.boolean_sculpt_union"
    bl_label = "Boolean Union"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        WM = context.window_manager
        Detailsize = bpy.context.window_manager.detail_size
        
        #Boolean         
        actObj = context.active_object
        for selObj in bpy.context.selected_objects:
            
            if selObj != context.active_object and(selObj.type == "MESH"):
                actObj = context.active_object
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                newMod = actObj.modifiers.new("Boolean"+ selObj.name,"BOOLEAN")
                newMod.operation = 'UNION'
                newMod.object = selObj
                bpy.ops.object.modifier_apply (modifier=newMod.name)
                bpy.ops.object.select_all(action='DESELECT')
                selObj.select = True
                bpy.ops.object.delete()
                actObj.select=True
        
        #Add Sharps
        if WM.use_sharps:
            bpy.ops.object.mode_set(mode = 'OBJECT') 
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.edges_select_sharp(sharpness=0.523599)
            bpy.ops.transform.edge_crease(value=1)  
                    
        #Add subsurf modifier
        if WM.subdivide_mesh :
            bpy.ops.object.mode_set(mode = 'OBJECT') 
            bpy.ops.object.modifier_add(type='SUBSURF')
            bpy.context.object.modifiers["Subsurf"].levels = 2
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
        else:
            pass
        
        
        #Check Dyntopo
        bpy.ops.object.mode_set(mode = 'SCULPT')
        if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
            pass
        else :
            bpy.ops.enable.dyntopo()
          
        #Update Detail Flood fill
        if WM.update_detail_flood_fill :  
            bpy.context.scene.tool_settings.sculpt.constant_detail = Detailsize       
            bpy.ops.sculpt.detail_flood_fill()
        else :
            pass
        
        bpy.ops.sculpt.optimize()
        
        #Smooth Mesh
        if WM.smooth_mesh :
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_add(type='SMOOTH')
            bpy.context.object.modifiers["Smooth"].factor = 1
            bpy.context.object.modifiers["Smooth"].iterations = 2
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")
            bpy.ops.object.mode_set(mode = 'SCULPT')
        
        #Comme back to Object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
            
        return {"FINISHED"}


##------------------------------------------------------  
#
# Boolean Difference
#
##------------------------------------------------------  
class BooleanSculptDifference(bpy.types.Operator):
    bl_idname = "object.boolean_sculpt_difference"
    bl_label = "Boolean Difference"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        WM = context.window_manager
        Detailsize = bpy.context.window_manager.detail_size
        
        #Boolean         
        actObj = context.active_object
        for selObj in bpy.context.selected_objects:
            
            if selObj != context.active_object and(selObj.type == "MESH"):
                actObj = context.active_object
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                newMod = actObj.modifiers.new("Boolean"+ selObj.name,"BOOLEAN")
                newMod.operation = 'DIFFERENCE'
                newMod.object = selObj
                bpy.ops.object.modifier_apply (modifier=newMod.name)
                bpy.ops.object.select_all(action='DESELECT')
                selObj.select = True
                bpy.ops.object.delete()
                actObj.select=True
        
        #Add Sharps
        if WM.use_sharps:
            bpy.ops.object.mode_set(mode = 'OBJECT') 
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.edges_select_sharp(sharpness=0.523599)
            bpy.ops.transform.edge_crease(value=1)  
                    
        #Add subsurf modifier
        if WM.subdivide_mesh :
            bpy.ops.object.mode_set(mode = 'OBJECT') 
            bpy.ops.object.modifier_add(type='SUBSURF')
            bpy.context.object.modifiers["Subsurf"].levels = 2
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
        else:
            pass
        
        
        #Check Dyntopo
        bpy.ops.object.mode_set(mode = 'SCULPT')
        if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
            pass
        else :
            bpy.ops.enable.dyntopo()
          
        #Update Detail Flood fill
        if WM.update_detail_flood_fill :  
            bpy.context.scene.tool_settings.sculpt.constant_detail = Detailsize       
            bpy.ops.sculpt.detail_flood_fill()
        else :
            pass
        
        bpy.ops.sculpt.optimize()
        
        #Smooth Mesh
        if WM.smooth_mesh :
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_add(type='SMOOTH')
            bpy.context.object.modifiers["Smooth"].factor = 1
            bpy.context.object.modifiers["Smooth"].iterations = 2
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")
            bpy.ops.object.mode_set(mode = 'SCULPT')
        
        #Comme back to Object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
       
        return {"FINISHED"}


##------------------------------------------------------  
#
# Boolean Rebool
#
##------------------------------------------------------          
class BooleanSculptRebool(bpy.types.Operator):
    bl_idname = "object.boolean_sculpt_rebool"
    bl_label = "Boolean Rebool"
    bl_description = "Slice object in 2 parts"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        WM = context.window_manager
        Detailsize = bpy.context.window_manager.detail_size
        #First Object
        act_obj = context.active_object
        #Booleal Object
        bool_obj = bpy.context.selected_objects[0] if bpy.context.selected_objects[0] != act_obj else bpy.context.selected_objects[1]
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
            #Duplicate, inverse, apply
            obj.select=False
            act_obj.select=True
            bpy.ops.object.duplicate_move()
            bpy.context.active_object.name = "rebool"
            bpy.context.object.modifiers[len(bpy.context.object.modifiers)-1].name="rebool"
            bpy.context.object.modifiers["rebool"].operation = 'INTERSECT'
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier='rebool')
            obj.select=False
            act_obj.select=True
            bpy.context.scene.objects.active = act_obj 
            #Use the Union for the Operation
            object.modifiers[bool_name].operation = 'DIFFERENCE'
            #Apply the Boolean
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Boolean')
            #unselect All
            bpy.ops.object.select_all(action='DESELECT')
            #Select Bool object and delete it
            bool_obj.select=True
            bool_obj = bpy.ops.object.delete(use_global=False)    
            #Select Act Object and make it active object
            bpy.data.objects['rebool'].select = True
            act_obj.select=True
            bpy.context.scene.objects.active = act_obj 
        

            #Smooth/Update
            sel=bpy.context.selected_objects
            for x in sel:
                bpy.ops.object.select_all(action='DESELECT') #deselect all objects
            
                #select current object
                bpy.context.scene.objects.active=x
                x.select=True
               
                #editmode select sharp edges mean crease to hold edges
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.edges_select_sharp(sharpness=0.7)
                bpy.ops.transform.edge_crease(value=1)
                bpy.ops.object.mode_set(mode = 'OBJECT')
                
                #Add subsurf modifier
                if WM.subdivide_mesh :
                    bpy.ops.object.modifier_add(type='SUBSURF')
                    bpy.context.object.modifiers["Subsurf"].levels = 2
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
                else:
                    pass
                
                #Go to sculpt mode dyntopo
                bpy.ops.sculpt.sculptmode_toggle()
                if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
                    pass
                else :
                    bpy.ops.enable.dyntopo()
                
                #Update Detail Flood fill
                if WM.update_detail_flood_fill :  
                    bpy.context.scene.tool_settings.sculpt.constant_detail = Detailsize   
                    bpy.ops.sculpt.detail_flood_fill()
                else :
                    pass
                
                bpy.ops.sculpt.optimize()
                
                #Comme back to Object mode
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.mode_set(mode='EDIT') 
                bpy.ops.object.mode_set(mode = 'OBJECT')
        
        return {"FINISHED"}

##------------------------------------------------------  
#
# Create Curve
#
##------------------------------------------------------        
class CreateCurve(bpy.types.Operator):
    bl_idname = "object.create_curve"
    bl_label = "Create Curve"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        saved_location = bpy.context.scene.cursor_location.copy()
        bpy.ops.view3d.cursor3d('INVOKE_DEFAULT')
        
        #Create Vertex
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=2.59374)
        bpy.ops.mesh.remove_doubles()

        bpy.ops.object.mode_set(mode='OBJECT')  

        bpy.ops.object.convert(target='CURVE')
        bpy.context.object.data.show_normal_face = False


        bpy.ops.object.mode_set(mode='EDIT') 
        bpy.ops.curve.select_all(action='TOGGLE')
        bpy.ops.curve.select_all(action='TOGGLE')
        
        bpy.ops.curve.de_select_first()
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.curve.select_all(action='TOGGLE')

        bpy.ops.curve.spline_type_set(type='BEZIER')
        bpy.ops.curve.handle_type_set(type='AUTOMATIC')

        if bpy.context.space_data.use_occlude_geometry == True :
            bpy.context.space_data.use_occlude_geometry = False
        else :
            pass
        
        bpy.ops.transform.translate('INVOKE_DEFAULT')
        
        bpy.context.scene.cursor_location = saved_location 
        return {"FINISHED"}

##------------------------------------------------------  
#
# Prepare Curve
#
##------------------------------------------------------   
def PrepareCurve():
    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.mode_set(mode='EDIT')  
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_all(action='TOGGLE')


    bpy.ops.mesh.edge_face_add()
    bpy.ops.mesh.f2()

    bpy.ops.object.mode_set(mode='OBJECT')  
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].use_even_offset = True
    bpy.context.object.modifiers["Solidify"].offset = 0
    bpy.context.object.modifiers["Solidify"].thickness = 10
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify")


##------------------------------------------------------  
#
# Cut Boolean
#
##------------------------------------------------------       
class CutBoolean(bpy.types.Operator):
    bl_idname = "object.cut_boolean"
    bl_label = "Cut Boolean"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        
        act_obj = context.active_object
        
        bool_obj = bpy.context.selected_objects[0] if bpy.context.selected_objects[0] != act_obj else bpy.context.selected_objects[1]
        object = bpy.context.active_object
        
        obj_bool_list = [obj for obj in context.selected_objects if obj != object ]

        for obj in obj_bool_list:
#            obj.select=False
            act_obj.select=False
            #Select Bool object and delete it
            bool_obj.select=True
            bpy.context.scene.objects.active = bool_obj 
#            PrepareCurve()


            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.mode_set(mode='EDIT')  
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.mesh.edge_face_add()
#            bpy.ops.mesh.f2()

            bpy.ops.object.mode_set(mode='OBJECT')  
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].use_even_offset = True
            bpy.context.object.modifiers["Solidify"].offset = 0
            bpy.context.object.modifiers["Solidify"].thickness = 10
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify")
            
            
            act_obj.select=True
            bpy.context.scene.objects.active = act_obj
            
            bpy.ops.object.boolean_sculpt_difference()
        
        return {"FINISHED"}

##------------------------------------------------------  
#
# Cut Boolean Rebool
#
##------------------------------------------------------       
class CutBooleanRebool(bpy.types.Operator):
    bl_idname = "object.cut_boolean_rebool"
    bl_label = "Cut Boolean Rebool"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        
        act_obj = context.active_object
        
        bool_obj = bpy.context.selected_objects[0] if bpy.context.selected_objects[0] != act_obj else bpy.context.selected_objects[1]
        object = bpy.context.active_object
        
        obj_bool_list = [obj for obj in context.selected_objects if obj != object ]

        for obj in obj_bool_list:
#            obj.select=False
            act_obj.select=False
            #Select Bool object and delete it
            bool_obj.select=True
            bpy.context.scene.objects.active = bool_obj 
#            PrepareCurve
            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.mode_set(mode='EDIT')  
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.mesh.edge_face_add()
#            bpy.ops.mesh.f2()

            bpy.ops.object.mode_set(mode='OBJECT')  
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].use_even_offset = True
            bpy.context.object.modifiers["Solidify"].offset = 0
            bpy.context.object.modifiers["Solidify"].thickness = 10
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify")
            
            act_obj.select=True
            bpy.context.scene.objects.active = act_obj
            
            bpy.ops.object.boolean_sculpt_rebool()
        
        return {"FINISHED"}               
                
##------------------------------------------------------  
#
# UI
#
##------------------------------------------------------ 
class BooleanSculptMenu(bpy.types.Panel):
    bl_idname = "boolean_sculpt_menu"
    bl_label = "Booleans Sculpt"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        WM = context.window_manager
        toolsettings = context.tool_settings
        sculpt = toolsettings.sculpt
        
        if len(context.selected_objects) >= 1 :
            #Detail Size
            row = layout.row(align=True)
            row.scale_x = 0.5
            row.prop(WM, "detail_size", text="Detail Size")
            row.scale_x = 1.2
            row.operator("object.update_dyntopo", text="", icon='FILE_TICK')

            
            if not bpy.context.object.mode == 'SCULPT':  
                layout.prop(WM, "subdivide_mesh", text="Subdivide")
                if WM.subdivide_mesh:
                    layout.prop(WM, "use_sharps", text="Sharp Edges")
            layout.prop(WM, "smooth_mesh", text="Smooth")
            layout.prop(WM, "update_detail_flood_fill", text="Update Detail Flood Fill")
            
            
            layout.separator()
            
            #boolean
            if len([obj for obj in context.selected_objects if obj.type == 'MESH']) > 1:
                    split = layout.split()
                    col = split.column(align=True)
                    col.operator("object.boolean_sculpt_union", text="Union", icon='MOD_BOOLEAN')
                    col.operator("object.boolean_sculpt_difference", text="Difference", icon='MOD_BOOLEAN')
                    col.operator("object.boolean_sculpt_rebool", text="Rebool", icon='MOD_BOOLEAN')
            else:
                    pass
            
            #Symmetrize
            if bpy.context.object.mode == 'SCULPT':  
                layout.prop(sculpt, "symmetrize_direction")
            layout.operator("object.symmetrize_x", text="Symmetrize", icon='UV_ISLANDSEL')
            
            
            #Curve
            if len(context.selected_objects) == 1 :
                layout.operator("object.create_curve", text="Create Curve", icon='OUTLINER_OB_CURVE')
                
            if [obj for obj in context.selected_objects if obj.type == 'CURVE']:  
                split = layout.split()
                col = split.column(align=True)
                col.operator("object.cut_boolean", text="Cut", icon='MOD_BOOLEAN')
                col.operator("object.cut_boolean_rebool", text="Cut Rebool", icon='MOD_BOOLEAN')  
    
        else:
            layout.label("No object selected", icon='ERROR')    
def register():
    bpy.utils.register_module(__name__)
    
    update_panel(None, bpy.context)   

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
        