# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
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
    'name': 'CTools',
    'author': 'chromoly',
    'version': (1, 8, 10),
    'blender': (2, 78, 0),
    'location': '',
    'description': 'Collection of add-ons',
    'warning': '',
    'wiki_url': 'https://github.com/chromoly/ctools',
    'category': 'User Interface',
}


import difflib
import hashlib
import importlib
import os
import pathlib
import shutil
import tempfile
import urllib.request
import zipfile

if 'bpy' in locals():
    importlib.reload(addongroup)
    CToolsPreferences.reload_submodules()
else:
    from .utils import addongroup

import bpy


class CToolsPreferences(addongroup.AddonGroup,
                        bpy.types.AddonPreferences):
    bl_idname = __name__

    submodules = [
        'aligntools',
        'armaturehelper',
        'boolutils',
        'dollyzoom',
        'drawnearest',
        'editpanelcategory',
        'emulatekeymap',
        '_groupmanager',
        'filebrowserconfirm',
        'listvalidkeys',
        'lockcoords',
        'lockcursor3d',
        'mousegesture',
        'overwrite_builtin_images',
        'quadview_move',
        'quickboolean',
        'regionruler',
        '_renametool',
        'panelrestriction',
        'piemenu',
        'screencastkeys',
        'splashscreen',
        'stdout2pyconsole',
        'systemsound',
        'updatetag',
        'uvgrid',

        '_space_view3d_colorwire',
        '_space_view3d_localgrid',
        '_piemenu',
        '_mesh_fake_knife',
        '_mesh_vertex_slide',
        '_space_view3d_snap_cursor',
        '_space_view3d_utility_menu',
        '_mesh_add_custom_menu_items',
        '_wm_custom_keymap',

        # 作業中
        '_groupeditor',

        'transformorientation',
    ]


