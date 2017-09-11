bl_info = {
    'name': 'Transform Extended',
    'author': 'Jakub Bełcik',
    'version': (1, 0),
    'blender': (2, 7, 3),
    'location': '3D View > Tools > Analyse DICOM',
    'description': '3 panels, Select, Modify, Transform',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Panel'
}
from .utils import AddonPreferences, SpaceProperty
import bpy
from bpy.props import StringProperty, FloatProperty, BoolProperty, EnumProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
import mathutils
from mathutils import Vector
from .utils import AddonPreferences, SpaceProperty, operator_call


def rendershowselected():
    for ob in bpy.data.objects:
        if ob.select == True:
            ob.hide_render = False


def renderhideselected():
    for ob in bpy.data.objects:
        if ob.select == True:
            ob.hide_render = True


def f_trim_x_fix(self, context):
    if context.scene.trim_x_start >= context.scene.trim_x_end:
        context.scene.trim_x_start -= 1
    return None


def f_trim_y_fix(self, context):
    if context.scene.trim_y_start >= context.scene.trim_y_end:
        context.scene.trim_y_start -= 1
    return None


def f_trim_z_fix(self, context):
    if context.scene.trim_z_start >= context.scene.trim_z_end:
        context.scene.trim_z_start -= 1
    return None


def f_clear_loc(self, context):
    obj_name = context.object.name

    if context.object.type != 'MESH':
        return None

    if context.object.mode != 'OBJECT':
        return None

    if context.object.hide:
        return None

    for i in bpy.data.objects:
        if i.name != obj_name:
            i.select = False

    bpy.ops.object.location_clear()

    return None


def f_dissect_fix(self, context):
    if context.scene.dissect_start >= context.scene.dissect_end:
        context.scene.dissect_start -= 1
    return None


def f_trim(self, context):
    obj_name = context.object.name
    obj = bpy.data.objects[obj_name]
    obj_mesh = obj.data
    guard = False

    if context.object.mode == 'OBJECT':
        bpy.ops.object.mode_set(mode='EDIT')

        if obj_mesh.total_vert_sel > 0:
            bpy.ops.mesh.select_all(action='TOGGLE')

        bpy.ops.mesh.select_all(action='TOGGLE')
        guard = True

    dim_x = obj.dimensions.x
    dim_y = obj.dimensions.y
    dim_z = obj.dimensions.z

    if context.scene.trim_x_start > 0:
        coord = obj.location.x - dim_x / 2 + dim_x * context.scene.trim_x_start / 100.0

        bpy.ops.mesh.bisect(
            plane_co=(coord, 0, 0),
            plane_no=(1, 0, 0),
            use_fill=context.scene.trim_use_fill,
            clear_inner=True,
            threshold=0.00001
        )

        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.select_all(action='TOGGLE')

    if context.scene.trim_x_end < 100:
        coord = obj.location.x - dim_x / 2 + dim_x * context.scene.trim_x_end / 100.0

        bpy.ops.mesh.bisect(
            plane_co=(coord, 0, 0),
            plane_no=(1, 0, 0),
            use_fill=context.scene.trim_use_fill,
            clear_outer=True,
            threshold=0.00001
        )

        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.select_all(action='TOGGLE')

    if context.scene.trim_y_start > 0:
        coord = obj.location.y - dim_y / 2 + dim_y * context.scene.trim_y_start / 100.0

        bpy.ops.mesh.bisect(
            plane_co=(0, coord, 0),
            plane_no=(0, 1, 0),
            use_fill=context.scene.trim_use_fill,
            clear_inner=True,
            threshold=0.00001
        )

        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.select_all(action='TOGGLE')

    if context.scene.trim_y_end < 100:
        coord = obj.location.y - dim_y / 2 + dim_y * context.scene.trim_y_end / 100.0

        bpy.ops.mesh.bisect(
            plane_co=(0, coord, 0),
            plane_no=(0, 1, 0),
            use_fill=context.scene.trim_use_fill,
            clear_outer=True,
            threshold=0.00001
        )

        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.select_all(action='TOGGLE')

    if context.scene.trim_z_start > 0:
        coord = obj.location.z - dim_z / 2 + dim_z * context.scene.trim_z_start / 100.0

        bpy.ops.mesh.bisect(
            plane_co=(0, 0, coord),
            plane_no=(0, 0, 1),
            use_fill=context.scene.trim_use_fill,
            clear_inner=True,
            threshold=0.00001
        )

        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.select_all(action='TOGGLE')

    if context.scene.trim_z_end < 100:
        coord = obj.location.z - dim_z / 2 + dim_z * context.scene.trim_z_end / 100.0

        bpy.ops.mesh.bisect(
            plane_co=(0, 0, coord),
            plane_no=(0, 0, 1),
            use_fill=context.scene.trim_use_fill,
            clear_outer=True,
            threshold=0.00001
        )

        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.select_all(action='TOGGLE')

    if guard:
        bpy.ops.object.mode_set(mode='OBJECT')

    return None


def f_intersect(self, context):
    obj_name = context.object.name
    obj = bpy.data.objects[obj_name]
    obj_mesh = obj.data
    guard = False

    if context.object.mode == 'OBJECT':
        bpy.ops.object.mode_set(mode='EDIT')
        guard = True
    elif context.object.mode != 'EDIT':
        self.report({'ERROR'}, 'Cannot perform intersection in this interaction mode')
        return {'CANCELLED'}

    if obj_mesh.total_vert_sel > 0:
        bpy.ops.mesh.select_all(action='TOGGLE')

    bpy.ops.mesh.select_all(action='TOGGLE')

    if context.scene.intersect_plane == '0':
        intersect_z = 1
        intersect_x = intersect_y = 0
    elif context.scene.intersect_plane == '1':
        intersect_y = 1
        intersect_x = intersect_z = 0
    elif context.scene.intersect_plane == '2':
        intersect_x = 1
        intersect_y = intersect_z = 0

    bpy.ops.mesh.bisect(
        plane_co=(0, 0, 0),
        plane_no=(intersect_x, intersect_y, intersect_z),
        use_fill=context.scene.intersect_use_fill,
        clear_inner=context.scene.intersect_clear_inner,
        clear_outer=context.scene.intersect_clear_outer,
        threshold=0.00001
    )

    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.mesh.select_all(action='TOGGLE')

    if guard:
        bpy.ops.object.mode_set(mode='OBJECT')

    return None


