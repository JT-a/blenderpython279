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
    "name": "Mocap Fcurve Editor Quick Tools",
    "description": "Quick access tools - editing fcurves for facial mocap.",
    "author": "Joel Daniels",
    "version": (0,1),
    "blender": (2, 6, 7),
    "location": "Graph Editor > UI",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"}


import bpy

class FCURVE_OT_QuickX(bpy.types.Operator):
    bl_label = "X Location"
    bl_idname = "fcurve_quicktools.x_loc"
    bl_description = "Show only X location fcurves for selected objects"
    
    def execute(self, context):
        try:
            action = context.object.animation_data.action
            selected_objects = context.selected_objects
        
            for object in selected_objects:
                if object.type != 'ARMATURE':
                    if object.animation_data.action != None:
                        for fcurve in object.animation_data.action.fcurves:
                            if fcurve.array_index == 0:
                                fcurve.hide = False
                                fcurve.select = True
                            else:
                                fcurve.hide = True
                                fcurve.select = False
                    else:
                        print(object.name, "has no animation data! Doing nothing.")
                elif object.type == 'ARMATURE':
                    selected_bones = [str(bone).split('"')[1] for bone in context.selected_pose_bones]
                    for fcurve in object.animation_data.action.fcurves:
                        bone_name = fcurve.data_path.split('"')[1]
                        if bone_name in selected_bones:
                            if fcurve.array_index == 0:
                                fcurve.hide = False
                                fcurve.select = True
                            else:
                                fcurve.hide = True
                                fcurve.select = False 
        except:
            pass 
        
        return {'FINISHED'}
#------------------------------------------------------------------

class FCURVE_OT_QuickY(bpy.types.Operator):
    bl_label = "Y Location"
    bl_idname = "fcurve_quicktools.y_loc"
    bl_description = "Show only Y location fcurves for selected objects"
    
    def execute(self, context):
        try:
            action = context.object.animation_data.action
            selected_objects = context.selected_objects
        
            for object in selected_objects:
                if ojbect.type != 'ARMATURE':    
                    if object.animation_data.action != None:
                        for fcurve in object.animation_data.action.fcurves:
                            if fcurve.array_index == 1:
                                fcurve.hide = False
                                fcurve.select = True
                            else:
                                fcurve.hide = True
                                fcurve.select = False
                    else:
                        print(object.name, "has no animation data! Doing nothing.")
                elif object.type == 'ARMATURE':
                    selected_bones = [str(bone).split('"')[1] for bone in context.selected_pose_bones]
                    for fcurve in object.animation_data.action.fcurves:
                        bone_name = fcurve.data_path.split('"')[1]
                        if bone_name in selected_bones:
                            if fcurve.array_index == 1:
                                fcurve.hide = False
                                fcurve.select = True
                            else:
                                fcurve.hide = True
                                fcurve.select = False
        except:
            pass
        
        return {'FINISHED'}    

#------------------------------------------------------------------
class FCURVE_OT_QuickZ(bpy.types.Operator):
    bl_label = "Z Location"
    bl_idname = "fcurve_quicktools.z_loc"
    bl_description = "Show only Z location fcurves for selected objects"
    
    def execute(self, context):
        try:
            selected_objects = context.selected_objects
            for object in selected_objects:
                if object.type != 'ARMATURE':
                    if object.animation_data.action != None:
                        for fcurve in object.animation_data.action.fcurves:
                            if fcurve.array_index == 2:
                                fcurve.hide = False
                                fcurve.select = True
                            else:
                                fcurve.hide = True
                                fcurve.select = False
                elif object.type == 'ARMATURE':
                    selected_bones = [str(bone).split('"')[1] for bone in context.selected_pose_bones]
                    for fcurve in object.animation_data.action.fcurves:
                        bone_name = fcurve.data_path.split('"')[1]
                        if bone_name in selected_bones:
                            if fcurve.array_index == 2:
                                fcurve.hide = False
                                fcurve.select = True
                            else:
                                fcurve.hide = True
                                fcurve.select = False
                    
                        
                    else:
                        print(object.name, "has no animation data! Doing nothing.") 
        except:
            pass
        
        return {'FINISHED'}   
#----------------------------------------------------------------
class GRAPH_EDITOR_OT_HideAll(bpy.types.Operator):
    bl_label = "Hide All Curves"
    bl_idname = "fcurve_quicktools.hideall"
    bl_description = "Hide all fcurves in the graph editor"
    
    def execute(self, context):
        scene = context.scene
        selected_objects = context.selected_objects
        for object in selected_objects:
                if object.animation_data.action != None:
                    for fcurve in object.animation_data.action.fcurves:
                        fcurve.hide = True
                        fcurve.select = False
                else:
                    print(object.name, "has no animation data! Doing nothing.") 
                        
        return {'FINISHED'}
    
#------------------------------------------------------------------
        
        
    
class FCURVE_OT_DeleteY(bpy.types.Operator):
    bl_label = "Delete Y Location Fcurves"
    bl_idname = "fcurve_quicktools.y_delete"
    bl_description = "Delete Y location fcurves for selected objects"
    
    def execute(self, context):
        try:
            selected_objects = context.selected_objects
        
            for object in selected_objects:
                if object.animation_data.action != None:
                    for fcurve in object.animation_data.action.fcurves:
                        if fcurve.array_index == 1:
                            fcurve.hide = False
                            bpy.ops.graph.select_all_toggle(invert=False)
                            bpy.ops.graph.delete()
                    
                    else:
                        continue
                else:
                    print(object.name, "has no animation data! Doing nothing.") 
        except:
            pass
        
        return {'FINISHED'}  
    
    
