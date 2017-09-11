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
    "name": "Spawn XYZ",
    "author": "Jimmy Hazevoet",
    "version": (0, 2, 0),
    "blender": (2, 7, 8),
    "location": "View3D > Tool Shelf",
    "description": "Adds copy's of multiple selected objects or groups at selected faces, with randomisation per object",
    "category": "Object"}

import bpy
from bpy.types import Operator
from bpy.props import (
        FloatProperty,
        IntProperty,
        BoolProperty,
        EnumProperty,
        )
from bpy_extras.mesh_utils import face_random_points
from mathutils import Matrix, Vector
from math import radians
from random import random, choice, seed


def use_random_seed(self):
    seed(self.rSeed)
    return


class CopyObjectsToFaces(bpy.types.Operator):
    bl_idname = "wm.place_objects_at_faces"
    bl_label = "Copy objects to faces"
    bl_description="Place copy's of multiple selected objects or groups at selected faces of active mesh"
    bl_options = {'REGISTER', 'UNDO','PRESET'}

    update_now = BoolProperty(name="Update",
            description="Update",
            default=True
            )
    duptypes = [('DUPLICATE', 'Duplicate', 'DUPLICATE'),
            ('LINKED', 'Linked duplicate', 'LINKED'),
            ('GROUP', 'Group instance', 'GROUP')]
    dup_mode = EnumProperty(name="Method",
            description="Duplication method",
            items=duptypes,
			default='DUPLICATE'
            )
    rSeed = IntProperty(
            name="Random seed",
            description="Random seed number",
            default=0,
            min=0, max=999999
            )
    probability = IntProperty(
            name="Probability",
            description="Chance of duplicating a object to a face",
            default=100,
            min=0, max=100
            )
    density = IntProperty(
            name="Number",
            description="Number of objects per face, if density is 0 it places one object at face center",
            default=0,
            min=0, max=1000, soft_max=50
            )
    offset = FloatProperty(
            name="Offset",
            description="Offset along face normal",
            precision=3,
            default=0.0,
            min=0.0, max=100.0
            )
    random_offset = FloatProperty(
            name="Random",
            description="Random offset along face normal",
            default=0.0,
            min=0.0, max=100.0
            )
    rotate = FloatProperty(
            name="Rotate",
            description="Rotate",
            precision=3,
            default=0.0,
            min=-360.0, max=360.0
            )
    random_rotate = FloatProperty(
            name="Random",
            description="Rotate random",
            default=0.0,
            min=0.0, max=100.0
            )
    re_size = FloatProperty(
            name="Size",
            description="Size",
            precision=3,
            default=1.0,
            min=0.0, max=100.0
            )
    random_size = FloatProperty(
            name="Random",
            description="Random size",
            default=0.0,
            min=0.0, max=100.0, soft_max=2.0
            )
    adaptive = BoolProperty(name="Adaptive size",
            description="Adaptive size",
            default=False
            )
    set_parent = BoolProperty(name="Parent",
            description="Set parent, attach objects to target object",
            default=False
            )

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, 'update_now', toggle=True, icon='FILE_REFRESH')
        col.separator()
        col.prop(self, 'dup_mode', text="")
        col.separator()
        col.prop(self, 'density')
        #col.prop(self, 'probability')
        col.separator()
        col.prop(self, 'offset')
        col.prop(self, 'random_offset')
        col.separator()
        col.prop(self, 'rotate')
        col.prop(self, 'random_rotate')
        col.separator()
        col.prop(self, 're_size')
        col.prop(self, 'random_size')
        col.prop(self, 'adaptive')
        col.separator()
        col.prop(self, 'rSeed')
        col.separator()
        col.prop(self, 'set_parent')
        col.prop(context.space_data, "show_relationship_lines")

    @classmethod
    def poll(self, context):
        ob = context.active_object
        return ((ob is not None) and
            (len(context.selected_objects) >=2) and
            (ob.type == 'MESH') and
            (context.mode == 'OBJECT'))

    def invoke(self, context, event):
        self.update_now = True
        return self.execute(context)

    def execute(self, context):
        if not self.update_now:
            return {'PASS_THROUGH'}
        obs = []
        group_donor=[]
        scn = bpy.context.scene
        use_random_seed(self)

        target_object = bpy.context.active_object
        donor = [o for o in bpy.context.selected_objects if o != target_object]
        if not donor: return{'FINISHED'}
        for do in donor:
            if do.type == 'EMPTY':
                self.report({'WARNING'}, 'Empty objects are not suported..!')
                return{'FINISHED'}

        for group in bpy.data.groups:
            group_objects = group.objects
            for dg in donor:
                if dg.name in group.objects and dg in group_objects[:]:
                    group_donor.append(group.name)

        bpy.ops.object.select_all(action='DESELECT')

        for f in target_object.data.polygons:
            if f.select:
                i=0
                frp = face_random_points(self.density, [f])
                obj_density = self.density
                if self.density == 0:
                    obj_density = 1
                while i < obj_density:
                    #if self.probability > int(random()*100):

                        if self.dup_mode == 'GROUP':
                            try:
                                instance = choice(group_donor)
                                bpy.ops.object.group_instance_add(name=instance, group=instance)                        
                                obj = bpy.context.active_object
                            except:
                                self.report({'WARNING'}, 'No group available..! Linked duplicate instead')
                                obj = choice(donor).copy()
                                scn.objects.link(obj)

                        elif self.dup_mode == 'LINKED':
                            obj = choice(donor).copy()
                            scn.objects.link(obj)

                        elif self.dup_mode == 'DUPLICATE':
                            obj = choice(donor).copy()
                            obj.data = obj.data.copy()
                            scn.objects.link(obj)

                        obs.append(obj)

                        # location
                        if self.density >= 1:
                            obj.location = frp[i]
                        elif self.density == 0:
                            obj.location = f.center

                        lvar = random() * self.random_offset
                        obj.location += f.normal*(self.offset + lvar)

                        if obj.type in ['LAMP','CAMERA']:
                            obj.matrix_basis += target_object.matrix_world
                            z_dir='-Z'
                        else:
                            obj.matrix_basis *= target_object.matrix_world
                            z_dir='Z'

                        # rotation
                        rvar = (1.0 + (random()-0.5) * self.random_rotate)
                        obj.rotation_euler = f.normal.to_track_quat(z_dir, 'Y').to_euler()
                        obj.matrix_basis *= Matrix.Rotation(radians(self.rotate * rvar), 4, 'Z')

                        # scale
                        if self.adaptive is True:
                            size = obj.scale * (f.area**0.25)
                        else:
                            size = obj.scale

                        svar = (1.0 + (random()-0.5) * self.random_size)
                        obj.scale = ((size[0] * self.re_size) * svar,
                                    (size[1] * self.re_size) * svar,
                                    (size[2] * self.re_size) * svar
                                    )
                        i+=1
                    ####

        scn.objects.active = target_object
        for ob in obs:
            ob.select = True
            if set_parent is True:
                bpy.ops.object.parent_set(type='OBJECT', xmirror=False, keep_transform=True)
            ob.layers[:] = target_object.layers
        target_object.select = False
        #self.update_now = False
        return{'FINISHED'}


class PanelCOTF(bpy.types.Panel):
    bl_label = 'Spawn XYZ'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Create"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(CopyObjectsToFaces.bl_idname) #, icon='SNAP_NORMAL')


def register():
    bpy.utils.register_class(CopyObjectsToFaces)
    bpy.utils.register_class(PanelCOTF)

def unregister():
    bpy.utils.unregister_class(CopyObjectsToFaces)
    bpy.utils.unregister_class(PanelCOTF)

if __name__ == '__main__':
    register()