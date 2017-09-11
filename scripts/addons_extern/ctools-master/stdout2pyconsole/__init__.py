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
    'name': 'StdOut to Python Console',
    'author': 'chromoly',
    'version': (0, 1, 0),
    'blender': (2, 78, 0),
    'location': 'Python Console',
    'description': 'Python stdout & stderr -> python console',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'System',
}


"""
pythonの標準出力と標準エラー出力をPythonConsoleにも出力する。
SyntaxErrorのエラー出力には対応していない。
"""


import importlib
import io
import sys

import bpy

try:
    importlib.reload(addongroup)
except NameError:
    from ..utils import addongroup


class StdOutToPythonConsolePreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__


stdout = stderr = None


class StdOut(io.StringIO):
    output_type = 'stdout'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buf = ''

    def write(self, text, flush=False):
        if self.output_type == 'stdout':
            stdout.write(text)
            scrollback_type = 'OUTPUT'
        else:
            stderr.write(text)
            scrollback_type = 'ERROR'

        console_areas = []
        try:
            # register時に使用した場合
            # AttributeError: '_RestrictContext' object has no attribute ...
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'CONSOLE':
                        console_areas.append((window, area))
        except:
            return

        if not console_areas:
            return

        self.buf += text
        if self.buf and '\n' in self.buf:
            lines = self.buf.split('\n')
            write_lines = lines[:-1]
            buf_next = lines[-1]
        else:
            write_lines = []
            buf_next = self.buf
        if flush and buf_next:
            flush_line = buf_next
            buf_next = ''
        else:
            flush_line = ''

        ctx = bpy.context.copy()

        for window, area in console_areas:
            ctx['window'] = window
            ctx['screen'] = window.screen
            ctx['area'] = area
            ctx['region'] = area.regions[-1]
            if write_lines:
                for line in write_lines:
                    bpy.ops.console.scrollback_append(ctx, text=line,
                                                      type=scrollback_type)
            if flush_line:
                bpy.ops.console.scrollback_append(ctx, text=flush_line,
                                                  type=scrollback_type)
        self.buf = buf_next

    def flush(self):
        self.write('', flush=True)


class StdErr(StdOut):
    output_type = 'stderr'


classes = [
    StdOutToPythonConsolePreferences
]


@StdOutToPythonConsolePreferences.register_addon
def register():
    global stdout, stderr
    for cls in classes:
        bpy.utils.register_class(cls)
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = StdOut()
    sys.stderr = StdErr()


@StdOutToPythonConsolePreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
    sys.stdout = stdout
    sys.stderr = stderr


if __name__ == '__main__':
    register()
