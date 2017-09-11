'''
Particle Fluid Tools
Copyright (C) 2012  Sebastian Röthlisberger (bashi)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/
'''

bl_info = {
    "name": "Particle Fluid Tools",
    "author": "bashi",
    "version": (0, 3, 1),
    "blender": (2, 6, 3),
    "api": 33333,
    "location": "View3D > Toolbar",
    "description": "Converts Particles to Metaball or Mesh",
    "warning": "alpha",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}


import bpy
import time

bpy.types.Scene.pfluid_size = bpy.props.FloatProperty(name="MBall Size", default=1.6, min=0.01, max=10)
bpy.types.Scene.pfluid_resolution = bpy.props.FloatProperty(name="MBall Resolution", default=1.0, min=0.05, max=2.0)  # MAX HACK

bpy.types.Scene.pfluid_threshold = bpy.props.FloatProperty(name="MBall threshold", default=0.5, min=0.01, max=1.0)

bpy.types.Scene.pfluid_shrink = bpy.props.BoolProperty(name="Shrink", description='Shrinkwrap on Particles', default=True)
bpy.types.Scene.pfluid_skin = bpy.props.FloatProperty(name="Skin", default=0.003, min=0.0001, max=0.2)

bpy.types.Scene.pfluid_smooth = bpy.props.BoolProperty(name="Smooth", description='Smooth Mesh', default=True)
# bpy.types.Scene.pfluid_mesh_subsurf_level = bpy.props.IntProperty(name = "Mesh Subsurf",default = 0)
bpy.types.Scene.pfluid_mesh_smooth_factor = bpy.props.FloatProperty(name="Mesh Smooth Factor", default=0.5, min=0.0, max=2.5)
bpy.types.Scene.pfluid_mesh_smooth_iterations = bpy.props.IntProperty(name="Mesh Smooth Iterations", default=8, min=0, max=200)

bpy.types.Scene.pfluid_mod_apply = bpy.props.BoolProperty(name="Modifiers Apply", description='Apply Modifiers', default=True)

bpy.types.Scene.pfluid_frame_start = bpy.props.IntProperty(name="Frame Start", default=1)
bpy.types.Scene.pfluid_frame_end = bpy.props.IntProperty(name="Frame End", default=250)


class PFluid_Tools(bpy.types.Panel):
    bl_label = "PFluid Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):

        scene = context.scene
        object = context.object
        # mball = object.data

        self.layout.prop(scene, "pfluid_size")
        self.layout.prop(scene, "pfluid_resolution")
        self.layout.prop(scene, "pfluid_threshold")
        # self.layout.operator("particle.pfluid_make_mball", icon="META_DATA")
        # self.layout.prop(object.data, "pfluid_size")
        # self.layout.operator("mball.pfluid_update", icon="FILE_REFRESH")

        self.layout.prop(scene, "pfluid_shrink")
        self.layout.prop(scene, "pfluid_skin")

        self.layout.prop(scene, "pfluid_smooth")
        # self.layout.prop(scene, "pfluid_mesh_subsurf_level")
        self.layout.prop(scene, "pfluid_mesh_smooth_factor")
        self.layout.prop(scene, "pfluid_mesh_smooth_iterations")
        self.layout.prop(scene, "pfluid_mod_apply")
        self.layout.operator("mball.pfluid_mesh", icon="OUTLINER_OB_META")

        self.layout.prop(scene, "pfluid_frame_start")
        self.layout.prop(scene, "pfluid_frame_end")
        self.layout.operator("mball.pfluid_mesh_seq", icon="OUTLINER_OB_CAMERA")