def f_nav_bis_dis(self, context, name, step, hide):
    if context.object == None:
        self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
        return {'CANCELLED'}

    if context.object.type != 'MESH':
        self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
        return {'CANCELLED'}

    if name == 'Intersection':
        info = 'intersection'
        length = -12
    elif name == 'Dissection':
        info = 'dissection'
        length = -10

    obj_name = context.object.name
    guard = False

    if obj_name[length - 3: -2] == '.' + name and step == 1:
        next_obj_name = obj_name + '.001'
    elif obj_name[length - 3: -2] == '.' + name and step == -1:
        self.report({'ERROR'}, 'This is the first product of ' + info)
        return {'CANCELLED'}
    elif obj_name[length - 7: -5] == '.' + name + '.':
        number = int(obj_name[-3:]) + step

        if number == 0:
            number_str = ''
        elif number < 10:
            number_str = '.00' + str(number)
        elif number < 100:
            number_str = '.0' + str(number)
        else:
            number_str = '.' + str(number)

        next_obj_name = obj_name[: -4] + number_str
    elif obj_name[length - 8: -6] == '.' + name + '.':
        number = int(obj_name[-4:]) + step

        if number == 0:
            number_str = ''
        if number < 10:
            number_str = '.000' + str(number)
        elif number < 100:
            number_str = '.00' + str(number)
        elif number < 999:
            number_str = '.0' + str(number)
        else:
            number_str = '.' + str(number)

        next_obj_name = obj_name[: -5] + number_str
    else:
        self.report({'ERROR'}, 'This object is not a product of ' + info)
        return {'CANCELLED'}

    if bpy.data.objects.find(next_obj_name) == -1 and step == 1:
        self.report({'ERROR'}, 'This is the last product of ' + info)
        return {'CANCELLED'}
    elif bpy.data.objects.find(next_obj_name) == -1 and step == -1:
        self.report({'ERROR'}, 'This is the first product of ' + info)
        return {'CANCELLED'}

    guard = False

    if context.object.mode != 'OBJECT':
        obj_mode = context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        guard = True

    bpy.ops.object.select_all(action='TOGGLE')

    obj = bpy.data.objects[obj_name]

    if hide:
        obj.hide = True
        obj.hide_render = True

    context.scene.objects.active = bpy.data.objects[next_obj_name]
    bpy.data.objects[next_obj_name].select = True

    bpy.data.objects[next_obj_name].hide = False
    bpy.data.objects[next_obj_name].hide_select = False
    bpy.data.objects[next_obj_name].hide_render = False

    obj_mesh = obj.data

    if guard:
        bpy.ops.object.mode_set(mode=obj_mode)

    return None


def f_delta_scale_xyz(self, context):
    if context.object.mode != 'OBJECT':
        return None

    if context.object.hide:
        return None

    obj_name = context.object.name
    obj = bpy.data.objects[obj_name]

    obj.delta_scale.xyz = obj.delta_scale_xyz

    return None

coords = [
    ('0', 'Common Translation', 'Translated, common coordinates for each axis'),
    ('1', 'Translation', 'Translated, separate coordinates for each axis'),
    ('2', 'Stagnation', 'Same coordinates as input object\'s')
]

orientations = [
    ('0', 'Z Axis', 'Cut across (perpendicularly to) Z axis'),
    ('1', 'Y Axis', 'Cut across (perpendicularly to) Y axis'),
    ('2', 'X Axis', 'Cut across (perpendicularly to) X axis')
]

bpy.types.Scene.trim_expand = BoolProperty(options={'HIDDEN'}, default=False, name='Expand', description='Expand/reduce trim properties panel')
bpy.types.Scene.trim_origin_translation = BoolProperty(options={'HIDDEN'}, default=True, name='Origin Translation', description='Translate coordinates of trimmed object')
bpy.types.Scene.trim_use_fill = BoolProperty(options={'HIDDEN'}, default=False, name='Fill', description='Fill in the cuts')

bpy.types.Scene.trim_x_start = IntProperty(options={'HIDDEN'}, name='Start', min=0, max=99, step=1, default=0, subtype='PERCENTAGE',
                                           update=f_trim_x_fix, description='Percentage value of starting position on X axis')
bpy.types.Scene.trim_x_end = IntProperty(options={'HIDDEN'}, name='End', min=1, max=100, step=1, default=100, subtype='PERCENTAGE',
                                         update=f_trim_x_fix, description='Percentage value of finishing position on X axis')
bpy.types.Scene.trim_y_start = IntProperty(options={'HIDDEN'}, name='Start', min=0, max=99, step=1, default=0, subtype='PERCENTAGE',
                                           update=f_trim_y_fix, description='Percentage value of starting position on Y axis')
bpy.types.Scene.trim_y_end = IntProperty(options={'HIDDEN'}, name='End', min=1, max=100, step=1, default=100, subtype='PERCENTAGE',
                                         update=f_trim_y_fix, description='Percentage value of finishing position on Y axis')
bpy.types.Scene.trim_z_start = IntProperty(options={'HIDDEN'}, name='Start', min=0, max=99, step=1, default=0, subtype='PERCENTAGE',
                                           update=f_trim_z_fix, description='Percentage value of starting position on Z axis')
bpy.types.Scene.trim_z_end = IntProperty(options={'HIDDEN'}, name='End', min=1, max=100, step=1, default=100, subtype='PERCENTAGE',
                                         update=f_trim_z_fix, description='Percentage value of finishing position on Z axis')

bpy.types.Scene.intersect_origin = EnumProperty(options={'HIDDEN'}, items=coords, default='1', name='Origin Location', description='Location of intersection product')

bpy.types.Scene.intersect_plane = EnumProperty(options={'HIDDEN'}, items=orientations, default='2', name='Plane Orientation', update=f_clear_loc,
                                               description='Cutting plane orientation')

bpy.types.Scene.intersect_expand = BoolProperty(options={'HIDDEN'}, default=False, name='Expand', description='Expand/reduce intersect properties panel')
bpy.types.Scene.intersect_use_fill = BoolProperty(options={'HIDDEN'}, default=False, name='Fill', description='Fill in the cuts')
bpy.types.Scene.intersect_hide = BoolProperty(options={'HIDDEN'}, default=False, name='Hide', description='Hide last active object browsing intersection products')

bpy.types.Scene.intersect_clear_inner = BoolProperty(options={'HIDDEN'}, default=True, name='Clear Inner', description='Remove geometry behind the plane')
bpy.types.Scene.intersect_clear_outer = BoolProperty(options={'HIDDEN'}, default=True, name='Clear Outer', description='Remove geometry in front of the plane')

bpy.types.Scene.dissect_origin = EnumProperty(options={'HIDDEN'}, items=coords, default='1', name='Origin Location', description='Location of dissection products')

