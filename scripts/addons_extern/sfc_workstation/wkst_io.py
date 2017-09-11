#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#
# ***** END GPL LICENCE BLOCK *****


import bpy
from bpy import*


###########  Menu  #######################

class WKST_Import(bpy.types.Menu):
    """Import / Export"""
    bl_label = "Import/Export"
    bl_idname = "wkst.import_export"

    def draw(self, context):
        layout = self.layout

        layout.menu("INFO_MT_file_import", text="Import", icon='EXPORT')
        layout.menu("INFO_MT_file_export", text="Export", icon='IMPORT')
        layout.menu("OBJECT_MT_selected_export", text="Export Selected", icon='IMPORT')


class WKST_AppLINK(bpy.types.Menu):
    """Link / Append"""
    bl_label = "Link/Append"
    bl_idname = "wkst.link_append"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.link", text="Link", icon='LINK_BLEND')
        layout.operator("wm.append", text="Append", icon='APPEND_BLEND')

        layout.separator()

        layout.operator("object.proxy_make")
        layout.operator("object.make_local")


############  REGISTER  #################

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
