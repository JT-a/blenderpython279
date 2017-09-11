# ArToKi-EPB.py (c) 2012 Thierry Maes (tmaes)
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****


bl_info = {
    "name": "ArToKi-House",
    "author": "Thierry Maes (tmaes)",
    "version": (0, 0, 7),
    "blender": (2, 67, 0),
    "api": 56533,
    "location": "Properties > Object > ArToKi House",
    "description": "Create houses based on simple 2 point lines.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

"""
This addon is made for mass planification.
It creates simple house primitives
"""


import bpy


def add_house(length, width):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    vertices = [0.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                1.0, -0.5, 0.0,
                0.0, -0.5, 0.0,
                1.0, 0.5, 0.0,
                0.0, 0.5, 0.0,
                ]
    edges = [0, 1,
             5, 4,
             3, 2,
             5, 0,
             3, 0,
             4, 1,
             2, 1,
             ]

    faces = [
        0, 3, 2, 1,
        0, 1, 4, 5,
    ]

#     apply size
    for i in range(0, len(vertices), 3):
        vertices[i] *= length
        vertices[i + 1] *= width

    return vertices, faces, edges

from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
)


class AddHouse(bpy.types.Operator):
    '''Add a simple house mesh'''
    bl_idname = "mesh.primitive_house_add"
    bl_label = "House"
    bl_options = {'REGISTER', 'UNDO'}

    atk_width = FloatProperty(
        name="House width",
        description="House width",
        min=0.0, max=500.0,
        default=5.0,
    )
    atk_length = FloatProperty(
        name="House length",
        description="House length",
        min=0.0, max=500.0,
        default=10.0,
    )
    atk_foundation_height = FloatProperty(
        name="Foundation thickness",
        description="Foundation Height",
        min=0.0, max=100.0,
        default=0.3,
    )
    atk_ground_floor_height = FloatProperty(
        name="Ground floor height",
        description="Ground Floor Height",
        min=0.0, max=10.0,
        default=2.5,
    )
    atk_floors_thickness = FloatProperty(
        name="Floors thickness",
        description="Floors thickness usually 0.3",
        min=0.0, max=10.0,
        default=0.3,
    )
    atk_first_floor_height = FloatProperty(
        name="First floor height",
        description="House Height",
        min=0.0, max=10.0,
        default=0.0,
    )
    atk_generic_floor_height = FloatProperty(
        name="Generic floor height",
        description="Second floor height",
        min=0.0, max=10.0,
        default=2.5,
    )
    atk_floors_number = IntProperty(
        name="Number of floors",
        description="Number of floors",
        min=0, max=300,
        default=1,
    )
    atk_last_floor_height = FloatProperty(
        name="Last floor height",
        description="Last floor height",
        min=0.0, max=10.0,
        default=0.0,
    )
    atk_cornice_thickness = FloatProperty(
        name="Cornice thickness",
        description="Last chance to tune the cornice",
        min=0.0, max=10.0,
        default=0.0,
    )
    atk_ridge_height = FloatProperty(
        name="Ridge height",
        description="Ridge height",
        min=0.0, max=100.0,
        default=3.0,
    )
    atk_walls_thickness = FloatProperty(
        name="Thickness of general exterior walls.",
        description="Thickness of general exterior walls.",
        min=0.0, max=1.0,
        default=0.35,
    )
    atk_roof_walls_height = FloatProperty(
        name="Height of general exterior walls.",
        description="Height of general exterior walls.",
        min=0.0, max=1.0,
        default=0.5,
    )
    atk_road_parallelism = BoolProperty(
        name="Parallel to the road.",
        description="Is the house parallel to the road.",
        default=True,
    )
    atk_create_interior = BoolProperty(
        name="Create interiors.",
        description="Create default ceillings.",
        default=False,
    )


