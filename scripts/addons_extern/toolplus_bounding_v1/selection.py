import bpy
from bpy import*
from bpy.props import  *






class VIEW3D_TP_BBoxSelection(bpy.types.Operator):
    """Select all existing bbox* in the scene"""
    bl_idname = "tp_ops.bbox_select_box"
    bl_label = "Select all BBox"     

    types_sel =  [("tp_01"    ,"CubeBox "  ," "   ,""  ,1),
                  ("tp_02"    ,"WireBox "  ," "   ,""  ,2), 
                  ("tp_03"    ,"CylBox "   ," "   ,""  ,3)]

    bpy.types.Scene.tp_sel = bpy.props.EnumProperty(name = "Select Boundings", default = "tp_01", description = "select all bounding geometry in the scene", items = types_sel)

    def execute(self, context):

        if context.scene.tp_sel == "tp_01":
            print(self)
            self.report({'INFO'}, "Select all BBox")
            bpy.ops.object.select_pattern(pattern="_bbox*")

        if context.scene.tp_sel == "tp_02":
            print(self)
            self.report({'INFO'}, "Select all WireBox")
            bpy.ops.object.select_pattern(pattern="_bwire*")

        if context.scene.tp_sel == "tp_03":
            print(self)
            self.report({'INFO'}, "Select all CylinderBox")
            bpy.ops.object.select_pattern(pattern="_bcyl*")

        return {'FINISHED'}     



def register():
    bpy.utils.register_module(__name__)
     
def unregister():
    bpy.utils.unregister_module(__name__)
 
if __name__ == "__main__":
    register()






















