import bpy
import bmesh


        ######################################
        ####    DISPLAY TEXT FONCTIONS    ####
        ######################################  
        
          
def editInfo():
    outputString = []
    vieportInfoProps = bpy.context.scene.vieportInfo
    label_color = vieportInfoProps.label_color
    value_color = vieportInfoProps.value_color
    CR = "Carriage return"         
    
    ob = bpy.context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    
    quads = tris = ngons = 0
    ngons_to_tris = 0             
    
    for f in bm.faces:                
        v = len(f.verts)
        if v == 3: # tris
            tris += 1
            if vieportInfoProps.display_color_enabled:
                f.material_index = 2
        elif v == 4: # quads
            quads += 1 
            if vieportInfoProps.display_color_enabled:
                f.material_index = 0 
        elif v > 4: # ngons
            ngons += 1            
            V = len(f.verts) - 2 # nomber of tris in ngons
            ngons_to_tris += V # get total tris of total ngons 
            if vieportInfoProps.display_color_enabled:
                f.material_index = 1 
                
    bmesh.update_edit_mesh(me)
    
    if vieportInfoProps.faces_count_edt:
        outputString.extend([CR, ("Faces: ", label_color), (str(len(bm.faces)), value_color)])
    if vieportInfoProps.tris_count_edt:
        outputString.extend([CR, ("Tris: ", label_color), (str(tris + quads*2 + ngons_to_tris), value_color)])
    if vieportInfoProps.ngons_count_edt:
        outputString.extend([CR, ("Ngons: ", label_color), (str(ngons), value_color)])
    if vieportInfoProps.verts_count_edt:
        outputString.extend([CR, ("Vertex: ", label_color), (str(len(bm.verts)), value_color)])

    return outputString


def trisCount():
    quads = tris = ngons = 0
    ngons_to_tris = 0

    ob = bpy.context.active_object
    for p in ob.data.polygons:
        count = p.loop_total
        if count == 3:
            tris += 1
        elif count == 4:
            quads += 1
        elif count > 4:
            ngons += 1
            V = count - 2
            ngons_to_tris += V
    tris_count = str(tris + quads*2 + ngons_to_tris)

    return tris_count

def ngonsCount():
    ngons = 0
    ob = bpy.context.active_object
    for p in ob.data.polygons:
        count = p.loop_total
        if count > 4:
            ngons += 1

    return str(ngons)
            
            
def objInfo():

    outputString=[]
    vieportInfoProps = bpy.context.scene.vieportInfo
    label_color = vieportInfoProps.label_color
    value_color = vieportInfoProps.value_color
    name_color = vieportInfoProps.name_color
    CR = "Carriage return"
    ob = bpy.context.active_object
    
    item_list = []

    if len(bpy.context.selected_objects) >= 2:
        for obj in bpy.context.selected_objects:
            item_list.append(obj)
        for obj in item_list:
            if obj.type == 'CAMERA':
                item_list.remove(obj)
      
    if len(item_list) >= 2 and vieportInfoProps.multi_obj_enabled:
            
        for obj in item_list: 

            bpy.context.scene.objects.active = bpy.data.objects[obj.name]                        
            outputString.extend([CR, (obj.name, name_color)])
                    
            if vieportInfoProps.faces_count_obj:
                faces = len(bpy.context.active_object.data.polygons)
                outputString.extend([(" F ", label_color), (str(faces) + ",", value_color)])
            if vieportInfoProps.tris_count_obj:
                outputString.extend([(" T ", label_color), (trisCount() + ",", value_color)])
            if vieportInfoProps.ngons_count_obj:
                outputString.extend([(" Ng ", label_color), (ngonsCount() + ",", value_color)])
            if vieportInfoProps.verts_count_obj:
                verts = len(bpy.context.active_object.data.vertices)
                outputString.extend([(" V ", label_color), (str(verts), value_color)])
    
    elif len(item_list) == 1: 
        for obj in item_list: 
            bpy.context.scene.objects.active = bpy.data.objects[obj.name] 
                  
            if vieportInfoProps.faces_count_obj:
                faces = len(bpy.context.active_object.data.polygons)
                outputString.extend([CR, ("Faces: ", label_color), (str(faces), value_color)])
            if vieportInfoProps.tris_count_obj:
                outputString.extend([CR, ("Tris: ", label_color), (trisCount(), value_color)])
            if vieportInfoProps.ngons_count_obj:
                outputString.extend([CR, ("Ngons: ", label_color), (ngonsCount(), value_color)])
            if vieportInfoProps.verts_count_obj:
                    verts = len(bpy.context.active_object.data.vertices)
                    outputString.extend([CR, ("Vertex: ", label_color), (str(verts), value_color)])
                    
    else:
        if bpy.context.object.type == 'MESH':
            if vieportInfoProps.faces_count_obj:
                faces = len(bpy.context.active_object.data.polygons)
                outputString.extend([CR, ("Faces: ", label_color), (str(faces), value_color)])
            if vieportInfoProps.tris_count_obj:
                outputString.extend([CR, ("Tris: ", label_color), (trisCount(), value_color)])
            if vieportInfoProps.ngons_count_obj:
                outputString.extend([CR, ("Ngons: ", label_color), (ngonsCount(), value_color)])
            if vieportInfoProps.verts_count_obj:
                    verts = len(bpy.context.active_object.data.vertices)
                    outputString.extend([CR, ("Vertex: ", label_color), (str(verts), value_color)])

    return outputString


