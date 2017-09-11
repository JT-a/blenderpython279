bl_info = {
    "name": "Node Group Libraries",
    "author": "Nathan Craddock",
    "blender": (2, 76, 0),
    "description": "Automatically links or appends nodegroups from a library .blend file",
    "support": 'COMMUNITY',
    "category": "Node"
}

import bpy
from bpy.app.handlers import persistent
from bpy.props import StringProperty, BoolProperty
from bpy.types import Panel, Operator

#############
# FUNCTIONS #
#############


@persistent
def import_node_groups(dummy):
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[__name__].preferences

    path = bpy.path.abspath(addon_prefs.library_path)
    link = addon_prefs.link

    # Scan a library file for node groups and append those that don't exist yet
    blend_node_groups = bpy.data.node_groups

    with bpy.data.libraries.load(path, link) as (data_from, data_to):
        data_to.node_groups = [group for group in data_from.node_groups if group not in blend_node_groups]
        print("Imported Node Groups")


#############
# OPERATORS #
#############

class NGLRefresh(Operator):
    bl_label = "Refresh"
    bl_idname = "ngl.refresh"
    bl_description = "Relinks the nodes from the library file (saves and reloads)"

    # A huge thanks to Pablo Vazquez
    # for the code from Amaranth (https://github.com/venomgfx/amaranth)

    def save_reload(self, context, path):
        if not path:
            bpy.ops.wm.save_as_mainfile("INVOKE_AREA")
            return
        bpy.ops.wm.save_mainfile()
        self.report({"INFO"}, "Saved & Reloaded")
        bpy.ops.wm.open_mainfile("EXEC_DEFAULT", filepath=path)

    def execute(self, context):
        path = bpy.data.filepath
        self.save_reload(context, path)
        return {"FINISHED"}


######
# UI #
######

class NGLSettings(bpy.types.AddonPreferences):
    bl_idname = __name__

    library_path = StringProperty(
        name="NodeGroup Library Path",
        description="Location for the node group .blend file",
        subtype='FILE_PATH',
    )

    link = BoolProperty(
        name="Link Groups",
        description="Link the node groups from the library",
        default=True,
    )

    def draw(self, context):
        layout = self.layout

        self.library_path = bpy.path.abspath(self.library_path)

        layout.prop(self, 'library_path')
        layout.prop(self, 'link')
        layout.operator('ngl.refresh')

        layout.separator()

        layout.label(text="Make sure to save user settings for persistent Node Groups!", icon="ERROR")


class NGLPanel(Panel):
    bl_label = "Node Group Library"
    bl_idname = "NGLibrary-panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        layout.operator('ngl.refresh')


def register():
    bpy.utils.register_module(__name__)

    bpy.app.handlers.load_post.append(import_node_groups)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
