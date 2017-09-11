bl_info = {
    "name": "Create Camera Image Plane",
    "author": "Torbjörn Westerlund",
    "category": "Object"
}

import bpy
from bpy_extras.image_utils import load_image
from mathutils import Vector, Euler
import math


class CreateCameraImagePlane(bpy.types.Operator):
    """Create image plane for camera"""
    bl_idname = "object.createcameraimageplane"
    bl_label = "Camera Image Plane"
    bl_options = {'REGISTER', 'UNDO'}

    def SetupDriverVariables(self, driver, imageplane):
        camAngle = driver.variables.new()
        camAngle.name = 'camAngle'
        camAngle.type = 'SINGLE_PROP'
        camAngle.targets[0].id = imageplane.parent
        camAngle.targets[0].data_path = "data.angle"

        depth = driver.variables.new()
        depth.name = 'depth'
        depth.type = 'TRANSFORMS'
        depth.targets[0].id = imageplane
        depth.targets[0].data_path = 'location'
        depth.targets[0].transform_type = 'LOC_Z'
        depth.targets[0].transform_space = 'LOCAL_SPACE'

    # unfortunately not possible to add driver on scene object
    #    resolution_x = driver.variables.new()
    #    resolution_x.name = 'resolution_x'
    #    resolution_x.type = 'SINGLE_PROP'
    #    resolution_x.targets[0].id =bpy.context.scene
    #    resolution_x.targets[0].data_path = 'render.resolution_x'
    #    resolution_y = driver.variables.new()
    #    resolution_y.name = 'resolution_y'
    #    resolution_y.type = 'SINGLE_PROP'
    #    resolution_y.targets[0].id =bpy.context.scene
    #    resolution_y.targets[0].data_path = 'render.resolution_y'
    #    pixel_x = driver.variables.new()
    #    pixel_x.name = 'pixel_x'
    #    pixel_x.type = 'SINGLE_PROP'
    #    pixel_x.targets[0].id =bpy.context.scene
    #    pixel_x.targets[0].data_path = 'render.pixel_aspect_x'
    #    pixel_y = driver.variables.new()
    #    pixel_y.name = 'pixel_y'
    #    pixel_y.type = 'SINGLE_PROP'
    #    pixel_y.targets[0].id =bpy.context.scene
    #    pixel_y.targets[0].data_path = 'render.pixel_aspect_y'

    def SetupDriversForImagePlane(self, imageplane):
        driver = imageplane.driver_add('scale', 1).driver
        driver.type = 'SCRIPTED'
        self.SetupDriverVariables(driver, imageplane)
        # driver.expression ="-depth*math.tan(camAngle/2)*resolution_y*pixel_y/(resolution_x*pixel_x)"
        driver.expression = "-depth*tan(camAngle/2)*bpy.context.scene.render.resolution_y * bpy.context.scene.render.pixel_aspect_y/(bpy.context.scene.render.resolution_x * bpy.context.scene.render.pixel_aspect_x)"
        driver = imageplane.driver_add('scale', 0).driver
        driver.type = 'SCRIPTED'
        self.SetupDriverVariables(driver, imageplane)
        driver.expression = "-depth*tan(camAngle/2)"

    # get selected camera (might traverse children of selected object until a camera is found?)
    # for now just pick the active object
    def createImagePlaneForCamera(self, camera):
        imageplane = None
        try:
            depth = 10

            # create imageplane
            bpy.ops.mesh.primitive_plane_add()  # radius = 0.5)
            imageplane = bpy.context.active_object
            imageplane.name = "imageplane"
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))
            bpy.ops.uv.smart_project(angle_limit=66, island_margin=0, user_area_weight=0)
            bpy.ops.uv.select_all(action='TOGGLE')
            bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1))
            bpy.ops.object.editmode_toggle()

            imageplane.location = (0, 0, -depth)
            imageplane.parent = camera

            # calculate scale
            # REPLACED WITH CREATING EXPRESSIONS
            self.SetupDriversForImagePlane(imageplane)

            # setup material
            if(len(imageplane.material_slots) == 0):
                bpy.ops.object.material_slot_add()
                # imageplane.material_slots.
            bpy.ops.material.new()
            mat_index = len(bpy.data.materials) - 1
            imageplane.material_slots[0].material = bpy.data.materials[mat_index]
            material = imageplane.material_slots[0].material
            # if not returned by new use imgeplane.material_slots[0].material
            material.name = 'mat_imageplane_' + camera.name
            material.use_nodes = True
            nodes = material.node_tree.nodes
            links = material.node_tree.links

            nodes.clear()
            emissive = nodes.new('ShaderNodeEmission')
            emissive.location = 0, 0
            transparent = nodes.new('ShaderNodeBsdfTransparent')
            transparent.location = 0, 100
            mix = nodes.new('ShaderNodeMixShader')
            mix.location = 400, 0
            links.new(emissive.outputs[0], mix.inputs[2])
            links.new(transparent.outputs[0], mix.inputs[1])
            outnode = nodes.new('ShaderNodeOutputMaterial')
            outnode.location = 800, 0
            links.new(mix.outputs[0], outnode.inputs[0])
            texture = nodes.new('ShaderNodeTexImage')
            texture.location = -400, 0
            links.new(texture.outputs[0], emissive.inputs[0])
            links.new(texture.outputs[1], mix.inputs[0])
            # texture.image = bpy.ops.image.open(filepath="c:\\nova\\keyed\\1\\1_5_1\\1_5_1.00000.png")

        except Exception as e:
            imageplane.select = False
            camera.select = True
            raise e
        return {'FINISHED'}

    def execute(self, context):
        camera = bpy.context.active_object  # bpy.data.objects['Camera']
        return self.createImagePlaneForCamera(camera)


# main
print("========================")
print("   SCRIPT STARTING")
print("========================")

# camera = bpy.context.active_object  # bpy.data.objects['Camera']
# createImagePlaneForCamera(camera)


# def register():
#    bpy.utils.register_class(CreateCameraImagePlane)
# def unregister():
#    bpy.utils.unregister_class(CreateCameraImagePlane)

def menu_func(self, context):
    self.layout.operator(CreateCameraImagePlane.bl_idname, icon='FILE_IMAGE')


def register():
    bpy.utils.register_class(CreateCameraImagePlane)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(CreateCameraImagePlane)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
