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
    "name": "Restrict Object",
    "author": "Omar Ahmed",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "Scene panel",
    "description": "Enable/Disable viewport visibility,selection and rendering based on restrict options",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}


import bpy
from bpy.props import EnumProperty, BoolProperty


class RestrictObject(bpy.types.Operator):
    """Restrict Object visability"""
    bl_idname = "object.restrict_object"
    bl_label = "Restrict Object"
    bl_options = {'UNDO', 'REGISTER'}

    Operation_boolean = BoolProperty(name="Disable", description="Disable selected property based on the other selected property", default=True)
    Operation_list = EnumProperty(items=[('Viewport visibility', 'Viewport visibility', 'viewport visibility'),
                                         ('Viewport selection', 'Viewport selection', 'viewport selection'),
                                         ('Rendering', 'Rendering', 'Rendering')],
                                  name="Property",
                                  description="Select the property you want to change",
                                  default="Rendering")
    Original_boolean = BoolProperty(name="Disabled", description="The original property", default=True)
    Property_list = EnumProperty(items=[('Viewport visibility', 'Viewport visibility', 'viewport visibility'),
                                        ('Viewport selection', 'Viewport selection', 'viewport selection'),
                                        ('Rendering', 'Rendering', 'Rendering')],
                                 name="Original property",
                                 description="Select the property in which the operation will be based on",
                                 default="Viewport visibility")

    def execute(self, context):

        op_dict = {
            "Viewport visibility": "hide",
            "Viewport selection": "hide_select"
        }

        # if self.operation_list is not explicitely mentioned in op_dict above
        # using .get() will return 'hide_render' instead.
        Restricted_property = op_dict.get(self.Operation_list, 'hide_render')
        Original_property = op_dict.get(self.Property_list, 'hide_render')

        for object in bpy.context.scene.objects:
            if getattr(object, Original_property) == self.Original_boolean:
                setattr(object, Restricted_property, self.Operation_boolean)

        return {'FINISHED'}


class RestrictObjectPanel(bpy.types.Panel):
    """Restrict Object Panel"""
    bl_idname = "SCENE_PT_Restrict_Object"
    bl_label = "Restrict Object Panel"

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        layout = self.layout
        layout.operator(RestrictObject.bl_idname, text="Restrict object", icon='FILE_REFRESH')


def register():
    bpy.utils.register_class(RestrictObject)
    bpy.utils.register_class(RestrictObjectPanel)


def unregister():
    bpy.utils.unregister_class(RestrictObject)
    bpy.utils.unregister_class(RestrictObjectPanel)


if __name__ == "__main__":
    register()
