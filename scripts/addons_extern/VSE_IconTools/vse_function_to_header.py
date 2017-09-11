bl_info = {
    "name": "Function to VSE Header",
    "author": "MKB",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "View3D",
    "description": "Function to VSE Header",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "VSE"}


import bpy
import os
import bpy.utils.previews
from bpy import*


class Dropdown_FTH_VSE_Props(bpy.types.PropertyGroup):
    """
    Fake module like class
    tp = context.window_manager.tp_vse_window
    """

    display_vse_view = bpy.props.BoolProperty(name="Open/Close", description="Open/Close", default=False)
    display_vse_select = bpy.props.BoolProperty(name="Open/Close", description="Open/Close", default=False)
    display_vse_move = bpy.props.BoolProperty(name="Open/Close", description="Open/Close", default=False)
    display_vse_marker = bpy.props.BoolProperty(name="Open/Close", description="Open/Close", default=False)
    display_vse_add = bpy.props.BoolProperty(name="Open/Close", description="Open/Close", default=False)
    display_vse_edit = bpy.props.BoolProperty(name="Open/Close", description="Open/Close", default=False)


bpy.utils.register_class(Dropdown_FTH_VSE_Props)
bpy.types.WindowManager.tp_vse_window = bpy.props.PointerProperty(type=Dropdown_FTH_VSE_Props)


