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
#
# ***** END GPL LICENCE BLOCK *****


bl_info = {
    "name": "BBox Origin Setup",
    "author": "mkbreuer",
    "version": (0, 1, 0),
    "blender": (2, 7, 5),
    "location": "View3D",
    "description": "create bounding box or set origin to bounding box > 27 places like vertices on a cube subdivided by one",
    "warning": "",
    "wiki_url": "",
    "category": "User Interface"
}


import bpy
import mathutils
import math
import re
from mathutils.geometry import intersect_line_plane
from mathutils import Vector
from math import radians
from bpy import*

bpy.types.Scene.AutoAlign_axis = bpy.props.EnumProperty(items=[("x", "X", "", 1), ("y", "Y", "", 2), ("z", "Z", "", 3)], description="Axis used by the mirror modifier")


############----------------------############
############  Props for DROPDOWN  ############
############----------------------############

class DropdownBBoxToolProps(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.bboxwindow
    """
    display_bboxfront = bpy.props.BoolProperty(name="Front", description="9 Places for Origin on BBox Frontside / +Y", default=False)
    display_bboxmiddle = bpy.props.BoolProperty(name="Middle", description="9 Places for  Origin on BBox Middle / XYZ", default=False)
    display_bboxback = bpy.props.BoolProperty(name="Back", description="9 Places for  Origin on BBox Backside / -Y", default=False)

bpy.utils.register_class(DropdownBBoxToolProps)
bpy.types.WindowManager.bboxwindow = bpy.props.PointerProperty(type=DropdownBBoxToolProps)

"""
############  Objectmode Operator  ############
class BBOXSET(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_bbox_setup"
    bl_label = "BBox Origin Setup"    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    #bl_region_type = 'TOOLS'
    #bl_category = "BBox"       
    

    def draw(self, context):      
        lt = context.window_manager.bboxwindow
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        

        
        if context.mode == 'OBJECT':  
            row = layout.row(1)
            row.scale_y = 1.2
            row.operator("object.bounding_box",text="", icon="BBOX")  
            row.operator("object.bounding_boxers",text="Wire Bounding Box")  
            row.operator("object.align_tools", text="", icon="ROTATE")             


            box = layout.box()      
            row = box.row(1)      
            row.operator("object.mirror1",text="MX", icon='ARROW_LEFTRIGHT')
            row.operator("object.mirror2",text="MY", icon='ARROW_LEFTRIGHT')
            row.operator("object.mirror3",text="MZ", icon='ARROW_LEFTRIGHT') 
            
            obj = context.active_object

            if obj:
                obj_type = obj.type
                if obj_type in {'MESH', 'CURVE', 'SURFACE', 'ARMATURE', 'FONT', 'LATTICE'}:
                    box = layout.box()      
                    row = box.row()
                    row.alignment= "CENTER" 
                    row.scale_x = 1.25   
                    row.operator_menu_enum("object.origin_set", "type", text="Set Origin", icon='LAYER_ACTIVE')
                                         
                
                if obj_type in {'CURVE'}: 
                    box = layout.box()      
                    row = box.column(1)
                    row.alignment= "CENTER" 
                    row.scale_x = 1.25       
                    row.operator("curve.switch_direction_obm","Start & Direction" ,icon = "PARTICLE_TIP")      



        else:         
            box = layout.box()
            row = box.row(1)
            row.operator("origin.selected_edm","Origin EDM", icon = "LAYER_ACTIVE")  
            row.operator("origin.selected_obm","Origin OBM", icon = "LAYER_ACTIVE") 
             
            


        obj = context.active_object
        if obj:
            obj_type = obj.type

            if obj_type in {'MESH'}:    #{'MESH', 'CURVE', 'SURFACE', 'ARMATURE', 'FONT', 'LATTICE', 'META'}:


                if context.mode == 'OBJECT': 

                    box = layout.box()
                    row = box.column(1)
                    ###space1###

                    #col = layout.column(align=True)
                    if lt.display_bboxback:
                        row.scale_y = 1.2                  
                        row.prop(lt, "display_bboxback", text="Back -Y", icon='TRIA_DOWN')

                    else:
                        row.scale_y = 1.2            
                        row.prop(lt, "display_bboxback", text="Back -Y", icon='TRIA_RIGHT')

                    ###space1###
                    if lt.display_bboxback:
                         col = layout.column(align=True)  
                         box = col.column(align=True).box().column()
                         col_top = box.column(align=True)
                        
                         #Top
                         row = col_top.row(align=True)
                         row.alignment = 'CENTER'
                         row.scale_x = 1.55

                         row.operator("object.cubeback_cornertop_minus_xy", "", icon = "LAYER_ACTIVE")#"Back- Left -Top")
                         row.operator("object.cubeback_edgetop_minus_y", "", icon = "LAYER_ACTIVE")#"Back - Top")
                         row.operator("object.cubeback_cornertop_plus_xy","", icon = "LAYER_ACTIVE")# "Back- Right -Top ")
                         

                         #Middle
                         row = col_top.row(align=True)
                         row.alignment = 'CENTER'
                         row.scale_x = 1.55             
                         row.operator("object.cubefront_edgemiddle_minus_x","", icon = "LAYER_ACTIVE")#"Back- Left")
                         row.operator("object.cubefront_side_plus_y","", icon = "LAYER_ACTIVE")# "Back") 
                         row.operator("object.cubefront_edgemiddle_plus_x","", icon = "LAYER_ACTIVE")#"Back- Right")   
                         
                         #Bottom
                         row = col_top.row(align=True)
                         row.alignment = 'CENTER'
                         row.scale_x = 1.55
                         row.operator("object.cubeback_cornerbottom_minus_xy","", icon = "LAYER_ACTIVE")# "Back- Left -Bottom")
                         row.operator("object.cubefront_edgebottom_plus_y","", icon = "LAYER_ACTIVE")#"Back - Bottom") 
                         row.operator("object.cubeback_cornerbottom_plus_xy","", icon = "LAYER_ACTIVE")# "Back- Right -Bottom")  
                    
                         ##############################
                         col = layout.column(align=True)  
                         box = col.column(align=True).box().column()
                         col_top = box.column(align=True)
                         row = box.column(1)
               
                     
                    ###space1###

                    #col = layout.column(align=True)
                    if lt.display_bboxmiddle:
                        row.scale_y = 1.2                    
                        row.prop(lt, "display_bboxmiddle", text="Middle", icon='TRIA_DOWN')

                    else:
                        row.scale_y = 1.2
                        row.prop(lt, "display_bboxmiddle", text="Middle", icon='TRIA_RIGHT')


                    ###space1###
                    if lt.display_bboxmiddle:              
                         col = layout.column(align=True)  
                         box = col.column(align=True).box().column()
                         col_top = box.column(align=True)

                         #Top
                         row = col_top.row(align=True)
                         row.alignment = 'CENTER'
                         row.scale_x = 1.55

                         row.operator("object.cubefront_edgetop_minus_x","", icon = "LAYER_ACTIVE")#"Middle - Left Top")
                         row.operator("object.cubefront_side_plus_z", "", icon = "LAYER_ACTIVE")#"Top")
                         row.operator("object.cubefront_edgetop_plus_x","", icon = "LAYER_ACTIVE")#"Middle - Right Top")              

                         
                         #Middle
                         row = col_top.row(align=True)
                         row.alignment = 'CENTER'
                         row.scale_x = 1.55             
                          
                         row.operator("object.cubefront_side_minus_x","", icon = "LAYER_ACTIVE")# "Left")
                         obj = context.object
                         if obj and obj.mode == 'EDIT':          
                             row.operator("mesh.origincenter", text="", icon="LAYER_ACTIVE") 
                         else:
                             row.operator("object.origin_set", text="", icon="LAYER_ACTIVE").type='ORIGIN_GEOMETRY'            
                                         
                         row.operator("object.cubefront_side_plus_x","", icon = "LAYER_ACTIVE")# "Right")              
                    

                         #Bottom
                         row = col_top.row(align=True)
                         row.alignment = 'CENTER'
                         row.scale_x = 1.55            
                         
                         row.operator("object.cubefront_edgebottom_minus_x","", icon = "LAYER_ACTIVE")#"Middle - Left Bottom")
                         row.operator("object.cubefront_side_minus_z","", icon = "LAYER_ACTIVE")# "Bottom")             
                         row.operator("object.cubefront_edgebottom_plus_x","", icon = "LAYER_ACTIVE")#"Middle - Right Bottom")  

                         
                         ##############################
                         col = layout.column(align=True)  
                         box = col.column(align=True).box().column()
                         col_top = box.column(align=True)
                         row = col_top.row(align=True)
                       
                           

                    ###space1###

                    if lt.display_bboxfront:
                        row.scale_y = 1.2
                        row.prop(lt, "display_bboxfront", text="Front +Y", icon='TRIA_DOWN')

                    else:
                        row.scale_y = 1.2           
                        row.prop(lt, "display_bboxfront", text="Front +Y", icon='TRIA_RIGHT')

                    ###space1###
                    if lt.display_bboxfront:
                         col = layout.column(align=True)  
                         box = col.column(align=True).box().column()
                         col_top = box.column(align=True)
                        
                         #Top
                         row = col_top.row(align=True)
                         row.alignment = 'CENTER'
                         row.scale_x = 1.55
                                    
                         row.operator("object.cubefront_cornertop_minus_xy", "", icon = "LAYER_ACTIVE")# "Front- Left -Top"
                         row.operator("object.cubeback_edgetop_plus_y","", icon = "LAYER_ACTIVE")# "Front - Top"
                         row.operator("object.cubefront_cornertop_plus_xy","", icon = "LAYER_ACTIVE")#  "Front- Right -Top"
                        
                        
                         #Middle
                         row = col_top.row(align=True)
                         row.alignment = 'CENTER'
                         row.scale_x = 1.55
                                      
                         row.operator("object.cubefront_edgemiddle_minus_y","", icon = "LAYER_ACTIVE")# "Front- Left"       
                         row.operator("object.cubefront_side_minus_y","", icon = "LAYER_ACTIVE")#  "Front"           
                         row.operator("object.cubefront_edgemiddle_plus_y","", icon = "LAYER_ACTIVE")# "Front- Right"              


                         #Bottom
                         row = col_top.row(align=True)
                         row.alignment = 'CENTER'
                         row.scale_x = 1.55
                         
                         row.operator("object.cubefront_cornerbottom_minus_xy","", icon = "LAYER_ACTIVE")# "Front- Left -Bottom"                
                         row.operator("object.cubefront_edgebottom_minus_y","", icon = "LAYER_ACTIVE")# "Front - Bottom"
                         row.operator("object.cubefront_cornerbottom_plus_xy", "", icon = "LAYER_ACTIVE")# "Front- Right -Bottom") 
                         
        ###space1###
        if context.mode == 'OBJECT':   

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)                                                

            row = col_top.row(align=True)            
            row.prop(context.scene, "AutoAlign_axis", text="Align Axis", expand=True)
            row = col_top.row(align=True) 
            row.operator("bbox.align_vertices", text="Execute BoxCylinder")
      

            obj = context.active_object
            if obj:
                obj_type = obj.type

                if obj_type in {'MESH'}:  

                    col_top = box.column(align=True)         
                    col_top = box.column(align=True) 
                    row = col_top.row(align=True)                               
                    row.operator("bbox.bevel_a")        
                    row.operator("bbox.bevel_b")        
                    row.operator("bbox.bevel_c")  
                     
                    row = col_top.row(align=True)                
                    row.operator("bbox.bevel_d")        
                    row.operator("bbox.bevel_e")        
                    row.operator("bbox.bevel_f")          
                   
                    col_top = box.column(align=True)  
                    col_top = box.column(align=True)  
                    row = col_top.row(align=True)
                    row.operator("view3d.bevelmodifier_one", text="1")
                    row.operator("view3d.bevelmodifier_two", text="2")
                    row.operator("view3d.bevelmodifier_three", text="3")
                    row.operator("view3d.bevelmodifier_four", text="4")
                    row.operator("view3d.bevelmodifier_five", text="5")
                    row.operator("view3d.bevel_remove", text="", icon ="PANEL_CLOSE")
                    row.operator("view3d.bevel_apply", text="", icon ="FILE_TICK")

                    col = layout.column(align=True)
                    box = col.column(align=True).box().column()
                    col_top = box.column(align=True)                                                

                    row = col_top.row(align=True) 
                    row.operator("view3d.bbox_select","BBox", icon ="RESTRICT_SELECT_OFF")
                    row.operator("view3d.bbox_select_wire","WBox", icon ="RESTRICT_SELECT_OFF") 
                    row.operator("view3d.bbox_select_zyl","ZBox", icon ="RESTRICT_SELECT_OFF")  
                    row = col_top.column(align=True)
                    row.operator("mesh.removedouble", "Remove all Double", icon="PANEL_CLOSE") 
                    row.operator("view3d.rec_normals", icon="SNAP_NORMAL") 
                    row = col_top.row(align=True)
                    row.operator("objects.multiedit_enter_operator") 
                    row.prop(bpy.context.scene, "Preserve_Location_Rotation_Scale","",icon="NDOF_DOM")
                 
            box = layout.box()
            row = box.row(1)        
            row.prop(context.object, "show_bounds", text="Show Bounds", icon='STICKY_UVS_LOC') 
            sub = row.row(1)
            sub.scale_x = 0.5  
            sub.prop(context.object, "draw_bounds_type", text="") 
                   
        else:
            if context.mode == "EDIT_MESH":  

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)                                                

                row = col_top.row(align=True)  
                row.operator("bbox.circle_div", text="EvenDiv")
                row.operator("mesh.subdivide",text="< OddDiv").number_cuts=1

                row = col_top.row(align=True)                            
                row.operator("bbox.mirror_extrude_x","X")               
                row.operator("bbox.mirror_extrude_y","Y")               
                row.operator("bbox.mirror_extrude_z","Z")               
                row.operator("bbox.mirror_extrude_n","N")               

                col = layout.column(align=True)
                box = col.column(align=True).box().column()
                col_top = box.column(align=True)                                                

                row = col_top.row(align=True)               
                row.operator("mesh.normals_make_consistent", text="Recalc.", icon="SNAP_NORMAL")
                row.operator("mesh.flip_normals", text="Flip", icon="FILE_REFRESH")
                
                row = col_top.row(align=True)   
                row.operator("objects.multiedit_exit_operator")                               
                row.prop(bpy.context.scene, "Preserve_Location_Rotation_Scale","",icon="NDOF_DOM")
                
        

