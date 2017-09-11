# Autor - Vladimir Pylev
# email - volodya.renderberg@gmail.com
# blog - http://clinicalfilm.blogspot.ru
# G+  - https://plus.google.com/u/0/115111937084055806830

# Important!!!
# to conduct the procedure for adding a group of helpers
# added group (with character rig) to the scene, to be at the origin of coordinates.

bl_info = {
    "name": "On Mesh Control",
    "description": "the establishment of controls attached to the mesh, but at the same time deform the mesh.",
    "author": "Vladimir Pylev",
    "version": (1, 0),
    "blender": (2, 77, 0),
    "location": "View3d tools panel",
    "warning": "",  # used for warning icon and text in addons panel
    "category": "Mesh"
}

import bpy
import mathutils
import math
import json
import webbrowser
# import os


class G(object):
    # panels
    to_group_panel = False
    to_armatures_panel = False

    # other
    h = 0.2
    hide_layer = [False] * 32
    hide_layer[29] = True
    control_layer = [False] * 32
    control_layer[20] = True
    mesh_layers = [False] * 20
    mesh_layers[19] = True
    helper_layer = [False] * 20
    helper_layer[18] = True

    removed_name = ''

    k = 0.7
    verts = (
        (1, 0, 0),
        (k, -k, 0),
        (0, -1, 0),
        (-k, -k, 0),
        (-1, 0, 0),
        (-k, k, 0),
        (0, 1, 0),
        (k, k, 0),
        (1, 0, 0),
        (k, 0, -k),
        (0, 0, -1),
        (-k, 0, -k),
        (-1, 0, 0),
        (-k, 0, k),
        (0, 0, 1),
        (k, 0, k),
        (1, 0, 0),
        (k, k, 0),
        (0, 1, 0),
        (0, k, -k),
        (0, 0, -1),
        (0, -k, -k),
        (0, -1, 0),
        (0, -k, k),
        (0, 0, 1),
        (0, k, k),
        (0, 1, 0),
    )

    def createMesh(self, name, verts, origin=(0, 0, 0), edges=[], faces=[]):
        if not edges:
            for i in range(0, (len(verts) - 1)):
                edges.append((i, i + 1))
            edges = tuple(edges)

        # Create mesh and object
        me = bpy.data.meshes.new(name + 'Mesh')
        ob = bpy.data.objects.new(name, me)
        ob.location = origin
        ob.show_name = True
        # Link object to scene
        bpy.context.scene.objects.link(ob)

        # Create mesh from given verts, edges, faces. Either edges or
        # faces should be [], or you ask for problems
        me.from_pydata(verts, edges, faces)

        # Update mesh with new data
        me.update(calc_edges=True)
        return ob


class ONMESH_main_panel(bpy.types.Panel):
    bl_idname = "on_mesh.main_panel"
    bl_label = "On Mesh Control"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("on_mesh.help", icon='QUESTION')
        layout.operator("on_mesh.make_control")
        layout.operator("on_mesh.remove_control", text='Remove Control')

        layout.label('Weight:')
        col = layout.column(align=True)
        col.operator("on_mesh.to_paint_weight")
        col.operator('on_mesh.edit_radius_of_influence')

        layout.label('Mirror (right to left):')
        col = layout.column(align=True)
        col.operator('on_mesh.mirror_control', text='Mirror Control')
        col.operator('on_mesh.mirror_weight_of_control', text='Mirror Weight')

        layout.label('Organization:')
        layout.operator("on_mesh.run_to_group_panel")


class ONMESH_to_group_panel(bpy.types.Panel):
    bl_idname = "on_mesh.to_group_panel"
    bl_label = "Select Group:"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"

    @classmethod
    def poll(self, context):
        if G.to_group_panel:
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        for group in bpy.data.groups:
            col.operator("on_mesh.append_to_group", text=group.name).name = group.name

        layout.operator("on_mesh.append_to_group", text='To All Groups').name = 'all'
        layout.operator("on_mesh.append_to_group", text='close').name = 'close'


class ONMESH_to_armatures_panel(bpy.types.Panel):
    bl_idname = "on_mesh.to_armatures_panel"
    bl_label = "Select Armature:"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"


    @classmethod
    def poll(self, context):
        if G.to_armatures_panel:
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        for ob in bpy.data.objects:
            if ob.type == 'ARMATURE':
                col.operator("on_mesh.create_to_selected_armatures", text=ob.name).name = ob.name

        layout.operator("on_mesh.create_to_selected_armatures", text='close').name = 'close'


