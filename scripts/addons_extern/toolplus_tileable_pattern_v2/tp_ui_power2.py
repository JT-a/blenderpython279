import bpy
from bpy import*
from bpy.props import *
#from . icons.icons import load_icons



class View3D_TP_Tileable_Array_Panel(bpy.types.Panel):
    """"""
    bl_label = "Array"
    bl_idname = "OBJECT_TP_Array_Pattern"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' 
    bl_category = "T+"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        isModelingMode = not (
        context.sculpt_object or 
        context.vertex_paint_object
        or context.weight_paint_object
        or context.image_paint_object)
        return (isModelingMode)


    def draw(self, context):
        layout = self.layout.column_flow(1)
        layout.operator_context = 'INVOKE_DEFAULT'

        #icons = load_icons()
        #CST = icons.get("CST")
        #row.label("Animation Render", icon_value=CST.icon_id)
        
        obj = context.active_object
        if obj:
            obj_type = obj.type
            
            if obj_type in {'MESH'}:    

                box = layout.box().column(1)

                row = box.row(1)          
                row.label(text="Join", icon = "MOD_MESHDEFORM")      

                box.separator()

                row = box.column(1)   
                row.operator("tp_ops.tileable_join",text = "merge mesh instances", icon = "FULLSCREEN_EXIT")   

                box.separator() 
                                   
                row = box.column(1)
                row.operator("tp_ops.tileable_cutout","cutout instance fill", icon = "GRID")
                
                box.separator()
               
        box = layout.box().column(1)

        row = box.row(1)           
        row.label(text="Power of Two", icon = "MOD_TRIANGULATE")      

        
        box.separator()
        
        row = box.row(1) 
        row.operator("tp_ops.tileable_arrays", "xy array modifier", icon = "MOD_ARRAY")
        
        sub = row.row(1)
        sub.scale_x = 1.4
        sub.operator("tp_ops.modifiers_off","",icon = 'VISIBLE_IPO_OFF')  
        sub.operator("tp_ops.modifiers_on", "",icon = 'RESTRICT_VIEW_OFF')   

        box.separator()
       
        row = box.column(1) 
                        
        mo_types = []
        append = mo_types.append

        for mo in context.active_object.modifiers:
            if mo.type == 'ARRAY':
                append(mo.type)

                box.label(mo.name)

                split = box.split()

                row = split.row(1)
                row.prop(mo, "count", text="")
                #row.prop(mo, "relative_offset_displace", text="")
      
        if context.active_object.modifiers:    
                            
            box.separator()
            
            row = box.column(1)                                               
            row.operator("tp_ops.tileable_array_scale","apply dimension", icon = "MAN_SCALE")             
            
            obj = context.active_object
            if obj:
                obj_type = obj.type                
                if obj_type in {'MESH'}: 
                    
                    row = box.row(1)                      
                    row.prop(context.scene, "tp_verts_offset", text="")
                    row.operator("tp_ops.add_vertices_offset","add offset")             
            
            box.separator()