bpy.types.Scene.dissect_plane = EnumProperty(options={'HIDDEN'}, items=orientations, default='2', name='Plane Orientation', description='Cutting plane orientation')

bpy.types.Scene.dissect_expand = BoolProperty(options={'HIDDEN'}, default=False, name='Expand', description='Expand/reduce dissect properties panel')
bpy.types.Scene.dissect_use_fill = BoolProperty(options={'HIDDEN'}, default=False, name='Fill', description='Fill in the cuts')
bpy.types.Scene.dissect_hide = BoolProperty(options={'HIDDEN'}, default=False, name='Hide', description='Hide last active object browsing dissection products')

bpy.types.Scene.dissect_uncut = BoolProperty(options={'HIDDEN'}, default=False, name='Keep Uncutted', description='Keep uncutted object pieces')

bpy.types.Scene.dissect_step = FloatProperty(options={'HIDDEN'}, name='Step', min=0.01, step=1, default=1, description='Gap between each section')

bpy.types.Scene.dissect_start = IntProperty(options={'HIDDEN'}, name='Start', min=0, max=99, step=1, default=0, subtype='PERCENTAGE',
                                            update=f_dissect_fix, description='Percentage value of starting position')
bpy.types.Scene.dissect_end = IntProperty(options={'HIDDEN'}, name='End', min=1, max=100, step=1, default=100, subtype='PERCENTAGE',
                                          update=f_dissect_fix, description='Percentage value of finishing position')


class OrbitUpView(bpy.types.Operator):
    bl_idname = 'opr.orbit_up_view'
    bl_label = 'Orbit Up View'
    bl_description = 'Orbit the view around to the Up'

    def execute(self, context):
        bpy.ops.view3d.view_orbit(type='ORBITUP')
        return {'FINISHED'}


class OrbitLeftView(bpy.types.Operator):
    bl_idname = 'opr.orbit_left_view'
    bl_label = 'Orbit Left View'
    bl_description = 'Orbit the view around to the Left'

    def execute(self, context):
        bpy.ops.view3d.view_orbit(type='ORBITLEFT')
        return {'FINISHED'}


class OrbitRightView(bpy.types.Operator):
    bl_idname = 'opr.orbit_right_view'
    bl_label = 'Orbit Right View'
    bl_description = 'Orbit the view around to the Right'

    def execute(self, context):
        bpy.ops.view3d.view_orbit(type='ORBITRIGHT')
        return {'FINISHED'}


class OrbitDownView(bpy.types.Operator):
    bl_idname = 'opr.orbit_down_view'
    bl_label = 'Orbit Down View'
    bl_description = 'Orbit the view around to the Down'

    def execute(self, context):
        bpy.ops.view3d.view_orbit(type='ORBITDOWN')
        return {'FINISHED'}


class PanUpView(bpy.types.Operator):
    bl_idname = 'opr.pan_up_view'
    bl_label = 'Pan Up View'
    bl_description = 'Pan the view to the Up'

    def execute(self, context):
        bpy.ops.view3d.view_pan(type='PANUP')
        return {'FINISHED'}


class PanLeftView(bpy.types.Operator):
    bl_idname = 'opr.pan_left_view'
    bl_label = 'Pan Left View'
    bl_description = 'Pan the view to the Left'

    def execute(self, context):
        bpy.ops.view3d.view_pan(type='PANLEFT')
        return {'FINISHED'}


class PanRightView(bpy.types.Operator):
    bl_idname = 'opr.pan_right_view'
    bl_label = 'Pan Righ Viewt'
    bl_description = 'Pan the view to the Right'

    def execute(self, context):
        bpy.ops.view3d.view_pan(type='PANRIGHT')
        return {'FINISHED'}


class PanDownView(bpy.types.Operator):
    bl_idname = 'opr.pan_down_view'
    bl_label = 'Pan Down View'
    bl_description = 'Pan the view to the Down'

    def execute(self, context):
        bpy.ops.view3d.view_pan(type='PANDOWN')
        return {'FINISHED'}


class ZoomInView(bpy.types.Operator):
    bl_idname = 'opr.zoom_in_view'
    bl_label = 'Zoom In View'
    bl_description = 'Zoom in in the view'

    def execute(self, context):
        bpy.ops.view3d.zoom(delta=1)
        return {'FINISHED'}


class ZoomOutView(bpy.types.Operator):
    bl_idname = 'opr.zoom_out_view'
    bl_label = 'Zoom Out View'
    bl_description = 'Zoom out in the view'

    def execute(self, context):
        bpy.ops.view3d.zoom(delta=-1)
        return {'FINISHED'}


class RollLeftView(bpy.types.Operator):
    bl_idname = 'opr.roll_left_view'
    bl_label = 'Roll Left View'
    bl_description = 'Roll the view left'

    def execute(self, context):
        bpy.ops.view3d.view_roll(angle=-0.261799)
        return {'FINISHED'}


class RollRightView(bpy.types.Operator):
    bl_idname = 'opr.roll_right_view'
    bl_label = 'Roll Right View'
    bl_description = 'Roll the view right'

    def execute(self, context):
        bpy.ops.view3d.view_roll(angle=0.261799)
        return {'FINISHED'}


class LeftViewpoint(bpy.types.Operator):
    bl_idname = 'opr.left_viewpoint'
    bl_label = 'Left Viewpoint'
    bl_description = 'View from the Left'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='LEFT')
        return {'FINISHED'}


class RightViewpoint(bpy.types.Operator):
    bl_idname = 'opr.right_viewpoint'
    bl_label = 'Right Viewpoint'
    bl_description = 'View from the Right'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='RIGHT')
        return {'FINISHED'}


class FrontViewpoint(bpy.types.Operator):
    bl_idname = 'opr.front_viewpoint'
    bl_label = 'Front Viewpoint'
    bl_description = 'View from the Front'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='FRONT')
        return {'FINISHED'}


class BackViewpoint(bpy.types.Operator):
    bl_idname = 'opr.back_viewpoint'
    bl_label = 'Back Viewpoint'
    bl_description = 'View from the Back'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='BACK')
        return {'FINISHED'}


class TopViewpoint(bpy.types.Operator):
    bl_idname = 'opr.top_viewpoint'
    bl_label = 'Top Viewpoint'
    bl_description = 'View from the Top'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='TOP')
        return {'FINISHED'}


class BottomViewpoint(bpy.types.Operator):
    bl_idname = 'opr.bottom_viewpoint'
    bl_label = 'Bottom Viewpoint'
    bl_description = 'View from the Bottom'

    def execute(self, context):
        bpy.ops.view3d.viewnumpad(type='BOTTOM')
        return {'FINISHED'}