class ONMESH_run_to_group_panel(bpy.types.Operator):
    bl_idname = "on_mesh.run_to_group_panel"
    bl_label = "Append To Group"

    def execute(self, context):
        G.to_group_panel = True
        return{'FINISHED'}


class ONMESH_append_to_group(bpy.types.Operator):
    bl_idname = "on_mesh.append_to_group"
    bl_label = "Append"

    name = bpy.props.StringProperty()

    def execute(self, context):
        if self.name == 'close':
            G.to_group_panel = False
            return{'FINISHED'}

        result, data = append_to_group(context, self.name)
        if result:
            self.report({'INFO'}, data)
            G.to_group_panel = False
        else:
            self.report({'WARNING'}, data)

        return{'FINISHED'}

#"on_mesh.to_armatures_add"


class ONMESH_create_to_selected_armatures(bpy.types.Operator):
    bl_idname = "on_mesh.create_to_selected_armatures"
    bl_label = "Append"

    name = bpy.props.StringProperty()

    def execute(self, context):
        if self.name == 'close':
            G.to_armatures_panel = False
            return{'FINISHED'}
        result, data = make_control(context, G.name, G.size, G.radius, armature=bpy.data.objects[self.name])
        if result:
            self.report({'INFO'}, data)
        else:
            self.report({'WARNING'}, data)
        G.to_armatures_panel = False
        return{'FINISHED'}


class ONMESH_make_control(bpy.types.Operator):
    bl_idname = "on_mesh.make_control"
    bl_label = "Make Control"

    name = bpy.props.StringProperty(name='name:')
    size = bpy.props.FloatProperty(name='bone size:', default=0.2)
    radius = bpy.props.FloatProperty(name='radius of influence:', default=2.0)

    def execute(self, context):
        if len(bpy.data.armatures) > 0:
            G.name = self.name
            G.size = self.size
            G.radius = self.radius
            G.to_armatures_panel = True
            return{'FINISHED'}

        result, data = make_control(context, self.name, self.size, self.radius)
        if result:
            self.report({'INFO'}, data)
        else:
            self.report({'WARNING'}, data)
        return{'FINISHED'}

    def invoke(self, context, event):
        # self.size = 0.2
        # self.radius = 2.0
        return context.window_manager.invoke_props_dialog(self)


class ONMESH_remove_control(bpy.types.Operator):
    bl_idname = "on_mesh.remove_control"
    bl_label = "You Are Sure?"

    deleted_name = bpy.props.StringProperty(name='delete this control?', default='')

    def execute(self, context):
        if not self.deleted_name:
            self.report({'WARNING'}, 'control is not selected!')
            return{'FINISHED'}
        result, data = remove_control(context)
        if result:
            self.report({'INFO'}, data)
        else:
            self.report({'WARNING'}, data)
        return{'FINISHED'}

    def invoke(self, context, event):
        pose = context.active_pose_bone
        if pose:
            self.deleted_name = pose.name
        else:
            self.deleted_name = ''
        return context.window_manager.invoke_props_dialog(self)


class ONMESH_to_paint_weight(bpy.types.Operator):
    bl_idname = "on_mesh.to_paint_weight"
    bl_label = "To Paint Weight"

    def execute(self, context):
        result, data = to_paint_weight(context)
        if result:
            self.report({'INFO'}, data)
        else:
            self.report({'WARNING'}, data)
        return{'FINISHED'}


class ONMESH_edit_radius_of_influence(bpy.types.Operator):
    bl_idname = "on_mesh.edit_radius_of_influence"
    bl_label = "Edit Radius Of Influence"

    radius = bpy.props.FloatProperty(name='radius of influence:', default=2.0)

    def execute(self, context):
        result, data = edit_radius_of_influence(context, self.radius)
        if result:
            self.report({'INFO'}, data)
        else:
            self.report({'WARNING'}, data)
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class ONMESH_mirror_control(bpy.types.Operator):
    bl_idname = "on_mesh.mirror_control"
    bl_label = "You Are Sure?"

    def execute(self, context):
        result, data = mirror_control(context)
        if result:
            self.report({'INFO'}, data)
        else:
            self.report({'WARNING'}, data)
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class ONMESH_mirror_weight_of_control(bpy.types.Operator):
    bl_idname = "on_mesh.mirror_weight_of_control"
    bl_label = "You Are Sure?"

    def execute(self, context):
        result, data = mirror_weight_of_control(context)
        if result:
            self.report({'INFO'}, data)
        else:
            self.report({'WARNING'}, data)
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class ONMESH_help(bpy.types.Operator):
    bl_idname = "on_mesh.help"
    bl_label = "Help"

    def execute(self, context):
        webbrowser.open_new_tab('https://sites.google.com/site/blenderfacialrig/onmesh-kontroly')
        return{'FINISHED'}


