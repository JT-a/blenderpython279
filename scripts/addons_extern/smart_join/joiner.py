__author__ = 'andrejivanis'
# BEGIN GPL LICENSE BLOCK #####
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
# END GPL LICENSE BLOCK #####

import bpy, bmesh


# these make Function.view expected a SpaceView3D type, not SpaceTimeline
def add_to_all_visible_layers(obj, scn):
    sd = bpy.context.space_data
    if sd and type(sd) is bpy.types.SpaceView3D:
        scn.object_bases[obj.name].layers_from_view(bpy.context.space_data)

def add_to_loc_view(obj, scn):
    layers = obj.layers[:]

    add_to_all_visible_layers(obj,scn)
    obj.layers = layers

def duplicate_linked(objects, some_visible_obj = None, visible_only = True):
    context = bpy.context
    scn = bpy.context.scene
    # sel = context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    # for o in scn.objects:
    #     o.select = False


    # link all object not in scene and select them
    to_unlink = []
    to_unhide = []
    for o in objects:
        # cpy = o.copy()
        # scn.objects.link(cpy)
        # cpy.select = True
        o.select = True

        # hidden object aren't duplicated properly
        if not visible_only:
            unhide_temp(o)

        if o.name not in scn.objects:
            scn.objects.link(o)
            to_unlink.append(o)

        # TODO: this needs to be reverted, but for now I always remove all object from scene somewhere later
        if some_visible_obj:
            o.layers = some_visible_obj.layers

        add_to_all_visible_layers(o, scn)
    scn.update()


    bpy.ops.object.duplicate(linked=True)
    for o in objects:
        rehide(o)


    for o in to_unlink:
        scn.objects.unlink(o)
    sel = context.selected_objects[:]
    for o in sel:
        rehide(o)

    scn.update()
    return sel




def unhide_temp(o):
    if o.hide:
        o.hide = False
        o['hide_temp'] = True

def rehide(o):
    ht = o.get('hide_temp')
    if ht:
        del o["hide_temp"]
        o.hide = True



def join_to_mesh(context, mesh, objects, some_visible_obj):

    sel = context.selected_objects
    act = context.active_object

    scn = context.scene

    duplicate_linked(objects, some_visible_obj)

    ## make real recursively in case of dupli groups inside dupli groups
    def doop(o):
        return o.dupli_type != 'NONE'
    while any([doop(o) for o in context.selected_objects]):
        bpy.ops.object.duplicates_make_real()

    # and once for particles
    bpy.ops.object.duplicates_make_real()

    # make new meshes and apply modifiers, can't use object.make_single_user because it can mess up curves used by modifiers I need copy all objects
    newObjs = []
    applied_meshes = []
    old_objs = []
    for obj in context.selected_objects[:]:
        if not obj.data:
            continue
        # to_mesh will fail if no geometry data is found
        try:
            m = obj.to_mesh(bpy.context.scene, True, 'PREVIEW')
            # looks like obj.to_mesh can return None (empty curve?)
            if not m:
                continue
        except:
            continue

        # if there are no material create empty slot so you don't get other materials in join
        if len(m.materials) == 0:
            m.materials.append(None)

        objcpy = bpy.data.objects.new('copy', object_data = m)
        scn.objects.link(objcpy)
        objcpy.layers = some_visible_obj.layers
        add_to_loc_view(objcpy, scn)
        objcpy.matrix_world = obj.matrix_world
        applied_meshes.append(m)
        newObjs.append(objcpy)
        old_objs.append(obj)



    # set all the sharp angles from autosmooth
    for i, new_mesh in enumerate(applied_meshes):
        o = old_objs[i]
        if o.type != 'MESH':
            continue


        # make unique UVMap
        # TODO: I won't ever need this probably, but I should keep other maps
        '''
        if 'sjoin_uvs' not in new_mesh.uv_textures:
            new_mesh.uv_textures.new('sjoin_uvs')
        '''

        for t in new_mesh.uv_textures[:]:
            # texture layer 'NGon Face' not found??? fixed by: and t.name in new_mesh.uv_textures
            if not t.active and t.name in new_mesh.uv_textures:
                new_mesh.uv_textures.remove(t)

        if new_mesh.uv_textures.active:
            new_mesh.uv_textures.active.name = 'UVMap'

        correct_normals(new_mesh, o.scale)




        if not o.data.use_auto_smooth or (o.data.use_auto_smooth and o.data.auto_smooth_angle == 180) or o.data.is_sjoin:
            pass
        else:
            #looks like o.data.auto_smooth_angle is in radians although displayed in degrees in GUI
            correct_somoothing(new_mesh, o.data.auto_smooth_angle)



    # delete copied objects and select duplicate ones
    bpy.ops.object.delete(use_global=False)

    for o in newObjs:
        o.select = True


    ### clear the mesh geometry
    # clear_mesh(mesh)

    ## autosmooth on (might not always help)
    mesh.use_auto_smooth = True
    mesh.auto_smooth_angle = 180

    #create new join object with given mesh
    j_obj = bpy.data.objects.new(name = 'temp_obj', object_data= mesh)

    j_obj.select = True
    j_obj.location = (0,0,0)
    j_obj.layers = [True] * 20
    scn.objects.link(j_obj)
    # without this local view won't work
    j_obj.layers = some_visible_obj.layers
    add_to_loc_view(j_obj, scn)

    scn.objects.active = j_obj

    ### join to mesh and delete objects if any left
    bpy.ops.object.join()

    # for o in newObjs:
    #     if o:
    #         if o.name in scn.objects:
    #             scn.objects.unlink(o)
    #         bpy.data.objects.remove(o)

    for m in applied_meshes:
        if m.users == 0:
            bpy.data.meshes.remove(m)


    # delete the joined object
    #  it looks like removing the object deletes materials of j_obj.data??? so I make a dummy mesh as a workaround
    bug_fix = bpy.data.meshes.new(name = 'bug_fix')
    j_obj.data = bug_fix
    for o in bpy.context.selected_objects[:]:
        scn.objects.unlink(o)
        #  this will mess up materials of o.data if i remove o afterwards?
        bpy.data.objects.remove(o)

    bpy.data.meshes.remove(bug_fix)

    ## get old selection
    for o in sel:
        o.select = True
    scn.objects.active = act
    # scn.update()


def clear_mesh(mesh):
    bm = bmesh.new()
    bm.to_mesh(mesh)
    bm.free()
    mesh.materials.clear()
    mesh.update()


def correct_normals(mesh, scale):
    tot_scale = 1
    # this is not real scale? but works anyways
    for s in scale:
        tot_scale *= 1 if s >= 0 else -1

    if tot_scale < 0:
        bm = bmesh.new()   # create an empty BMesh
        bm.from_mesh(mesh)   # fill it in from a Mesh

        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])

        # Finish up, write the bmesh back to the mesh
        bm.to_mesh(mesh)
        bm.free()




def correct_somoothing(mesh, angle):
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(mesh)   # fill it in from a Mesh

    bmesh_correct_somoothing(bm, angle)

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(mesh)
    bm.free()

def bmesh_correct_somoothing(bm, angle):

    for e in bm.edges:
        ang = e.calc_face_angle(None)

        if ang:
            if ang > angle:
                e.smooth = False
