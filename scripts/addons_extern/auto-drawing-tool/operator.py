import bpy
from . import auto_drawing_tool

# Operation class.
class AutoDrawOperation(bpy.types.Operator):
    bl_idname = "scene.auto_drawing" # Access by bpy.ops.scene.auto_drawing.
    bl_label = "Set Auto drawing"
    bl_description = "Make auto drawing settings."
    bl_options = {'REGISTER', 'UNDO'}
    
    # Input after execution------------------------
    #  Reference by self.~ in execute().
    basic_check = bpy.props.BoolProperty(
        name = "1.Build Modifier & Freestyle",
        description = "Activate build modifier and freestyle.",
        default = True
    )
    blrender_check = bpy.props.BoolProperty(
        name = "2.Blender Render",
        description = "Go to Blender render engine.",
        default = True
    )
    world_check = bpy.props.BoolProperty(
        name = "3.Apply White World",
        description = "Set white world for Blender render",
        default = True
    )
    material_check = bpy.props.BoolProperty(
        name = "4.Apply White Shadeless Material",
        description = "Set shadeless white material.",
        default = True
    )
    modifier_check = bpy.props.BoolProperty(
        name = "5.Subsurf Modifier",
        description = "Apply subdivision surface.",
        default = False
    )
    line_thick_float = bpy.props.FloatProperty(
        name = "Line Thickness",
        description = "Set line thickness.",
        default = 2
    )
    freestyle_select = bpy.props.EnumProperty(
        name = "Freestyle Preset",
        description = "Set Freestyle Preset",
        items = [('NONE', 'NONE', "None."),
                ('MARKER_PEN', 'MARKER_PEN', "Marker pen."),
                ('BRUSH_PEN', 'BRUSH_PEN', "Brush pen."),
                ('SCRIBBLE', 'SCRIBBLE', "Scribble."),
                ('FREE_HAND', 'FREE_HAND', "Free hand."),
                ('CHILDISH', 'CHILDISH', "Childish.")]
    )
    sort_select = bpy.props.EnumProperty(
        name = "Change Drawing Order(Only for MESH)",
        description = "Sort faces of mesh for build modifier.",
        items = [('NONE', 'NONE', "None."),
                ('REVERSE', 'REVERSE', "Reverse."),
                ('CURSOR_DISTANCE', 'CURSOR_DISTANCE', "Draw from a nearest point to cursor."),
                ('CAMERA', 'CAMERA', "Draw from a nearest point to camera."),
                ('VIEW_ZAXIS', 'VIEW_ZAXIS', "Draw along with Z axis."),
                ('VIEW_XAXIS', 'VIEW_XAXIS', "Draw along with X axis."),
                ('SELECTED', 'SELECTED', "Draw from selected point."),
                ('MATERIAL', 'MATERIAL', "Draw along with material.")]
    )
    divide_frame_select = bpy.props.EnumProperty(
        name = "Draw Objects In Turn.",
        description = "Divide frame per object for build modifier.",
        items = [('NONE', 'NONE', "None."),
                ('SIMPLE_DIVIDE', 'SIMPLE', "Divide frame simply from order of object list."),
                ('ALONG_CURVE', 'ALONG_CURVE', "Divide frame from order of nearer object to curve.")]
    )
    # -----------------------------------------

    '''
    @classmethod
    def poll(cls, context):
     return (context.object is not None)
    '''
    
    # Execute main function.
    def execute(self, context):
        sce = context.scene
        auto_drawing_tool.autoDraw(frame_range=[sce.draw_start_frame, sce.draw_end_frame],
             basic=self.basic_check, bl_render=self.blrender_check,
             material=self.material_check, world=self.world_check, modifier=self.modifier_check,
             sort=self.sort_select, freestyle_preset=self.freestyle_select, line_thick=self.line_thick_float,
             divide_frame=self.divide_frame_select, sort_along_curve=None)
        
        # Finish at end frame.
        bpy.context.scene.frame_current = sce.draw_end_frame
        
        # Finish with cursor at center.
        #bpy.context.scene.cursor_location = [0,0,0]

        return {'FINISHED'}

# Menu and input settings.
class AutoDrawingPanel(bpy.types.Panel):
    bl_label = "Auto Drawing Tool"
    bl_idname = "auto_drawing_tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS" # Menu in toolsheld.
    bl_category = "Animate" # Menu on Tools tab.
    bl_context = (("objectmode")) # In object mode.
    
    # Input on Menu.
    def draw(self, context):
         sce = context.scene
         layout = self.layout
         
         row1 = layout.row()
         row1.prop(sce, "draw_start_frame") # bpy.types.Scene.draw_start_frame.
         row1.prop(sce, "draw_end_frame") # bpy.types.Scene.draw_end_frame.
         # Execute button for operator class.
         layout.operator(AutoDrawOperation.bl_idname)
