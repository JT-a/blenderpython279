bl_info = {
    "name": "Grating",
    "description": "Adds adjustable grating",
    "category": "Add Mesh",
                "author": "Jacob Morris",
                "version": (0, 4),
                "location": "View3D > Add > Mesh"
}

import bpy


def addGrating(context, over_width, width_num, over_length, length_num, thickness, height):
    # convert meters to inches and round to 5 decimals places
    w = round(over_width / 39.3701, 5)
    l = round(over_length / 39.3701, 5)
    t = round(thickness / 39.3701, 5)
    h = round(height / 39.3701, 5)

    # figure out if t is possible
    if t > w / (width_num + 1) or t > l / (length_num + 1):
        t1 = (w / (width_num + 1)) - 0.001
        t2 = (l / (length_num + 1)) - 0.001
        if t1 < t2:
            t = t1
        elif t2 < t1:
            t = t2
    # figure out spacing
    w_s = w / (width_num + 1)
    w_m = w_s
    w_s -= t
    l_s = l / (length_num + 1)
    l_m = l_s
    l_s -= t

    verts = []
    # number of verts for bottom
    num_for_b = 0

    # first row of verts
    cur_po_x = (w / 2) + (0.5 * t)
    cur_po_y = 0.0
    cur_po_z = 0.0

    # all verts
    for up_down in range(2):
        for num in range(length_num + 2):
            for i in range(width_num + 2):
                verts.append((cur_po_x, cur_po_y, cur_po_z))
                cur_po_x -= t
                verts.append((cur_po_x, cur_po_y, cur_po_z))
                cur_po_x -= w_s
            cur_po_x = (w / 2) + (0.5 * t)
            cur_po_y += t
            for i in range(width_num + 2):
                verts.append((cur_po_x, cur_po_y, cur_po_z))
                cur_po_x -= t
                verts.append((cur_po_x, cur_po_y, cur_po_z))
                cur_po_x -= w_s
            cur_po_y += l_s
            cur_po_x = (w / 2) + (0.5 * t)
        # reset variables
        cur_po_y = 0.0
        cur_po_x = (w / 2) + (0.5 * t)
        cur_po_z = h
        if num_for_b == 0:
            num_for_b = len(verts)

    # faces
    faces = []
    # bottom verts
    # counter
    c = 0
    width_po = 0
    row_vert = (width_num + 2) * 2
    length_vert = (length_num + 2) * 2
    # solid row or slates
    s_s = "solid"
    # bottom and top faces
    for bt in range(2):
        for vt in range(row_vert * (length_vert - 1)):
            if s_s == "solid":
                if width_po + 1 < row_vert:
                    if c < num_for_b:
                        faces.append((c, c + 1, c + row_vert + 1, c + row_vert))
                    else:
                        faces.append((c, c + row_vert, c + row_vert + 1, c + 1))
            elif s_s == "slates":
                if width_po % 2 == 0:
                    if c < num_for_b:
                        faces.append((c, c + 1, c + row_vert + 1, c + row_vert))
                    else:
                        faces.append((c, c + row_vert, c + row_vert + 1, c + 1))
            c += 1
            width_po += 1
            if width_po == row_vert:
                width_po = 0
                if s_s == "solid":
                    s_s = "slates"
                elif s_s == "slates":
                    s_s = "solid"
        c = num_for_b
        width_po = 0
        s_s = "solid"
    # rest of faces
    c = 0
    c_r = 1
    width_po = 0
    inner_out = False
    for i in range(row_vert * length_vert):
        # first row
        if c_r == 1:
            if width_po == 0 or width_po + 1 == row_vert:
                if width_po + 1 == row_vert:
                    faces.append((c, c + num_for_b, c + row_vert + num_for_b, c + row_vert))
                else:
                    faces.append((c, c + row_vert, c + row_vert + num_for_b, c + num_for_b))
                    faces.append((c, c + num_for_b, c + num_for_b + 1, c + 1))
            elif 0 < width_po < row_vert:
                faces.append((c, c + num_for_b, c + num_for_b + 1, c + 1))
        # outer rows (even numbers)
        elif c_r % 2 == 0 and c_r != length_vert:
            if width_po == 0 or width_po + 1 == row_vert:
                if width_po == 0:
                    faces.append((c, c + row_vert, c + row_vert + num_for_b, c + num_for_b))
                else:
                    faces.append((c, c + num_for_b, c + row_vert + num_for_b, c + row_vert))
            elif width_po % 2 != 0:
                faces.append((c, c + num_for_b, c + row_vert + num_for_b, c + row_vert))
                faces.append((c, c + 1, c + num_for_b + 1, c + num_for_b))
            elif width_po % 2 == 0:
                faces.append((c, c + row_vert, c + row_vert + num_for_b, c + num_for_b))
        # inner rows (odd numbers)
        elif c_r % 2 != 0:
            if width_po == 0 or width_po + 1 == row_vert:
                if width_po == 0:
                    faces.append((c, c + row_vert, c + row_vert + num_for_b, c + num_for_b))
                else:
                    faces.append((c, c + num_for_b, c + row_vert + num_for_b, c + row_vert))
            else:
                if inner_out == False:
                    faces.append((c, c + num_for_b, c + num_for_b + 1, c + 1))
                    inner_out = True
                else:
                    inner_out = False
        # last row
        elif c_r == length_vert:
            if width_po + 1 != row_vert:
                faces.append((c, c + 1, c + num_for_b + 1, c + num_for_b))

        width_po += 1
        c += 1
        if width_po == row_vert:
            width_po = 0
            c_r += 1

    me = bpy.data.meshes.new("grating")
    me.from_pydata(verts, [], faces)
    ob = bpy.data.objects.new("grating", me)
    context.scene.objects.link(ob)
    context.scene.objects.active = ob
    return ob

