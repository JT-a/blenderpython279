###ADDON INFO###
bl_info = {
        "name": "Barndoor Light",
        "category": "Object",
        "author": "Miika Puustinen"
        }



import bpy


 
 
class OBJECT_OT_addBarndoorLight(bpy.types.Operator):
    bl_idname = "lamp.barndoor_light" #name used to refer to this operator
    bl_label = "Barndoor Light" #operator's label
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add Spotlight with Barndoors" #tooltip
   
    def execute(self, context):

        scene = bpy.context.scene


        #add lamp data
        lamp_data = bpy.data.lamps.new(name="spot_lamp_data", type='SPOT')

        #add lamp ojbect
        lamp_object = bpy.data.objects.new(name="Spot Lamp", object_data=lamp_data)

        #add lamp to scene
        spot = scene.objects.link(lamp_object)


        lamp_data.use_nodes = True





        #ADD NODES
        output_node = lamp_data.node_tree.nodes['Lamp Output']
        output_node.location = (900,300)

        emission1 = lamp_data.node_tree.nodes['Emission']
        emission1.location = (300,300)

        mix_rgb = lamp_data.node_tree.nodes.new('ShaderNodeMixRGB')
        mix_rgb.blend_type = 'MULTIPLY'
        mix_rgb.inputs[0].default_value = 1.0
        mix_rgb.location = (emission1.location[0] -250, emission1.location[1])

        #multiply1
        multiply1 = lamp_data.node_tree.nodes.new('ShaderNodeMath')
        multiply1.operation = 'MULTIPLY'
        multiply1.location = (-300,300)

        #multiply2
        multiply2 = lamp_data.node_tree.nodes.new('ShaderNodeMath')
        multiply2.operation = 'MULTIPLY'
        multiply2.location = (-600,450)

        #multiply3
        multiply3 = lamp_data.node_tree.nodes.new('ShaderNodeMath')
        multiply3.operation = 'MULTIPLY'
        multiply3.location = (-600,150)

        #ramp1
        ramp1 = lamp_data.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp1.color_ramp.interpolation = 'CONSTANT'
        ramp1.color_ramp.elements[0].color = (1,1,1,1)
        ramp1.color_ramp.elements[1].color = (0,0,0,1)
        ramp1.location = (-1000,900)

        #ramp1
        ramp2 = lamp_data.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp2.color_ramp.interpolation = 'CONSTANT'
        ramp2.color_ramp.elements[0].color = (1,1,1,1)
        ramp2.color_ramp.elements[1].color = (0,0,0,1)
        ramp2.location = (ramp1.location[0],ramp1.location[1] - 300)

        #ramp1
        ramp3 = lamp_data.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp3.color_ramp.interpolation = 'CONSTANT'
        ramp3.color_ramp.elements[0].color = (1,1,1,1)
        ramp3.color_ramp.elements[1].color = (0,0,0,1)
        ramp3.location = (ramp2.location[0],ramp2.location[1] - 300)

        #ramp1
        ramp4 = lamp_data.node_tree.nodes.new('ShaderNodeValToRGB')
        ramp4.color_ramp.interpolation = 'CONSTANT'
        ramp4.color_ramp.elements[0].color = (1,1,1,1)
        ramp4.color_ramp.elements[1].color = (0,0,0,1)
        ramp4.location = (ramp3.location[0],ramp3.location[1] - 300)


        #gradient1
        gradient1 = lamp_data.node_tree.nodes.new('ShaderNodeTexGradient')
        gradient1.location = (ramp1.location[0] -300, ramp1.location[1])

        #gradient2
        gradient2 = lamp_data.node_tree.nodes.new('ShaderNodeTexGradient')
        gradient2.location = (gradient1.location[0], gradient1.location[1]-300)

        #gradient2
        gradient3 = lamp_data.node_tree.nodes.new('ShaderNodeTexGradient')
        gradient3.location = (gradient2.location[0], gradient2.location[1]-300)

        #gradient2
        gradient4 = lamp_data.node_tree.nodes.new('ShaderNodeTexGradient')
        gradient4.location = (gradient3.location[0], gradient3.location[1]-300)


        #mapping1
        mapping1 = lamp_data.node_tree.nodes.new('ShaderNodeMapping')
        mapping1.location = (gradient1.location[0] -500, gradient1.location[1])
        mapping1.rotation[1] = 3.141593


        #mapping2
        mapping2 = lamp_data.node_tree.nodes.new('ShaderNodeMapping')
        mapping2.location = (gradient3.location[0] -500, gradient3.location[1]+100)
        mapping2.rotation[2] = 1.570796

        #mapping3
        mapping3 = lamp_data.node_tree.nodes.new('ShaderNodeMapping')
        mapping3.location = (gradient4.location[0] -500, gradient4.location[1])
        mapping3.rotation[2] = -1.570796

        #reroute
        reroute1 = lamp_data.node_tree.nodes.new('NodeReroute')
        reroute1.location = (gradient2.location[0]-1000, gradient2.location[1]-100)

        #combine_XYZ
        combine_xyz1 = lamp_data.node_tree.nodes.new('ShaderNodeCombineXYZ')
        combine_xyz1.location = (reroute1.location[0] -300, reroute1.location[1]+50)

        #divide1
        divide1 = lamp_data.node_tree.nodes.new('ShaderNodeMath')
        divide1.operation = 'DIVIDE'
        divide1.location = (combine_xyz1.location[0]-300 ,combine_xyz1.location[1]+100)

        #divide2
        divide2 = lamp_data.node_tree.nodes.new('ShaderNodeMath')
        divide2.operation = 'DIVIDE'
        divide2.location = (combine_xyz1.location[0]-300 ,combine_xyz1.location[1]-100)

        #combine_XYZ
        separate_xyz1 = lamp_data.node_tree.nodes.new('ShaderNodeSeparateXYZ')
        separate_xyz1.location = (combine_xyz1.location[0]-600 ,combine_xyz1.location[1])


        #mapping4
        mapping4 = lamp_data.node_tree.nodes.new('ShaderNodeMapping')
        mapping4.location = (separate_xyz1.location[0] -600, separate_xyz1.location[1])
        mapping4.use_min = True
        mapping4.use_max = True
        mapping4.min[0] = -1.0
        mapping4.min[1] = -1.0
        mapping4.min[2] = -1.0


        #mapping5
        mapping5 = lamp_data.node_tree.nodes.new('ShaderNodeMapping')
        mapping5.location = (mapping4.location[0] -400, mapping4.location [1])
        mapping5.use_min = True
        mapping5.use_max = True
        mapping5.min[0] = -1.0
        mapping5.min[1] = -1.0
        mapping5.min[2] = -1.0

        #mapping6
        mapping6 = lamp_data.node_tree.nodes.new('ShaderNodeMapping')
        mapping6.location = (mapping5.location[0] -400, mapping5.location [1])
        mapping6.use_min = True
        mapping6.use_max = True
        mapping6.min[0] = -1.0
        mapping6.min[1] = -1.0
        mapping6.min[2] = -1.0

        #geometry node
        geometry1 = lamp_data.node_tree.nodes.new('ShaderNodeNewGeometry')
        geometry1.location = (mapping6.location[0] -400, mapping6.location [1])







        # create a group
        test_group = bpy.data.node_groups.new('BarndoorSettings', 'ShaderNodeTree')


        # create group inputs
        group_inputs = test_group.nodes.new('NodeGroupInput')
        group_inputs.location = (-350,0)
        test_group.inputs.new('NodeSocketShader','Shader In')
        light_color = test_group.inputs.new('NodeSocketColor','Light Color')
        light_color.default_value = (1,1,1,1)
        strength = test_group.inputs.new('NodeSocketFloat','Light Strength')
        strength.min_value = 0
        strength.default_value = 100.0
        left = test_group.inputs.new('NodeSocketFloat','Left')
        left.min_value = 0
        left.max_value = 1.0
        right = test_group.inputs.new('NodeSocketFloat','Right')
        right.min_value = 0
        right.max_value = 1.0
        top = test_group.inputs.new('NodeSocketFloat','Top')
        top.min_value = 0
        top.max_value = 1.0
        bottom = test_group.inputs.new('NodeSocketFloat','Bottom')
        bottom.min_value = 0
        bottom.max_value = 1.0


        # create group outputs
        group_outputs = test_group.nodes.new('NodeGroupOutput')
        group_outputs.location = (300,0)
        test_group.outputs.new('NodeSocketShader','Shader Out')

        # link group in - group out
        test_group.links.new(group_inputs.outputs['Shader In'], group_outputs.inputs['Shader Out'])

        #add group to the scene
        barndoor_settings = lamp_data.node_tree.nodes.new('ShaderNodeGroup')
        barndoor_settings.location = (550,300)
        barndoor_settings.node_tree = test_group



        #CREATE NODE LINKS



        links = lamp_data.node_tree.links
        link = links.new(barndoor_settings.outputs[0], output_node.inputs[0])
        link = links.new(emission1.outputs[0], barndoor_settings.inputs[0])
        link = links.new(mix_rgb.outputs[0], emission1.inputs[0])
        link = links.new(multiply1.outputs[0], mix_rgb.inputs[1])
        link = links.new(multiply2.outputs[0], multiply1.inputs[0])
        link = links.new(multiply3.outputs[0], multiply1.inputs[1])
        link = links.new(ramp1.outputs[0], multiply2.inputs[0])
        link = links.new(ramp2.outputs[0], multiply2.inputs[1])
        link = links.new(ramp3.outputs[0], multiply3.inputs[0])
        link = links.new(ramp4.outputs[0], multiply3.inputs[1])
        link = links.new(gradient1.outputs[0], ramp1.inputs[0])
        link = links.new(gradient2.outputs[0], ramp2.inputs[0])
        link = links.new(gradient3.outputs[0], ramp3.inputs[0])
        link = links.new(gradient4.outputs[0], ramp4.inputs[0])
        link = links.new(mapping1.outputs[0], gradient1.inputs[0])
        link = links.new(reroute1.outputs[0], gradient2.inputs[0])
        link = links.new(mapping2.outputs[0], gradient3.inputs[0])
        link = links.new(mapping3.outputs[0], gradient4.inputs[0])
        link = links.new(reroute1.outputs[0], mapping1.inputs[0])
        link = links.new(reroute1.outputs[0], mapping2.inputs[0])
        link = links.new(reroute1.outputs[0], mapping3.inputs[0])
        link = links.new(combine_xyz1.outputs[0], reroute1.inputs[0])
        link = links.new(divide1.outputs[0], combine_xyz1.inputs[0])
        link = links.new(divide2.outputs[0], combine_xyz1.inputs[1])
        link = links.new(separate_xyz1.outputs[0], divide1.inputs[0])
        link = links.new(separate_xyz1.outputs[1], divide2.inputs[0])
        link = links.new(separate_xyz1.outputs[2], divide1.inputs[1])
        link = links.new(separate_xyz1.outputs[2], divide2.inputs[1])
        link = links.new(separate_xyz1.outputs[2], combine_xyz1.inputs[2])
        link = links.new(mapping4.outputs[0], separate_xyz1.inputs[0])
        link = links.new(mapping5.outputs[0], mapping4.inputs[0])
        link = links.new(mapping6.outputs[0], mapping5.inputs[0])
        link = links.new(geometry1.outputs[4], mapping6.inputs[0])






                #CREATE DRIVERS





        def add_driver_variable(driven, ob_name, property):
            #Create variable
            newVar = driven.driver.variables.new()
            newVar.name = "var"
            
            #If driver is the sky settings
            if ob_name == 'LAMP':
                newVar.targets[0].id_type = 'LAMP'
                newVar.targets[0].id = lamp_data
                newVar.targets[0].data_path = property
                driven.driver.expression = "var"
             
            #if driver is an object   
            else:
                newVar.targets[0].id_type = 'OBJECT'
                newVar.targets[0].id = ob_name
                newVar.type = 'TRANSFORMS'
                newVar.targets[0].transform_type = property    
                driven.driver.expression = "-var"
            
            return None

        nodes = lamp_data.node_tree.nodes


        #Add driver
        driver1 = nodes[ramp1.name].color_ramp.elements[1].driver_add('position')

        #Define property for driver (string)
        property1 = 'node_tree.nodes["Group"].inputs[3].default_value'
        		
        #Add driver variables and links
        add_driver_variable(driver1, 'LAMP', property1)

        #Change driver expression
        driver1.driver.expression = '1-var'


        #ramp2
        driver2 = nodes[ramp2.name].color_ramp.elements[1].driver_add('position')
        property2 = 'node_tree.nodes["Group"].inputs[4].default_value'
        add_driver_variable(driver2, 'LAMP', property2)
        driver2.driver.expression = '1-var'

        #ramp3
        driver3 = nodes[ramp3.name].color_ramp.elements[1].driver_add('position')
        property3 = 'node_tree.nodes["Group"].inputs[5].default_value'
        add_driver_variable(driver3, 'LAMP', property3)
        driver3.driver.expression = '1-var'

        #ramp4
        driver4 = nodes[ramp4.name].color_ramp.elements[1].driver_add('position')
        property4 = 'node_tree.nodes["Group"].inputs[6].default_value'
        add_driver_variable(driver4, 'LAMP', property4)
        driver4.driver.expression = '1-var'

        #emission1
        driver5 = nodes[emission1.name].inputs[1].driver_add('default_value')
        property5 = 'node_tree.nodes["Group"].inputs[2].default_value'
        add_driver_variable(driver5, 'LAMP', property5)

        #Light color RED
        driver6 = nodes[mix_rgb.name].inputs['Color2'].driver_add('default_value', 0)
        property6 = 'node_tree.nodes["Group"].inputs[1].default_value[0]'
        add_driver_variable(driver6, 'LAMP', property6)

        #Light color GREEN
        driver7 = nodes[mix_rgb.name].inputs['Color2'].driver_add('default_value', 1)
        property7 = 'node_tree.nodes["Group"].inputs[1].default_value[1]'
        add_driver_variable(driver7, 'LAMP', property7)

        #Light color BLUE
        driver8 = nodes[mix_rgb.name].inputs['Color2'].driver_add('default_value', 2)
        property8 = 'node_tree.nodes["Group"].inputs[1].default_value[2]'
        add_driver_variable(driver8, 'LAMP', property8)

        #Lamp = lamp_object

        driver9 = nodes[mapping4.name].driver_add('rotation', 0)
        property9 = 'ROT_X'
        add_driver_variable(driver9, lamp_object, property9)


        driver10 = nodes[mapping5.name].driver_add('rotation', 1)
        property10 = 'ROT_Y'
        add_driver_variable(driver10, lamp_object, property10)

        driver11 = nodes[mapping6.name].driver_add('rotation', 2)
        property11 = 'ROT_Z'
        add_driver_variable(driver11, lamp_object, property11)
        
        

        return{'FINISHED'}
 
 
def menu_item(self, context):
       self.layout.operator(OBJECT_OT_addBarndoorLight.bl_idname, text="Barndoors", icon="LAMP_SPOT")
 
def register():
       bpy.utils.register_module(__name__)
       bpy.types.INFO_MT_lamp_add.append(menu_item)
 
def unregister():
       bpy.utils.unregister_module(__name__)
       bpy.types.INFO_MT_lamp_add.remove(menu_item)
 
if __name__ == "__main__":
       register()
