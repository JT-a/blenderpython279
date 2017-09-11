import bpy

from . operator import drawTextCallback,vp_info_handle, updateTextProperties


class viewportInfoCollectionGroup(bpy.types.PropertyGroup):
    updated_edt_text = []
    updated_obj_text = []
    update_toggle_mode = bpy.props.StringProperty()
    obj_pre = []
    def DrawVieportInfoProperties(self, context):
        updateTextProperties(context)
        if bpy.context.scene.vieportInfo.vp_info_enabled != False:
            if vp_info_handle:
                bpy.types.SpaceView3D.draw_handler_remove(vp_info_handle[0], 'WINDOW')
            args = (self, context)
            vp_info_handle[:] = [bpy.types.SpaceView3D.draw_handler_add(drawTextCallback, args, 'WINDOW', 'POST_PIXEL')]

        else:
            if vp_info_handle:
                bpy.types.SpaceView3D.draw_handler_remove(vp_info_handle[0], 'WINDOW')
                vp_info_handle[:] = []

    vp_info_display_panel = bpy.props.BoolProperty(
        name="",
        description="Display selected options in the viewport",
        default=False)

    vp_info_enabled = bpy.props.BoolProperty(
        description="Switch enabled/desable",
        default=False,
        update=DrawVieportInfoProperties)

    # EDIT PROPERTIES
    edt_use = bpy.props.BoolProperty(
        name="Edit mode",
        description="Display of the information in edit mode",
        default=True
    )
    edt_options = bpy.props.BoolProperty(
        name="",
        description="Options of the edit mode",
        default=False)
    tris_count_edt = bpy.props.BoolProperty(
        name="Tris count",
        default=True
    )
    verts_count_edt = bpy.props.BoolProperty(
        name="Vertex count",
        default=False
    )
    faces_count_edt = bpy.props.BoolProperty(
        name="Faces count",
        default=False
    )
    ngons_count_edt = bpy.props.BoolProperty(
        name="Ngons count",
        default=True
    )
    edt_corner = bpy.props.EnumProperty(
        items=(('1', "Top L", ""),
               ('2', "Top R", ""),
               ('3', "Bot L", ""),
               ('4', "Bot R", "")),
        default='1',
        name=" ")

    edt_pos_x = bpy.props.IntProperty(name="Pos X",
                                      default=29,
                                      min=0, max=500)

    edt_pos_y = bpy.props.IntProperty(name="Pos Y",
                                      default=75,
                                      min=0, max=500)

    # OBJECT PROPERTIES
    obj_use = bpy.props.BoolProperty(
        name="Object mode",
        description="Display of the information in object mode",
        default=True
    )
    obj_options = bpy.props.BoolProperty(
        name="",
        description="Options of the object mode",
        default=False
    )
    tris_count_obj = bpy.props.BoolProperty(
        name="Tris count",
        default=True
    )
    verts_count_obj = bpy.props.BoolProperty(
        name="Vertex count",
        default=False
    )
    faces_count_obj = bpy.props.BoolProperty(
        name="Face count",
        default=False
    )
    ngons_count_obj = bpy.props.BoolProperty(
        name="Ngon count",
        default=True
    )

    obj_corner = bpy.props.EnumProperty(
        items=(('1', "Top L", ""),
               ('2', "Top R", ""),
               ('3', "Bot L", ""),
               ('4', "Bot R", "")),
        default='1',
        name=" ")
    multi_obj_enabled = bpy.props.BoolProperty(
        name="Multi object",
        description="Display the options for every selected objects",
        default=True,
    )
    obj_pos_x = bpy.props.IntProperty(
        name="Pos X",
        default=29,
        min=0, max=500)
    obj_pos_y = bpy.props.IntProperty(
        name="Pos Y",
        default=75,
        min=0, max=500)

    # SCULPT PROPERTIES
    sculpt_use = bpy.props.BoolProperty(
        name="Sculpt mode",
        description="Display of the information in sculpt mode",
        default=True
    )
    sculpt_options = bpy.props.BoolProperty(
        name="",
        description="Options of the sculpt mode",
        default=False)
    refine_method = bpy.props.BoolProperty(
        name="Detail refine method",
        default=True
    )
    detail_type = bpy.props.BoolProperty(
        name="Detail type method",
        default=True
    )
    brush_radius = bpy.props.BoolProperty(
        name="Brush radius",
        default=True
    )
    brush_strength = bpy.props.BoolProperty(
        name="Brush strenght",
        default=True
    )
    symmetry_use = bpy.props.BoolProperty(
        name="Symetry axis",
        default=True
    )
    sculpt_corner = bpy.props.EnumProperty(
        items=(('1', "Top L", ""),
               ('2', "Top R", ""),
               ('3', "Bot L", ""),
               ('4', "Bot R", "")),
        default='1',
        name=" ")
    sculpt_pos_x = bpy.props.IntProperty(name="Pos X",
                                         default=29,
                                         min=0, max=500)
    sculpt_pos_y = bpy.props.IntProperty(name="Pos Y",
                                         default=75,
                                         min=0, max=500)

    # CUSTOM TEXT PROPERTIES
    options_use = bpy.props.BoolProperty(
        name="Options",
        description="Size and color text",
        default=False)
    text_font_size = bpy.props.IntProperty(
        name="Font",
        description="Font size",
        default=18,
        min=10, max=50)
    name_color = bpy.props.FloatVectorProperty(
        name="Name",
        default=(0.7, 1.0, 0.7),
        min=0, max=1,
        subtype='COLOR')
    label_color = bpy.props.FloatVectorProperty(
        name="Label",
        default=(0.65, 0.8, 1.0),
        min=0, max=1,
        subtype='COLOR')
    value_color = bpy.props.FloatVectorProperty(
        name="Value",
        default=(0.9, 0.9, 0.9),
        min=0, max=1,
        subtype='COLOR')

    # DISPLAY COLOR PROPERTIES    
    display_color_enabled = bpy.props.BoolProperty(
        name="Mesh check enabled",
        description="Display faces color",
        default=False)
    active_shade = bpy.props.StringProperty()
    matcap_enabled = bpy.props.BoolProperty(
        name="Mesh check matcap",
        description="Define if matcap enabled or disabled",
        default=False)
    save_mat = []
    update_mode_enabled = bpy.props.BoolProperty(
        default=False)

    # SELECTION TRIS/NGONS PROPERTIES
    select_mode = bpy.props.StringProperty()