class VSE_HEADER(bpy.types.Header):
    bl_space_type = 'SEQUENCE_EDITOR'

    @classmethod
    def poll(self, context):
        return

    def draw(self, context):
        tp = context.window_manager.tp_vse_window
        layout = self.layout

        if context.space_data.view_type in {'SEQUENCER', 'SEQUENCER_PREVIEW'}:

            icons = icon_collections["main"]

            layout.operator_context = 'INVOKE_REGION_WIN'
            layout.operator_context = 'INVOKE_REGION_PREVIEW'
            layout.operator_context = 'INVOKE_DEFAULT'

            if tp.display_vse_view:

                row = layout.row(1)
                row.operator_context = 'INVOKE_REGION_WIN'

                view_all = icons.get("view_all")
                row.operator("sequencer.view_all", text="", icon_value=view_all.icon_id)

                view_selected = icons.get("view_selected")
                row.operator("sequencer.view_selected", text="", icon_value=view_selected.icon_id)

                row = layout.row(1)

                range_clear = icons.get("range_clear")
                row.operator("anim.previewrange_clear", text="", icon_value=range_clear.icon_id)

                range_set = icons.get("range_set")
                row.operator("anim.previewrange_set", text="", icon_value=range_set.icon_id)

            if tp.display_vse_add:

                # layout.separator()

                row = layout.row(1)

                add_strips = icons.get("add_strips")
                row.menu("tp_vse.add", text="", icon_value=add_strips.icon_id)

                add_effects = icons.get("add_effects")
                row.menu("SEQUENCER_MT_add_effect", text="", icon_value=add_effects.icon_id)

            if tp.display_vse_select:

                row = layout.row(1)

                select_all_left = icons.get("select_all_left")
                props = row.operator("sequencer.select", text="", icon_value=select_all_left.icon_id)
                props.left_right = 'LEFT'
                props.linked_time = True

                select_left = icons.get("select_left")
                row.operator("sequencer.select_active_side", text="", icon_value=select_left.icon_id).side = 'LEFT'

                select_handle_left = icons.get("select_handle_left")
                row.operator("sequencer.select_handles", text="", icon_value=select_handle_left.icon_id).side = 'LEFT'

                select_handle_both = icons.get("select_handle_both")
                row.operator("sequencer.select_handles", text="", icon_value=select_handle_both.icon_id).side = 'BOTH'

                select_handle_right = icons.get("select_handle_right")
                row.operator("sequencer.select_handles", text="", icon_value=select_handle_right.icon_id).side = 'RIGHT'

                select_right = icons.get("select_right")
                row.operator("sequencer.select_active_side", text="", icon_value=select_right.icon_id).side = 'RIGHT'

                select_all_right = icons.get("select_all_right")
                props = row.operator("sequencer.select", text="", icon_value=select_all_right.icon_id)
                props.left_right = 'RIGHT'
                props.linked_time = True

            if tp.display_vse_move:

                row = layout.row(1)

                swap_left = icons.get("swap_left")
                row.operator("sequencer.swap", text="", icon_value=swap_left.icon_id).side = 'LEFT'

                row.operator("transform.transform", text="", icon="MAN_TRANS").mode = 'TRANSLATION'

                snap = icons.get("snap")
                row.operator("sequencer.snap", text="", icon_value=snap.icon_id)

                swap_right = icons.get("swap_right")
                row.operator("sequencer.swap", text="", icon_value=swap_right.icon_id).side = 'RIGHT'

                row = layout.row(1)

                row.operator("sequencer.slip", text="", icon="SNAP_INCREMENT")

                time_extend = icons.get("time_extend")
                row.operator("transform.transform", text="", icon_value=time_extend.icon_id).mode = 'TIME_EXTEND'

                clear_offset = icons.get("clear_offset")
                row.operator("sequencer.offset_clear", text="", icon_value=clear_offset.icon_id)

                row = layout.row(1)

                row.operator("sequencer.duplicate_move", text="", icon="PASTEFLIPDOWN")

            if tp.display_vse_edit:

                row = layout.row(1)

                cut_soft = icons.get("cut_soft")
                row.operator("sequencer.cut", text="", icon_value=cut_soft.icon_id).type = 'HARD'

                cut_hard = icons.get("cut_hard")
                row.operator("sequencer.cut", text="", icon_value=cut_hard.icon_id).type = 'SOFT'

                row = layout.row(1)

                gap_insert = icons.get("gap_insert")
                row.operator("sequencer.gap_insert", text="", icon_value=gap_insert.icon_id)

                gap_remove = icons.get("gap_remove")
                row.operator("sequencer.gap_remove", text="", icon_value=gap_remove.icon_id).all = False

                row = layout.row(1)

                meta_make = icons.get("meta_make")
                row.operator("sequencer.meta_make", text="", icon_value=meta_make.icon_id)

                meta_separate = icons.get("meta_separate")
                row.operator("sequencer.meta_separate", text="", icon_value=meta_separate.icon_id)

                row = layout.row(1)
                row.operator("sequencer.unmute", text="", icon="VISIBLE_IPO_ON").unselected = False
                row.operator("sequencer.mute", text="", icon="VISIBLE_IPO_OFF").unselected = False

                mute_unselected = icons.get("mute_unselected")
                row.operator("sequencer.mute", text="", icon_value=mute_unselected.icon_id).unselected = True

                row = layout.row(1)
                row.operator("sequencer.lock", text="", icon="LOCKED")
                row.operator("sequencer.unlock", text="", icon="UNLOCKED")

                row = layout.row(1)
                row.operator("sequencer.images_separate", text="", icon="RENDERLAYERS")

                deinterlace = icons.get("deinterlace")
                row.operator("sequencer.deinterlace_selected_movies", text="", icon_value=deinterlace.icon_id)
                row.operator("sequencer.rebuild_proxy", text="", icon="FILE_REFRESH")

            if tp.display_vse_marker:

                row = layout.row(1)

                marker_add = icons.get("marker_add")
                row.operator("marker.add", text="", icon_value=marker_add.icon_id)

                marker_rename = icons.get("marker_rename")
                row.operator("marker.rename", text="", icon_value=marker_rename.icon_id)

                marker_dupli = icons.get("marker_dupli")
                row.operator("marker.duplicate", text="", icon_value=marker_dupli.icon_id)

                row = layout.row(1)

                marker_jump_left = icons.get("marker_jump_left")
                row.operator("screen.marker_jump", text="", icon_value=marker_jump_left.icon_id).next = False

                marker_move = icons.get("marker_move")
                row.operator("marker.move", text="", icon_value=marker_move.icon_id)

                marker_jump_right = icons.get("marker_jump_right")
                row.operator("screen.marker_jump", text="", icon_value=marker_jump_right.icon_id).next = True

                row = layout.row(1)

                # if len(bpy.data.scenes) > 10:
                # marker_dupli_scene = icons.get("marker_dupli_scene")
                #row.operator_context = 'INVOKE_DEFAULT'
                # row.operator("marker.make_links_scene", text="", icon_value=marker_dupli_scene.icon_id)
                # else:
                # marker_dupli_scene = icons.get("marker_dupli_scene")
                #row.operator_context = 'INVOKE_DEFAULT'
                #row.operator_menu_enum("marker.make_links_scene", "scene", text="", icon_value=marker_dupli_scene.icon_id)

                marker_lock = icons.get("marker_lock")
                row.prop(bpy.context.tool_settings, "lock_markers", text="", icon_value=marker_lock.icon_id)

                marker_delete = icons.get("marker_delete")
                row.operator("marker.delete", text="", icon_value=marker_delete.icon_id)

            if tp.display_vse_edit:

                row = layout.row(1)

                strip = context.scene.sequence_editor.active_strip
                if strip:
                    stype = strip.type

                    if stype == 'EFFECT':
                        pass
                    elif stype == 'IMAGE':

                        row.operator("sequencer.rendersize", text="", icon="AXIS_TOP")
                    elif stype == 'SCENE':
                        pass
                    elif stype == 'MOVIE':
                        row.operator_context = 'INVOKE_REGION_WIN'
                        row.operator("sequencer.rendersize", text="", icon="AXIS_TOP")

                    elif stype == 'SOUND':
                        row.operator_context = 'INVOKE_REGION_WIN'
                        row.operator("sequencer.crossfade_sounds", text="", icon="SOUND")

                row = layout.row(1)
                row.operator("ed.undo", text="", icon="LOOP_BACK")
                row.operator("ed.redo", text="", icon="LOOP_FORWARDS")


