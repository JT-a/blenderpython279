import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty, StringProperty, CollectionProperty
from bpy.types import PropertyGroup

def GetVertexGroups(scene, context):

    items = [
        ("1", "None",  "", 0),
    ]

    ob = bpy.context.active_object
    u = 1

    for i,x in enumerate(ob.vertex_groups):

        items.append((str(i+1), x.name, x.name))

    return items

class PS_Properties(PropertyGroup):

    update_toggle = BoolProperty(
        name = "Update Toggle",
        description = "Prevents recursion loops in specific, multi-select operations",
        default = False)
