bl_info = {
    "name": "Rotate Local",
    "author": "JuhaW",
    "version": (1, 0, 0),
    "blender": (2, 76, 0),
    "location": "Tools",
    "description": "Objects local rotations",
    "warning": "beta",
    "wiki_url": "",
    "category": "Object",
}


import bpy
from math import radians
from mathutils import Euler
from bpy.props import FloatProperty

# class RotatePanel(bpy.types.Panel):


class RotatePanel(bpy.types.Panel):
    """Creates a Panel in the Tools panel"""

    bl_label = "Local Rotation"
    bl_idname = "Rotation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_region_type = 'UI'
    # bl_options = {'REGISTER', 'UNDO'}	# enable undo for the operator.
    # bl_context = "object"

    v = [1, 2, 4]
    r = ['X', 'Y', 'Z']
    bpy.types.Scene.rotx = bpy.props.FloatProperty(default=90, step=100)
    bpy.types.Scene.roty = bpy.props.FloatProperty(default=90, step=100)
    bpy.types.Scene.rotz = bpy.props.FloatProperty(default=90, step=100)
    bpy.types.Scene.boolx = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.booly = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.boolz = bpy.props.BoolProperty(default=False)

    xyz = ['x', 'y', 'z']

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)

        for j, i in enumerate(self.v):

            #row.label('Rotate ' + self.r[j]+': ' + str(RotateX.xyz[i]*90) + "\xb0")
            #row.alignment = 'LEFT'

            row.label('Rot' + self.r[j])

            row.prop(context.scene, 'bool' + self.xyz[j], '', icon='MANIPUL')

            row.prop(context.scene, 'rot' + self.xyz[j], '')  # "\xb0")

            #row.operator('rotate.x', text ="").axis =  ((i,0,0))
            row.operator('rotate.x', text="", icon='TRIA_LEFT').axis = ((i, 0, 0))

            row.operator('rotate.x', text="", icon='TRIA_RIGHT').axis = ((i, 1, 0))

            row = layout.row(align=True)
        #row.label(text ='Create an empty object at the location and rotation of the selected object')
        row = layout.row()
        row.operator('create.empty', icon='OUTLINER_OB_MESH')
        row = layout.row()
        row.operator('orientation.create', icon='SNAP_SURFACE')
        #row.operator('rotate.x', 'Reset values').axis = ((0,0,0))


class Orientation_create(bpy.types.Operator):
    """Select objects, Edit mode select geometry where to align transformation of the selected objects"""
    bl_idname = "orientation.create"
    bl_label = "Set Orientation"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 1 and context.mode == 'EDIT_MESH'

    def execute(self, context):

        activeobj = context.scene.objects.active
        #loc = o.location

        bpy.ops.view3d.snap_cursor_to_active()
        bpy.ops.transform.create_orientation(use=True, overwrite=True)
        selobjs = [o for o in bpy.context.selected_objects if o != bpy.context.scene.objects.active]

        bpy.ops.object.mode_set(mode='OBJECT')
        activeobj.select = False
        context.scene.objects.active = selobjs[0]
        bpy.ops.transform.transform(mode='ALIGN')

        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
        bpy.context.space_data.transform_orientation = 'LOCAL'

        return {'FINISHED'}


class Object_create_empty(bpy.types.Operator):
    """Create an empty object at the location and rotation of the selected objects"""
    bl_idname = "create.empty"
    bl_label = "Create Empty object"

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'

    def execute(self, context):

        for o in context.selected_objects:
            #o = context.object
            loc = o.location
            # add empty
            empty = bpy.data.objects.new('Empty', None)
            context.scene.objects.link(empty)
            empty.location = loc
            empty.rotation_euler = o.rotation_euler
            bpy.ops.object.select_all(action='DESELECT')
            empty.show_x_ray = True

        empty.select = True
        context.scene.objects.active = empty
        return {'FINISHED'}


