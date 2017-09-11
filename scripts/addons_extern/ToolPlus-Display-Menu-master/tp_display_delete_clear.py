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
    "name": "TP Display Curve & Surface",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }



import bpy, re
from bpy import *


                                                

def draw_delete_history_tools(context, layout):
    settings = context.tool_settings
    layout.operator_context = 'INVOKE_REGION_WIN'

    # Special Menu
    layout.operator("screen.repeat_last", icon ="FF") 
    layout.operator("ed.undo_history", icon ="REW") 



class VIEW3D_TP_Display_Delete(bpy.types.Menu):
    bl_label = "Delete [X]"
    bl_idname = "tp_display.delete_clear"   
   
    def draw(self, context):
        layout = self.layout
        
        ob = context       
        if ob.mode == 'OBJECT':
                           
            layout.operator("object.delete", "Delete Selected", icon = "PANEL_CLOSE")
                 
            layout.separator()                                     
                        
            layout.menu("clearup", text="Clear Up", icon = "DISCLOSURE_TRI_RIGHT_VEC") 
            
            layout.separator()           
   
            layout.menu("VIEW3D_MT_object_showhide", "Hide / Show", icon = "VISIBLE_IPO_ON")
                                  
            layout.separator()

            draw_delete_history_tools(context, layout)


        elif ob.mode == 'EDIT_MESH':

            layout.operator("mesh.delete", "Vertices", icon="SNAP_VERTEX").type="VERT"
            layout.operator("mesh.dissolve_verts")
            layout.operator("mesh.remove_doubles")

            layout.separator()
            
            layout.operator("mesh.delete", "Edges", icon="SNAP_EDGE").type="EDGE"
            layout.operator("mesh.dissolve_edges")
            layout.operator("mesh.delete_edgeloop", text="Remove Edge Loop")
            
            layout.separator()
            
            layout.operator("mesh.delete", "Faces", icon="SNAP_FACE").type="FACE"
            layout.operator("mesh.dissolve_faces")
            layout.operator("mesh.delete", "Remove only Faces").type="ONLY_FACE"            
            
            
            layout.separator()

            layout.operator("mesh.dissolve_limited", icon="MATCUBE")		
            layout.operator("mesh.dissolve_degenerate")
            layout.operator("mesh.delete", "Remove Edge & Faces").type="EDGE_FACE"
            
            layout.separator() 
                        
            layout.menu("cleanup", text="Clean Up Mesh", icon = "RIGHTARROW_THIN") 
            
            layout.separator() 
                        
            layout.operator("mesh.reveal", text="Clear Hide", icon = "RESTRICT_VIEW_OFF") 
                      
            layout.separator()

            draw_delete_history_tools(context, layout)
            
               
        if ob.mode == 'EDIT_CURVE':

            layout.operator("curve.delete", "Vertices", icon="PARTICLE_TIP").type="VERT"
            layout.operator("curve.delete", "Segment", icon="IPO_EASE_IN_OUT").type="SEGMENT"

            layout.separator() 
                        
            layout.operator("curve.reveal", text="Clear Hide", icon = "RESTRICT_VIEW_OFF")            

            layout.separator()

            draw_delete_history_tools(context, layout)
                                                
       
        if ob.mode == 'EDIT_SURFACE':

            layout.operator("curve.delete", "Vertices", icon="PARTICLE_TIP").type="VERT"
            layout.operator("curve.delete", "Segments", icon="IPO_EASE_IN_OUT").type="SEGMENT"

            layout.separator() 
                        
            layout.operator("curve.reveal", text="Clear Hide", icon = "RESTRICT_VIEW_OFF") 
     
            layout.separator()

            draw_delete_history_tools(context, layout)

                
        if ob.mode == 'EDIT_METABALL':
           
            layout.operator("mball.delete_metaelems", icon="META_BALL")

            layout.separator() 
            
            layout.operator("mball.reveal_metaelems", text="Clear Hide", icon = "RESTRICT_VIEW_OFF") 
            
            layout.separator()

            draw_delete_history_tools(context, layout)
            
         
        elif ob.mode == 'EDIT_LATTICE':

            draw_delete_history_tools(context, layout)
            
           
        if  context.mode == 'PARTICLE':

            layout.operator("particle.delete")

            layout.separator()

            layout.operator("particle.remove_doubles")
            
            layout.separator()

            layout.menu("VIEW3D_MT_particle_showhide", text = "Clear Hide", icon = "RESTRICT_VIEW_OFF")                        
            
            layout.separator()

            draw_delete_history_tools(context, layout)                 

                   
        ob = context  
        if ob.mode == 'PAINT_WEIGHT':

            draw_delete_history_tools(context, layout)           

                                    
        elif ob.mode == 'PAINT_VERTEX':           

            draw_delete_history_tools(context, layout)

                       
        elif ob.mode == 'PAINT_TEXTURE':
            
            draw_delete_history_tools(context, layout)
            
                        
        elif ob.mode == 'SCULPT':
             
            props = layout.operator("paint.hide_show", text="Clear All Hide", icon = "RESTRICT_VIEW_OFF")
            props.action = 'SHOW'
            props.area = 'ALL'
            
            layout.separator()

            draw_delete_history_tools(context, layout)
            
     
        elif ob.mode == 'EDIT_ARMATURE':
            
            layout.operator("armature.delete", text = "Selected Bone(s)", icon = "RIGHTARROW_THIN")

            layout.separator()
            
            layout.operator("sketch.delete", text = "Sketch Delete", icon = "RIGHTARROW_THIN")  
            
            layout.separator()
                         
            layout.operator("armature.parent_clear", icon = "RIGHTARROW_THIN").type='CLEAR'

            layout.separator()

            draw_delete_history_tools(context, layout)

            
        if context.mode == 'POSE':
            arm = context.active_object.data 

            layout.operator("anim.keyframe_clear_v3d", text = "Clear Keyframe")
            layout.operator("pose.paths_clear", text = "Clear Motion Path")

            layout.separator()

            layout.menu("VIEW3D_MT_pose_transform", text="Clear Location")  
            layout.menu("clearparent", text="Clear Parenting")
            layout.operator("pose.constraints_clear", text="Clear Constraint")            

            layout.separator()
              
            layout.operator("pose.reveal", text = "Clear Hide", icon = "RESTRICT_VIEW_OFF") 

            layout.separator()

            draw_delete_history_tools(context, layout)

                 

