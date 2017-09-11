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
    "name": "Object Mode: Key: Tab key",
    "location": "Tab key",
    "category": "3D View",
}


from collections import OrderedDict

import bpy

from ..utils import addongroup

import pie_menu


class Empty:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def has_particle(context):
    actob = context.active_object
    if actob:
        if actob.particle_systems:
            return True
        else:
            for mod in actob.modifiers:
                if mod.type in ('CLOTH', 'SOFT_BODY'):
                    return True
    return False


def has_gpencil(context):
    return bool(context.gpencil_data)


class ObjectModeMenuMore:
    idname = "object_mode_set_more"
    label = "Object Mode"
    quick_action = 'NONE'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []
        prop = bpy.types.Object.bl_rna.properties["mode"]
        enum_items = OrderedDict([(e.identifier, e) for e in prop.enum_items])

        execute = "bpy.ops.object.mode_set(mode='{}', toggle={})"
        if has_particle(context):
            e = enum_items['PARTICLE_EDIT']
            item = Empty(label=e.name)
            item.icon = e.icon
            item.execute = execute.format(e.identifier, "False")
        else:
            item = None
        self.menu_items.append(item)

        if has_gpencil(context):
            e = enum_items['GPENCIL_EDIT']
            item = Empty(label=e.name)
            item.icon = e.icon
            item.execute = execute.format(e.identifier, "False")
        else:
            item = None
        self.menu_items.append(item)


class ObjectModeMenu:
    idname = "object_mode_set"
    label = "Object Mode"
    quick_action = 'W'
    item_order = 'CW6'

    def init(self, context):
        self.menu_items = []

        actob = context.active_object

        self.quick_action = 'S'

        prop = bpy.types.Object.bl_rna.properties["mode"]
        enum_items = OrderedDict([(e.identifier, e) for e in prop.enum_items])
        for enum_item in enum_items.values():
            mode = enum_item.identifier
            add = False
            execute = "bpy.ops.object.mode_set(mode='{}', toggle={})"
            if mode == 'OBJECT':
                # if actob and actob.type in {'EMPTY', 'CAMERA', 'LAMP',
                #                             'SPEAKER'}:
                #     self.quick_action = 'W'
                add = True
            elif mode == 'EDIT':
                if actob and actob.type in {
                        'MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE',
                        'LATTICE'}:
                    self.quick_action = 'SW'
                    add = True
            elif mode == 'POSE':
                if actob and actob.type == 'ARMATURE':
                    add = True
            elif mode in {'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT',
                          'TEXTURE_PAINT'}:
                if actob and actob.type == 'MESH':
                    add = True
            elif mode in {'PARTICLE_EDIT', 'GPENCIL_EDIT'}:
                continue

            if add:
                item = Empty(label=enum_item.name)
                item.icon = enum_item.icon
                if mode == 'EDIT':
                    item.execute = execute.format(mode, "True")
                else:
                    item.execute = execute.format(mode, "False")
                self.menu_items.append(item)
            else:
                self.menu_items.append(None)

        if has_particle(context) or has_gpencil(context):
            e1 = enum_items['PARTICLE_EDIT']
            e2 = enum_items['GPENCIL_EDIT']
            name = "{} / {}".format(e1.name, e2.name)
            item = Empty(label=name)
            item.icon = "PLUS"
            item.menu = "object_mode_set_more"
            self.menu_items.append(item)
        else:
            self.menu_items.append(None)


class PieMenuObjectModeSetAddonPreferences(
        addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    menus = [ObjectModeMenuMore, ObjectModeMenu]

    def draw(self, context):
        pie_menu.draw_menus(self, context, self.layout)
        addongroup.AddonGroup.draw(self, context)


# order = {'OBJECT': 0,
#          'EDIT': 4,
#          'POSE': 2,
#          'SCULPT': 1,
#          'VERTEX_PAINT': 5,
#          'WEIGHT_PAINT': 6,
#          'TEXTURE_PAINT': 2,
#          'PARTICLE_EDIT': 3,
#          'GPENCIL_EDIT': 7,
#          }


menu_keymap_items = {
    "object_mode_set": [
        ["Object Non-modal", {"type": 'TAB', "value": 'PRESS'}],
        ["Grease Pencil Stroke Edit Mode", {"type": 'TAB', "value": 'PRESS'}]]
}


classes = [
    PieMenuObjectModeSetAddonPreferences
]


@PieMenuObjectModeSetAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    addon_prefs = PieMenuObjectModeSetAddonPreferences.get_instance()

    pie_menu.register_addon(addon_prefs)

    for idname, km_items in menu_keymap_items.items():
        for km_name, kwargs in km_items:
            km = pie_menu.get_keymap(km_name)
            if km:
                kmi = km.keymap_items.new("wm.pie_menu", **kwargs)
                kmi.properties.menu = idname


@PieMenuObjectModeSetAddonPreferences.unregister_addon
def unregister():
    addon_prefs = PieMenuObjectModeSetAddonPreferences.get_instance()
    pie_menu.unregister_addon(addon_prefs)
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
