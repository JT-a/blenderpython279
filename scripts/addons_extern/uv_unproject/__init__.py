bl_info = {
    'name': "UV Unproject",
    'author': "Matthew Collett",
    'version': (0, 9, 8),
    'blender': (2, 7, 0),
    'api': '19e627c',
    'location': "UV/Image Editor > UVs > UV Unproject",
    'description': "Create a camera from a perspective view represented in UV coordinates",
    'warning': "",
    'wiki_url': "",
    'tracker_url': "",
    'support': 'COMMUNITY',
    'category': "UV"}

import bpy
import mathutils
from mathutils import Matrix, Vector
from uv_unproject import camera_resection

DEFAULT_SENSOR = 32.0  # Notional size of sensor or film in Blender camera (mm)
TELEPHOTO_LENGTH = 5000.0  # Maximum focal length of Blender camera (mm)


class ModeSaver():
    '''Preserve and restore the mode of the active object by RAII.'''

    def __enter__(self):
        self.mode = bpy.context.active_object.mode
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    def __exit__(self, _type, _value, _traceback):
        bpy.ops.object.mode_set(mode=self.mode, toggle=False)


def selectedUVs(mesh, context, uvlayer=None):
    '''Get the vertices visible and selected in the UV view.'''
    sync = context.scene.tool_settings.use_uv_select_sync
    uvlayer = uvlayer or mesh.uv_layers.active
    uvs = {}
    for f, uv in zip(mesh.loops, uvlayer.data):
        if mesh.vertices[f.vertex_index].select and (sync or uv.select):
            uvs[f.vertex_index] = uv.uv
    return uvs


def sensorSize(lens):
    '''Get the effective sensor size'''
    return lens.sensor_height if lens.sensor_fit == 'VERTICAL' else lens.sensor_width


def fitAspect(fit, width, height):
    '''Get the aspect ratio of an image; selected or larger dimension = 1.0.'''
    extent = {
        'HORIZONTAL': width,
        'VERTICAL': height
    }.get(fit, max(width, height))
    return [width / extent, height / extent]


def imageAspect(frame_aspect, image):
    '''Get the aspect ratio of an image cropped to camera frame.'''
    if image and image.has_data:
        scale = min(image.size[0] / frame_aspect[0], image.size[1] / frame_aspect[1])
        return [image.size[0] / scale, image.size[1] / scale]
    else:
        return render_aspect


def scale2D(p, scale, centre=(0.5, 0.5)):
    '''Scale and recentre image points.'''
    return (scale[0] * (p[0] - centre[0]), scale[1] * (p[1] - centre[1]))


def diagonal(v):
    '''Make a 4x4 diagonal matrix from a 3-vector.'''
    m = Matrix([[v[0], 0, 0], [0, v[1], 0], [0, 0, v[2]]])
    m.resize_4x4()
    return m


def extendClip(lens, closest, furthest):
    '''Extend camera clipping range if needed.'''
    if lens.clip_start > closest:
        lens.clip_start = closest / 2.0
    if lens.clip_end < furthest:
        lens.clip_end = 2.0 * furthest - closest

######################################################################


