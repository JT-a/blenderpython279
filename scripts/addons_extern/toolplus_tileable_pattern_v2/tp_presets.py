import bpy
from bpy import*
from bpy.props import *





class TP_Tileable_Render_Presets(bpy.types.Operator):
    """Render Presets"""
    bl_idname = "tp_ops.render_presets"
    bl_label = "Render Presets"
    bl_options = {'REGISTER', 'UNDO'}  

    onek = bpy.props.BoolProperty(name="1k Camera",  description="1k Camera > 1024x1024", default=False)     
    twok = bpy.props.BoolProperty(name="2k Camera",  description="2k Camera > 2048x2048", default=False)     
    fourk = bpy.props.BoolProperty(name="4k Camera",  description="4k Camera > 4096x4096", default=False)     
    halfk = bpy.props.BoolProperty(name="1/2k Camera",  description="1/2k Camera > 512x512", default=False)     
    quarderk = bpy.props.BoolProperty(name="1/4k Camera",  description="1/4k Camera > 256x256", default=False)     
    eighthk = bpy.props.BoolProperty(name="1/8k Camera",  description="1/8k Camera > 128x128", default=False)     
    camview = bpy.props.BoolProperty(name="CamView",  description="Camera View", default=True)     

    zero = bpy.props.BoolProperty(name="Clear Location",  description="Clear Location", default=False)   

    def draw(self, context):
        layout = self.layout.column(1)       

        row = layout.row(1)
        row.prop(self, 'zero', text="Clear Location")  

        row = layout.row(1)
        row.prop(self, 'onek', text="1k", icon ="RENDER_REGION")  
        row.prop(self, 'twok', text="2k", icon ="RENDER_REGION")  
        row.prop(self, 'fourk', text="4k", icon ="RENDER_REGION")  

        row = layout.row(1)
        row.prop(self, 'halfk', text="1/2k", icon ="RENDER_REGION")  
        row.prop(self, 'quarderk', text="1/4k", icon ="RENDER_REGION")  
        row.prop(self, 'eighthk', text="1/8k", icon ="RENDER_REGION")  

        row = layout.row(1)
        row.operator("help.tileable_cam","Help", icon ="INFO") 
        row.operator("view3d.viewnumpad", text="CamView", icon ="OUTLINER_DATA_CAMERA").type='CAMERA'
        row.operator("render.render", text="Render", icon='RENDER_STILL')

    def execute(self, context):
                         
        for i in range(self.onek):
            print(self)
            self.report({'INFO'}, "1/8k_128x128")   

            bpy.context.object.name = "1/8k_RenderResult"
            bpy.context.scene.render.resolution_x = 128
            bpy.context.scene.render.resolution_y = 128

        for i in range(self.twok):
            print(self)
            self.report({'INFO'}, "1/4K_256x256")   

            bpy.context.object.name = "1/4k_RenderResult"
            bpy.context.scene.render.resolution_x = 256
            bpy.context.scene.render.resolution_y = 256
            
        for i in range(self.fourk):
            print(self)
            self.report({'INFO'}, "1/2K_512x512")   

            bpy.context.object.name = "1/2k_RenderResult"
            bpy.context.scene.render.resolution_x = 512
            bpy.context.scene.render.resolution_y = 512

        for i in range(self.onek):
            print(self)
            self.report({'INFO'}, "1K_1024x1024")   

            bpy.context.object.name = "1K_RenderResult"
            bpy.context.scene.render.resolution_x = 1024
            bpy.context.scene.render.resolution_y = 1024

        for i in range(self.twok):
            print(self)
            self.report({'INFO'}, "2K_2048x2048")   

            bpy.context.object.name = "2K_RenderResult"
            bpy.context.scene.render.resolution_x = 2048
            bpy.context.scene.render.resolution_y = 2048
            
        for i in range(self.fourk):
            print(self)
            self.report({'INFO'}, "4K_4096x4096")   

            bpy.context.object.name = "4K_RenderResult"
            bpy.context.scene.render.resolution_x = 4096
            bpy.context.scene.render.resolution_y = 4096

        bpy.context.scene.render.resolution_percentage = 100  
        
        bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, 0, 50), rotation=(0, 0, 0))
        bpy.context.object.data.type = 'ORTHO'
        bpy.context.object.data.ortho_scale = 34.68

        bpy.ops.object.lamp_add(type='SUN', radius=1, view_align=False, location=(0, 0, 40))                
        bpy.context.object.data.energy = 0.25

        for i in range(self.zero):            
            bpy.ops.transform.translate(value=(17.34, 17.34, 50))

        bpy.context.object.name = "Camera_Pattern"

        return {'FINISHED'}