def append_to_group(context, group_name):
    if not bpy.data.armatures:
        return(False, 'Not Found Armatures!')
    # get data
    armature = context.object
    if 'OnMeshControls' in armature.data:
        OnMeshControls = json.loads(armature.data['OnMeshControls'])
    else:
        return(False, 'OnMeshControls not found! **')

    for key in OnMeshControls.keys():
        # get root object
        root_name = 'root.' + key
        if root_name not in bpy.data.objects:
            print(('object with name: ' + root_name + ' not found!'))
            continue
        root = bpy.data.objects[root_name]
        # get constraint object
        cns_to_mesh_name = 'constraint_to_mesh.' + key
        if cns_to_mesh_name not in bpy.data.objects:
            print(('object with name: ' + cns_to_mesh_name + ' not found!'))
            continue
        cns_to_mesh = bpy.data.objects[cns_to_mesh_name]

        objects = [root]

        # append objects to group
        if group_name == 'all':
            for group in bpy.data.groups:
                for ob in objects:
                    if ob.name not in group.objects:
                        group.objects.link(ob)
        else:
            group = bpy.data.groups[group_name]
            for ob in objects:
                if ob.name not in group.objects:
                    group.objects.link(ob)

    return(True, 'Ok!')


def make_control(context, name, size, radius, vtx_index=False, armature=False):
    data_dict = {'bones': [], 'objects': [], 'vertex_group': []}
    # test exists name
    name = name.replace(' ', '.')
    if name in bpy.data.objects.keys():
        return(False, 'This Name is Not Unique!')

    # test selected
    ob = bpy.context.object
    if not ob:
        return(False, 'Objet Not Selected!')
    elif ob.type != 'MESH':
        return(False, 'invalid object type!')
    elif ob.mode != 'EDIT' and not vtx_index:
        return(False, 'invalid object mode!')

    data_dict['deform_mesh'] = ob.name

    # Get selected vertex ***********************
    vertex = None
    v_co = None
    if not vtx_index:
        bpy.ops.object.mode_set(mode='OBJECT')
        for vtx in ob.data.vertices:
            if vtx.select:
                vertex = vtx
                v_co = vertex.co

        if not vertex:
            bpy.ops.object.mode_set(mode='EDIT')
            return(False, 'Not Selected Vertices!')
    else:
        vertex = ob.data.vertices[vtx_index]
        v_co = vertex.co

    # GET OPTIMAL VERTICES ****
    edges_keys = []
    for key in ob.data.edge_keys:
        if key[0] == vertex.index or key[1] == vertex.index:
            edges_keys.append(key)

    vertexes = []
    for key in edges_keys:
        for i in key:
            if i != vertex.index:
                vertexes.append(i)
                break

    # get
    optimal_vertices = [vertex.index]
    if len(vertexes) == 4:
        # new method
        optimal_vertices = [vertexes[0], vertexes[1], vertexes[2]]
        '''
		# old method
		pre = (vertex.index - 1)
		pos = (vertex.index + 1)
		if pre in vertexes and pos in vertexes:
			dist1 = get_dist(ob.data.vertices[pre].co, ob.data.vertices[pos].co)
			athers = []
			for i in vertexes:
				if i !=  pre and i !=  pos:
					athers.append(i)
			dist2 = get_dist(ob.data.vertices[athers[0]].co, ob.data.vertices[athers[1]].co)
			if dist2<dist1:
				optimal_vertices = [vertex.index, athers[0], athers[1]]
			else:
				optimal_vertices = [vertex.index, pos, pre]

			print(dist1, dist2)

		else:
			return(False, 'Deffective Topology! *** ')
		'''
    else:
        return(False, 'Deffective Topology! *** ')
    optimal_vertices = tuple(optimal_vertices)

    # get empty position
    ob_matrix = ob.matrix_world
    empty_pos = ob_matrix * v_co
    # print(empty_pos)

    '''
	# MAKE ROOT FOR EMPTIES
	EM_name = 'ON_MESH_EMPTIES'
	if not EM_name in bpy.data.objects.keys():
		EM_root = bpy.data.objects.new(EM_name, None)
		bpy.context.scene.objects.link(EM_root)
		EM_root.hide = True
	else:
		EM_root = bpy.data.objects[EM_name]
		EM_root.hide = True
	'''

    # Make Armature ****************************************
    # Make control Mesh
    name_mesh = 'mesh.' + name
    data_dict['objects'].append(name_mesh)
    mesh = G().createMesh(name_mesh, G().verts)
    mesh.layers = G().mesh_layers
    mesh.location = empty_pos
    mesh.scale = (size, size, size)

    # get exists Armature
    if not armature:
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE':
                armature = obj

        if not armature:
            arm = bpy.data.armatures.new('Armature')
            armature = bpy.data.objects.new('rig', arm)
            bpy.context.scene.objects.link(armature)
            bpy.types.Armature.OnMeshControls = bpy.props.StringProperty(name='OnMeshControls')
            arm.OnMeshControls = json.dumps({})

    armature.data.layers[20] = True
    armature.data.layers[29] = False

    # MAKE BONES
    bpy.context.scene.objects.active = armature
    # -- add StringProperty to Armature
    if not 'OnMeshControls' in armature.data:
        bpy.types.Armature.OnMeshControls = bpy.props.StringProperty(name='OnMeshControls')
        armature.data.OnMeshControls = json.dumps({})
    # -- add [IntProperty, FloatProperty] to PoseBone
    bpy.types.PoseBone.Vertex = bpy.props.IntProperty(name="Vertex")
    bpy.types.PoseBone.Radius = bpy.props.FloatProperty(name="Radius")
    bpy.types.PoseBone.Size = bpy.props.FloatProperty(name="Size")
    # to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    # -- exists bone
    if name in armature.data.edit_bones:
        bpy.ops.object.mode_set(mode='POSE')
        return(False, 'Already Exists!')
    # -- bones names
    root_bone_name = 'root.' + name
    offset_bone_name = 'offset.' + name
    reverse_bone_name = 'reverse.' + name
    data_dict['bones'] = [root_bone_name, offset_bone_name, reverse_bone_name, name]
    # -- root bone
    root_bone = armature.data.edit_bones.new(root_bone_name)
    root_bone.head = empty_pos
    root_bone.tail = (empty_pos[0], empty_pos[1], (empty_pos[2] + size))
    root_bone.roll = 0.0000
    root_bone.layers = G().hide_layer
    root_bone.use_deform = False
    root_bone.hide_select = True
    # -- offset bone
    offset_bone = armature.data.edit_bones.new(offset_bone_name)
    offset_bone.head = empty_pos
    offset_bone.tail = (empty_pos[0], empty_pos[1], (empty_pos[2] + size))
    offset_bone.roll = 0.0000
    offset_bone.parent = root_bone
    offset_bone.layers = G().hide_layer
    offset_bone.use_deform = False
    offset_bone.hide_select = True
    # -- reverse bone
    reverse_bone = armature.data.edit_bones.new(reverse_bone_name)
    reverse_bone.head = empty_pos
    reverse_bone.tail = (empty_pos[0], empty_pos[1], (empty_pos[2] + size))
    reverse_bone.roll = 0.0000
    reverse_bone.parent = offset_bone
    reverse_bone.layers = G().hide_layer
    reverse_bone.use_deform = False
    reverse_bone.hide_select = True
    # -- control_bone
    bone = armature.data.edit_bones.new(name)
    bone.head = empty_pos
    bone.tail = (empty_pos[0], empty_pos[1], (empty_pos[2] + size))
    bone.roll = 0.0000
    bone.parent = reverse_bone
    bone.layers = G().control_layer
    bone.use_deform = False
    bone.show_wire = True

    # CONSTRAINT to MESH *************************
    bpy.context.scene.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')
    root_pose = armature.pose.bones[root_bone_name]

    # write vertex.index to control_bone
    control_pose = armature.pose.bones[name]
    control_pose.Vertex = vertex.index
    control_pose.Radius = radius
    control_pose.Size = size
    control_pose.lock_rotation = (True, True, True)
    control_pose.lock_rotation_w = True
    # -- groups
    red_name = "Face.red.cnts"
    if red_name not in armature.pose.bone_groups:
        group = armature.pose.bone_groups.new(name=red_name)
        group.color_set = 'THEME01'
    else:
        group = armature.pose.bone_groups[red_name]
    control_pose.bone_group = group

    # NEW method
    # make empty
    cns_name = 'constraint_to_mesh.' + name
    data_dict['objects'].append(cns_name)
    cns_em = bpy.data.objects.new(cns_name, None)
    bpy.context.scene.objects.link(cns_em)
    cns_em.hide = True
    cns_em.hide_select = True
    cns_em.parent = ob
    cns_em.parent_type = 'VERTEX_3'
    cns_em.parent_vertices = optimal_vertices
    # -- location constraint
    # root_pose = armature.pose.bones[root_bone_name]
    cns = root_pose.constraints.new('COPY_LOCATION')
    cns.target_space = 'WORLD'
    cns.owner_space = 'WORLD'
    cns.target = cns_em
    # -- orient constraint
    cns = root_pose.constraints.new('COPY_ROTATION')
    cns.use_offset = True
    cns.target_space = 'WORLD'
    cns.owner_space = 'WORLD'
    cns.target = cns_em

    '''
	### OLD method
	# -- vertex group
	connect_grp_name = 'connect.' + name
	vertex_grp = ob.vertex_groups.new(connect_grp_name)
	vertex_grp.add([vertex.index], 1.0, 'REPLACE')
	# -- location constraint
	# root_pose = armature.pose.bones[root_bone_name]
	cns = root_pose.constraints.new('COPY_LOCATION')
	cns.target_space = 'WORLD'
	cns.owner_space = 'WORLD'
	cns.target = ob
	cns.subtarget = connect_grp_name
	# -- orient constraint
	cns = root_pose.constraints.new('COPY_ROTATION')
	cns.use_offset = True
	cns.target_space = 'WORLD'
	cns.owner_space = 'WORLD'
	cns.target = ob
	cns.subtarget = connect_grp_name
	'''

    # MAKE DEFORMER EMPTIES
    # -- root
    root_name = 'root.' + name
    data_dict['objects'].append(root_name)
    root_em = bpy.data.objects.new(root_name, None)
    bpy.context.scene.objects.link(root_em)
    root_em.hide = True
    root_em.hide_select = True
    root_em.location = empty_pos
    # root_em.parent = EM_root
    # -- control
    control_name = 'location.' + name
    data_dict['objects'].append(control_name)
    control_em = bpy.data.objects.new(control_name, None)
    bpy.context.scene.objects.link(control_em)
    control_em.hide = True
    control_em.hide_select = True
    control_em.parent = root_em
    # -- to_hook
    data_dict['objects'].append(name)
    hook_em = bpy.data.objects.new(name, None)
    bpy.context.scene.objects.link(hook_em)
    hook_em.hide = True
    hook_em.hide_select = True
    # control_em.parent = EM_root

    # -- ORIENT
    # -- constraint
    cns = root_em.constraints.new('COPY_ROTATION')
    cns.target_space = 'WORLD'
    cns.owner_space = 'WORLD'
    cns.target = armature
    cns.subtarget = root_bone_name
    # -- update affect
    bpy.ops.anim.update_animated_transform_constraints(use_convert_to_radians=True)
    # -- save matrix
    matrix = root_em.matrix_world
    v0 = tuple(matrix[0])
    v1 = tuple(matrix[1])
    v2 = tuple(matrix[2])
    v3 = tuple(matrix[3])
    m = mathutils.Matrix((mathutils.Vector(v0), mathutils.Vector(v1), mathutils.Vector(v2), mathutils.Vector(v3)))
    # -- remove constraint
    root_em.constraints.remove(cns)
    # -- apply matrix and position root
    root_em.matrix_world = m
    root_em.location = (0.0, 0.0, 0.0)
    # -- constrain to hook_em
    cns = hook_em.constraints.new('COPY_LOCATION')
    cns.target_space = 'WORLD'
    cns.owner_space = 'WORLD'
    cns.target = control_em

    # Mesh Shape
    bone_pose = armature.pose.bones[name]
    bone_pose.custom_shape = mesh

    # INVERSE
    space = 'LOCAL_SPACE'
    for key in [(0, 'LOC_X'), (1, 'LOC_Y'), (2, 'LOC_Z')]:
        # -- inverse X
        fcurve = armature.pose.bones[reverse_bone_name].driver_add('location', key[0])
        drv = fcurve.driver
        drv.type = 'SCRIPTED'
        drv.expression = 'var * -1'
        drv.show_debug_info = True
        # --- var
        var = drv.variables.new()
        var.name = 'var'
        var.type = 'TRANSFORMS'
        # --- targ
        targ = var.targets[0]
        targ.id = armature
        targ.transform_type = key[1]
        targ.bone_target = name
        targ.transform_space = space

    # return(True, 'Ok!')

    # make HOOK
    # -- driver to control
    space = 'LOCAL_SPACE'
    # for key in [(0, 'LOC_X', 'var'), (1, 'LOC_Z', 'var * -1'), (2, 'LOC_Y', 'var')]:
    for key in [(0, 'LOC_X', 'var'), (1, 'LOC_Y', 'var'), (2, 'LOC_Z', 'var')]:
        # -- inverse X
        fcurve = control_em.driver_add('location', key[0])
        drv = fcurve.driver
        drv.type = 'SCRIPTED'
        drv.expression = key[2]
        drv.show_debug_info = True
        # --- var
        var = drv.variables.new()
        var.name = 'var'
        var.type = 'TRANSFORMS'
        # --- targ
        targ = var.targets[0]
        targ.id = armature
        targ.transform_type = key[1]
        targ.bone_target = name
        targ.transform_space = space
    # -- make vertex group
    data_dict['vertex_group'].append(name)
    vtx_grp = ob.vertex_groups.new(name)
    for v in ob.data.vertices:
        r = radius * 0.05
        k = 20
        dist = ((v.co[0] - empty_pos[0])**2 + (v.co[1] - empty_pos[1])**2 + (v.co[2] - empty_pos[2])**2)**0.5
        if dist > (r * k):
            vtx_grp.add([v.index], 0.0, 'REPLACE')
        elif dist < r:
            vtx_grp.add([v.index], 1.0, 'REPLACE')
        else:
            a = r
            b = r * k
            weight = 1 - (a - dist) / (a - b)
            vtx_grp.add([v.index], weight, 'REPLACE')
    # -- make Hook
    bpy.context.scene.objects.active = ob
    hook = ob.modifiers.new(name, 'HOOK')
    hook.object = hook_em
    hook.vertex_group = name
    for mod in ob.modifiers:
        bpy.ops.object.modifier_move_up(modifier=name)

    # Apply data_dict
    current_dict = json.loads(armature.data['OnMeshControls'])
    current_dict[name] = data_dict
    # print(json.dumps(current_dict, sort_keys = True, indent = 4))
    armature.data['OnMeshControls'] = json.dumps(current_dict, sort_keys=True, indent=4)

    # to help layer
    cns_em.layers = G().helper_layer
    root_em.layers = G().helper_layer
    control_em.layers = G().helper_layer
    hook_em.layers = G().helper_layer

    return(True, 'Ok!')


