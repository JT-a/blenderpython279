###### BEGIN GPL LICENSE BLOCK #####
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###### END GPL LICENSE BLOCK #####

# Plugin info
bl_info = {
    "name": "Fractal dome",
    "author": "Jasmin Dettelbach",
    "version": (1, 0, 0),
    "blender": (2, 6, 2),
    "location": "Add > Fractal dome",
    "description": "Generate a fratal dome model",
    'warning': '',
    "category": "Mesh"}

# Import
import bpy
import math
from bpy.props import *

######################
# GUI-Class
######################


class MESH_OT_fractal_dome(bpy.types.Operator):
    bl_idname = "mesh.fractal_dome"
    bl_label = "Add fractal dome"
    bl_options = {'REGISTER', 'UNDO'}
    # GUI Elements
    size = FloatProperty(name="Size", description="Size of the dome", min=0.1, max=100, default=1)
    recursion = IntProperty(name="Recursion", description="Recursion steps", min=0, max=5, default=0)
    octa = BoolProperty(name="Only Octagon", description="Toggle between star and octagon")
    # Execute

    def execute(self, context):
        # Main function
        ob = addDome(self.size, self.recursion, self.octa)
        return{'FINISHED'}

######################
# Main function
######################


def addDome(size, rec, octa):
    for i in range(rec + 1):
        verts, faces = generate([0, 0, 0], size, i, [], [], size, octa)
        mesh = bpy.data.meshes.new(str(i) + "level")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        print("dome" + str(i))
        obj = bpy.data.objects.new("dome" + str(i), mesh)
    bpy.context.scene.objects.link(obj)
    # Select Vertices with z < -0.1 and delete them
    bpy.context.scene.objects.active = obj
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
    for v in range(len(mesh.vertices)):
        if mesh.vertices[v].co.z < -0.1:
            mesh.vertices[v].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete()
    bpy.ops.object.editmode_toggle()
    return obj

######################
# Calculate z
######################


def height(x, y, size):
    z = (-1 / (2 * size)) * (x)**(2) - (1 / (2 * size)) * (y)**(2) + (size * 1.1)
    return z

######################
# Generate dome
######################


