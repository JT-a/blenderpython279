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
    "name": "Pie Menu",
    "author": "chromoly",
    "version": (0, 9, 3),
    "blender": (2, 78, 0),
    "location": "UserPreferences > Input > Pie Menu",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "User Interface"
}


from collections import OrderedDict
import ctypes as ct
import importlib
import inspect
import os
import sys
import time
import traceback

if "bpy" in locals():
    # importlib.reload(pie_menu)
    importlib.reload(stubs)
    importlib.reload(custom_icons)
    importlib.reload(oputils)
    importlib.reload(operators)
    importlib.reload(menu_items)
    # importlib.reload(draw_ui)
    importlib.reload(preferences)
    # importlib.reload(menu_item)
    importlib.reload(drawicon)
    importlib.reload(draw)
    # importlib.reload(pie_menu)
    PieMenuPreferences.reload_submodules()

import bpy
from mathutils import Vector
import bgl

from ..utils import structures as st
from ..utils import vagl

try:
    import pie_menu
except:
    pie_menu = None

from . import stubs
from . import custom_icons
from . import oputils
from . import operators
from . import menu_items
# from . import draw_ui
from . import preferences
# from . import menu_item
from . import drawicon
from . import draw
# from . import pie_menu

from .stubs import gen_screenshot_texture, draw_texture, cross2d
from .preferences import PieMenu, PieMenu_PG_Colors, PieMenuPreferences
from .draw import DrawingManager


DISABLE_CROSS_CURSOR = True

TOOLTIP_TIME = 0.4


def regionruler_disable(context):
    try:
        import ctools.regionruler as regionruler
        u = context.user_preferences
        p = u.addons["ctools"].preferences.get_instance("regionruler")
        regionruler_disable.draw_cross_cursor = p.draw_cross_cursor
        simple_measure = regionruler.data.simple_measure
        regionruler.data.simple_measure = False
        regionruler.data.measure_points.clear()

        if DISABLE_CROSS_CURSOR and (regionruler_disable.draw_cross_cursor or
                                     simple_measure):
            if not context.screen.is_animation_playing:
                p.draw_cross_cursor = False
                if context.area.type in ('VIEW_3D', 'IMAGE_EDITOR'):
                    if context.region.type == 'WINDOW':
                        context.region.tag_redraw()
    except:
        # traceback.print_exc()
        pass


def regionruler_restore(context):
    try:
        u = context.user_preferences
        p = u.addons["ctools"].preferences.get_instance("regionruler")
        p.draw_cross_cursor = regionruler_disable.draw_cross_cursor
    except:
        pass


def is_overlap_region(context, area, region):
    u = context.user_preferences
    if u.system.use_region_overlap:
        if u.system.window_draw_method in {'AUTOMATIC', 'TRIPLE_BUFFER'}:
            if 'WM_is_draw_triple(context.window)':
                if area.type in {'VIEW_3D', 'SEQUENCE_EDITOR'}:
                    if region.type in {'TOOLS', 'UI', 'TOOL_PROPS'}:
                        return True
                elif area.type == 'IMAGE_EDITOR':
                    if region.type in {'TOOLS', 'UI', 'TOOL_PROPS',
                                       'PREVIEW'}:
                        return True
    return False


def has_overlap_regions(context):
    for area in context.screen.areas:
        for region in area.regions:
            if region.id != 0:
                if is_overlap_region(context, area, region):
                    return True
    return False


space_types = {
    'CLIP_EDITOR': bpy.types.SpaceClipEditor,
    'CONSOLE': bpy.types.SpaceConsole,
    'DOPESHEET_EDITOR': bpy.types.SpaceDopeSheetEditor,
    'EMPTY': None,
    'FILE_BROWSER': bpy.types.SpaceFileBrowser,
    'GRAPH_EDITOR': bpy.types.SpaceGraphEditor,
    'IMAGE_EDITOR': bpy.types.SpaceImageEditor,
    'INFO': bpy.types.SpaceInfo,
    'LOGIC_EDITOR': bpy.types.SpaceLogicEditor,
    'NLA_EDITOR': bpy.types.SpaceNLA,
    'NODE_EDITOR': bpy.types.SpaceNodeEditor,
    'OUTLINER': bpy.types.SpaceOutliner,
    'PROPERTIES': bpy.types.SpaceProperties,
    'SEQUENCE_EDITOR': bpy.types.SpaceSequenceEditor,
    'TEXT_EDITOR': bpy.types.SpaceTextEditor,
    'TIMELINE': bpy.types.SpaceTimeline,
    'USER_PREFERENCES': bpy.types.SpaceUserPreferences,
    'VIEW_3D': bpy.types.SpaceView3D,
}


