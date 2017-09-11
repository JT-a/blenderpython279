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
    'name': 'Print Hook',
    'author': 'chromoly',
    'version': (0, 1),
    'blender': (2, 76, 0),
    'location': '',
    'description': '',
    'wiki_url': '',
    'category': '3D View'
}


import sys
import traceback
import os
import tempfile
import threading
import stat
import platform
import ctypes
import ctypes.util

import bpy

from .addonutils.utils import AddonPreferences, operator_call


class PrintHookPreferences(
        AddonPreferences,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    stdout_text = bpy.props.StringProperty(
        name='StdOut',
        default='sys.stdout',
    )
    history_text = bpy.props.StringProperty(
        name='Operator History',
        default='operator_history',
    )
    max_text_size = bpy.props.IntProperty(
        name='Max Log Size',
        default=500,
        min=100,
        max=10000,
    )

    log_file = bpy.props.StringProperty(
        name='Log File',
        default='blender_stdout.txt',
        subtype='FILE_PATH',
    )
    max_log_file_size = bpy.props.IntProperty(
        name='Max Log File Size',
        default=500,
        min=100,
        max=10000,
    )

    encoding = bpy.props.StringProperty(
        name='Encoding',
        default='utf-8',
    )
    PIXEL_SIZE = bpy.props.FloatProperty(
        name='PIXEL_SIZE',
        default=1.0,
        min=1.0,
        max=5.0
    )

    def draw(self, context):
        layout = self.layout
        """:type: bpy.types.UILayout"""
        split = layout.split()

        col = split.column()
        col.prop(self, 'stdout_text')
        col.prop(self, 'history_text')
        col.prop(self, 'max_text_size')

        col = split.column()
        col.prop(self, 'log_file')
        path = self.log_file
        if not os.path.isabs(path):
            path = os.path.join(bpy.utils.resource_path('USER'), path)
        col.label(path)
        col.prop(self, 'max_log_file_size')

        col = split.column()
        col.prop(self, 'encoding')
        col.prop(self, 'PIXEL_SIZE')


def get_widget_unit(context):
    prefs = PrintHookPreferences.get_instance()
    PIXEL_SIZE = prefs.PIXEL_SIZE
    # U.widget_unit = (U.pixelsize * U.dpi * 20 + 36) / 72;
    U = context.user_preferences
    if U.system.virtual_pixel_mode == 'NATIVE':
        pixel_size = PIXEL_SIZE * 1.0
    else:  # 'DOUBLE'
        pixel_size = PIXEL_SIZE * 2.0
    dpi = U.system.dpi
    return int((pixel_size * dpi * 20 + 36) / 72)


def calc_space_values(context, space):
    widget_unit = get_widget_unit(context)
    lheight = space.font_size
    lheight_dpi = int((widget_unit * lheight) / 20)
    TXT_OFFSET = int(0.5 * widget_unit)
    TXT_LINE_SPACING = int(0.3 * lheight_dpi)  # space between lines

    d = {'widget_unit': widget_unit,
         'lheight': lheight,
         'lheight_dpi': lheight_dpi,
         'TXT_OFFSET': TXT_OFFSET,
         'TXT_LINE_SPACING': TXT_LINE_SPACING,
         'line_height': lheight_dpi + TXT_LINE_SPACING,  # 一行の高さ表す
         }
    return d


def region_location_from_cursor(context, space, line, column):
    """SpaceTextEditor.region_location_from_cursorのバグ修正した値を返す

    editors/space_text/text_draw.c: ED_text_region_location_from_cursor
    - r_pixel_co[1] = (ar->winy - (r_pixel_co[1] + TXT_OFFSET)) - st->lheight_dpi;
    + r_pixel_co[1] = ar->winy - r_pixel_co[1] - (st->lheight_dpi + TXT_LINE_SPACING) / 2;

    :type context: bpy.types.Context
    :type space: bpy.types.SpaceTextEditor
    :type line: int
    :type column: int
    :return: カーソルの中心のregion座標
    :rtype: (int, int)
    """

    loc = space.region_location_from_cursor(line, column)
    if loc == (-1, -1):
        return loc

    d = calc_space_values(context, space)
    y = loc[1] + d['TXT_OFFSET'] + d['lheight_dpi']  # 余計な計算を戻す
    y -= d['line_height'] / 2

    return loc[0], y


def get_text(history=False, new=True):
    """
    :param history:
    :type history: bool
    :param new: 無ければ作成
    :type new: bool
    :rtype: bpy.types.Text
    """
    prefs = PrintHookPreferences.get_instance()
    name = prefs.history_text if history else prefs.stdout_text
    if not name:
        return None
    if name not in bpy.data.texts and new:
        bpy.data.texts.new(name)
    return bpy.data.texts[name]


def get_log_file():
    prefs = PrintHookPreferences.get_instance()
    if prefs.log_file:
        try:
            p = os.path.abspath(prefs.log_file)
            return open(p, 'r+', encoding='utf-8')
        except:
            pass
    return None


def get_platform():
    """ 'linux', 'windows', 'darwin', """
    return platform.platform().split('-')[0].lower()


if get_platform() == 'windows':
    kernel32 = ctypes.WinDLL('kernel32')
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12


class OutputStream:
    """sys.stdout, sys.stderrをこれに置き換えておく"""
    def __init__(self, mode, use_mkstemp=True):
        self.mode = mode
        self.use_mkstemp = use_mkstemp
        self.stdout = self.stderr = self.excepthook = None
        self.begin()

    # def __call__(self, type, value, tb):
    #     """例外 sys.excepthook 用"""
    #     msg = ''.join(traceback.format_exception(type, value, tb))
    #     self.write(msg)

    # def write(self, string):
    #     context = bpy.context
    #     U = context.user_preferences
    #     prefs = PrintHookPreferences.get_instance()
    #
    #     # 標準出力への書き込み
    #     if self.mode == 'stdout':
    #         self.stdout.write(string)
    #     else:
    #         self.stderr.write(string)
    #
    #     # Textへの書き込み
    #     text = get_text()
    #     if text:
    #         areas = []
    #         for win in bpy.context.window_manager.windows:
    #             for area in win.screen.areas:
    #                 if area.type == 'TEXT_EDITOR':
    #                     space = area.spaces.active
    #                     if space.text == text:
    #                         areas.append([win, area])
    #
    #         ctx = bpy.context.copy()
    #         if areas:
    #             win, area = areas[0]
    #             ctx['window'] = win
    #             ctx['screen'] = win.screen
    #             ctx['area'] = area
    #             ctx['region'] = area.regions[-1]
    #             ctx['edit_text'] = text
    #
    #         text.write('')  # 空の文字列を書き込めば、カーソルが末尾に移動する。
    #         text.write(string)
    #
    #         if len(text.lines) > prefs.max_text_size:
    #             operator_call(bpy.ops.text.move, ctx, type='FILE_TOP',
    #                           _scene_update=False)
    #             for i in range(len(text.lines) - prefs.max_text_size):
    #                 operator_call(bpy.ops.text.move_select, ctx,
    #                               type='NEXT_LINE', _scene_update=False)
    #                 operator_call(bpy.ops.text.delete, ctx,
    #                               _scene_update=False)
    #         operator_call(bpy.ops.text.move, ctx, type='FILE_BOTTOM',
    #                       _scene_update=False)
    #
    #         for win, area in areas:
    #             ctx['window'] = win
    #             ctx['screen'] = win.screen
    #             ctx['area'] = area
    #             ctx['region'] = area.regions[-1]
    #             space = ctx['area'].spaces.active
    #             if space.show_word_wrap:
    #                 operator_call(bpy.ops.text.move, ctx, type='LINE_END',
    #                               _scene_update=False)
    #             else:
    #                 operator_call(bpy.ops.text.move, ctx, type='LINE_BEGIN',
    #                               _scene_update=False)
    #
    #             d = calc_space_values(context, space)
    #             line_height = d['line_height']
    #             wheel_scroll_lines = U.inputs.wheel_scroll_lines
    #             U.inputs.wheel_scroll_lines = 1
    #             x, y = region_location_from_cursor(
    #                     context, space, len(text.lines) - 1, 0)
    #             y -= line_height * 0.5
    #             if y > line_height:
    #                 cnt = -int(y / line_height)
    #                 operator_call(bpy.ops.text.scroll, ctx, lines=cnt,
    #                                   _scene_update=False)
    #             elif y < 0:
    #                 sys.__stdout__.write('eee\n')
    #                 cnt = int(-y / line_height) + 1
    #                 operator_call(bpy.ops.text.scroll, ctx, lines=cnt,
    #                                   _scene_update=False)
    #             U.inputs.wheel_scroll_lines = wheel_scroll_lines
    #         text.update_tag()
    #
    #         # 再描画
    #         for win, area in areas:
    #             area.tag_redraw()
    #
    #     # ログファイルへの書き込み
    #     log_file = get_log_file()
    #     if log_file:
    #         log_file.write(string)
    #         log_file.flush()
    #         log_file.seek(0)
    #         lines = log_file.readlines()
    #         if len(lines) > prefs.max_log_file_size:
    #             lines[:len(lines) - prefs.max_log_file_size] = []
    #         log_file.close()
    #         log_file = get_log_file()
    #         log_file.write(''.join(lines))
    #         log_file.close()

    # def flush(self):
    #     pass

    def begin(self):
        prefs = PrintHookPreferences.get_instance()
        # out = getattr(sys, self.mode)
        # out.flush()
        # setattr(self, self.mode, os.dup(out.fileno()))
        sys.stdout.flush()
        sys.stderr.flush()
        self.stdout = os.dup(sys.stdout.fileno())
        self.stderr = os.dup(sys.stderr.fileno())

        if True:
            # path = os.path.join(bpy.app.tempdir, 'print_hook_test.txt')
            # path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            #                     'print_hook_test.txt')
            path = prefs.log_file
            if not os.path.isabs(path):
                path = os.path.join(bpy.utils.resource_path('USER'), path)
            fd = os.open(path, os.O_RDWR|os.O_CREAT|os.O_TRUNC)
            # fd = os.open(path, os.O_RDWR|os.O_CREAT)
            if get_platform() == 'linux':
                os.chmod(fd, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP |
                             stat.S_IWGRP)
            os.lseek(fd, 0, os.SEEK_END)
            self.file = (fd, path)
            os.dup2(fd, sys.stdout.fileno())
            os.dup2(fd, sys.stderr.fileno())
            os.close(fd)
            if get_platform() == 'windows':
                if sys.version_info < (3, 5):
                    libc = ctypes.CDLL(ctypes.util.find_library('c'))
                else:
                    if hasattr(sys, 'gettotalrefcount'): # debug build
                        libc = ctypes.CDLL('ucrtbased')
                    else:
                        libc = ctypes.CDLL('api-ms-win-crt-stdio-l1-1-0')

                    # VC 14.0 doesn't implement printf dynamically, just
                    # __stdio_common_vfprintf. This take a va_array arglist,
                    # which I won't implement, so I escape format specificiers.

                    class _FILE(ctypes.Structure):
                        """opaque C FILE type"""

                    libc.__acrt_iob_func.restype = ctypes.POINTER(_FILE)

                    def _vprintf(format, arglist_ignored):
                        options = ctypes.c_longlong(0) # no legacy behavior
                        stdout = libc.__acrt_iob_func(1)
                        format = format.replace(b'%%', b'\0')
                        format = format.replace(b'%', b'%%')
                        format = format.replace(b'\0', b'%%')
                        arglist = locale = None
                        return libc.__stdio_common_vfprintf(
                            options, stdout, format, locale, arglist)

                    def _printf(format, *args):
                        return _vprintf(format, args)

                    libc.vprintf = _vprintf
                    libc.printf = _printf
                self.hStandardOutput = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
                self.hStandardError = kernel32.GetStdHandle(STD_ERROR_HANDLE)
                kernel32.SetStdHandle(STD_OUTPUT_HANDLE, libc._get_osfhandle(1))
                kernel32.SetStdHandle(STD_ERROR_HANDLE, libc._get_osfhandle(2))

        else:
            if self.use_mkstemp:
                fd, path = tempfile.mkstemp()
                self.file = (fd, path)
                # os.dup2(fd, out.fileno())
                os.dup2(fd, sys.stdout.fileno())
                os.dup2(fd, sys.stderr.fileno())
                os.close(fd)
            else:
                f = tempfile.NamedTemporaryFile(delete=False)
                fd = f.fileno()
                self.file = (fd, f.name)
                # os.dup2(fd, out.fileno())
                os.dup2(fd, sys.stdout.fileno())
                os.dup2(fd, sys.stderr.fileno())
                f.close()

    def end(self):
        # out = getattr(sys, self.mode)
        # os.dup2(getattr(self, self.mode), out.fileno())
        os.dup2(self.stdout, sys.stdout.fileno())
        os.dup2(self.stderr, sys.stderr.fileno())
        os.remove(self.file[1])

        if get_platform() == 'windows':
            kernel32.SetStdHandle(STD_OUTPUT_HANDLE, self.hStandardOutput)
            kernel32.SetStdHandle(STD_ERROR_HANDLE, self.hStandardError)


# import os
# import io
# print(os.getcwd())
#
#
# stream = io.StringIO()
# import sys
# import os
# sys.stdout.flush()
# bak_fd = os.dup(sys.stdout.fileno())
# print('back', bak_fd)
# fd = os.open('spam.txt', os.O_WRONLY|os.O_CREAT)
# os.dup2(fd, sys.stdout.fileno())

class TEXT_OT_print_hook(bpy.types.Operator):
    bl_idname = 'text.print_hook'
    bl_label = 'stdout'
    bl_description = 'Display print() output'

    enable = False
    stdout = stderr = excepthook = None

    st_mtime = 0
    st_size = 0

    def execute(self, context):
        cls = self.__class__
        if not self.enable:
            cls.enable = True
            cls.stdout = OutputStream('stdout')
            # cls.stderr = OutputStream('stderr')
            # cls.excepthook = OutputStream('excepthook')

            stream = cls.stdout
            fd, path = stream.file
            stat_result = os.stat(path)
            cls.st_mtime = stat_result.st_mtime
            cls.st_size = stat_result.st_size

            bpy.app.handlers.scene_update_pre.append(self.callback)
        else:
            cls.enable = False
            cls.stdout.end()
            # cls.stderr.end()
            # cls.excepthook.end()
            bpy.app.handlers.scene_update_pre.remove(self.callback)
        return {'FINISHED'}

    @classmethod
    def callback(cls, dummy):
        if not cls.enable:
            return

        stream = cls.stdout
        fd, path = stream.file

        stat_result = os.stat(path)
        if not (stat_result.st_size > cls.st_size):
            return

        text = get_text()
        if not text:
            return

        context = bpy.context
        U = context.user_preferences
        prefs = PrintHookPreferences.get_instance()

        areas = []
        for win in bpy.context.window_manager.windows:
            for area in win.screen.areas:
                if area.type == 'TEXT_EDITOR':
                    space = area.spaces.active
                    if space.text == text:
                        areas.append([win, area])

        ctx = bpy.context.copy()
        if areas:
            win, area = areas[0]
            ctx['window'] = win
            ctx['screen'] = win.screen
            ctx['area'] = area
            ctx['region'] = area.regions[-1]
        ctx['edit_text'] = text

        text.write('')  # 空の文字列を書き込めば、カーソルが末尾に移動する。

        with threading.Lock():  # 役に立ってるのか？？
            f = open(path, mode='r+', encoding='utf-8')
            f.flush()
            os.fsync(f.fileno())
            f.seek(0, 2)
            loc = f.tell()
            added_length = stat_result.st_size - cls.st_size
            f.seek(loc - added_length)
            string = f.read()
            f.seek(0, 2)
            f.close()

        text.write(string)

        try:
            os.write(stream.stdout, string.encode(prefs.encoding))
        except:
            pass

        if len(text.lines) > prefs.max_text_size:
            operator_call(bpy.ops.text.move, ctx, type='FILE_TOP',
                          _scene_update=False)
            for i in range(len(text.lines) - prefs.max_text_size):
                operator_call(bpy.ops.text.move_select, ctx,
                              type='NEXT_LINE', _scene_update=False)
                operator_call(bpy.ops.text.delete, ctx,
                              _scene_update=False)
        operator_call(bpy.ops.text.move, ctx, type='FILE_BOTTOM',
                      _scene_update=False)

        for win, area in areas:
            ctx['window'] = win
            ctx['screen'] = win.screen
            ctx['area'] = area
            ctx['region'] = area.regions[-1]
            space = ctx['area'].spaces.active
            if space.show_word_wrap:
                operator_call(bpy.ops.text.move, ctx, type='LINE_END',
                              _scene_update=False)
            else:
                operator_call(bpy.ops.text.move, ctx, type='LINE_BEGIN',
                              _scene_update=False)

            d = calc_space_values(context, space)
            line_height = d['line_height']
            wheel_scroll_lines = U.inputs.wheel_scroll_lines
            U.inputs.wheel_scroll_lines = 1
            x, y = region_location_from_cursor(
                    context, space, len(text.lines) - 1, 0)
            y -= line_height * 0.5
            if y > line_height:
                cnt = -int(y / line_height)
                operator_call(bpy.ops.text.scroll, ctx, lines=cnt,
                                  _scene_update=False)
            elif y < 0:
                sys.__stdout__.write('eee\n')
                cnt = int(-y / line_height) + 1
                operator_call(bpy.ops.text.scroll, ctx, lines=cnt,
                                  _scene_update=False)
            U.inputs.wheel_scroll_lines = wheel_scroll_lines
        text.update_tag()

        # 再描画
        for win, area in areas:
            area.tag_redraw()

        cls.st_mtime = stat_result.st_mtime
        cls.st_size = stat_result.st_size


class TEXT_PT_print_hook(bpy.types.Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_label = 'Print Hook'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.area and context.area.type == 'TEXT_EDITOR'

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.active = TEXT_OT_print_hook.enable
        op = col.operator('text.print_hook', text='StdOut')


###############################################################################
# Register
###############################################################################
classes = [
    PrintHookPreferences,
    TEXT_OT_print_hook,
    TEXT_PT_print_hook,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    if TEXT_OT_print_hook.callback in bpy.app.handlers.scene_update_pre:
        bpy.app.handlers.scene_update_pre.remove(TEXT_OT_print_hook.callback)


if __name__ == '__main__':
    register()
