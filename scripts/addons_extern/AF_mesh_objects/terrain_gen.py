bl_info = {
    "name": "Terrain Generator",
    "author": "Nellie Robinson",
    "version": (0, 1),
    "blender": (2, 67, 0),
    "location": "View3D > Add > Mesh",
    "description": "Adds Terrain",
    "category": "Add Mesh"}

import bpy
import bmesh
from bpy.props import IntProperty, FloatProperty, BoolProperty
from random import randint, uniform
from mathutils import Vector


class TerrainGenerator(bpy.types.Operator):
    bl_idname = "mesh.primitive_terrain_add"
    bl_label = "Generate Terrain"
    bl_options = {'REGISTER', 'UNDO'}

    # updates mesh
    auto_update = BoolProperty(
        name="update",
        default=True,
    )

    # number of iterations to perform
    n = IntProperty(
        name="iterations",
        default=5,
        min=0,
        max=9,
    )

    # terrain roughness
    roughness = FloatProperty(
        name="roughness",
        default=30,
        precision=0,
        min=0.0,
        max=200.0,
    )

    size = FloatProperty(
        name="size",
        default=30,
        precision=0,
        min=1.0,
        max=100.0
    )

    corner = FloatProperty(
        name="corner",
        default=0,
        precision=0,
        min=-20.0,
        max=20.0
    )

    triangulate = BoolProperty(
        name="triangulate",
        default=True
    )

    corner0 = corner + tuple()
    corner1 = corner + tuple()
    corner2 = corner + tuple()
    corner3 = corner + tuple()

    # initializes variables and creates grid
    def start_terrain(self):
        self.dim = int(pow(2, self.n)) + 1
        self.sideLength = self.dim - 1
        self.vertices = [0] * (self.dim * self.dim)
        bpy.ops.mesh.primitive_grid_add(
            x_subdivisions=self.dim,
            y_subdivisions=self.dim,
            enter_editmode=True,
            radius=self.size,
            location=(0, 0, 0))
        mesh = bpy.context.edit_object.data
        self.bm = bmesh.from_edit_mesh(mesh)

    # calculates noise
    def calcError(self):
        return uniform(-self.rough, self.rough)

    # plots single point
    def plot(self, x, y, z):
        index = y * self.dim + x
        self.bm.verts.ensure_lookup_table()
        self.bm.verts[index].co += Vector((0, 0, z))

    # sets altitude of single point
    def setZ(self, x, y, z):
        self.vertices[int(y * self.dim + x)] = float(z)

    def in_range(self, n):
        return n >= 0 and n < self.dim

    # gets altitude of single point
    def getZ(self, x, y):
        if self.in_range(x) and self.in_range(y):
            return self.vertices[y * self.dim + x]
        else:
            raise IndexError("Point out of bounds.", x, y)

    # plots entire array
    def plotArray(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.plot(i, j, self.getZ(i, j))
        if self.triangulate:
            bpy.ops.mesh.quads_convert_to_tris()

    # calculates points' altitudes using diamond-square algorithm
    def iterate(self):
        side = self.sideLength
        while side >= 2:
            half = int(side / 2)
            # square:
            for x in range(0, self.sideLength, side):
                for y in range(0, self.sideLength, side):
                    newZ = (self.getZ(x, y) + self.getZ(x + side, y) +
                            self.getZ(x, y + side) + self.getZ(x + side, y + side)) / 4
                    self.setZ(x + half, y + half, newZ + self.calcError())
            # diamond:
            for x in range(0, self.dim, half):
                for y in range(int((x + half) % side), self.dim, side):
                    newZ = 0.0
                    on_edge = False
                    for (i, j) in [(x, y - half), (x + half, y), (x, y + half), (x - half, y)]:
                        try:
                            newZ += self.getZ(i, j)
                        except IndexError:
                            if not on_edge:
                                on_edge = True
                            else:
                                raise ArithmeticError("Point cannot be on two edges.")
                    newZ /= 3 if on_edge else 4
                    self.setZ(x, y, newZ + self.calcError())
            side //= 2
            self.rough /= 2

    # initializes four corners
    def init_corners(self):
        self.setZ(0, 0, self.corner0)
        self.setZ(0, self.sideLength, self.corner1)
        self.setZ(self.sideLength, 0, self.corner2)
        self.setZ(self.sideLength, self.sideLength, self.corner3)

    # creates terrain mesh
    def make_terrain(self):
        self.rough = self.roughness
        self.start_terrain()
        self.init_corners()
        self.iterate()
        self.plotArray()

    # executes operator
    def execute(self, context):
        if bpy.context.selected_objects == [] or self.auto_update != 0:
            self.make_terrain()
            self.auto_update = False
            return {'FINISHED'}
        else:
            return {'PASS_THROUGH'}

    # adds menu
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, 'n')
        box.prop(self, 'roughness')
        box.prop(self, 'size')
        box.prop(self, 'corner0')
        box.prop(self, 'corner1')
        box.prop(self, 'corner2')
        box.prop(self, 'corner3')
        box.prop(self, 'auto_update')
        box.prop(self, 'triangulate')

# adds operator to blender menu


def menu_func(self, context):
    self.layout.operator(TerrainGenerator.bl_idname, text="Terrain", icon='PLUGIN')

# registers the operator


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)

# unregisters the operator


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
