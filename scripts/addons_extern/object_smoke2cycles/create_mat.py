# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.69.x+ Smoke2Cycles-Addon
# --------------------------------------------------------------------------
#
# Author:
# HiPhiSch
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
#

import bpy
from traceback import print_exc

class Smoke2CyclesScriptProperty(bpy.types.PropertyGroup):
    """Script custom properties for Smoke2Cycles"""
    script_id = bpy.props.IntProperty(name="Script ID", min=-1, default=-1)

class Smoke2CyclesOSLScriptProvider(object):    
    import_script_id = 1
    import_script = \
    """// Author: HiPhiSch
// version 0.4
// changes:
// v 0.4 - Flame support, EXR, embedded in addon
// v 0.3 - Bugfix: y mirror
// v 0.2 - z interpolation
// v 0.1 - first published version

#include "stdosl.h"

// Renders a specially exported smoke texture as volume texture
shader smoke_vol_texture(
    point Vector = P,
    string TextureFilenameBase="//smoke_export",
    int CurrentFrame = 1,
    int Divisions = 32,
    int EnableZInterp = 1,
    output float SmokeDensity = 0.0,
    output float FireDensity = 0.0
)
{
    // outside of [-1,1] cube?
    vector Pos = 0.5 * (Vector + vector(1.0,1.0,1.0));

    if ((Pos[0] < 0.0) || (Pos[0] > 1.0) || 
        (Pos[1] < 0.0) || (Pos[1] > 1.0) ||
        (Pos[2] < 0.0) || (Pos[2] > 1.0)) 
    {
        return;
    }

    // x and y texture influence
    float x = Pos[0] ;
    float y = (1.0 - Pos[1]) / Divisions;


    string fn = format("%s_%03d.exr", TextureFilenameBase, CurrentFrame);
    // result of texture calls goes here:    
    color smoke_fire_tex;
    if (EnableZInterp == 0)
    {
        // no interpolation
        float z = 1.0 - trunc(Pos[2] * Divisions) / Divisions;    
        y += z;
    
        // read from texture
        smoke_fire_tex = texture(fn, x, y);
    } else {
        // upper, lower interval border of z
        float zfloor = trunc(Pos[2] * Divisions) / Divisions;    
        float zceil = zfloor + 1.0 / Divisions;
        // fraction for interpolation
        float zfrac = (Pos[2] - zfloor) * Divisions;
        color smoke_fire_ceil;
        
        // read from texture
        smoke_fire_tex = texture(fn, x, y + 1.0 - zfloor);
        smoke_fire_ceil = texture(fn, x, y + 1.0 - zceil);

        // interpolate
        smoke_fire_tex = (1.0 - zfrac) * smoke_fire_tex + zfrac * smoke_fire_ceil;
    }
    
    SmokeDensity = smoke_fire_tex[0];
    FireDensity = smoke_fire_tex[1];
}
"""
    
    temperature_script = """// Author: HiPhiSch
// Maps a normalized value to a given temperature

#include "stdosl.h"

shader tempature_remap(
    float FireDensity = 0.0,
    float LowTemp = 1250.0,
    float HighTemp = 1750.0,
    output float Temp = 0.0)
{
    Temp = (HighTemp - LowTemp) * FireDensity + LowTemp;
}"""
    temperature_script_id = 1001
    scripts = {
        'IMPORT': (import_script_id, import_script, "Smoke2CyclesImpScr.osl") ,
        'TEMPERATURE': (temperature_script_id, temperature_script, "Smoke2CyclesTempRemap.osl")
        }


class NodeLayouter(object):
    """Adds nodes with simple layout"""
    def __init__(self, node_tree):
        self.__node_tree = node_tree
        self.next_x = 0.0
        self.x_margin = 80.0
        self.y_margin = 100.0
              
    def add(self, nodes, y_offset=0.0):
        """Add one or more nodes to the right of the setup"""
        if type(nodes) in (tuple, list):
            # add node
            if len(nodes) == 0:
                return []
            
            res = []
            heights = [0.0]
            current_y_offset = 0.0
            for n in nodes:
                # y-offset?
                splt = n.split("_")
                if (len(splt) == 2) and (splt[0] == "YSPACER"):
                    current_y_offset += float(splt[1])
                    continue
                
                # create node 
                r = self.__add_single(n)
                # r.update()
                res.append(r)
                heights[-1] += current_y_offset
                heights.append(r.height + self.y_margin)
                current_y_offset = 0.0
            heights[-1] += current_y_offset - self.y_margin

            if len(res) == 0:
                return []

            # distribute over y   
            top = (sum(heights) - res[0].height) // 2            
            for r, h in zip(res, heights):
                r.location[1] = top - h
                top -= h
                
            # get maximum width
            width = max([r.width for r in res])
        else:
            # add
            res = self.__add_single(nodes)
            # get width
            width = res.width

        # set x position for next call
        self.next_x += self.x_margin + width
        return res
    
    def __add_single(self, node,):
        """internal procedure which performs the insertion of the new node"""        
        res = self.__node_tree.nodes.new(node)
        res.location[0] = self.next_x
        res.location[1] = 0.0
        return res
    