def is_timer_event(event, timer):
    """
    :type event: bpy.types.Event
    :type timer: bpy.types.Timer
    :rtype: bool
    """
    ev = st.wmEvent.cast(event)
    return event.type == 'TIMER' and ev.customdata == timer.as_pointer()


###############################################################################
# Operator
###############################################################################
class WM_OT_pie_menu_exec(bpy.types.Operator):
    bl_idname = "wm.pie_menu_exec"
    bl_label = "Pie Menu Exec"
    bl_description = ""
    bl_options = {'INTERNAL'}

    item = None
    result = None

    def invoke(self, context, event):
        cls = self.__class__
        item = cls.item
        try:
            cls.result = item.execute(context, event)
        except:
            err = traceback.format_exc()
            print(err)
            self.report({'ERROR'}, err)
            cls.result = None
            # return {'CANCELLED'}
        return {'FINISHED'}


class WM_OT_pie_menu_exec_register(bpy.types.Operator):
    bl_idname = "wm.pie_menu_exec_register"
    bl_label = "Pie Menu Exec"
    bl_description = ""
    bl_options = {'REGISTER', 'INTERNAL'}

    item = None
    result = None

    def invoke(self, context, event):
        cls = self.__class__
        item = cls.item
        try:
            cls.result = item.execute(context, event)
            # 履歴のメッセージを任意の物にする為、bl_optionsには'UNDO'を入れずに
            # ここでundo_push()を行う。
            bpy.ops.ed.undo_push(message=item.label)
        except:
            err = traceback.format_exc()
            print(err)
            self.report({'ERROR'}, err)
            cls.result = None
            # return {'CANCELLED'}
        return {'FINISHED'}


dm = DrawingManager(None, None)