def to_paint_weight(context):
    name = None
    removed_data = None

    pose = context.active_pose_bone
    armature = context.active_object

    if pose:
        name = pose.name
    else:
        return(False, 'control is not selected! ***')

    # get data
    if 'OnMeshControls' in armature.data:
        removed_data = json.loads(armature.data['OnMeshControls'])
    else:
        return(False, 'Removed data not found! ***')

    mesh_name = removed_data[name]['deform_mesh']
    if mesh_name not in bpy.data.objects:
        return(False, ('Mesh with name: ' + mesh_name + ' not found!'))

    ob = bpy.data.objects[mesh_name]
    if name not in ob.vertex_groups:
        return(False, 'Not Found Vertex Group!')

    vtx_grp = ob.vertex_groups[name]
    index = vtx_grp.index
    ob.vertex_groups.active_index = index

    context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

    return(True, ('Painting: ' + name))


def edit_radius_of_influence(context, radius):
    name = None
    removed_data = None
    vertex_index = None

    pose = context.active_pose_bone
    armature = context.active_object

    if pose:
        name = pose.name
        vertex_index = pose['Vertex']
        pose['Radius'] = radius
    else:
        return(False, 'control is not selected! ***')

    # get data
    if 'OnMeshControls' in armature.data:
        removed_data = json.loads(armature.data['OnMeshControls'])
    else:
        return(False, 'Removed data not found! ***')

    mesh_name = removed_data[name]['deform_mesh']
    if mesh_name not in bpy.data.objects:
        return(False, ('Mesh with name: ' + mesh_name + ' not found!'))

    ob = bpy.data.objects[mesh_name]
    if name not in ob.vertex_groups:
        return(False, 'Not Found Vertex Group!')

    vtx_grp = ob.vertex_groups[name]

    vertex = ob.data.vertices[vertex_index]
    ob_matrix = ob.matrix_world
    empty_pos = ob_matrix * vertex.co
    for v in ob.data.vertices:
        r = radius * 0.05
        k = 20
        dist = ((v.co[0] - empty_pos[0])**2 + (v.co[1] - empty_pos[1])**2 + (v.co[2] - empty_pos[2])**2)**0.5
        if dist > (r * k):
            vtx_grp.add([v.index], 0.0, 'REPLACE')
        elif dist < r:
            vtx_grp.add([v.index], 1.0, 'REPLACE')
        else:
            a = r
            b = r * k
            weight = 1 - (a - dist) / (a - b)
            vtx_grp.add([v.index], weight, 'REPLACE')

    return(True, 'Ok!')


