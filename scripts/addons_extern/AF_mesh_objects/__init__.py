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
# Contributed to by
# Pontiac, Fourmadmen, varkenvarken, tuga3d, meta-androcto, metalliandy, dreampainter, cotejrp1 #
# liero, Kayo Phoenix, sugiany, dommetysk, Phymec, Anthony D'Agostino, Pablo Vazquez, Richard Wilks #
# xyz presets by elfnor
from .add_mesh_building_objects import build
from .add_mesh_icicle_snowflake import add_mesh_icicle_gen
from .add_mesh_icicle_snowflake import add_mesh_snowflake
from .add_mesh_siding_wall import add_mesh_drystone
from .add_mesh_siding_wall import add_mesh_floor_planks
from .add_mesh_siding_wall import add_mesh_plancher
from .add_mesh_siding_wall import add_mesh_siding
from .add_bound_box import bound_box
from .add_mesh_rocks import rock_generator
from .bookGen import __init__
from .bookGen import utils
from .add_mesh_castle import __init__
from .add_mesh_castle import Castle


bl_info = {
    "name": "AF: Mesh Objects",
    "author": "Multiple Authors",
    "version": (0, 4, 9),
    "blender": (2, 7, 6),
    "location": "View3D > Add > Mesh",
    "description": "Add extra mesh object types",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Add_Extra",
    "category": "Addon Factory",
}

if "bpy" in locals():
    import importlib
    importlib.reload(add_mesh_cave_gen)
    importlib.reload(add_mesh_lowpoly_rock)
    importlib.reload(fractalDome)
    importlib.reload(terrain_gen)
    importlib.reload(add_dual_mesh)
    importlib.reload(add_mesh_grating)
    importlib.reload(add_mesh_propeller)
    importlib.reload(add_mesh_curved_plane)
    importlib.reload(add_mesh_backdrop)
    importlib.reload(add_mesh_curlicue)
    importlib.reload(add_ArToKi_House)

else:
    from . import add_mesh_cave_gen
    from . import add_mesh_lowpoly_rock
    from . import fractalDome
    from . import terrain_gen
    from . import add_dual_mesh
    from . import add_mesh_grating
    from . import add_mesh_propeller
    from . import add_mesh_curved_plane
    from . import add_mesh_backdrop
    from . import add_mesh_curlicue
    from . import add_ArToKi_House


import bpy


class INFO_MT_mesh_ant_add1(bpy.types.Menu):
    # Define the "Ice" menu
    bl_idname = "INFO_MT_mesh_ant_add1"
    bl_label = "ANT Mod"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_terrain_add", text="Terrain")
        layout.operator("mesh.rocks", text="Rock Gen")
        layout.operator("mesh.primitive_cave_gen",
                        text="Cave Gen")
        layout.operator("mesh.lowpoly_rock_add",
                        text="Low Poly Rock")

class INFO_MT_mesh_math_add1(bpy.types.Menu):
    # Define the "Math Function" menu
    bl_idname = "INFO_MT_mesh_math_add1"
    bl_label = "Math Functions"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.operator("object.dual_mesh_operator", text="Dual Mesh")


class INFO_MT_mesh_extras_add1(bpy.types.Menu):
    # Define the "Simple Objects" menu
    bl_idname = "INFO_MT_mesh_extras_add1"
    bl_label = "More Extras"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.curved_plane",
                        text="Curved Plane", icon="SMOOTHCURVE")
        layout.operator("mesh.fractal_dome",
                        text="Fractal Dome")
        layout.operator("mesh.backdrop",
                        text="Backdrop")
        layout.operator("mesh.curlicue",
                        text="Curlicue")
        layout.operator("mesh.propeller_add", text="Propeller", icon="SCRIPTWIN")

class INFO_MT_mesh_torus_add1(bpy.types.Menu):
    # Define the "Simple Objects" menu
    bl_idname = "INFO_MT_mesh_torus_add1"
    bl_label = "Torus Objects"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_twisted_torus_add",
                        text="Twisted Torus")
        layout.operator("mesh.primitive_supertoroid_add",
                        text="Supertoroid")
        layout.operator("mesh.primitive_torusknot_add",
                        text="Torus Knot")


class INFO_MT_mesh_icy_add1(bpy.types.Menu):
    # Define the "Ice" menu
    bl_idname = "INFO_MT_mesh_ice_add1"
    bl_label = "Ice & Snow"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.icicle_gen",
                        text="Icicle Generator")
        layout.operator("mesh.snowflake",
                        text="Snowflake")


class INFO_MT_mesh_floorwall_add1(bpy.types.Menu):
    # Define the "Ice" menu
    bl_idname = "INFO_MT_mesh_floorwall_add1"
    bl_label = "Floors & Walls"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.primitive_add_siding",
                        text="Siding")
        layout.operator("mesh.drystone",
                        text="Drystone")
        layout.operator("mesh.floor_boards_add",
                        text="Floor Boards")
        layout.operator("mesh.ajout_primitive",
                        text="Plancher")


