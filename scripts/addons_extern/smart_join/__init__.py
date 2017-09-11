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



bl_info = {
    "name": "Smart Join",
    "author": "Andrej Ivanis",
    "version": (1, 0, 3),
    "blender": (2, 73, 0),
    "location": "Relationships tab, Specials menu (w-key)",
    "warning": "",
    "description": "Enables non-destructive join of the objects",
    "wiki_url": "",
    "category": "Object"}


if "bpy" in locals():
    import imp
    imp.reload(core)
    imp.reload(gui)
else:
    from . import core, gui

import bpy, bmesh
from bpy.props import *

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Mesh.is_sjoin = BoolProperty(default=False)

    # this is used if mesh is renamed or duplicated
    bpy.types.Mesh.sjoin_link_name = StringProperty()
    bpy.types.Mesh.expanded_obj = StringProperty()
    bpy.types.Object.sjoin_mesh = StringProperty(default = '')
    # add empty smart join
    # bpy.types.INFO_MT_add.append(add_menu_func)
    bpy.types.VIEW3D_MT_object_specials.append(special_menu_func)
    bpy.app.handlers.scene_update_post.append(core.scene_update)
    bpy.app.handlers.save_pre.append(core.before_save)
    # global update_lock
    # update_lock = False
    
    
class ExampleAddonPreferences(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    allow_edit_mode = bpy.props.BoolProperty(
            name="Allow edit mode",
            default=False
            )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "allow_edit_mode")
        layout.label(text="NOTE: any changes to smart join in the edit mode will be reverted after expanding")
        layout.label(text="You can Apply the join in the Relationships tab, but you won't be able to expand it any more")

def special_menu_func(self, context):
    self.layout.separator()
    layout = self.layout
    layout.operator('sjoin.join')
    layout.operator('sjoin.join_add')
    layout.operator('sjoin.separate')
    layout.operator('sjoin.update_rec')
    layout.separator()
    layout.operator('sjoin.expand')
    layout.operator('sjoin.collapse')


def unregister():
    del bpy.types.Mesh.is_sjoin
    del bpy.types.Object.sjoin_mesh
    bpy.types.VIEW3D_MT_object_specials.remove(special_menu_func)
    bpy.app.handlers.scene_update_post.remove(core.scene_update)
    bpy.app.handlers.save_pre.remove(core.before_save)
    # bpy.types.INFO_MT_add.remove(add_menu_func)
    bpy.utils.unregister_module(__name__)



if __name__ == "__main__":
    register()
