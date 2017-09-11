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
    "name": "TP Display Armature",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }

import bpy, re
from bpy import *



class TP_Display_Special_Armature(bpy.types.Menu):
    bl_label = "Armature [CTRL+F]"
    bl_idname = "tp_display.special_armature"    

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

  
        ob = context
        if ob.mode == 'EDIT_ARMATURE':

            layout.operator("screen.redo_last", text="Settings", icon="SCRIPTWIN")
 
            layout.separator() 

            layout.menu("tp_display.armature_cut")           

            layout.separator()

            layout.operator("transform.transform", text="Scale Envelope Distance").mode = 'BONE_SIZE'
            layout.operator("transform.transform", text="Scale B-Bone Width").mode = 'BONE_SIZE'
            
            layout.separator()

            layout.operator("armature.extrude_move")
            layout.operator("armature.extrude_forked")

            layout.separator()

            layout.operator("armature.duplicate_move")
            layout.operator("armature.merge")
            layout.operator("armature.fill")
            layout.operator("armature.delete")
            layout.operator("armature.separate")

            layout.separator()
            layout.operator_context = 'EXEC_AREA'
            layout.operator("armature.symmetrize")
            layout.operator("armature.switch_direction", text="Switch Direction")

            layout.separator()     
                    
            layout.operator("armature.flip_names")
            layout.menu("tp_display.armature_name")            

            layout.separator() 

            layout.menu("VIEW3D_MT_edit_armature_parent")
            layout.menu("VIEW3D_MT_edit_armature_roll")

            layout.separator() 
            
            layout.operator_context = 'INVOKE_DEFAULT'
            layout.operator("armature.armature_layers")
            layout.operator("armature.bone_layers")
 
            layout.separator() 
             
            layout.menu("VIEW3D_MT_bone_options_toggle", text="Bone Settings")
        

        if context.mode == 'POSE':
            
            arm = context.active_object.data  

            layout.operator("screen.redo_last", text="Settings", icon="SCRIPTWIN")

            layout.separator()

            if arm.draw_type in {'BBONE', 'ENVELOPE'}:
                layout.operator("transform.transform", text="Scale Envelope Distance").mode = 'BONE_SIZE'            

            layout.menu("VIEW3D_MT_object_animation", icon = "SHAPEKEY_DATA")
            layout.menu("VIEW3D_MT_pose_propagate")
            layout.menu("VIEW3D_MT_pose_slide")
            layout.menu("tp_display.animation_player", text="Play Animation", icon = "TRIA_RIGHT") 
            layout.menu("VIEW3D_MT_object_specials", text = "Special Render", icon = "SCENE")
            
            layout.separator()

            layout.operator("pose.copy", icon = "COPYDOWN")
            layout.operator("pose.paste", icon = "PASTEDOWN")
            layout.operator("pose.paste", text="Paste X-Flipped Pose", icon = "PASTEFLIPDOWN").flipped = True

            layout.separator()

            layout.menu("VIEW3D_MT_pose_library", icon = "POSE_HLT")
            layout.menu("VIEW3D_MT_pose_motion")
            layout.menu("VIEW3D_MT_pose_group")

            layout.separator()

            layout.menu("VIEW3D_MT_object_parent", icon = "CONSTRAINT_BONE")
            layout.menu("VIEW3D_MT_pose_constraints")
            layout.menu("VIEW3D_MT_pose_ik")

            layout.separator()             
          
            layout.operator("pose.flip_names", icon = "ARROW_LEFTRIGHT")
            layout.operator("pose.quaternions_flip")
            layout.menu("tp_display.pose_name")
            
            layout.separator()             

            layout.operator_context = 'INVOKE_AREA'
            layout.operator("pose.bone_layers", text="Change Bone Layers...", icon = "NLA")
            layout.operator("armature.armature_layers",  text="Change Armature Layers...")

            layout.separator() 
                       
            layout.menu("VIEW3D_MT_bone_options_toggle",  text="Bone Settings", icon = "SCRIPTWIN")

            layout.separator() 
            

            layout.menu("VIEW3D_MT_pose_showhide")
            
            layout.separator()
             
            scene = context.scene            
            layout.prop(scene, "frame_current", text="Set Current Frame")






class TP_Display_Armature_Name(bpy.types.Menu):
    bl_label = "Armature Name"
    bl_idname = "tp_display.armature_name"
    
    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'EXEC_AREA'
        
        layout.operator("armature.autoside_names", text="AutoName Left/Right").type = 'XAXIS'
        layout.operator("armature.autoside_names", text="AutoName Front/Back").type = 'YAXIS'
        layout.operator("armature.autoside_names", text="AutoName Top/Bottom").type = 'ZAXIS'


bpy.utils.register_class(TP_Display_Armature_Name)



class TP_Display_Armature_Cut(bpy.types.Menu):
    bl_label = "Subdivide"
    bl_idname = "tp_display.armature_cut"
    
    def draw(self, context):
        layout = self.layout
  
        layout.operator("armature.subdivide",text="1 Cut").number_cuts=1
        layout.operator("armature.subdivide",text="2 Cut").number_cuts=2
        layout.operator("armature.subdivide",text="3 Cut").number_cuts=3
        layout.operator("armature.subdivide",text="4 Cut").number_cuts=4
        layout.operator("armature.subdivide",text="5 Cut").number_cuts=5
        layout.operator("armature.subdivide",text="6 Cut").number_cuts=6     

bpy.utils.register_class(TP_Display_Armature_Cut)



class TP_Display_Pose_Names(bpy.types.Menu):
    bl_label = "Pose Names"
    bl_idname = "tp_display.pose_name" 
    
    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'EXEC_AREA'
        layout.operator("pose.autoside_names", text="AutoName Left/Right").axis = 'XAXIS'
        layout.operator("pose.autoside_names", text="AutoName Front/Back").axis = 'YAXIS'
        layout.operator("pose.autoside_names", text="AutoName Top/Bottom").axis = 'ZAXIS'

bpy.utils.register_class(TP_Display_Pose_Names)



class TP_Display_Animation_Player(bpy.types.Menu):
    bl_label = "Animation Player"
    bl_idname = "tp_display.animation_player"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        toolsettings = context.tool_settings
        screen = context.screen

        layout.operator("screen.frame_jump", text="Jump REW", icon='REW').end = False
        layout.operator("screen.keyframe_jump", text="Previous FR", icon='PREV_KEYFRAME').next = False
        layout.operator("screen.animation_play", text="Reverse", icon='PLAY_REVERSE').reverse = True
        
        layout.operator("screen.animation_play", text="PLAY", icon='PLAY')
        
        layout.operator("screen.animation_play", text="Stop", icon='PAUSE')
        
        layout.operator("screen.keyframe_jump", text="Next FR", icon='NEXT_KEYFRAME').next = True
        layout.operator("screen.frame_jump", text="Jump FF", icon='FF').end = True    

bpy.utils.register_class(TP_Display_Animation_Player)




def register():

    bpy.utils.register_class(TP_Display_Special_Armature)
      
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Pose')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.special_armature"      

        km = kc.keymaps.new(name='Armature')
        kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', ctrl=True)
        kmi.properties.name = "tp_display.special_armature"



def unregister():

    bpy.utils.unregister_class(TP_Display_Special_Armature)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:

        km = kc.keymaps['Pose']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 
              
        km = kc.keymaps['Armature']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break 


if __name__ == "__main__":
    register() 	

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=TP_Display_Special_Armature.bl_idname)
  
  
  
   









































