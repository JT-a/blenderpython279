bl_info = {
    "name": "Pixel Art to Cubes",
    "category": "Object"
}

import bpy


class To3DPixels(bpy.types.Operator):
    """Convert to Voxels"""
    bl_idname = "object.pixel_art"
    bl_label = "Create 3D Pixel Art"
    bl_options = {'REGISTER', 'UNDO'}

    # Settings for default material for all our cubes.
    def makeMat(self, name, d, s, a):
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = d
        mat.diffuse_shader = "LAMBERT"
        mat.diffuse_intensity = 1.0
        mat.specular_color = s
        mat.specular_shader = "COOKTORR"
        mat.specular_intensity = 0.5
        mat.alpha = a
        return mat

    # Apply a mat to an object
    def setMat(self, ob, mat):
        me = ob.data
        me.materials.append(mat)

    def execute(self, context):
        cursor = bpy.context.scene.cursor_location  # Grab 3D cursors position
        for area in bpy.context.screen.areas:
            if bpy.context.area.type == 'IMAGE_EDITOR':
                image_object = bpy.context.area.spaces.active.image  # Use the active image editor's image for the pixel art
                break
            else:
                return {"CANCELLED"}  # Active space isn't an image editor cancel out
        count = 0
        for y in range(image_object.size[1]):
            for x in range(image_object.size[0]):
                if image_object.pixels[count + 3] > 0:  # We don't need fully transparent cubes, so lets only make one if alpha > 0
                    pixel_color = (
                        image_object.pixels[count],  # Red
                        image_object.pixels[count + 1],  # Green
                        image_object.pixels[count + 2]  # Blue
                    )
                    bpy.ops.mesh.primitive_cube_add(  # Add our pixel's cube
                        radius=0.49,  # ToDo make easier to customize via UI
                        location=[x + (cursor[0] - image_object.size[0] / 2), y + (cursor[1] - image_object.size[1] / 2), 0 + cursor[2]])  # Places center of pixel art at cursor
                    newmat = self.makeMat("pixel", (pixel_color), (1.0, 1.0, 1.0), 1)  # Create a new material with the diffuse color of the pixel
                    self.setMat(bpy.context.object, newmat)  # apply the mat to our pixel
                count += 4

        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(To3DPixels.bl_idname)


def register():
    bpy.utils.register_class(To3DPixels)
    bpy.types.IMAGE_MT_image.append(menu_func)


def unregister():
    bpy.utils.unregister_class(To3DPixels)
    bpy.types.IMAGE_MT_image.remove(menu_func)
