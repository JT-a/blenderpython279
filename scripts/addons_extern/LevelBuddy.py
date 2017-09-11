#  ***** BEGIN GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  ***** END GPL LICENSE BLOCK *****

bl_info = {
    "name": "Level Buddy",
    "author": "Matt Lucas",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "View3D > Tools",
    "description": "A set of workflow tools based on concepts from Doom and Unreal level mapping.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Game Engine",
}

import bpy


def update_location_percision(ob):
    ob.location.x = round(ob.location.x, 1)
    ob.location.y = round(ob.location.y, 1)
    ob.location.z = round(ob.location.z, 1)
    cleanup_vert_percision(ob)


def freeze_transforms(ob):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern=ob.name)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.select_all(action='DESELECT')


def update_sector_lighting(ob):
    mesh = ob.data
    color_layer = mesh.vertex_colors.active
    light_value = ob.sector_light_value
    light_type = 1.0
    if ob.sector_light_type == "NONE":
        light_type = 1.0
    if ob.sector_light_type == "PULSE":
        light_type = 0.0
    if ob.sector_light_type == "FLICKER":
        light_type = 0.1
    if ob.sector_light_type == "SWITCH 1":
        light_type = 0.2
    if ob.sector_light_type == "SWITCH 2":
        light_type = 0.3
    if ob.sector_light_type == "SWITCH 3":
        light_type = 0.4
    if ob.sector_light_type == "SWITCH 4":
        light_type = 0.5
    if ob.sector_light_type == "BLINK":
        light_type = 0.6
    light_max = ob.sector_light_max
    rgb = (light_value, light_type, light_max)
    if not mesh.vertex_colors:
        mesh.vertex_colors.new()
    for v in color_layer.data:
        v.color = rgb


def update_sector_plane_modifier(ob):
    if ob.modifiers:
        mod = ob.modifiers[0]
        if mod.type == "SOLIDIFY":
            if ob.floor_height > 0:
                mod.thickness = ob.ceiling_height - ob.floor_height
            else:
                mod.thickness = ob.ceiling_height - ob.floor_height
            mod.material_offset = 1
            mod.material_offset_rim = 2


def update_sector_plane_materials(ob):
    if bpy.data.materials.find(ob.ceiling_texture) != -1:
        ob.material_slots[0].material = bpy.data.materials[ob.ceiling_texture]
    if bpy.data.materials.find(ob.floor_texture) != -1:
        ob.material_slots[1].material = bpy.data.materials[ob.floor_texture]
    if bpy.data.materials.find(ob.wall_texture) != -1:
        ob.material_slots[2].material = bpy.data.materials[ob.wall_texture]


def update_sector(self, context):
    ob = context.active_object
    scene = bpy.context.scene
    if ob.type == 'MESH' and ob.sector_type == 'PLANE':
        update_sector_lighting(ob)
        update_location_percision(ob)
        if ob.is_sector_mesh == False:
            update_sector_plane_modifier(ob)
            update_sector_plane_materials(ob)
    if ob.type != 'NONE' or ob.sector_type != 'PLANE':
        update_sector_lighting(ob)
        update_location_percision(ob)
    if bpy.context.scene["map_live_update"]:
        bpy.ops.scene.level_buddy_build_map()
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern=ob.name)
    bpy.context.scene.objects.active = ob


def cleanup_vert_percision(ob):
    if ob.type == 'MESH':
        for v in ob.data.vertices:
            if ob.sector_type == 'PLANE':
                v.co.z = ob.floor_height
            v.co.x = round(v.co.x, 1)
            v.co.y = round(v.co.y, 1)
            v.co.z = round(v.co.z, 1)
            

def apply_boolean(obj_active, x, bool_op, delete_original=False):
    bpy.ops.object.select_all(action='DESELECT')
    obj_active.select = True
    me = bpy.data.objects[x].to_mesh(bpy.context.scene, True, "PREVIEW")
    ob_bool = bpy.data.objects.new("_booley", me)
    copy_transforms(ob_bool, bpy.data.objects[x])
    cleanup_vert_percision(ob_bool)
    copy_materials(obj_active, bpy.data.objects[x])
    mod = obj_active.modifiers.new(name=x, type='BOOLEAN')
    mod.object = ob_bool
    mod.operation = bool_op
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=x)
    if delete_original:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_pattern(pattern=x)
        bpy.ops.object.delete()


def flip_object_normals(ob):
    bpy.ops.object.select_all(action='DESELECT')
    ob.select = True
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.editmode_toggle()


