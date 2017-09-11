import bpy
import blf
import bgl
from . data_init import *
from bpy.app.handlers import persistent



def updateTextHandlers(scene):
    vieportInfoProps = bpy.context.scene.vieportInfo
    if bpy.context.object is not None:
        mode = bpy.context.object.mode
        if mode == 'EDIT':
            if vieportInfoProps.update_mode_enabled:
                if vieportInfoProps.update_toggle_mode != 'EDIT':
                    vieportInfoProps.update_toggle_mode = bpy.context.object.mode
                    vieportInfoProps.updated_edt_text[:]=editInfo()
            if vieportInfoProps.edt_use:
                ob = scene.objects.active
                if ob.data.is_updated_data:
                    vieportInfoProps.updated_edt_text[:] =editInfo()
        elif mode == 'OBJECT':        
            if vieportInfoProps.update_toggle_mode != 'OBJECT':
                vieportInfoProps.update_toggle_mode = bpy.context.object.mode
                vieportInfoProps.updated_obj_text[:] =objInfo()

            if vieportInfoProps.obj_use:
                if bpy.context.selected_objects not in vieportInfoProps.obj_pre:
                    vieportInfoProps.obj_pre[:] = []
                    vieportInfoProps.obj_pre.append(bpy.context.selected_objects)
                    vieportInfoProps.updated_obj_text[:] =objInfo()
                    # print("updateTextHandlers ")
                    # print(vieportInfoProps.updated_obj_text)

vp_info_handle = []

@persistent
def DrawVieportInfoProperties(scn):
    # if not(context.object is not None and (context.object.type == 'MESH' or context.object.type == 'CAMERA')):
    #     return
    updateTextProperties('ads')
    if bpy.context.scene.vieportInfo.vp_info_enabled != False:
        if vp_info_handle:
            bpy.types.SpaceView3D.draw_handler_remove(vp_info_handle[0], 'WINDOW')
        args=(bpy.context.scene.vieportInfo,bpy.context)
        vp_info_handle[:] = [bpy.types.SpaceView3D.draw_handler_add(drawTextCallback, args,'WINDOW', 'POST_PIXEL')]

    else:
        if vp_info_handle:
            bpy.types.SpaceView3D.draw_handler_remove(vp_info_handle[0], 'WINDOW')
            vp_info_handle[:] = []

@persistent
def updateTextProperties(context):
    if bpy.context.scene.vieportInfo.vp_info_enabled == True:
        if not updateTextHandlers in bpy.app.handlers.scene_update_post:
            # __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
            bpy.app.handlers.scene_update_post.append(updateTextHandlers)
    else:
        if updateTextHandlers in bpy.app.handlers.scene_update_post:
            bpy.app.handlers.scene_update_post.remove(updateTextHandlers)

        

def drawObjTextArray(text, corner, pos_x, pos_y):
    vieportInfoProps = bpy.context.scene.vieportInfo
    mode = bpy.context.object.mode
    font_id = 0
    height = bpy.context.region.height
    width = bpy.context.region.width
    txt_width = []
    list_line_width = []
    blf.size(font_id, vieportInfoProps.text_font_size, 72)
    x_offset = 0
    y_offset = 0
    line_height = (blf.dimensions(font_id, "M")[1] * 1.45) 
    x = 0
    y = 0 
    
    for command in text:            
        if len(command) == 2:
            Text, Color = command             
            text_width, text_height = blf.dimensions(font_id, Text) 
            txt_width.append(text_width)
    
    if corner == '1' or corner == '3':
        x = pos_x
            
    else:
        if mode == 'OBJECT' and vieportInfoProps.obj_use and vieportInfoProps.multi_obj_enabled and (len(bpy.context.selected_objects) >= 2):
            count_obj = len(bpy.context.selected_objects)            
            len_list = len(txt_width)                           # count of item in the list
            count_item = int(len_list / count_obj)              # count of item by object
            i = 0
            start = 0
            end = count_item
            list_text = [] 
            
            for item in txt_width:
                while i < count_obj:
                    list_text.append(txt_width[start:start + end])
                    start+=end
                    i+=1      
            for item in list_text:
                list_line_width.append(sum(item[:]))
            x = width - (max(list_line_width) + pos_x)
        else:
            if txt_width:
                for label, value in zip(txt_width[0::2], txt_width[1::2]): 
                    l_width = label + value        
                    list_line_width.append(l_width) 
                x = width - (max(list_line_width) + pos_x)
            
    if corner == '1' or corner == '2': 
        y = height - pos_y
    
    else: 
        if mode == 'OBJECT' and vieportInfoProps.obj_use and vieportInfoProps.multi_obj_enabled and (len(bpy.context.selected_objects) >= 2):
            line_count = len(bpy.context.selected_objects)
            y = pos_y + (line_height*line_count)
        else:
            line_count = text.count("Carriage return")   
            y = pos_y + (line_height*line_count)
    
        
    for command in text:            
        if len(command) == 2:
            Text, Color = command          
            bgl.glColor3f(*Color)
            text_width, text_height = blf.dimensions(font_id, Text)                                                   
            blf.position(font_id, (x + x_offset), (y + y_offset), 0)          
            blf.draw(font_id, Text)                
            x_offset += text_width  
                      
        else:                
            x_offset = 0           
            y_offset -= line_height
                                
