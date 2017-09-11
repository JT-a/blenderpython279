bl_info = {
    "name": "Archi-UV",
    "author": "Gertjan Van den Broek",
    "version": (0, 1),
    "blender": (2, 7, 0),
    "location": "3D View, Toolbox",
    "description": "Assists you in quickly unwrapping and aligning UVs'of different meshes",
    "wiki_url": ""
                "",
    "tracker_url": ""
                   "",
    "support": 'COMMUNITY',
    "category": "Object"}


if "bpy" in locals():
    import imp
    imp.reload(architools_vao)
    imp.reload(architools_uv)
    imp.reload(architools_util)
    print("Reloaded modules")
else:
    from . import architools_vao
    from . import architools_uv
    from . import architools_util
#    import architools_vao
#    import architools_uv
    print("Imported Modules")
    
import bpy
import os
#os.system('cls')

# the main panel
class ArchiUVPanel(bpy.types.Panel):
    bl_label = "Archi-UV"
    bl_idname = "archiuvtools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'Tools'
    
    def draw(self,context):
        layout = self.layout
        obj = context.object
        scene = context.scene


        layout.label("Entire UV:")
        row = layout.row(align=True)
        row.prop(scene, "archiuv_operationOrigin")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("archiuv_unwrap.button" ,"" , icon="LOOP_BACK").rotationMod = -90
        row.operator("archiuv_unwrap.button" ,"" , icon="BACK").rotationMod = -45
        row.operator("archiuv_unwrap.button" ,"" , icon='NODE_SEL').rotationMod = 0 
        row.operator("archiuv_unwrap.button" ,"" , icon="FORWARD").rotationMod = 45
        row.operator("archiuv_unwrap.button" ,"" , icon="LOOP_FORWARDS").rotationMod = 90
        
        layout.label("Vertex AO")
        row = layout.row()
        row.operator("archiuv_vao_addmap.button")
        row = layout.row(align=True)
        row.prop(scene, "archiuv_vao_horizontalsurfacescan", "Exclude Horizontal")
#        row.prop(scene, "archiuv_vao_planarthresshold", "Angle")
        row = layout.row()
        row.operator("archiuv_vao_local.button", "local", icon="MATSPHERE")

        row = layout.row(align=True)
        row.operator("archiuv_vao_cursor.button", "BOT", icon="GROUP_VERTEX").topbot='BOT'
        row.operator("archiuv_vao_cursor.button", "TOP", icon="GROUP_VERTEX").topbot='TOP'

        layout.row()
        layout.label("Utils")
        row = layout.row()
        row.operator("wm.call_menu", text="Select Similar", icon = 'RESTRICT_SELECT_OFF').name="architools_selectsimilar.menu"
        row = layout.row()
        row.operator("archiutil_applysharedtransform.button")
        row = layout.row()
        row.prop(scene, "archiutil_copymods_array", "Include Array")
        row.prop(scene, "archiutil_copymods_edgesplit", "Include Edge Split")

        row = layout.row()
        row.operator("archiutil_copymods.button")


def register():
    bpy.utils.register_module(__name__);


def unregister():
    bpy.utils.unregister_module(__name__);



if __name__ == "__main__":
    register()
