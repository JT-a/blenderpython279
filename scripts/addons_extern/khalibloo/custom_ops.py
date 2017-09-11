# <pep8 compliant>
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


import bpy
import os

working_dir = os.path.dirname(__file__)
bpy.types.Scene.khalibloo_opblocks = []
indentLevel = 0

#FILTERS ORDER
#filter_mesh = 0
#filter_curve = 1
#filter_armature = 2
#filter_surface = 3
#filter_meta = 4
#filter_camera = 5
#filter_lamp = 6
#filter_speaker = 7
#filter_font = 8
#filter_lattice = 9
#filter_empty = 10

template_imp_bpy = "import bpy\n"
template_imp_init = "from khalibloo import custom_ops\n"

template_opblock_remove01 = "class OperatorBlock"
template_opblock_remove02 = "Remove(bpy.types.Operator):\n    \"\"\"Remove operator block\"\"\"\n    bl_idname = \"object.khalibloo_opblock"
template_opblock_remove03 = "_remove\"\n    bl_label = \"Remove Operator Block\"\n    @classmethod\n    def poll(cls, context):\n        return True\n    def execute(self, context):\n        for opblock in context.scene.khalibloo_opblocks:\n            if (opblock != None):\n                if (opblock.index == "
template_opblock_remove04 = "):\n                    custom_ops.deleteOpblock(opblock)\n                    break\n        del bpy.types.Scene.khalibloo_opblock"
template_opblock_remove05 = "_action\n        del bpy.types.Scene.khalibloo_opblock"
template_opblock_remove06 = "_action_mode\n        return {'FINISHED'}\nbpy.utils.register_class(OperatorBlock"
template_opblock_remove07 = "Remove)"

template_opblock_moveup01 = "class OperatorBlock"
template_opblock_moveup02 = "MoveUp(bpy.types.Operator):\n    \"\"\"Move operator block Up\"\"\"\n    bl_idname = \"object.khalibloo_opblock"
template_opblock_moveup03 = "_move_up\"\n    bl_label = \"Move Operator Block Up\"\n    @classmethod\n    def poll(cls, context):\n        return True\n    def execute(self, context):\n        for opblock in context.scene.khalibloo_opblocks:\n            if (opblock != None):\n                if (opblock.index == "
template_opblock_moveup04 = "):\n                    block = opblock\n                    break\n        custom_ops.moveOpblock(opblock=block, direction='UP')\n        return {'FINISHED'}\nbpy.utils.register_class(OperatorBlock"
template_opblock_moveup05 = "MoveUp)"

template_opblock_movedown01 = "class OperatorBlock"
template_opblock_movedown02 = "MoveDown(bpy.types.Operator):\n    \"\"\"Move operator block Down\"\"\"\n    bl_idname = \"object.khalibloo_opblock"
template_opblock_movedown03 = "_move_down\"\n    bl_label = \"Move Operator Block Down\"\n    @classmethod\n    def poll(cls, context):\n        return True\n    def execute(self, context):\n        for opblock in context.scene.khalibloo_opblocks:\n            if (opblock != None):\n                if (opblock.index == "
template_opblock_movedown04 = "):\n                    block = opblock\n                    break\n        custom_ops.moveOpblock(opblock=block, direction='DOWN')\n        return {'FINISHED'}\nbpy.utils.register_class(OperatorBlock"
template_opblock_movedown05 = "MoveDown)"

template_opblock_action_mode_pre = "bpy.types.Scene."
template_opblock_action_mode_post = " = bpy.types.Scene.khalibloo_opblock_action_mode\n"

template_opblock_action_pre = "bpy.types.Scene."
template_opblock_action_post = " = bpy.types.Scene.khalibloo_opblock_action\n"


def updateBlockActionMode(block):
    block.updateActionMode(bpy.context)

def updateBlockAction(block):
    block.updateAction(bpy.context)