#     generic transform props
    view_align = BoolProperty(
        name="Align to View",
        default=False,
    )
    location = FloatVectorProperty(
        name="Location",
        subtype='TRANSLATION',
    )
    rotation = FloatVectorProperty(
        name="Rotation",
        subtype='EULER',
    )
    layers = BoolVectorProperty(
        name="Layers",
        size=20,
        subtype='LAYER',
        options={'HIDDEN', 'SKIP_SAVE'},
    )

    def execute(self, context):
        #     creating the basis shape...
        verts_loc, faces, edges = add_house(self.atk_length, self.atk_width)

        mesh = bpy.data.meshes.new("House")

        mesh.vertices.add(len(verts_loc) // 3)
        mesh.edges.add(len(edges) // 2)
        mesh.tessfaces.add(len(faces) // 4)

        mesh.vertices.foreach_set("co", verts_loc)
        mesh.edges.foreach_set("vertices", edges)
        mesh.tessfaces.foreach_set("vertices_raw", faces)
        mesh.update()
#    the mesh is created let's transform it into house...


#    add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)


#    prepare selections and variables before to start geometry
        obj = bpy.context.active_object
        scn = bpy.context.scene
        # base_faces=[]
        # roof_faces=[]
        ridge_vertices = []
        try:
            scn['atk_house_id']
        except KeyError:
            scn['atk_house_id'] = 0
        else:
            scn['atk_house_id'] = scn['atk_house_id'] + 1


#    add custom properties
        obj['atk_Id'] = scn['atk_house_id']
        obj['atk_Width'] = self.atk_width
        obj['atk_Length'] = self.atk_length
        obj['atk_Foundation_Height'] = self.atk_foundation_height
        obj['atk_Ground_Floor_Height'] = self.atk_ground_floor_height
        obj['atk_Floors_Thickness'] = self.atk_floors_thickness
        obj['atk_First_Floor_Height'] = self.atk_first_floor_height
        obj['atk_Generic_Floor_Height'] = self.atk_generic_floor_height
        obj['atk_Floors_Number'] = self.atk_floors_number
        obj['atk_Last_Floor_Height'] = self.atk_last_floor_height
        obj['atk_Cornice_Thickness'] = self.atk_cornice_thickness
        obj['atk_Ridge_Height'] = self.atk_ridge_height
        obj['atk_Walls_Thickness'] = self.atk_walls_thickness
        obj['atk_Roof_Walls_Height'] = self.atk_roof_walls_height
        obj['atk_Road_Parallelism '] = self.atk_road_parallelism
        obj['atk_House_Location'] = self.location
        obj['atk_House_Rotation'] = self.rotation
        obj['atk_Create_Interior'] = self.atk_create_interior

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.context.tool_settings.mesh_select_mode = [False, False, True]


#
#
#   1 foundation
        if self.atk_foundation_height > 0:

            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_foundation_height)})

#   2 walls ground floor

        if self.atk_ground_floor_height > 0:

            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_ground_floor_height)})

#   3 walls for eventual additionnal floors
#       1st floor

        if self.atk_first_floor_height > 0:

            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_floors_thickness)})
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_first_floor_height)})


#       more floors
        if self.atk_generic_floor_height > 0:

            for i in range(self.atk_floors_number):
                bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_floors_thickness)})
                bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_generic_floor_height)})

#   4 walls for last floor
        if self.atk_last_floor_height > 0:

            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_floors_thickness)})
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_last_floor_height)})

#   5 cornice
        if self.atk_cornice_thickness > 0:

            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_cornice_thickness)})


#   6 roof, flat if ridge height=0
#       1 not flat roof

        if self.atk_ridge_height > 0:
            # print('prout')
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0)})


#
            bpy.context.tool_settings.mesh_select_mode = [True, False, False]
            bpy.ops.object.mode_set(mode='OBJECT')
            ridge_verts = []
            for i in obj.data.vertices:
                #                print(i.index,i.co[1],i.select)
                if i.select == True:
                    if i.co[1] == 0:
                        ridge_verts.append(i.index)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            for i in ridge_verts:
                obj.data.vertices[i].select = True
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.transform.translate(value=(0, 0, self.atk_ridge_height))

#           Clean isolated vertexes
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.object.mode_set(mode='OBJECT')
            if self.atk_create_interior == True:
                bpy.context.tool_settings.mesh_select_mode = [True, False, False]

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()
                bpy.ops.object.mode_set(mode='OBJECT')

                bpy.context.active_object.modifiers.new(name='Solidify', type='SOLIDIFY')
                obj.modifiers['Solidify'].thickness = self.atk_walls_thickness
                obj.modifiers['Solidify'].offset = -1
                obj.modifiers['Solidify'].use_even_offset = True
                # bpy.ops.object.modifier_apply(modifier="Solidify")


#       2 flat roof
        else:
            #
            if self.atk_roof_walls_height > 0:
                bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, self.atk_roof_walls_height)})
##
#            bpy.ops.mesh.edge_face_add()
            if self.atk_walls_thickness > 0:
                #                bpy.ops.fi.op0_id(opp=self.atk_walls_thickness, b_=False)
                bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, use_relative_offset=False, thickness=self.atk_walls_thickness, depth=0, use_outset=False, use_select_inset=False)
            if self.atk_roof_walls_height > 0:
                bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, -self.atk_roof_walls_height)})

# The interior part of flat roof houses must be recoded
#
#            if self.atk_create_interior == True:
#                bpy.context.tool_settings.mesh_select_mode = [True, False, False]
#
#                bpy.ops.object.mode_set(mode='EDIT')
#                bpy.ops.mesh.select_all(action='SELECT')
#                bpy.ops.mesh.remove_doubles(mergedist=0.0001)
#                bpy.ops.object.mode_set(mode='OBJECT')
#
#
#                bpy.context.active_object.modifiers.new(name='Solidify', type='SOLIDIFY')
#                obj.modifiers['Solidify'].thickness=self.atk_walls_thickness
#                obj.modifiers['Solidify'].offset=-1
#                obj.modifiers['Solidify'].use_even_offset=False
#                #bpy.ops.object.modifier_apply(modifier="Solidify")
#
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.show_all_edges = True
        obj.show_wire = True
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddHouse.bl_idname, icon='DISK_DRIVE')


def register():
    bpy.utils.register_class(AddHouse)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddHouse)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