class CLEANUP(bpy.types.Menu):
    bl_label = "Clean Up Mesh"
    bl_idname = "cleanup"
    
    def draw(self, context):
        layout = self.layout
             
        layout.label("Clean Up")
        
        layout.separator()        
            
        layout.operator("mesh.fill_holes") 
        layout.operator("mesh.delete_loose")

        layout.operator("mesh.edge_collapse")            
                   
        layout.separator()

        layout.operator("mesh.tris_convert_to_quads", icon="OUTLINER_OB_LATTICE")
        layout.operator("mesh.quads_convert_to_tris", icon="OUTLINER_OB_MESH")
        layout.operator("mesh.vert_connect_nonplanar", icon="OUTLINER_OB_MESH")

bpy.utils.register_class(CLEANUP)



class CLEARUP(bpy.types.Menu):
    bl_label = "Clear Up"
    bl_idname = "clearup"
    
    def draw(self, context):
        layout = self.layout
             
        layout.label("Clear Up")
        
        layout.separator()                         
        
        layout.menu("VIEW3D_MT_object_clear", text="Clear Location", icon='EMPTY_DATA')

        layout.separator()

        layout.operator("material.remove", text="Clear Materials")

        layout.separator()
                    
        layout.menu("clearparent", text="Clear Parenting", icon='CONSTRAINT')
        layout.menu("cleartrack", text="Clear Tracking")
        layout.operator("object.constraints_clear", text="Clear Constraint")

        layout.separator()
        layout.operator("anim.keyframe_clear_v3d", text = "Clear Keyframe", icon='KEY_DEHLT')                        
        layout.operator("object.game_property_clear")            

bpy.utils.register_class(CLEARUP)


class CLEARPARENT(bpy.types.Menu):
    bl_label = "Clear Parenting"
    bl_idname = "clearparent"
        
    def draw(self, context):
        layout = self.layout
        
        layout.operator_enum("object.parent_clear", "type")
        
bpy.utils.register_class(CLEARPARENT)


class CLEARTRACK(bpy.types.Menu):
    bl_label = "Clear Tracking"
    bl_idname = "cleartrack"
       
    def draw(self, context):
        layout = self.layout
        
        layout.operator_enum("object.track_clear", "type")
        
bpy.utils.register_class(CLEARTRACK)


class deleteMat(bpy.types.Operator):
    """delete materials with an value slider"""
    bl_idname = "material.remove"
    bl_label = "Delete all Material"
    bl_options = {'REGISTER', 'UNDO'}

    deleteMat = bpy.props.IntProperty(name="Delete all Material", description="How many times?", default=100, min=1, soft_max=5000, step=1)
    
    def execute(self, context):        
        for i in range(self.deleteMat):      
            bpy.ops.object.material_slot_remove()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)  

bpy.utils.register_class(deleteMat)


def register():
     
    bpy.utils.register_class(VIEW3D_TP_Display_Delete)  
   
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'X', 'PRESS')
        kmi.properties.name = "tp_display.delete_clear"



def unregister():

    bpy.utils.unregister_class(VIEW3D_TP_Display_Delete)    

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
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_Delete.bl_idname)
  
  
           


















