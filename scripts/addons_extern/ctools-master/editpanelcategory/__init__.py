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
    'name': 'Edit Panel Category',
    'author': 'chromoly',
    'version': (0, 1, 1),
    'blender': (2, 78, 0),
    'location': '',
    'description': '',
    'wiki_url': '',
    'category': 'User Interface',
}


"""
Panelのcategoryを変更する。

UserPreferencesのEditボタンを押して出てきたTextを編集・保存すると
次回起動時から反映される。Alt+PでTextを実行するとすぐに適用される。

おまけ。TOOLSとUIでアクティブなタブを変更するオペレーター
bpy.ops.screen.panel_category_active_set(region_type='TOOLS', category='')
:param: region_type: 'TOOLS' or 'UI'
:type region_type: str
:param category: category(タブ名)を指定
:type category: str
"""


import ctypes as ct
import os
import types
import traceback

import bpy

try:
    importlib.reload(addongroup)
    importlib.reload(customproperty)
    importlib.reload(structures)
except NameError:
    from ..utils import addongroup
    from ..utils import customproperty
    from ..utils import structures


translation_dict = {
    'ja_JP': {
        ('*', 'String'): '文字列',
    }
}

iface = bpy.app.translations.pgettext_iface


###############################################################################
# User Preferences
###############################################################################
FILE_NAME = 'panel_category_settings.py'

try:
   _ = default_panel_categories
except:
    default_panel_categories = None


