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
    "name": "TP Display View",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy
from bpy import *


class VIEW3D_TP_Display_Object_Mesh(bpy.types.Menu):
    bl_label = "Display [ALT+3]"
    bl_idname = "tp_display.object_mesh"

    def draw(self, context):
        layout = self.layout

        obj = context.object
        obj_type = obj.type
        is_geometry = (obj_type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'})
        is_wire = (obj_type in {'CAMERA', 'EMPTY'})
        is_empty_image = (obj_type == 'EMPTY' and obj.empty_draw_type == 'IMAGE')
        is_dupli = (obj.dupli_type != 'NONE')

        mesh = context.active_object.data
        
        if obj and obj.mode == 'EDIT':

            layout.operator("wm.context_toggle", text="Limit to Visible", icon="ORTHO").data_path = "space_data.use_occlude_geometry"
            layout.menu("tp_display.mesh_overlays", icon ="RETOPO")

            layout.separator() 
          
        layout.prop(obj, "show_axis", text="Axis")        
        layout.prop(obj, "show_name", text="Name")
        
        layout.operator("tp_display.wire_all", text ="Wire all", icon = "CHECKBOX_DEHLT")
        
        if is_geometry or is_dupli:
            layout.prop(obj, "show_wire", text="Wire")
        if obj_type == 'MESH' or is_dupli:
            layout.prop(obj, "show_all_edges")
            
        layout.prop(obj, "show_x_ray", text="X-Ray")

        if obj and obj.mode == 'OBJECT':
            if obj_type == 'MESH' or is_empty_image:
                layout.prop(obj, "show_transparent", text="Transparency")

        layout.separator()
        
        if obj and obj.mode == 'OBJECT':                
            layout.prop(obj, "show_bounds", text="Bounds")
            layout.prop(obj, "draw_bounds_type", text="", icon="BBOX")
            
            layout.separator()
        
        if is_geometry:
            layout.prop(obj, "show_texture_space", text="Texture Space")

        if is_wire:
            layout.active = is_dupli
            layout.label(text="Maximum Dupli Draw Type:")
        else:
            layout.label(text="Maximum Draw Type:")
        layout.prop(obj, "draw_type", text="", icon="BRUSH_DATA")

        layout.separator()
		
        layout.operator("tp_display.new_material", text="New Material", icon = "STYLUS_PRESSURE")
        layout.operator("tp_display.material_remove", text="Delete All Materials")        
        if is_geometry or is_empty_image:
           
            layout.label(text="Object Color:", icon="COLOR")
            layout.prop(obj, "color", text="") 
         
        layout.separator()
		
        layout.prop(mesh, "show_double_sided", text = "Normals: Double Sided")     
        layout.prop(mesh, "use_auto_smooth", text = "Normals: Auto Smooth") 
        layout.prop(mesh, "auto_smooth_angle", text="Auto Smooth Angle")
		


          
class TP_Mesh_Overlays(bpy.types.Menu):
    bl_label = "Mesh Overlays"
    bl_idname = "tp_display.mesh_overlays"
   
    def draw(self, context):
        layout = self.layout
        
        with_freestyle = bpy.app.build_options.freestyle

        mesh = context.active_object.data
        scene = context.scene
              
        layout.prop(mesh, "show_faces", text="Faces")
        layout.prop(mesh, "show_edges", text="Edges")
        layout.prop(mesh, "show_edge_crease", text="Creases")
        layout.prop(mesh, "show_weight", text = "Weights")

        if with_freestyle:
            layout.prop(mesh, "show_edge_seams", text="Seams")

        if not with_freestyle:
            layout.prop(mesh, "show_edge_seams", text="Seams")

        layout.prop(mesh, "show_edge_sharp", text="Sharp")
        layout.prop(mesh, "show_edge_bevel_weight", text="Bevel")  
            
        if with_freestyle:
            layout.prop(mesh, "show_freestyle_edge_marks", text="Edge Marks")
            layout.prop(mesh, "show_freestyle_face_marks", text="Face Marks")              
               
        if bpy.app.debug:
            layout.prop(mesh, "show_extra_indices")       

bpy.utils.register_class(TP_Mesh_Overlays)



class TP_Wire_All(bpy.types.Operator):
    bl_idname = "tp_display.wire_all"
    bl_label = "Wire All"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        for obj in bpy.data.objects:
            if obj.show_wire:
                obj.show_all_edges = False
                obj.show_wire = False
            else:
                obj.show_all_edges = True
                obj.show_wire = True
        return {'FINISHED'}

bpy.utils.register_class(TP_Wire_All)

        
class TP_New_Material(bpy.types.Operator):
    """add a new material and enable color object in options"""
    bl_idname = "tp_display.new_material"
    bl_label = "Add new Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.view3d.assign_material()
        bpy.context.object.active_material.use_object_color = True
        return {'FINISHED'}

bpy.utils.register_class(TP_New_Material) 


class TP_Material_Remove(bpy.types.Operator):
    """Remove material slots from active objects"""
    bl_idname = "tp_display.material_remove"
    bl_label = "Remove All Material Slots"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        remove_materials()
        return {'FINISHED'}
    
bpy.utils.register_class(TP_Material_Remove)


def register():    

    bpy.utils.register_class(VIEW3D_TP_Display_Object_Mesh)    
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'THREE', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.object_mesh"      


def unregister():
  
    bpy.utils.unregister_class(VIEW3D_TP_Display_Object_Mesh)    
    
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
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_Object_Mesh.bl_idname)
         









