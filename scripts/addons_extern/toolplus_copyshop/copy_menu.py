import bpy


class View3D_TP_Copy_Origin_Menu(bpy.types.Menu):
    """Set Origin"""
    bl_label = "Set Origin"
    bl_idname = "tp_menu.copyshop_origin_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("tp_ops.origin_plus_z", text="Top", icon="LAYER_USED")  
        layout.operator("object.origin_set", text="Middle", icon="LAYER_USED").type='ORIGIN_GEOMETRY'
        layout.operator("tp_ops.origin_minus_z", text="Bottom", icon="LAYER_USED")


class View3D_TP_Copy_Optimize_Menu(bpy.types.Menu):
    """Optimize"""
    bl_label = "Optimize"
    bl_idname = "tp_menu.copyshop_optimize_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.make_links_data","Set", icon="LINKED").type='OBDATA'
        layout.operator("tp_ops.make_single","Clear", icon="UNLINKED")                        
        layout.operator("object.select_linked", text="Select Linked", icon="RESTRICT_SELECT_OFF")   
        layout.operator("object.join", text="Join all", icon="AUTOMERGE_ON")   


class View3D_TP_Copy_Array_Menu(bpy.types.Menu):
    """ArrayTools"""
    bl_label = "ArrayTools"
    bl_idname = "tp_menu.copyshop_array_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("tp_ops.x_array", text="X Array")    
        layout.operator("tp_ops.y_array", text="Y Array")    
        layout.operator("tp_ops.z_array", text="Z Array")   
        
        
class View3D_TP_Copy_Menu(bpy.types.Menu):
    """TP CopyShop :)"""
    bl_label = "TP CopyShop :)"
    bl_idname = "tp_menu.copyshop_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("mft.radialclone", text="Radial Clone", icon="FILE_REFRESH")
        layout.operator("tp_ops.copy_to_faces", text="Copy to Faces",icon="UV_FACESEL")        
        layout.operator("tp_ops.copy_to_cursor", text="Copy to Cursor", icon="NEXT_KEYFRAME")
        layout.operator("object.simplearewo", text="ARewO Replicator", icon="FRAME_NEXT") 

        layout.separator()
        
        layout.menu("tp_menu.copyshop_array_menu", icon="MOD_ARRAY")
        
        layout.separator()
        
        layout.menu("tp_menu.copyshop_optimize_menu", icon="UV_SYNC_SELECT")

        layout.separator()
        
        layout.menu("tp_menu.copyshop_origin_menu", icon="LAYER_ACTIVE")
                




def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.register_module(__name__)

if __name__ == "__main__":
    register()


