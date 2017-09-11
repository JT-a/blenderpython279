bl_info = {
    "name": "Camera Tools",
    "author": "Alfonso Annarumam",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "View3D > Tools",
    "description": "Manage Camera anche create path for animation ",
    "warning": "",
    "wiki_url": "",
    "category": "Camera",
    }


import bpy
from bpy.types import Menu, Panel, UIList, PropertyGroup
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, FloatProperty, PointerProperty



def main(context):
    loc_list = []
    rot_list = []
    sec_list =[]
    scene = context.scene
    
    fps = scene.render.fps
    
    
    cam_list = scene.cameraitems
    
    for cam in cam_list:
        name = cam.name
        sec = cam.sec
        ob = scene.objects[name]
        if ob.type == 'CAMERA':
            
            loc_list.append(ob.location)
            rot_list.append(ob.rotation_euler)
            sec_list.append(sec)

    bpy.ops.object.camera_add()
    context.object.name = "CameraMorph"
    cam = context.object
    scene.camera = cam
    for loc,rot,sec in zip(loc_list,rot_list,sec_list):
        
        cam.location = loc
        cam.rotation_euler = rot
        #print(matr)
        bpy.ops.anim.keyframe_insert(type='BUILTIN_KSI_LocRot')
        frame_range = sec*fps
        scene.frame_current += frame_range

class UICameraOperator(bpy.types.Operator):
    """Make Render Camera"""
    bl_idname = "camera.ui_camera_operator"
    bl_label = "UI Camera Operator"
    
    name = bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        
        name = self.name
        scene = context.scene
        camera = scene.objects[name]
        
        scene.camera = camera
        
        return {'FINISHED'}
class CameraItem_remove(bpy.types.Operator):
    """Remove and select a new layer group"""
    bl_idname = "scene.camera_item_remove"
    bl_label = "Remove Camera to list for Camera Tools"
    
    camera_idx = bpy.props.IntProperty()
    
#    @classmethod
#    def poll(cls, context):
#        return bool(context.scene)

    def execute(self, context):
        scene = context.scene
        camera_idx = self.camera_idx

        scene.cameraitems.remove(camera_idx)
        if scene.cameraitems_index > len(scene.cameraitems) - 1:
            scene.cameraitems_index = len(scene.cameraitems) - 1

        return {'FINISHED'}



class CameraItem_move(bpy.types.Operator):
    """Add and select a new layer group"""
    bl_idname = "scene.camera_item_move"
    bl_label = "Move Camera in list for Camera Tools"
    
    move = StringProperty()
    camera_idx = IntProperty()
    
    @classmethod
    def poll(cls, context):
        return bool(context.scene)

    def execute(self, context):
        scene = context.scene
        cameraitems = scene.cameraitems
        camera_idx = self.camera_idx
        if self.move == 'UP':
            cameraitems.move(camera_idx, camera_idx-1)
            scene.cameraitems_index = camera_idx-1    
        if self.move == 'DOWN':
            cameraitems.move(camera_idx, camera_idx+1)
            scene.cameraitems_index = camera_idx+1

        return {'FINISHED'}


class CameraItem_add(bpy.types.Operator):
    """Add and select a new layer group"""
    bl_idname = "scene.camera_item_add"
    bl_label = "Add Camera to list for Camera Tools"

    

    def execute(self, context):
        scene = context.scene
        cameraitems = scene.cameraitems
        
        for cam in context.selected_objects:
            if cam.type == 'CAMERA':
                 
                camera_idx = len(cameraitems)
                camera_item = cameraitems.add()
                camera_item.name = cam.name
                
                scene.cameraitems_index = camera_idx

        return {'FINISHED'}



class CameraItem(PropertyGroup):
    #use_toggle = BoolProperty(name="", default=False)
    #use_wire = BoolProperty(name="", default=False)
    #use_lock = BoolProperty(name="", default=False)

    camera = StringProperty(name="Cameras")
    sec = FloatProperty(default=2.0, description="Second from the next camera keyframe", name="Time",min=0, soft_min=0, soft_max=360.0)
    
class CameraItemsList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        camera_item = item

        

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(camera_item, "name", text="", emboss=False)
            layout.prop(camera_item, "sec", text="", emboss=False)
            # lock operator
#            use_lock = layer_group.use_lock
#            icon = 'LOCKED' if use_lock else 'UNLOCKED'
#            op = layout.operator("scene.namedlayer_lock_all", text="", emboss=False, icon=icon)
#            op.use_lock = use_lock
#            op.group_idx = index
#            op.layer_idx = -1