class WM_OT_pie_menu(bpy.types.Operator):
    bl_idname = "wm.pie_menu"
    bl_label = "Pie Menu"
    bl_description = ""

    bl_options = {'INTERNAL'}

    menu = bpy.props.StringProperty(
        name="Menu",
        description="Menu idname")
    """:type: str"""

    def __init__(self):
        self.base_menu = None
        """:type: PieMenu"""

        self.timer = None
        """:type: bpy.types.Timer"""

        self.dpi = bpy.context.user_preferences.system.dpi

        self.mco = None  # <Vector>
        """:type: mathutils.Vector"""
        self.mco_left = None  # <Vector>
        self.mco_middle = None  # <Vector>
        self.mco_right = None  # <Vector>

        self.mco_left_prev = None  # <Vector>
        self.mco_middle_prev = None  # <Vector>
        self.mco_right_prev = None  # <Vector>

        self.shift = False
        self.ctrl = False
        self.alt = False
        self.oskey = False

        self.running_modal = False

        self.event_type = ''  # 起動時のevent.type
        self.last_action_time = time.perf_counter()
        self.show_tooltip = False
        self.mco_tooltip = None  # <Vector>
        self.moving = False

        # {event.type: {"mco": Vector2D, "shift": bool, ...}, ...}
        self.event_history = OrderedDict()

        self.menu_history = []  # [(idname, label), ...]

        self.texture = None  # <int>
        self.handles = []  # [(handle, area type, region type), ...]
        self.region_tex = None  # <bpy.types.Region>
        self.region_pie = None  # <bpy.types.Region>

    # Draw Callback -----------------------------------------------------------
    def area_from_region(self, region):
        for area in region.id_data.areas:
            for r in area.regions:
                if r == region:
                    return area

    def draw_callback(self, context, region_tex=None, region_pie=None):
        win = context.window
        area = context.area
        region = context.region

        # regions = []
        # for sa in context.screen.areas:
        #     for ar in sa.regions:
        #         regions.append(ar)
        # print(regions.index(region), area.type, region.type)

        glsettings = vagl.GLSettings(context)

        if not is_overlap_region(context, area, region):
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.texture)
            bgl.glCopyTexSubImage2D(
                bgl.GL_TEXTURE_2D, 0, region.x, region.y,
                region.x, region.y, region.width, region.height)
            # bgl.glFlush()
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)

        if region == region_tex:
            with glsettings.push_attrib():
                with glsettings.window_pixel_space():
                    bgl.glDisable(bgl.GL_SCISSOR_TEST)
                    draw_texture(0, 0, win.width, win.height,
                                 self.texture)

        area_pie = self.area_from_region(region_pie)
        regions_pie = list(area_pie.regions)
        if region == region_pie:
            with glsettings.push_attrib():
                with glsettings.window_pixel_space():
                    bgl.glDisable(bgl.GL_SCISSOR_TEST)
                    dm.draw(context)
        elif region in regions_pie:
            if regions_pie.index(region) > regions_pie.index(region_pie):
                with glsettings.push_attrib():
                    with glsettings.window_pixel_space():
                        dm.draw(context)

    def gen_texture(self, context):
        win = context.window
        w, h = win.width, win.height
        self.texture = gen_screenshot_texture(0, 0, w, h)

    def delete_textures(self):
        buf = bgl.Buffer(bgl.GL_INT, 1, [self.texture])
        bgl.glDeleteTextures(1, buf)

    def draw_handler_add(self, context):
        area_tex = region_tex = None
        area_pie = region_pie = None

        has_overlap = has_overlap_regions(context)
        for area in context.screen.areas:
            for region in area.regions:
                if region.id != 0:
                    if has_overlap:
                        if is_overlap_region(context, area, region):
                            area_pie = area
                            region_pie = region
                    else:
                        area_pie = area
                        region_pie = region
                    if not area_tex:
                        area_tex = area
                        region_tex = region

        if region_pie.type == 'WINDOW':
            for region in area_pie.regions:
                if region.id != 0:
                    if region.type != 'WINDOW':
                        region_pie = region

        self.draw_handler_remove()

        added = set()
        for area in context.screen.areas:
            for region in area.regions:
                if region.id != 0:
                    key = (area.type, region.type)
                    if key in added:
                        continue
                    handle = area.spaces.active.draw_handler_add(
                        self.draw_callback,
                        (context, region_tex, region_pie),
                        region.type, 'POST_PIXEL')

                    self.handles.append((handle, area.type, region.type))
                    added.add(key)

        self.region_tex = region_tex
        self.region_pie = region_pie

        """
        NOTE: Call draw handler

        addr = region.as_pointer()
        ar = cast(c_void_p(addr), POINTER(ARegion)).contents
        art = ar.type
        lb = art.contents.drawcalls
        handle = area.spaces.active.draw_handler_add(
            self.draw_callback_tex, (context,), region.type,
            'POST_PIXEL')
        func = ctypes.pythonapi.PyCapsule_GetPointer
        func.restype = c_void_p
        p = func(ctypes.py_object(handle), b'RNA_HANDLE')
        print('handle', p)
        print('listbase', lb.first, lb.last)
        """

    def draw_handler_remove(self):
        for handle, area_type, region_type in self.handles:
            space = space_types[area_type]
            space.draw_handler_remove(handle, region_type)
        self.handles.clear()

    @classmethod
    def redraw_all(cls, context):
        for area in context.screen.areas:
            area.tag_redraw()

    def redraw(self, context, init=False):
        self.region_tex.tag_redraw()
        self.region_pie.tag_redraw()
        if init:
            for area in context.screen.areas:
                for region in area.regions:
                    if is_overlap_region(context, area, region):
                        area.tag_redraw()
                        continue

    # Event -------------------------------------------------------------------
    def event_history_update(self, event):
        """
        :type event: bpy.types.Event
        """
        mco = Vector((event.mouse_x, event.mouse_y))
        values = {key: getattr(event, key)
                  for key in ("shift", "ctrl", "alt", "oskey")}
        values["mco"] = mco
        if event.value == 'PRESS':
            if event.type in self.event_history:
                self.event_history.move_to_end(event.type)
            self.event_history[event.type] = values
        elif event.value == 'RELEASE':
            if event.type in self.event_history:
                del self.event_history[event.type]

    def modifiers_update(self, event):
        """Update self.shift, self.ctrl
        :type event: bpy.types.Event
        :return: is attribute value changed
        :rtype: bool
        """
        shift_bak = self.shift
        ctrl_bak = self.ctrl
        alt_bak = self.alt
        oskey_bak = self.oskey
        if event.type in {'LEFT_SHIFT', 'RIGHT_SHIFT'}:
            if event.value == 'PRESS':
                self.shift = True
            elif event.value == 'RELEASE':
                self.shift = False
        elif event.type in {'LEFT_CTRL', 'RIGHT_CTRL'}:
            if event.value == 'PRESS':
                self.ctrl = True
            elif event.value == 'RELEASE':
                self.ctrl = False
        elif event.type in {'LEFT_ALT', 'RIGHT_ALT'}:
            if event.value == 'PRESS':
                self.alt = True
            elif event.value == 'RELEASE':
                self.alt = False
        elif event.type in {'LEFT_OSKEY', 'RIGHT_OSKEY'}:
            if event.value == 'PRESS':
                self.oskey = True
            elif event.value == 'RELEASE':
                self.oskey = False
        return (self.shift != shift_bak or self.ctrl != ctrl_bak or
                self.alt != alt_bak or self.oskey != oskey_bak)

    def last_modifier(self):
        pressed = []
        for key in self.event_history:
            for mod in ["SHIFT", "CTRL", "ALT", "OSKEY"]:
                if key in {'LEFT_' + mod, 'RIGHT_' + mod}:
                    pressed.append(mod)
        if pressed:
            return pressed[-1].lower()
        else:
            return ""

    def mouse_update(self, event):
        """update mouse coorfinates
        """
        self.mco = mco = Vector((event.mouse_x, event.mouse_y))

        self.mco_left_prev = self.mco_left
        self.mco_middle_prev = self.mco_middle
        self.mco_right_prev = self.mco_right

        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                self.mco_left = mco.copy()
            elif event.value == 'RELEASE':
                self.mco_left = None
        elif event.type == 'MIDDLEMOUSE':
            if event.value == 'PRESS':
                self.mco_middle = mco.copy()
            elif event.value == 'RELEASE':
                self.mco_middle = None
        elif event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                self.mco_right = mco.copy()
            elif event.value == 'RELEASE':
                self.mco_right = None

    def set_menu(self, context, idname, co=None):
        addon_prefs = PieMenuPreferences.get_instance()

        if co is None:
            co = self.base_menu.co

        menu = pie_menu.get_menu(idname)
        """:type: PieMenu"""
        if not menu:
            self.report({'ERROR'}, "Menu '{}' not fond".format(idname))
            return None

        if inspect.isclass(menu):
            menu = PieMenu(menu())
        else:
            menu = PieMenu(menu)

        if not menu.poll(context):
            return False

        self.base_menu = menu

        menu.init(context)
        menu.co = co
        menu.update_current_items(context, self)
        menu.correct_radius()
        menu.update_active(self.mco, self.mco_left)
        return True

    def modal(self, context, event):
        """
        LEFTMOUSEはRELEASE、それ以外はPRESSで確定する。
        """
        # if event.type != 'TIMER':
        #     print(event.type, event.value)
        if self.running_modal:
            if not event.type.startswith("TIMER"):
                return {'FINISHED', 'PASS_THROUGH'}

        if (event.type == 'INBETWEEN_MOUSEMOVE' or
                event.type == 'MOUSEMOVE' and
                event.mouse_x == event.mouse_prev_x and
                event.mouse_y == event.mouse_prev_y):
            return {'RUNNING_MODAL'}

        # イベント履歴
        event_history_bak = self.event_history.copy()
        self.event_history_update(event)

        dm.update(context, self)

        addon_prefs = PieMenuPreferences.get_instance()
        wm = context.window_manager
        win = context.window
        current_time = time.perf_counter()

        menu = self.base_menu

        # マウス関連
        self.mouse_update(event)
        mco = self.mco

        # 修飾キー属性更新
        do_update_current_items = self.modifiers_update(event)

        item_index = menu.active_index

        # メニューの各属性を更新・再計算
        if do_update_current_items:
            menu.update_current_items(context, self)
        menu.update_active(self.mco, self.mco_left_prev)

        # tooltip描画の判定
        if event.type.startswith('TIMER'):
            pass
        elif event.type == 'MOUSEMOVE':
            if (self.show_tooltip and item_index == menu.active_index):
                pass
            else:
                self.last_action_time = current_time
        elif event.value == 'PRESS' and event.type in event_history_bak:
            # キーリピートは無視する
            pass
        else:
            self.last_action_time = current_time

        if menu.active_index == -1:
            show_tooltip = False
        else:
            show_tooltip = (current_time - self.last_action_time >=
                            TOOLTIP_TIME)
        if show_tooltip:
            if not self.show_tooltip:
                self.mco_tooltip = mco.copy()
            self.show_tooltip = True
        else:
            self.show_tooltip = False

        # Confirm -------------------------------------------------------------
        confirm = False
        click = False
        release = False
        active_item = None
        item_shortcuts = {item.shortcut if item else ''
                          for item in menu.current_items}
        if event.type == self.event_type and event.value == 'RELEASE':
            if menu.is_valid_click:
                confirm = True
                release = True
            self.event_type = ''
        elif (event.type == 'LEFTMOUSE' and event.value == 'RELEASE' and
              'LEFTMOUSE' in event_history_bak):
            if menu.is_valid_click:
                confirm = True
                click = True
        if not confirm:
            for item in menu.current_items:
                if item and item.shortcut:
                    if event.type == item.shortcut and event.value == 'PRESS':
                        confirm = True
                        active_item = item
                        if 0:
                            self.event_type = event.type
                            self.hack_lock_pie_event(context, event.type)
                        break
        if not confirm:
            if (event.type in {'SPACE', 'RET', 'NUMPAD_ENTER'} and
                    event.value == 'PRESS'):
                shortcuts = [item.shortcut for item in menu.current_items
                             if item and item.shortcut]
                if event.type not in shortcuts:
                    confirm = True

        if confirm and not active_item:
            if menu.active_item_index != -1:
                if menu.quick_action == 'NONE' and menu.active_index == -1:
                    pass
                else:
                    active_item = menu.current_items[menu.active_item_index]

        if confirm and active_item:
            retval = None

            if active_item.enabled:
                menu.set_last_item_direction(active_item.direction)
                modal_handlers_pre = st.wmWindow.modal_handlers(win)

                if active_item.undo_push:
                    WM_OT_pie_menu_exec_register.item = active_item
                    bpy.ops.wm.pie_menu_exec_register('INVOKE_DEFAULT',
                                                      True)
                    result = WM_OT_pie_menu_exec_register.result
                else:
                    WM_OT_pie_menu_exec.item = active_item
                    bpy.ops.wm.pie_menu_exec('INVOKE_DEFAULT', True)
                    result = WM_OT_pie_menu_exec.result

                modal_handlers_post = st.wmWindow.modal_handlers(win)
                # running_modal = (ct.addressof(modal_handlers_pre[0][0]) !=
                #                  ct.addressof(modal_handlers_post[0][0]))
                running_modal = (len(modal_handlers_pre) !=
                                 len(modal_handlers_post))

                if active_item.menu or isinstance(result, str):
                    if active_item.menu:
                        sub_menu = active_item.menu
                    else:
                        sub_menu = result

                    co = None if addon_prefs.lock_menu_location else mco
                    menu_test = self.set_menu(context, sub_menu, co)
                    if menu_test is None:
                        retval = {'FINISHED'}
                    elif not menu_test:  # poll_()の結果がFalse
                        pass
                    else:
                        self.menu_history.append((menu.idname, menu.label))
                # elif self.test_grab_cursor(context):
                #     self.running_modal = True
                #     retval = {'RUNNING_MODAL'}
                elif running_modal:
                    self.running_modal = True
                    retval = {'RUNNING_MODAL'}
                else:
                    retval = {'FINISHED'}
            else:
                if not click:
                    # menu.set_last_item_direction('NONE')
                    retval = {'CANCELLED'}

            if retval is not None:
                self.draw_handler_remove()
                self.delete_textures()
                wm.event_timer_remove(self.timer)
                regionruler_restore(context)
                self.redraw_all(context)
                return retval
            else:
                # areaやregionに変更が加えられた可能性があるので更新する
                self.draw_handler_add(context)

        # Cancel --------------------------------------------------------------
        cancel = False
        if event.type == 'RIGHTMOUSE':
            cancel = True
        elif event.type == 'ESC':
            if event.type not in item_shortcuts:
                cancel = True
        elif confirm and not active_item:
            if release and menu.active_index != -1:
                cancel = True
        #     pass
        # elif confirm and menu.quick_action != 'NONE' and not active_item:
        #     if menu.active_index == -1:
        #         cancel = True

        if cancel:
            self.draw_handler_remove()
            self.delete_textures()
            wm.event_timer_remove(self.timer)
            regionruler_restore(context)
            self.redraw_all(context)
            return {'CANCELLED'}

        # 移動
        if self.mco_middle and self.shift:
            menu.co = mco.copy()
            menu.update_active(self.mco, self.mco_left)
            menu.is_valid_click = False

        # 次/前のメニュー
        elif event.type in ('WHEELUPMOUSE', 'WHEELDOWNMOUSE'):
            if event.type == 'WHEELUPMOUSE':
                if menu.prev:
                    self.set_menu(context, menu.prev)
            elif event.type == 'WHEELDOWNMOUSE':
                if menu.next:
                    self.set_menu(context, menu.next)

        # 親メニューへ
        elif (event.type == 'MIDDLEMOUSE' and event.value == 'PRESS' and
              not self.shift):
            if self.menu_history:
                idname, label = self.menu_history.pop(-1)
                # if prefs.lock_menu_location:
                #     self.set_menu(context, parent)
                # else:
                #     self.set_menu(context, parent, mco)
                self.set_menu(context, idname)

        # 無駄な再描画をしない
        if 0:  # ScreenCastKeysで描画されない問題が起こる
            if event.type == 'TIMER':
                t = current_time - self.last_action_time
                if t < TOOLTIP_TIME or t > TOOLTIP_TIME + 0.5:
                    return {'RUNNING_MODAL'}

        dm.update(context, self)

        self.redraw(context)

        return {'RUNNING_MODAL'}

    @staticmethod
    def hack_lock_pie_event(context, event_type):
        items = bpy.types.Event.bl_rna.properties['type'].enum_items
        # NOTE: get(name)はEnumPropertyItemを、find(name)はインデックスを得る
        value = items.get(event_type).value
        win = st.wmWindow.cast(context.window)
        win.lock_pie_event = value

    def invoke(self, context, event):
        oputils.events[context.window.as_pointer()] = event
        pie_menu.addon_preferences = PieMenuPreferences.get_instance()
        wm = context.window_manager
        if not self.menu or not pie_menu.get_menu(self.menu):
            self.report({'ERROR'}, "menu '{}' not found".format(self.menu))
            return {'CANCELLED'}

        self.event_type = event.type

        # ctypes
        if event.type in {'LEFTMOUSE'}:
            self.hack_lock_pie_event(context, 'NONE')
        else:
            self.hack_lock_pie_event(context, event.type)

        dm.update(context, self)

        self.mouse_update(event)
        self.modifiers_update(event)
        self.event_history_update(event)

        self.menu_history.clear()

        menu_test = self.set_menu(context, self.menu, self.mco)
        if menu_test is None:
            self.report({'ERROR'}, "menu '{}' not found".format(self.menu))
            return {'CANCELLED'}

        elif not menu_test:  # poll_()でFalseを返す
            return {'CANCELLED', 'PASS_THROUGH'}

        wm.modal_handler_add(self)

        self.gen_texture(context)
        self.draw_handler_add(context)

        self.timer = wm.event_timer_add(0.1, context.window)

        regionruler_disable(context)

        context.area.tag_redraw()
        self.redraw(context, True)

        return {'RUNNING_MODAL'}


classes = [
    WM_OT_pie_menu,
    WM_OT_pie_menu_exec,
    WM_OT_pie_menu_exec_register,

    PieMenu_PG_Colors,
    PieMenuPreferences,
]


@PieMenuPreferences.register_addon
def register():
    operators.register()
    for cls in classes:
        bpy.utils.register_class(cls)

    custom_icons.register()

    addon_prefs = PieMenuPreferences.get_instance()
    if pie_menu:
        pie_menu.addon_preferences = addon_prefs
        # pie_menu.register_addon(PieMenuPreferences.get_instance())

    # Enable all sub modules if not disabled
    for name, mod in PieMenuPreferences._fake_submodules_.items():
        key = "use_" + name
        if key not in addon_prefs.addons:
            setattr(addon_prefs.addons, key, True)


@PieMenuPreferences.unregister_addon
def unregister():
    if pie_menu:
        # pie_menu.unregister_addon(PieMenuPreferences.get_instance())
        pie_menu.addon_preferences = None

    custom_icons.unregister()

    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
    operators.unregister()
    drawicon.unregister()  # delete textures