class INFO_MT_mesh_boundbox_add1(bpy.types.Menu):
    # Define the "Bound Box" menu
    bl_idname = "INFO_MT_mesh_boundbox_add1"
    bl_label = "Bound Box Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.boundbox_add",
                        text="Bound Box Add")
        layout.operator("object.min_bounds",
                        text="Minimum Bounds")

class INFO_MT_mesh_building_add1(bpy.types.Menu):
    # Define the "Building" menu
    bl_idname = "INFO_MT_mesh_building_add1"
    bl_label = "Building"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("INFO_MT_mesh_floorwall_add", text="Floors & Walls", icon="UV_ISLANDSEL")
        layout.operator("mesh.add_say3d_balcony",
                        text="Balcony")
        layout.operator("mesh.add_say3d_sove",
                        text="Sove")
        layout.operator("mesh.stairs",
                        text="Stair Builder")
        layout.operator("mesh.primitive_add_grating",
                        text="Grating")
        layout.operator("object.book_gen",
                        text="Book Gen")
        layout.operator("mesh.add_castle",
                        text="Castle")
        layout.operator("mesh.primitive_house_add", text="ArToKi House", icon="MOD_LATTICE")

# Define "Extras" menu


def menu_ant(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    col = layout.column()
    self.layout.menu("INFO_MT_mesh_ant_add1", text="Landscape+", icon="RNDCURVE")


def menu_math(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    col = layout.column()
    self.layout.menu("INFO_MT_mesh_math_add1", text="Math Extras", icon="PACKAGE")

def menu_building(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    col = layout.column()
    self.layout.menu("INFO_MT_mesh_building_add1", text="Building", icon="UV_ISLANDSEL")

def menu_extras(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    col = layout.column()
    self.layout.menu("INFO_MT_mesh_extras_add1", text="More Extras", icon="MESH_DATA")
    self.layout.menu("INFO_MT_mesh_ice_add", text="Ice & Snow", icon="FREEZE")
    self.layout.menu("INFO_MT_mesh_boundbox_add1", text="Bound Box", icon="LATTICE_DATA")
# Addons Preferences


class MeshObjectPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__

    bpy.types.Scene.Enable_Tab_01 = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.Enable_Tab_02 = bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "Enable_Tab_01", text="info", icon="INFO")
        if context.scene.Enable_Tab_01:
            row = layout.row()
            layout.label(text="----Add Extra Extra Mesh Objects----")
            layout.label(text="Merges most Mesh Object Addons into One")
            layout.label(text="New sub menu's & organization")

        layout.prop(context.scene, "Enable_Tab_02", text="Mesh Objects", icon="INFO")
        if context.scene.Enable_Tab_02:
            row = layout.row()
            layout.label(text="Add Bound Box: Adds bounding box with options")
            layout.label(text="Erode: Add erosion To ANT Landscape mesh")
            layout.label(text="Terrain: create large Terrain mesh")
            layout.label(text="Rock Gen: Create displacement Rocks")
            layout.label(text="Cave Gen: Create Caves with lights")
            layout.label(text="Low Poly Rock: Create Low Poly Rock Shapes")
            layout.label(text="Duel Mesh: Create duel copy of mesh")
            layout.label(text="Propeller: Add Aerodynamic propeller")
            layout.label(text="Floors & Walls: Siding, Drystone, Floorboards, Plancher")
            layout.label(text="Balcony, Sove")
            layout.label(text="Wall Factory: Add Castle Wall")
            layout.label(text="Stair Builder: Add Stairs")
            layout.label(text="Grating: Add mesh Grating")
            layout.label(text="Book Gen: Create rows of books")
            layout.label(text="Castle: Create Castles (wip)")
            layout.label(text="Icicle & Snowflake")
            layout.label(text="Simple Star, Step Pyramid, Honeycomb")
            layout.label(text="Fractal Dome")
            layout.label(text="Basket Arch")


def register():
    bpy.utils.register_module(__name__)

    # Add "AF:" menu to the "Add Mesh" menu
    bpy.types.INFO_MT_mesh_add.append(menu_ant)
    try:
        bpy.types.INFO_MT_mesh_math_add.prepend(menu_math)
        bpy.types.INFO_MT_mesh_extras_add.prepend(menu_extras)
    except:
        pass

    bpy.types.INFO_MT_mesh_add.append(menu_building)


def unregister():
    # Remove "AF:" menu from the "Add Mesh" menu.
    bpy.types.INFO_MT_mesh_add.remove(menu_ant)
    try:
        bpy.types.INFO_MT_mesh_math_add.remove(menu_math)
        bpy.types.INFO_MT_mesh_extras_add.remove(menu_extras)
    except:
        pass
    bpy.types.INFO_MT_mesh_add.remove(menu_building)

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
