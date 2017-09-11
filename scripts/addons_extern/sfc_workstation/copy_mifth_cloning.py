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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****


# bl_info = {
#    "name": "Mifth Tools",
#    "author": "Paul Geraskin",
#    "version": (0, 1, 0),
#    "blender": (2, 71, 0),
#    "location": "3D Viewport",
#    "description": "Mifth Tools",
#    "warning": "",
#    "wiki_url": "",
#    "tracker_url": "",
#    "category": "Tools"}


import bpy
from bpy.props import *
from bpy.types import Operator, AddonPreferences

import math


class MFTRadialClone(bpy.types.Operator):
    bl_idname = "mft.radialclone"
    bl_label = "Radial Clone"
    bl_description = "Radial Clone"
    bl_options = {'REGISTER', 'UNDO'}

    radialClonesAngle = FloatProperty(
        default=360.0,
        min=-360.0,
        max=360.0
    )
    clonez = IntProperty(
        default=8,
        min=2,
        max=300
    )

    def execute(self, context):

        if len(bpy.context.selected_objects) > 0:
            activeObj = bpy.context.scene.objects.active
            selObjects = bpy.context.selected_objects
            mifthTools = bpy.context.scene.mifthTools
            #self.clonez = mifthTools.radialClonesNumber

            activeObjMatrix = activeObj.matrix_world

            for i in range(self.clonez - 1):
                bpy.ops.object.duplicate(linked=True, mode='DUMMY')
                #newObj = bpy.context.selected_objects[0]
                # print(newObj)
                # for obj in bpy.context.selected_objects:
                theAxis = None

                if mifthTools.radialClonesAxis == 'X':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][0], activeObjMatrix[1][0], activeObjMatrix[2][0])
                    else:
                        theAxis = (1, 0, 0)

                elif mifthTools.radialClonesAxis == 'Y':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][1], activeObjMatrix[1][1], activeObjMatrix[2][1])
                    else:
                        theAxis = (0, 1, 0)

                elif mifthTools.radialClonesAxis == 'Z':
                    if mifthTools.radialClonesAxisType == 'Local':
                        theAxis = (activeObjMatrix[0][2], activeObjMatrix[1][2], activeObjMatrix[2][2])
                    else:
                        theAxis = (0, 0, 1)

                rotateValue = (math.radians(self.radialClonesAngle) / float(self.clonez))
                bpy.ops.transform.rotate(value=rotateValue, axis=theAxis)

            bpy.ops.object.select_all(action='DESELECT')

            for obj in selObjects:
                obj.select = True
            selObjects = None
            bpy.context.scene.objects.active = activeObj
        else:
            self.report({'INFO'}, "Select Objects!")

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)


def register():

    class MFTProperties(bpy.types.PropertyGroup):

        # Radial Clone Settings
        # radialClonesNumber = IntProperty(
            #default = 8,
            #min = 2,
            #max = 300
        #)

        radialClonesAxis = EnumProperty(
            items=(('X', 'X', ''),
                   ('Y', 'Y', ''),
                   ('Z', 'Z', '')
                   ),
            default='Z'
        )

        radialClonesAxisType = EnumProperty(
            items=(('Global', 'Global', ''),
                   ('Local', 'Local', '')
                   ),
            default='Global'
        )

    bpy.utils.register_module(__name__)

    bpy.types.Scene.mifthTools = PointerProperty(name="Mifth Tools Variables", type=MFTProperties, description="Mifth Tools Properties")


def unregister():

    del bpy.types.Scene.mifthTools

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
