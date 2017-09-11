# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

if "bpy" in locals():
    import imp
    imp.reload(operator)

else:
    from . import operator

import bpy


bl_info = {
    "name": "Auto Drawing Tool",
    "author": "Nobuyuki Hirakata",
    "version": (0, 3, 0),
    "blender": (2, 76, 0),
    "location": "View3D > Toolshelf > Animation tab",
    "description": "Make auto-drawing setting using Build modifier and Freestyle.",
    "warning": "",
    "wiki_url": "http://blenderartists.org/forum/showthread.php?394426-Addon-Auto-Drawing-Tool",
    "tracker_url": "http://blenderartists.org/forum/showthread.php?394426-Addon-Auto-Drawing-Tool",
    "category": "Animation"
}

def register():
    bpy.utils.register_module(__name__)

    # Input on toolshelf before execution --------------------------
    #  In Panel subclass, In bpy.types.Operator subclass, reference them by context.scene.~.
    bpy.types.Scene.draw_start_frame = bpy.props.IntProperty(
        name = "Start Frame",
        description = "Set start frame",
        default = 1
    )
    bpy.types.Scene.draw_end_frame = bpy.props.IntProperty(
        name = "End Frame",
        description = "Set end frame",
        default = 100
    )

def unregister():
    # Delete bpy.types.Scene.~.
    del bpy.types.Scene.draw_start_frame
    del bpy.types.Scene.draw_end_frame
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