def remove_control(context, contin=False):
    # get context data
    name = None
    removed_data = None

    pose = context.active_pose_bone
    armature = context.active_object
    if pose:
        name = pose.name
    else:
        return(False, 'control is not selected! ***')

    # get data
    if 'OnMeshControls' in armature.data:
        removed_data = json.loads(armature.data['OnMeshControls'])
    else:
        return(False, 'Removed data not found! ***')

    # removed keys: vertex_group, objects, bones
    # deformable: deform_mesh

    print(removed_data)
    # Remove Bones
    bpy.ops.object.mode_set(mode='EDIT')
    for bone_name in removed_data[name]['bones']:
        if bone_name in armature.data.edit_bones:
            bone = armature.data.edit_bones[bone_name]
            armature.data.edit_bones.remove(bone)
        else:
            print(('Not Found Bone: ' + bone_name))

    # Removed Hook
    mesh_name = removed_data[name]['deform_mesh']
    if mesh_name in bpy.data.objects:
        if name in bpy.data.objects[mesh_name].modifiers:
            hook = bpy.data.objects[mesh_name].modifiers[name]
            bpy.data.objects[mesh_name].modifiers.remove(hook)
        else:
            print('not Deleted modifier!')

        # Remove Vertex Group
        if name in bpy.data.objects[mesh_name].vertex_groups:
            vertex_grp = bpy.data.objects[mesh_name].vertex_groups[name]
            bpy.data.objects[mesh_name].vertex_groups.remove(vertex_grp)
        else:
            print('not Deleted vertex group!')

    # Remove Animation Data of objects
    for ob_name in removed_data[name]['objects']:
        if ob_name not in bpy.data.objects:
            print(('object with name \"' + ob_name + '\" - not found!'))
            continue

        ob = bpy.data.objects[ob_name]
        ob.driver_remove('location')

        # Removed Constraints
        if ob.constraints:
            for cns in ob.constraints:
                ob.constraints.remove(cns)

    # Removed Objects:
    for ob_name in removed_data[name]['objects']:
        if ob_name not in bpy.data.objects:
            print(('object with name \"' + ob_name + '\" - not found!'))
            continue

        # print(ob_name)
        ob = bpy.data.objects[ob_name]

        # Unlink Ob
        for scene in bpy.data.scenes:
            if ob_name in scene.objects:
                scene.objects.unlink(ob)
        for group in bpy.data.groups:
            if ob_name in group.objects:
                group.objects.unlink(ob)
        try:
            bpy.data.objects.remove(ob)
        except:
            print(('Not Deleted - ' + ob_name))

    # Clear removed_data
    del(removed_data[name])
    armature.data['OnMeshControls'] = json.dumps(removed_data)

    bpy.ops.object.mode_set(mode='POSE')

    return(True, name)