class RotateX(bpy.types.Operator):
    """Rotate the components of a mesh around the local axis. If manipulator icon is enabled the original of the model is maintained."""
    bl_idname = "rotate.x"
    bl_label = "Rotate"

    axis = bpy.props.FloatVectorProperty()
    FILTER_OUT = ['EMPTY', 'ARMATURE', 'SPEAKER', 'LATTICE', 'CAMERA', 'LAMP', 'SURFACE', 'CURVE', 'FONT']

    def execute(self, context):

        if not context.selected_objects:
            print("no objects selected")
            return {'FINISHED'}

        activeobject = context.object
        v0 = int(self.axis[0])
        v1 = int(self.axis[1])
        v2 = int(self.axis[2])

        if v0 == 0:
            RotateX.xyz = [0, 0, 0, 0, 0]
            return {'FINISHED'}

        x = bool(1 & v0)
        y = bool(2 & v0)
        z = bool(4 & v0)
        lockbool = [context.scene.boolx, context.scene.booly, context.scene.boolz]

        bpy.types.Scene.boolz
        mode = bpy.context.object.mode
        c = context.scene

        # cursor to object origin & pivot point to cursor
        area = [area for area in bpy.context.screen.areas if area.type == 'VIEW_3D']
        d = area[0].spaces.active
        pivotmode = d.pivot_point

        for o in bpy.context.selected_objects:
            bpy.context.scene.cursor_location = o.location
            bpy.context.scene.objects.active = o
            d.pivot_point = 'CURSOR'
            srot = [c.rotx, c.roty, c.rotz]

            if v0 == 1 or v0 == 2 or v0 == 4:
                rot = radians(srot[int(v0 / 2)]) if v1 else -radians(srot[int(v0 / 2)])

            if not context.object.type in (self.FILTER_OUT):
                if o.mode == 'OBJECT' and not lockbool[int(v0 / 2)]:
                    #print ("Object mode and not lockbool")
                    RotateObjectMode(o, d, rot, srot, v0)
                elif activeobject.mode == 'EDIT' or lockbool[int(v0 / 2)]:
                    #print ("Edit mode or lockbool")
                    # edit mode
                    RotateEditMode(rot, x, y, z)
                    d.pivot_point = 'INDIVIDUAL_ORIGINS'
                    boo = [c.boolx, c.booly, c.boolz]
                    # object mode
                    if boo[int(v0 / 2)]:
                        #print ("continue and lockbool")
                        rot = -rot
                        RotateObjectMode(o, d, rot, srot, v0)
                    if activeobject.mode == 'EDIT':
                        #print ("edit mode and break")
                        break
                # object mode
                elif not lockbool[int(v0 / 2)]:
                    print("elif Object mode and not lockbool")
                    RotateObjectMode(o, d, rot, srot, v0)

            bpy.ops.object.mode_set(mode='OBJECT')

        d.pivot_point = pivotmode

        #RotateX.xyz[v0] = RotateX.xyz[v0] + 1 if v1 else RotateX.xyz[v0] - 1
        #RotateX.xyz[v0] = RotateX.xyz[v0] & 3
        bpy.ops.object.mode_set(mode=mode)
        bpy.context.scene.objects.active = activeobject
        return {'FINISHED'}


def RotateObjectMode(o, d, rot, srot, v0):
    bpy.ops.object.mode_set(mode='OBJECT')
    d.pivot_point = 'INDIVIDUAL_ORIGINS'
    o.rotation_euler.rotate_axis(RotatePanel.r[int(v0 / 2)], rot)


def RotateEditMode(rot, x, y, z):

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.rotate(value=rot, axis=(int(x), int(y), int(z)), constraint_axis=(x, y, z), constraint_orientation='LOCAL')
    bpy.ops.mesh.normals_make_consistent()


def register():
    bpy.utils.register_module(__name__)
    RotateX.xyz = [0, 0, 0, 0, 0]
    bpy.types.VIEW3D_PT_view3d_display.append(RotatePanel)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