def sculptInfo():  
    sculpt_text = []
    vieportInfoProps = bpy.context.scene.vieportInfo
    label_color = vieportInfoProps.label_color
    value_color = vieportInfoProps.value_color
    CR = "Carriage return"     
    tool_settings = bpy.context.scene.tool_settings
    Detail_Size = tool_settings.sculpt.detail_size
    Constant_Detail = tool_settings.sculpt.constant_detail
    if(hasattr(tool_settings.sculpt, 'detail_percent')):
        Detail_Percent = tool_settings.sculpt.detail_percent
    active_brush = bpy.context.tool_settings.sculpt.brush.name            
    detail_refine = tool_settings.sculpt.detail_refine_method
    Detail_Type = tool_settings.sculpt.detail_type_method
    
    if bpy.context.sculpt_object.use_dynamic_topology_sculpting:
        if vieportInfoProps.refine_method:
            if tool_settings.sculpt.detail_type_method == 'RELATIVE':
                sculpt_text.extend([CR, (detail_refine.lower() + ": ", label_color), (str(round(Detail_Size, 2)) + " px", value_color)])
            elif tool_settings.sculpt.detail_type_method == 'CONSTANT':
                sculpt_text.extend([CR, (detail_refine.lower() + ": ", label_color), (str(round(Constant_Detail, 2)) + " %", value_color)])
            elif tool_settings.sculpt.detail_type_method == 'BRUSH':
                sculpt_text.extend([CR, (detail_refine.lower() + ": ", label_color), (str(round(Detail_Percent, 2)) + " %", value_color)])                 
        if vieportInfoProps.detail_type:
            sculpt_text.extend([CR, (Detail_Type.lower(), label_color)])
            
    if vieportInfoProps.brush_radius:
        sculpt_text.extend([CR, ("Radius: ", label_color), (str(tool_settings.unified_paint_settings.size) + " px", value_color)])

    if vieportInfoProps.brush_strength:
        sculpt_text.extend([CR, ("Strenght: ", label_color), (str(round(bpy.data.brushes[active_brush].strength, 3)), value_color)])

    if vieportInfoProps.symmetry_use:
        
        if tool_settings.sculpt.use_symmetry_x and tool_settings.sculpt.use_symmetry_y and tool_settings.sculpt.use_symmetry_z:
            sculpt_text.extend([CR, ("Symmetry: ", label_color), ("X, Y, Z", value_color)])
        elif tool_settings.sculpt.use_symmetry_x and tool_settings.sculpt.use_symmetry_y:
            sculpt_text.extend([CR, ("Symmetry: ", label_color), ("X, Y", value_color)])
        elif tool_settings.sculpt.use_symmetry_x and tool_settings.sculpt.use_symmetry_z:
            sculpt_text.extend([CR, ("Symmetry: ", label_color), ("X, Z", value_color)])
        elif tool_settings.sculpt.use_symmetry_y and tool_settings.sculpt.use_symmetry_z:
            sculpt_text.extend([CR, ("Symmetry: ", label_color), ("Y, Z", value_color)])
        elif tool_settings.sculpt.use_symmetry_x:
            sculpt_text.extend([CR, ("Symmetry: ", label_color), ("X", value_color)])
        elif tool_settings.sculpt.use_symmetry_y:
            sculpt_text.extend([CR, ("Symmetry: ", label_color), ("Y", value_color)])
        elif tool_settings.sculpt.use_symmetry_z:
            sculpt_text.extend([CR, ("Symmetry: ", label_color), ("Z", value_color)])
        else:
            sculpt_text.extend([CR, ("Symmetry: ", label_color), ("OFF", value_color)]) 
             
    return sculpt_text  
            
            

        
        
