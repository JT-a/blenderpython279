bl_info = {
    "name": "BatchBake-dirtmap v2.0",
    "description": "Script to bake AO-Dirtmap for a group of objects",
    "author": "Sergey Sharybin ( v2.0 script rewrite ) Nicolò Zubbini(for v0.1 proof-of-concept script)",
    "version": (0, 1),
    "blender": (2, 61, 4),
    "location": "Properties > Render > BatchBake",
    "warning": "work in progress",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/"
                "Scripts/My_Script",
    "tracker_url": "http://projects.blender.org/tracker/index.php?"
                   "func=detail&aid=<number>",
    "category": "Render"}

import bpy
from bpy.types import Operator, Panel


def LOG(message):
    if False:
        print(message)
    else:
        pass


class RENDER_OT_batch_unwrap_bake(Operator):
    bl_idname = "render.batch_unwrap_bake"
    bl_label = "Batch Unwrap and bake"
    bl_space_type = 'VIEW_3D'

    def _set_ut_texture_image(self, objects, image_name):
        for ob in objects:
            data = ob.data

            active_uv = data.uv_textures.active

            for d in active_uv.data:
                d.image = bpy.data.images[image_name]

    def _flip_normals(self, scene, objects):
        for ob in objects:
            scene.objects.active = ob
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    def _create_compat(self, contrast, image, image_ao2_name,
            image_ao_name, image_inv_ao_name):
        if image + '_AOComp' in bpy.data.materials:
            mat = bpy.data.materials[image + '_AOComp']
        else:
            mat = bpy.data.materials.new(image + '_AOComp')

        mat.use_shadeless = True
        mat.diffuse_color = (0.55, 0.55, 0.55)
        for slot in range(9):
            mat.texture_slots.clear(index=slot)

        for img in [image_ao_name, image_inv_ao_name, image_ao2_name]:
            if img not in bpy.data.textures:
                cTex = bpy.data.textures.new(img, type='IMAGE')

            mtex = mat.texture_slots.add()
            cTex = bpy.data.textures[img]
            cTex.image = bpy.data.images[img]
            mtex.texture = cTex
            mtex.texture_coords = 'UV'
            mtex.mapping = 'FLAT'
            mtex.use_map_color_diffuse = True

            if img.endswith('AO'):
                mtex.blend_type = 'MULTIPLY'
                mtex.diffuse_color_factor = contrast
            elif img.endswith('AOInv'):
                mtex.blend_type = 'ADD'
                mtex.invert = True
                mtex.diffuse_color_factor = contrast * 1.35
            elif img.endswith('AO2'):
                mtex.blend_type = 'MULTIPLY'
                mtex.diffuse_color_factor = contrast * 1.1

    def _teporary_disable(self, objects):
        disabled = {}
        for ob in objects:
            for mod in ob.modifiers:
                if mod.show_render:
                    if mod.type in ['BEVEL', 'SOLIDIFY', 'MIRROR', 'ARRAY']:
                        if ob.name in disabled:
                            disabled[ob.name].append(mod.name)
                        else:
                            disabled[ob.name] = [mod.name]
                        mod.show_render = False
        return disabled

    def _teporary_enable(self, disabled):
        for obname in disabled:
            for modname in disabled[obname]:
                bpy.data.objects[obname].modifiers[modname].show_render = True

    def execute(self, context):
        scene = context.scene