template_prep_obj_type_filters = "obj_type_filters = []\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[0]):\n    obj_type_filters.append('MESH')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[1]):\n    obj_type_filters.append('CURVE')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[2]):\n    obj_type_filters.append('ARMATURE')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[3]):\n    obj_type_filters.append('SURFACE')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[4]):\n    obj_type_filters.append('META')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[5]):\n    obj_type_filters.append('CAMERA')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[6]):\n    obj_type_filters.append('LAMP')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[7]):\n    obj_type_filters.append('SPEAKER')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[8]):\n    obj_type_filters.append('FONT')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[9]):\n    obj_type_filters.append('LATTICE')\nif (bpy.context.scene.khalibloo_ops_obj_type_filters[10]):\n    obj_type_filters.append('EMPTY')\n"
template_target_is_obj = "target = obj\n"
template_obj_as_active = "bpy.context.scene.objects.active = obj\n"
template_scope_actions = "for obj in bpy.data.actions:\n"
template_scope_groups = "for obj in bpy.data.groups:\n"
template_scope_images = "for obj in bpy.data.images:\n"
template_scope_linestyles = "for obj in bpy.data.linestyles:\n"
template_scope_materials = "for obj in bpy.data.materials:\n"
template_scope_obj_all_mats_01 = "for slot in obj.material_slots:\n"
template_scope_obj_all_mats_02 = "obj = slot.material\n"
template_scope_obj_active_mat = "obj = obj.active_material\n"
template_scope_movieclips = "for obj in bpy.data.movieclips:\n"
template_scope_selected_objects = "for obj in bpy.context.selected_objects:\n"
template_scope_all_objects = "for obj in bpy.data.objects:\n"
template_scope_scene_objects = "for obj in bpy.context.scene.objects:\n"
template_scope_active_object = "obj = bpy.context.active_object\n"
template_scope_obj_type_filters = "if (obj.type in obj_type_filters):\n"
template_scope_all_modifiers = "for obj in obj.modifiers:\n"
template_scope_specific_modifier_01 = "for obj in obj.modifiers:\n"
template_scope_specific_modifier_02 = "if (obj.type == '"
template_scope_specific_modifier_03 = "'):\n"
template_scope_all_constraints = "for obj in obj.constraints:\n"
template_scope_specific_constraint_01 = "for obj in obj.constraints:\n"
template_scope_specific_constraint_02 = "if (obj.type == '"
template_scope_specific_constraint_03 = "'):\n"
template_scope_all_vgroups = "for obj in obj.vertex_groups:\n"
template_scope_active_vgroup = "obj = obj.vertex_groups.active\n"
template_scope_all_shape_keys = "for obj in obj.data.shape_keys.key_blocks:\n"
template_scope_active_shape_key = "obj = obj.active_shape_key\n"
template_scope_all_uvmaps = "for obj in obj.data.uv_textures:\n"
template_scope_active_uvmap = "obj = obj.data.uv_textures.active\n"
template_scope_all_vcols = "for obj in obj.data.vertex_colors:\n"
template_scope_active_vcols = "obj = obj.data.vertex_colors.active\n"
template_scope_all_particle_systems = "for obj in obj.particle_systems:\n"
#template_scope_active_particle_system = "obj = obj.particle_systems.active\n"
template_scope_all_scenes = "for obj in bpy.data.scenes:\n"
template_scope_current_scene = "obj = bpy.context.scene\n"
template_scope_render = "obj = obj.render\n"
template_scope_sounds = "for obj in bpy.data.sounds:\n"
template_scope_texts = "for obj in bpy.data.texts:\n"
template_scope_textures = "for obj in bpy.data.textures:\n"
template_scope_all_textures = "for obj in obj.texture_slots:\n"
template_scope_active_texture = "obj = obj.active_texture\n"
#template_scope_enabled_textures = "for tex in obj.textures:\nif (obj.use_textures[X])"
#template_scope_disabled_textures = ""
template_scope_all_worlds = "for obj in bpy.data.worlds:\n"
template_scope_current_world = "obj = bpy.context.scene.world\n"
template_set_mode_pre = "bpy.ops.object.mode_set(mode='"
template_set_mode_post = "')\n"


