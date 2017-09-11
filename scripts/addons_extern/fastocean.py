# -*- coding: utf-8 -*-

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Fast Ocean",
    "author": "Laurent Laget",
    "version": (0, 9),
    "blender": (2, 78, 0),
    "location": "Add > Mesh",
    "description": "Create a dynamic ocean and turn any object easily into a collider",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy

def main(context):
    for ob in context.scene.objects:
        print(ob)

#classe fastocean
class fastocean(bpy.types.Operator):
    """description"""
    bl_idname = "object.fastocean"
    bl_label = "fastocean"
    bl_options = {'REGISTER', 'UNDO'}
   
    def invoke(self, context, event):
        
        #Set cycles
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.volume_bounces = 2
        
        #ground creation
        bpy.ops.mesh.primitive_plane_add(radius=30, view_align=False, enter_editmode=False, location=(0, 0, -25), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.context.object.name = "Ground"
        bpy.ops.transform.resize(value=(2, 2, 2), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.apply.transformall()

        #creation water plane
        bpy.ops.mesh.primitive_plane_add()
        
        #name and creation modifier ocean
        bpy.context.object.name = "Ocean"
        bpy.ops.object.modifier_add(type='OCEAN')
        
        #setup modifier ocean
        bpy.context.object.modifiers["Ocean"].repeat_x = 1
        bpy.context.object.modifiers["Ocean"].repeat_y = 1
        bpy.context.object.modifiers["Ocean"].resolution = 12
        bpy.context.object.modifiers["Ocean"].wave_scale = 2

        bpy.context.object.modifiers["Ocean"].use_normals = True
        bpy.context.object.modifiers["Ocean"].use_foam = True
        bpy.context.object.modifiers["Ocean"].foam_layer_name = "foam_layer"

        obj = bpy.context.active_object
        
        #creation material
        mat_name = "M_ocean"
        materials = bpy.data.materials
        mat = materials.get(mat_name) or materials.new(mat_name) 
        
        if mat is None:
            mat = bpy.data.materials.new(name="M_ocean")

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
        
        ###creation shader###
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        mat = materials.get(mat_name) or materials.new(mat_name) 

        for node in nodes:
            nodes.remove(node)
         
        #node blue water
        water_node = nodes.new('ShaderNodeBsdfGlass')
        water_node.location = (80,50)
        water_node.distribution=('MULTI_GGX')
        water_node.inputs[0].default_value = (0.11,0.44,0.8,1)
        water_node.inputs[2].default_value = (1.330)
        water_node.label = ('Water Shader - Glass BSDF')
        
        ### nodes for foam, attribute and noise
        
        #attribute node for wet map
        wet_node = nodes.new('ShaderNodeAttribute')
        wet_node.location = (-780,790)
        wet_node.attribute_name = ('dp_wetmap')
        wet_node.label = ('Wet map attribute')
        
        #attribute node 2 for wet map
        wet_node2 = nodes.new('ShaderNodeAttribute')
        wet_node2.location = (-780,920)
        wet_node2.attribute_name = ('dp_wetmap')
        wet_node2.label =('Wet map attribute 2')
        
        #add texture coordinate
        ocean_texcoord_node = nodes.new('ShaderNodeTexCoord')
        ocean_texcoord_node.location = (-780,620)
        
        #mixrgb add node
        mixrgb_add_node = nodes.new('ShaderNodeMixRGB')
        mixrgb_add_node.location = (-600,920)
        mixrgb_add_node.use_clamp = True
        mixrgb_add_node.blend_type = ('ADD')
        
        #texture noise for first vector object
        noisevec1_node = nodes.new('ShaderNodeTexNoise')
        noisevec1_node.location = (-600,730)
        noisevec1_node.inputs[1].default_value = (10)
        noisevec1_node.inputs[2].default_value = (5)
        
        #texture noise for second vector object
        noisevec2_node = nodes.new('ShaderNodeTexNoise')
        noisevec2_node.location = (-600,550)
        noisevec2_node.inputs[1].default_value = (2)
        noisevec2_node.inputs[2].default_value = (5)
        noisevec2_node.inputs[3].default_value = (1)
        
        #mixrgb substract node
        mixrgb_substract_node = nodes.new('ShaderNodeMixRGB')
        mixrgb_substract_node.location = (-180,920)
        mixrgb_substract_node.use_clamp = True
        mixrgb_substract_node.blend_type = ('SUBTRACT')
        
        #mixrgb substract node 2
        mixrgb_substract2_node = nodes.new('ShaderNodeMixRGB')
        mixrgb_substract2_node.location = (80,920)
        mixrgb_substract2_node.use_clamp = True
        mixrgb_substract2_node.blend_type = ('SUBTRACT')
        mixrgb_substract2_node.label = ('Subtract 2')
        
        #multiply node for displacement
        multiply_displace_node = nodes.new('ShaderNodeMath')
        multiply_displace_node.operation = ('MULTIPLY')
        multiply_displace_node.inputs[0].default_value = (2)
        multiply_displace_node.location = (250,920)
        
        #wet shader with attributes
        wetshader_node = nodes.new(type='ShaderNodeBsdfDiffuse')
        wetshader_node.location = (250,700)
        wetshader_node.label = ('Wet Shader')
        
        #Color ramp for noise texture for attribute section
        gradient_noise_node = nodes.new(type='ShaderNodeValToRGB')
        gradient_noise_node.location = (-180,700)
        
        #Color ramp 2 for noise texture for attribute section
        gradient_noise_node2 = nodes.new(type='ShaderNodeValToRGB')
        gradient_noise_node2.location = (-440,750)
         
        #foam attribute for both shaders
        foam_node = nodes.new('ShaderNodeAttribute')
        foam_node.location = (-350,300)
        foam_node.attribute_name = ('foam_layer')
        foam_node.label = ('Foam Attribute')
        
        #diffuse shader, half part of foam
        diffuse_foam_node = nodes.new(type='ShaderNodeBsdfDiffuse')
        diffuse_foam_node.location = (-180,360)
        
        #glossy shader, half part of foam
        glossy_foam_node = nodes.new(type='ShaderNodeBsdfGlossy')
        glossy_foam_node.location = (-180,220)

        #mix gloss and diffuse shader for foam node
        mix_foam_node = nodes.new('ShaderNodeMixShader')
        mix_foam_node.location = (0,310)
        mix_foam_node.label = ('Mix Foam nodes')
        
        #mix attributes and foam shader
        mix_attribute_node = nodes.new('ShaderNodeMixShader')
        mix_attribute_node.location = (180,310)
        mix_attribute_node.label =('Mix attributes foam')
        
        
        ### nodes for water, bump and volume
          
        #texture noise for bump
        noise_node = nodes.new('ShaderNodeTexNoise')
        noise_node.location = (-700,50)
        
        #gradient water
        gradient_water_node = nodes.new(type='ShaderNodeValToRGB')
        gradient_water_node.location = (-530,50)
        gradient_water_node.color_ramp.elements[0].color = (1, 1, 1, 1)
        gradient_water_node.color_ramp.elements[1].color = (0, 0, 0, 1)
        
        #vector bump node
        bump_water_node = nodes.new('ShaderNodeBump')
        bump_water_node.location = (-250,50)
        
        #mix shader
        mix_node = nodes.new('ShaderNodeMixShader')
        mix_node.location = (350,150)
        mix_node.label = ('Mix glass with attributes')
                   
        #shader volume scatter
        volume_node = nodes.new('ShaderNodeVolumeScatter')
        volume_node.location = (80,-150)
        volume_node.inputs[0].default_value = (0.0863 , 0.3681 , 0.2131,1)
        volume_node.inputs[1].default_value = (0.29)
        
        #shader volume absorption
        absorption_node = nodes.new('ShaderNodeVolumeAbsorption')
        absorption_node.location = (80,-300)
        absorption_node.inputs[0].default_value = (0.115 , 0.5681 , 0.1944,1)
        absorption_node.inputs[1].default_value = (0.400)
        
        #mix volume shader
        volume_mix_node = nodes.new('ShaderNodeMixShader')
        volume_mix_node.location = (250,-200)
        volume_mix_node.label = ('mix volumes')
        
        #node output
        node_output = nodes.new(type='ShaderNodeOutputMaterial')   
        node_output.location = 600,100
        
        ###creation of links###
        
        ### Links for water ###
        
        #link blue glass to mix
        mat.node_tree.links.new(water_node.outputs['BSDF'], mix_node.inputs[2])
        
        #link noise to water gradient
        mat.node_tree.links.new(noise_node.outputs[0] , gradient_water_node.inputs[0])
        
        #link water gradient to vector bump
        mat.node_tree.links.new(gradient_water_node.outputs[0] , bump_water_node.inputs[2])
        
        #link vector bump to blue gloss water shader
        mat.node_tree.links.new(bump_water_node.outputs[0] , water_node.inputs[3])
        
        #link volume node to volmix
        mat.node_tree.links.new(volume_node.outputs[0] , volume_mix_node.inputs[1])
        
        #link absorption node to volmix
        mat.node_tree.links.new(absorption_node.outputs[0] , volume_mix_node.inputs[2])
        
        #link volmix to output volume
        mat.node_tree.links.new(volume_mix_node.outputs[0] , node_output.inputs['Volume'])
        
        #link mix to output
        mat.node_tree.links.new(mix_node.outputs[0], node_output.inputs['Surface'])
        
        ### links for attributes and foam ###
        
        #link wet paint attribute to add node
        mat.node_tree.links.new(wet_node2.outputs[0], mixrgb_add_node.inputs[1])
        
        #link foam paint attribute to add node
        mat.node_tree.links.new(wet_node.outputs[0], mixrgb_add_node.inputs[2])
        
        #link texture coordinate to noise vec1
        mat.node_tree.links.new(ocean_texcoord_node.outputs['Object'], noisevec1_node.inputs[0])

        #link texture coordinate to noise vec2
        mat.node_tree.links.new(ocean_texcoord_node.outputs['Object'], noisevec2_node.inputs[0])
        
        #link add to subtract1 
        mat.node_tree.links.new(mixrgb_add_node.outputs[0], mixrgb_substract_node.inputs[1])
        
        #link noisevec1 to gradient_noise_node2
        mat.node_tree.links.new(noisevec1_node.outputs[0], gradient_noise_node2.inputs[0])
        
        #link noisevec2 to gradient_noise_node 
        mat.node_tree.links.new(noisevec2_node.outputs[0], gradient_noise_node.inputs[0])
        
        #link subtract1 to subtract2
        mat.node_tree.links.new(mixrgb_substract_node.outputs[0], mixrgb_substract2_node.inputs[1])
        
        #link gradient_noise_node to subtract2
        mat.node_tree.links.new(gradient_noise_node.outputs[0], mixrgb_substract2_node.inputs[2])
        
        #link gradient_noise_node2  to subtract1
        mat.node_tree.links.new(gradient_noise_node2.outputs[0], mixrgb_substract_node.inputs[2])
        
        
        #link subtract2 to wet shader
        mat.node_tree.links.new(mixrgb_substract2_node.outputs[0], wetshader_node.inputs[0])
        
        #link foam_node to diffuse and glossy foam nodes
        mat.node_tree.links.new(foam_node.outputs[0], diffuse_foam_node.inputs[0])
        mat.node_tree.links.new(foam_node.outputs[0], glossy_foam_node.inputs[0])
        
        
        #link diffuse and glossy foam nodes to mix_foam_node
        mat.node_tree.links.new(diffuse_foam_node.outputs[0], mix_foam_node.inputs[1])
        mat.node_tree.links.new(glossy_foam_node.outputs[0], mix_foam_node.inputs[2])
        
        
        #link wet shader to attribute mix
        mat.node_tree.links.new(wetshader_node.outputs['BSDF'], mix_attribute_node.inputs[1])

        #link mix_foam_node to mix_attribute_node
        mat.node_tree.links.new(mix_foam_node.outputs[0], mix_attribute_node.inputs[2])
        
        #link mix_attribute_node to mix glass with attributes
        mat.node_tree.links.new(mix_attribute_node.outputs[0], mix_node.inputs[0])
        mat.node_tree.links.new(mix_attribute_node.outputs[0], mix_node.inputs[1])
        
        #link substract2 to multiply displacement
        mat.node_tree.links.new(mixrgb_substract2_node.outputs[0], multiply_displace_node.inputs[1])
        
        #link multiply displacement to displacement output
        mat.node_tree.links.new(multiply_displace_node.outputs[0], node_output.inputs['Displacement'])
        
        
        ###apply dynamic paint and setup the ocean as a canvas###
        bpy.ops.object.modifier_add(type='DYNAMIC_PAINT')
        bpy.ops.dpaint.type_toggle(type='CANVAS')
        bpy.context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["Surface"].preview_id = 'WETMAP'
        bpy.context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["Surface"].use_dissolve = True
        bpy.ops.dpaint.output_toggle(output='A')
        bpy.ops.dpaint.output_toggle(output='B')
        bpy.context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["Surface"].use_antialiasing = True
        
        ###apply a second layer of dynamic paint with a wave effect###
        bpy.ops.dpaint.surface_slot_add()
        bpy.context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["Surface.001"].name = "onde"
        bpy.context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["onde"].surface_type = 'WAVE'
        bpy.context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["onde"].use_antialiasing = True
        bpy.context.object.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["onde"].use_wave_open_border = True

        return {'FINISHED'}
    
#classe collider_ocean
class collider_ocean(bpy.types.Operator):
    """description"""
    bl_idname = "object.collider_ocean"
    bl_label = "collider_ocean"
    bl_options = {'REGISTER', 'UNDO'}
   
    def invoke(self, context, event):
        
        #apply dynamic paint, and setup the object as a brush
        bpy.ops.object.modifier_add(type='DYNAMIC_PAINT')
        bpy.context.object.modifiers["Dynamic Paint"].ui_type = 'BRUSH'
        bpy.ops.dpaint.type_toggle(type='BRUSH')
        bpy.context.object.modifiers["Dynamic Paint"].brush_settings.paint_source = 'VOLUME_DISTANCE'
        bpy.context.object.modifiers["Dynamic Paint"].brush_settings.paint_distance = 4
        bpy.context.object.modifiers["Dynamic Paint"].brush_settings.wave_factor = 2

        return {'FINISHED'}

def menu_item(self, context):
       self.layout.operator(fastocean.bl_idname, text="fast ocean", icon="PLUGIN")
       self.layout.operator(collider_ocean.bl_idname, text="Make object collide with ocean", icon="PLUGIN")
       
       
def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_item)

    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_item)

if __name__ == "__main__":
    register()
