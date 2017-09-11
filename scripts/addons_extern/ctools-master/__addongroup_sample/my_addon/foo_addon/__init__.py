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
    "name": "Foo Add-on",
    "version": (0, 1),
    "description": "Addon group test",
    "category": "3D View",
}


if "bpy" in locals():
    FooAddonPreferences.reload_submodules()
else:
    from .. import addongroup

import bpy


class FooAddonPreferences(addongroup.AddonGroup, bpy.types.PropertyGroup):
    bl_idname = __name__

    submodules = [
        "bar_addon"
    ]

    foo_prop = bpy.props.IntProperty(name="Foo Add-on Prop")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "foo_prop")

        layout.separator()
        super().draw(context)

    @classmethod
    def register(cls):
        super().register()

    @classmethod
    def unregister(cls):
        super().unregister()


class FooPanel(bpy.types.Panel):
    bl_idname = "FooPanel"
    bl_label = "Foo Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        pass


classes = [
    FooAddonPreferences,
    FooPanel,
]


@FooAddonPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    prefs = FooAddonPreferences.get_instance()
    value = prefs.foo_prop


@FooAddonPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