def executeProp(context):
    scene = context.scene
    output = []
    global indentLevel
    indentLevel = 0

    datatype = scene.khalibloo_ops_datatype
    obj_subtype = scene.khalibloo_ops_obj_subtype
    mat_subtype_01 = scene.khalibloo_ops_mat_subtype_01
    mat_subtype_02 = scene.khalibloo_ops_mat_subtype_02
    mod_subtype = scene.khalibloo_ops_mod_subtype
    const_subtype = scene.khalibloo_ops_const_subtype
    scene_subtype = scene.khalibloo_ops_scene_subtype
    mod_scope = scene.khalibloo_ops_mod_scope
    const_scope = scene.khalibloo_ops_const_scope
    scope01 = scene.khalibloo_ops_scope01
    scope02 = scene.khalibloo_ops_scope02
    scope03 = scene.khalibloo_ops_scope03
    scope04_01 = scene.khalibloo_ops_scope04_01
    scope04_02 = scene.khalibloo_ops_scope04_02
    scope05 = scene.khalibloo_ops_scope05

    #import bpy
    output.append(template_imp_bpy)
    #ACTIONS
    if (datatype == 'ACTIONS'): # All actions
        output.append(template_scope_actions)
        indentLevel += 1
        #output.append(autoIndent(template_target_is_obj))
    #GROUPS
    elif (datatype == 'GROUPS'): # All groups
        output.append(template_scope_groups)
        indentLevel += 1
        #output.append(autoIndent(template_target_is_obj))
    #IMAGES
    elif (datatype == 'IMAGES'): # All images
        output.append(template_scope_images)
        indentLevel += 1
        #output.append(autoIndent(template_target_is_obj))
    #LINESTYLES
    elif (datatype == 'LINESTYLES'): # All linestyles
        output.append(template_scope_linestyles)
        indentLevel += 1
        #output.append(autoIndent(template_target_is_obj))
    #MATERIALS
    elif (datatype == 'MATERIALS'): # All materials
        output.append(template_scope_materials)
        indentLevel += 1
        #output.append(autoIndent(template_target_is_obj))
    #MOVIECLIPS
    elif (datatype == 'MOVIECLIPS'): # All movieclips
        output.append(template_scope_movieclips)
        indentLevel += 1
        #output.append(autoIndent(template_target_is_obj))
    #OBJECTS
    elif (datatype == 'OBJECTS'):
        if (context.scene.khalibloo_ops_use_obj_type_filters): #If filters are enabled
            output.append(template_prep_obj_type_filters)
        if (scope03 == 'ALL'): # All objects
            output.append(template_scope_all_objects)
            indentLevel += 1
            #output.append(autoIndent(template_target_is_obj))
        elif (scope03 == 'SELECTED'): # Selected objects
            output.append(template_scope_selected_objects)
            indentLevel += 1
            #output.append(autoIndent(template_target_is_obj))
        elif (scope03 == 'SCENE'): # Scene objects
            output.append(template_scope_scene_objects)
            indentLevel += 1
            #output.append(autoIndent(template_target_is_obj))
        elif (scope03 == 'ACTIVE'): # Active object
            output.append(template_scope_active_object)
            #output.append(autoIndent(template_target_is_obj))
        if (context.scene.khalibloo_ops_use_obj_type_filters): #If filters are enabled
            output.append(autoIndent(template_scope_obj_type_filters))
            indentLevel += 1
        #OBJ SUBTYPES
        #OBJ MATERIALS
        if (obj_subtype == 'MATERIALS'):
            if (scope01 == 'ALL'): # All materials
                output.append(autoIndent(template_scope_obj_all_mats_01))
                indentLevel += 1
                output.append(autoIndent(template_scope_obj_all_mats_02))
                #output.append(autoIndent(template_target_is_obj))
            elif (scope01 == 'ACTIVE'): # Active material
                output.append(autoIndent(template_scope_obj_active_mat))
                #output.append(autoIndent(template_target_is_obj))
            #OBJ MAT TEXTURES
            if (mat_subtype_01 == 'TEXTURES'):
                if (scope04_01 == 'ALL'): # All textures
                    output.append(autoIndent(template_scope_all_textures))
                    indentLevel += 1
                    #output.append(autoIndent(template_target_is_obj))
                elif (scope04_01 == 'ACTIVE'): # Active textures
                    output.append(autoIndent(template_scope_active_texture))
                    #output.append(autoIndent(template_target_is_obj))
                elif (scope04_01 == 'ENABLED'): # Enabled textures
                    output.append(autoIndent(template_scope_enabled_textures))
                    #output.append(autoIndent(template_target_is_obj))
                elif (scope04_01 == 'DISABLED'): # Disabled textures
                    output.append(autoIndent(template_scope_disabled_textures))
                    #output.append(autoIndent(template_target_is_obj))
        #OBJ MODIFIERS
        elif (obj_subtype == 'MODIFIERS'):
            if (mod_scope == 'ALL'): # All modifiers
                output.append(autoIndent(template_scope_all_modifiers))
                indentLevel += 1
                #output.append(autoIndent(template_target_is_obj))
            else: # Specific modifier
                # TODO: for modifier of type XXX
                output.append(autoIndent(template_scope_specific_modifier_01))
                indentLevel += 1
                output.append(autoIndent(template_scope_specific_modifier_02 + mod_subtype + template_scope_specific_modifier_03))
                indentLevel += 1
        #OBJ CONSTRAINTS
        elif (obj_subtype == 'CONSTRAINTS'):
            if (const_scope == 'ALL'):
                output.append(autoIndent(template_scope_all_constraints))
                indentLevel += 1
                #output.append(autoIndent(template_target_is_obj))
            else:
                # TODO: for constraint of type XXX
                output.append(autoIndent(template_scope_specific_constraint_01))
                indentLevel += 1
                output.append(autoIndent(template_scope_specific_constraint_02 + const_subtype + template_scope_specific_constraint_03))
                indentLevel += 1
        #OBJ VERTEX GROUPS
        elif (obj_subtype == 'VERTEX_GROUPS'):
            if (scope01 == 'ALL'): # All vertex groups
                output.append(autoIndent(template_scope_all_vgroups))
                indentLevel += 1
                #output.append(autoIndent(template_target_is_obj))
            elif (scope01 == 'ACTIVE'): # Active vertex groups
                output.append(autoIndent(template_scope_active_vgroup))
                #output.append(autoIndent(template_target_is_obj))
        #OBJ SHAPE KEYS
        elif (obj_subtype == 'SHAPE_KEYS'):
            if (scope01 == 'ALL'): # All shape keys
                output.append(autoIndent(template_scope_all_shape_keys))
                indentLevel += 1
                #output.append(autoIndent(template_target_is_obj))
            elif (scope01 == 'ACTIVE'): # Active shape keys
                output.append(autoIndent(template_scope_active_shape_key))
                #output.append(autoIndent(template_target_is_obj))
        #OBJ UV MAPS
        elif (obj_subtype == 'UV_MAPS'):
            if (scope01 == 'ALL'): # All uv maps
                output.append(autoIndent(template_scope_all_uvmaps))
                indentLevel += 1
                #output.append(autoIndent(template_target_is_obj))
            elif (scope01 == 'ACTIVE'): # Active uv maps
                output.append(autoIndent(template_scope_active_uvmap))
                #output.append(autoIndent(template_target_is_obj))
        #OBJ VERTEX COLORS
        elif (obj_subtype == 'VERTEX_COLORS'):
            if (scope01 == 'ALL'): # All vertex colors
                output.append(autoIndent(template_scope_all_vcols))
                indentLevel += 1
                #output.append(autoIndent(template_target_is_obj))
            elif (scope01 == 'ACTIVE'): # Active vertex colors
                output.append(autoIndent(template_scope_active_vcols))
                #output.append(autoIndent(template_target_is_obj))
        #OBJ PARTICLE SYSTEMS
        elif (obj_subtype == 'PARTICLE_SYSTEMS'): # All particle systems
            output.append(autoIndent(template_scope_all_particle_systems))
            indentLevel += 1
            #output.append(autoIndent(template_target_is_obj))
    #SCENES
    elif (datatype == 'SCENES'):
        if (scope05 == 'ALL'):
            output.append(template_scope_all_scenes)
            indentLevel += 1
            #output.append(autoIndent(template_target_is_obj))
        elif (scope05 == 'CURRENT'):
            output.append(template_scope_active_scene)
            #output.append(autoIndent(template_target_is_obj))
        #SCENE SUBTYPES
        #SCENE RENDER
        if (scene_subtype == 'RENDER'):
            output.append(template_scope_render) # obj = obj.render
            #output.append(autoIndent(template_target_is_obj))
    #SOUNDS
    elif (datatype == 'SOUNDS'): # All sounds
        output.append(template_scope_sounds)
        indentLevel += 1
        #output.append(autoIndent(template_target_is_obj))
    #TEXTS
    elif (datatype == 'TEXTS'): # All texts
        output.append(template_scope_texts)
        indentLevel += 1
        #output.append(autoIndent(template_target_is_obj))
    #TEXTURES
    elif (datatype == 'TEXTURES'): # All textures
        output.append(template_scope_textures)
        indentLevel += 1
        #output.append(autoIndent(template_target_is_obj))
    #WORLDS
    elif (datatype == 'WORLDS'):
        if (scope05 == 'ALL'):
            output.append(template_scope_all_worlds)
            indentLevel += 1
            #output.append(autoIndent(template_target_is_obj))
        elif (scope05 == 'CURRENT'):
            output.append(template_scope_current_world)
            #output.append(autoIndent(template_target_is_obj))
    return output