class ShowHideObject(bpy.types.Operator):
    bl_idname = 'opr.show_hide_object'
    bl_label = 'Show/Hide Object'
    bl_description = 'Show/hide selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.select:
                if i.hide:
                    i.hide = False
                    i.hide_select = False
                    i.hide_render = False
                else:
                    i.hide = True
                    i.select = False

                    if i.type not in ['CAMERA', 'LAMP']:
                        i.hide_render = True
        return {'FINISHED'}


class ShowAllObjects(bpy.types.Operator):
    bl_idname = 'opr.show_all_objects'
    bl_label = 'Show All Objects'
    bl_description = 'Show all objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for i in bpy.data.objects:
            i.hide = False
            i.hide_select = False
            i.hide_render = False
        return {'FINISHED'}


class HideAllObjects(bpy.types.Operator):
    bl_idname = 'opr.hide_all_objects'
    bl_label = 'Hide All Objects'
    bl_description = 'Hide all inactive objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            for i in bpy.data.objects:
                i.hide = True
                i.select = False

                if i.type not in ['CAMERA', 'LAMP']:
                    i.hide_render = True
        else:
            obj_name = context.object.name

            for i in bpy.data.objects:
                if i.name != obj_name:
                    i.hide = True
                    i.select = False

                    if i.type not in ['CAMERA', 'LAMP']:
                        i.hide_render = True

        return {'FINISHED'}


class SelectAll(bpy.types.Operator):
    bl_idname = 'opr.select_all'
    bl_label = '(De)select All'
    bl_description = '(De)select all objects, verticies, edges or faces'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            bpy.ops.object.select_all(action='TOGGLE')
        elif context.object.mode == 'EDIT':
            bpy.ops.mesh.select_all(action='TOGGLE')
        elif context.object.mode == 'OBJECT':
            bpy.ops.object.select_all(action='TOGGLE')
        else:
            self.report({'ERROR'}, 'Cannot perform this operation in this mode')
            return {'CANCELLED'}

        return {'FINISHED'}


class InverseSelection(bpy.types.Operator):
    bl_idname = 'opr.inverse_selection'
    bl_label = 'Inverse Selection'
    bl_description = 'Inverse selection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            bpy.ops.object.select_all(action='INVERT')
        elif context.object.mode == 'EDIT':
            bpy.ops.mesh.select_all(action='INVERT')
        elif context.object.mode == 'OBJECT':
            bpy.ops.object.select_all(action='INVERT')
        else:
            self.report({'ERROR'}, 'Cannot perform this operation in this mode')
            return {'CANCELLED'}

        return {'FINISHED'}


class LoopMultiSelect(bpy.types.Operator):
    bl_idname = 'opr.loop_multi_select'
    bl_label = 'Edge Loop Select'
    bl_description = 'Select a loop of connected edges'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.loop_multi_select(ring=False)
        return {'FINISHED'}


class DeleteVerts(bpy.types.Operator):
    bl_idname = 'opr.delete_verts'
    bl_label = 'Delete Vertices'
    bl_description = 'Delete selected vertices'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='VERT')
        return {'FINISHED'}


class DeleteEdges(bpy.types.Operator):
    bl_idname = 'opr.delete_edges'
    bl_label = 'Delete Edges'
    bl_description = 'Delete selected edges'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='EDGE')
        return {'FINISHED'}


class DeleteFaces(bpy.types.Operator):
    bl_idname = 'opr.delete_faces'
    bl_label = 'Delete Faces'
    bl_description = 'Delete selected faces'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'}


class DeleteOnlyFaces(bpy.types.Operator):
    bl_idname = 'opr.delete_only_faces'
    bl_label = 'Delete Only Faces'
    bl_description = 'Delete only selected faces'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='ONLY_FACE')
        return {'FINISHED'}


class DeleteOnlyEdgesFaces(bpy.types.Operator):
    bl_idname = 'opr.delete_only_edges_faces'
    bl_label = 'Delete Only Edges & Faces'
    bl_description = 'Delete only selected edges & faces'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='EDGE_FACE')
        return {'FINISHED'}


class ImportPlyObject(bpy.types.Operator, ImportHelper):
    bl_idname = 'opr.import_ply_object'
    bl_label = 'Import Stanford (.ply) Object'
    bl_description = 'Load a PLY geometry file'
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.ply'
    filter_glob = StringProperty(default='*.ply', options={'HIDDEN'})

    def execute(self, context):
        if context.object != None:
            if context.object.mode != 'OBJECT':
                self.report({'ERROR'}, 'This operation can be performed only in object mode')
                return {'CANCELLED'}

            bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.import_mesh.ply(filepath=self.filepath)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()
        bpy.ops.object.scale_clear()
        bpy.ops.view3d.view_selected()

        return {'FINISHED'}


class ImportStlObject(bpy.types.Operator, ImportHelper):
    bl_idname = 'opr.import_stl_object'
    bl_label = 'Import Stl (.stl) Object'
    bl_description = 'Load a STL triangle mesh data'
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = '.stl'
    filter_glob = StringProperty(default='*.stl', options={'HIDDEN'})

    def execute(self, context):
        if context.object != None:
            if context.object.mode != 'OBJECT':
                self.report({'ERROR'}, 'This operation can be performed only in object mode')
                return {'CANCELLED'}

            bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.import_mesh.stl(filepath=self.filepath)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()
        bpy.ops.object.scale_clear()
        bpy.ops.view3d.view_selected()

        return {'FINISHED'}


class EnterEditMode(bpy.types.Operator):
    bl_idname = 'opr.enter_edit_mode'
    bl_label = 'Enter Edit Mode'
    bl_description = 'Sets the object interaction mode: Edit Mode'

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.ed.undo_push(message='Toggle Editmode')

        return {'FINISHED'}


class EnterObjectMode(bpy.types.Operator):
    bl_idname = 'opr.enter_object_mode'
    bl_label = 'Enter Object Mode'
    bl_description = 'Sets the object interaction mode: Object Mode'

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.ed.undo_push(message='Toggle Editmode')
        return {'FINISHED'}


class FixOrigin(bpy.types.Operator):
    bl_idname = 'opr.fix_origin'
    bl_label = 'Origin To Geometry Bounds'
    bl_description = 'Move object origin to center of object geometry bounds'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        return {'FINISHED'}


class AddDecimateModifier(bpy.types.Operator):
    bl_idname = 'opr.add_decimate_modifier'
    bl_label = 'Add Decimate Modifier'
    bl_description = 'Add a modifier to the active object: Decimate'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        bpy.ops.object.modifier_add(type='DECIMATE')

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        obj.modifiers['Decimate'].name = 'DCIM.Decimate'
        return {'FINISHED'}