class SEQUENCER_FTH_ADD(bpy.types.Menu):
    bl_label = "Add"
    bl_idname = "tp_vse.add"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("sequencer.movie_strip_add", text="Movie")
        layout.operator("sequencer.image_strip_add", text="Image")
        layout.operator("sequencer.sound_strip_add", text="Sound")

        if len(bpy.data.scenes) > 10:
            layout.operator_context = 'INVOKE_DEFAULT'
            layout.operator("sequencer.scene_strip_add", text="Scene...")
        else:
            layout.operator_menu_enum("sequencer.scene_strip_add", "scene", text="Scene...")

        if len(bpy.data.movieclips) > 10:
            layout.operator_context = 'INVOKE_DEFAULT'
            layout.operator("sequencer.movieclip_strip_add", text="Clips...")
        else:
            layout.operator_menu_enum("sequencer.movieclip_strip_add", "clip", text="Clip...")

        if len(bpy.data.masks) > 10:
            layout.operator_context = 'INVOKE_DEFAULT'
            layout.operator("sequencer.mask_strip_add", text="Masks...")
        else:
            layout.operator_menu_enum("sequencer.mask_strip_add", "mask", text="Mask...")


class Enable_All(bpy.types.Operator):
    """Enable all Icon Tools"""
    bl_idname = "tp_vse.enable_all"
    bl_label = "Enable All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_add = True
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_view = True
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_select = True
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_move = True
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_marker = True
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_edit = True

        return {'FINISHED'}


class Disable_All(bpy.types.Operator):
    """Disable all Icon Tools"""
    bl_idname = "tp_vse.disable_all"
    bl_label = "Disable All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_add = False
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_view = False
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_select = False
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_move = False
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_marker = False
        bpy.data.window_managers["WinMan"].tp_vse_window.display_vse_edit = False

        return {'FINISHED'}


def draw_item(self, context):
    tp = context.window_manager.tp_vse_window
    layout = self.layout

    layout.separator()

    layout.operator("tp_vse.enable_all", text="Enable All", icon="TRIA_RIGHT")
    layout.operator("tp_vse.disable_all", text="Disable All", icon="TRIA_LEFT")

    if tp.display_vse_add:
        layout.prop(tp, "display_vse_add", text="Icon Add")
    else:
        layout.prop(tp, "display_vse_add", text="Icon Add")

    if tp.display_vse_view:
        layout.prop(tp, "display_vse_view", text="Icon View")
    else:
        layout.prop(tp, "display_vse_view", text="Icon View")

    if tp.display_vse_select:
        layout.prop(tp, "display_vse_select", text="Icon Select")
    else:
        layout.prop(tp, "display_vse_select", text="Icon Select")

    if tp.display_vse_move:
        layout.prop(tp, "display_vse_move", text="Icon Move")
    else:
        layout.prop(tp, "display_vse_move", text="Icon Move")

    if tp.display_vse_marker:
        layout.prop(tp, "display_vse_marker", text="Icon Marker")
    else:
        layout.prop(tp, "display_vse_marker", text="Icon Marker")

    if tp.display_vse_edit:
        layout.prop(tp, "display_vse_edit", text="Icon Strip")
    else:
        layout.prop(tp, "display_vse_edit", text="Icon Strip")

    layout.label("VSE IconTools")

    layout.separator()


### Registry ###
icon_collections = {}


