
bl_info = {
        "name": "Areatype Toggle Switch",
        "description":"Timeline/Node Editor, 3d View/Image Editor, Prefs/Text Editor",
        "author":"dustractor, meta-androcto",
        "version":(0,1),
        "blender":(2,78,0),
        "location":"First button on the header.",
        "warning":"",
        "wiki_url":"",
        "category": "Addon Factory"
        }

import bpy

class AREATYPE_OT_switch(bpy.types.Operator):
    bl_idname = "areatype.switch"
    bl_label = "areatype.switch"
    switchto = bpy.props.StringProperty()
    def execute(self,context):
        context.area.type = self.switchto
        return {"FINISHED"}

def timedraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="NODETREE").switchto = "NODE_EDITOR"

def nodedraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="TIME").switchto = "TIMELINE"

def prefsdraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="TEXT").switchto = "TEXT_EDITOR"

def textdraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="PREFERENCES").switchto = "USER_PREFERENCES"

def viewdraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="IMAGE_COL").switchto = "IMAGE_EDITOR"

def uvdraw(self,context):
    layout = self.layout
    layout.operator("areatype.switch",text="",icon="MESH_CUBE").switchto = "VIEW_3D"

def register():
    bpy.types.TIME_HT_header.prepend(timedraw)
    bpy.types.NODE_HT_header.prepend(nodedraw)
    bpy.types.USERPREF_HT_header.prepend(prefsdraw)
    bpy.types.TEXT_HT_header.prepend(textdraw)
    bpy.types.IMAGE_HT_header.prepend(uvdraw)
    bpy.types.VIEW3D_HT_header.prepend(viewdraw)
    bpy.utils.register_module(__name__)

def unregister():
    bpy.types.TIME_HT_header.remove(timedraw)
    bpy.types.NODE_HT_header.remove(nodedraw)
    bpy.types.USERPREF_HT_header.remove(prefsdraw)
    bpy.types.TEXT_HT_header.remove(textdraw)
    bpy.types.IMAGE_HT_header.remove(uvdraw)
    bpy.types.VIEW3D_HT_header.remove(viewdraw)
 
    bpy.utils.unregister_module(__name__)
    
# The End
if __name__ == "__main__":
    register()