class MoveUpDecimateModifier(bpy.types.Operator):
    bl_idname = 'opr.move_up_decimate_modifier'
    bl_label = 'Move Up Decimate Modifier'
    bl_description = 'Move modifier up in the stack'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        bpy.ops.object.modifier_move_up(modifier='DCIM.Decimate')
        return {'FINISHED'}


class MoveDownDecimateModifier(bpy.types.Operator):
    bl_idname = 'opr.move_down_decimate_modifier'
    bl_label = 'Move Down Decimate Modifier'
    bl_description = 'Move modifier down in the stack'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation cann be performed only on MeshType objects')
            return {'CANCELLED'}

        bpy.ops.object.modifier_move_down(modifier='DCIM.Decimate')
        return {'FINISHED'}


class RemoveDecimateModifier(bpy.types.Operator):
    bl_idname = 'opr.remove_decimate_modifier'
    bl_label = 'Remove Decimate Modifier'
    bl_description = 'Remove modifier from the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        bpy.ops.object.modifier_remove(modifier='DCIM.Decimate')
        return {'FINISHED'}


class ApplyDecimateModifier(bpy.types.Operator):
    bl_idname = 'opr.apply_decimate_modifier'
    bl_label = 'Apply Decimate Modifier'
    bl_description = 'Apply modifier and remove from the stack'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        bpy.ops.object.modifier_apply(apply_as='DATA', modifier='DCIM.Decimate')
        return {'FINISHED'}


class AddSmoothModifier(bpy.types.Operator):
    bl_idname = 'opr.add_smooth_modifier'
    bl_label = 'Add Smooth Modifier'
    bl_description = 'Add a modifier to the active object: Smooth'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        bpy.ops.object.modifier_add(type='SMOOTH')

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        obj.modifiers['Smooth'].name = 'DCIM.Smooth'

        return {'FINISHED'}


class MoveUpSmoothModifier(bpy.types.Operator):
    bl_idname = 'opr.move_up_smooth_modifier'
    bl_label = 'Move Up Smooth Modifier'
    bl_description = 'Move modifier up in the stack'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        bpy.ops.object.modifier_move_up(modifier='DCIM.Smooth')
        return {'FINISHED'}


class MoveDownSmoothModifier(bpy.types.Operator):
    bl_idname = 'opr.move_down_smooth_modifier'
    bl_label = 'Move Down Smooth Modifier'
    bl_description = 'Move modifier down in the stack'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        bpy.ops.object.modifier_move_down(modifier='DCIM.Smooth')
        return {'FINISHED'}


class RemoveSmoothModifier(bpy.types.Operator):
    bl_idname = 'opr.remove_smooth_modifier'
    bl_label = 'Remove Smooth Modifier'
    bl_description = 'Remove modifier from the active object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        bpy.ops.object.modifier_remove(modifier='DCIM.Smooth')
        return {'FINISHED'}


class ApplyAsShapeSmoothModifier(bpy.types.Operator):
    bl_idname = 'opr.apply_as_shape_smooth_modifier'
    bl_label = 'Apply as Shape Smooth Modifier'
    bl_description = 'Apply modifier and remove from the stack'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        bpy.ops.object.modifier_apply(apply_as='SHAPE', modifier='DCIM.Smooth')

        return {'FINISHED'}


class ApplySmoothModifier(bpy.types.Operator):
    bl_idname = 'opr.apply_smooth_modifier'
    bl_label = 'Apply Smooth Modifier'
    bl_description = 'Apply modifier and remove from the stack'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        bpy.ops.object.modifier_apply(apply_as='DATA', modifier='DCIM.Smooth')

        return {'FINISHED'}


class TrimExpand(bpy.types.Operator):
    bl_idname = 'opr.trim_expand'
    bl_label = 'Expand Trim Panel'
    bl_description = 'Expand/reduce trim properties panel'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.trim_expand = not context.scene.trim_expand
        return {'FINISHED'}


class SaveTrimmed(bpy.types.Operator):
    bl_idname = 'opr.save_trimmed'
    bl_label = 'Save Trimmed'
    bl_description = 'Save trimmed object as a new object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot trim NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'Only MeshType objects can be trimmed')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot trim hidden object')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        guard = False

        if context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            guard = True
        elif context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'Cannot perform dissection in this interaction mode')
            return {'CANCELLED'}

        new_obj_name = obj_name + '.Trimmed'

        bpy.ops.object.duplicate()

        dup_obj_name = context.object.name
        new_obj = bpy.data.objects[dup_obj_name]
        new_obj.name = new_obj_name
        new_obj.data.name = new_obj_name

        f_trim(self, context)

        if context.scene.trim_origin_translation:
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

            new_obj.location.y += - obj.dimensions.y - 1.0

        new_obj.select = False
        obj.select = True
        context.scene.objects.active = obj

        if guard:
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


class TrimObject(bpy.types.Operator):
    bl_idname = 'opr.trim_object'
    bl_label = 'Trim Object'
    bl_description = 'Cut out piece of an object by axes'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot trim NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'Only MeshType objects can be trimmed')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot trim hidden object')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        guard = False

        if context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            guard = True
        elif context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'Cannot trim in this interaction mode')
            return {'CANCELLED'}

        f_trim(self, context)

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        if guard:
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


class IntersectExpand(bpy.types.Operator):
    bl_idname = 'opr.intersect_expand'
    bl_label = 'Expand Intersect Panel'
    bl_description = 'Expand/reduce intersect properties panel'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.intersect_expand = not context.scene.intersect_expand
        return {'FINISHED'}


class ShowPrevIntersection(bpy.types.Operator):
    bl_idname = 'opr.show_prev_intersection'
    bl_label = 'Show Prev Intersection'
    bl_description = 'Show previous intersection product'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        f_nav_bis_dis(self, context, 'Intersection', -1, context.scene.intersect_hide)
        return {'FINISHED'}


class ShowNextIntersection(bpy.types.Operator):
    bl_idname = 'opr.show_next_intersection'
    bl_label = 'Show Next Intersection'
    bl_description = 'Show next intersection product'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        f_nav_bis_dis(self, context, 'Intersection', 1, context.scene.intersect_hide)
        return {'FINISHED'}


