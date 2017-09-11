# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Save Cams",
    "author": "Couzar Michel",
    "description": "Store camera positions",
    "version": (0, 0, 4),
    "blender": (2, 7, 6),
    "location": "View3D > Properties > Save Cams",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Camera"}

import bpy

def apply_cam_settings(context):
    
    cam = context.scene.save_cam_collection[obj.save_cam]

def display_toggle_callback(self, context):
    apply_cam_settings(context)
    
class property_collection_save_cam(bpy.types.PropertyGroup):
    cindex = bpy.props.IntProperty(name='Index')
    name = bpy.props.StringProperty(name="Cam name", default="Cam"),
    camLocs = bpy.props.FloatVectorProperty(name = "Cam Location")
    camRots = bpy.props.FloatVectorProperty(name="Cam Rotation")
    flen = bpy.props.FloatProperty(name='Focal Length')
    res_x = bpy.props.IntProperty(name='X Resolution')
    res_y = bpy.props.IntProperty(name='Y Resolution')
    bpy.types.Scene.save_cam_collection_index = bpy.props.IntProperty(
        name = "Cam Scene Index",
        description = "***",
        default = 0,
        min = 0,
        )

class cam_collection_UL(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
    
        cam = item        
        layout.prop(cam, "name", text="", icon_value=icon, emboss=False)        
        icon_cam = 'CAMERA_DATA' 
        
class VIEW3D_cam_panel(bpy.types.Panel):
    bl_label = "Stored Cams"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cams"
    bl_context = "objectmode"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == "CAMERA"
    
    def draw(self, context):
        layout = self.layout  
        
        row = layout.row()
        col = row.column()
        col.template_list("cam_collection_UL", "", context.scene, "save_cam_collection", context.scene, "save_cam_collection_index")
        
        col = row.column()
        sub = col.column(align=True)
        sub.operator("add_cam_from_collection.btn", icon='ZOOMIN', text="")        
        sub.operator("add_from_view.btn", icon = "ZOOM_IN", text = "")
        sub.operator("reassign_cam_from_collection.btn", icon="FILE_REFRESH", text='')
        sub.operator("remove_cam_from_collection.btn", icon='ZOOMOUT', text="")        
        sub = col.column(align=True)
        sub.operator("assign_cam.btn", icon="CAMERA_DATA", text='')
        sub.operator("cam_cycle_up.btn", icon="TRIA_UP", text='')
        sub.operator("cam_cycle_down.btn", icon="TRIA_DOWN", text='')
        
class cam_add(bpy.types.Operator):
    bl_idname = "add_cam_from_collection.btn"
    bl_label = "Add"
    bl_description = "Add cam"
    
    def execute(self, context):
        cam = context.active_object
        item = context.scene.save_cam_collection.add()
        item.name = "Cam"+str(len(context.scene.save_cam_collection))
        item.camLocs = cam.location
        item.camRots = cam.rotation_euler
        item.flen = cam.data.lens
        item.res_x = context.scene.render.resolution_x
        item.res_y = context.scene.render.resolution_y
        context.scene.save_cam_collection_index = len(context.scene.save_cam_collection)-1
        return{'FINISHED'}

class cam_remove(bpy.types.Operator):
    bl_idname = "remove_cam_from_collection.btn"
    bl_label = "Remove"
    bl_description = "Remove cam"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.save_cam_collection) > 0
    
    def execute(self, context):
        index = context.scene.save_cam_collection_index
        context.scene.save_cam_collection.remove(index)
        for cam in context.scene.save_cam_collection:
            if cam.cindex > index:
                cam.cindex = cam.cindex - 1
        if len(context.scene.save_cam_collection) == index:
            context.scene.save_cam_collection_index = index-1
        else:
            context.scene.save_cam_collection_index = index
        return{'FINISHED'}

class cam_assign(bpy.types.Operator):
    bl_idname = "assign_cam.btn"
    bl_label = "Assign"
    bl_description = "Assign cam"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.save_cam_collection) > 0
    
    def execute(self, context):
        cam = context.active_object
        item = context.scene.save_cam_collection[context.scene.save_cam_collection_index]
        cam.location = item.camLocs
        cam.rotation_euler = item.camRots
        cam.data.lens = item.flen
        context.scene.render.resolution_x = item.res_x
        context.scene.render.resolution_y = item.res_y
        return{'FINISHED'}
        
class cam_reassign(bpy.types.Operator):
    bl_idname = "reassign_cam_from_collection.btn"
    bl_label = "Reassign"
    bl_description = "Reassign selected cam"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.save_cam_collection) > 0
    
    def execute(self, context):
        cam = context.active_object
        item = context.scene.save_cam_collection[context.scene.save_cam_collection_index]
        item.camLocs = cam.location
        item.camRots = cam.rotation_euler
        item.flen = cam.data.lens
        item.res_x = context.scene.render.resolution_x
        item.res_y = context.scene.render.resolution_y
        return{'FINISHED'}
    
class cam_add_from_view(bpy.types.Operator):
    bl_idname = "add_from_view.btn"
    bl_label = "Add from View"
    bl_description = "Add selected cam from view"
    
    @classmethod
    def poll(cls, context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':                
                return  area.spaces[0].region_3d.view_perspective != 'CAMERA'

    def execute(self, context):
        bpy.ops.view3d.camera_to_view()
        bpy.ops.add_cam_from_collection.btn()        
        return{'FINISHED'}
    
class cam_cycle_up(bpy.types.Operator):
    bl_idname = "cam_cycle_up.btn"
    bl_label = "Cycle Up"
    bl_description = "Cycle up through cam views"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.save_cam_collection) > 0
    
    def execute(self, context):
        if context.scene.save_cam_collection_index == 0:
            context.scene.save_cam_collection_index = len(context.scene.save_cam_collection) - 1
        else:
            context.scene.save_cam_collection_index -= 1
        if context.active_object.type != 'CAMERA':
            context.scene.objects.active = context.scene.camera
        bpy.ops.assign_cam.btn()
        return{'FINISHED'}
    
class cam_cycle_down(bpy.types.Operator):
    bl_idname = "cam_cycle_down.btn"
    bl_label = "Cycle Down"
    bl_description = "Cycle down through cam views"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.save_cam_collection) > 0
    
    def execute(self, context):
        if context.scene.save_cam_collection_index == len(context.scene.save_cam_collection) - 1:
            context.scene.save_cam_collection_index = 0
        else:
            context.scene.save_cam_collection_index += 1
        if context.active_object.type != 'CAMERA':
            context.scene.objects.active = context.scene.camera
        bpy.ops.assign_cam.btn()
        return{'FINISHED'}
        
def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.save_cam_collection = \
        bpy.props.CollectionProperty(type=property_collection_save_cam)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.save_cam_collection

if __name__ == "__main__":
    register()


