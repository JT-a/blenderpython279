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

if "bpy" in locals():
    import imp
    imp.reload(joiner)
else:
    from . import joiner

import bpy, bmesh

def get_sjmesh(name):
    mesh = bpy.data.meshes.get(name)
    if mesh and mesh.is_sjoin:
        return mesh
    return None

def get_stored_sjobjects_unsafe(sj_mesh_name):
    return [o for o in bpy.data.objects if o.sjoin_mesh == sj_mesh_name]

def check_fix_rename(sj_mesh, sj_obj = None, scn = None):

    # sjoin check performed by update object

    # first, check if mesh is renamed or duplicated
    if sj_mesh.sjoin_link_name != sj_mesh.name and sj_mesh.sjoin_link_name != '':
        # make sure some delete mesh didn't leave objects
        objs = get_stored_sjobjects_unsafe(sj_mesh.name)
        for o in objs:
            o.sjoin_mesh = ''
            o.fake_user = False


        # mesh is renamed or duplicated, see if there is old mesh with this name to determine
        old_mesh = get_sjmesh(sj_mesh.sjoin_link_name)
        if old_mesh:
            # duplicated, duplicate all the object and link them to this mesh
            if scn:
                sel = [o for o in scn.objects if o.select]
            collapse_expanded(old_mesh)
            if sj_obj:
                set_object_collapsed(sj_obj)

                '''
                if len(sj_obj.children) == 0:
                    set_object_collapsed(sj_obj)
                else:
                    set_object_expended(sj_obj)
                '''
            sj_objs = get_stored_sjobjects_unsafe(sj_mesh.sjoin_link_name)
            duplicates = joiner.duplicate_linked(sj_objs, sj_obj, False)
            for new_o in duplicates:
                unlink_store(new_o, sj_mesh)

            if scn:
                for o in sel:
                    o.select = True

            # introduces crash bug
            # update_stored(sj_mesh)
        else:
            # renamed
            sj_objs = get_stored_sjobjects_unsafe(sj_mesh.sjoin_link_name)
            for o in sj_objs:
                o.sjoin_mesh = sj_mesh.name

        # no matter what keep sjoin_link_name same as sj_mesh.name
        sj_mesh.sjoin_link_name = sj_mesh.name


    # make sure there are no two expended objects, actually ones that look expended, this can happen if expended sj is duplicated
    if not check_is_expended(sj_obj):
        set_object_collapsed(sj_obj)


def check_is_sjoin_obj(obj):
    return obj and obj.type == 'MESH' and obj.data.is_sjoin


def check_is_expended(obj):
    return check_is_sjoin_obj(obj) and obj.data.expanded_obj == obj.name

def check_is_there_expended_obj(mesh):
    return mesh.expanded_obj != ''

def get_stored_sjobjects(sj_mesh):
    # check_fix_rename(sj_mesh)
    return get_stored_sjobjects_unsafe(sj_mesh.name)

import mathutils

# def collect_children_no_clear

def get_dependent_meshes(data):
    dep = []
    for o in bpy.data.objects:
        if o.data == data:
            # if object is part of sjoin add it
            sj = get_sjmesh(o.sjoin_mesh)
            if sj and sj != data and not check_is_there_expended_obj(sj):
                dep.append(sj)
    return dep


def update_stored(mesh):
    joiner.clear_mesh(mesh)
    # I need to redesign this passing bpy.context.active_object is bad, pass context everywhere or something
    if bpy.context.active_object:
        joiner.join_to_mesh(bpy.context, mesh, get_stored_sjobjects(mesh), bpy.context.active_object)


def update_meshes_rec_co(meshes, c):
    if c == 10:
        return

    next_dep = []
    for mesh in meshes:
        update_stored(mesh)
        next_dep += get_dependent_meshes(mesh)

    update_meshes_rec_co(next_dep, c+1)

def update_meshes_rec(meshes):
    update_meshes_rec_co(meshes, 0)

def update_data_rec(data):
    mashes = get_dependent_meshes(data)
    update_meshes_rec(mashes)

def collect_children_unsafe(obj, scn):
    if not obj:
        return
    set_object_collapsed(obj)
    joiner.clear_mesh(obj.data)
    all_ch = get_all_children(obj)


    obj.data.sjoin_link_name = obj.data.name


    for ch in all_ch:
        # unlink_store(ch, obj.data)
        if ch.parent == obj:
            basis = ch.matrix_parent_inverse * ch.matrix_basis
            ch.parent = None
            ch.matrix_basis = basis

    scn.update()
    joiner.join_to_mesh(bpy.context, obj.data, all_ch + get_stored_sjobjects(obj.data), obj)
    update_meshes_rec(get_dependent_meshes(obj.data))

    for ch in all_ch:
        unlink_store(ch, obj.data)