def mirror_control(context):
    name = None
    left_name = None
    OnMeshControls = None
    vertex_index = None
    radius = None
    size = None

    pose = context.active_pose_bone
    armature = context.active_object

    if pose:
        name = pose.name
        vertex_index = pose['Vertex']
        radius = pose['Radius']
        size = pose['Size']
    else:
        return(False, 'control is not selected! ***')

    # NAME TEST
    if name[-2:] == '.r':
        left_name = name[:-1] + 'l'
    elif name[-2:] == '.R':
        left_name = name[:-1] + 'L'
    else:
        return(False, 'this is not the right of \"control\"!')

    if left_name in bpy.data.objects:
        return(False, 'already exists!')

    # get OnMeshControls data
    if 'OnMeshControls' in armature.data:
        OnMeshControls = json.loads(armature.data['OnMeshControls'])
    else:
        return(False, 'Removed data not found! ***')

    # get mesh
    mesh_name = OnMeshControls[name]['deform_mesh']
    if mesh_name not in bpy.data.objects:
        return(False, ('Mesh with name: ' + mesh_name + ' not found!'))
    mesh = bpy.data.objects[mesh_name]

    # get mirror vertex_index
    v = mesh.data.vertices[vertex_index]
    if v.co[0] == 0.0:
        return(False, 'This Is Control of Middle!')
    # -- mirror co
    m_co = (-v.co[0], v.co[1], v.co[2])

    # -- get near mirror vertex
    dist = abs(v.co[0]) * 2
    m_v = v
    for vtx in mesh.data.vertices:
        # d = ((vtx.co[0] - m_co[0])**2 + (vtx.co[1] - m_co[1])**2 + (vtx.co[2] - m_co[2])**2)**0.5
        d = get_dist(vtx.co, m_co)
        if d < dist:
            dist = d
            m_v = vtx
        else:
            continue

    if vertex_index == m_v.index:
        return(False, 'This Is Control of Middle!')

    # Make Control
    context.scene.objects.active = mesh
    result, data = make_control(context, left_name, size, radius, vtx_index=m_v.index, armature=armature)
    if not result:
        return(False, data)

    result, data = mirror_weight_of_control(context, name=name, left_name=left_name, armature=armature)
    if not result:
        return(False, data)

    return(True, ('mirror: ' + name + ' to ' + left_name))