#   User interface

from bpy.props import *


class MESH_OT_primitive_add_grating(bpy.types.Operator):
    '''Add Grating'''
    bl_idname = "mesh.primitive_add_grating"
    bl_label = "Add Grating"
    bl_options = {'REGISTER', 'UNDO'}

    over_width = FloatProperty(name="Overall Width (in)",
                               description="From outer to outer slate centers",
                               default=10.0, min=1.0, max=2000.0)
    width_num = IntProperty(name="Width Slates (#)",
                            description="Number of slates between edges",
                            default=6, min=0, max=256)
    over_length = FloatProperty(name="Overall Length (in)",
                                description="From end to end slate centers",
                                default=24.0, min=1.0, max=2000.0)
    length_num = IntProperty(name="Length Slates (#)",
                             description="Number of slates between ends",
                             default=4, min=0, max=256)
    thickness = FloatProperty(name="Thickness (in)",
                              description="Grating thickness (width)",
                              default=0.5, min=0.1, max=6.0)
    height = FloatProperty(name="Height (in)",
                           description="Grating height",
                           default=2.0, min=0.5, max=12.0)
    rotation = FloatVectorProperty(name="Rotation (XYZ)", description="Rotate grating",
                                   unit="ROTATION")

    def execute(self, context):
        if context.mode == "OBJECT":
            ob = addGrating(context,
                            self.over_width, self.width_num, self.over_length, self.length_num, self.thickness, self.height)
            ob.location = bpy.context.scene.cursor_location
            ob.rotation_euler = self.rotation
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator("mesh.primitive_add_grating",
                         text="Grating",
                         icon='MESH_GRID')

# Register


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.prepend(menu_func)
    try:
        bpy.types.MESH_PT_addons.append(menu_func)
    except:
        pass


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
    try:
        bpy.types.MESH_PT_addons.remove(menu_func)
    except:
        pass
if __name__ == "__main__":
    register()