class SaveIntersection(bpy.types.Operator):
    bl_idname = 'opr.save_intersection'
    bl_label = 'Save Intersection'
    bl_description = 'Save intersection as a new object'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform intersection on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'Intersection can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform intersection on hidden object')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        guard = False

        if context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            guard = True
        elif context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'Cannot perform intersection in this interaction mode')
            return {'CANCELLED'}

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        if context.scene.intersect_plane == '0':
            intersect_plane = 'Z'
        elif context.scene.intersect_plane == '1':
            intersect_plane = 'Y'
        elif context.scene.intersect_plane == '2':
            intersect_plane = 'X'

        new_obj_name = obj_name + '.Intersection.' + intersect_plane

        bpy.ops.object.duplicate()

        dup_obj_name = context.object.name
        new_obj = bpy.data.objects[dup_obj_name]
        new_obj.name = new_obj_name
        new_obj.data.name = new_obj_name

        if context.scene.intersect_origin == '0':
            if intersect_plane == 'X':
                new_obj_location_x = - obj.location.x
                new_obj_location_y = - obj.dimensions.y - 1.0
                new_obj_location_z = 0
            elif intersect_plane == 'Y':
                new_obj_location_x = 0
                new_obj_location_y = - obj.location.y - obj.dimensions.y - 1.0
                new_obj_location_z = 0
            elif intersect_plane == 'Z':
                new_obj_location_x = 0
                new_obj_location_y = - obj.dimensions.y - 1.0
                new_obj_location_z = - obj.location.z
        elif context.scene.intersect_origin == '1':
            if intersect_plane == 'X':
                new_obj_location_x = - obj.location.x - obj.dimensions.x - 1.0
                new_obj_location_y = 0
                new_obj_location_z = 0
            elif intersect_plane == 'Y':
                new_obj_location_x = 0
                new_obj_location_y = - obj.location.y + obj.dimensions.y + 1.0
                new_obj_location_z = 0
            elif intersect_plane == 'Z':
                new_obj_location_x = obj.dimensions.x + 1.0
                new_obj_location_y = 0
                new_obj_location_z = - obj.location.z

        f_intersect(self, context)

        if context.scene.intersect_origin != '2':
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

            new_obj.location.x += new_obj_location_x
            new_obj.location.y += new_obj_location_y
            new_obj.location.z += new_obj_location_z

        new_obj.select = False
        obj.select = True
        context.scene.objects.active = obj

        if guard:
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


class IntersectObject(bpy.types.Operator):
    bl_idname = 'opr.intersect_object'
    bl_label = 'Intersect Object'
    bl_description = 'Cut geometry along a plane'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform intersection on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'Intersection can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform intersection on hidden object')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        f_intersect(self, context)

        return {'FINISHED'}


class DissectExpand(bpy.types.Operator):
    bl_idname = 'opr.dissect_expand'
    bl_label = 'Expand Dissect Panel'
    bl_description = 'Expand/reduce dissect properties panel'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.dissect_expand = not context.scene.dissect_expand
        return {'FINISHED'}


class ShowPrevDissection(bpy.types.Operator):
    bl_idname = 'opr.show_prev_dissection'
    bl_label = 'Show Prev Dissection'
    bl_description = 'Show previous dissection product'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        f_nav_bis_dis(self, context, 'Dissection', -1, context.scene.dissect_hide)
        return {'FINISHED'}


class ShowNextDissection(bpy.types.Operator):
    bl_idname = 'opr.show_next_dissection'
    bl_label = 'Show Next Dissection'
    bl_description = 'Show next dissection product'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        f_nav_bis_dis(self, context, 'Dissection', 1, context.scene.dissect_hide)
        return {'FINISHED'}


class DissectObject(bpy.types.Operator):
    bl_idname = 'opr.dissect_object'
    bl_label = 'Dissect Object'
    bl_description = 'Cut object into slices'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform dissection on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'Dissection can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform dissection on hidden object')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        guard = False

        if context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            guard = True
        elif context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'Cannot perform dissection in this interaction mode')
            return {'CANCELLED'}

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        if context.scene.dissect_plane == '0':
            dissect_plane = 'Z'

            start = obj.location.z - obj.dimensions.z / 2 + obj.dimensions.z * context.scene.dissect_start / 100.0
            end = obj.location.z - obj.dimensions.z / 2 + obj.dimensions.z * context.scene.dissect_end / 100.0
        elif context.scene.dissect_plane == '1':
            dissect_plane = 'Y'

            start = obj.location.y - obj.dimensions.y / 2 + obj.dimensions.y * context.scene.dissect_start / 100.0
            end = obj.location.y - obj.dimensions.y / 2 + obj.dimensions.y * context.scene.dissect_end / 100.0
        elif context.scene.dissect_plane == '2':
            dissect_plane = 'X'

            start = obj.location.x - obj.dimensions.x / 2 + obj.dimensions.x * context.scene.dissect_start / 100.0
            end = obj.location.x - obj.dimensions.x / 2 + obj.dimensions.x * context.scene.dissect_end / 100.0

        i = start

        while True:
            if context.scene.dissect_uncut:
                if i == start:
                    dissect_clear_inner = False
                    dissect_clear_outer = True
                elif i >= end - context.scene.dissect_step:
                    dissect_clear_inner = True
                    dissect_clear_outer = False
                else:
                    dissect_clear_inner = True
                    dissect_clear_outer = True
            else:
                dissect_clear_inner = True
                dissect_clear_outer = True

            if i >= end:
                break

            new_obj_name = obj_name + '.Dissection.' + dissect_plane

            bpy.ops.object.duplicate()

            dup_obj_name = context.object.name
            new_obj = bpy.data.objects[dup_obj_name]
            new_obj.name = new_obj_name
            new_obj.data.name = new_obj_name

            if context.scene.dissect_origin == '0':
                new_obj_location_x = 0
                new_obj_location_y = - obj.dimensions.y - 1.0
                new_obj_location_z = 0
            elif context.scene.dissect_origin == '1':
                if dissect_plane == 'X':
                    new_obj_location_x = - obj.dimensions.x - 1.0
                    new_obj_location_y = 0
                    new_obj_location_z = 0
                elif dissect_plane == 'Y':
                    new_obj_location_x = 0
                    new_obj_location_y = obj.dimensions.y + 1.0
                    new_obj_location_z = 0
                elif dissect_plane == 'Z':
                    new_obj_location_x = obj.dimensions.x + 1.0
                    new_obj_location_y = 0
                    new_obj_location_z = 0

            new_obj_mesh = new_obj.data

            bpy.ops.object.mode_set(mode='EDIT')

            if new_obj_mesh.total_vert_sel > 0:
                bpy.ops.mesh.select_all(action='TOGGLE')

            bpy.ops.mesh.select_all(action='TOGGLE')

            if dissect_plane == 'X':
                dissect_co_x = i
                dissect_co_y = dissect_co_z = 0

                dissect_no_x = 1
                dissect_no_y = dissect_no_z = 0
            elif dissect_plane == 'Y':
                dissect_co_y = i
                dissect_co_x = dissect_co_z = 0

                dissect_no_y = 1
                dissect_no_x = dissect_no_z = 0
            elif dissect_plane == 'Z':
                dissect_co_z = i
                dissect_co_x = dissect_co_y = 0

                dissect_no_z = 1
                dissect_no_x = dissect_no_y = 0

            bpy.ops.mesh.bisect(
                plane_co=(dissect_co_x, dissect_co_y, dissect_co_z),
                plane_no=(dissect_no_x, dissect_no_y, dissect_no_z),
                use_fill=context.scene.dissect_use_fill,
                clear_inner=dissect_clear_inner,
                clear_outer=dissect_clear_outer,
                threshold=0.00001
            )

            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.mesh.select_all(action='TOGGLE')

            bpy.ops.object.mode_set(mode='OBJECT')

            if context.scene.dissect_origin != '2':
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

                new_obj.location.x += new_obj_location_x
                new_obj.location.y += new_obj_location_y
                new_obj.location.z += new_obj_location_z

            new_obj.select = False
            obj.select = True
            context.scene.objects.active = obj

            i += context.scene.dissect_step

        if guard:
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