#            # view operator
#            icon = 'RESTRICT_VIEW_OFF' if layer_group.use_toggle else 'RESTRICT_VIEW_ON'
#            op = layout.operator("scene.namedlayer_toggle_visibility", text="", emboss=False, icon=icon)
#            op.use_spacecheck = use_spacecheck
#            op.group_idx = index
#            op.layer_idx = -1

#            # wire operator
#            use_wire = layer_group.use_wire
#            icon = 'WIRE' if use_wire else 'POTATO'
#            op = layout.operator("scene.namedlayer_toggle_wire", text="", emboss=False, icon=icon)
#            op.use_wire = not use_wire
#            op.group_idx = index
#            op.layer_idx = -1

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            
            
class Camera_items_Panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = "Display"
    bl_label = "Camera Morph"
    bl_options = {'DEFAULT_CLOSED'}

    

    def draw(self, context):
        scene = context.scene
        group_idx = scene.cameraitems_index

        layout = self.layout
        row = layout.row()
        row.template_list("CameraItemsList", "", scene, "cameraitems", scene, "cameraitems_index")

        col = row.column(align=True)
        col.operator("scene.camera_item_add", icon='ZOOMIN', text="")
        col.operator("scene.camera_item_remove", icon='ZOOMOUT', text="").camera_idx = group_idx
        up = col.operator("scene.camera_item_move", icon='TRIA_UP', text="")
        down =col.operator("scene.camera_item_move", icon='TRIA_DOWN', text="")
        up.camera_idx = group_idx
        down.camera_idx = group_idx
        up.move = 'UP'
        down.move = 'DOWN'
        
        row = layout.row()
        row.operator("scene.camera_morph", text="Camera morph")
#        if bool(scene.layergroups):
#            layout.prop(scene.layergroups[group_idx], "layers", text="", toggle=True)
#            layout.prop(scene.layergroups[group_idx], "name", text="Name:")


class UI_Camera_panel(bpy.types.Panel):
    """Manage Camera"""
    bl_label = "Camera Manager"
    bl_idname = "OBJECT_PT_Camera_Interface"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Display"
    
    def draw(self, context):
        
        layout = self.layout
        
        riga = layout.row()
        
        riga.label(text="Camera in Scene")
        
        objs = context.scene.objects
        
        for obj in objs:
            
            
            if obj.type == 'CAMERA':
                riga2 = layout.row()
                
                riga2.prop(obj, "name", text="")
                riga2.prop(obj, "select", text="")
                riga2.prop(obj, "hide", text="")
                riga2.operator("camera.ui_camera_operator", text="", icon='OUTLINER_DATA_CAMERA').name = obj.name


       
class CameraMorph(bpy.types.Operator):
    """Camera Morph"""
    bl_idname = "scene.camera_morph"
    bl_label = "Camera Morph"

   
    
    def execute(self, context):
        
        main(context)
        return {'FINISHED'}


def register():
    
    bpy.utils.register_class(UICameraOperator)
    bpy.utils.register_class(CameraMorph)
    bpy.utils.register_class(UI_Camera_panel)
    bpy.utils.register_class(CameraItemsList)
    bpy.utils.register_class(CameraItem)
    bpy.utils.register_class(Camera_items_Panel)
    bpy.utils.register_class(CameraItem_add)
    bpy.utils.register_class(CameraItem_remove)
    bpy.utils.register_class(CameraItem_move)
    bpy.types.Scene.cameraitems = CollectionProperty(type=CameraItem)
    # Unused, but this is needed for the TemplateList to work...
    bpy.types.Scene.cameraitems_index = IntProperty(default=-1)

def unregister():
    bpy.utils.unregister_class(UICameraOperator)
    bpy.utils.unregister_class(CameraMorph)
    bpy.utils.unregister_class(UI_Camera_panel)
    bpy.utils.unregister_class(CameraItemsList)
    bpy.utils.unregister_class(CameraItem)
    bpy.utils.unregister_class(Camera_items_Panel)
    bpy.utils.unregister_class(CameraItem_add)
    bpy.utils.unregister_class(CameraItem_remove)
    bpy.utils.unregister_class(CameraItem_move)
    del bpy.types.Scene.cameraitems_index
    del bpy.types.Scene.cameraitems

if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.camera.camera_morph()