class Smoke2CyclesImportMaterialGenerator(object):
    """Generate the required cycles material for smoke import"""
    
    @classmethod
    def generate_material(cls, mat_type):
        MAT_TYPES = ['FIRE', 'SMOKE', 'SMOKE_FIRE']
        if not mat_type in MAT_TYPES:
            raise KeyError('Wrong material type: %s not in %r' % (mat_type, MAT_TYPES))

        # get required osl scripts            
        osl_import = cls.find_or_create_script('IMPORT')            
        osl_temp_remap = None if mat_type == 'SMOKE' else cls.find_or_create_script('TEMPERATURE')
        
        # switch to cycles render engine for now
        re = bpy.context.scene.render.engine
        try:
            bpy.context.scene.render.engine = 'CYCLES' 
            
            # create material
            m = bpy.data.materials.new("Smoke2CyclesMaterial")
            m.use_nodes = True
            n_tr = m.node_tree
            n_tr.nodes.clear()
            
            # setup input part
            nl = NodeLayouter(n_tr)
            nodes = ["ShaderNodeTexCoord"]
            nodes.append("ShaderNodeScript")
            
            # create nodes
            input_nodes = [nl.add(n) for n in nodes]
                       
            # load osl script
            input_nodes[-1].script = osl_import
            
            # link nodes           
            n_tr.links.new(input_nodes[0].outputs["Object"], input_nodes[1].inputs["Vector"])
            
            input_nodes[1].name = "S2C_IMPORT_SCRIPT"
            input_nodes[1].label = "Smoke2Cycles - Import"
            
            # setup converter part
            nodes = [[], []]
            sm_offs = [0, 0]
            if mat_type in ('SMOKE', 'SMOKE_FIRE'):
                nodes[1].append("ShaderNodeMath")
                
                sm_offs = [len(n) for n in nodes]
                
            if mat_type in ('FIRE', 'SMOKE_FIRE'):
                nodes[0].append('YSPACER_300')
                nodes[0].append("ShaderNodeScript")

                nodes[1].append("ShaderNodeMath")
                nodes[1].append("ShaderNodeBlackbody")
            
            # create nodes    
            converter_nodes = [nl.add(n) for n in nodes]
            
            if mat_type in ('SMOKE', 'SMOKE_FIRE'):
                # set up math node
                converter_nodes[1][0].operation = 'MULTIPLY'
                converter_nodes[1][0].inputs[1].default_value = 10.0
                
                # link node
                n_tr.links.new(input_nodes[-1].outputs["SmokeDensity"], converter_nodes[1][0].inputs[0])
                
                sm_dens = converter_nodes[1][0].outputs["Value"]
                converter_nodes[1][0].label = "Smoke Density Scaler"
                
            if mat_type in ('FIRE', 'SMOKE_FIRE'):                
                # setup math node
                converter_nodes[1][0 + sm_offs[1]].operation = 'MULTIPLY'
                converter_nodes[1][0 + sm_offs[1]].inputs[1].default_value = 5.0

                # load script
                converter_nodes[0][0 + sm_offs[0]].script = osl_temp_remap
                                
                # link nodes
                n_tr.links.new(input_nodes[-1].outputs["FireDensity"], converter_nodes[0][0 + sm_offs[0]].inputs["FireDensity"])
                n_tr.links.new(input_nodes[-1].outputs["FireDensity"], converter_nodes[1][0 + sm_offs[1]].inputs[0])
                n_tr.links.new(converter_nodes[0][0 + sm_offs[0]].outputs["Temp"], converter_nodes[1][1 + sm_offs[1]].inputs["Temperature"])
                
                # name
                converter_nodes[0][0 + sm_offs[0]].name = "S2C_FIRE_TEMP"
                
                fr_dens = converter_nodes[1][0 + sm_offs[1]].outputs["Value"]
                fr_color = converter_nodes[1][1 + sm_offs[1]].outputs["Color"]
                
                converter_nodes[1][0 + sm_offs[1]].label = "Fire Density Scale"
                converter_nodes[0][0 + sm_offs[0]].label = "Smoke2Cycles - Temperature Remap"
            
            # setup shader part
            nodes = [[],[]]
            sm_offs_shd = [0,0]
            
            if mat_type in ('SMOKE', 'SMOKE_FIRE'):
                nodes[0].append("ShaderNodeVolumeAbsorption")
                nodes[0].append("ShaderNodeVolumeScatter")
                nodes[1].append("ShaderNodeAddShader")
                
                sm_offs_shd = [len(sn) for sn in nodes]
                
            if mat_type in ('FIRE', 'SMOKE_FIRE'):
                if mat_type == 'SMOKE_FIRE':
                    nodes[0].append("YSPACER_400")
                nodes[1].append("ShaderNodeEmission")
                
            # create nodes    
            shader_nodes = [nl.add(n) for n in nodes]
            
            if mat_type in ('SMOKE', 'SMOKE_FIRE'):
                # create links
                n_tr.links.new(sm_dens, shader_nodes[0][0].inputs["Density"])   
                n_tr.links.new(sm_dens, shader_nodes[0][1].inputs["Density"])  
                n_tr.links.new(shader_nodes[0][0].outputs["Volume"], shader_nodes[1][0].inputs[0])
                n_tr.links.new(shader_nodes[0][1].outputs["Volume"], shader_nodes[1][0].inputs[1])
                
                shader_nodes[0][1].inputs["Anisotropy"].default_value = 0.85
                
                sm_shader = shader_nodes[1][0].outputs["Shader"]
            
            if mat_type in ('FIRE', 'SMOKE_FIRE'):
                # create links
                n_tr.links.new(fr_dens, shader_nodes[1][0 + sm_offs_shd[1]].inputs["Strength"])   
                n_tr.links.new(fr_color, shader_nodes[1][0 + sm_offs_shd[1]].inputs["Color"])   

                fr_shader = shader_nodes[1][0 + sm_offs_shd[1]].outputs["Emission"]
                
            nodes = [[], ["ShaderNodeOutputMaterial"]]
            
            if mat_type == 'SMOKE_FIRE':
                nodes[0].append("ShaderNodeAddShader")
            
            output_nodes = [nl.add(n) for n in nodes]
            
            if mat_type == 'FIRE':
                n_tr.links.new(fr_shader, output_nodes[1][0].inputs["Volume"])
            elif mat_type == 'SMOKE':
                n_tr.links.new(sm_shader, output_nodes[1][0].inputs["Volume"])
            elif mat_type == 'SMOKE_FIRE':
                n_tr.links.new(sm_shader, output_nodes[0][0].inputs[0])
                n_tr.links.new(fr_shader, output_nodes[0][0].inputs[1])
                
                n_tr.links.new(output_nodes[0][0].outputs["Shader"], output_nodes[1][0].inputs["Volume"])
                
            
        finally:
            bpy.context.scene.render.engine = re
        
        return m    
    
    @staticmethod
    def find_or_create_script(script_type):    
        """find or create an internal text with the corresponding osl script"""
        if not script_type in Smoke2CyclesOSLScriptProvider.scripts:
            raise KeyError("script type: %s not in %r" % (script_type, list(Smoke2CyclesOSLScriptProvider.scripts)) )
        
        # if script is present provide it    
        script_id = Smoke2CyclesOSLScriptProvider.scripts[script_type][0]
        for txt in bpy.data.texts:
            if txt.smoke2cycles.script_id == script_id:
                return txt
        
        # create new
        id, scr, nm = Smoke2CyclesOSLScriptProvider.scripts[script_type]
        txt = bpy.data.texts.new(nm)
        txt.smoke2cycles.script_id = id
        txt.from_string(scr)
        return txt
        

def register():
    bpy.utils.register_class(Smoke2CyclesScriptProperty)
    
    bpy.types.Text.smoke2cycles = bpy.props.PointerProperty(type=bpy.types.Smoke2CyclesScriptProperty)
    
def unregister():
    del bpy.types.Text.smoke2cycles
    
    bpy.utils.unregister_class(bpy.types.Smoke2CyclesScriptProperty)
    
if __name__ == "__main__":
    print ("-" * 40)
    try:
        unregister()
    except:
        print ("WARNING: unregister failed")
        print_exc()    
    register()    
    
    # tests
    Smoke2CyclesImportMaterialGenerator.generate_material('SMOKE')
    Smoke2CyclesImportMaterialGenerator.generate_material('FIRE')
    Smoke2CyclesImportMaterialGenerator.generate_material('SMOKE_FIRE')