# Converts MBall to Mesh and add Subsurf and Smooth modifier
class OBJECT_OT_MBallMesh(bpy.types.Operator):
    bl_idname = "mball.pfluid_mesh"
    bl_label = "Make Mesh"

    def execute(self, context):

        scene = context.scene

        start = time.time()

        objs = context.selected_objects
        # particles = obj.particle_systems[0].particles

        def make_pcloud(objs):

           # Make Point Cloud list
            pc = []

            for obj in objs:
                # Has Particle Systems
                if len(obj.particle_systems) > 0:
                    # print('has Particles')
                    for p_sys in obj.particle_systems:
                        for particle in p_sys.particles:
                            if 'ALIVE' in particle.alive_state:
                                p_data = particle.location  # , particle.velocity
                                # print(p_data)
                                pc.append(p_data)

                # Has no Particles,  Treat as Object -> Get Vertices
                else:
                    # print('has no Particles')
                    for vertex in obj.data.vertices:
                        p_data = vertex.co + obj.location
                        pc.append(p_data)

            # print(pc)
            return(pc)

        def make_mesh(objs):

            pc = make_pcloud(objs)

            mball = bpy.data.metaballs.new('mball')
            bpy.data.objects.new('metaball', mball)
            metaball = bpy.data.objects['metaball']
            bpy.context.scene.objects.link(metaball)

            metaball.scale = (0.05, 0.05, 0.05)

            mball.resolution = scene.pfluid_resolution
            mball.render_resolution = scene.pfluid_resolution
            mball.threshold = scene.pfluid_threshold
            mball.update_method = 'FAST'

            bpy.ops.object.select_all(action='DESELECT')
            metaball.select = 1
            bpy.context.scene.objects.active = metaball

            for point in pc:

                el = mball.elements.new()
                el.co = point / 0.05

                el.radius = scene.pfluid_size

            bpy.ops.object.convert()
            metaball = context.object

            # Apply Smooth
            mod_check = 0
            if scene.pfluid_shrink == True:

                pc_mesh = bpy.data.meshes.new('pc_mesh')

                bpy.data.objects.new('pc_obj', pc_mesh)
                pc_obj = bpy.data.objects['pc_obj']
                bpy.context.scene.objects.link(pc_obj)

                count = 0
                for point in pc:
                    print(point)
                    pc_mesh.vertices.add(1)
                    pc_mesh.vertices[count].co = point

                    count += 1

                # Pre-Smooth to get rid of Shrinkwrap Problems
                metaball.modifiers.new('presmooth', type='SMOOTH')
                metaball.modifiers['presmooth'].factor = 0.18
                metaball.modifiers['presmooth'].iterations = 64
                # bpy.ops.object.convert()
                # metaball = context.object

                metaball.modifiers.new('shrink', type='SHRINKWRAP')
                metaball.modifiers['shrink'].target = pc_obj
                metaball.modifiers['shrink'].wrap_method = 'NEAREST_VERTEX'
                metaball.modifiers['shrink'].offset = scene.pfluid_skin
                # bpy.ops.object.convert()  # To Avoid Problems while Point Cloud is deleted and Modifier still there
                # metaball = context.object

                # Remove Doubles
                # bpy.ops.object.editmode_toggle()
                # bpy.ops.mesh.remove_doubles()
                # bpy.ops.object.editmode_toggle()

                bpy.context.scene.objects.unlink(pc_obj)

                mod_check += 1

            if scene.pfluid_smooth == True:
                metaball.modifiers.new('smooth', type='SMOOTH')
                metaball.modifiers['smooth'].factor = scene.pfluid_mesh_smooth_factor
                metaball.modifiers['smooth'].iterations = scene.pfluid_mesh_smooth_iterations
                mod_check += 1

            if scene.pfluid_mod_apply == True:
                bpy.ops.object.convert()
                metaball = context.object

                # Remove Doubles
                bpy.ops.object.editmode_toggle()
                bpy.ops.mesh.remove_doubles()
                bpy.ops.object.editmode_toggle()

                # delete PointCloud Object

            # if mod_check is not 0:
                # bpy.context.scene.objects.unlink(pobj)

        make_mesh(objs)

        end = time.time()
        print(str(end - start))

        return{'FINISHED'}