class UVUnproject(bpy.types.Operator):
    '''Place a camera that would generate the active UV mapping by projection.'''
    bl_idname = 'uv.unproject'
    bl_label = "UV Unproject"
    bl_options = {'REGISTER', 'UNDO'}

    name = bpy.props.StringProperty(name="Camera name",
                                    description="Name of new or existing camera")
    camera = bpy.props.EnumProperty(name="Camera type",
                                    items=[('PERSP', "Perspective", "A perspective camera"),
                                           ('ORTHO', "Orthographic", "An orthographic camera")],
                                    description="Camera type", default='PERSP')
    centering = bpy.props.EnumProperty(name="Centering",
                                       items=[('EXACT', "Exact", "Optical centre at image centre"),
                                              ('APPROX', "Approximate", "Optical centre near image centre"),
                                              ('NONE', "None", "Optical centre anywhere")],
                                       description="Constraint on optical centre", default='APPROX')
    weight = bpy.props.FloatProperty(name="Weight",
                                     description="Weight of approximate centering", default=0.01)
    fixed = bpy.props.BoolProperty(name="Fixed camera",
                                   description="Move object intead of camera")
    rescale = bpy.props.BoolVectorProperty(name="Scale", subtype='XYZ',
                                           description="For models with unknown proportions")

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.uv_textures)

    def execute(self, context):
        with ModeSaver():
            return self(context)

    def __call__(self, context):
        model = context.active_object
        mesh = model.data
        ortho = (self.camera == 'ORTHO')
        centering = self.weight
        if self.centering == 'EXACT':
            centering = -1
        elif self.centering == 'NONE':
            centering = 0

        # Use the vertices visible and selected in the UV view
        selected = selectedUVs(mesh, context)
        if len(selected) < (4 if ortho else 6):
            self.report({'ERROR_INVALID_INPUT'}, "UV Unproject needs more vertices")
            return {'CANCELLED'}

        # Get the existing camera, if any
        camera = context.scene.objects.get(self.name)
        if camera and (camera.type == 'CAMERA'):
            lens = camera.data
            fit = lens.sensor_fit
            telephoto = TELEPHOTO_LENGTH / (max(sensorSize(lens), DEFAULT_SENSOR))
        else:
            fit = 'AUTO'
            telephoto = TELEPHOTO_LENGTH / DEFAULT_SENSOR
            camera = None

        # Normalise 2D coordinates; 3D coordinates in world space
        render = context.scene.render
        aspect = imageAspect(
            fitAspect(fit, render.resolution_x, render.resolution_y),
            context.edit_image
        )
        points = [((model.matrix_world * mesh.vertices[v].co)[0:3],
                   scale2D(u, aspect)) for v, u in selected.items()]

        # Calculate camera matrix
        try:
            if not ortho:
                f, shift, ext, scale, converged = camera_resection.resect_persp(
                    points, centering, self.rescale)
                ortho = f > telephoto
            if ortho:
                f, ext, scale, converged = camera_resection.resect_ortho(
                    points, self.rescale)
                shift = (0.0, 0.0)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        if not converged:
            self.report({'WARNING'}, "Poor convergence of camera matrix")

        # Set camera parameters
        if not camera:
            lens = bpy.data.cameras.new(self.name)
            camera = bpy.data.objects.new(self.name, lens)
            context.scene.objects.link(camera)
        if ortho:
            lens.type = 'ORTHO'
            lens.ortho_scale = 1.0 / f
            lens.shift_x = 0.0
            lens.shift_y = 0.0
        else:
            lens.type = 'PERSP'
            lens.lens = f * sensorSize(lens)
            lens.shift_x = -shift[0]
            lens.shift_y = -shift[1]

        # Set relative position of camera and subject, and scale of subject
        external = Matrix(ext)
        external.resize_4x4()
        if self.fixed:
            model.matrix_world = (camera.matrix_world * external *
                                  diagonal(scale) * model.matrix_world)
        else:
            camera.matrix_world = external.inverted()
            model.matrix_world = diagonal(scale) * model.matrix_world

        # Ensure clipping range includes all vertices
        origin = Vector(camera.location)
        direction = -Vector(camera.matrix_world.col[2][0:3])
        mat = model.matrix_world
        dist = [(mat * mesh.vertices[v].co - origin) * direction
                for v in selected]
        extendClip(lens, min(dist), max(dist))

        return {'FINISHED'}

    def invoke(self, context, event):
        mesh = context.active_object.data
        self.name = mesh.uv_textures.active.name
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout.row()
        row.prop(self, 'name')
        row = self.layout.row()
        row = row.split(percentage=0.6)
        row.prop(self, 'camera', text="", icon='CAMERA_DATA')
        row.alignment = 'RIGHT'
        row.prop(self, 'fixed')
        row = self.layout.row()
        row = row.split(percentage=0.6)
        row.prop(self, 'centering')
        row.prop(self, 'weight')
        row = self.layout.row()
        row.alignment = 'LEFT'
        row.prop(self, 'rescale')


def menu_item(menu, context):
    menu.layout.operator(UVUnproject.bl_idname)


def register():
    bpy.utils.register_class(UVUnproject)
    bpy.types.IMAGE_MT_uvs.append(menu_item)


def unregister():
    bpy.types.IMAGE_MT_uvs.remove(menu_item)
    bpy.utils.unregister_class(UVUnproject)

if __name__ == '__main__':
    register()

    # test call
    bpy.ops.uv.unproject('INVOKE_DEFAULT')