def auto_texture(ob):
    bpy.ops.object.select_all(action='DESELECT')
    ob.select = True
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.texture_buddy_uv()
    bpy.ops.object.editmode_toggle()


def move_object_to_layer(ob, layer_number):
    layers = 20 * [False]
    layers[layer_number] = True
    ob.layers = layers


def create_new_boolean_object(scn, name):
    old_map = None
    if bpy.data.meshes.get(name + "_MESH") is not None:
        old_map = bpy.data.meshes[name + "_MESH"]
        old_map.name = "map_old"
    me = bpy.data.meshes.new(name + "_MESH")
    if bpy.data.objects.get(name) is None:
        ob = bpy.data.objects.new(name, me)
        scn.objects.link(ob)
    else:
        ob = bpy.data.objects[name]
        ob.data = me
    if old_map is not None:
        bpy.data.meshes.remove(old_map)
    ob.layers[scn.active_layer] = True
    scn.objects.active = ob
    ob.select = True
    return ob


def add_all_materials(ob):
    i = 0
    for m in bpy.data.materials:
        if len(ob.data.materials) > i:
            has_material = False
            for mat in ob.data.materials:
                if mat.name == m.name:
                    has_material = True
            if not has_material:
                ob.data.materials[i] = m
        else:
            ob.data.materials.append(m)
        i += 1


def copy_materials(a, b):
    for m in b.data.materials:
        has_material = False
        for mat in a.data.materials:
            if mat is not None and m is not None:
                if mat.name == m.name:
                    has_material = True
        if not has_material and m is not None:
            a.data.materials.append(m)


def copy_transforms(a, b):
    a.location = b.location
    a.scale = b.scale
    a.rotation_euler = b.rotation_euler


def get_active_layers():
    scn = bpy.context.scene
    active_layer = [False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                    False, False, False, False, False, False]
    active_layer[scn.active_layer] = True
    return active_layer


bpy.types.Object.ceiling_height = bpy.props.FloatProperty(name="Ceiling Height", default=4, step=20, precision=1,
                                                          update=update_sector)
bpy.types.Object.floor_height = bpy.props.FloatProperty(name="Floor Height", default=0, step=20, precision=1,
                                                        update=update_sector)
bpy.types.Object.floor_texture = bpy.props.StringProperty(name="Floor Texture", update=update_sector)
bpy.types.Object.wall_texture = bpy.props.StringProperty(name="Wall Texture", update=update_sector)
bpy.types.Object.ceiling_texture = bpy.props.StringProperty(name="Ceiling Texture", update=update_sector)
bpy.types.Object.sector_light_value = bpy.props.FloatProperty(name="Light Value", default=1.0, step=1, min=0.0, max=1.0,
                                                              update=update_sector)
bpy.types.Object.sector_light_type = bpy.props.EnumProperty(items=[
    ("PULSE", "Pulse", "lit with a pulsing light, no brighter then the light max and no darker then the light value."),
    ("FLICKER", "Flicker", "lit with a flickering light, no brighter then the light max and no darker then the light value."),
    ("BLINK", "Blink", "lit with a blinking light, no brighter then the light max and no darker then the light value."),
    ("SWITCH 1", "Light 1", "lit by light 1 which can be turned on and off through game logic. (ID=-1)"),
    ("SWITCH 2", "Light 2", "lit by light 2 which can be turned on and off through game logic. (ID=-2)"),
    ("SWITCH 3", "Light 3", "lit by light 3 which can be turned on and off through game logic. (ID=-3)"),
    ("SWITCH 4", "Light 4", "lit by light 4 which can be turned on and off through game logic. (ID=-4)"),
    ("NONE", "None", "light with the normal steady light value.")
], name="Light Type", description="the lighting type for the sector", default='NONE', update=update_sector)
bpy.types.Object.sector_light_max = bpy.props.FloatProperty(name="Light Max", default=1.0, step=1, min=0.0, max=1.0,
                                                              update=update_sector)
