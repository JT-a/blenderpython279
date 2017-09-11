bl_info = {
    'name': "View Manage tool",
    'author': "luxuy blendercn",
    'version': (1, 0, 1),
    'blender': (2, 70, 0),
    'location': "3D View->properties panel",
    'warning': "",
    'category': 'View'}

import bpy
import math
import mathutils
import bmesh
from bpy.props import FloatProperty, IntProperty, BoolProperty, EnumProperty, StringProperty
from mathutils import Matrix, Vector
from ..utils import AddonPreferences, SpaceProperty

#----------------------------------------------------------------------------


class ViewManage_Panel(bpy.types.Operator):

    bl_label = "View Manager Tool"
    bl_idname = "view3d.manage_panel"

    bpy.types.Scene.b1 = BoolProperty(name="a", default=0)
    bpy.types.Scene.b2 = BoolProperty(name="b", default=0)
    bpy.types.Scene.b3 = BoolProperty(name="c", default=0)

    bpy.types.Scene.saved_views = EnumProperty(items=[('view 0', 'view 0', '')], name="Saved views")

    def update_func(self, context):
        scn = context.scene
        r3d = context.space_data.region_3d

        if scn.saved_views:
            r3d.view_rotation = ViewSave.views[scn.saved_views][0]
        q = mathutils.Quaternion((0.0, 0.0, 1.0), math.radians(-scn.ang))
        save = None
        if ViewSave.views[scn.saved_views][3] != 'ORTHO':
            save = ViewSave.views[scn.saved_views][3]
            ViewSave.views[scn.saved_views][3] = 'ORTHO'
        r3d.view_perspective = 'ORTHO'
        r3d.view_rotation *= q
        r3d.view_location = ViewSave.views[scn.saved_views][1]
        r3d.view_distance = ViewSave.views[scn.saved_views][2]
        r3d.view_perspective = ViewSave.views[scn.saved_views][3]
        # context.area.tag_redraw()
        if save:
            ViewSave.views[scn.saved_views][3] = save
            r3d.view_perspective = save
        #bpy.context.space_data.show_floor = False
        #bpy.context.space_data.show_axis_z = False
        #bpy.context.space_data.show_axis_y = False
        #bpy.context.space_data.show_axis_x = False
        return None
    bpy.types.Scene.ang = FloatProperty(update=update_func, name="Angle", default=0, min=-180, max=180, step=5, precision=1)


def menu(self, context):
    scn = bpy.context.scene
    l = self.layout
    l.label('Save Views:')
    l.operator('view.goto_view')

    r = l.row(align=True)

    s = r.split(percentage=0.2, align=True)
    # c=s.column()
    s.operator('view.view_del', text='', icon='X')
    s = s.split(percentage=0.75, align=True)
    s.prop(scn, "saved_views", text="")
    s.operator('view.view_save', text='', icon='ZOOMIN')

    r = l.row()
    #s= r.split(percentage=0.2)
    # c=s.column()
    # s.operator('view.view_rot_rel',text='<').name='left'
    #s= s.split(percentage=0.75)
    r.prop(scn, "ang")
    # s.operator('view.view_rot_rel',text='>').name='right'

    # l.operator('view.view_align_pts')
    # r=l.row(align=True)
    # r.alignment='CENTER'
    # r.prop(scn,"b1",text="AA",icon='X')
    # r.prop(scn,"b2",text="",icon='ZOOMOUT')
    # r.prop(scn,"b3",toggle=True,text="",icon='ZOOMIN')
    # r.enabled=False


class GotoView(bpy.types.Operator):
    """Back to selected view in list"""
    bl_idname = "view.goto_view"
    bl_label = "Go to View"

    def execute(self, context):
        scn = context.scene
        r3d = context.space_data.region_3d

        if scn.saved_views:
            r3d.view_rotation = ViewSave.views[scn.saved_views][0]

        r3d.view_location = ViewSave.views[scn.saved_views][1]
        r3d.view_distance = ViewSave.views[scn.saved_views][2]
        r3d.view_perspective = ViewSave.views[scn.saved_views][3]
        scn.ang = 0
        return {'FINISHED'}


class ViewSave(bpy.types.Operator):
    """Add current view to list"""
    bl_idname = "view.view_save"
    bl_label = "View Save"
    bl_options = {'REGISTER', 'UNDO'}

    views = {'view 0': [mathutils.Quaternion((0.0, 0.0, 1.0), 0), Vector((0, 0, 0)), 10, 'ORTHO']}

    rename = StringProperty(name="View rename", default="view 0")

    def execute(self, context):
        scn = bpy.context.scene
        r3d = context.space_data.region_3d
        q = r3d.view_rotation
        view_name = self.rename

        if len(ViewSave.views) < 100:

            if view_name == scn.saved_views:
                view_name = "view " + str(len(ViewSave.views) - 1)

                if view_name in ViewSave.views.keys():
                    view_name = "view " + str(len(ViewSave.views))
                self.rename = view_name

                ViewSave.views[view_name] = [q.copy(), r3d.view_location.copy(), r3d.view_distance, r3d.view_perspective]
                bpy.types.Scene.saved_views = EnumProperty(
                    items=[(i, i, '') for i in ViewSave.views], name="Saved views")
                scn.saved_views = view_name
            else:

                if scn.saved_views in ViewSave.views.keys():

                    ViewSave.views[self.rename] = [q.copy(), r3d.view_location.copy(), r3d.view_distance, r3d.view_perspective]
                    del(ViewSave.views[scn.saved_views])
                    bpy.types.Scene.saved_views = EnumProperty(
                        items=[(i, i, '') for i in ViewSave.views], name="Saved views")
                else:
                    ViewSave.views[scn.saved_views] = [q.copy(), r3d.view_location.copy(), r3d.view_distance, r3d.view_perspective]
                scn.saved_views = self.rename

        else:
            ViewSave.views[view_name] = [q.copy(), r3d.view_location.copy(), r3d.view_distance, r3d.view_perspective]
        scn.ang = 0
        return {'FINISHED'}


class ViewDel(bpy.types.Operator):
    """Del current view from list"""
    bl_idname = "view.view_del"
    bl_label = "View Del"

    def execute(self, context):
        scn = bpy.context.scene
        name = scn.saved_views
        if len(ViewSave.views) > 1:
            del(ViewSave.views[name])
            bpy.types.Scene.saved_views = EnumProperty(
                items=[(i, i, '') for i in ViewSave.views], name="Saved views")
            scn.saved_views = list(ViewSave.views.keys())[0]
        scn.ang = 0
        return {'FINISHED'}

classes = [
    ViewManage_Panel,
    GotoView,
    ViewSave,
    ViewDel,
]

#---------------------------------------------


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_PT_view3d_properties.append(menu)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_PT_view3d_properties.remove(menu)

if __name__ == "__main__":
    register()