def mirror_weight_of_control(context, name=None, left_name=None, armature=None):
    if not armature:
        ob = context.object
    else:
        ob = armature

    if ob.type != 'ARMATURE':
        return(False, 'invalid object type!')
    pose = context.active_pose_bone

    if not name:
        # GET NAME
        if pose:
            name = pose.name
        else:
            return(False, 'Not Found Selected Control!')

    if not left_name:
        # GET LEFT NAME
        if name[-2:] == '.r':
            left_name = name[:-2] + '.l'
        elif name[-2:] == '.R':
            left_name = name[:-2] + '.L'
        else:
            return(False, 'Only Right to Left!')

    # GET MESH
    OnMeshControls = json.loads(ob.data['OnMeshControls'])
    mesh_name = OnMeshControls[name]['deform_mesh']
    mesh = bpy.data.objects[mesh_name]

    # Get Vertex Groups
    r_vertex_group_name = OnMeshControls[name]['vertex_group'][0]
    r_vertex_group = mesh.vertex_groups[r_vertex_group_name]
    l_vertex_group_name = OnMeshControls[left_name]['vertex_group'][0]
    l_vertex_group = mesh.vertex_groups[l_vertex_group_name]

    # Mirror WEIGHTs
    for v in mesh.data.vertices:
        dist = abs(v.co[0]) * 2
        m_co = (-v.co[0], v.co[1], v.co[2])
        m_v = v
        # get mirror vertex
        for vtx in mesh.data.vertices:
            d = get_dist(vtx.co, m_co)
            if d < dist:
                dist = d
                m_v = vtx
            else:
                continue
        # get weight
        l_vertex_group.add([m_v.index], 0, 'REPLACE')
        # continue
        try:
            weight = r_vertex_group.weight(v.index)
            l_vertex_group.add([m_v.index], weight, 'REPLACE')
        except:
            l_vertex_group.add([m_v.index], 0, 'REPLACE')

    return(True, 'Ok!')


