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
# by meta-androcto, parts based on work by Saidenka #

bl_info = {
    "name": "AF: 3d View Specials",
    "author": "Meta Androcto, ",
    "version": (0, 2),
    "blender": (2, 75, 0),
    "location": "W key > Object, Edit, Pose, Armature",
    "description": "Extended Specials: W key > Object, Edit, Pose, Armature",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6"\
        "/Py/Scripts",
    "tracker_url": "",
    "category": "Addon Factory"}


if "bpy" in locals():
    import importlib
    importlib.reload(VIEW3D_MT_armature_specials)
    importlib.reload(VIEW3D_MT_edit_mesh_specials)
    importlib.reload(VIEW3D_MT_select_object)
    importlib.reload(VIEW3D_MT_pose_specials)
    importlib.reload(VIEW3D_MT_object_batch)


else:
    from . import VIEW3D_MT_armature_specials
    from . import VIEW3D_MT_edit_mesh_specials
    from . import VIEW3D_MT_object_specials
    from . import VIEW3D_MT_pose_specials
    from . import VIEW3D_MT_object_batch


import bpy
# Addons Preferences
class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	
	def draw(self, context):
		layout = self.layout
		layout.label(text="----3d View Specials Menu's----")
		layout.label(text="Concept for populating the w key specials menu's")
		layout.label(text="W key Specials> Object, Edit, Pose & Armature Modes")

def register():
    bpy.utils.register_module(__name__)
    # Add "Extras" menu to the "Add Mesh" menu
    bpy.types.VIEW3D_MT_armature_specials.append(VIEW3D_MT_armature_specials.menu)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(VIEW3D_MT_edit_mesh_specials.menu)
    bpy.types.VIEW3D_MT_object_specials.append(VIEW3D_MT_object_specials.menu)
    bpy.types.VIEW3D_MT_pose_specials.append(VIEW3D_MT_pose_specials.menu)
    bpy.types.VIEW3D_MT_object_specials.append(VIEW3D_MT_object_batch.menu)


def unregister():
	bpy.utils.unregister_module(__name__)
    # Remove "Extras" menu from the "Add Mesh" menu.
	bpy.types.VIEW3D_MT_armature_specials.remove(VIEW3D_MT_armature_specials.menu)
	bpy.types.VIEW3D_MT_edit_mesh_specials.remove(VIEW3D_MT_edit_mesh_specials.menu)
	bpy.types.VIEW3D_MT_object_specials.remove(VIEW3D_MT_object_specials.menu)
	bpy.types.VIEW3D_MT_pose_specials.remove(VIEW3D_MT_pose_specials.menu)
	bpy.types.VIEW3D_MT_object_specials.remove(VIEW3D_MT_object_batch.menu)


if __name__ == "__main__":
    register()