def deleteOpblock(opblock):
    scene = bpy.context.scene
    index = scene.khalibloo_opblocks.index(opblock)
    scene.khalibloo_opblocks[index] = None #fill slot with a useless value

def moveOpblock(opblock, direction): # direction: 'UP' or 'DOWN'
    scene = bpy.context.scene
    indexA = scene.khalibloo_opblocks.index(opblock)
    indexB = indexA # copy for iteration
    a = scene.khalibloo_opblocks[indexA]
    b = 0
    if ((indexB > 0) and (direction == 'UP')):
        searching = True
        while(searching):
            indexB -= 1
            if (indexB == 0): # beginning of the list
                searching = False
            if (scene.khalibloo_opblocks[indexB] != None):
                b = scene.khalibloo_opblocks[indexB]
                searching = False
        if (b):
            scene.khalibloo_opblocks[indexA] = b
            scene.khalibloo_opblocks[indexB] = a
    elif ((indexB < len(scene.khalibloo_opblocks)-1) and (direction == 'DOWN')):
        searching = True
        while(searching):
            indexB += 1
            if (indexB == len(scene.khalibloo_opblocks)-1): # end of the list
                searching = False
            if (scene.khalibloo_opblocks[indexB] != None):
                b = scene.khalibloo_opblocks[indexB]
                searching = False
        if (b):
            scene.khalibloo_opblocks[indexA] = b
            scene.khalibloo_opblocks[indexB] = a

def autoIndent(string):
    indent = "    "
    indent *= indentLevel
    result = indent + string
    return result