def drawTextArray(text, corner, pos_x, pos_y):
    vieportInfoProps = bpy.context.scene.vieportInfo
    font_id = 0
    height = bpy.context.region.height
    width = bpy.context.region.width
    txt_width = []
    list_line_width = []
    blf.size(font_id, vieportInfoProps.text_font_size, 72)
    x_offset = 0
    y_offset = 0
    line_height = (blf.dimensions(font_id, "M")[1] * 1.45) 
    x = 0
    y = 0 
    
    for command in text:            
        if len(command) == 2:
            Text, Color = command             
            text_width, text_height = blf.dimensions(font_id, Text) 
            txt_width.append(text_width)
    
    if corner == '1' or corner == '3':
        x = pos_x
            
    else:
        if txt_width:
            for label, value in zip(txt_width[0::2], txt_width[1::2]): 
                l_width = label + value        
                list_line_width.append(l_width) 
            x = width - (max(list_line_width) + pos_x)
            
    if corner == '1' or corner == '2': 
        y = height - pos_y
    
    else: 
        line_count = text.count("Carriage return")   
        y = pos_y + (line_height*line_count)
    
        
    for command in text:            
        if len(command) == 2:
            Text, Color = command          
            bgl.glColor3f(*Color)
            text_width, text_height = blf.dimensions(font_id, Text)                                                   
            blf.position(font_id, (x + x_offset), (y + y_offset), 0)          
            blf.draw(font_id, Text)                
            x_offset += text_width  
                      
        else:                
            x_offset = 0           
            y_offset -= line_height
            
             
                                                                       
# Draw the text in the viewport
def drawTextCallback(self,context):
    vieportInfoProps = bpy.context.scene.vieportInfo

    if context.object is not None: 
        if context.object.mode == 'EDIT':
            if vieportInfoProps.edt_use:
                drawTextArray(vieportInfoProps.updated_edt_text, vieportInfoProps.edt_corner, vieportInfoProps.edt_pos_x, vieportInfoProps.edt_pos_y)
        elif context.object.mode == 'OBJECT':              
            if vieportInfoProps.obj_use:
                # __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
                # print('draw callpback-----  '+str(vieportInfoProps.updated_obj_text))
                drawObjTextArray(vieportInfoProps.updated_obj_text, vieportInfoProps.obj_corner, vieportInfoProps.obj_pos_x, vieportInfoProps.obj_pos_y)
        elif context.object.mode == 'SCULPT':
            if vieportInfoProps.sculpt_use:
                drawTextArray(sculptInfo(),vieportInfoProps.sculpt_corner, vieportInfoProps.sculpt_pos_x, vieportInfoProps.sculpt_pos_y)

 

class DATA_OP_triangles_select(bpy.types.Operator):
    """Select triangles"""
    bl_idname = "data.triangles_select"
    bl_label = "Select triangles"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'

    def execute(self, context):
        vieportInfoProps = bpy.context.scene.vieportInfo

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        context.tool_settings.mesh_select_mode=(False, False, True)
        bpy.ops.mesh.select_face_by_sides(number=3, type='EQUAL')
        bpy.ops.mesh.select_mode(type=vieportInfoProps.select_mode)
        return {'FINISHED'} 
    
        

class DATA_OP_ngons_select(bpy.types.Operator):
    """Select ngons"""
    bl_idname = "data.ngons_select"
    bl_label = "Select ngons"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'

    def execute(self, context):
        vieportInfoProps = bpy.context.scene.vieportInfo
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        context.tool_settings.mesh_select_mode=(False, False, True)
        bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
        bpy.ops.mesh.select_mode(type=vieportInfoProps.select_mode)
        return {'FINISHED'}  