#--------------------------------------------

class FCURVE_OT_CursorToCurve(bpy.types.Operator):
    bl_label = "Cursor to First Frame"
    bl_idname = "fcurve_quicktools.cursormove"
    bl_description = "Center cursor at first keyframe of current curve"
    
    def execute(self, context):
        scene = context.scene
        action = context.active_object.animation_data.action
        
        if action is not None:
            for fcurve in action.fcurves:
                if fcurve.hide == False:
                    frame_val = fcurve.keyframe_points[0].co.y
                    frame_num = fcurve.keyframe_points[0].co.x
                    #Put 2D cursor at first key in current fcurve's animation
                    bpy.ops.graph.cursor_set(frame=frame_num, value=frame_val)
                elif fcurve.hide == True:
                    pass
        
        
        return {'FINISHED'}
    
    
class FCURVE_OT_CopyCurve(bpy.types.Operator):
    bl_label = "Copy Fcurve"
    bl_idname = "fcurve_quicktools.fcurvecopy"
    bl_description = "Copy the active fcurve"
    
    def execute(self, context):
        try:
            scene = context.scene
            action = context.active_object.animation_data.action
            
            bpy.ops.graph.select_all_toggle(invert=False)
            bpy.ops.graph.copy()
        except RuntimeError:
            self.report({'INFO'}, "Please deselect all fcurves in graph editor. Doing nothing.")    
        return {'FINISHED'}
            
#----------------------------------------------------------------
class FCURVE_OT_PasteToZero(bpy.types.Operator):
    bl_label = "Paste Curve to Zero Y"
    bl_idname = "fcurve_quicktools.pastetozero"
    bl_description = "Paste the copied curve to the bone's default location. NOTICE: Make sure you only have desired fcurve visible!"
    
    def execute(self, context):
        scene = context.scene
        selected_bone_list = [str(bone).split('"')[1] for bone in context.selected_pose_bones]
        
#        try:
        bpy.ops.graph.paste(offset='NONE', merge='OVER_ALL')
#            if context.space_data.cursor_position_y != 0.0:
#                move_dist = -(context.space_data.cursor_position_y)
#                bpy.ops.transform.translate(value=(0, move_dist, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.0323491, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=False)
#        except RuntimeError:
#            self.report({'INFO'}, "Please deselect all fcurves in graph editor.")
        for fcurve in context.object.animation_data.action.fcurves:
            if fcurve.hide == False:
                bone_name = fcurve.data_path.split('"')[1]
                if bone_name in selected_bone_list:
                    if fcurve.keyframe_points[0].co.y != 0.0:
                        move_dist = -(fcurve.keyframe_points[0].co.y)
                        for point in fcurve.keyframe_points:
                            point.co.y += move_dist
                            point.handle_left.y += move_dist
                            point.handle_right.y += move_dist                        
                 
        return {'FINISHED'}
        
#--------------------------------------------------------------
class GRAPH_EDITOR_OT_FlipCurves(bpy.types.Operator):
    bl_idname = "fcurve_quicktools.flipcurves"
    bl_label = "Flip Fcurves"
    bl_description = "Flip X and Y fcurves on selected bones"
    
    def execute(self, context):
        scene = context.scene
        
        rig_name = context.object.name
        #a list of the names of selected bones
        selected_bone_list = [str(bone).split('"')[1] for bone in context.selected_pose_bones]
        
        
        if context.object.type == 'ARMATURE':    

            for fcurve in scene.objects[rig_name].animation_data.action.fcurves:
                #if fcurve.array_index == 0 or 1:
                bone_name = fcurve.data_path.split('"')[1]
                if bone_name in selected_bone_list:
                    if fcurve.hide == False:
                        for point in fcurve.keyframe_points:
                            point.co.y *= -1
                            point.handle_left.y *= -1   
                            point.handle_right.y *= -1 

                    else:
                        continue
                else:
                    continue
        #Make them visible for user to see updated curves
        #bpy.ops.anim.channels_select_all_toggle()
        #bpy.ops.anim.channels_visibility_toggle()
        
        return {'FINISHED'}
#---------------------------------------------------------------------------
    
class VIEW_PT_Quicktools_Panel(bpy.types.Panel):
    bl_label = "Mocap Quick Tools"
    bl_space_type = "GRAPH_EDITOR"
    bl_region_type = "UI"
    
    @classmethod
    def poll(self, context):
        return context.object is not None

    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row(align=True)
        row.operator("fcurve_quicktools.x_loc")
        
        layout.operator("fcurve_quicktools.y_loc")

        layout.operator("fcurve_quicktools.z_loc")
        
        layout.separator()
        layout.operator("fcurve_quicktools.hideall")
        
        layout.separator()

        layout.operator("fcurve_quicktools.cursormove", icon = "CURSOR")
        
        row = layout.row()
        row.operator("fcurve_quicktools.fcurvecopy")
        row.operator("fcurve_quicktools.pastetozero")
        
        layout.operator("fcurve_quicktools.flipcurves", icon = "ARROW_LEFTRIGHT")
        
        layout.separator()

        layout.operator("fcurve_quicktools.y_delete", icon='ERROR')
        

def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()
        