def runScript(text):
    filepath = os.path.join(working_dir, "temp.py")
    try:
        os.mkdir(working_dir)
    except(FileExistsError):
        pass
    try:
        os.remove(filepath)
    except(FileNotFoundError):
        pass
    file = open(filepath, mode='x')
    file.write(text)
    file.close()
    bpy.ops.script.python_file_run(filepath=filepath)

class OperatorBlock():

    def __init__(self, context, index):
        self.name = "Operator Block"
        self.index = index
        self.strIndex = str(self.index)
        self.prefix = "khalibloo_opblock" + self.strIndex + "_"
        self.action = ""
        self.actionMode = 'OBJECT'
        #action mode
        runScript(template_imp_bpy + template_opblock_action_mode_pre + self.prefix + "action_mode" + template_opblock_action_mode_post)
        #action
        runScript(template_imp_bpy + template_opblock_action_pre + self.prefix + "action" + template_opblock_action_post)
        #delete operator
        runScript(template_imp_bpy + template_imp_init + template_opblock_remove01 + self.strIndex + template_opblock_remove02 + self.strIndex + template_opblock_remove03 + self.strIndex + template_opblock_remove04 + self.strIndex + template_opblock_remove05 + self.strIndex + template_opblock_remove06 + self.strIndex + template_opblock_remove07)
        #move operators
        runScript(template_imp_bpy + template_imp_init + template_opblock_moveup01 + self.strIndex + template_opblock_moveup02 + self.strIndex + template_opblock_moveup03 + self.strIndex + template_opblock_moveup04 + self.strIndex + template_opblock_moveup05)
        runScript(template_imp_bpy + template_imp_init + template_opblock_movedown01 + self.strIndex + template_opblock_movedown02 + self.strIndex + template_opblock_movedown03 + self.strIndex + template_opblock_movedown04 + self.strIndex + template_opblock_movedown05)

    def updateActionMode(self, context):
        runScript("import bpy\nbpy.context.scene.khalibloo_opblocks["+self.strIndex+"].actionMode = bpy.context.scene." + self.prefix + "action_mode\n")

    def updateAction(self, context):
        runScript("import bpy\nbpy.context.scene.khalibloo_opblocks["+self.strIndex+"].action = bpy.context.scene." + self.prefix + "action\n")


class OperatorBlockAdd(bpy.types.Operator):
    """Add new operator block"""
    bl_idname = "object.khalibloo_opblock_add"
    bl_label = "Add Operator Block"


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        newOpBlock = OperatorBlock(context, index=context.scene.khalibloo_custom_ops_current_index)
        context.scene.khalibloo_opblocks.append(newOpBlock)
        context.scene.khalibloo_custom_ops_current_index += 1
        return {'FINISHED'}


class OperatorsExecute(bpy.types.Operator):
    """Execute operator blocks"""
    bl_idname = "object.khalibloo_opblocks_execute"
    bl_label = "Execute Operator Blocks"


    @classmethod
    def poll(cls, context):
        for block in context.scene.khalibloo_opblocks:
            if (block != None):
                return True
        return False

    def execute(self, context):
        scene = context.scene
        output = []
        action = ""
        global indentLevel
        indentLevel = 0
        previous_block_type = 'NONE' #NONE, PROP, OP

        #output.append(template_imp_bpy)
        output = executeProp(context)
        for block in scene.khalibloo_opblocks:
            if (block != None):
                block.updateActionMode(context)
                block.updateAction(context)
                if (block.action.startswith("bpy.ops.")): # Our block is an op block
                    #if (previous_block_type != 'OP'):
                    #    output.append(executeProp(context))
                    #set obj as active
                    output.append(autoIndent(template_obj_as_active))
                    #set mode
                    output.append(autoIndent(template_set_mode_pre + block.actionMode + template_set_mode_post))
                    #carryout action
                    output.append(autoIndent(block.action + "\n"))
                    previous_block_type = 'OP'
                else:
                    #if (previous_block_type != 'PROP'): # Our block is a prop block
                        #output.append(executeProp(context))
                    #SET MODE
                    output.append(autoIndent(template_set_mode_pre + block.actionMode + template_set_mode_post))
                    #ACTION
                    output.append(autoIndent("obj." + block.action + "\n"))
                    previous_block_type = 'PROP'
        action = action.join(output)
        print(action)
        runScript(action)
        return {'FINISHED'}


