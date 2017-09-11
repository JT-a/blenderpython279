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

ddddddfa

"""
MeshのEditModeに於いて、右クリックで選択される頂点/辺/面を強調表示する。
"""

bl_info = {
    'name': 'Bake Closest Normal',
    'author': 'chromoly',
    'version': (0, 1),
    'blender': (2, 76, 0),
    'location': '',
    'wiki_url': '',
    'category': '3D View',
}


import bpy


class OBJECT_OT_bake_normal(bpy.types.Operator):
    bl_label = 'Bake Normal'
    bl_idname = 'object.bake_normal'

    def execute(self, context):
        # アクティブにimage作成、割当。normalをworldで焼く
        # selectにimage作成、割当。normalをworldで焼く
        # アクティブのimageでループ。Object.closest_point_on_mesh()を使う


        return {'FINISED'}


classes = [

]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