def register():

    mkb_icons = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    mkb_icons.load("cut_soft", os.path.join(icons_dir, "cut_soft.png"), 'IMAGE')
    mkb_icons.load("cut_hard", os.path.join(icons_dir, "cut_hard.png"), 'IMAGE')
    mkb_icons.load("gap_insert", os.path.join(icons_dir, "gap_insert.png"), 'IMAGE')
    mkb_icons.load("gap_remove", os.path.join(icons_dir, "gap_remove.png"), 'IMAGE')
    mkb_icons.load("meta_make", os.path.join(icons_dir, "meta_make.png"), 'IMAGE')
    mkb_icons.load("meta_separate", os.path.join(icons_dir, "meta_separate.png"), 'IMAGE')
    mkb_icons.load("snap", os.path.join(icons_dir, "snap.png"), 'IMAGE')
    mkb_icons.load("mute_unselected", os.path.join(icons_dir, "mute_unselected.png"), 'IMAGE')
    mkb_icons.load("deinterlace", os.path.join(icons_dir, "deinterlace.png"), 'IMAGE')
    mkb_icons.load("swap_right", os.path.join(icons_dir, "swap_right.png"), 'IMAGE')
    mkb_icons.load("swap_left", os.path.join(icons_dir, "swap_left.png"), 'IMAGE')
    mkb_icons.load("clear_offset", os.path.join(icons_dir, "clear_offset.png"), 'IMAGE')
    mkb_icons.load("time_extend", os.path.join(icons_dir, "time_extend.png"), 'IMAGE')
    mkb_icons.load("view_selected", os.path.join(icons_dir, "view_selected.png"), 'IMAGE')
    mkb_icons.load("view_all", os.path.join(icons_dir, "view_all.png"), 'IMAGE')
    mkb_icons.load("range_set", os.path.join(icons_dir, "range_set.png"), 'IMAGE')
    mkb_icons.load("range_clear", os.path.join(icons_dir, "range_clear.png"), 'IMAGE')
    mkb_icons.load("select_all_left", os.path.join(icons_dir, "select_all_left.png"), 'IMAGE')
    mkb_icons.load("select_left", os.path.join(icons_dir, "select_left.png"), 'IMAGE')
    mkb_icons.load("select_all_right", os.path.join(icons_dir, "select_all_right.png"), 'IMAGE')
    mkb_icons.load("select_right", os.path.join(icons_dir, "select_right.png"), 'IMAGE')
    mkb_icons.load("select_handle_left", os.path.join(icons_dir, "select_handle_left.png"), 'IMAGE')
    mkb_icons.load("select_handle_both", os.path.join(icons_dir, "select_handle_both.png"), 'IMAGE')
    mkb_icons.load("select_handle_right", os.path.join(icons_dir, "select_handle_right.png"), 'IMAGE')
    mkb_icons.load("add_strips", os.path.join(icons_dir, "add_strips.png"), 'IMAGE')
    mkb_icons.load("add_effects", os.path.join(icons_dir, "add_effects.png"), 'IMAGE')
    mkb_icons.load("marker_delete", os.path.join(icons_dir, "marker_delete.png"), 'IMAGE')
    mkb_icons.load("marker_dupli", os.path.join(icons_dir, "marker_dupli.png"), 'IMAGE')
    mkb_icons.load("marker_dupli_scene", os.path.join(icons_dir, "marker_dupli_scene.png"), 'IMAGE')
    mkb_icons.load("marker_add", os.path.join(icons_dir, "marker_add.png"), 'IMAGE')
    mkb_icons.load("marker_move", os.path.join(icons_dir, "marker_move.png"), 'IMAGE')
    mkb_icons.load("marker_jump_left", os.path.join(icons_dir, "marker_jump_left.png"), 'IMAGE')
    mkb_icons.load("marker_jump_right", os.path.join(icons_dir, "marker_jump_right.png"), 'IMAGE')
    mkb_icons.load("marker_lock", os.path.join(icons_dir, "marker_lock.png"), 'IMAGE')
    mkb_icons.load("marker_rename", os.path.join(icons_dir, "marker_rename.png"), 'IMAGE')

    icon_collections['main'] = mkb_icons

    bpy.utils.register_class(VSE_HEADER)
    bpy.utils.register_class(SEQUENCER_FTH_ADD)
    bpy.utils.register_class(Enable_All)
    bpy.utils.register_class(Disable_All)

    bpy.types.SEQUENCER_MT_view.prepend(draw_item)


def unregister():

    for icon in icon_collections.values():
        bpy.utils.previews.remove(icon)
    icon_collections.clear()

    bpy.utils.unregister_class(VSE_HEADER)
    bpy.utils.unregister_class(SEQUENCER_FTH_Add)
    bpy.utils.unregister_class(Enable_All)
    bpy.utils.unregister_class(Disable_All)

    bpy.types.SEQUENCER_MT_view.remove(draw_item)

if __name__ == "__main__":
    register()