# Run MBall, make_mesh and Export -obj for Range
class OBJECT_OT_Mesh_Sequence(bpy.types.Operator):
    bl_idname = "mball.pfluid_mesh_seq"
    bl_label = "Mesh Sequence"
    # def mesh_sequence(frame_start, frame_end):

    def execute(self, context):

        frame_start = context.scene.pfluid_frame_start
        frame_end = context.scene.pfluid_frame_end
        objs = context.selected_objects

        bpy.ops.object.add()
        empty = context.object
        empty.name = "PFluid Meshes"
        bpy.ops.object.select_all()

        mat = bpy.data.materials.new("Fluid")

        bpy.context.scene.frame_set(frame_start)

        for i in range(frame_start, frame_end + 2):

            for obj in objs:
                obj.select = True

            # frame = frame_start+i
            # bpy.context.scene.frame_set(i)

            # print(frame)
            print(context.scene.frame_current)

            bpy.ops.mball.pfluid_mesh()

            bpy.context.object.parent = empty
            bpy.context.object.data.materials.append(mat)

            set_visibility(context.object)

            # bpy.ops.object.select_all()

            obj.select = True

            bpy.context.scene.frame_set(i)

        return{'FINISHED'}


'''# Run MBall, make_mesh and Export -obj for Range
class OBJECT_OT_Mesh_Sequence(bpy.types.Operator):
    bl_idname = "mball.pfluid_mesh_seq"
    bl_label = "Mesh Sequence"
    # def mesh_sequence(frame_start, frame_end):

    def execute(self, context):


        frame_start = context.scene.pfluid_frame_start
        frame_end = context.scene.pfluid_frame_end
        obj = context.selected_objects

        bpy.ops.object.add()
        empty = bpy.context.object
        empty.name = "PFluid Meshes"
        bpy.ops.object.select_all()

        mat = bpy.data.materials.new("Fluid")


        for i in range(len(obj)):
            obj[i].select = True

        bpy.context.scene.frame_set(frame_start)

        for i in range(frame_start, frame_end+1):

            print(i)



            bpy.ops.mball.pfluid_mesh()
            bpy.context.object.parent = empty
            bpy.context.object.data.materials.append(mat)

            set_visibility(context.object)

            # bpy.ops.object.select_all()
            for i in range(len(obj)):
                obj[i].select = True



            bpy.context.scene.frame_set(frame_start+i)
        return{'FINISHED'}

'''


def set_visibility(obj):

    i = bpy.context.scene.frame_current

    obj.hide_render = False
    obj.hide = False
    obj.keyframe_insert("hide")
    obj.keyframe_insert("hide_render")

    bpy.context.scene.frame_set(i - 1)
    obj.hide_render = True
    obj.hide = True
    obj.keyframe_insert("hide")
    obj.keyframe_insert("hide_render")

    bpy.context.scene.frame_set(i + 1)
    obj.hide_render = True
    obj.hide = True
    obj.keyframe_insert("hide")
    obj.keyframe_insert("hide_render")


def register():
    bpy.utils.register_class(PFluid_Tools)
    # bpy.utils.register_class(OBJECT_OT_MakeMBall)
    bpy.utils.register_class(OBJECT_OT_MBallMesh)
    bpy.utils.register_class(OBJECT_OT_Mesh_Sequence)
    # bpy.utils.register_class(OBJECT_OT_Set_Mball_Size)


def unregister():
    bpy.utils.unregister_class(PFluid_Tools)
    # bpy.utils.unregister_class(OBJECT_OT_MakeMBall)
    bpy.utils.unregister_class(OBJECT_OT_MBallMesh)
    bpy.utils.unregister_class(OBJECT_OT_Mesh_Sequence)
    # bpy.utils.unregister_class(OBJECT_OT_Set_Mball_Size)


if __name__ == '__main__':
    register()