#        use_color_management = scene.render.use_color_management
        light_dist = scene.world.light_settings.distance
        old_samples = scene.world.light_settings.samples
        obact = scene.objects.active

        AODist = scene.BatchBakeAODist
        InvAODist = scene.BatchBakeInvAODist
        uvmap = scene.BatchBakeUVMap
        image = scene.BatchBakeImage
        resolution_x = scene.BatchBakeResolX
        resolution_y = scene.BatchBakeResolY
        auto_unwrap = scene.BatchBakeAutoUnwrap
        contrast = scene.BatchBakeContrast
        samples = scene.BatchBakeSamples

        image_ao2_name = image + "_" + "AO2"
        image_ao_name = image + "_" + "AO"
        image_inv_ao_name = image + "_" + "AOInv"
        image_dirt_name = image + "_" + "DIRT"
        all_image_names = [image_ao2_name, image_ao_name,
                image_inv_ao_name, image_dirt_name]

        # list of all affecting objects
        LOG("Creating list of objects to be baked")
        objects = []
        for ob in scene.objects:
            if ob.is_visible(scene) and ob.select:
                if ob.type == 'MESH':
                    objects.append(ob)
                else:
                    ob.select = False

        disabled = self._teporary_disable(objects)

        LOG("Ensuring for objects' material slots")
        for ob in objects:
            if not ob.material_slots:
                mat_name = "BatchBakeMaterial"
                if mat_name not in bpy.data.materials:
                    bpy.data.materials.new(name=mat_name)
                ob.data.materials.append(bpy.data.materials[mat_name])

        # create needed images
        LOG("Creating images to bake to")
        for name in all_image_names:
            if name not in bpy.data.images:
                bpy.data.images.new(name=name,
                        width=resolution_x, height=resolution_y)
            else:
                img = bpy.data.images[name]
                img.generated_width = resolution_x
                img.generated_height = resolution_y

        # create UV layers and assign image
        LOG("Creating UV layers for baking objects")
        for ob in objects:
            data = ob.data

            if uvmap not in data.uv_textures:
                data.uv_textures.new(name=uvmap)

            data.uv_textures.active = data.uv_textures[uvmap]
            data.uv_textures.active.active_render = True

        # unwrap
        if auto_unwrap:
            LOG("Unwrapping objects")
            bpy.ops.uv.smart_project(island_margin=0.01, user_area_weight=0)

        #  setup baking settings
#        scene.render.use_color_management = False
        scene.render.bake_type = 'AO'
        scene.render.use_bake_clear = False
        scene.render.use_bake_antialiasing = True
        scene.render.use_bake_normalize = True
        scene.world.light_settings.samples = samples

        ##  batch bake each object

        # bake AO 1
        LOG("Baking AO")
        self._set_ut_texture_image(objects, image_ao_name)
        scene.world.light_settings.distance = AODist
        bpy.ops.object.bake_image()

        # bake AO 2
        LOG("Baking AO2")
        self._set_ut_texture_image(objects, image_ao2_name)
        scene.world.light_settings.distance = AODist * 0.25
        bpy.ops.object.bake_image()

        # bake inverted AO
        LOG("Baking inverted AO")
        self._flip_normals(scene, objects)
        self._set_ut_texture_image(objects, image_inv_ao_name)

        scene.world.light_settings.distance = InvAODist

        bpy.ops.object.bake_image()

        self._flip_normals(scene, objects)

        ## bake AO and Inv AO together
        ### material creation
        LOG("Creating composite material")
        self._create_compat(contrast, image, image_ao2_name, image_ao_name,
                image_inv_ao_name)

        # duplicate for final bake
        LOG("Duplicating and joining objects for final bake")
        bpy.ops.object.duplicate()
        
        # ensure the active object has multires 'WORKAROUND' - bug [#31637]
        for ob in bpy.context.selected_objects:
            if {True for m in ob.modifiers
                    if m.type == 'MULTIRES' and (m.sculpt_levels or m.render_levels)}:

                scene.objects.active = ob
                break
        # end workaround

        bpy.ops.object.join()

        # assign bake material
        ob = bpy.context.selected_objects[0]

        LOG("Adding composite material slot to joined object")
        for slot in ob.material_slots:
            slot.material = bpy.data.materials[image + '_AOComp']

        # create and assign new image
        LOG("Assigning image for final bake")
        for d in ob.data.uv_textures[uvmap].data:
            d.image = bpy.data.images[image_dirt_name]

        # settings and bake textures
        scene.render.bake_type = 'TEXTURE'
        scene.render.use_bake_clear = True
        LOG("Final bake")
        bpy.ops.object.bake_image()
        LOG("Deleting temporary objects")
        bpy.ops.object.delete(use_global=False)

        # assign final dirt map to group
        LOG("Assign final dirt map to objects")
        self._set_ut_texture_image(objects, image_dirt_name)

        self._teporary_enable(disabled)

