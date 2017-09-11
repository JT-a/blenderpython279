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
    'name': "Link Sky To Sun",
    'author': "Eugenio Pignataro Oscurart, Greg Zaal",
    'version': (1, 0),
    'blender': (2, 70, 0),
    'location': "World settings, when a Sky Texture is used.",
    'description': "Drive the Sky Texture's direction using the rotation of a Sun Lamp",
    'warning': "",
    'wiki_url': "",
    'tracker_url': "",
    'category': "Scene",
}

import bpy
from random import random

class LinkSkyToSun(bpy.types.Operator):
    bl_idname = "world.link_sky_to_sun"
    bl_label = "Link Sky To Sun Lamp"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.scene.SunObject:
            return False
        world = context.scene.world
        tree = world.node_tree
        if tree and world.use_nodes:
            if [n for n in tree.nodes if n.type == "TEX_SKY"]:
                return True
        return False

    def execute(self, context):

        tree = context.scene.world.node_tree
        if tree.nodes.active.type  == "TEX_SKY":
            node = tree.nodes.active
        else:
            node = [n for n in tree.nodes if n.type == "TEX_SKY"][0]
        lampob = bpy.data.objects[context.scene.SunObject]

        valid = True
        if tree.animation_data:
            if tree.animation_data.action:
                for fc in tree.animation_data.action.fcurves:
                    if fc.data_path == ("nodes[\""+node.name+"\"].sun_direction"):
                        valid = False
                        self.report({'ERROR'}, "Sun Direction is animated")
            elif tree.animation_data.drivers:
                for dr in tree.animation_data.drivers:
                    if dr.data_path == ("nodes[\""+node.name+"\"].sun_direction"):
                        valid = False
                        self.report({'ERROR'}, "Sun Direction has drivers")
        if valid:
            dr = node.driver_add("sun_direction")

            nodename = ""
            for ch in node.name:
                if ch.isalpha():  # make sure node name can be used in expression
                    nodename += ch
            varname = nodename + "_" + str(int(random()*89998 + 10000))  # create unique variable name for each node

            dr[0].driver.expression = varname
            var = dr[0].driver.variables.new()
            var.name = varname
            var.type = 'SINGLE_PROP'
            var.targets[0].id = lampob
            var.targets[0].data_path = 'matrix_world[2][0]'
            # Y
            dr[1].driver.expression = varname
            var = dr[1].driver.variables.new()
            var.name = varname
            var.type = 'SINGLE_PROP'
            var.targets[0].id = lampob
            var.targets[0].data_path = 'matrix_world[2][1]'    
            # Y
            dr[2].driver.expression = varname
            var = dr[2].driver.variables.new()
            var.name = varname
            var.type = 'SINGLE_PROP'
            var.targets[0].id = lampob
            var.targets[0].data_path = 'matrix_world[2][2]'              

            return {'FINISHED'}
        else:
            return {'CANCELLED'}


def sun_sky_menu_func(self, context):
    world = context.scene.world
    tree = world.node_tree
    if tree and world.use_nodes:
        col = self.layout.column(align = True)
        row = col.row(align = True)
        row.prop_search(context.scene, "SunObject", bpy.data, "objects")
        row.operator(LinkSkyToSun.bl_idname, icon="LAMP_SUN")



def register():
    bpy.types.Scene.SunObject = bpy.props.StringProperty(
        name="Sun Obj",
        default="",
        description="The lamp object to use to drive the Sky rotation")

    bpy.utils.register_module(__name__)

    bpy.types.CyclesWorld_PT_surface.append(sun_sky_menu_func)


def unregister():
    del bpy.types.Scene.SunObject

    bpy.utils.unregister_module(__name__)

    bpy.types.CyclesWorld_PT_surface.remove(sun_sky_menu_func)

if __name__ == "__main__":
    register()
