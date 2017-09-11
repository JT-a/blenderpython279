bl_info = {
    "name": "Bool Tool Plugin",
    "author": "JuhaW",
    "version": (0, 1, 0),
    "blender": (2, 77, 0),
    "location": "Tools",
    "description": "hide/parent boolean objects",
    "warning": "beta",
    "wiki_url": "",
    "category": "Object",
}


import bpy
'''
import os, sys
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
	sys.path.insert(0, parentPath)
	print (sys.path)
'''

# from . import object_bool_tool  # as BoolToolAddon

# parent boolean objects


def update_BoolParent(self, context):
    ao = context.scene.objects.active
    objs = [i.object for i in ao.modifiers if i.type == 'BOOLEAN']

    if context.scene.BoolParent:
        for o in objs:
            try:
                o.parent = ao
                o.matrix_parent_inverse = ao.matrix_world.inverted()
            except:
                pass
    else:
        for o in objs:
            ob_matrix_orig = o.matrix_world.copy()
            o.matrix_parent_inverse.identity()
            o.matrix_basis = ob_matrix_orig
            o.parent = None
        ao.update()


# Hide boolean objects
def update_BoolHide(self, context):
    ao = context.scene.objects.active
    objs = [i.object for i in ao.modifiers if i.type == 'BOOLEAN']
    bool = False
    if context.scene.BoolHide:
        bool = True

    for o in objs:
        o.hide = bool


def bool_tools_panel(self, context):

    layout = self.layout
    row = layout.row()
    row.prop(context.scene, 'BoolHide', text="Hide objects")
    row.prop(context.scene, 'BoolParent', text="Parent objects")


def register():
    # bpy.utils.register_module(__name__)
    # bpy.types.BoolToolAddon.BoolTool_Config.append(bool_tools_panel)
    # bpy.utils.register_class(BoolToolAddon.BoolTool_Config)
    bpy.types.BoolTool_BConfig.append(bool_tools_panel)

    # Scene variables
    bpy.types.Scene.BoolHide = bpy.props.BoolProperty(default=False, description='Hide boolean objects', update=update_BoolHide)
    bpy.types.Scene.BoolParent = bpy.props.BoolProperty(default=False, description='Parent boolean objects', update=update_BoolParent)


def unregister():
    # bpy.utils.unregister_module(__name__)
    # Scene variables
    del bpy.types.Scene.BoolHide
    del bpy.types.Scene.BoolParent


if __name__ == "__main__":
    register()