bpy.types.Object.is_sector = bpy.props.BoolProperty(name="Is Sector", default=False)
bpy.types.Object.is_sector_mesh = bpy.props.BoolProperty(name="Is Sector Mesh", default=False)
bpy.types.Object.is_brush = bpy.props.BoolProperty(name="Is Brush", default=False)
bpy.types.Object.no_combine = bpy.props.BoolProperty(name="No Combine", default=False)
bpy.types.Object.sector_type = bpy.props.EnumProperty(items=[
    ("STATIC", "Static Mesh", "a normal static mesh, might be used later when light mapping gets added"),
    ("SUBTRACT", "Brush Subtractive", "like a brush but instead of adding geo it removes it"),
    ("BRUSH", "Brush", "is a 3d brush volume"),
    ("MESH", "3D Sector", "is a 3d sector mesh"),
    ("PLANE", "2D Sector", "is a 2d sector plane"),
    ("NONE", "None", "marks the objet as not a sector")
], name="Sector Type", description="the sector type", default='NONE')
bpy.types.Scene.map_layer = bpy.props.IntProperty(name="Map Layer", default=0, min=0, max=19)
bpy.types.Scene.map_name = bpy.props.StringProperty(name="Map Name", default="Map")
bpy.types.Scene.brush_material = bpy.props.StringProperty(name="Active Material", default="")
bpy.types.Scene.map_live_update = bpy.props.BoolProperty(name="Live Update!", default=False)


class LevelBuddyPanel(bpy.types.Panel):
    bl_label = "Level Buddy"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "LevelBuddy"

    def draw(self, context):
        ob = context.active_object
        scn = bpy.context.scene
        layout = self.layout
        col = layout.column(align=True)
        col.label(icon="WORLD", text="Map Settings")
        col.prop(scn, "map_name", text="Name")
        col.operator("scene.level_buddy_build_map", text="Build Map", icon="MOD_BUILD").bool_op = "UNION"
        col.prop(scn, "map_layer")
        col.prop(scn, "map_live_update")
        layout.separator()
        col = layout.column(align=True)
        col.label(icon="SNAP_PEEL_OBJECT", text="New Sector")
        col.operator("scene.level_new_sector", text="New 2D Sector", icon="SURFACE_NCURVE")
        col.operator("scene.level_new_brush", text="New 3D Sector", icon="SNAP_FACE").s_type = 'MESH'
        col.operator("scene.level_new_brush", text="New Brush", icon="SNAP_VOLUME").s_type = 'BRUSH'
        col.prop_search(scn, "brush_material", bpy.data, "materials", icon="POTATO", text="")
        layout.separator()
        col = layout.column(align=True)
        col.operator("scene.level_buddy_cleanup", icon="ERROR")
        col.operator("scene.level_buddy_empty_trash", icon="ERROR")
        layout.separator()
        col = layout.column(align=True)
        if ob != None:
            col.label(icon="FORCE_LENNARDJONES", text="Sector Settings")
            col.prop(ob, "sector_type", text="Type")
            col.prop(ob, "draw_type", text="")
            col.prop(ob, "no_combine", icon="FORCE_CHARGE")
            layout.separator()
            col = layout.column(align=True)
            if ob != None and len(bpy.context.selected_objects) > 0:
                if ob.sector_type != 'NONE' or ob.sector_type != 'PLANE':
                    col.label(icon="LAMP_SUN", text="Sector Lighting")
                    col.prop(ob, "sector_light_type")
                    col.prop(ob, "sector_light_value")
                    col.prop(ob, "sector_light_max")
                    col.operator("scene.level_buddy_copy", text="Copy Lighting").copy_op = "LIGHT_VALUE"
                    layout.separator()
                    col = layout.column(align=True)
                if ob.sector_type == 'PLANE':
                    if ob.modifiers:
                        mod = ob.modifiers[0]
                        if mod.type == "SOLIDIFY":
                            col.label(icon="MOD_ARRAY", text="Sector Heights")
                            col.prop(ob, "ceiling_height")
                            col.prop(ob, "floor_height")
                            layout.separator()
                            col = layout.column(align=True)
                            col.label(icon="FACESEL_HLT", text="Sector Materials")
                            col.prop_search(ob, "ceiling_texture", bpy.data, "materials", icon="FACESEL_HLT",
                                            text="Ceiling")
                            col.prop_search(ob, "wall_texture", bpy.data, "materials", icon="FACESEL_HLT", text="Wall")
                            col.prop_search(ob, "floor_texture", bpy.data, "materials", icon="FACESEL_HLT",
                                            text="Floor")
                            layout.separator()
                            col = layout.column(align=True)
                            col.label(icon="PASTEFLIPUP", text="Copy Heights")
                            col.operator("scene.level_buddy_copy", text="Ceiling").copy_op = "HEIGHT_CEILING"
                            col.operator("scene.level_buddy_copy", text="Floor").copy_op = "HEIGHT_FLOOR"
                            col.operator("scene.level_buddy_copy", text="ALL").copy_op = "HEIGHT_ALL"
                            layout.separator()
                            col = layout.column(align=True)
                            col.label(icon="PASTEFLIPUP", text="Copy Textures")
                            col.operator("scene.level_buddy_copy", text="Ceiling").copy_op = "TEXTURE_CEILING"
                            col.operator("scene.level_buddy_copy", text="Wall").copy_op = "TEXTURE_WALL"
                            col.operator("scene.level_buddy_copy", text="Floor").copy_op = "TEXTURE_FLOOR"
                            col.operator("scene.level_buddy_copy", text="ALL").copy_op = "TEXTURE_ALL"
                            layout.separator()
                            col = layout.column(align=True)
                            col.label(icon="PASTEFLIPUP", text="Copy ALL")
                            col.operator("scene.level_buddy_copy", text="Copy Heights & Textures").copy_op = "ALL"
                    layout.separator()


