import bpy, bgl, blf, os, importlib, time

bl_info={
"name": "ProSelect",
"description": "Select vertices that are connected through a specific number of edges",
"author": "Kilon ",
"version": (1, 0, 0, 0),
"blender": (2, 77, 0),
"location": "View3D",
"wiki_url": "http://www.kilon-alios.com",
"category": "Object"}




def pro_select_menu_draw(self, context):
    layout = self.layout
    layout.separator()
    scene = context.scene


    col = layout.column(align=True)
    
    row = col.row(align=True)
    row.label(text="by amount of connected verices")
    row = col.row(align=True)
    row.operator("view3d.pro_select",text="Select all")
    
    row = col.row(align=True)

    row.prop(scene,"number_of_verts",text="       amount",slider=True)
  


class ProSelectOperator(bpy.types.Operator):
    bl_idname = "view3d.pro_select"
    bl_label = "ProSelect"


    def execute(self, context):
        svert_index = 0
        ob = bpy.context.active_object
        oldmode = ob.mode
        if oldmode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT') 
        num_of_edges= context.scene.number_of_verts
        trvert = []
        for vert in ob.data.vertices:
            count_edges=0
            for x in range(0,len(ob.data.edges)):
                for verte in ob.data.edges[x].vertices:
                    if verte == vert.index:
                        count_edges = count_edges +1
            if count_edges == num_of_edges:
                trvert.append(vert)
                vert.select = True
        if oldmode != 'OBJECT':
            bpy.ops.object.mode_set(mode=oldmode) 
        return {'FINISHED'}



def register():
    bpy.utils.register_class(ProSelectOperator)
    bpy.types.VIEW3D_MT_edit_mesh_select_similar.append(pro_select_menu_draw)
    bpy.types.Scene.number_of_verts = bpy.props.IntProperty(default=3,soft_min=0,soft_max=100,name="Number of Vertices",description="Number of Vertices connected with edges")

def unregister():

    bpy.utils.unregister_class(ProSelectOperator)

    del bpy.types.Scene.number_of_verts





                
    