bpy.types.Scene.Render_Setup = bpy.props.EnumProperty(items = [("a", "128x128", ""),
                                                               ("b", "256x256", ""),
                                                               ("c", "512x512", ""),
                                                               ("d", "1k > 1024x1024", ""),
                                                               ("e", "2k > 2048x2048", ""),
                                                               ("f", "4k > 4096x4096", "")],description="Render Resolution")

class TP_Instance_RenderRes(bpy.types.Operator):
    """Render Setup"""
    bl_idname = "tp_ops.instances_render_res"
    bl_label = "Render Resolution"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):
        set = bpy.context.scene.Render_Setup                

        if set == 'a':
            bpy.context.scene.render.resolution_x = 128
            bpy.context.scene.render.resolution_y = 128

        if set == 'b':
            bpy.context.scene.render.resolution_x = 256
            bpy.context.scene.render.resolution_y = 256
            
        if set == 'c':
            bpy.context.scene.render.resolution_x = 512
            bpy.context.scene.render.resolution_y = 512

        if set == 'd':
            bpy.context.scene.render.resolution_x = 1024
            bpy.context.scene.render.resolution_y = 1024

        if set == 'e':
            bpy.context.scene.render.resolution_x = 2048
            bpy.context.scene.render.resolution_y = 2048

        if set == 'f':
            bpy.context.scene.render.resolution_x = 4096
            bpy.context.scene.render.resolution_y = 4096

        bpy.context.scene.render.resolution_percentage = 100  
           
        return {'FINISHED'}


class TP_Instance_Render(bpy.types.Operator):
    """Apply choosen Resolution"""
    bl_idname = "tp_ops.instances_res_apply"
    bl_label = "Render Images"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context):             
        bpy.ops.tp_ops.instances_render_res()
        return {'FINISHED'}


class TP_Instance_Render_Edit(bpy.types.Operator):
    """Render choosen Resolution"""
    bl_idname = "tp_ops.instances_render_edit"
    bl_label = "Render Images"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context): 
        bpy.ops.object.editmode_toggle()                    
        bpy.ops.tp_ops.instances_render_res()
        bpy.ops.render.render()
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}


class TP_Render_Window(bpy.types.Operator):
    """Display Render in a new Window"""
    bl_idname = "tp_ops.tp_view"
    bl_label = "RenderView"
    bl_options = {'REGISTER', 'UNDO'}  

    def execute(self, context): 
        bpy.context.scene.render.display_mode = 'WINDOW'
        bpy.ops.render.view_show()

        return {'FINISHED'}


def register():

    bpy.utils.register_class(TP_Tileable_Render_Presets)
    bpy.utils.register_class(TP_Instance_RenderRes)
    bpy.utils.register_class(TP_Instance_Render)
    bpy.utils.register_class(TP_Instance_Render_Edit)
    bpy.utils.register_class(TP_Render_Window)

def unregister():

    bpy.utils.unregister_class(TP_Tileable_Render_Presets)
    bpy.utils.unregister_class(TP_Instance_RenderRes)
    bpy.utils.unregister_class(TP_Instance_Render)
    bpy.utils.unregister_class(TP_Instance_Render_Edit)
    bpy.utils.unregister_class(TP_Render_Window)

if __name__ == "__main__":
    register()

