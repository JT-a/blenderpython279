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
    "name": "TP Display Selections",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy
from bpy import *


class VIEW3D_TP_Display_Selection(bpy.types.Menu):
    bl_label = "Selections [ALT+Q]"
    bl_idname = "tp_display.menu_selection"   

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'
     

        ob = context
        if ob.mode == 'OBJECT':

            layout.operator("view3d.select_circle", icon ="BORDER_LASSO")
            layout.operator("view3d.select_border", icon ="BORDER_RECT")

            layout.separator()
              
            layout.operator("object.select_all")             

            layout.separator()

            layout.operator("object.select_linked", text="Linked", icon = "LINKED") 
            layout.operator("object.select_grouped", text="Group")        
            layout.operator("object.select_by_type", text="Type")        

            layout.separator()

            layout.operator("object.select_by_layer", text="Layer", icon = "SEQ_SEQUENCER")
            layout.operator("object.select_pattern", text="Name")
            layout.operator("object.select_camera", text="Camera")

            layout.separator()

            layout.operator("object.select_random", text="Random", icon = "RNDCURVE")            
            layout.operator("object.select_all", text="Inverse").action = 'INVERT'
            layout.operator("object.select_mirror", text="Mirror")
            


        if ob.mode == 'EDIT_MESH':

            layout.operator("view3d.select_circle", icon ="BORDER_LASSO")
            layout.operator("view3d.select_border", icon ="BORDER_RECT")

            layout.separator()
                          
            layout.operator("mesh.select_all") 
            layout.menu("tp_display.selection_modes") 
            
            layout.separator()
        
            layout.operator("mesh.select_linked",text="Linked", icon = "LINKED")
            layout.operator("mesh.select_similar",text="Similar")              
            layout.operator("mesh.select_all", text="Inverse").action = 'INVERT'  

            layout.separator()
            
            layout.operator("mesh.select_axis", text="Active Side", icon = "SNAP_FACE")                        
            layout.operator("mesh.select_face_by_sides",text="Face by Side")
            layout.operator("mesh.faces_select_linked_flat", text="Linked Faces")
            
            layout.separator()
            
            layout.operator("mesh.select_nth") 

            layout.separator()                        
            
            layout.operator("mesh.loop_multi_select",text="Edge Loop", icon="ZOOMOUT").ring=False          
            layout.operator("mesh.loop_multi_select",text="Edge Ring", icon="COLLAPSEMENU").ring=True

            layout.separator()
            
            layout.operator("mesh.select_loose",text="Loose", icon="STICKY_UVS_DISABLE")
            layout.operator("meshlint.select", "Meshlint")

            if context.scene.tool_settings.mesh_select_mode[2] is False:
                layout.operator("mesh.select_non_manifold", text="Non Manifold")  
            layout.operator("mesh.select_interior_faces", text="Interior Faces") 

            
            layout.separator()
            layout.operator("mesh.edges_select_sharp", text="Sharp", icon="SNAP_EDGE")                          
            layout.operator("mesh.select_random", text="Random")
                                                    
            layout.separator()

            layout.operator("mesh.region_to_loop", text = "Edge Boundry Loop")
            layout.operator("mesh.loop_to_region", text = "Edge Loop Inner-Region")
                               


        if ob.mode == 'EDIT_CURVE':
            
            layout.operator("view3d.select_circle", icon ="BORDER_LASSO")
            layout.operator("view3d.select_border", icon ="BORDER_RECT")

            layout.separator()
                          
            layout.operator("curve.select_all").action = 'TOGGLE'            

            layout.separator()

            layout.operator("curve.select_linked", text="Linked", icon = "LINKED") 
            layout.operator("curve.select_all", text="Inverse").action = 'INVERT'
            layout.operator("curve.select_nth",text="Nth Selected") 
            layout.operator("curve.select_random") 
            
            layout.separator()

            layout.operator("curve.de_select_first", text = "Select First", icon = "TRIA_UP") 
            layout.operator("curve.de_select_last", text = "Select Last", icon = "TRIA_DOWN") 
    
            layout.separator()
                        
            layout.operator("curve.select_next", icon = "TRIA_RIGHT") 
            layout.operator("curve.select_previous", icon = "TRIA_LEFT") 

            layout.separator()

            layout.operator("curve.select_more", text="More", icon="ZOOMIN") 
            layout.operator("curve.select_less", text="Less", icon="ZOOMOUT")


       
        if ob.mode == 'EDIT_SURFACE':
            
            layout.operator("view3d.select_circle", icon ="BORDER_LASSO")
            layout.operator("view3d.select_border", icon ="BORDER_RECT")

            layout.separator()
                          
            layout.operator("curve.select_all").action = 'TOGGLE'            

            layout.separator()

            layout.operator("curve.select_linked", text="Linked", icon = "LINKED") 
            layout.operator("curve.select_all", text="Inverse").action = 'INVERT'
            layout.operator("curve.select_nth",text="Nth Selected") 
            layout.operator("curve.select_random") 
            
            layout.separator()

            layout.operator("curve.select_more", text="More", icon="ZOOMIN") 
            layout.operator("curve.select_less", text="Less", icon="ZOOMOUT")



        if ob.mode == 'EDIT_METABALL':
            
            layout.operator("view3d.select_circle", icon ="BORDER_LASSO")
            layout.operator("view3d.select_border", icon ="BORDER_RECT")

            layout.separator()
                          
            layout.operator("mball.select_all").action = 'TOGGLE'
            
            layout.separator()
            
            layout.operator_menu_enum("mball.select_similar", "type", text="Similar") 
            layout.operator("mball.select_all", text="Inverse").action = 'INVERT'
            layout.operator("mball.select_random_metaelems") 


   
        if ob.mode == 'EDIT_LATTICE':
            
            layout.operator("view3d.select_circle", icon ="BORDER_LASSO")
            layout.operator("view3d.select_border", icon ="BORDER_RECT")

            layout.separator()
                          
            layout.operator("lattice.select_all").action = 'TOGGLE'
            
            layout.separator()

            layout.operator("lattice.select_mirror", text="Mirror", icon = "ARROW_LEFTRIGHT")
            layout.operator("lattice.select_all", text="Inverse").action = 'INVERT'
            layout.operator("lattice.select_random") 

            layout.separator()

            layout.menu("vgroupmenu", icon="GROUP_VERTEX")   
            
            layout.separator()

            layout.operator("lattice.select_ungrouped", text="Ungrouped Verts")
            
                 

        if  context.mode == 'PARTICLE':
       
            layout.operator("view3d.select_border", icon ="BORDER_RECT")

            layout.separator()
            
            layout.operator("particle.select_all", icon="RESTRICT_SELECT_OFF").action = 'TOGGLE'

            layout.separator()

            layout.operator("particle.select_tips", text = "Tips", icon = "IPO_EASE_OUT")  
            layout.operator("particle.select_roots", text = "Roots")

            layout.separator()

            layout.operator("particle.select_linked", text="Linked", icon = "LINKED") 
            layout.operator("particle.select_all", text="Inverse").action = 'INVERT'

            layout.separator()

            layout.operator("particle.select_more", text="More", icon="ZOOMIN")
            layout.operator("particle.select_less", text="Less", icon="ZOOMOUT")


        if ob.mode == 'EDIT_ARMATURE':

            arm = context.active_object.data 

            layout.operator("view3d.select_circle", icon ="BORDER_LASSO")
            layout.operator("view3d.select_border", icon ="BORDER_RECT")

            layout.separator()
                          
            layout.operator("armature.select_all").action = 'TOGGLE'
            
            layout.separator()
            
            layout.operator("armature.select_mirror", text="Mirror", icon = "ARROW_LEFTRIGHT").extend = False
            layout.operator("armature.select_all", text="Inverse").action = 'INVERT'

            layout.separator()

            layout.operator("armature.select_hierarchy", text="Parent", icon="BONE_DATA").direction = 'PARENT'
 
            props = layout.operator("armature.select_hierarchy", text="Extend Parent")
            props.extend = True
            props.direction = 'PARENT'
                        
            layout.operator("armature.select_hierarchy", text="Child", icon="CONSTRAINT_BONE").direction = 'CHILD'

            props = layout.operator("armature.select_hierarchy", text="Extend Child")
            props.extend = True
            props.direction = 'CHILD'

            layout.separator()  

            layout.operator_menu_enum("armature.select_similar", "type", text="Similar")
            layout.operator("object.select_pattern", text="Select Pattern...")
            
            layout.separator()

            layout.operator("armature.select_more", text="More", icon="ZOOMIN")
            layout.operator("armature.select_less", text="Less", icon="ZOOMOUT")
            

        if context.mode == 'POSE':

            arm = context.active_object.data   
    
            layout.operator("view3d.select_circle", icon ="BORDER_LASSO")
            layout.operator("view3d.select_border", icon ="BORDER_RECT")

            layout.separator()
                        
            layout.operator("pose.select_all").action = 'TOGGLE'
            
            layout.separator()

            layout.operator("pose.select_all", text="Inverse").action = 'INVERT'
            layout.operator("pose.select_mirror", text="Flip Active")
            layout.operator("pose.select_constraint_target", text="Constraint Target", icon ="LINK_AREA")
            layout.operator("pose.select_linked", text="CONSTRAINT_BONE", icon="CONSTRAINT") 

            layout.separator()

            layout.operator("pose.select_hierarchy", text="Parent", icon ="BONE_DATA").direction = 'PARENT'
            props = layout.operator("pose.select_hierarchy", text="Extend Parent")
            props.extend = True
            props.direction = 'PARENT'
            
            layout.separator()
                                    
            layout.operator("pose.select_hierarchy", text="Child", icon ="CONSTRAINT_BONE").direction = 'CHILD'

            props = layout.operator("pose.select_hierarchy", text="Extend Child")
            props.extend = True
            props.direction = 'CHILD'

            layout.separator()

            layout.operator_menu_enum("pose.select_grouped", "type", text="Grouped", icon ="GROUP_BONE")
            layout.operator("object.select_pattern", text="Select Pattern...")
            



