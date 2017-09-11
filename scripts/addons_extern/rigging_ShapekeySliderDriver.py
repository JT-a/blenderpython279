bl_info = {
    "name": "Shapekey Slider Driver",
    "author": "Fernando Macias-Jimenez",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "View3D > Add > Armature",
    "description": "Creates a 3D-View UI slider to control a shape key.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"}

import bpy
from math import pi


class ShapekeySliderCreator(bpy.types.Operator):
    """Shapekey Slider Driver"""
    bl_idname = "object.ssd"
    bl_label = "Shapekey Slider Driver"
    bl_options = {'REGISTER', 'UNDO'}

    mesh = []
    amt = bpy.props.PointerProperty()
    rig = bpy.props.PointerProperty()
    slider = bpy.props.PointerProperty()

    def createArmature(self):

        # Create armature and object
        arm = bpy.data.armatures.new("GUIcontrol_Armature")
        self.amt = arm
        self.rig = bpy.data.objects.new("GUIcontrol", self.amt)
        self.rig.location = (0, 0, 0)
        self.rig.show_x_ray = True
        self.amt.show_names = False
        # Link object to scene
        scn = bpy.context.scene
        scn.objects.link(self.rig)

        scn.update()

        # Create bones
    # next two lines by PKHG SVN 36504 W32
        bpy.context.scene.objects.active = self.rig
        bpy.ops.object.editmode_toggle()
    #    bpy.ops.object.mode_set(mode='EDIT')
    # original does not work??!!    bpy.ops.object.mode_set(mode='EDIT')
        base = self.amt.edit_bones.new('Base')
        base.head = (0, 0, 0)
        base.tail = (0, 0, 0.4)
        base.show_wire = True

        self.slider = self.amt.edit_bones.new('Slider')
        self.slider.head = (0, 0, 0.4)
        self.slider.tail = (0, 0, 0.8)
        self.slider.parent = base
        self.slider.use_connect = False
        self.slider.show_wire = True

        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.mode_set(mode='POSE')

        slidered = bpy.context.active_object.pose.bones["Slider"]
        slidered.lock_location[0] = True
        slidered.lock_location[2] = True
        slidered.custom_shape = bpy.data.objects["S_Slider"]

        holder = bpy.context.active_object.pose.bones["Base"]
        holder.custom_shape = bpy.data.objects["S_Holder"]

        pMid = self.rig.pose.bones['Slider']
        cns1 = pMid.constraints.new('LIMIT_LOCATION')
        cns1.name = 'LocLimit'
        cns1.owner_space = 'LOCAL'
        cns1.use_min_y = True
        cns1.min_y = 0.0
        cns1.use_max_y = True
        cns1.max_y = 0.7
        cns1.use_transform_limit = True

        bpy.ops.object.mode_set(mode='OBJECT')

        return

    def createText(self):

        loc = (0, 0, 0)
        # layers = 20*[False]
        # layers[18] = True
        bpy.ops.object.text_add(
            location=loc,
            rotation=(pi / 2, 0, 0),
            # layers=layers
        )
        txt = bpy.context.object
        txt.name = "Text"
        txt.show_name = False
        tcu = txt.data
        tcu.name = "Text"

        # TextCurve attributes
        tcu.body = "Text"
        tcu.font = bpy.data.fonts[0]
        # tcu.offset_x = -9
        # tcu.offset_y = -0.25
        # tcu.shear = 0.5
        tcu.size = 0.2
        # tcu.space_character = 2
        # tcu.space_word = 4
        txt.draw_type = 'WIRE'

        # arm = bpy.data.objects["GUIcontrol"]
        # txt = bpy.data.objects["Text"]
        txt.parent = self.rig  # arm

        txt.location = self.rig.location  # arm.location
        txt.location.x = txt.location.x - 0.2
        txt.location.z = txt.location.z + 0.05

        return

    def createShapes(self):

        layers = 20 * [False]
        layers[19] = True
        scn = bpy.context.scene
        scn.layers[19] = True

        bpy.ops.mesh.primitive_plane_add(
            location=(0, 0, 0),
            layers=layers
        )
        ob1 = bpy.context.object
        ob1.name = "S_Slider"
        pl1 = ob1.data
        pl1.name = "S_Slider"

        bpy.ops.mesh.primitive_plane_add(
            location=(0, 0, 0),
            layers=layers
        )
        ob2 = bpy.context.object
        ob2.name = "S_Holder"
        pl2 = ob2.data
        pl2.name = "S_Holder"

        # resize Holder shape
        bpy.context.scene.objects.active = ob2
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.transform.resize(value=(1.5, 5.0, 1))
        bpy.ops.transform.resize(value=(0.25, 0.25, 1))
        bpy.ops.transform.translate(value=(0, 1.87, 0))
        bpy.ops.object.mode_set(mode='OBJECT')

        # resize Slider shape
        bpy.context.scene.objects.active = ob1
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.transform.resize(value=(0.25, 0.25, 1))
        bpy.ops.object.mode_set(mode='OBJECT')

        scn.layers[19] = False

        bpy.context.scene.update()

        return

    def createDriver(self):

        bpy.context.scene.objects.active = self.mesh[0]

        fc = bpy.context.active_object.active_shape_key.driver_add('value', -1)
        fc.driver.type = 'AVERAGE'
        dvar = fc.driver.variables.new()
        dvar.type = 'TRANSFORMS'
        dvar.targets[0].id = self.rig
        dvar.targets[0].bone_target = "Slider"
        dvar.targets[0].transform_type = 'LOC_Y'
        dvar.targets[0].transform_space = 'LOCAL_SPACE'

        fmod = fc.modifiers[0]
        fmod.coefficients = (0.0, 1.428)

        return

    def execute(self, context):

        self.mesh = bpy.context.selected_objects
        print(self.mesh)
        self.createShapes()
        self.createArmature()
        self.createText()
        if self.mesh:
            if self.mesh[0].type == 'MESH':
                bpy.context.scene.objects.active = self.mesh[0]
                if bpy.context.active_object.active_shape_key:
                    self.createDriver()
        for n in bpy.data.objects:
            n.select = False
        bpy.context.scene.objects.active = self.rig
        bpy.data.objects[self.rig.name].select = True

        return {'FINISHED'}


def add_object_button(self, context):
    self.layout.operator(
        ShapekeySliderCreator.bl_idname,
        text=ShapekeySliderCreator.__doc__,
        icon='PLUGIN')


def register():
    bpy.utils.register_class(ShapekeySliderCreator)
    bpy.types.INFO_MT_armature_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(ShapekeySliderCreator)
    bpy.types.INFO_MT_armature_add.remove(add_object_button)

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()
