import bpy

# Metadata for the addon

bl_info = {
    "name": "Cycles Auto Image",
    "author": "Théo Friberg",
    "blender": (2, 70, 0),
    "location": "With Cycles as the active render engine and a mesh"
    " selected, Space > Automatic Material from Image",
    "description": "One-click material setup from texture for the Cycles"
    " render engine. Blur from:"
    " https://bwide.wordpress.com/node-groups/bwide-nodepack-for-blender/",
    "warning": "Still a work in progress",
    "wiki_url": "",
    "tracker_url": "mailto:theo.friberg@gmail.com?subject="
    "Bug report for Cycles Automatic Materials addon&body="
    "I have come across the following error while using the Cycles automatic"
    " materials addon (Please explain both the symptoms of the error and"
    " what you were doing when the error occured. If you think a specific"
    " action of yours is related to the error, please include a description"
    " of it too.):",
    "support": "COMMUNITY",
    "category": "Material"}


class AutomatOperatorFromTexture(bpy.types.Operator):

    """This operator generates automatic materials from textures in Cycles.

This is a subclass from bpy.types.Operator.
"""

    # Metadata of the operator

    bl_idname = "com.new_automat"
    bl_label = "Automatic Material from Image"
    bl_options = {"UNDO"}

    # Variables used for storing the filepath given by blender's file manager

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    filename = bpy.props.StringProperty()
    directory = bpy.props.StringProperty(subtype="FILE_PATH")

    def _addBlurSetup(self, context, mat, x, y, strength=0.5):
        """Function that adds the blur's nodes to the given material at the
given position

Blur based on work by Sebastian “bashi” Röthlisberger, see here:
https://bwide.wordpress.com/node-groups/bwide-nodepack-for-blender/
for the rest of his nodes.  The blur is called ImageBlur.

This is private.
"""

        # Take a reference to the trees nodes.

        nodes = mat.node_tree.nodes

        # Create a dictionary representing the nodes.

        nodes_dict = {
            "Correct strength vector math": ("ShaderNodeVectorMath", (x, y)),
            "Add noise": ("ShaderNodeVectorMath", (x - 200, y)),
            "Correct strength": ("ShaderNodeMixRGB", (x - 400, y)),
            "Transform to RGB": ("ShaderNodeMixRGB", (x - 400, y - 200)),
            "Blur strength": ("ShaderNodeValue", (x - 800, y - 50)),
            "Noise source": ("ShaderNodeTexNoise", (x - 600, y - 150))
        }

        # Create the actual nodes.

        for node_name in nodes_dict.keys():
            technical_name = nodes_dict[node_name][0]
            location = nodes_dict[node_name][1]
            nodes_dict[node_name] = nodes.new(technical_name)
            nodes_dict[node_name].location = location
            nodes_dict[node_name].name = node_name
            nodes_dict[node_name].label = node_name

        # Set the settings of nodes that have some.

        nodes_dict["Correct strength vector math"].operation = "SUBTRACT"
        nodes_dict["Correct strength"].inputs[1].default_value = (0, 0, 0, 1)
        nodes_dict["Transform to RGB"].inputs[1].default_value = (1, 1, 1, 1)
        nodes_dict["Transform to RGB"].inputs[2].default_value = (0, 0, 0, 1)
        nodes_dict["Noise source"].inputs[1].default_value = 1000.0
        nodes_dict["Blur strength"].outputs[0].default_value = strength

        # Link up the nodes.

        links = mat.node_tree.links

        links.new(nodes_dict["Noise source"].outputs["Color"],
                  nodes_dict["Correct strength"].inputs["Color2"])
        links.new(nodes_dict["Correct strength"].outputs["Color"],
                  nodes_dict["Add noise"].inputs[1])
        links.new(nodes_dict["Blur strength"].outputs[0],
                  nodes_dict["Correct strength"].inputs[0])
        links.new(nodes_dict["Blur strength"].outputs[0],
                  nodes_dict["Transform to RGB"].inputs[0])
        links.new(nodes_dict["Add noise"].outputs["Vector"],
                  nodes_dict["Correct strength vector math"].inputs[0])
        links.new(nodes_dict["Transform to RGB"].outputs["Color"],
                  nodes_dict["Correct strength vector math"].inputs[1])

        # Return the references to the inputs and outputs.

        return {"in": [nodes_dict["Add noise"]], "out": [nodes_dict["Correct strength vector math"]]}

    def execute(self, context):
        """This is the main runnable method of the operator.

This creates all the node setup."""

        # Create the material

        mat = bpy.data.materials.new("Material")

        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        for node in nodes.keys():
            nodes.remove(nodes[node])

        # Add the three blur setups

        blur_setup_1_IO = self._addBlurSetup(context, mat, -2000, -300)
        blur_setup_2_IO = self._addBlurSetup(context, mat, -1800, 300)
        blur_setup_3_IO = self._addBlurSetup(context, mat, -1000, 600, 1000)

        # Create dictionary of the nodes to be used

        nodes_dict = {
            "Texture Co-ordinate": ("ShaderNodeTexCoord", (-3200, 0)),
            "Greater Than": ("ShaderNodeMath", (-1400, 0)),
            "Bumpmap Mix RGB": ("ShaderNodeMixRGB", (-1200, 0)),
            "Color Image": ("ShaderNodeTexImage", (-450, 100)),
            "Bump Image": ("ShaderNodeTexImage", (-850, -150)),
            "Layer Weight": ("ShaderNodeLayerWeight", (-500, 500)),
            "Multiply bumpmap": ("ShaderNodeMixRGB", (-450, -150)),
            "Add bumpmap": ("ShaderNodeMixRGB", (-650, -150)),
            "Add fresnel reflection": ("ShaderNodeMixRGB", (-300, 500)),
            "Diffuse component": ("ShaderNodeBsdfDiffuse", (-100, 100)),
            "Glossy component": ("ShaderNodeBsdfGlossy", (-100, -100)),
            "Mix shader": ("ShaderNodeMixShader", (100, 0)),
            "Desaturate reflection": ("ShaderNodeMixRGB", (-270, 0)),
            "Output": ("ShaderNodeOutputMaterial", (400, 0)),
            "Average color": ("ShaderNodeTexImage", (-750, 400)),
            "Substract average": ("ShaderNodeMath", (-100, 350))}

        # Create the actual nodes

        for node_name in nodes_dict.keys():
            technical_name = nodes_dict[node_name][0]
            location = nodes_dict[node_name][1]
            nodes_dict[node_name] = nodes.new(technical_name)
            nodes_dict[node_name].location = location
            nodes_dict[node_name].name = node_name
            nodes_dict[node_name].label = node_name

        # Set the settings of nodes that have some.

        nodes_dict["Greater Than"].operation = "GREATER_THAN"
        nodes_dict["Greater Than"].inputs[1].default_value = 0.4
        nodes_dict["Multiply bumpmap"].blend_type = "MULTIPLY"
        nodes_dict["Multiply bumpmap"].inputs[0].default_value = 1
        nodes_dict["Multiply bumpmap"].inputs[2].default_value = (0, 0, 1, 1)
        nodes_dict["Add bumpmap"].blend_type = "ADD"
        nodes_dict["Add bumpmap"].inputs[0].default_value = 1
        nodes_dict["Add bumpmap"].inputs[2].default_value = (0, 0, 1, 1)
        nodes_dict["Add fresnel reflection"].blend_type = "MULTIPLY"
        nodes_dict["Add fresnel reflection"].inputs[0].default_value = 1
        nodes_dict["Glossy component"].distribution = "ASHIKHMIN_SHIRLEY"
        nodes_dict["Desaturate reflection"].inputs[0].default_value = 0.7
        nodes_dict["Substract average"].operation = "SUBTRACT"
        nodes_dict["Substract average"].use_clamp = True

        # Open the Image nodes' textures.

        image_data = bpy.data.images.load(self.filepath)
        nodes_dict["Color Image"].image = image_data
        nodes_dict["Bump Image"].image = image_data
        nodes_dict["Average color"].image = image_data

        # Connect the nodes up

        links = mat.node_tree.links

        links.new(nodes_dict["Texture Co-ordinate"].outputs["UV"],
                  nodes_dict["Color Image"].inputs["Vector"])
        links.new(nodes_dict["Texture Co-ordinate"].outputs["UV"],
                  nodes_dict["Multiply bumpmap"].inputs[1])
        links.new(blur_setup_2_IO["out"][0].outputs[0],
                  nodes_dict["Greater Than"].inputs[0])
        links.new(nodes_dict["Greater Than"].outputs[0],
                  nodes_dict["Bumpmap Mix RGB"].inputs[0])
        links.new(nodes_dict["Bumpmap Mix RGB"].outputs["Color"],
                  nodes_dict["Bump Image"].inputs["Vector"])
        links.new(nodes_dict["Color Image"].outputs["Color"],
                  nodes_dict["Diffuse component"].inputs[0])
        links.new(nodes_dict["Color Image"].outputs["Color"],
                  nodes_dict["Desaturate reflection"].inputs[1])
        links.new(nodes_dict["Bump Image"].outputs["Color"],
                  nodes_dict["Add bumpmap"].inputs[1])
        links.new(nodes_dict["Add bumpmap"].outputs["Color"],
                  nodes_dict["Multiply bumpmap"].inputs[1])
        links.new(nodes_dict["Desaturate reflection"].outputs["Color"],
                  nodes_dict["Glossy component"].inputs[0])
        links.new(nodes_dict["Multiply bumpmap"].outputs["Color"],
                  nodes_dict["Glossy component"].inputs["Normal"])
        links.new(nodes_dict["Multiply bumpmap"].outputs["Color"],
                  nodes_dict["Diffuse component"].inputs["Normal"])
        links.new(nodes_dict["Multiply bumpmap"].outputs["Color"],
                  nodes_dict["Layer Weight"].inputs["Normal"])
        links.new(nodes_dict["Layer Weight"].outputs["Fresnel"],
                  nodes_dict["Add fresnel reflection"].inputs[2])
        links.new(nodes_dict["Color Image"].outputs["Color"],
                  nodes_dict["Add fresnel reflection"].inputs[1])
        links.new(nodes_dict["Substract average"].outputs[0],
                  nodes_dict["Mix shader"].inputs[0])
        links.new(nodes_dict["Diffuse component"].outputs["BSDF"],
                  nodes_dict["Mix shader"].inputs[1])
        links.new(nodes_dict["Glossy component"].outputs["BSDF"],
                  nodes_dict["Mix shader"].inputs[2])
        links.new(nodes_dict["Mix shader"].outputs["Shader"],
                  nodes_dict["Output"].inputs[0])
        links.new(blur_setup_1_IO["out"][0].outputs[0],
                  nodes_dict["Bumpmap Mix RGB"].inputs[2])
        links.new(nodes_dict["Texture Co-ordinate"].outputs["UV"],
                  nodes_dict["Bumpmap Mix RGB"].inputs[1])
        links.new(nodes_dict["Texture Co-ordinate"].outputs["UV"],
                  blur_setup_1_IO["in"][0].inputs[0])
        links.new(nodes_dict["Average color"].outputs["Color"],
                  nodes_dict["Substract average"].inputs[0])
        links.new(nodes_dict["Add fresnel reflection"].outputs["Color"],
                  nodes_dict["Substract average"].inputs[1])
        links.new(blur_setup_3_IO["out"][0].outputs[0],
                  nodes_dict["Average color"].inputs[0])

        # Try to add the material to the selected object

        try:
            bpy.context.object.data.materials.append(mat)
        except AttributeError:

            # If there is no object with materials selected,
            # don't add the material to anythinng.

            pass

        # Tell that all went well

        return {"FINISHED"}

    def invoke(self, context, event):
        """This method opens the file browser. After that, the
execute(...) method gets ran, creating the node setup.
It also checks that the render engine is Cycles.  """

        if bpy.context.scene.render.engine == 'CYCLES':
            self.filename = ""
            context.window_manager.fileselect_add(self)
            return {"RUNNING_MODAL"}
        else:
            self.report({'ERROR'}, "Can't generate Cycles material with Blender internal as active renderer.")
            return {"FINISHED"}


def register():
    """This method registers the AutomatOperatorFromTexture
operator.  """

    bpy.utils.register_class(AutomatOperatorFromTexture)


def unregister():
    """This method unregisters the AutomatOperatorFromTexture
operator.  """

    bpy.utils.unregister_class(AutomatOperatorFromTexture)

# Run register if the file is ran from blenders text editor

if __name__ == "__main__":
    register()