def initialize():
    bpy.types.Scene.khalibloo_custom_ops_current_index = bpy.props.IntProperty()
    bpy.types.Scene.khalibloo_ops_mod_subtype = bpy.props.EnumProperty(items =(
                                             #Modify
                                             ('MESH_CACHE', 'Mesh Cache', '', 'MOD_MESHDEFORM', 0),
                                             ('UV_PROJECT', 'UV Project', '', 'MOD_UVPROJECT', 1),
                                             ('UV_WARP', 'UV Warp', '', 'MOD_UVPROJECT', 2),
                                             ('VERTEX_WEIGHT_EDIT', 'Vertex Weight Edit', '', 'MOD_VERTEX_WEIGHT', 3),
                                             ('VERTEX_WEIGHT_MIX', 'Vertex Weight Mix', '', 'MOD_VERTEX_WEIGHT', 4),
                                             ('VERTEX_WEIGHT_PROXIMITY', 'Vertex Weight Proximity', '', 'MOD_VERTEX_WEIGHT', 5),
                                             #Generate
                                             ('ARRAY', 'Array', '', 'MOD_ARRAY', 6),
                                             ('BEVEL', 'Bevel', '', 'MOD_BEVEL', 7),
                                             ('BOOLEAN', 'Boolean', '', 'MOD_BOOLEAN', 8),
                                             ('BUILD', 'Build', '', 'MOD_BUILD', 9),
                                             ('DECIMATE', 'Decimate', '', 'MOD_DECIM', 10),
                                             ('EDGE_SPLIT', 'Edge Split', '', 'MOD_EDGESPLIT', 11),
                                             ('MASK', 'Mask', '', 'MOD_MASK', 12),
                                             ('MIRROR', 'Mirror', '', 'MOD_MIRROR', 13),
                                             ('MULTIRES', 'Multiresolution', '', 'MOD_MULTIRES', 14),
                                             ('REMESH', 'Remesh', '', 'MOD_REMESH', 15),
                                             ('SCREW', 'Screw', '', 'MOD_SCREW', 16),
                                             ('SKIN', 'Skin', '', 'MOD_SKIN', 17),
                                             ('SOLIDIFY', 'Solidify', '', 'MOD_SOLIDIFY', 18),
                                             ('SUBSURF', 'Subsurface Division', '', 'MOD_SUBSURF', 19),
                                             ('TRIANGULATE', 'Triangulate', '', 'MOD_TRIANGULATE', 20),
                                             ('WIREFRAME', 'Wireframe', '', 'MOD_WIREFRAME', 21),
                                             #Deform
                                             ('ARMATURE', 'Armature', '', 'MOD_ARMATURE', 22),
                                             ('CAST', 'Cast', '', 'MOD_CAST', 23),
                                             ('CURVE', 'Curve', '', 'MOD_CURVE', 24),
                                             ('DISPLACE', 'Displace', '', 'MOD_DISPLACE', 25),
                                             ('HOOK', 'Hook', '', 'HOOK', 26),
                                             ('LAPLACIANDEFORM', 'Laplacian Deform', '', 'MOD_MESHDEFORM', 27),
                                             ('LAPLACIANSMOOTH', 'Laplacian Smooth', '', 'MOD_SMOOTH', 28),
                                             ('LATTICE', 'Lattice', '', 'MOD_LATTICE', 29),
                                             ('MESH_DEFORM', 'Mesh Deform', '', 'MOD_MESHDEFORM', 30),
                                             ('SHRINKWRAP', 'Shrinkwrap', '', 'MOD_SHRINKWRAP', 31),
                                             ('SIMPLE_DEFORM', 'Simple Deform', '', 'MOD_SIMPLEDEFORM', 32),
                                             ('SMOOTH', 'Smooth', '', 'MOD_SMOOTH', 33),
                                             ('WARP', 'Warp', '', 'MOD_WARP', 34),
                                             ('WAVE', 'Wave', '', 'MOD_WAVE', 35),
                                             #Simulate
                                             ('CLOTH', 'Cloth', '', 'MOD_CLOTH', 36),
                                             ('COLLISION', 'Collision', '', 'MOD_PHYSICS', 37),
                                             ('DYNAMIC_PAINT', 'Dynamic Paint', '', 'MOD_DYNAMICPAINT', 38),
                                             ('EXPLODE', 'Explode', '', 'MOD_EXPLODE', 39),
                                             ('FLUID_SIMULATION', 'Fluid Simulation', '', 'MOD_FLUIDSIM', 40),
                                             ('OCEAN', 'Ocean', '', 'MOD_OCEAN', 41),
                                             ('PARTICLE_INSTANCE', 'Particle Instance', '', 'MOD_PARTICLES', 42),
                                             ('PARTICLE_SYSTEM', 'Particle System', '', 'MOD_PARTICLES', 43),
                                             ('SMOKE', 'Smoke', '', 'MOD_SMOKE', 44),
                                             ('SOFT_BODY', 'Soft Body', '', 'MOD_SOFT', 45)),
                                             name = '',
                                             description = 'Select type of modifier to be operated on',
                                             default = 'SUBSURF')

    bpy.types.Scene.khalibloo_ops_const_subtype = bpy.props.EnumProperty(items =(
                                             #Motion tracking
                                             ('CAMERA_SOLVER', 'Camera Solver', '', 'CONSTRAINT_DATA', 0),
                                             ('FOLLOW_TRACK', 'Follow Track', '', 'CONSTRAINT_DATA', 1),
                                             ('OBJECT_SOLVER', 'Object Solver', '', 'CONSTRAINT_DATA', 2),
                                             #Transform
                                             ('COPY_LOCATION', 'Copy Location', '', 'CONSTRAINT_DATA', 3),
                                             ('COPY_ROTATION', 'Copy Rotation', '', 'CONSTRAINT_DATA', 4),
                                             ('COPY_SCALE', 'Copy Scale', '', 'CONSTRAINT_DATA', 5),
                                             ('COPY_TRANSFORMS', 'Copy Transforms', '', 'CONSTRAINT_DATA', 6),
                                             ('LIMIT_DISTANCE', 'Limit Distance', '', 'CONSTRAINT_DATA', 7),
                                             ('LIMIT_LOCATION', 'Limit Location', '', 'CONSTRAINT_DATA', 8),
                                             ('LIMIT_ROTATION', 'Limit Rotation', '', 'CONSTRAINT_DATA', 9),
                                             ('LIMIT_SCALE', 'Limit Scale', '', 'CONSTRAINT_DATA', 10),
                                             ('MAINTAIN_VOLUME', 'Maintain Volume', '', 'CONSTRAINT_DATA', 11),
                                             ('TRANSFORM', 'Transformation', '', 'CONSTRAINT_DATA', 12),
                                             #Tracking
                                             ('CLAMP_TO', 'Clamp To', '', 'CONSTRAINT_DATA', 13),
                                             ('DAMPED_TRACK', 'Damped Track', '', 'CONSTRAINT_DATA', 14),
                                             ('IK', 'Inverse Kinematics', '', 'CONSTRAINT_DATA', 15),
                                             ('LOCKED_TRACK', 'Locked Track', '', 'CONSTRAINT_DATA', 16),
                                             ('SPLINE_IK', 'Spline IK', '', 'CONSTRAINT_DATA', 17),
                                             ('STRETCH_TO', 'Stretch To', '', 'CONSTRAINT_DATA', 18),
                                             ('TRACK_TO', 'Track To', '', 'CONSTRAINT_DATA', 19),
                                             #Relationship
                                             ('ACTION', 'Action', '', 'CONSTRAINT_DATA', 20),
                                             ('CHILD_OF', 'Child Of', '', 'CONSTRAINT_DATA', 21),
                                             ('FLOOR', 'Floor', '', 'CONSTRAINT_DATA', 22),
                                             ('FOLLOW_PATH', 'Follow Path', '', 'CONSTRAINT_DATA', 23),
                                             ('PIVOT', 'Pivot', '', 'CONSTRAINT_DATA', 24),
                                             ('RIGID_BODY_JOINT', 'Rigid Body Joint', '', 'CONSTRAINT_DATA', 25),
                                             ('SHRINKWRAP', 'Shrinkwrap', '', 'CONSTRAINT_DATA', 26)),
                                             name = '',
                                             description = 'Select type of constraint to be operated on',
                                             default = 'COPY_LOCATION')

    bpy.types.Scene.khalibloo_ops_datatype = bpy.props.EnumProperty(items=(
                                                ('ACTIONS', 'Actions', ''),
                                                ('GROUPS', 'Groups', ''),
                                                ('IMAGES', 'Images', ''),
                                                ('LINESTYLES', 'Freestyle Linestyles', ''),
                                                ('MATERIALS', 'Materials', ''),
                                                ('MOVIECLIPS', 'Movie Clips', ''),
                                                ('OBJECTS', 'Objects', ''),
                                                ('SCENES', 'Scenes', ''),
                                                ('SOUNDS', 'Sounds', ''),
                                                ('TEXTS', 'Texts', ''),
                                                ('TEXTURES', 'Textures', ''),
                                                ('WORLDS', 'Worlds', '')),
                                                name='Data Type',
                                                description='Type of data to operate on',
                                                default='OBJECTS')
    bpy.types.Scene.khalibloo_ops_scope01 = bpy.props.EnumProperty(items=(
                                                ('ALL', 'All', ''),
                                                ('ACTIVE', 'Active', '')),
                                                name='Scope',
                                                description='Scope of data to operate on',
                                                default='ALL')
    bpy.types.Scene.khalibloo_ops_scope02 = bpy.props.EnumProperty(items=(
                                                ('ALL', 'All', ''),
                                                ('ACTIVE', 'Active', ''),
                                                ('RENDER', 'Render', '')),
                                                name='Scope',
                                                description='Scope of data to operate on',
                                                default='ALL')
    bpy.types.Scene.khalibloo_ops_scope03 = bpy.props.EnumProperty(items=(
                                                ('ALL', 'All', ''),
                                                ('SCENE', 'Scene', ''),
                                                ('SELECTED', 'Selected', ''),
                                                ('ACTIVE', 'Active', '')),
                                                name='Scope',
                                                description='Scope of objects to operate on',
                                                default='SELECTED')
    bpy.types.Scene.khalibloo_ops_scope04_01 = bpy.props.EnumProperty(items=( #all, active, enabled, disabled
                                                ('ALL', 'All', ''),
                                                ('ACTIVE', 'Active', '')),
                                                name='Scope',
                                                description='Scope of textures to operate on',
                                                default='ALL')
    bpy.types.Scene.khalibloo_ops_scope04_02 = bpy.types.Scene.khalibloo_ops_scope04_01
    bpy.types.Scene.khalibloo_ops_scope05 = bpy.props.EnumProperty(items=(
                                                ('ALL', 'All', ''),
                                                ('CURRENT', 'Current', '')),
                                                name='Scope',
                                                description='Scope of data to operate on',
                                                default='ALL')
    bpy.types.Scene.khalibloo_ops_obj_subtype = bpy.props.EnumProperty(items=(
                                                ('NONE', 'None', ''),
                                                ('MATERIALS', 'Materials', ''),
                                                ('MODIFIERS', 'Modifiers', ''),
                                                ('CONSTRAINTS', 'Constraints', ''),
                                                ('VERTEX_GROUPS', 'Vertex Groups', ''),
                                                ('SHAPE_KEYS', 'Shape Keys', ''),
                                                ('UV_MAPS', 'UV Maps', ''),
                                                ('VERTEX_COLORS', 'Vertex Colors', ''),
                                                ('PARTICLE_SYSTEMS', 'Particle Systems', '')),
                                                name = "Object Data Subtype",
                                                description = "Subtype of object data to operate on",
                                                default = 'NONE')
    bpy.types.Scene.khalibloo_ops_mat_subtype_01 = bpy.props.EnumProperty(items=(
                                                ('NONE', 'None', ''),
                                                ('TEXTURES', 'Textures', '')),
                                                name = "Material Data Subtype",
                                                description = "Subtype of material data to operate on",
                                                default = 'NONE')
    bpy.types.Scene.khalibloo_ops_mat_subtype_02 = bpy.types.Scene.khalibloo_ops_mat_subtype_01
    bpy.types.Scene.khalibloo_ops_mod_scope = bpy.props.EnumProperty(items=(
                                                ('ALL', 'All', ''),
                                                ('SPECIFIC', 'Specific', '')),
                                                name='Scope',
                                                description='Scope of operation',
                                                default='ALL')
    bpy.types.Scene.khalibloo_ops_const_scope = bpy.props.EnumProperty(items=(
                                                ('ALL', 'All', ''),
                                                ('SPECIFIC', 'Specific', '')),
                                                name='Scope',
                                                description='Scope of operation',
                                                default='ALL')
    bpy.types.Scene.khalibloo_ops_scene_subtype = bpy.props.EnumProperty(items=(
                                                ('NONE', 'None', ''),
                                                ('RENDER', 'Render', '')),
                                                name = "Scene Data Subtype",
                                                description = "Subtype of scene data to operate on",
                                                default = 'NONE')
    bpy.types.Scene.khalibloo_ops_obj_type_filters = bpy.props.BoolVectorProperty(name='Filters',
                                    description='Object types to operate on',
                                    default=([True]*11),
                                    size=11)
    bpy.types.Scene.khalibloo_opblock_action_mode = bpy.props.EnumProperty(items=(
                                                ('OBJECT', 'Object Mode', ''),
                                                ('EDIT', 'Edit Mode', ''),
                                                ('POSE', 'Pose Mode', ''),
                                                ('SCULPT', 'Sculpt Mode', ''),
                                                ('VERTEX_PAINT', 'Vertex Paint Mode', ''),
                                                ('WEIGHT_PAINT', 'Weight Paint Mode', ''),
                                                ('TEXTURE_PAINT', 'Texture Paint Mode', ''),
                                                ('PARTICLE_EDIT', 'Particle Edit Mode', '')),
                                                name='Mode',
                                                description='Mode',
                                                default='OBJECT')
    bpy.types.Scene.khalibloo_opblock_action = bpy.props.StringProperty(
                                                name='Action',
                                                description='Action to perform',
                                                default='name = "khalibloo"')
    bpy.types.Scene.khalibloo_ops_use_obj_type_filters = bpy.props.BoolProperty(
                                                name="Use Object Type Filters",
                                                description="Filter objects by type",
                                                default=False)


# def nameOpBlock(name="operator block"):
    # global opBlockNames
    # if (name in opBlockNames): # We have a name conflict
        # if (name[-4] == "." and name[-1].isdigit() and name[-2].isdigit() and name[-3].isdigit()): # Is it already an extended name?
            # extension = int(name[-3:])
            # extension += 1
            # name += name[:-4] + str(extension)
        # else: # it's not an extended name
            # name += ".001"
        # nameOpBlock()
    # else:
        # opBlockNames.append(name)
        # return name