"""


######  Menu  #########################

class BBox_Retopo_Menu(bpy.types.Menu):
    """Bounding Boxes"""
    bl_label = "Bounding Boxes"
    bl_idname = "object.bbox_retopo_menu"

    def draw(self, context):
        layout = self.layout

        layout.label("Bounding Boxes")

        layout.operator("object.bounding_box", text="Solid Box")
        layout.operator("object.bounding_boxers", text="Wire Box")

bpy.utils.register_class(BBox_Retopo_Menu)


class BBoxOrigin_CornerMenu(bpy.types.Menu):
    """BBox Origin Corner"""
    bl_label = "BBox Origin Corner"
    bl_idname = "object.bbox_origin_corner_menu"

    def draw(self, context):
        layout = self.layout

        # Origin to Corners on Top
        layout.operator("object.cubefront_cornertop_minus_xy", "Front-Top-Left -XY")
        layout.operator("object.cubefront_cornertop_plus_xy", "Front-Top-Right +XY")
        layout.operator("object.cubefront_cornerbottom_minus_xy", "Front-Bottom-Left -XY")
        layout.operator("object.cubefront_cornerbottom_plus_xy", "Front-Bottom-Right +XY")

        layout.separator()

        # Origin to Corners on Bottom
        layout.operator("object.cubeback_cornertop_minus_xy", "Back-Top-Left -XY")
        layout.operator("object.cubeback_cornertop_plus_xy", "Back-Top-Right +XY")
        layout.operator("object.cubeback_cornerbottom_minus_xy", "Back-Bottom-Left -XY")
        layout.operator("object.cubeback_cornerbottom_plus_xy", "Back-Bottom-Right +XY")

bpy.utils.register_class(BBoxOrigin_CornerMenu)


class BBoxOrigin_EdgeMenu(bpy.types.Menu):
    """BBox Origin Edge"""
    bl_label = "BBox Origin Edge"
    bl_idname = "object.bbox_origin_edge_menu"

    def draw(self, context):
        layout = self.layout

        # Origin to Back +Y
        layout.operator("object.cubeback_edgetop_minus_y", "Back-Top +Y")
        layout.operator("object.cubefront_edgebottom_plus_y", "Back-Bottom -Y")
        layout.operator("object.cubefront_edgemiddle_minus_x", "Back-Left -X")
        layout.operator("object.cubefront_edgemiddle_plus_x", "Back-Right +X")

        layout.separator()

        # Origin to the Middle
        layout.operator("object.cubefront_edgetop_minus_x", "Middle-Left-Top -X")
        layout.operator("object.cubefront_edgetop_plus_x", "Middle-Right-Top +X")
        layout.operator("object.cubefront_edgebottom_minus_x", "Middle-Left-Bottom -X")
        layout.operator("object.cubefront_edgebottom_plus_x", "Middle-Right-Bottom +X")

        layout.separator()

        # Origin to Front -Y
        layout.operator("object.cubeback_edgetop_plus_y", "Front-Top +Y")
        layout.operator("object.cubefront_edgebottom_minus_y", "Front-Bottom -Y")
        layout.operator("object.cubefront_edgemiddle_minus_y", "Front-Left -Y")
        layout.operator("object.cubefront_edgemiddle_plus_y", "Front-Right +Y")


bpy.utils.register_class(BBoxOrigin_EdgeMenu)


class BBoxOrigin_SideMenu(bpy.types.Menu):
    """BBox Origin Side"""
    bl_label = "BBox Origin Side"
    bl_idname = "object.bbox_origin_side_menu"

    def draw(self, context):
        layout = self.layout

        # Origin to the Middle of Side
        layout.operator("object.cubefront_side_plus_z", "Top +Z")
        layout.operator("object.cubefront_side_minus_z", "Bottom -Z")
        layout.operator("object.cubefront_side_minus_y", "Front -Y")
        layout.operator("object.cubefront_side_plus_y", "Back +Y")
        layout.operator("object.cubefront_side_minus_x", "Left -X")
        layout.operator("object.cubefront_side_plus_x", "Right +X")

bpy.utils.register_class(BBoxOrigin_SideMenu)


# further function for BoundingBoxSource
class BoundingBox (bpy.types.Operator):
    """create a bound boxes for selected object"""
    bl_idname = "object.bounding_boxers"
    bl_label = "BBox"
    bl_options = {'REGISTER', 'UNDO'}

    bbox_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)
    bbox_wire = bpy.props.BoolProperty(name="Wire only", description="Delete Face", default=False)
    bbox_origin = bpy.props.BoolProperty(name="Origin Center", description="Origin to BBox-Center", default=False)
    bbox_renderoff = bpy.props.BoolProperty(name="Render off", description="Hide from Render", default=False)
    bbox_freeze = bpy.props.BoolProperty(name="Freeze Selection", description="Hide from Selection", default=False)
    bbox_apply = bpy.props.BoolProperty(name="Apply Scale & Rotation", description="Apply Scale & Rotation", default=False)
    bbox_clear = bpy.props.BoolProperty(name="Clear Scale & Rotation", description="Clear Scale & Rotation", default=False)

    def execute(self, context):
        if bpy.context.selected_objects:
            if context.space_data.local_view is not None:
                bpy.ops.view3d.localview()
                bpy.ops.object.bounding_box_wire()
                bpy.ops.object.select_pattern(pattern="_bbox_wire*", case_sensitive=False, extend=False)
                #bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            else:
                bpy.ops.object.bounding_box_wire()
                bpy.ops.object.select_pattern(pattern="_bbox_wire*", case_sensitive=False, extend=False)
                #bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        else:
            bpy.ops.mesh.primitive_cube_add()
            bpy.context.object.name = "_bbox"

        for obj in bpy.context.selected_objects:

            bpy.context.scene.objects.active = obj
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent()

            for i in range(self.bbox_subdiv):
                bpy.ops.mesh.subdivide(number_cuts=1)

            for i in range(self.bbox_wire):
                bpy.ops.mesh.delete(type='ONLY_FACE')

            bpy.ops.object.editmode_toggle()

            for i in range(self.bbox_origin):
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            for i in range(self.bbox_freeze):
                bpy.context.object.hide_select = True

            for i in range(self.bbox_renderoff):
                bpy.context.object.hide_render = True

            for i in range(self.bbox_clear):
                bpy.ops.object.rotation_clear()
                bpy.ops.object.scale_clear()

            for i in range(self.bbox_apply):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            bpy.ops.view3d.rec_normals()

        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)


# further function for BoundingBoxSource
class BoundingBoxDirect (bpy.types.Operator):
    """create a bound boxes for selected object"""
    bl_idname = "object.bounding_box"
    bl_label = "BBox"
    bl_options = {'REGISTER', 'UNDO'}

    bbox_apply = bpy.props.BoolProperty(name="Apply Scale & Rotation", description="Apply Scale & Rotation", default=False)
    bbox_clear = bpy.props.BoolProperty(name="Clear Scale & Rotation", description="Clear Scale & Rotation", default=False)

    def execute(self, context):

        if bpy.context.selected_objects:
            if context.space_data.local_view is not None:
                bpy.ops.view3d.localview()
                bpy.ops.object.bounding_box_source()
                #bpy.ops.object.select_pattern(pattern="_bbox*", case_sensitive=False, extend=False)
                #bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            else:
                bpy.ops.object.bounding_box_source()
                #bpy.ops.object.select_pattern(pattern="_bbox*", case_sensitive=False, extend=False)
                #bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        else:
            bpy.ops.mesh.primitive_cube_add()
            bpy.context.object.name = "_bbox"

        bpy.ops.object.select_pattern(pattern="_bbox*", case_sensitive=False, extend=False)

        for i in range(self.bbox_clear):
            bpy.ops.object.rotation_clear()
            bpy.ops.object.scale_clear()

        for i in range(self.bbox_apply):
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        bpy.ops.view3d.rec_normals()

        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}


# BoundingBoxSource from nikitron (Gorodetskiy Nikita / http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Object/Nikitron_tools)
class BoundingBoxSource (bpy.types.Operator):
    """Make bound boxes for selected objects"""
    bl_idname = "object.bounding_box_source"
    bl_label = "Bounding boxes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects = bpy.context.selected_objects
        i = 0
        for a in objects:
            self.make_it(i, a)
            i += 1
        return {'FINISHED'}

    def make_it(self, i, obj):
        box = bpy.context.selected_objects[i].bound_box
        mw = bpy.context.selected_objects[i].matrix_world
        name = ('_bbox')  # (bpy.context.selected_objects[i].name + '_bbox')
        me = bpy.data.meshes.new(name)  # bpy.data.meshes.new(name +  '_bbox')
        ob = bpy.data.objects.new(name, me)

        ob.location = mw.translation
        ob.scale = mw.to_scale()
        ob.rotation_euler = mw.to_euler()
        ob.show_name = False
        bpy.context.scene.objects.link(ob)
        loc = []
        for ver in box:
            loc.append(mathutils.Vector((ver[0], ver[1], ver[2])))
        me.from_pydata((loc), [], ((0, 1, 2, 3), (0, 1, 5, 4), (4, 5, 6, 7), (6, 7, 3, 2), (0, 3, 7, 4), (1, 2, 6, 5)))
        me.update(calc_edges=True)
        return


class BoundingBoxSource_wire (bpy.types.Operator):
    """Make bound boxes for selected objects"""
    bl_idname = "object.bounding_box_wire"
    bl_label = "Bounding Box Wire"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects = bpy.context.selected_objects
        i = 0
        for a in objects:
            self.make_it(i, a)
            i += 1
        return {'FINISHED'}

    def make_it(self, i, obj):
        box = bpy.context.selected_objects[i].bound_box
        mw = bpy.context.selected_objects[i].matrix_world
        name = ('_bbox_wire')  # (bpy.context.selected_objects[i].name + '_bbox_wire')
        me = bpy.data.meshes.new(name)  # bpy.data.meshes.new(name + '_bbox_wire')
        ob = bpy.data.objects.new(name, me)

        ob.location = mw.translation
        ob.scale = mw.to_scale()
        ob.rotation_euler = mw.to_euler()
        ob.show_name = False
        bpy.context.scene.objects.link(ob)
        loc = []
        for ver in box:
            loc.append(mathutils.Vector((ver[0], ver[1], ver[2])))
        me.from_pydata((loc), [], ((0, 1, 2, 3), (0, 1, 5, 4), (4, 5, 6, 7), (6, 7, 3, 2), (0, 3, 7, 4), (1, 2, 6, 5)))
        me.update(calc_edges=True)
        return

# further function for BoundingBoxSource


class BoundingBox_Extrude(bpy.types.Operator):
    """create a bound boxes for selected object"""
    bl_idname = "object.bbox_extrude"
    bl_label = "BBox"
    bl_options = {'REGISTER', 'UNDO'}

    bbox_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)
    bbox_wire = bpy.props.BoolProperty(name="Wire only", description="Delete Face", default=False)
    bbox_origin = bpy.props.BoolProperty(name="Origin Center", description="Origin to BBox-Center", default=False)
    bbox_renderoff = bpy.props.BoolProperty(name="Render off", description="Hide from Render", default=False)
    bbox_freeze = bpy.props.BoolProperty(name="Freeze Selection", description="Hide from Selection", default=False)
    bbox_apply = bpy.props.BoolProperty(name="Apply Scale & Rotation", description="Apply Scale & Rotation", default=False)
    bbox_clear = bpy.props.BoolProperty(name="Clear Scale & Rotation", description="Clear Scale & Rotation", default=False)

    def execute(self, context):
        if bpy.context.selected_objects:
            if context.space_data.local_view is not None:
                bpy.ops.view3d.localview()
                bpy.ops.object.bounding_box_wire()
                bpy.ops.object.select_pattern(pattern="_bbox_wire*", case_sensitive=False, extend=False)
                #bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            else:
                bpy.ops.object.bounding_box_wire()
                bpy.ops.object.select_pattern(pattern="_bbox_wire*", case_sensitive=False, extend=False)
                #bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        else:
            bpy.ops.mesh.primitive_cube_add()
            bpy.context.object.name = "_bbox"

        for obj in bpy.context.selected_objects:

            bpy.context.scene.objects.active = obj
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent()

            for i in range(self.bbox_subdiv):
                bpy.ops.mesh.subdivide(number_cuts=1)

            for i in range(self.bbox_wire):
                bpy.ops.mesh.delete(type='ONLY_FACE')

            bpy.ops.object.editmode_toggle()

            for i in range(self.bbox_origin):
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            for i in range(self.bbox_freeze):
                bpy.context.object.hide_select = True

            for i in range(self.bbox_renderoff):
                bpy.context.object.hide_render = True

            for i in range(self.bbox_clear):
                bpy.ops.object.rotation_clear()
                bpy.ops.object.scale_clear()

            for i in range(self.bbox_apply):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            bpy.ops.view3d.rec_normals()

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)


class FullCurve(bpy.types.Operator):
    """Add a full beveled Curve"""
    bl_idname = "view3d.fullcurve"
    bl_label = "A full Bevel Curve"
    bl_options = {'REGISTER', 'UNDO'}

    curve_subdiv = bpy.props.IntProperty(name="Subdivide Curve", description="How often?", default=0, min=0, soft_max=10, step=1)
    curve_depth = bpy.props.IntProperty(name="Curve Bevel Depth", description="Depth?", default=0, min=0, soft_max=100, step=1)

    def execute(self, context):

        bpy.ops.curve.primitive_bezier_curve_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        bpy.ops.transform.resize(value=(5, 5, 5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.bevel_resolution = 4
        bpy.context.object.data.resolution_u = 10
        bpy.context.object.data.bevel_depth = 0.2
        bpy.context.object.name = "FullCurve"
        bpy.ops.object.copynametodata()

        bpy.ops.object.editmode_toggle()
        bpy.context.object.data.show_normal_face = False
        bpy.ops.curve.select_all(action='SELECT')

        for i in range(self.curve_depth):
            bpy.context.object.data.bevel_depth = 0.1

        for i in range(self.curve_subdiv):
            bpy.ops.curve.subdivide(number_cuts=1)

        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class FullCircleCurve(bpy.types.Operator):
    """Add a full beveled Circle Curve"""
    bl_idname = "view3d.fullcirlcecurve"
    bl_label = "A full Bevel CircleCurve"
    bl_options = {'REGISTER', 'UNDO'}

    curve_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)

    curve_cycle = bpy.props.BoolProperty(name="Open?", description="Open", default=False)

    def execute(self, context):

        bpy.ops.curve.primitive_bezier_circle_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        bpy.ops.transform.resize(value=(5, 5, 5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.bevel_resolution = 4
        bpy.context.object.data.resolution_u = 10
        bpy.context.object.data.bevel_depth = 0.2

        bpy.ops.object.editmode_toggle()

        bpy.context.object.data.show_normal_face = False

        for i in range(self.curve_subdiv):
            bpy.ops.curve.subdivide(number_cuts=1)

        for i in range(self.curve_cycle):
            bpy.ops.curve.cyclic_toggle(direction='CYCLIC_U')

        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


############  Editmode Operator  ############

class MeshCenter(bpy.types.Operator):
    """Origin to Center of Mesh"""
    bl_idname = "mesh.origincenter"
    bl_label = "Center of Mesh"

    def execute(self, context):
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.loops9()
        bpy.ops.mesh.select_all(action='DESELECT')
        return {'FINISHED'}


class SINGLEVERTEX(bpy.types.Operator):
    """Add a single Vertex in Editmode"""
    bl_idname = "mesh.s_vertex"
    bl_label = "Single Vertex"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.mesh.merge(type='CENTER')
        return {'FINISHED'}


class SINGLELINE_X(bpy.types.Operator):
    """Add a single Line in Editmode"""
    bl_idname = "mesh.s_line_x"
    bl_label = "Single Line"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror": False}, TRANSFORM_OT_translate={"value": (2, 0, 0), "constraint_axis": (True, False, False), "constraint_orientation": 'GLOBAL', "mirror": False, "proportional": 'DISABLED', "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "texture_space": False, "remove_on_cancel": False, "release_confirm": False})
        bpy.ops.mesh.select_linked(limit=False)
        return {'FINISHED'}


class SINGLELINE_Y(bpy.types.Operator):
    """Add a single Line in Editmode"""
    bl_idname = "mesh.s_line_y"
    bl_label = "Single Line"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror": False}, TRANSFORM_OT_translate={"value": (0, 2, 0), "constraint_axis": (False, True, False), "constraint_orientation": 'GLOBAL', "mirror": False, "proportional": 'DISABLED', "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "texture_space": False, "remove_on_cancel": False, "release_confirm": False})
        bpy.ops.mesh.select_linked(limit=False)
        return {'FINISHED'}


class SINGLELINE_Z(bpy.types.Operator):
    """Add a single Line in Editmode"""
    bl_idname = "mesh.s_line_z"
    bl_label = "Single Line"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror": False}, TRANSFORM_OT_translate={"value": (0, 0, 2), "constraint_axis": (False, False, True), "constraint_orientation": 'GLOBAL', "mirror": False, "proportional": 'DISABLED', "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "texture_space": False, "remove_on_cancel": False, "release_confirm": False})
        bpy.ops.mesh.select_linked(limit=False)
        return {'FINISHED'}


class SINGLEPLANE_X(bpy.types.Operator):
    """Add a vertical Plane in Editmode"""
    bl_idname = "mesh.s_plane_x"
    bl_label = "Single Plane"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}


class SINGLEPLANE_Y(bpy.types.Operator):
    """Add a vertical Plane in Editmode"""
    bl_idname = "mesh.s_plane_y"
    bl_label = "Single Plane"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}


class SINGLEPLANE_Z(bpy.types.Operator):
    """Add a vertical Plane in Editmode"""
    bl_idname = "mesh.s_plane_z"
    bl_label = "Single Plane"

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}


# ----------------------------------------------------------------------------------------
###  Origin to Corners on Top  ###
##################################


class Origin_CubeBack_CornerTop_Minus_XY(bpy.types.Operator):
    """Origin to -XY Corner / Top of Cubeback"""
    bl_idname = "object.cubeback_cornertop_minus_xy"
    bl_label = "Origin to -XY Corner / Top of Cubeback"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z += c
                x.co.x -= a

            o.location.y -= b
            o.location.z -= c
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z += c
                x.co.x -= a

            o.location.y -= b
            o.location.z -= c
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeBack_CornerTop_Minus_XY)


class Origin_CubeBack_CornerTop_Plus_XY(bpy.types.Operator):
    """Origin to +XY Corner / Top of Cubeback"""
    bl_idname = "object.cubeback_cornertop_plus_xy"
    bl_label = "Origin to +XY Corner / Top of Cubeback"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z += c
                x.co.x += a

            o.location.y -= b
            o.location.z -= c
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z += c
                x.co.x += a

            o.location.y -= b
            o.location.z -= c
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeBack_CornerTop_Plus_XY)


class Origin_CubeFront_CornerTop_Minus_XY(bpy.types.Operator):
    """Origin to -XY Corner / Top of Cubefront"""
    bl_idname = "object.cubefront_cornertop_minus_xy"
    bl_label = "Origin to -XY Corner / Top of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z += c
                x.co.x -= a

            o.location.y += b
            o.location.z -= c
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z += c
                x.co.x -= a

            o.location.y += b
            o.location.z -= c
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_CornerTop_Minus_XY)


class Origin_CubeFront_CornerTop_Plus_XY(bpy.types.Operator):
    """Origin to +XY Corner / Top of Cubefront"""
    bl_idname = "object.cubefront_cornertop_plus_xy"
    bl_label = "Origin to +XY Corner / Top of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z += c
                x.co.x += a

            o.location.y += b
            o.location.z -= c
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z += c
                x.co.x += a

            o.location.y += b
            o.location.z -= c
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_CornerTop_Plus_XY)


# ----------------------------------------------------------------------------------------
###  Origin to Corners on Bottom  ###
#####################################

class Origin_CubeFront_CornerBottom_Minus_XY(bpy.types.Operator):
    """Origin to -XY Corner / Bottom of CubeFront"""
    bl_idname = "object.cubefront_cornerbottom_minus_xy"
    bl_label = "Origin to -XY Corner / Bottom of CubeFront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z -= c
                x.co.x -= a

            o.location.y += b
            o.location.z += c
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z -= c
                x.co.x -= a

            o.location.y += b
            o.location.z += c
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_CornerBottom_Minus_XY)


class Origin_CubeFront_CornerBottom_Plus_XY(bpy.types.Operator):
    """Origin to +XY Corner / Bottom of CubeFront"""
    bl_idname = "object.cubefront_cornerbottom_plus_xy"
    bl_label = "Origin to +XY Corner / Bottom of CubeFront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z -= c
                x.co.x += a

            o.location.y += b
            o.location.z += c
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z -= c
                x.co.x += a

            o.location.y += b
            o.location.z += c
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_CornerBottom_Plus_XY)


class Origin_CubeBack_CornerBottom_Minus_XY(bpy.types.Operator):
    """Origin to -XY Corner / Bottom of Cubefront"""
    bl_idname = "object.cubeback_cornerbottom_minus_xy"
    bl_label = "Origin to -XY Corner / Bottom of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z -= c
                x.co.x -= a

            o.location.y -= b
            o.location.z += c
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z -= c
                x.co.x -= a

            o.location.y -= b
            o.location.z += c
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeBack_CornerBottom_Minus_XY)


class Origin_CubeBack_CornerBottom_Plus_XY(bpy.types.Operator):
    """Origin to +XY Corner / Bottom of Cubefront"""
    bl_idname = "object.cubeback_cornerbottom_plus_xy"
    bl_label = "Origin to +XY Corner / Bottom of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z -= c
                x.co.x += a

            o.location.y -= b
            o.location.z += c
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z -= c
                x.co.x += a

            o.location.y -= b
            o.location.z += c
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeBack_CornerBottom_Plus_XY)


# ----------------------------------------------------------------------------------------
###  Origin to the Middle of the Top Edges  ###
###############################################


class Origin_CubeBack_EdgeTop_Minus_Y(bpy.types.Operator):
    """Origin to -Y Edge / Top of Cubeback"""
    bl_idname = "object.cubeback_edgetop_minus_y"
    bl_label = "Origin to -Y Edge / Top of Cubeback"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z += c

            o.location.y -= b
            o.location.z -= c
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z += c

            o.location.y -= b
            o.location.z -= c
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeBack_EdgeTop_Minus_Y)


class Origin_CubeBack_EdgeTop_Plus_Y(bpy.types.Operator):
    """Origin to +Y Edge / Top of Cubeback"""
    bl_idname = "object.cubeback_edgetop_plus_y"
    bl_label = "Origin to +Y Edge / Top of Cubeback"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z += c

            o.location.y += b
            o.location.z -= c
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z += c

            o.location.y += b
            o.location.z -= c
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeBack_EdgeTop_Plus_Y)


class Origin_CubeFront_EdgeTop_Minus_X(bpy.types.Operator):
    """Origin to -X Edge / Top of Cubefront"""
    bl_idname = "object.cubefront_edgetop_minus_x"
    bl_label = "Origin to -X Edge / Top of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.x -= a
                x.co.z += c

            o.location.x += a
            o.location.z -= c
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.x -= a
                x.co.z += c

            o.location.x += a
            o.location.z -= c
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeTop_Minus_X)


class Origin_CubeFront_EdgeTop_Plus_X(bpy.types.Operator):
    """Origin to +X Edge / Top of Cubefront"""
    bl_idname = "object.cubefront_edgetop_plus_x"
    bl_label = "Origin to +X Edge / Top of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.x += a
                x.co.z += c

            o.location.x -= a
            o.location.z -= c
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.x += a
                x.co.z += c

            o.location.x -= a
            o.location.z -= c
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeTop_Plus_X)


# -----------------------------------------------------------------------------------
###  Origin to the Middle of the Bottom Edges  ###
##################################################


class Origin_CubeFront_EdgeBottom_Minus_Y(bpy.types.Operator):
    """Origin to -Y Edge / Bottom of CubeFront"""
    bl_idname = "object.cubefront_edgebottom_minus_y"
    bl_label = "Origin to -Y Edge / Bottom of CubeFront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z -= c

            o.location.y += b
            o.location.z += c
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.z -= c

            o.location.y += b
            o.location.z += c
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeBottom_Minus_Y)


class Origin_CubeFront_EdgeBottom_Plus_Y(bpy.types.Operator):
    """Origin to +Y Edge / Bottom of CubeFront"""
    bl_idname = "object.cubefront_edgebottom_plus_y"
    bl_label = "Origin to +Y Edge / Bottom of CubeFront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z -= c

            o.location.y -= b
            o.location.z += c
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.z -= c

            o.location.y -= b
            o.location.z += c
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeBottom_Plus_Y)


class Origin_CubeFront_EdgeBottom_Minus_X(bpy.types.Operator):
    """Origin to -X Edge / Bottom of Cubefront"""
    bl_idname = "object.cubefront_edgebottom_minus_x"
    bl_label = "Origin to -X Edge / Bottom of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.x -= a
                x.co.z -= c

            o.location.x += a
            o.location.z += c
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.x -= a
                x.co.z -= c

            o.location.x += a
            o.location.z += c
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeBottom_Minus_X)


class Origin_CubeFront_EdgeBottom_Plus_X(bpy.types.Operator):
    """Origin to +X Edge / Bottom of Cubefront"""
    bl_idname = "object.cubefront_edgebottom_plus_x"
    bl_label = "Origin to +X Edge / Bottom of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.x += a
                x.co.z -= c

            o.location.x -= a
            o.location.z += c
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.x += a
                x.co.z -= c

            o.location.x -= a
            o.location.z += c
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeBottom_Plus_X)


# -----------------------------------------------------------------------------------
###  Origin to the Middle of the Side Edges  ###
################################################


class Origin_CubeFront_EdgeMiddle_Minus_Y(bpy.types.Operator):
    """Origin to -Y Edge / Middle of CubeFront"""
    bl_idname = "object.cubefront_edgemiddle_minus_y"
    bl_label = "Origin to -Y Edge / Middle of CubeFront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.x -= a

            o.location.y += b
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.x -= a

            o.location.y += b
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeMiddle_Minus_Y)


class Origin_CubeFront_EdgeMiddle_Plus_Y(bpy.types.Operator):
    """Origin to +Y Edge / Middle of CubeFront"""
    bl_idname = "object.cubefront_edgemiddle_plus_y"
    bl_label = "Origin to +Y Edge / Middle of CubeFront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.x += a

            o.location.y += b
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y -= b
                x.co.x += a

            o.location.y += b
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeMiddle_Plus_Y)


class Origin_CubeFront_EdgeMiddle_Minus_X(bpy.types.Operator):
    """Origin to -X Edge / Middle of Cubefront"""
    bl_idname = "object.cubefront_edgemiddle_minus_x"
    bl_label = "Origin to -X Edge / Middle of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.x -= a

            o.location.y -= b
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.x -= a

            o.location.y -= b
            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeMiddle_Minus_X)


class Origin_CubeFront_EdgeMiddle_Plus_X(bpy.types.Operator):
    """Origin to +X Edge / Middle of Cubefront"""
    bl_idname = "object.cubefront_edgemiddle_plus_x"
    bl_label = "Origin to +X Edge / Middle of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.x += a

            o.location.y -= b
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    b = x.co.y
                    c = x.co.z

                    init = 1

                elif x.co.x < a:
                    a = x.co.x

                elif x.co.y < b:
                    b = x.co.y

                elif x.co.z < c:
                    c = x.co.z

            for x in o.data.vertices:
                x.co.y += b
                x.co.x += a

            o.location.y -= b
            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_EdgeMiddle_Plus_X)


# ----------------------------------------------------------------------------------
###  Origin to the Middle of Side  ###
######################################


class Origin_CubeFront_Side_Minus_Y(bpy.types.Operator):
    """Origin to -Y Edge / Bottom of CubeFront"""
    bl_idname = "object.cubefront_side_minus_y"
    bl_label = "Origin to -Y Edge / Bottom of CubeFront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.y
                    init = 1
                elif x.co.y < a:
                    a = x.co.y

            for x in o.data.vertices:
                x.co.y -= a

            o.location.y += a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.y
                    init = 1
                elif x.co.y < a:
                    a = x.co.y

            for x in o.data.vertices:
                x.co.y -= a

            o.location.y += a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_Side_Minus_Y)


class Origin_CubeFront_Side_Plus_Y(bpy.types.Operator):
    """Origin to +Y Edge / Bottom of CubeFront"""
    bl_idname = "object.cubefront_side_plus_y"
    bl_label = "Origin to +Y Edge / Bottom of CubeFront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.y
                    init = 1
                elif x.co.y < a:
                    a = x.co.y

            for x in o.data.vertices:
                x.co.y += a

            o.location.y -= a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.y
                    init = 1
                elif x.co.y < a:
                    a = x.co.y

            for x in o.data.vertices:
                x.co.y += a

            o.location.y -= a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_Side_Plus_Y)


class Origin_CubeFront_Side_Minus_X(bpy.types.Operator):
    """Origin to -X Edge / Bottom of Cubefront"""
    bl_idname = "object.cubefront_side_minus_x"
    bl_label = "Origin to -X Edge / Bottom of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    init = 1
                elif x.co.x < a:
                    a = x.co.x

            for x in o.data.vertices:
                x.co.x -= a

            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    init = 1
                elif x.co.x < a:
                    a = x.co.x

            for x in o.data.vertices:
                x.co.x -= a

            o.location.x += a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


bpy.utils.register_class(Origin_CubeFront_Side_Minus_X)


class Origin_CubeFront_Side_Plus_X(bpy.types.Operator):
    """Origin to +X Edge / Bottom of Cubefront"""
    bl_idname = "object.cubefront_side_plus_x"
    bl_label = "Origin to +X Edge / Bottom of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    init = 1
                elif x.co.x < a:
                    a = x.co.x

            for x in o.data.vertices:
                x.co.x += a

            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.x
                    init = 1
                elif x.co.x < a:
                    a = x.co.x

            for x in o.data.vertices:
                x.co.x += a

            o.location.x -= a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_Side_Plus_X)


class Origin_CubeFront_Side_Minus_Z(bpy.types.Operator):
    """Origin to -Z Edge / Bottom of Cubefront"""
    bl_idname = "object.cubefront_side_minus_z"
    bl_label = "Origin to -Z Edge / Bottom of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.z
                    init = 1
                elif x.co.z < a:
                    a = x.co.z

            for x in o.data.vertices:
                x.co.z -= a

            o.location.z += a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.z
                    init = 1
                elif x.co.z < a:
                    a = x.co.z

            for x in o.data.vertices:
                x.co.z -= a

            o.location.z += a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_Side_Minus_Z)


class Origin_CubeFront_Side_Plus_Z(bpy.types.Operator):
    """Origin to +Z Edge / Bottom of Cubefront"""
    bl_idname = "object.cubefront_side_plus_z"
    bl_label = "Origin to +Z Edge / Bottom of Cubefront"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.z
                    init = 1
                elif x.co.z < a:
                    a = x.co.z

            for x in o.data.vertices:
                x.co.z += a

            o.location.z -= a
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.editmode_toggle()

        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            o = bpy.context.active_object
            init = 0
            for x in o.data.vertices:
                if init == 0:
                    a = x.co.z
                    init = 1
                elif x.co.z < a:
                    a = x.co.z

            for x in o.data.vertices:
                x.co.z += a

            o.location.z -= a
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

bpy.utils.register_class(Origin_CubeFront_Side_Plus_Z)


# from curvetools2
class CurveOriginStart(bpy.types.Operator):
    """Origin to Start Point"""
    bl_idname = "curve.origin_start_point"
    bl_label = "Origin to Start Point"
    bl_description = "Sets the origin of the active/selected curve to the starting point of the (first) spline. Nice for curve modifiers."

    def execute(self, context):
        blCurve = context.active_object
        blSpline = blCurve.data.splines[0]
        newOrigin = blCurve.matrix_world * blSpline.bezier_points[0].co

        origOrigin = bpy.context.scene.cursor_location.copy()
        print("--", "origOrigin: %.6f, %.6f, %.6f" % (origOrigin.x, origOrigin.y, origOrigin.z))
        print("--", "newOrigin: %.6f, %.6f, %.6f" % (newOrigin.x, newOrigin.y, newOrigin.z))

        bpy.context.scene.cursor_location = newOrigin
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor_location = origOrigin

        self.report({'INFO'}, "TODO: Origin to Start Point")

        return {'FINISHED'}


# Origin  #######-------------------------------------------------------
# Origin  #######-------------------------------------------------------

class ORIGIN_SELECT_OBM(bpy.types.Operator):
    """set origin to selected / objectmode"""
    bl_idname = "origin.selected_obm"
    bl_label = "origin to selected / toggle to objectmode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class ORIGIN_SELECT_EDM(bpy.types.Operator):
    """set origin to selected / stay in editmode """
    bl_idname = "origin.selected_edm"
    bl_label = "origin to selected / stay in editmode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class CurveDirection(bpy.types.Operator):
    """switch curve direction"""
    bl_idname = "curve.switch_direction_obm"
    bl_label = "Curve Direction"
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.switch_direction()
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.origin_start_point()
        return {'FINISHED'}

# Fake Bevel


class BBoxBevel_A(bpy.types.Operator):
    """BBox with 15mm Fake Bevel"""
    bl_idname = "bbox.bevel_a"
    bl_label = "FB-15"
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.bounding_boxers(bbox_wire=False)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.bevel(offset=0.15, segments=2, profile=1, vertex_only=False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.shade_smooth()

        bpy.context.object.name = "_bbox_f15"

        return {'FINISHED'}


class BBoxBevel_B(bpy.types.Operator):
    """BBox with 20mm Fake Bevel"""
    bl_idname = "bbox.bevel_b"
    bl_label = "FB-20"
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.bounding_boxers(bbox_wire=False)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.bevel(offset=0.20, segments=2, profile=1, vertex_only=False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.shade_smooth()

        bpy.context.object.name = "_bbox_f20"

        return {'FINISHED'}


class BBoxBevel_C(bpy.types.Operator):
    """BBox with 25mm Fake Bevel"""
    bl_idname = "bbox.bevel_c"
    bl_label = "FB-25"
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.bounding_boxers(bbox_wire=False)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.bevel(offset=0.25, segments=2, profile=1, vertex_only=False)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.shade_smooth()

        bpy.context.object.name = "_bbox_f25"

        return {'FINISHED'}

# Round Bevel


class BBoxBevel_D(bpy.types.Operator):
    """BBox with 15mm Round Bevel"""
    bl_idname = "bbox.bevel_d"
    bl_label = "RB-15"
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.bounding_boxers(bbox_wire=False)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.bevel(offset=0.15, segments=2, profile=0.5, vertex_only=False)
        bpy.ops.object.editmode_toggle()
        # bpy.ops.object.shade_smooth()

        bpy.context.object.name = "_bbox_r15"

        return {'FINISHED'}


class BBoxBevel_E(bpy.types.Operator):
    """BBox with 20mm Round Bevel"""
    bl_idname = "bbox.bevel_e"
    bl_label = "RB-20"
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.bounding_boxers(bbox_wire=False)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.bevel(offset=0.20, segments=2, profile=0.5, vertex_only=False)
        bpy.ops.object.editmode_toggle()
        # bpy.ops.object.shade_smooth()

        bpy.context.object.name = "_bbox_r20"

        return {'FINISHED'}


class BBoxBevel_F(bpy.types.Operator):
    """BBox with 25mm Round Bevel"""
    bl_idname = "bbox.bevel_f"
    bl_label = "RB-25"
    #bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.bounding_boxers(bbox_wire=False)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.bevel(offset=0.25, segments=2, profile=0.5, vertex_only=False)
        bpy.ops.object.editmode_toggle()

        bpy.context.object.name = "_bbox_r25"

        # bpy.ops.object.shade_smooth()

        return {'FINISHED'}


############### Operator ###############
# ScriptSnippet from Author:  Lapineige (Automirror)

class BBoxAlign(bpy.types.Operator):
    """ BBox Quad to choosen Axis """
    bl_idname = "bbox.align_vertices"
    bl_label = "BBox Quad to choosen Axis"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Execute BBox Quad")
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.bbox_extrude(bbox_wire=False)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        bpy.ops.object.mode_set(mode='OBJECT')

        x1, y1, z1 = bpy.context.scene.cursor_location
        bpy.ops.view3d.snap_cursor_to_selected()

        x2, y2, z2 = bpy.context.scene.cursor_location

        bpy.context.scene.cursor_location[0], bpy.context.scene.cursor_location[1], bpy.context.scene.cursor_location[2] = 0, 0, 0

        # Vertices coordinate to 0 (local coordinate, so on the origin)
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if bpy.context.scene.AutoAlign_axis == 'x':
                    axis = 0
                elif bpy.context.scene.AutoAlign_axis == 'y':
                    axis = 1
                elif bpy.context.scene.AutoAlign_axis == 'z':
                    axis = 2
                vert.co[axis] = 0

        bpy.context.scene.cursor_location = x2, y2, z2

        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        bpy.context.scene.cursor_location = x1, y1, z1

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent()
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.5)

        bpy.context.object.name = "_zylbox"
        bpy.ops.mesh.select_all(action='SELECT')
        return {'FINISHED'}


class BBoxCircle_DIV(bpy.types.Operator):
    """BBox Circle SubDiv"""
    bl_idname = "bbox.circle_div"
    bl_label = "CylDiv"
    bl_options = {'REGISTER', 'UNDO'}

    circle_subdiv = bpy.props.IntProperty(name="Subdivide", description="How often?", default=0, min=0, soft_max=10, step=1)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "BBox Circle SubDiv")
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        for i in range(self.circle_subdiv):
            bpy.ops.mesh.subdivide(number_cuts=0)

        bpy.ops.mesh.remove_doubles(threshold=0.5)
        bpy.ops.mesh.looptools_circle(custom_radius=False, fit='best', flatten=True, influence=100, lock_x=False, lock_y=False, lock_z=False, radius=1, regular=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.view3d.snap_selected_to_cursor()
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class BBox_MirrorExtrudeX(bpy.types.Operator):
    """mirror extrude in x direction"""
    bl_idname = "bbox.mirror_extrude_x"
    bl_label = "Mirror Extrude X"
    bl_options = {'REGISTER', 'UNDO'}

    extrude_x = bpy.props.IntProperty(name="Extrude X", description="How long?", default=0, min=0, soft_max=1000, step=1)
    origin = bpy.props.BoolProperty(name="Set Back", description="set back", default=True)
    bevel = bpy.props.BoolProperty(name="Bevel 2mm", description="set bevel", default=False)
    smooth = bpy.props.BoolProperty(name="Smooth", description="set smooth", default=False)
    normals = bpy.props.BoolProperty(name="NormalsFlip", description="flip normals", default=False)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Extrude Cylinder")
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.normals_make_consistent()
        bpy.ops.mesh.extrude_region()

        for i in range(self.extrude_x):
            bpy.ops.transform.translate(value=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(self.origin):
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.view3d.snap_selected_to_cursor()
            bpy.ops.object.editmode_toggle()

        for i in range(self.bevel):
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)

        for i in range(self.smooth):
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.faces_shade_smooth()

        for i in range(self.normals):
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()

        return {'FINISHED'}


class BBox_MirrorExtrudeY(bpy.types.Operator):
    """mirror extrude in y direction"""
    bl_idname = "bbox.mirror_extrude_y"
    bl_label = "Mirror Extrude Y"
    bl_options = {'REGISTER', 'UNDO'}

    extrude_y = bpy.props.IntProperty(name="Extrude Y", description="How long?", default=0, min=0, soft_max=1000, step=1)

    origin = bpy.props.BoolProperty(name="Set Back", description="set back", default=True)
    bevel = bpy.props.BoolProperty(name="Bevel 2mm", description="set bevel", default=False)
    smooth = bpy.props.BoolProperty(name="Smooth", description="set smooth", default=False)
    normals = bpy.props.BoolProperty(name="NormalsFlip", description="flip normals", default=False)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Extrude Cylinder")
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.normals_make_consistent()
        bpy.ops.mesh.extrude_region()

        for i in range(self.extrude_y):
            bpy.ops.transform.translate(value=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(self.origin):
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.view3d.snap_selected_to_cursor()
            bpy.ops.object.editmode_toggle()

        for i in range(self.bevel):
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)

        for i in range(self.smooth):
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.faces_shade_smooth()

        for i in range(self.normals):
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()

        return {'FINISHED'}


class BBox_MirrorExtrudeZ(bpy.types.Operator):
    """mirror extrude in z direction"""
    bl_idname = "bbox.mirror_extrude_z"
    bl_label = "Mirror Extrude Z"
    bl_options = {'REGISTER', 'UNDO'}

    extrude_z = bpy.props.IntProperty(name="Extrude Z", description="How long?", default=0, min=0, soft_max=1000, step=1)
    origin = bpy.props.BoolProperty(name="Set Back", description="set back", default=True)
    bevel = bpy.props.BoolProperty(name="Bevel 2mm", description="set bevel", default=False)
    smooth = bpy.props.BoolProperty(name="Smooth", description="set smooth", default=False)
    normals = bpy.props.BoolProperty(name="NormalsFlip", description="flip normals", default=False)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Extrude Cylinder")
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.normals_make_consistent()
        bpy.ops.mesh.extrude_region()

        for i in range(self.extrude_z):
            bpy.ops.transform.translate(value=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(self.origin):
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.view3d.snap_selected_to_cursor()
            bpy.ops.object.editmode_toggle()

        for i in range(self.bevel):
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)

        for i in range(self.smooth):
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.faces_shade_smooth()

        for i in range(self.normals):
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()

        return {'FINISHED'}


class BBox_MirrorExtrudeN(bpy.types.Operator):
    """mirror extrude in normal direction"""
    bl_idname = "bbox.mirror_extrude_n"
    bl_label = "Mirror Extrude N"
    bl_options = {'REGISTER', 'UNDO'}

    extrude_n = bpy.props.IntProperty(name="Extrude Normal", description="How long?", default=0, min=0, soft_max=1000, step=1)
    origin = bpy.props.BoolProperty(name="Set Back", description="set back", default=True)
    bevel = bpy.props.BoolProperty(name="Bevel 2mm", description="set bevel", default=False)
    smooth = bpy.props.BoolProperty(name="Smooth", description="set smooth", default=False)
    normals = bpy.props.BoolProperty(name="NormalsFlip", description="flip normals", default=False)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Extrude Cylinder")
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.normals_make_consistent()
        bpy.ops.mesh.extrude_region()

        for i in range(self.extrude_n):
            bpy.ops.transform.translate(value=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        for i in range(self.origin):
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            bpy.ops.view3d.snap_selected_to_cursor()
            bpy.ops.object.editmode_toggle()

        for i in range(self.bevel):
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.bevel(offset=0.2, segments=2, profile=1, vertex_only=False)

        for i in range(self.smooth):
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.faces_shade_smooth()

        for i in range(self.normals):
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()

        return {'FINISHED'}


###########################################

class BevelModifier_one(bpy.types.Operator):
    """Add a bevel modifier to all selected objects"""
    bl_idname = "view3d.bevelmodifier_one"
    bl_label = "Bevel Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    width = bpy.props.BoolProperty(name="2mm to 3mm", description="Width", default=False)
    angle = bpy.props.BoolProperty(name="Angle Limit", description="Profil", default=False)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Add Bevel Modifier")
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_remove(modifier="Bevel")

            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.ops.view3d.display_modifiers_cage_on()
            bpy.context.object.modifiers["Bevel"].segments = 1
            bpy.context.object.modifiers["Bevel"].profile = 0.5
            bpy.context.object.modifiers["Bevel"].width = 0.2

            for i in range(self.width):
                bpy.context.object.modifiers["Bevel"].width = 0.3

            for i in range(self.angle):
                bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'

        return {'FINISHED'}

from bpy.props import *


class BevelModifier_two(bpy.types.Operator):
    """Add a bevel modifier to all selected objects"""
    bl_idname = "view3d.bevelmodifier_two"
    bl_label = "Bevel Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    width = bpy.props.BoolProperty(name="2mm to 3mm", description="Width", default=False)
    profil_one = bpy.props.BoolProperty(name="Profil 1 or 0.5", description="Profil", default=False)
    angle = bpy.props.BoolProperty(name="Angle Limit", description="Profil", default=False)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Add Bevel Modifier")
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_remove(modifier="Bevel")

            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.ops.view3d.display_modifiers_cage_on()
            bpy.context.object.modifiers["Bevel"].segments = 2
            bpy.context.object.modifiers["Bevel"].profile = 0.5
            bpy.context.object.modifiers["Bevel"].width = 0.2

            for i in range(self.width):
                bpy.context.object.modifiers["Bevel"].width  # = 0.3

            for i in range(self.profil_one):
                bpy.context.object.modifiers["Bevel"].profile = 1

            for i in range(self.angle):
                bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'

        return {'FINISHED'}


class BevelModifier_three(bpy.types.Operator):
    """Add a bevel modifier to all selected objects"""
    bl_idname = "view3d.bevelmodifier_three"
    bl_label = "Bevel Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    width = bpy.props.BoolProperty(name="2mm to 3mm", description="Width", default=False)
    profil_one = bpy.props.BoolProperty(name="Profil 1 or 0.5", description="Profil", default=False)
    angle = bpy.props.BoolProperty(name="Angle Limit", description="Profil", default=False)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Add Bevel Modifier")
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_remove(modifier="Bevel")

            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.ops.view3d.display_modifiers_cage_on()
            bpy.context.object.modifiers["Bevel"].segments = 3
            bpy.context.object.modifiers["Bevel"].profile = 0.5
            bpy.context.object.modifiers["Bevel"].width = 0.2

            for i in range(self.width):
                bpy.context.object.modifiers["Bevel"].width = 0.3

            for i in range(self.profil_one):
                bpy.context.object.modifiers["Bevel"].profile = 1

            for i in range(self.angle):
                bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'

        return {'FINISHED'}


class BevelModifier_four(bpy.types.Operator):
    """Add a bevel modifier to all selected objects"""
    bl_idname = "view3d.bevelmodifier_four"
    bl_label = "Bevel Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    width = bpy.props.BoolProperty(name="2mm to 3mm", description="Width", default=False)
    profil_one = bpy.props.BoolProperty(name="Profil 1 or 0.5", description="Profil", default=False)
    angle = bpy.props.BoolProperty(name="Angle Limit", description="Profil", default=False)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Add Bevel Modifier")
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_remove(modifier="Bevel")

            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.ops.view3d.display_modifiers_cage_on()
            bpy.context.object.modifiers["Bevel"].segments = 4
            bpy.context.object.modifiers["Bevel"].profile = 0.5
            bpy.context.object.modifiers["Bevel"].width = 0.2

            for i in range(self.width):
                bpy.context.object.modifiers["Bevel"].width = 0.3

            for i in range(self.profil_one):
                bpy.context.object.modifiers["Bevel"].profile = 1

            for i in range(self.angle):
                bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'

        return {'FINISHED'}


class BevelModifier_five(bpy.types.Operator):
    """Add a bevel modifier to all selected objects"""
    bl_idname = "view3d.bevelmodifier_five"
    bl_label = "Bevel Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    width = bpy.props.BoolProperty(name="2mm to 3mm", description="Width", default=False)
    profil = bpy.props.BoolProperty(name="Profil 1 or 0.5", description="Profil", default=False)
    angle = bpy.props.BoolProperty(name="Angle Limit", description="Profil", default=False)

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Add Bevel Modifier")
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_remove(modifier="Bevel")

            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.ops.view3d.display_modifiers_cage_on()
            bpy.context.object.modifiers["Bevel"].segments = 5
            bpy.context.object.modifiers["Bevel"].profile = 0.5
            bpy.context.object.modifiers["Bevel"].width = 0.2

            for i in range(self.width):
                bpy.context.object.modifiers["Bevel"].width = 0.3

            for i in range(self.profil_one):
                bpy.context.object.modifiers["Bevel"].profile = 1

            for i in range(self.angle):
                bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'

        return {'FINISHED'}


class BevelModifierApply(bpy.types.Operator):
    """Add a bevel modifier to all selected objects"""
    bl_idname = "view3d.bevel_apply"
    bl_label = "Apply Bevel Modifier"

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Apply Bevel Modifier")
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Bevel")

        return {'FINISHED'}


class BevelModifierRemove(bpy.types.Operator):
    """Add a bevel modifier to all selected objects"""
    bl_idname = "view3d.bevel_remove"
    bl_label = "Remove Bevel Modifier"

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Remove Bevel Modifier")
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj
            bpy.ops.object.modifier_remove(modifier="Bevel")

        return {'FINISHED'}


class Normals(bpy.types.Operator):
    """Recalculate Normals for all selected Objects in Objectmode"""
    bl_idname = "view3d.rec_normals"
    bl_label = "Recalculate Normals"

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Recalculate Normals")
        for obj in bpy.context.selected_objects:
            bpy.context.scene.objects.active = obj

            if obj:
                obj_type = obj.type

                if obj_type in {'MESH'}:
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.normals_make_consistent()
                    bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


# Albertofx
class removedoubles(bpy.types.Operator):
    """Removes doubles on selected objects."""
    bl_idname = "mesh.removedouble"
    bl_label = "Remove Doubles off Selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.join()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        return {'FINISHED'}


#######################################

class BBoxSelection(bpy.types.Operator):
    """Select all existing bbox* in the scene"""
    bl_idname = "view3d.bbox_select"
    bl_label = "Select all BBox"

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Select all BBox")
        bpy.ops.object.select_pattern(pattern="_bbox*")
        return {'FINISHED'}


class BBoxSelection_Wire(bpy.types.Operator):
    """Select all existing wirebox* in the scene"""
    bl_idname = "view3d.bbox_select_wire"
    bl_label = "Select all BBox"

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Select all BBox")
        bpy.ops.object.select_pattern(pattern="_bbox_wire*")

        return {'FINISHED'}


class BBoxSelection_Zyl(bpy.types.Operator):
    """Select all existing zylbox* in the scene"""
    bl_idname = "view3d.bbox_select_zyl"
    bl_label = "Select all BBox"

    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Select all BBox")
        bpy.ops.object.select_pattern(pattern="_zylbox*")

        return {'FINISHED'}


############  Draw Menu  ############


# add a menu to objectmode
def draw_item_OBM(self, context):
    layout = self.layout
    layout.menu(CustomAddMenu_OBM.bl_idname, icon="ROTATE")


# add a menu to editmode
def draw_item_EDM(self, context):
    layout = self.layout
    if context.mode == 'EDIT_MESH':
        layout.menu(CustomAddMenu_EDM.bl_idname, icon="ROTATE")

"""
#add single operator    
def draw_item_Vert(self, context):
    layout = self.layout
    if context.mode == 'EDIT_MESH':
        layout.operator("mesh.s_vertex", text="Vertex", icon = "LAYER_ACTIVE")