#        scene.render.use_color_management = use_color_management
        scene.world.light_settings.distance = light_dist
        scene.objects.active = obact
        scene.world.light_settings.samples = old_samples

        for ob in objects:
            ob.select = True

        return {'FINISHED'}


class RENDER_PT_batch_bake(Panel):
    bl_label = "Batch Bake"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    COMPAT_ENGINES = {'BLENDER_RENDER'}

    @classmethod
    def poll(cls, context):
        return context.active_object

    def draw(self, context):
        scene = context.scene
        obact = context.active_object
        me = obact.data if obact.type == 'MESH' else None

        layout = self.layout
        col = layout.column()

        col.prop(scene, "BatchBakeImage")

        if me:
            col.prop_search(scene, "BatchBakeUVMap", me, "uv_textures")
        else:
            col.prop(scene, "BatchBakeUVMap")
        col.prop(scene, "BatchBakeAutoUnwrap")

        split = layout.split()
        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Resolution")
        sub.prop(scene, "BatchBakeResolX", text="X")
        sub.prop(scene, "BatchBakeResolY", text="Y")

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="AD Distance")
        sub.prop(scene, "BatchBakeAODist", text="Distance")
        sub.prop(scene, "BatchBakeInvAODist", text="Inverse")

        col = layout.column(align=True)
        col.prop(scene, "BatchBakeContrast")
        col.prop(scene, "BatchBakeSamples")

        layout.operator("render.batch_unwrap_bake")


def register():
    bpy.types.Scene.BatchBakeImage = bpy.props.StringProperty(
            name="Image",
            default='batchbake',
            description="Prefix for name of image data blocks " + \
                        "crated when baking")

    bpy.types.Scene.BatchBakeUVMap = bpy.props.StringProperty(
            name="UV map",
            default='dirtmap',
            description="Name of UV map to be used for baking")

    bpy.types.Scene.BatchBakeAODist = bpy.props.FloatProperty(
            name="AO Distance",
            default=1.5,
            description="Radius for concave/dark areas")

    bpy.types.Scene.BatchBakeInvAODist = bpy.props.FloatProperty(
            name="Invese AO R",
            default=0.1,
            description="Radius for edges/bright areas")

    bpy.types.Scene.BatchBakeResolX = bpy.props.IntProperty(
            name="Resolution X",
            default=1024,
            min=4,
            max=30000,
            description="Resolution in X direction for baking images")

    bpy.types.Scene.BatchBakeResolY = bpy.props.IntProperty(
            name="Resolution Y",
            default=1024,
            min=4,
            max=30000,
            description="Resolution in Y direction for baking images")

    bpy.types.Scene.BatchBakeAutoUnwrap = bpy.props.BoolProperty(
            name="Auto Unwrap",
            default=True,
            description="Use auto LSCM unwrap")

    bpy.types.Scene.BatchBakeContrast = bpy.props.FloatProperty(
            name="AO Contrast",
            default=1.25,
            description="Contrast for final dirtmap")

    bpy.types.Scene.BatchBakeSamples = bpy.props.IntProperty(
            name="AO Samples",
            default=5,
            min=0,
            max=1000,
            description="Number of AO samples when baking")

    bpy.utils.register_module(__name__)


def unregister():
    del bpy.types.Scene.BatchBakeImage
    del bpy.types.Scene.BatchBakeUVMap
    del bpy.types.Scene.BatchBakeAORadius
    del bpy.types.Scene.BatchBakeInvAORadius
    del bpy.types.Scene.BatchBakeResolX
    del bpy.types.Scene.BatchBakeResolY
    del bpy.types.Scene.BatchBakeAutoUnwrap
    del bpy.types.Scene.BatchBakeContrast
    del bpy.types.Scene.BatchBakeSamples

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