class ClearLoc(bpy.types.Operator):
    bl_idname = 'opr.clear_loc'
    bl_label = 'Reset Location'
    bl_description = 'Reset the object\'s location'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.location_clear()

        return {'FINISHED'}


class ApplyLoc(bpy.types.Operator):
    bl_idname = 'opr.apply_loc'
    bl_label = 'Apply Location'
    bl_description = 'Apply the object\'s location'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

        return {'FINISHED'}


class ClearRot(bpy.types.Operator):
    bl_idname = 'opr.clear_rot'
    bl_label = 'Reset Rotation'
    bl_description = 'Reset the object\'s rotation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.rotation_clear()

        return {'FINISHED'}


class ApplyRot(bpy.types.Operator):
    bl_idname = 'opr.apply_rot'
    bl_label = 'Apply Rotation'
    bl_description = 'Apply the object\'s rotation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        return {'FINISHED'}


class ClearScl(bpy.types.Operator):
    bl_idname = 'opr.clear_scl'
    bl_label = 'Reset Scale'
    bl_description = 'Reset the object\'s scale'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.scale_clear()

        context.scene.objects[obj_name].delta_scale.xyz = 1.0
        obj.delta_scale.xyz = 1.0
        context.object.delta_scale.xyz = 1.0

        return {'FINISHED'}


class ApplyScl(bpy.types.Operator):
    bl_idname = 'opr.apply_scl'
    bl_label = 'Apply Scale'
    bl_description = 'Apply the object\'s scale'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        context.scene.objects[obj_name].delta_scale.xyz = 1.0
        obj.delta_scale.xyz = 1.0
        context.object.delta_scale.xyz = 1.0

        return {'FINISHED'}


class ShowRenderAllSelected(bpy.types.Operator):  # nb: CamelCase
    bl_idname = "view3d.render_show_all_selected"  # nb underscore_case
    bl_label = "Render On"
    bl_description = 'Render all objects'
    trigger = BoolProperty(default=False)
    mode = BoolProperty(default=False)

    def execute(self, context):
        rendershowselected()
        return {'FINISHED'}


class HideRenderAllSelected(bpy.types.Operator):
    bl_idname = "view3d.render_hide_all_selected"
    bl_label = "Render Off"
    bl_description = 'Hide Selected Object(s) from Render'
    trigger = BoolProperty(default=False)
    mode = BoolProperty(default=False)

    def execute(self, context):
        renderhideselected()
        return {'FINISHED'}


class Transform(bpy.types.Panel):
    bl_idname = 'pan.transform'
    bl_label = 'Transform Extend'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Move'
    bl_options = {'DEFAULT_CLOSED'}

    bpy.types.Object.delta_scale_xyz = FloatProperty(options={'HIDDEN'}, name='XYZ', min=0.0, max=20.0, step=1, default=1.0, update=f_delta_scale_xyz,
                                                     description='Proportional scaling in every direction')

    def draw(self, context):
        layout = self.layout

        if context.object != None:
            obj_name = context.object.name
            obj = bpy.data.objects[obj_name]

            if	obj_name[-12 : -2] != '.Intersection'	and obj_name[-16 : -5] != '.Intersection.'		and obj_name[-17 : -6] != '.Intersection.' \
                    and obj_name[-13: -2] != '.Dissection' and obj_name[-17: -5] != '.Dissection.' and obj_name[-18: -6] != '.Dissection.':
                box = layout.box()
                col = box.column()
                col.label(text='Name:')
                col.prop(obj, 'name', text='')

            if not context.object.hide:
                if context.object.mode != 'EDIT':
                    box = layout.box()
                    col = box.column()
                    col.prop(context.object, 'location')

                    col = box.column()
                    spl = col.split(0.5)
                    col = spl.column()
                    col.operator('opr.clear_loc', text='Reset')

                    if context.object.type == 'MESH':
                        col = spl.column()
                        col.operator('opr.apply_loc', text='Apply')

                    box = layout.box()
                    col = box.column()
                    col.prop(context.object, 'rotation_euler')

                    col = box.column()
                    spl = col.split(0.5)
                    col = spl.column()
                    col.operator('opr.clear_rot', text='Reset')

                    if context.object.type == 'MESH':
                        col = spl.column()
                        col.operator('opr.apply_rot', text='Apply')

                    box = layout.box()
                    col = box.column()
                    col.label(text='Delta Scale:')
                    col.prop(obj, 'delta_scale_xyz')
                    col = box.column()
                    col.prop(context.object, 'scale')

                    col = box.column()
                    spl = col.split(0.5)
                    col = spl.column()
                    col.operator('opr.clear_scl', text='Reset')

                    if context.object.type == 'MESH':
                        col = spl.column()
                        col.operator('opr.apply_scl', text='Apply')

# Auto Mirror