class TP_Display_Selection_Modes(bpy.types.Menu):
    bl_label = "Selection Modes"
    bl_idname = "tp_display.selection_modes"   
    
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        prop = layout.operator("wm.context_set_value", text="Vertex Select", icon='VERTEXSEL')
        prop.value = "(True, False, False)"
        prop.data_path = "tool_settings.mesh_select_mode"

        prop = layout.operator("wm.context_set_value", text="Edge Select", icon='EDGESEL')
        prop.value = "(False, True, False)"
        prop.data_path = "tool_settings.mesh_select_mode"

        prop = layout.operator("wm.context_set_value", text="Face Select", icon='FACESEL')
        prop.value = "(False, False, True)"
        prop.data_path = "tool_settings.mesh_select_mode"
        
        layout.separator()

        prop = layout.operator("wm.context_set_value", text="Vertex & Edge Select", icon='EDITMODE_HLT')
        prop.value = "(True, True, False)"
        prop.data_path = "tool_settings.mesh_select_mode"

        prop = layout.operator("wm.context_set_value", text="Vertex & Face Select", icon='ORTHO')
        prop.value = "(True, False, True)"
        prop.data_path = "tool_settings.mesh_select_mode"

        prop = layout.operator("wm.context_set_value", text="Edge & Face Select", icon='SNAP_FACE')
        prop.value = "(False, True, True)"
        prop.data_path = "tool_settings.mesh_select_mode"
        layout.separator()

        prop = layout.operator("wm.context_set_value", text="Vertex & Edge & Face Select", icon='SNAP_VOLUME')
        prop.value = "(True, True, True)"
        prop.data_path = "tool_settings.mesh_select_mode"

bpy.utils.register_class(TP_Display_Selection_Modes)  



def register():
    
    bpy.utils.register_class(VIEW3D_TP_Display_Selection)    

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name='3D View', space_type ='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.menu_selection" 

                
def unregister():
    
    bpy.utils.unregister_class(VIEW3D_TP_Display_Selection)    
           
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps['3D View']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break


if __name__ == "__main__":
    register() 	

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_Selection.bl_idname)
  
  
           

















