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
    'name': 'System Sound',
    'author': 'chromoly',
    'version': (0, 1, 0),
    'blender': (2, 78, 0),
    'location': '',
    'description': 'Play sound file',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'User Interface',
}


"""
特定のアクションの時に指定フォルダにある音声ファイルをランダムで一つ選んで再生する。

* 起動
* 終了
* blendファイルの読み込み
* blendファイルの保存(AutoSaveを含む)
* スタートアップファイルの再読み込み(Ctrl+N)
* UserPreferences画面の表示(Ctrl+Alt+U)

終了時の音声(Power Off Post)は再生終了までユーザーからの入力を
一切受け付けなくなるので注意。
"""


import ctypes as ct
import importlib
import os
import random
import time
import traceback

import bpy
import aud

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(st)
    importlib.reload(wrapoperator)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import structures as st
    from ..utils import wrapoperator


DEFAULT_VOLUME = 100

device = aud.device()
device.volume = DEFAULT_VOLUME / 100.0
# factory = None
handle = None


###############################################################################
# Addon Preferences
###############################################################################
class AddonSystemSoundPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    def volume_update(self, context):
        device.volume = self.volume / 100.0

    volume = bpy.props.IntProperty(
        name='Volume',
        min=0,
        max=100,
        default=DEFAULT_VOLUME,
        update=volume_update
    )

    startup = bpy.props.StringProperty(
        name='Start Up',
        default='//startup',
        subtype='DIR_PATH',
    )
    quit_pre = bpy.props.StringProperty(
        name='Power Off Pre',
        description='When popup is displayed',
        default='//quit_pre',
        subtype='DIR_PATH',
    )
    quit_post= bpy.props.StringProperty(
        name='Power Off Post',
        default='//quit_post',
        subtype='DIR_PATH',
    )
    userprefs = bpy.props.StringProperty(
        name='User Preferences',
        default='//userprefs',
        subtype='DIR_PATH',
    )
    load_pre = bpy.props.StringProperty(
        name='Load Pre',
        description='When file browser is displayed',
        default='//load_pre',
        subtype='DIR_PATH',
    )
    load_post = bpy.props.StringProperty(
        name='Load Post',
        default='//load_post',
        subtype='DIR_PATH',
    )
    load_home = bpy.props.StringProperty(
        name='Load Home File',
        description='When popup is displayed',
        default='//load_home',
        subtype='DIR_PATH',
    )
    save_pre = bpy.props.StringProperty(
        name='Save Pre',
        description='When file browser is displayed',
        default='//save_pre',
        subtype='DIR_PATH',
    )
    save_post = bpy.props.StringProperty(
        name='Save Post',
        default='//save_post',
        subtype='DIR_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.context_pointer_set('addon_prefs', self)

        split = layout.split()
        column = split.column()
        column.prop(self, 'volume')
        split.column()
        split.column()

        column = layout.column()
        column.prop(self, 'startup')
        column.prop(self, 'quit_pre')
        column.prop(self, 'quit_post')
        column.prop(self, 'userprefs')
        column.prop(self, 'load_pre')
        column.prop(self, 'load_post')
        column.prop(self, 'load_home')
        column.prop(self, 'save_pre')
        column.prop(self, 'save_post')

        layout.separator()

        super().draw(context)


###############################################################################
# play sound
###############################################################################
def play_sound(kind):
    global handle

    addon_prefs = AddonSystemSoundPreferences.get_instance()

    dir_path = getattr(addon_prefs, kind)
    if not dir_path:
        return
    if dir_path.startswith('//'):
        dir_path = bpy.path.abspath(
            dir_path, os.path.join(os.path.dirname(__file__), 'sound'))

    try:
        files = os.listdir(dir_path)
    except:
        traceback.print_exc()
        return

    cwd = os.getcwd()
    os.chdir(dir_path)

    files = [f for f in files if not f.startswith('.') and os.path.isfile(f)]

    i = random.randint(0, len(files) - 1)
    path = os.path.join(dir_path, files[i])
    factory = aud.Factory(path)

    os.chdir(cwd)

    if handle and handle.status:
        handle.stop()
    try:
        device.volume = addon_prefs.volume / 100.0
        handle = device.play(factory)
    except:
        # aud.error: AUD_OpenALDevice: Buffer couldn't be generated.
        try:
            handle = device.play(factory)
        except:
            traceback.print_exc()


###############################################################################
# replace functions
###############################################################################
operators = {}


class Operator:
    exec_type = ct.CFUNCTYPE(ct.c_int, ct.c_void_p, ct.c_void_p)
    invoke_type = ct.CFUNCTYPE(ct.c_int, ct.c_void_p, ct.c_void_p, ct.c_void_p)

    def __init__(self, idname, **functions):
        self.idname = idname
        self.functions = functions
        self.new_functions = {}

    def replace(self):
        ot = wrapoperator.get_operator_type(self.idname)
        for name, func in self.functions.items():
            if name == 'invoke':
                func_type = self.invoke_type
            elif name == 'exec':
                func_type = self.exec_type
            addr = ct.cast(getattr(ot, name), ct.c_void_p).value
            orig_func = func_type(addr)
            setattr(self, name, orig_func)
            new_func = func_type(func)
            self.new_functions[name] = new_func
            setattr(ot, name, new_func)

    def restore(self):
        ot = wrapoperator.get_operator_type(self.idname)
        for name in self.functions:
            setattr(ot, name, getattr(self, name))


def replace_functions():
    # wm.open_mainfile ----------------------------------------------
    def execute(self, context):
        r = operators['wm.open_mainfile'].exec(self, context)
        if 'CANCELLED' not in wrapoperator.convert_return_flag(r):
            play_sound('load_post')
        return r

    def invoke(self, context, event):
        r = operators['wm.open_mainfile'].invoke(
            self, context, event)
        if 'RUNNING_MODAL' in wrapoperator.convert_return_flag(r):
            play_sound('load_pre')
        return r

    operators['wm.open_mainfile'] = Operator(
        'wm.open_mainfile', invoke=invoke, exec=execute)

    # wm.save_mainfile ----------------------------------------------
    def execute(self, context):
        r = operators['wm.save_mainfile'].exec(self, context)
        if 'CANCELLED' not in wrapoperator.convert_return_flag(r):
            play_sound('save_post')
        return r

    def invoke(self, context, event):
        r = operators['wm.save_mainfile'].invoke(
            self, context, event)
        if 'RUNNING_MODAL' in wrapoperator.convert_return_flag(r):
            play_sound('save_pre')
        return r

    operators['wm.save_mainfile'] = Operator(
        'wm.save_mainfile', invoke=invoke, exec=execute)

    # wm.save_as_mainfile -------------------------------------------
    def execute(self, context):
        r = operators['wm.save_as_mainfile'].exec(self, context)
        if 'CANCELLED' not in wrapoperator.convert_return_flag(r):
            play_sound('save_post')
        return r

    def invoke(self, context, event):
        r = operators['wm.save_as_mainfile'].invoke(
            self, context, event)
        if 'RUNNING_MODAL' in wrapoperator.convert_return_flag(r):
            play_sound('save_pre')
        return r

    operators['wm.save_as_mainfile'] = Operator(
        'wm.save_as_mainfile', invoke=invoke, exec=execute)

    # wm.read_homefile ----------------------------------------------
    def execute(self, context):
        r = operators['wm.read_homefile'].exec(self, context)
        if 'CANCELLED' not in wrapoperator.convert_return_flag(r):
            play_sound('load_post')
        return r

    def invoke(self, context, event):
        r = operators['wm.read_homefile'].invoke(
            self, context, event)
        if 'INTERFACE' in wrapoperator.convert_return_flag(r):
            play_sound('load_home')
        return r

    operators['wm.read_homefile'] = Operator(
        'wm.read_homefile', invoke=invoke, exec=execute)

    # screen.userpref_show ----------------------------------------------
    def invoke(self, context, event):
        r = operators['screen.userpref_show'].invoke(
            self, context, event)
        if 'CANCELLED' not in wrapoperator.convert_return_flag(r):
            play_sound('userprefs')
        return r

    operators['screen.userpref_show'] = Operator(
        'screen.userpref_show', invoke=invoke)

    # wm.quit_blender -----------------------------------------------
    def execute(self, context):
        try:
            play_sound('quit_post')
            while handle.status:
                time.sleep(0.1)
        except:
            traceback.print_exc()
        r = operators['wm.quit_blender'].exec(self, context)
        return r

    def invoke(self, context, event):
        r = operators['wm.quit_blender'].invoke(
            self, context, event)
        if 'INTERFACE' in wrapoperator.convert_return_flag(r):
            play_sound('quit_pre')
        return r

    operators['wm.quit_blender'] = Operator(
        'wm.quit_blender', invoke=invoke, exec=execute)

    # attrs, _ = wrapoperator.convert_operator_attributes('')
    # print(attrs.keys())

    # replace -------------------------------------------------------
    for op in operators.values():
        op.replace()


def restore_functions():
    for op in operators.values():
        op.restore()
    operators.clear()


###############################################################################
# start up sound
###############################################################################
try:
    _ = is_startup
    is_startup = False
except NameError:
    is_startup = True


@bpy.app.handlers.persistent
def scene_update_pre(scene):
    global handle
    try:
        play_sound('startup')
    except:
        traceback.print_exc()

    bpy.app.handlers.scene_update_pre.remove(scene_update_pre)


###############################################################################
# Register
###############################################################################
classes = [
    AddonSystemSoundPreferences,
]


@AddonSystemSoundPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    if is_startup:
        bpy.app.handlers.scene_update_pre.append(scene_update_pre)

    addon_prefs = AddonSystemSoundPreferences.get_instance()
    device.volume = addon_prefs.volume / 100.0

    replace_functions()


@AddonSystemSoundPreferences.unregister_addon
def unregister():
    restore_functions()

    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    if scene_update_pre in bpy.app.handlers.scene_update_pre:
        bpy.app.handlers.scene_update_pre.remove(scene_update_pre)


if __name__ == '__main__':
    register()
