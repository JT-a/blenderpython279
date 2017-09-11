import bpy
import os
from . properties import *
from . operator import *
import bpy.utils.previews

operator_behaviours = ['triangle', 'ngon']
preview_collections = {}

def displayViewportInfoPanel(self, context):
    layout = self.layout   
    vieportInfoProps = context.scene.vieportInfo
    pcoll = preview_collections["nav_main"]
    
    row = layout.row(align=True)    
    if vieportInfoProps.vp_info_enabled:
        row.prop(vieportInfoProps,'vp_info_enabled', text="Viewport info", icon='RESTRICT_VIEW_OFF' )
    else:
        row.prop(vieportInfoProps,'vp_info_enabled', text="Viewport info", icon='RESTRICT_VIEW_ON')
    if vieportInfoProps.vp_info_display_panel:
        icon='TRIA_UP'
    else:
        icon='SCRIPTWIN'
    row.prop(vieportInfoProps, "vp_info_display_panel", icon=icon)

    if vieportInfoProps.vp_info_display_panel:
        
        # Edit mode
        split = layout.split(percentage=0.1)
        split.separator()
        split2 = split.split()
        row = split2.row(align=True)       
        row.prop(vieportInfoProps, "edt_use", text="Edit", icon='EDITMODE_HLT')
        if vieportInfoProps.edt_options:
            icon='TRIA_UP'
        else:
            icon='SCRIPTWIN'
        row.prop(vieportInfoProps, "edt_options", icon=icon)
        if vieportInfoProps.edt_options:
            box = layout.box()
            row = box.row(align=True)
            row.prop(vieportInfoProps, "faces_count_edt")
            row.prop(vieportInfoProps, "tris_count_edt")
            row = box.row(align=True)            
            row.prop(vieportInfoProps, "ngons_count_edt")
            row.prop(vieportInfoProps, "verts_count_edt")
            row = box.row()
            row.prop(vieportInfoProps, "edt_corner", expand=True)
            row = box.row(align=True)
            row.prop(vieportInfoProps, "edt_pos_x")
            row.prop(vieportInfoProps, "edt_pos_y")
                  
        
        # Object mode
        split = layout.split(percentage=0.1)
        split.separator()
        split2 = split.split()
        row = split2.row(align=True) 
        row.prop(vieportInfoProps, "obj_use", text="Object", icon='OBJECT_DATAMODE')
        if vieportInfoProps.obj_options:
            icon='TRIA_UP'
        else:
            icon='SCRIPTWIN'
        row.prop(vieportInfoProps, "obj_options", icon=icon)
        if vieportInfoProps.obj_options:
            box = layout.box()
            row = box.row(align=True)
            row.prop(vieportInfoProps, "faces_count_obj")
            row.prop(vieportInfoProps, "tris_count_obj")
            row = box.row(align=True)            
            row.prop(vieportInfoProps, "ngons_count_obj")
            row.prop(vieportInfoProps, "verts_count_obj")
            if len(bpy.context.selected_objects) >= 2:
                row = box.row()
                row.prop(vieportInfoProps, "multi_obj_enabled")
            row = box.row()
            row.prop(vieportInfoProps, "obj_corner", expand=True)
            row = box.row(align=True)
            row.prop(vieportInfoProps, "obj_pos_x")
            row.prop(vieportInfoProps, "obj_pos_y")
            
        
        # Sculpt mode
        split = layout.split(percentage=0.1)
        split.separator()
        split2 = split.split()
        row = split2.row(align=True) 
        row.prop(vieportInfoProps, "sculpt_use", text="Sculpt", icon='SCULPTMODE_HLT')
        if vieportInfoProps.sculpt_options:
            icon='TRIA_UP'
        else:
            icon='SCRIPTWIN'
        row.prop(vieportInfoProps, "sculpt_options", icon=icon)
        if vieportInfoProps.sculpt_options:
            box = layout.box()
            row = box.row(align=True)           
            row.prop(vieportInfoProps, "brush_radius")
            row.prop(vieportInfoProps, "brush_strength")
            row = box.row()            
            row.prop(vieportInfoProps, "symmetry_use")
            row = box.row()
            box.label("Dyntopo fonctions:")
            row = box.row(align=True)             
            row.prop(vieportInfoProps, "refine_method")
            row.prop(vieportInfoProps, "detail_type")
            row = box.row()
            row.prop(vieportInfoProps, "sculpt_corner", expand=True)
            row = box.row(align=True)
            row.prop(vieportInfoProps, "sculpt_pos_x")
            row.prop(vieportInfoProps, "sculpt_pos_y")


            
        
        # Text options
        split = layout.split(percentage=0.1)
        split.separator()
        split2 = split.split()
        if vieportInfoProps.options_use:
            icon='TRIA_UP'
        else:
            icon='SCRIPTWIN'
        split2.prop(vieportInfoProps, "options_use", text="Options", icon=icon)
        if vieportInfoProps.options_use:
            box = layout.box()
            row = box.row()
            row.prop(vieportInfoProps, "text_font_size")
            row = box.row()
            row.prop(vieportInfoProps, "name_color")
            row = box.row()
            row.prop(vieportInfoProps, "label_color")
            row = box.row()
            row.prop(vieportInfoProps, "value_color")
        
        
def register_pcoll():
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    for img in operator_behaviours:
        full_img_name = (img + ".png")
        img_path = os.path.join(icons_dir, full_img_name)
        pcoll.load(img, img_path, 'IMAGE')

    preview_collections["nav_main"] = pcoll


def unregister_pcoll():

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    
    