def register():
    bpy.utils.register_class(OrbitUpView)
    bpy.utils.register_class(OrbitLeftView)
    bpy.utils.register_class(OrbitRightView)
    bpy.utils.register_class(OrbitDownView)
    bpy.utils.register_class(PanUpView)
    bpy.utils.register_class(PanLeftView)
    bpy.utils.register_class(PanRightView)
    bpy.utils.register_class(PanDownView)
    bpy.utils.register_class(ZoomInView)
    bpy.utils.register_class(ZoomOutView)
    bpy.utils.register_class(RollLeftView)
    bpy.utils.register_class(RollRightView)
    bpy.utils.register_class(LeftViewpoint)
    bpy.utils.register_class(RightViewpoint)
    bpy.utils.register_class(FrontViewpoint)
    bpy.utils.register_class(BackViewpoint)
    bpy.utils.register_class(TopViewpoint)
    bpy.utils.register_class(BottomViewpoint)
    bpy.utils.register_class(ShowHideObject)
    bpy.utils.register_class(ShowAllObjects)
    bpy.utils.register_class(HideAllObjects)
    bpy.utils.register_class(SelectAll)
    bpy.utils.register_class(InverseSelection)
    bpy.utils.register_class(LoopMultiSelect)
    bpy.utils.register_class(DeleteVerts)
    bpy.utils.register_class(DeleteEdges)
    bpy.utils.register_class(DeleteFaces)
    bpy.utils.register_class(DeleteOnlyFaces)
    bpy.utils.register_class(DeleteOnlyEdgesFaces)
    bpy.utils.register_class(ImportPlyObject)
    bpy.utils.register_class(ImportStlObject)
    bpy.utils.register_class(EnterEditMode)
    bpy.utils.register_class(EnterObjectMode)
    bpy.utils.register_class(FixOrigin)
    bpy.utils.register_class(AddDecimateModifier)
    bpy.utils.register_class(MoveUpDecimateModifier)
    bpy.utils.register_class(MoveDownDecimateModifier)
    bpy.utils.register_class(RemoveDecimateModifier)
    bpy.utils.register_class(ApplyDecimateModifier)
    bpy.utils.register_class(AddSmoothModifier)
    bpy.utils.register_class(MoveUpSmoothModifier)
    bpy.utils.register_class(MoveDownSmoothModifier)
    bpy.utils.register_class(RemoveSmoothModifier)
    bpy.utils.register_class(ApplyAsShapeSmoothModifier)
    bpy.utils.register_class(ApplySmoothModifier)
    bpy.utils.register_class(TrimExpand)
    bpy.utils.register_class(SaveTrimmed)
    bpy.utils.register_class(TrimObject)
    bpy.utils.register_class(IntersectExpand)
    bpy.utils.register_class(ShowPrevIntersection)
    bpy.utils.register_class(ShowNextIntersection)
    bpy.utils.register_class(SaveIntersection)
    bpy.utils.register_class(IntersectObject)
    bpy.utils.register_class(DissectExpand)
    bpy.utils.register_class(ShowPrevDissection)
    bpy.utils.register_class(ShowNextDissection)
    bpy.utils.register_class(DissectObject)
    bpy.utils.register_class(ClearLoc)
    bpy.utils.register_class(ApplyLoc)
    bpy.utils.register_class(ClearRot)
    bpy.utils.register_class(ApplyRot)
    bpy.utils.register_class(ClearScl)
    bpy.utils.register_class(ApplyScl)
    bpy.utils.register_class(Transform)


def unregister():
    bpy.utils.unregister_class(OrbitUpView)
    bpy.utils.unregister_class(OrbitLeftView)
    bpy.utils.unregister_class(OrbitRightView)
    bpy.utils.unregister_class(OrbitDownView)
    bpy.utils.unregister_class(PanUpView)
    bpy.utils.unregister_class(PanLeftView)
    bpy.utils.unregister_class(PanRightView)
    bpy.utils.unregister_class(PanDownView)
    bpy.utils.unregister_class(ZoomInView)
    bpy.utils.unregister_class(ZoomOutView)
    bpy.utils.unregister_class(RollLeftView)
    bpy.utils.unregister_class(RollRightView)
    bpy.utils.unregister_class(LeftViewpoint)
    bpy.utils.unregister_class(RightViewpoint)
    bpy.utils.unregister_class(FrontViewpoint)
    bpy.utils.unregister_class(BackViewpoint)
    bpy.utils.unregister_class(TopViewpoint)
    bpy.utils.unregister_class(BottomViewpoint)
    bpy.utils.unregister_class(ShowHideObject)
    bpy.utils.unregister_class(ShowAllObjects)
    bpy.utils.unregister_class(HideAllObjects)
    bpy.utils.unregister_class(SelectAll)
    bpy.utils.unregister_class(InverseSelection)
    bpy.utils.unregister_class(LoopMultiSelect)
    bpy.utils.unregister_class(DeleteVerts)
    bpy.utils.unregister_class(DeleteEdges)
    bpy.utils.unregister_class(DeleteFaces)
    bpy.utils.unregister_class(DeleteOnlyFaces)
    bpy.utils.unregister_class(DeleteOnlyEdgesFaces)
    bpy.utils.unregister_class(ImportPlyObject)
    bpy.utils.unregister_class(ImportStlObject)
    bpy.utils.unregister_class(EnterEditMode)
    bpy.utils.unregister_class(EnterObjectMode)
    bpy.utils.unregister_class(FixOrigin)
    bpy.utils.unregister_class(AddDecimateModifier)
    bpy.utils.unregister_class(MoveUpDecimateModifier)
    bpy.utils.unregister_class(MoveDownDecimateModifier)
    bpy.utils.unregister_class(RemoveDecimateModifier)
    bpy.utils.unregister_class(ApplyDecimateModifier)
    bpy.utils.unregister_class(AddSmoothModifier)
    bpy.utils.unregister_class(MoveUpSmoothModifier)
    bpy.utils.unregister_class(MoveDownSmoothModifier)
    bpy.utils.unregister_class(RemoveSmoothModifier)
    bpy.utils.unregister_class(ApplyAsShapeSmoothModifier)
    bpy.utils.unregister_class(ApplySmoothModifier)
    bpy.utils.unregister_class(TrimExpand)
    bpy.utils.unregister_class(SaveTrimmed)
    bpy.utils.unregister_class(TrimObject)
    bpy.utils.unregister_class(IntersectExpand)
    bpy.utils.unregister_class(ShowPrevIntersection)
    bpy.utils.unregister_class(ShowNextIntersection)
    bpy.utils.unregister_class(SaveIntersection)
    bpy.utils.unregister_class(IntersectObject)
    bpy.utils.unregister_class(DissectExpand)
    bpy.utils.unregister_class(ShowPrevDissection)
    bpy.utils.unregister_class(ShowNextDissection)
    bpy.utils.unregister_class(DissectObject)
    bpy.utils.unregister_class(ClearLoc)
    bpy.utils.unregister_class(ApplyLoc)
    bpy.utils.unregister_class(ClearRot)
    bpy.utils.unregister_class(ApplyRot)
    bpy.utils.unregister_class(ClearScl)
    bpy.utils.unregister_class(ApplyScl)
    bpy.utils.unregister_class(Transform)

if __name__ == '__main__':
    register()