class SCRIPT_OT_cutils_module_update(bpy.types.Operator):
    """このアドオンのディレクトリの中身を全部消して置換する"""
    bl_idname = 'script.cutils_module_update'
    bl_label = 'Update'

    ctools_dir = os.path.dirname(os.path.abspath(__file__))
    bl_description = 'Download and install addon. ' + \
        'Warning: remove all files under {}/'.format(ctools_dir)

    url = 'https://github.com/chromoly/ctools/archive/master.zip'
    log_name = 'ctools_update.log'  # name of bpy.types.Text

    dry_run = bpy.props.BoolProperty(
            'Dry Run', default=False, options={'SKIP_SAVE'})
    diff = bpy.props.BoolProperty(
            'Create Diff Text', default=True, options={'SKIP_SAVE'})

    def execute(self, context):
        if not self.dry_run:
            # '.git'が存在すればやめる
            if '.git' in os.listdir(self.ctools_dir):
                self.report(type={'ERROR'},
                            message="Found '.git' directory. "
                                    "Please use git command")
                return {'CANCELLED'}

        context.window.cursor_set('WAIT')

        diff_lines = []  # 行末に改行文字を含む
        diff_text = None

        try:
            req = urllib.request.urlopen(self.url)

            with tempfile.TemporaryDirectory() as tmpdir_name:
                with tempfile.NamedTemporaryFile(
                        'wb', suffix='.zip', dir=tmpdir_name,
                        delete=False) as tmpfile:
                    tmpfile.write(req.read())
                    req.close()
                zf = zipfile.ZipFile(tmpfile.name, 'r')
                dirname = ''
                for name in zf.namelist():
                    p = pathlib.PurePath(name)
                    if len(p.parts) == 1:
                        dirname = p.parts[0]
                    zf.extract(name, path=tmpdir_name)
                zf.close()

                ctools_dir_tmp = os.path.join(tmpdir_name, dirname)

                # 差分表示
                src_files = []
                dst_files = []
                ignore_dirs = ['__pycache__', '.git', 'subtree']
                os.chdir(ctools_dir_tmp)
                for root, dirs, files in os.walk('.'):
                    for name in files:
                        p = os.path.normpath(os.path.join(root, name))
                        src_files.append(p)
                    for name in ignore_dirs:
                        if name in dirs:
                            dirs.remove(name)
                os.chdir(self.ctools_dir)
                for root, dirs, files in os.walk('.'):
                    for name in files:
                        p = os.path.normpath(os.path.join(root, name))
                        dst_files.append(p)
                    for name in ignore_dirs:
                        if name in dirs:
                            dirs.remove(name)

                files = []
                for name in src_files:
                    if name in dst_files:
                        files.append((name, 'update'))
                    else:
                        files.append((name, 'new'))
                for name in dst_files:
                    if name not in src_files:
                        files.append((name, 'delete'))

                for name, status in files:
                    if name.endswith(('.py', '.md', '.patch', '.sh')):
                        if status in {'new', 'update'}:
                            p1 = os.path.join(ctools_dir_tmp, name)
                            with open(p1, 'r', encoding='utf-8') as f1:
                                src = f1.readlines()
                        else:
                            src = []
                        if status in {'delete', 'update'}:
                            p2 = os.path.join(self.ctools_dir, name)
                            with open(p2, 'r', encoding='utf-8') as f2:
                                dst = f2.readlines()
                        else:
                            dst = []

                        lines = list(difflib.unified_diff(
                                dst, src, fromfile=name, tofile=name))
                        if lines:
                            for line in lines:
                                diff_lines.append(line)
                    else:
                        if status in {'new', 'update'}:
                            p1 = os.path.join(ctools_dir_tmp, name)
                            with open(p1, 'rb') as f1:
                                src = f1.read()
                            h1 = hashlib.md5(src).hexdigest()
                        if status in {'delete', 'update'}:
                            p2 = os.path.join(self.ctools_dir, name)
                            with open(p2, 'rb') as f2:
                                dst = f2.read()
                            h2 = hashlib.md5(dst).hexdigest()

                        if status == 'new':
                            line = 'New: {}\n'.format(name)
                            diff_lines.append(line)
                        elif status == 'delete':
                            line = 'Delete: {}\n'.format(name)
                            diff_lines.append(line)
                        else:
                            if h1 != h2:
                                line = 'Update: {}\n'.format(name)
                                diff_lines.append(line)
                                line = '    md5: {} -> {}\n'.format(h1, h2)
                                diff_lines.append(line)

                if diff_lines:
                    if self.diff:
                        diff_text = bpy.data.texts.new(self.log_name)
                        diff_text.from_string(''.join(diff_lines))
                    if not self.dry_run:
                        # delete
                        for name in os.listdir(self.ctools_dir):
                            if name == '__pycache__':
                                continue
                            p = os.path.join(self.ctools_dir, name)
                            if os.path.isdir(p):
                                shutil.rmtree(p, ignore_errors=True)
                            elif os.path.isfile(p):
                                os.remove(p)

                        # copy all
                        for name, status in files:
                            if status in {'new', 'update'}:
                                dst = os.path.join(self.ctools_dir, name)
                                dst = os.path.normpath(dst)
                                src = os.path.join(ctools_dir_tmp, name)
                                src = os.path.normpath(src)
                                if not os.path.exists(os.path.dirname(dst)):
                                    os.makedirs(os.path.dirname(dst))
                                with open(dst, 'wb') as dst_f, \
                                     open(src, 'rb') as src_f:
                                    dst_f.write(src_f.read())

        # except:
        #     traceback.print_exc()
        #     self.report(type={'ERROR'}, message='See console')
        #     return {'CANCELLED'}

        finally:
            context.window.cursor_set('DEFAULT')

        if diff_lines:
            if diff_text:
                msg = "See '{}' in the text editor".format(diff_text.name)
                self.report(type={'INFO'}, message=msg)
            if not self.dry_run:
                msg = 'Updated. Please restart.'
                self.report(type={'WARNING'}, message=msg)
        else:
            self.report(type={'INFO'}, message='No updates were found')

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


classes = [
    CToolsPreferences,
    SCRIPT_OT_cutils_module_update,
]


@CToolsPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


@CToolsPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)