class LevelNewSector(bpy.types.Operator):
    bl_idname = "scene.level_new_sector"
    bl_label = "Level New Sector"

    def execute(self, context):
        scn = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0),
                                         layers=get_active_layers())
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].offset = 1
        bpy.context.object.modifiers["Solidify"].use_even_offset = True
        bpy.context.object.modifiers["Solidify"].use_quality_normals = True
        ob = bpy.context.active_object
        ob.name = "sector"
        ob.data.name = "sector"
        ob.ceiling_height = 4
        ob.floor_height = 0
        ob.sector_type = 'PLANE'
        ob.draw_type = 'WIRE'
        bpy.context.object.game.physics_type = 'NO_COLLISION'
        bpy.context.object.hide_render = True
        if len(bpy.data.materials) > 0:
            if scn.brush_material is not "":
                ob.data.materials.append(bpy.data.materials[scn.brush_material])
                ob.data.materials.append(bpy.data.materials[scn.brush_material])
                ob.data.materials.append(bpy.data.materials[scn.brush_material])
                ob.ceiling_texture = scn.brush_material
                ob.wall_texture = scn.brush_material
                ob.floor_texture = scn.brush_material
            else:
                ob.data.materials.append(bpy.data.materials[0])
                ob.data.materials.append(bpy.data.materials[0])
                ob.data.materials.append(bpy.data.materials[0])
                ob.ceiling_texture = bpy.data.materials[0].name
                ob.wall_texture = bpy.data.materials[0].name
                ob.floor_texture = bpy.data.materials[0].name
        else:
            bpy.ops.object.material_slot_add()
            bpy.ops.object.material_slot_add()
            bpy.ops.object.material_slot_add()
            ob.ceiling_texture = ""
            ob.wall_texture = ""
            ob.floor_texture = ""
        scn.objects.active = ob
        bpy.ops.object.level_update_sector()
        return {"FINISHED"}


class LevelNewBrush(bpy.types.Operator):
    bl_idname = "scene.level_new_brush"
    bl_label = "Level New Brush"

    s_type = bpy.props.StringProperty(name="s_type", default='BRUSH')

    def execute(self, context):
        scn = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0),
                                        layers=get_active_layers())
        ob = bpy.context.active_object
        ob.draw_type = 'WIRE'
        ob.name = self.s_type
        ob.data.name = self.s_type
        ob.sector_type = self.s_type
        if scn.brush_material is not "":
            ob.data.materials.append(bpy.data.materials[scn.brush_material])
        scn.objects.active = ob
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.texture_buddy_uv()
        bpy.ops.object.editmode_toggle()
        bpy.context.object.game.physics_type = 'NO_COLLISION'
        bpy.context.object.hide_render = True
        return {"FINISHED"}


class LevelUpdateSector(bpy.types.Operator):
    bl_idname = "object.level_update_sector"
    bl_label = "Level Update Sector"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        for ob in selected_objects:
            update_sector_plane_modifier(ob)
        return {"FINISHED"}


class LevelBuddyCopy(bpy.types.Operator):
    bl_idname = "scene.level_buddy_copy"
    bl_label = "Level Buddy Copy"

    copy_op = bpy.props.StringProperty(name="copy_op", default="ALL")

    def execute(self, context):
        ob = context.object
        selected_objects = bpy.context.selected_objects
        for s in selected_objects:
            if s.sector_type == 'PLANE':
                if self.copy_op == "HEIGHT_CEILING" or self.copy_op == "HEIGHT_ALL" or self.copy_op == "ALL":
                    s.ceiling_height = ob.ceiling_height
                if self.copy_op == "HEIGHT_FLOOR" or self.copy_op == "HEIGHT_ALL" or self.copy_op == "ALL":
                    s.floor_height = ob.floor_height
                if self.copy_op == "TEXTURE_CEILING" or self.copy_op == "TEXTURE_ALL" or self.copy_op == "ALL":
                    s.ceiling_texture = ob.ceiling_texture
                if self.copy_op == "TEXTURE_WALL" or self.copy_op == "TEXTURE_ALL" or self.copy_op == "ALL":
                    s.wall_texture = ob.wall_texture
                if self.copy_op == "TEXTURE_FLOOR" or self.copy_op == "TEXTURE_ALL" or self.copy_op == "ALL":
                    s.floor_texture = ob.floor_texture
                if self.copy_op == "LIGHT_VALUE":
                    s.sector_light_value = ob.sector_light_value
                    s.sector_light_type = ob.sector_light_type
                    s.sector_light_max = ob.sector_light_max
                bpy.context.scene.objects.active = s
                bpy.ops.object.level_update_sector()
        bpy.context.scene.objects.active = ob
        return {"FINISHED"}