def get_dist(co1, co2):
    dist = math.sqrt(math.pow((co1[0] - co2[0]), 2) + math.pow((co1[1] - co2[1]), 2) + math.pow((co1[2] - co2[2]), 2))
    return(dist)


def register():
    bpy.utils.register_class(ONMESH_main_panel)
    bpy.utils.register_class(ONMESH_run_to_group_panel)
    bpy.utils.register_class(ONMESH_to_armatures_panel)
    bpy.utils.register_class(ONMESH_make_control)
    bpy.utils.register_class(ONMESH_remove_control)
    bpy.utils.register_class(ONMESH_to_paint_weight)
    bpy.utils.register_class(ONMESH_edit_radius_of_influence)
    bpy.utils.register_class(ONMESH_to_group_panel)
    bpy.utils.register_class(ONMESH_append_to_group)
    bpy.utils.register_class(ONMESH_mirror_control)
    bpy.utils.register_class(ONMESH_mirror_weight_of_control)
    bpy.utils.register_class(ONMESH_create_to_selected_armatures)
    bpy.utils.register_class(ONMESH_help)


def unregister():
    bpy.utils.unregister_class(ONMESH_main_panel)
    bpy.utils.unregister_class(ONMESH_run_to_group_panel)
    bpy.utils.unregister_class(ONMESH_to_armatures_panel)
    bpy.utils.unregister_class(ONMESH_make_control)
    bpy.utils.unregister_class(ONMESH_remove_control)
    bpy.utils.unregister_class(ONMESH_to_paint_weight)
    bpy.utils.unregister_class(ONMESH_edit_radius_of_influence)
    bpy.utils.unregister_class(ONMESH_to_group_panel)
    bpy.utils.unregister_class(ONMESH_append_to_group)
    bpy.utils.unregister_class(ONMESH_mirror_control)
    bpy.utils.unregister_class(ONMESH_mirror_weight_of_control)
    bpy.utils.unregister_class(ONMESH_create_to_selected_armatures)
    bpy.utils.unregister_class(ONMESH_help)

if __name__ == "__main__":
    register()