class ToolPropsPanelPreferences(
        addongroup.AddonGroup,
        bpy.types.PropertyGroup if '.' in __name__ else
        bpy.types.AddonPreferences):
    bl_idname = __name__

    use_last_operator_panel_tools = bpy.props.BoolProperty(
        name='Last Operator Panel (3D View - Tools)',
    )
    use_last_operator_panel_ui = bpy.props.BoolProperty(
        name='Last Operator Panel (3D View - UI)',
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        file_path = os.path.join(bpy.utils.user_resource('CONFIG'),
                                 FILE_NAME)
        row.label('Config File: {}'.format(file_path), translate=False)

        split = layout.split()
        col = split.column()
        col.operator(EditPanelCategory.bl_idname, text='Edit')

        col = split.column()
        col = split.column()

        layout.separator()
        row = layout.row()
        row.prop(self, 'use_last_operator_panel_tools')
        row.prop(self, 'use_last_operator_panel_ui')

        layout.separator()
        super().draw(context)


###############################################################################
# Functions
###############################################################################
# PanelType.draw_header == view3d_panel_operator_redo_header
# void (*draw_header)(const struct bContext *, struct Panel *);
draw_header_func = None

# PanelType.draw == view3d_panel_operator_redo
# void (*draw)(const struct bContext *, struct Panel *);
draw_func = None


def get_space_types():
    """
    :rtype: dict[str, T]
    """
    screen = bpy.context.screen
    area = screen.areas[0]
    sa = structures.ScrArea.cast(area)

    st_p = sa.type
    st = None
    while st_p:
        st = st_p.contents
        st_p = st.prev

    space_types = {}
    while st:
        try:
            name = structures.RNAEnumSpaceTypeItems(st.spaceid).name
            if name != 'EMPTY':
                space_types[name] = st
        except ValueError:
            pass
        if st.next:
            st = st.next.contents
        else:
            st = None
    return space_types


def get_region_types():
    """
    :return: {'VIEW_3D': {'TOOLS': rt, 'TOOL_PROPS': rt, ...}, ...}
    :rtype: dict[str, dict[str, T]]
    """
    result = {}
    for name, st in get_space_types().items():
        d = result[name] = {}
        region_types = st.regiontypes.to_list(structures.ARegionType)
        for art in region_types:
            region_name = structures.RNAEnumRegionTypeItems(art.regionid).name
            d[region_name] = art
    return result


def UI_panel_category_find(region, idname):
    ar = structures.ARegion.cast(region)
    return ar.panels_category.find_string(
        idname.encode('utf-8'), structures.PanelCategoryDyn.idname.offset)


def UI_panel_category_active_get(region):
    """UI_panel_category_active_getを真似る"""

    if region.type not in {'TOOLS', 'UI'}:
        raise ValueError()

    ar = structures.ARegion.cast(region)
    pc_act_ptr = ct.cast(ar.panels_category_active.first,
                         ct.POINTER(structures.PanelCategoryStack))
    while pc_act_ptr:
        pc_act = pc_act_ptr.contents
        idname = pc_act.idname.decode('utf-8')
        if UI_panel_category_find(region, idname):
            return idname
        pc_act_ptr = pc_act.next

    return None


def UI_panel_category_active_set(context, region, idname):
    """UI_panel_category_active_setのようなもの"""

    if region.type not in {'TOOLS', 'UI'}:
        raise ValueError()

    ar = structures.ARegion.cast(region)

    if not UI_panel_category_find(region, idname):
        return False

    active_category = UI_panel_category_active_get(region)
    if active_category is None:
        return False
    # 再描画させる為にコメントアウト
    # elif active_category == idname:
    #     return True

    # wmEvent(仮)の作成
    event = structures.wmEvent()
    event.type = 0x00db  # TABKEY
    event.val = 1  # KM_PRESS
    event.ctrl = 1

    # 関数: wmEventHandler.ui_handle
    ui_handle_type = ct.CFUNCTYPE(ct.c_int, ct.c_void_p, ct.c_void_p,
                                  ct.c_void_p)

    # ui_region_handler内でCTX_wm_region()が使われる為、ここで上書きする
    py_context = context.copy()
    py_context['region'] = region
    py_context_bak = structures.context_py_dict_set(context, py_context)

    active_category_bak = active_category
    for handler in ar.handlers.to_list(structures.wmEventHandler):
        if not handler.ui_handle:
            continue
        ui_handle = ui_handle_type(handler.ui_handle)
        retval = ui_handle(context.as_pointer(), ct.byref(event), None)
        if retval == 1:  # WM_UI_HANDLER_BREAK
            while True:
                active_category = UI_panel_category_active_get(region)
                if active_category == idname:
                    break
                elif active_category == active_category_bak:
                    break
                ui_handle(context.as_pointer(), ct.byref(event), None)
        if active_category == idname:
            break

    # py_contextを戻す
    structures.context_py_dict_set(context, py_context_bak)

    # 再描画。(必要か？)
    region.tag_redraw()

    return active_category == idname


def panel_categories_from_string(text):
    """文字列から辞書を作って返す"""
    mod = types.ModuleType('tmp')
    try:
        exec(text, mod.__dict__)
    except:
        traceback.print_exc()
        return None

    if 'panel_category' in mod.__dict__:
        if isinstance(mod.panel_category, dict):
            return mod.panel_category


def init_default_panel_categories():
    """最初のscene_updateで呼び出して初期化する。blender起動中に一回のみ"""
    global default_panel_categories

    if default_panel_categories is None:
        default_panel_categories = {}
    else:
        return

    for space_type, region_types in get_region_types().items():
        for region_type, art in region_types.items():
            if region_type not in {'TOOLS', 'UI'}:
                continue
            for pt in art.paneltypes.to_list(structures.PanelType):
                ctx = pt.context.decode('utf-8')
                idname = iface(pt.idname.decode('utf-8'), ctx)
                default_panel_categories[idname] = pt.category.decode('utf-8')


def apply_panel_categories(context, panel_categories):
    """panel_categories_from_string()で作った辞書を適用する"""

    if not panel_categories:
        return {'CANCELLED'}

    for space_type, region_types in get_region_types().items():
        for region_type, art in region_types.items():
            if region_type not in {'TOOLS', 'UI'}:
                continue
            for pt in art.paneltypes.to_list(structures.PanelType):
                ctx = pt.context.decode('utf-8')
                idname = iface(pt.idname.decode('utf-8'), ctx)
                if idname in panel_categories:
                    category = panel_categories[idname].encode('utf-8')
                    pt.category = category

    for win in context.window_manager.windows:
        for area in win.screen.areas:
            area.tag_redraw()


###############################################################################
# Operator
###############################################################################
class EditPanelCategoryRun(bpy.types.Operator):
    """bpy.ops.screen.edit_panel_category()で作ったTextObjectを
    実行すると呼ばれる
    """
    bl_idname = 'screen.edit_panel_category_run'
    bl_label = 'Apply Panel Category'
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'TEXT_EDITOR' and context.edit_text

    def execute(self, context):
        text = context.edit_text
        panel_categories = panel_categories_from_string(text.as_string())
        apply_panel_categories(context, panel_categories)

        return {'FINISHED'}


class EditPanelCategory(bpy.types.Operator):
    """User Preferencesのボタンから起動。TextObjectを作る"""
    bl_idname = 'screen.edit_panel_category'
    bl_label = 'Edit Panel Category'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        global default_panel_categories

        file_path = os.path.join(bpy.utils.user_resource('CONFIG'),
                                 FILE_NAME)

        for text in bpy.data.texts:
            if text.filepath == file_path:
                break
        else:
            try:
                with open(file_path, 'a', encoding='utf-8'):
                    pass
            except:
                traceback.print_exc()
                return {'CANCELLED'}
            text = bpy.data.texts.load(file_path)

        user_panel_categories = panel_categories_from_string(
            text.as_string())

        text.clear()
        text.write('panel_category = {\n')

        for space_type, region_types in get_region_types().items():
            ls = []
            if 'TOOLS' in region_types:
                ls.append(('TOOLS', region_types['TOOLS']))
            if 'UI' in region_types:
                ls.append(('UI', region_types['UI']))
            if not ls:
                continue

            for region_type, art in ls:
                panel_types = art.paneltypes.to_list(structures.PanelType)
                if not panel_types:
                    continue

                text.write('\n')
                text.write('    ' + '#' * 70 + '\n')
                text.write(
                    '    # {}: {}\n'.format(space_type, region_type))
                text.write('    ' + '#' * 70 + '\n')

                for pt in panel_types:
                    ctx = pt.context.decode('utf-8')
                    idname = iface(pt.idname.decode('utf-8'), ctx)

                    name = iface(pt.label.decode('utf-8'), ctx)
                    text.write('\n')
                    text.write('    # {}\n'.format(name))

                    category = pt.category.decode('utf-8')
                    comment_out = False
                    if (user_panel_categories is not None and
                                idname in user_panel_categories):
                        text.write('    ')
                    elif (idname not in default_panel_categories or
                                  default_panel_categories[
                                      idname] == category):
                        text.write('    # ')
                        comment_out = True
                    else:
                        text.write('    ')
                    # ファイルの設定より現在の設定が優先される
                    text.write("'{}': '{}',".format(idname, category))
                    if not comment_out:
                        if idname in default_panel_categories:
                            text.write("  # default: '{}'".format(
                                default_panel_categories[idname]))
                        if idname in user_panel_categories:
                            text.write("  # user: '{}'".format(
                                user_panel_categories[idname]))
                    text.write('\n')

                    if (user_panel_categories is not None and
                                idname in user_panel_categories):
                        del user_panel_categories[idname]

        if user_panel_categories:
            text.write('\n    # Unknown\n')
            for idname, category in user_panel_categories.items():
                text.write("    '{}': '{}',\n".format(idname, category))

        text.write('}\n\n')
        text.write('if __name__ == \'__main__\':\n')
        text.write('    import bpy\n')
        text.write('    bpy.ops.screen.edit_panel_category_run()\n')

        self.report({'INFO'}, "See '{}' in the text editor".format(FILE_NAME))

        return {'FINISHED'}


class SetPanelActiveCategory(bpy.types.Operator):
    bl_idname = 'screen.panel_category_active_set'
    bl_label = 'Set Panel Active Category'
    bl_options = {'REGISTER'}

    region_type = bpy.props.EnumProperty(
        name='Region Type',
        items=(('TOOLS', 'Tools', ''),
               ('UI', 'UI', '')),
        default='TOOLS'
    )
    category = bpy.props.StringProperty(
        name='Category',
    )

    def execute(self, context):
        area = context.area
        for region in area.regions:
            if region.type == self.region_type:
                break
        else:
            return {'CANCELLED'}
        UI_panel_category_active_set(context, region, self.category)
        return {'FINISHED'}


###############################################################################
# Update Operator History Count
###############################################################################
last_operator_count = last_operator_address = 0


def update_history_count(context):
    """SpaceInfoのcallbackとしても使う
    """
    global last_operator_count, last_operator_address

    wm = context.window_manager
    if wm.operators:
        history = [op.as_pointer() for op in wm.operators]
        if history:
            if last_operator_address in history:
                i = history.index(last_operator_address)
                last_operator_count += len(history) - i - 1
            else:
                last_operator_count = len(history) - 1
            last_operator_address = history[-1]

        # # redo operator
        # redo_operator = None
        # redo_operator_count = last_operator_count
        # for op in list(wm.operators)[::-1]:
        #     if 'REGISTER' in op.bl_options and 'UNDO' in op.bl_options:
        #         redo_operator = op
        #         break
        #     redo_operator_count -= 1
    else:
        last_operator_count = last_operator_address = 0


###############################################################################
# Panel
###############################################################################
class LastOperatorPanel:
    # bl_idname = 'VIEW3D_PT_last_operator_tools'
    bl_label = 'Last Operator'
    bl_space_type = 'VIEW_3D'
    # bl_region_type = 'TOOLS'
    bl_category = 'ToolProps'

    # def draw_header(self, context):
    #     if draw_header_func:
    #         draw_header_func(context.as_pointer(), self.as_pointer())
    #
    # def draw(self, context):
    #     if draw_func:
    #         draw_func(context.as_pointer(), self.as_pointer())

    def operator_last_redo(self, context):
        wm = context.window_manager
        for op in list(wm.operators)[::-1]:
            if 'REGISTER' in op.bl_options and 'UNDO' in op.bl_options:
                return op
        return None

    def draw_header(self, context):
        wm = context.window_manager

        if wm.operators:
            update_history_count(context)

            # redo operator
            redo_operator = None
            redo_operator_count = last_operator_count
            for op in list(wm.operators)[::-1]:
                if 'REGISTER' in op.bl_options and 'UNDO' in op.bl_options:
                    redo_operator = op
                    break
                redo_operator_count -= 1
            if redo_operator:
                op = redo_operator
                count = redo_operator_count
            else:
                op = wm.operators[-1]
                count = last_operator_count
            name = bpy.app.translations.pgettext_iface(op.name, 'Operator')
            text = '[{}]  {}'.format(count, name)

        else:
            text = bpy.app.translations.pgettext_iface('Operator', '*')

        pa = structures.Panel.cast(self)
        pa.drawname = text.encode('utf-8')[:64]

    def draw(self, context):
        # layout = self.layout
        #
        # wm = context.window_manager
        # if wm.operators:
        #     name = bpy.app.translations.pgettext_iface(
        #         wm.operators[-1].name, 'Operator')
        #     layout.label('[{}]  {}'.format(last_operator_count, name))

        if draw_func:
            draw_func(context.as_pointer(), self.as_pointer())


class LastOperatorPanelTools(LastOperatorPanel, bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_last_operator_tools'
    bl_region_type = 'TOOLS'

    @classmethod
    def poll(self, context):
        prefs = ToolPropsPanelPreferences.get_instance()
        return prefs.use_last_operator_panel_tools


class LastOperatorPanelUI(LastOperatorPanel, bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_last_operator_ui'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        prefs = ToolPropsPanelPreferences.get_instance()
        return prefs.use_last_operator_panel_ui


###############################################################################
# Callback
###############################################################################
@bpy.app.handlers.persistent
def callback_get_draw_func(scene=None):
    global draw_header_func, draw_func

    if draw_header_func:
        return draw_header_func, draw_func

    region_types = get_region_types()
    art = region_types['VIEW_3D']['TOOL_PROPS']

    # PanelTypeからdraw関数を取得
    for pt in art.paneltypes.to_list(structures.PanelType):
        if pt.idname == b'VIEW3D_PT_last_operator':
            draw_header_func = pt.draw_header
            draw_func = pt.draw

    if draw_header_func:
        if callback_get_draw_func in bpy.app.handlers.scene_update_pre:
            bpy.app.handlers.scene_update_pre.remove(callback_get_draw_func)

    if draw_header_func:
        return draw_header_func, draw_func
    else:
        return None


@bpy.app.handlers.persistent
def callback_init_categories(scene):
    init_default_panel_categories()

    file_path = os.path.join(bpy.utils.user_resource('CONFIG'), FILE_NAME)
    found = True
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except:
        found = False
        # traceback.print_exc()
    if found:
        apply_panel_categories(bpy.context, panel_categories_from_string(text))

    bpy.app.handlers.scene_update_pre.remove(callback_init_categories)


###############################################################################
# Property
###############################################################################
def region_active_category_getter(self):
    if self.type not in {'TOOLS', 'UI'}:
        return None
    return UI_panel_category_active_get(self)


def region_active_category_setter(self, category):
    UI_panel_category_active_set(bpy.context, self, category)


def region_panel_categories_get(self):
    ar = structures.ARegion.cast(self)
    categories = ar.panels_category.to_list(structures.PanelCategoryDyn)
    return [c.idname.decode('utf-8') for c in categories]


###############################################################################
# Register / Unregister
###############################################################################
classes = [
    ToolPropsPanelPreferences,
    SetPanelActiveCategory,
    LastOperatorPanelUI,
    LastOperatorPanelTools,
    EditPanelCategory,
    EditPanelCategoryRun,
]


@ToolPropsPanelPreferences.register_addon
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    if not bpy.app.background:
        bpy.app.handlers.scene_update_pre.append(callback_get_draw_func)
    bpy.app.handlers.scene_update_pre.append(callback_init_categories)

    bpy.types.Region.active_panel_category = property(
        region_active_category_getter, region_active_category_setter)
    bpy.types.Region.panel_categories = property(region_panel_categories_get)

    update_history_count._handler = bpy.types.SpaceInfo.draw_handler_add(
        update_history_count, (bpy.context,), 'HEADER', 'POST_PIXEL')

    bpy.app.translations.register(__name__, translation_dict)

    # wm = bpy.context.window_manager
    # kc = wm.keyconfigs.addon
    # if kc:
    #     km = ToolPropsPanelPreferences.get_keymap('Screen')


@ToolPropsPanelPreferences.unregister_addon
def unregister():
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)

    if callback_get_draw_func in bpy.app.handlers.scene_update_pre:
        bpy.app.handlers.scene_update_pre.remove(callback_get_draw_func)
    if callback_init_categories in bpy.app.handlers.scene_update_pre:
        bpy.app.handlers.scene_update_pre.remove(callback_init_categories)

    del bpy.types.Region.active_panel_category
    del bpy.types.Region.panel_categories

    bpy.types.SpaceInfo.draw_handler_remove(
        update_history_count._handler, 'HEADER')

    bpy.app.translations.unregister(__name__)


if __name__ == '__main__':
    register()