class LevelCleanupPercision(bpy.types.Operator):
    bl_idname = "scene.level_buddy_cleanup"
    bl_label = "Level Cleanup Percision"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        for ob in selected_objects:
            update_location_percision(ob)
        return {"FINISHED"}
        
        
class LevelEmptyTrash(bpy.types.Operator):
    bl_idname = "scene.level_buddy_empty_trash"
    bl_label = "Level Empty Trash"

    def execute(self, context):
        for o in bpy.data.objects:
            if o.users == 0:
                bpy.data.objects.remove(o)
        for m in bpy.data.meshes:
            if m.users == 0:
                bpy.data.meshes.remove(m)
        return {"FINISHED"}


class LevelBuddyBuildMap(bpy.types.Operator):
    bl_idname = "scene.level_buddy_build_map"
    bl_label = "Level Buddy Build Map"

    bool_op = bpy.props.StringProperty(name="bool_op", default="INTERSECT")

    def execute(self, context):
        scn = bpy.context.scene
        sector_list = []
        brush_list = []
        subtract_list = []
        #print("============================================================")
        #print(" LEVEL BUDDY MAP COMPILE")
        #print("============================================================")
        #print("...START")
        map = create_new_boolean_object(scn, scn.map_name)
        #print("...collecting sectors and brushes")
        visible_objects = bpy.context.visible_objects
        for ob in visible_objects:
            if ob.no_combine == False and ob.type == 'MESH' and ob.sector_type != 'NONE' and ob != map:
                if ob.sector_type == 'PLANE' or ob.sector_type == 'MESH':
                    sector_list.append(ob.name)
                    freeze_transforms(ob)
                if ob.sector_type == 'BRUSH':
                    brush_list.append(ob.name)
                    update_location_percision(ob)
                if ob.sector_type == 'SUBTRACT':
                    subtract_list.append(ob.name)
                    update_location_percision(ob)
        #print("...combining sector")
        for x in sector_list:
            if x != sector_list[0]:
                apply_boolean(map, x, 'UNION')
            else:
                map.data = bpy.data.objects[x].to_mesh(bpy.context.scene, True, "PREVIEW")
                scn.objects.active = map
        if len(sector_list) > 0:
            flip_object_normals(map)
        #print("...combining brush")
        for x in brush_list:
            apply_boolean(map, x, 'UNION')
            update_location_percision(map)
        for x in subtract_list:
            apply_boolean(map, x, 'DIFFERENCE')
            update_location_percision(map)
        #print("...texture unwrap")
        auto_texture(map)
        #print("...moving map to new layer and making it current selection")
        move_object_to_layer(map, scn.map_layer)
        map.hide_select = True
        bpy.ops.object.select_all(action='DESELECT')
        #print("...FINISHED")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(LevelBuddyPanel)
    bpy.utils.register_class(LevelBuddyBuildMap)
    bpy.utils.register_class(LevelNewSector)
    bpy.utils.register_class(LevelBuddyCopy)
    bpy.utils.register_class(LevelUpdateSector)
    bpy.utils.register_class(LevelNewBrush)
    bpy.utils.register_class(LevelCleanupPercision)
    bpy.utils.register_class(LevelEmptyTrash)


def unregister():
    bpy.utils.unregister_class(LevelBuddyPanel)
    bpy.utils.unregister_class(LevelBuddyBuildMap)
    bpy.utils.unregister_class(LevelNewSector)
    bpy.utils.unregister_class(LevelBuddyCopy)
    bpy.utils.unregister_class(LevelUpdateSector)
    bpy.utils.unregister_class(LevelNewBrush)
    bpy.utils.unregister_class(LevelCleanupPercision)
    bpy.utils.unregister_class(LevelEmptyTrash)


if __name__ == "__main__":
    register()
