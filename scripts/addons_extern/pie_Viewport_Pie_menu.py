"""
Pie menu for selecting editors and viewport with split and join functions.

Default key binding is SHIFT+SPACE. Editors are categorized, such as anim,
utils and image editors. Split the editor with the split subpie. To join,
invoke the join operation over the editor you want to keep, then click on
an adjacent editor you wish to remove. The two editors must share an edge
like normal editor joining (triple lines in editor corners).

Known issues:
Editors may become unstable if you invoke the join operation and click in
the original editor. If this occurs, merge another editor over the
troublesome editor and split off a new editor. This will return behavior
to normal.

-- italic
"""

bl_info = {
    "name": "Viewport Pie menu",
    "author": "TARDIS Maker, pitiwazou, italic",
    "version": (1, 5, 0),
    "blender": (2, 76, 0),
    "description": "A pie menu for selecting editor or viewport type, "
                   "with split and join functions.",
    "location": "Hotkey: SHIFT + Spacebar, Help: Addon file",
    "category": "Pie Menu"}

import bpy

from bpy.types import Menu, Operator
from bpy.props import IntProperty

"""
Order of pie entries (filled sequentially):
    Left
    Right
    Bottom
    Top
    Top Left
    Top Right
    Bottom Left
    Bottom Right
"""


class ViewMenu(Operator):

    bl_idname = "object.view_menu"
    bl_label = "View Menu"
    bl_options = {'INTERNAL'}
    vp = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.area.type = self.vp
        return {'FINISHED'}


class PieAreaViews(Menu):
    """Main pie layout."""

    bl_label = "Pie Views"

    def draw(self, context):
        """Draw the main pie. Up to 8 entries."""
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("wm.call_menu_pie", text="Images", icon='IMAGE_COL').name = "PieAreaViewsImage"
        pie.operator("wm.call_menu_pie", text="Anim", icon='IPO').name = "PieAreaViewsAnim"
        pie.operator("screen.screen_full_area", text="Full Screen", icon='FULLSCREEN_ENTER')
        pie.operator("object.view_menu", text="3D View", icon='VIEW3D').vp = "VIEW_3D"

        # DIAGONALS
        pie.operator("wm.call_menu_pie", text="Utils", icon='BUTS').name = "PieAreaViewsUtils"
        pie.separator()
        pie.operator("area.joinarea", text="Join", icon='X')
        pie.operator("wm.call_menu_pie", text="Split", icon='SPLITSCREEN').name = "pie.split_viewport"


class PieAreaViewsAnim(Menu):
    """Animation editors."""

    bl_label = "Anim"

    def draw(self, context):
        """Draw anim subpie."""
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("object.view_menu", text="Dope Sheet", icon='ACTION').vp = "DOPESHEET_EDITOR"
        pie.operator("object.view_menu", text="Graph Editor", icon='IPO').vp = "GRAPH_EDITOR"
        pie.operator("object.view_menu", text="NLA Editor", icon='NLA').vp = "NLA_EDITOR"
        pie.operator("object.view_menu", text="Timeline", icon='TIME').vp = "TIMELINE"


class PieAreaViewsImage(Menu):
    """Image editors."""

    bl_label = "Image"

    def draw(self, context):
        """Draw media editor subpie."""
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("object.view_menu", text="Node Editor", icon='NODETREE').vp = "NODE_EDITOR"
        pie.operator("object.view_menu", text="UV Image Editor", icon='IMAGE_COL').vp = "IMAGE_EDITOR"
        pie.operator("object.view_menu", text="Video Sequece Editor", icon='SEQUENCE').vp = "SEQUENCE_EDITOR"
        pie.operator("object.view_menu", text="Movie Clip Editor", icon='CLIP').vp = "CLIP_EDITOR"


class PieAreaViewsUtils(Menu):
    """Utility editors."""

    bl_label = "Utils"

    def draw(self, context):
        """Draw utils subpie."""
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("object.view_menu", text="Properties", icon='BUTS').vp = "PROPERTIES"
        pie.operator("object.view_menu", text="Text Editor", icon='TEXT').vp = "TEXT_EDITOR"
        pie.operator("object.view_menu", text="Python Console", icon='CONSOLE').vp = "CONSOLE"
        pie.operator("object.view_menu", text="Outliner", icon='OOPS').vp = "OUTLINER"
        pie.operator("object.view_menu", text="File Browser", icon='FILESEL').vp = "FILE_BROWSER"


class PieSplitViewport(Menu):
    """Split viewport."""

    bl_idname = "pie.split_viewport"
    bl_label = "Split Viewport"

    def draw(self, context):
        """Draw split subpie."""
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("split.vertical", text="Vertical", icon='DOWNARROW_HLT')
        pie.operator("split.horizontal", text="Horizontal", icon='RIGHTARROW')


class SplitHorizontal(Operator):
    """Split the viewport in half horizontally."""

    bl_idname = "split.horizontal"
    bl_label = "split horizontal"

    def execute(self, context):
        bpy.ops.screen.area_split(direction='HORIZONTAL')
        return {'FINISHED'}


class SplitVertical(Operator):
    """Split the viewport in half vertically."""

    bl_idname = "split.vertical"
    bl_label = "split vertical"

    def execute(self, context):
        bpy.ops.screen.area_split(direction='VERTICAL')
        return {'FINISHED'}


class JoinArea(Operator):
    """Invoke operator over editor and click on adjacent editor to join."""

    bl_idname = "area.joinarea"
    bl_label = "Join Area"
    min_x = IntProperty()
    min_y = IntProperty()

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':
            self.max_x = event.mouse_x
            self.max_y = event.mouse_y
            bpy.ops.screen.area_join(min_x=self.min_x, min_y=self.min_y,
                                     max_x=self.max_x, max_y=self.max_y)
            bpy.ops.screen.screen_full_area()
            bpy.ops.screen.screen_full_area()
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.min_x = event.mouse_x
        self.min_y = event.mouse_y
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


classes = (
    ViewMenu,
    PieAreaViews,
    PieAreaViewsAnim,
    PieAreaViewsImage,
    PieAreaViewsUtils,
    PieSplitViewport,
    SplitHorizontal,
    SplitVertical,
    JoinArea
)

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Screen')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'SPACE', 'PRESS', shift=True)
    kmi.properties.name = "PieAreaViews"
    addon_keymaps.append(km)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)
                wm.keyconfigs.addon.keymaps.remove(km)

    addon_keymaps.clear()


if __name__ == "__main__":
    register()