def generate(location, scale, level, currentVerts, currentFaces, size, bool):
    x, y, z = location
    a = x + scale * (1 / 2)**(1 / 2)
    b = x - scale * (1 / 2)**(1 / 2)
    c = y + scale * (1 / 2)**(1 / 2)
    d = y - scale * (1 / 2)**(1 / 2)
    # Recursion
    if level:
        generate([x, y, z], scale, level - 1, currentVerts, currentFaces, size, bool)
        generate([a, c, height(a, c, size)], scale / 2, level - 1, currentVerts, currentFaces, size, bool)
        generate([b, c, height(b, c, size)], scale / 2, level - 1, currentVerts, currentFaces, size, bool)
        generate([b, d, height(b, d, size)], scale / 2, level - 1, currentVerts, currentFaces, size, bool)
        generate([a, d, height(a, d, size)], scale / 2, level - 1, currentVerts, currentFaces, size, bool)
    # Calculate points and define faces
    else:
        start = len(currentVerts)
        e = x + scale * (2)**(1 / 2)
        f = x - scale * (2)**(1 / 2)
        g = x + scale * ((2)**(1 / 2) - 1)
        h = x - scale * ((2)**(1 / 2) - 1)
        i = y + scale * (2)**(1 / 2)
        j = y - scale * (2)**(1 / 2)
        k = y + scale * ((2)**(1 / 2) - 1)
        l = y - scale * ((2)**(1 / 2) - 1)
        offset = 0.025 * scale
        off = 0.036 * scale
        off2 = offset * 2
    ##########
    # Edges
    ##########
        # Octagon
        currentVerts += [(x + scale + off2, y, height(x + scale + off2, y, size) + offset),
                         (x + scale + off2, y, height(x + scale + off2, y, size) - offset),
                         (x + scale - off2, y, height(x + scale - off2, y, size) + offset),
                         (x + scale - off2, y, height(x + scale - off2, y, size) - offset),\
                         # 2
                         (a + off, c + off, height(a + off, c + off, size) + offset),\
                         (a + off, c + off, height(a + off, c + off, size) - offset),\
                         (a - off, c - off, height(a - off, c - off, size) + offset),\
                         (a - off, c - off, height(a - off, c - off, size) - offset),\
                         # 3
                         (x, y + scale + off2, height(x, y + scale + off2, size) + offset),\
                         (x, y + scale + off2, height(x, y + scale + off2, size) - offset),\
                         (x, y + scale - off2, height(x, y + scale - off2, size) + offset),\
                         (x, y + scale - off2, height(x, y + scale - off2, size) - offset),\
                         # 4
                         (b - off, c + off, height(b - off, c + off, size) + offset),\
                         (b - off, c + off, height(b - off, c + off, size) - offset),\
                         (b + off, c - off, height(b + off, c - off, size) + offset),\
                         (b + off, c - off, height(b + off, c - off, size) - offset),\
                         # 5
                         (x - scale - off2, y, height(x - scale - off2, y, size) + offset),\
                         (x - scale - off2, y, height(x - scale - off2, y, size) - offset),\
                         (x - scale + off2, y, height(x - scale + off2, y, size) + offset),\
                         (x - scale + off2, y, height(x - scale + off2, y, size) - offset),\
                         # 6
                         (b - off, d - off, height(b - off, d - off, size) + offset),\
                         (b - off, d - off, height(b - off, d - off, size) - offset),\
                         (b + off, d + off, height(b + off, d + off, size) + offset),\
                         (b + off, d + off, height(b + off, d + off, size) - offset),\
                         # 7
                         (x, y - scale - off2, height(x, y - scale - off2, size) + offset),\
                         (x, y - scale - off2, height(x, y - scale - off2, size) - offset),\
                         (x, y - scale + off2, height(x, y - scale + off2, size) + offset),\
                         (x, y - scale + off2, height(x, y - scale + off2, size) - offset),\
                         # 8
                         (a + off, d - off, height(a + off, d - off, size) + offset),\
                         (a + off, d - off, height(a + off, d - off, size) - offset),\
                         (a - off, d + off, height(a - off, d + off, size) + offset),\
                         (a - off, d + off, height(a - off, d + off, size) - offset)]
        # Extend to star
        if bool == False:
            currentVerts += [(e + off2, k, height(e + off2, k, size) + offset),
                             (e + off2, k, height(e + off2, k, size) - offset),
                             (e - off2, k, height(e - off2, k, size) + offset),
                             (e - off2, k, height(e - off2, k, size) - offset),\
                             # 10
                             (g, i + off2, height(g, i + off2, size) + offset),\
                             (g, i + off2, height(g, i + off2, size) - offset),\
                             (g, i - off2, height(g, i - off2, size) + offset),\
                             (g, i - off2, height(g, i - off2, size) - offset),\
                             # 11
                             (h, i + off2, height(h, i + off2, size) + offset),\
                             (h, i + off2, height(h, i + off2, size) - offset),\
                             (h, i - off2, height(h, i - off2, size) + offset),\
                             (h, i - off2, height(h, i - off2, size) - offset),\
                             # 12
                             (f - off2, k, height(f - off2, k, size) + offset),\
                             (f - off2, k, height(f - off2, k, size) - offset),\
                             (f + off2, k, height(f + off2, k, size) + offset),\
                             (f + off2, k, height(f + off2, k, size) - offset),\
                             # 13
                             (f - off2, l, height(f - off2, l, size) + offset),\
                             (f - off2, l, height(f - off2, l, size) - offset),\
                             (f + off2, l, height(f + off2, l, size) + offset),\
                             (f + off2, l, height(f + off2, l, size) - offset),\
                             # 14
                             (h, j - off2, height(h, j - off2, size) + offset),\
                             (h, j - off2, height(h, j - off2, size) - offset),\
                             (h, j + off2, height(h, j + off2, size) + offset),\
                             (h, j + off2, height(h, j + off2, size) - offset),\
                             # 15
                             (g, j - off2, height(g, j - off2, size) + offset),\
                             (g, j - off2, height(g, j - off2, size) - offset),\
                             (g, j + off2, height(g, j + off2, size) + offset),\
                             (g, j + off2, height(g, j + off2, size) - offset),\
                             # 16
                             (e + off2, l, height(e + off2, l, size) + offset),\
                             (e + off2, l, height(e + off2, l, size) - offset),\
                             (e - off2, l, height(e - off2, l, size) + offset),\
                             (e - off2, l, height(e - off2, l, size) - offset)]
    ###########
    # Faces
    ###########
        # Octagon
        for u in range(0, 29, 4):
            if u < 25:
                currentFaces += [(start + u, start + u + 1, start + u + 5, start + u + 4),
                                 (start + u + 1, start + u + 3, start + u + 7, start + u + 5),
                                 (start + u + 2, start + u + 3, start + u + 7, start + u + 6),
                                 (start + u, start + u + 2, start + u + 6, start + u + 4)]
            else:
                currentFaces += [(start + u, start + u + 1, start + 1, start),
                                 (start + u + 1, start + u + 3, start + 3, start + 1),
                                 (start + u + 2, start + u + 3, start + 3, start + 2),
                                 (start + u, start + u + 2, start + 2, start)]
        # Extend to star
        if bool == False:
            for v in range(0, 29, 4):
                if v < 25:
                    currentFaces += [(start + v, start + v + 1, start + v + 33, start + v + 32),
                                     (start + v + 1, start + v + 3, start + v + 35, start + v + 33),
                                     (start + v + 2, start + v + 3, start + v + 35, start + v + 34),
                                     (start + v, start + v + 2, start + v + 34, start + v + 32),
                                     (start + v + 32, start + v + 33, start + v + 5, start + v + 4),
                                     (start + v + 33, start + v + 35, start + v + 7, start + v + 5),
                                     (start + v + 34, start + v + 35, start + v + 7, start + v + 6),
                                     (start + v + 32, start + v + 34, start + v + 6, start + v + 4)]
                else:
                    currentFaces += [(start + v, start + v + 1, start + v + 33, start + v + 32),
                                     (start + v + 1, start + v + 3, start + v + 35, start + v + 33),
                                     (start + v + 2, start + v + 3, start + v + 35, start + v + 34),
                                     (start + v, start + v + 2, start + v + 34, start + v + 32),
                                     (start + v + 32, start + v + 33, start + 1, start),
                                     (start + v + 33, start + v + 35, start + 3, start + 1),
                                     (start + v + 34, start + v + 35, start + 3, start + 2),
                                     (start + v + 32, start + v + 34, start + 2, start)]
    return [currentVerts, currentFaces]

######################
# Create Menu item
######################


def menu_func(self, context):
    self.layout.operator("mesh.fractal_dome",
                         text="Fractal dome",
                         icon='MESH_CIRCLE')

######################
# (Un)Register
######################


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.prepend(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
