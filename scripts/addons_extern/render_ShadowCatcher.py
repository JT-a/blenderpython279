bl_info = {
    "name": "Shadow Catcher",
    "author": "Steve Hargreaves (Roken)",
    "version": (1, 0),
    "blender": (2, 7, 7),
    "location": "View3D > Tools > Shadow Catcher",
    "description": "Enables/Disables the shadow catcher and background",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"}

import bpy
import io
import sys
import os

# def scene_init(lock,passedSleepTime):
#    time.sleep(passedSleepTime) # Feel free to alter time in seconds as needed.
#    print("Threading: scene_init")


class ShadowCatcherPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Shadow Catcher Panel"
    bl_idname = "OBJECT_PT_Shadow"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Shadow Catcher"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)

        row = layout.row()
        row.prop(scene, "enable")

        row = layout.row()
        row.prop(scene, "background")


def setupscenes():
    def_scene = bpy.context.scene
    def_scene.name = "Scene"
    main_layer = bpy.data.scenes["Scene"].render.layers.new(name="Main")
    main_layer = bpy.data.scenes["Scene"].render.layers.new(name="Shadow")
    main_layer = bpy.data.scenes["Scene"].render.layers.new(name="Shadow Clean")
    bpy.ops.scene.render_layer_remove()

    background_scene = bpy.ops.scene.new(type="EMPTY")
    bg_scene = bpy.context.scene
    bg_scene.name = "Scene Background"
    bg_layer = bpy.data.scenes["Scene Background"].render.layers.new(name="Background")
    bpy.ops.scene.render_layer_remove()
    bpy.data.scenes["Scene Background"].cycles.samples = 1
    # bpy.data.scenes["Scene Background"].render.layers["RenderLayer"].use = False

    # Main layer
    for layer in range(0, len(bpy.context.scene.layers)):
        bpy.data.scenes["Scene Background"].render.layers["Background"].layers[layer] = False

    for layer in range(1, len(bpy.context.scene.layers)):
        print(layer)
        bpy.data.scenes["Scene"].render.layers["Main"].layers[layer] = False

    for layer in range(0, len(bpy.context.scene.layers)):
        print(layer)
        bpy.data.scenes["Scene"].render.layers["Main"].layers_exclude[layer] = False

    for layer in range(0, len(bpy.context.scene.layers)):
        print(layer)
        bpy.data.scenes["Scene"].render.layers["Main"].layers_zmask[layer] = False

    # Shadow layer
    for layer in range(0, len(bpy.context.scene.layers)):
        bpy.data.scenes["Scene"].render.layers["Shadow"].layers[layer] = False

    for layer in range(0, len(bpy.context.scene.layers)):
        print(layer)
        bpy.data.scenes["Scene"].render.layers["Shadow"].layers[layer] = False

    for layer in range(0, len(bpy.context.scene.layers)):
        print(layer)
        bpy.data.scenes["Scene"].render.layers["Shadow"].layers_exclude[layer] = False

    for layer in range(0, len(bpy.context.scene.layers)):
        print(layer)
        bpy.data.scenes["Scene"].render.layers["Shadow"].layers_zmask[layer] = False

    bpy.data.scenes["Scene"].render.layers["Shadow"].layers[1] = True
    bpy.data.scenes["Scene"].render.layers["Shadow"].layers[19] = False

    # Clean Shadow layer
    for layer in range(0, len(bpy.context.scene.layers)):
        bpy.data.scenes["Scene"].render.layers["Shadow Clean"].layers[layer] = False

    for layer in range(0, len(bpy.context.scene.layers)):
        print(layer)
        bpy.data.scenes["Scene"].render.layers["Shadow Clean"].layers[layer] = False

    for layer in range(0, len(bpy.context.scene.layers)):
        print(layer)
        bpy.data.scenes["Scene"].render.layers["Shadow Clean"].layers_exclude[layer] = False

    for layer in range(0, len(bpy.context.scene.layers)):
        print(layer)
        bpy.data.scenes["Scene"].render.layers["Shadow Clean"].layers_zmask[layer] = False

    bpy.data.scenes["Scene"].render.layers["Shadow Clean"].layers[1] = True
    bpy.data.scenes["Scene"].render.layers["Shadow Clean"].layers[19] = False
    bpy.data.scenes["Scene"].render.layers["Shadow Clean"].layers_exclude[0] = True

    bpy.context.screen.scene = bpy.data.scenes["Scene"]

    return


def setcomp():
    # Switch on nodes
    bpy.context.scene.use_nodes = True
    comptree = bpy.context.scene.node_tree
    complinks = comptree.links

    # clear default nodes
    for node in comptree.nodes:
        comptree.nodes.remove(node)

    # create input image node
    main_node = comptree.nodes.new(type='CompositorNodeRLayers')
    main_node.location = 0, 0
    main_node.scene = bpy.data.scenes['Scene']
    main_node.layer = "Main"

    subtract_node = comptree.nodes.new(type='CompositorNodeMixRGB')
    subtract_node.location = 400, 0
    subtract_node.blend_type = 'SUBTRACT'

    mix_node = comptree.nodes.new(type='CompositorNodeMixRGB')
    mix_node.location = 1000, -100
    mix_node.blend_type = 'MULTIPLY'

    invert_node = comptree.nodes.new(type='CompositorNodeInvert')
    invert_node.location = 500, 0

    RGB1_node = comptree.nodes.new(type='CompositorNodeCurveRGB')
    RGB1_node.location = 600, 0
    RGB2_node = comptree.nodes.new(type='CompositorNodeCurveRGB')
    RGB2_node.location = 850, 0

    shadow_node = comptree.nodes.new(type='CompositorNodeRLayers')
    shadow_node.location = 100, 100
    shadow_node.scene = bpy.data.scenes['Scene']
    shadow_node.layer = "Shadow"

    clean_node = comptree.nodes.new(type='CompositorNodeRLayers')
    clean_node.location = 200, 200
    clean_node.scene = bpy.data.scenes['Scene']
    clean_node.layer = "Shadow Clean"

    background_node = comptree.nodes.new(type='CompositorNodeRLayers')
    background_node.location = 0, 200
    background_node.scene = bpy.data.scenes['Scene Background']
    background_node.layer = "Background"

    alpha_node = comptree.nodes.new(type='CompositorNodeAlphaOver')
    alpha_node.location = 1100, 100

    # create output node
    comp_node_main = comptree.nodes.new('CompositorNodeComposite')
    comp_node_main.location = 1500, 0
    # link nodes
    link = complinks.new(shadow_node.outputs[0], subtract_node.inputs[2])
    link = complinks.new(clean_node.outputs[0], subtract_node.inputs[1])
    link = complinks.new(subtract_node.outputs[0], invert_node.inputs[1])
    link = complinks.new(invert_node.outputs[0], RGB1_node.inputs[1])
    link = complinks.new(RGB1_node.outputs[0], RGB2_node.inputs[1])
    link = complinks.new(RGB2_node.outputs[0], mix_node.inputs[2])
    link = complinks.new(background_node.outputs[0], mix_node.inputs[1])
    link = complinks.new(mix_node.outputs[0], alpha_node.inputs[1])
    link = complinks.new(main_node.outputs[0], alpha_node.inputs[2])
    link = complinks.new(alpha_node.outputs[0], comp_node_main.inputs[0])
    if bpy.data.scenes["Scene"].enable is False:
        link = complinks.new(main_node.outputs[0], comp_node_main.inputs[0])
    if bpy.data.scenes["Scene"].background is False:
        link = complinks.remove(background_node.outputs[0].links[0])
        mix_node.inputs[1].default_value[3] = 0
    return(complinks)


def shadowtoggle(self, context):
    global firstrun
    print(bpy.data.scenes["Scene"].enable)
    if firstrun is True:
        if bpy.data.scenes["Scene"].enable is True:
            setupscenes()
            firstrun = False

    if bpy.data.scenes["Scene"].enable is True:
        setcomp()
        bpy.data.scenes["Scene"].render.layers["Shadow"].use = bpy.data.scenes["Scene"].enable
        bpy.data.scenes["Scene"].render.layers["Shadow Clean"].use = bpy.data.scenes["Scene"].enable
        bpy.data.scenes["Scene"].cycles.film_transparent = bpy.data.scenes["Scene"].enable
        bpy.data.scenes["Scene"].render.layers["Main"].layers[1] = abs(bpy.data.scenes["Scene"].enable - 1)
    return


def backgroundtoggle(self, context):
    bpy.data.scenes["Scene Background"].render.layers["Background"].use = bpy.data.scenes["Scene"].background
    bpy.data.scenes["Scene Background"].cycles.film_transparent = abs(bpy.data.scenes["Scene"].background - 1)
    setcomp()
    return


def register():
    print("Starting")
    global firstrun
    firstrun = True
    bpy.types.Scene.enable = bpy.props.BoolProperty(
        name="Enable or Disable",
        description="Enable Shadow Catcher",
        default=0,
        update=shadowtoggle
    )

    bpy.types.Scene.background = bpy.props.BoolProperty(
        name="Enable or Disable background",
        description="Enable background",
        default=0,
        update=backgroundtoggle
    )

    bpy.utils.register_class(ShadowCatcherPanel)


def unregister():
    bpy.utils.unregister_class(ShadowCatcherPanel)

register()
