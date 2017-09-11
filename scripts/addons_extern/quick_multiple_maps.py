import bpy, os, ntpath
from bpy.props import StringProperty

bl_info = {
    "name": "Quick Multiple Maps",
    "author": "Aurelien Chane-Foc",
    "version": (1, 1),
    "blender": (2, 78, 0),
    "location": "Node Editor > Texture > Multiple Maps",
    "description": "Fast import set of texture map.",
    "category": "Node"}

yeColor = ["Color", "Diffuse", "Col", "Dif"]
noColor = ["Height", "Displacement", "Normal", "Bump", "Ao"]

class View3dPanel():    
    bl_space_type="NODE_EDITOR"
    bl_region_type="TOOLS"
    bl_category="Texture"

#Ui
class PanelA(View3dPanel,bpy.types.Panel):
    
    bl_label="Multiple Maps"
    
    def draw(self,context):
        layout=self.layout
        layout=layout.box()
        col=layout.column(align = True)
        col.prop(context.scene, "mapPath", text="Texture Map")
        col.operator("my.button", text="Import")
        col = layout.column()
        
#Event 

class OBJECT_OT_Button(bpy.types.Operator):
    bl_idname = "my.button"
    bl_label = "Button"
    number = bpy.props.IntProperty()
    row = bpy.props.IntProperty()
    loc = bpy.props.StringProperty()
 
    def execute(self, context):
        main(bpy.path.abspath(bpy.data.scenes[context.scene.name].mapPath), self, bpy.data.scenes[context.scene.name].mapPath)
        return{'FINISHED'}    
        
def main(path, self, pure):

    convRel = False
    
    if path != pure:
        convRel = True
    
    dir = os.path.dirname(path)
    ext = os.path.splitext(path)[1]
    pattern = os.path.splitext(ntpath.basename(path))[0].rsplit("_", 1)[0]
    
    if bpy.context.object.active_material:
        
        mat = bpy.data.materials[bpy.context.object.active_material.name]
        nodes = mat.node_tree.nodes
        i = 0
        
        for file in os.listdir(dir):
            try:
                tempTest = os.path.splitext(ntpath.basename(file))[0].rsplit("_", 1)
                if file.endswith(ext) and tempTest[0] == pattern:
                    node_texture = nodes.new(type="ShaderNodeTexImage")
                    node_texture.image = bpy.data.images.load(dir+"\\"+file)
                    if convRel:
                        node_texture.image = bpy.data.images.load(bpy.path.relpath(dir+"\\"+file))
                    node_texture.label = tempTest[1]
                    try:
                        for item in yeColor:
                            if item.lower() in tempTest[1].lower():
                                node_texture.color_space = "COLOR"
                                print("rrrrrrrr  :"+tempTest[1].lower())
                                break
                                
                            else:
                                node_texture.color_space = "NONE"
                    except:
                        pass
                    
                    if i % 2 == 0:
                        node_texture.location = 0,-250/2*i
                    else:
                        node_texture.location = 170,-250/2*i
                    i+=1
                    
            except:
                pass
                
            
    else:
        self.report({'WARNING'}, "No Material in stack")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.mapPath = StringProperty(name="ImportMaps", 
        description="Select any map of desired set",
        subtype='FILE_PATH')
        
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.mapPath

if __name__ == "__main__":
    register()