# careful this return parent too
def get_leaf_children(obj):
    if len(obj.children) == 0:
        return [obj]
    else:
        return [x for o in obj.children for x in get_leaf_children(o)]

def get_all_children(obj):
    if len(obj.children) == 0:
        return []
    else:
        return list(obj.children) + [x for o in obj.children for x in get_leaf_children(o)]

def get_children_hierarchically(obj_list):
    if not obj_list:
        return []

    next_level = []
    for obj in obj_list:
        next_level += list(obj.children)


    return get_children_hierarchically(next_level) + obj_list

def get_expanded_obj(sj_mesh):
    return bpy.data.objects.get(sj_mesh.expanded_obj)

def collapse_expanded(sj_mesh):
    obj = get_expanded_obj(sj_mesh)
    if obj:
        collect_children(obj, bpy.context.scene)


def collect_children(obj, scn):
    # collect_children_unsafe(obj, scn)
    # return
    if obj is None:
        return

    global update_lock
    update_lock = True

    children = get_children_hierarchically([obj])

    for ch in children:
        # check_is_expended fixed the crashing bug
        if check_is_expended(ch):
            collect_children_unsafe(ch, scn)


    update_lock = False



def set_object_expended(j_obj):
    j_obj.data.expanded_obj = j_obj.name
    j_obj.draw_type = 'BOUNDS'

def set_object_collapsed(j_obj):
    if j_obj.data.expanded_obj == j_obj.name:
        j_obj.data.expanded_obj = ''

    #check to avoid rerendering
    if j_obj.draw_type != 'TEXTURED':
        j_obj.draw_type = 'TEXTURED'
        # if somebody hide bounding box
        j_obj.hide = False

def expand_objects(j_obj, scn):
    if j_obj is None:
        return

    global update_lock
    update_lock = True

    # if there is expended collapse it
    collapse_expanded(j_obj.data)


    # set current to expended
    set_object_expended(j_obj)

    # for o in bpy.data.objects:
    #     if o.data.is_sjoin:
    #         collect_children(o, scn)
    j_obj.select = False

    sj_objects = get_stored_sjobjects(j_obj.data)

    for o in sj_objects:
        link_stored(o, j_obj, scn)

    update_lock = False



def unlink_store(obj, sjoin_mesh):
    obj.use_fake_user = True
    obj.sjoin_mesh = sjoin_mesh.name

    # remove parent, and make transform relative to ex-parent

    for s in obj.users_scene[:]:
        s.objects.unlink(obj)

def link_stored(obj, sjoin_object, scn):
    if obj.name not in scn.objects:
        scn.objects.link(obj)

    scn.update()

    if not obj.parent:
        obj.parent = sjoin_object

    # always call fake_ser and sjoin_mesh together

    # this adds objects to local view
    obj.layers = sjoin_object.layers
    joiner.add_to_loc_view(obj, scn)

    obj.use_fake_user = False
    obj.sjoin_mesh = ''

    obj.select = True
    scn.objects.active = obj


from bpy.app.handlers import persistent


# looks like scene_update will be called by every operator in join_to_mesh update so I need to lock it
update_lock = False
@persistent
def scene_update(scene):
    # disable edit mode for sjoin objects

    global update_lock
    if update_lock:
        return
    update_lock = True
    active = scene.objects.active
    if check_is_sjoin_obj(scene.objects.active) and active.data.is_editmode:
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences
        if not addon_prefs.allow_edit_mode:
            bpy.ops.object.mode_set(mode='OBJECT')
        # this below won't always work??
        '''
        scene.update()
        bpy.ops.sjoin.expand()
        scene.update()
        '''

    object_update(active, scene)

    # this won't detect modifier updates
    # according to the wiki it should http://wiki.blender.org/index.php/Dev:2.6/Source/Render/UpdateAPI
    '''
    if bpy.data.objects.is_updated:
        for ob in scene.objects[:]:
            if ob.is_updated or ob.is_updated_data:
                object_update(ob, scene)
            # if not check_is_sjoin_obj(ob) and ob.data and ob.is_updated_data:
            #     print('updating object data for ', ob.data)
                # update_data_rec(ob.data)
    '''

    update_lock = False


def object_update(obj, scn):
    if check_is_sjoin_obj(obj):
        # update_lock = True
        check_fix_rename(obj.data, obj, scn)
        # recursive update could be added here but it might be slow for large scenes
        # update_lock = False

@persistent
def before_save(dummy):
    # don't save any meshes that have fake user because of sjoin if sjoin is deleted or has 0 users
    for o in bpy.data.objects:
        if o.sjoin_mesh != '':
            sjoin = get_sjmesh(o.sjoin_mesh)
            if not sjoin or not sjoin.is_sjoin:
                o.use_fake_user = False
                o.sjoin_mesh = ''
            else:
                o.use_fake_user = sjoin.users != 0