"""

# add a menu to objectmode


def draw_item_Curve(self, context):
    layout = self.layout
    if context.mode == 'OBJECT':
        layout.separator()

        layout.operator("view3d.fullcurve", "Bevel Curve", icon="CURVE_BEZCURVE")
        layout.operator("view3d.fullcirlcecurve", "Bevel Circle", icon="CURVE_BEZCIRCLE")


# add bbox operator
def draw_item_BBox(self, context):
    layout = self.layout
    layout.menu("object.bbox_set_menu", "BBox", icon="BBOX")


############  REGISTER  ############
def register():

    bpy.utils.register_class(BoundingBoxSource)
    bpy.utils.register_class(BoundingBox)
    bpy.utils.register_class(BoundingBoxDirect)

    bpy.utils.register_class(FullCurve)
    bpy.utils.register_class(FullCircleCurve)

    # bpy.utils.register_class(BBOXSET)
    bpy.utils.register_class(BBoxBevel_A)
    bpy.utils.register_class(BBoxBevel_B)
    bpy.utils.register_class(BBoxBevel_C)
    bpy.utils.register_class(BBoxBevel_D)
    bpy.utils.register_class(BBoxBevel_E)
    bpy.utils.register_class(BBoxBevel_F)
    bpy.utils.register_class(BBoxAlign)
    bpy.utils.register_class(BBoxCircle_DIV)
    bpy.utils.register_class(BBox_MirrorExtrudeX)
    bpy.utils.register_class(BBox_MirrorExtrudeY)
    bpy.utils.register_class(BBox_MirrorExtrudeZ)
    bpy.utils.register_class(BBox_MirrorExtrudeN)

    # bpy.utils.register_class(ExampleAddonPreferences)
    #update_panel(None, bpy.context)

    # prepend = to MenuTop / append to MenuBottom
    bpy.types.INFO_MT_add.prepend(draw_item_BBox)
    # bpy.types.INFO_MT_mesh_add.prepend(draw_item_BBox)

    # bpy.types.INFO_MT_add.prepend(draw_item_OBM)
    bpy.types.INFO_MT_mesh_add.append(draw_item_EDM)
    bpy.types.INFO_MT_curve_add.append(draw_item_Curve)

    bpy.utils.register_module(__name__)


def unregister():

    bpy.utils.unregister_class(BoundingBoxSource)
    bpy.utils.unregister_class(BoundingBox)
    bpy.utils.unregister_class(BoundingBoxDirect)

    bpy.utils.unregister_class(FullCurve)
    bpy.utils.unregister_class(FullCircleCurve)

    # bpy.utils.unregister_class(BBOXSET)
    bpy.utils.unregister_class(BBoxBevel_A)
    bpy.utils.unregister_class(BBoxBevel_B)
    bpy.utils.unregister_class(BBoxBevel_C)
    bpy.utils.unregister_class(BBoxBevel_D)
    bpy.utils.unregister_class(BBoxBevel_E)
    bpy.utils.unregister_class(BBoxBevel_F)
    bpy.utils.unregister_class(BBoxAlign)
    bpy.utils.unregister_class(BBoxCircle_DIV)
    bpy.utils.unregister_class(BBox_MirrorExtrudeX)
    bpy.utils.unregister_class(BBox_MirrorExtrudeY)
    bpy.utils.unregister_class(BBox_MirrorExtrudeZ)
    bpy.utils.unregister_class(BBox_MirrorExtrudeN)

    # bpy.utils.unregister_class(ExampleAddonPreferences)

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
