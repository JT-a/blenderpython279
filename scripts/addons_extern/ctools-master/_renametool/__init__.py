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
    'name': 'Rename Tool',
    'author': 'chromoly',
    'version': (0, 1, 6),
    'blender': (2, 78, 0),
    'location': 'View3D > Tools > Rename Selections',
    'description': '',
    'warning': '',
    'category': 'Object'}


from collections import OrderedDict

import bpy

try:
    importlib.reload(vaob)
    importlib.reload(vaarm)
    importlib.reload(vau)
except NameError:
    from ..utils import vaobject as vaob
    from ..utils import vaarmature as vaarm
    from ..utils import vautils as vau


"""
文法:
http://docs.python.org/py3k/library/string.html#format-string-syntax
http://www.python.jp/doc/nightly/library/string.html#formatstrings (Japanese)
"""


handle = None


# Templates. 後述のRenameData参照
templates = OrderedDict((
    ('Default', {'use_format': True,
                 'use_format2': True,
                 'object_format': 'Cube',
                 'object_format2': '.{0:03d}',
                 'object_values': 'i',
                 'object_sortkey': 'lambda o: o.matrix_world[3][0]',
                 'bone_format': 'Bone',
                 'bone_format2': '.{0:03d}',
                 'bone_values': 'i',
                 'bone_sortkey': 'lambda b: b.head[0]',
                 'replace': False,
                 'replace_pattern': '^.*(?=\.(L|R|Fr|Bk|Bot|Top)$)',
                 'replace_count': 0,
                 'overwrite': False,
                 'smaller': False,
                 'number_pattern': '(^.*\.)(?P<i>\d+)(\.\D+$|$)',
                 'ordertype': 'default'}),
    ('Replace Basename', {'replace': True,
                          'replace_pattern': '^[^\.]*'}),
    ('Replace Number (After period)', {'replace': True,
                                       'replace_pattern': '(?<=\.)\d+'}),
    ('Replace Number', {'replace': True,
                        'replace_pattern': '\d+'}),
    ('Add Head', {'replace': True,
                  'replace_pattern': '^'}),
    ('Add Tail', {'replace': True,
                  'replace_pattern': '$'}),
    ('Cube, Cube.001, Cube.002 ...',
        {'replace': False,
         'object_format': 'Cube',
         'object_format2': '{0}{1:{2}}',
         'object_values': "*('.', i, '03d') if i != 0 else ('', '', '')",
         'bone_format': 'Bone',
         'bone_format2': '{0}{1:{2}}',
         'bone_values': "*('.', i, '03d') if i != 0 else ('', '', '')"})
    ))


class RenameData:
    # TMP_NAME: 名前変更時に重複が有った場合、一時的にこの名前に退避させる。
    TMP_NAME = 'OT_RENAME_OBJECTS_tmp_name'

    def __init__(self, default_tmplate):
        """
        replace: 置換。
        replace_pattern, replace_count: 置換を行う場合に使用。
        overwrite: 重複が有った場合、非選択の方の名前を変える。
        smaller: 重複が有った場合、小さな数値から重複が無いかを探す。
        number_pattern: 重複が有った場合に、数値と判断して増減する文字列。
                         数値にはiの名前を付けておく
        ordertype: 選択object(bone)の並び順。 ('default', 'select', 'sort')
        """
        self.use_format = True
        self.use_format2 = True
        self.object_format = ''
        self.object_format2 = ''
        self.object_values = ''
        self.object_sortkey = ''
        self.bone_format = ''
        self.bone_format2 = ''
        self.bone_values = ''
        self.bone_sortkey = ''
        self.replace = False
        self.replace_pattern = ''
        self.replace_count = 0
        self.overwrite = False
        self.ordertype = 'default'
        self.smaller = False
        self.number_pattern = ''

        self.watching_windows = set()  # context.window.as_pointer()
        self.orderd_objects = OrderedDict()  # selected objects 選択順
        self.orderd_bones = OrderedDict()  # selected bones 選択順

        self.callback_added = False

        # set default template
        for attr, value in default_tmplate.items():
            setattr(self, attr, value)

rd = RenameData(templates['Default'])


class VIEW3D_OT_watch_selected(bpy.types.Operator):
    bl_description = 'Watch selected objects or bones. modal_handler_add()'
    bl_idname = 'view3d.watch_selected'
    bl_label = 'Watch Selected'
    bl_options = {'REGISTER'}

    disable = bpy.props.BoolProperty(name='Disable')

    @classmethod
    def poll(cls, context):
        modes = ('OBJECT', 'POSE', 'EDIT_ARMATURE')
        return context.area is not None and context.mode in modes

    def update_ordered_dict(self, context):
        ordered = None
        if context.mode == 'OBJECT':
            ordered = rd.orderd_objects
            names = {ob.name for ob in context.selected_objects}
        elif context.mode in ('POSE', 'EDIT_ARMATURE'):
            ordered = rd.orderd_bones
            actob = context.active_object
            selected_bones = vaarm.get_selected_bones(actob, mode=context.mode)
            names = {bone.name for bone in selected_bones}
        if ordered is not None:
            for name in list(ordered.keys()):
                if name not in names:
                    del ordered[name]
            for name in names:
                if name not in ordered:
                    ordered[name] = True

    def draw_callback_px(self, context):
        if context.window_manager.rename_objects_update_redraw:
            pointer = context.window.as_pointer()
            if pointer in rd.watching_windows:
                self.update_ordered_dict(context)

    def modal(self, context, event):
        global handle
        windows = bpy.context.window_manager.windows
        pointers = {window.as_pointer() for window in windows}
        rd.watching_windows = rd.watching_windows.intersection(pointers)
        pointer = context.window.as_pointer()
        if pointer in rd.watching_windows:
            if not context.window_manager.rename_objects_update_redraw:
                self.update_ordered_dict(context)
            return {'PASS_THROUGH'}
        else:
            if not rd.watching_windows:
                context.space_data.draw_handler_remove(handle, 'WINDOW')
                handle = None
            return {'FINISHED'}

    def invoke(self, context, event):
        # modal draw
        global handle
        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, 'View3D not found, cannot run operator')
            return {'CANCELLED'}
        pointer = context.window.as_pointer()
        if self.disable:
            if pointer in rd.watching_windows:
                rd.watching_windows.remove(pointer)
            return {'FINISHED'}
        else:
            if pointer in rd.watching_windows:
                return {'FINISHED'}
            else:
                context.window_manager.modal_handler_add(self)
                rd.watching_windows.add(pointer)
                if not handle:
                    handle = context.space_data.draw_handler_add(
                               self.draw_callback_px, (context,),
                               'WINDOW', 'POST_PIXEL')
                return {'RUNNING_MODAL'}


class OBJECT_OT_rename_items:
    bl_description = 'Rename selected objects'
    bl_idname = 'object.rename_objects'
    bl_label = 'Rname Objects'
    bl_options = {'REGISTER', 'UNDO'}

    #mode = bpy.props.StringProperty('Mode', default='', options={'HIDDEN'})
    mode = bpy.props.EnumProperty(
        name='Mode',
        items=(('OBJECT', 'Object', ''),
               ('POSE', 'Pose', ''),
               ('EDIT_ARMATURE', 'Edit Armature', ''),
               ('AUTO', 'Auto', '')),
        default='AUTO',
        options={'HIDDEN'})
    err = bpy.props.StringProperty(
        name='Error',
        description='Error message')

    use_format = bpy.props.BoolProperty(
        name='UseFormat1',
        description='Use Format1',
        default=True)
    use_format2 = bpy.props.BoolProperty(
        name='UseFormat2',
        description='Use Format2',
        default=True)
    format = bpy.props.StringProperty(
        name='Format1',
        default=rd.object_format)
    format2 = bpy.props.StringProperty(
        name='Format2',
        default=rd.object_format2)
    text = 'i(loopIndex), con(=context), scn(scene), actob, ob, bone, ' + \
           'type(object only), name, basename'
    format_values = bpy.props.StringProperty(
        name='Values',
        description=text,
        default=rd.object_values)
    text = 're.sub(ReplacePattern, (Format1+Format2).format(Values), ' + \
           'name, count)'
    replace_pattern = bpy.props.StringProperty(
        name='Replace Pattern',
        description=text,
        default=rd.replace_pattern)
    text = 'sorted(selected_objects, key=SortKey)'
    sortkey = bpy.props.StringProperty(
        name='Sort Key',
        description=text,
        default=rd.object_sortkey)
    text = 'Overlapped: Consider match strings as number'
    number_pattern = bpy.props.StringProperty(
        name='Number', description=text,
        default=rd.number_pattern)

    replace = bpy.props.BoolProperty(
        name='Replace',
        description='Replace names with "re.sub"',
        default=rd.replace)
    replace_count = bpy.props.IntProperty(
        name='Count',
        description='Replace conut',
        default=rd.replace_count, min=0)
    text = 'Overlapped: Rename not selected one'
    overwrite = bpy.props.BoolProperty(
        name='Overwrite',
        description=text,
        default=rd.overwrite)
    text = 'Overlapped: Search smaller number. e.g. Cube.005 -> Cube.000'
    smaller = bpy.props.BoolProperty(
        name='Search Smaller',
        description=text,
        default=rd.smaller)
    ordertype = bpy.props.EnumProperty(
        name='Order Type',
        description='Selected objects order',
        items=(('default', 'Default', ''),
               #('parent', 'Parent', ''),  # 調整中
               ('select', 'Select', ''),
               ('sort', 'Sort', '')),
        default=rd.ordertype)

    @classmethod
    def poll(cls, context):
        return context.mode in ('OBJECT', 'POSE', 'EDIT_ARMATURE')

    def cancel(self, context):
        print('Rename Error: ', self.err)
        self.report({'ERROR'}, 'Invalid format or values.')
        if self.mode == 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
        elif self.mode == 'EDIT_ARMATURE':
            bpy.ops.object.mode_set(mode='EDIT')
        return {'CANCELLED'}

    def save_props(self):
        # save changed format_values
        if self.mode == 'OBJECT':
            rd.object_format = self.format
            rd.object_format2 = self.format2
            rd.object_values = self.format_values
            rd.object_sortkey = self.sortkey
        else:
            rd.bone_format = self.format
            rd.bone_format2 = self.format2
            rd.bone_values = self.format_values
            rd.bone_sortkey = self.sortkey
        rd.use_format = self.use_format
        rd.use_format2 = self.use_format2
        rd.replace = self.replace
        rd.replace_count = self.replace_count
        rd.replace_pattern = self.replace_pattern
        rd.overwrite = self.overwrite
        rd.ordertype = self.ordertype
        rd.smaller = self.smaller
        rd.number_pattern = self.number_pattern

    def get_selected(self, context):
        """self.ordertype == selectの場合はここでソートしておく"""
        if self.mode == 'OBJECT':
            rd.orderd_objects = self.orderd_objects_bak.copy()
            names = rd.orderd_objects.keys()
            objects = bpy.data.objects
            if self.ordertype == 'select' and self.watching:
                selected_objects = [objects[name] for name in names]
            else:
                selected_objects = context.selected_objects
            if self.watching:
                watching_objects = [objects[name] for name in names]
            else:
                watching_objects = []
            return objects, selected_objects, watching_objects
        else:
            rd.orderd_bones = self.orderd_bones_bak.copy()
            names = rd.orderd_bones.keys()
            actob = context.active_object
            if self.mode == 'POSE':
                bones = actob.pose.bones
                if self.ordertype == 'select' and self.watching:
                    selected_bones = [bones[name] for name in names]
                else:
                    selected_bones = vaarm.get_selected_bones(actob, 'POSE')
            else:  # 'EDIT_ARMATURE'
                bones = actob.data.bones
                if self.ordertype == 'select' and self.watching:
                    selected_bones = [bones[name] for name in names]
                else:
                    selected_bones = vaarm.get_selected_bones(actob, 'OBJECT')
            if self.watching:
                watching_bones = [bones[name] for name in names]
            else:
                watching_bones = []
            return bones, selected_bones, watching_bones

    def sort_selected(self, selected_items):
        if self.ordertype == 'parent':
            # 複数回使うのでリストに変換
            items = list(vaob.sorted_objects(selected_items))
        elif self.ordertype == 'sort':
            sortstring = 'sorted(selected_items, key={0})'
            evalsortstring = sortstring.format(self.sortkey)
            try:
                items = eval(evalsortstring)
            except Exception as err:
                if selected_items:
                    print(dir(selected_items[0]))
                self.cancel(err)
                return None
        else:
            items = selected_items
        return items

    def execute(self, context):
        self.save_props()
        self.err = ''
        if self.mode == 'AUTO':
            self.mode = context.mode
        if not self.format and not self.format2:
            return {'FINISHED'}
        pointer = context.window.as_pointer()
        self.watching = pointer in rd.watching_windows
        if self.ordertype == 'select':
            if not self.watching:
                self.report({'WARNING'}, 'Press Observe button')
                return {'FINISHED'}

        bpy.ops.object.mode_set(mode='OBJECT')

        # Get selected
        all_items, selected_items, watching_items = self.get_selected(context)
        selected_items = self.sort_selected(selected_items)
        if selected_items is None:
            self.err = 'No Selections'
            return {'CANCELLED'}

        # Prepare eval()
        f = self.format if self.use_format else ''
        f2 = self.format2 if self.use_format2 else ''
        evalstring = '"{f}{f2}".format({v})'.format(f=f, f2=f2, v=self.format_values)
        # Set locals (used str.format)
        con = context
        scn = context.scene
        actob = context.active_object

        # Rename
        setitems = set(selected_items)
        othernames = {item.name for item in all_items if item not in setitems}
        new_names = set()  # 選択item内で重複しない為に
        item_names = [item.name for item in selected_items]  # 変更を反映しない為に
        num_rename = num_self = num_overwrite = 0  # used Info
        for i, item in enumerate(selected_items):
            # Set locals (used str.format)
            name = item_names[i]
            basename = vau.get_basename(name)
            if self.mode == 'OBJECT':
                ob = item
                bone = ''
                type = ob.type.title()
            else:
                ob = context.active_object
                bone = item
                type = ''

            # Make New Name
            try:  # Check. can make?
                new_name_check = eval(evalstring)
            except Exception as err:
                self.err = err
                return {'CANCELLED'}
            if self.replace:
                replace = (self.replace_pattern, name, self.replace_count)
            else:
                replace = None
            newname = vau.no_overlap_name_eval(
                        evalstring, globals(), locals().copy(),
                        new_names, replace, self.smaller, self.number_pattern)
            if not isinstance(newname, str):
                self.err = newname
                return {'CANCELLED'}

            if newname in othernames:
                if self.overwrite:  # 他を変更
                    replacename = vau.no_overlap_name(newname, othernames,
                                                  self.smaller,
                                                  self.number_pattern)
                    if not isinstance(newname, str):
                        self.err = replacename
                        return {'CANCELLED'}
                    tmp_item = all_items[newname]
                    tmp_item.name = rd.TMP_NAME + str(i)
                    item.name = newname
                    tmp_item.name = replacename
                    num_overwrite += 1
                else:  # 自己を変更
                    if self.replace:
                        replace = (self.replace_pattern, name,
                                   self.replace_count)
                    else:
                        replace = None
                    replacename = vau.no_overlap_name_eval(evalstring, globals(),
                                          locals().copy(), othernames, replace,
                                          self.smaller, self.number_pattern)
                    if not isinstance(newname, str):
                        self.err = newname
                        return {'CANCELLED'}
                    if replacename in [item.name for item in selected_items]:
                        # 選択itemの中に同名が有る場合(=未処理)それをtmp名に退避
                        tmp_item = all_items[replacename]
                        tmp_item.name = rd.TMP_NAME + str(i)
                    newname = replacename
                    item.name = newname
                    num_self += 1
                othernames.add(replacename)
            else:
                if newname in [item.name for item in selected_items]:
                    # 選択itemの中に同名が有る場合(=未処理)、それをtmp名に退避。
                    tmp_item = all_items[newname]
                    tmp_item.name = rd.TMP_NAME + str(i)
                othernames.add(newname)
                item.name = newname
                num_rename += 1
            new_names.add(newname)

        # save changed format_values
        if self.mode == 'OBJECT':
            txt = 'Rename:{0}, Self:{1}, Overwrite:{2}'
            infotxt = txt.format(num_rename, num_self, num_overwrite)
            self.report({'INFO'}, infotxt)
            if self.watching:
                rd.orderd_objects.clear()
                for ob in watching_items:
                    rd.orderd_objects[ob.name] = True
        else:
            infotxt = 'Rename {0} bones'.format(len(selected_items))
            self.report({'INFO'}, infotxt)
            if self.watching:
                rd.orderd_bones.clear()
                for ob in watching_items:
                    rd.orderd_bones[ob.name] = True
            if self.mode == 'POSE':
                bpy.ops.object.mode_set(mode='POSE')
            else:
                bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

    def invoke(self, context, event):
        if self.mode == 'AUTO':
            self.mode = context.mode
        if self.mode == 'OBJECT':
            self.format = rd.object_format
            self.format2 = rd.object_format2
            self.format_values = rd.object_values
            self.sortkey = rd.object_sortkey
            self.orderd_objects_bak = rd.orderd_objects.copy()
        else:
            self.format = rd.bone_format
            self.format2 = rd.bone_format2
            self.format_values = rd.bone_values
            self.sortkey = rd.bone_sortkey
            self.orderd_bones_bak = rd.orderd_bones.copy()
        self.use_format = rd.use_format
        self.use_format2 = rd.use_format2
        self.replace = rd.replace
        self.replace_count = rd.replace_count
        self.replace_pattern = rd.replace_pattern
        self.overwrite = rd.overwrite
        self.ordertype = rd.ordertype
        pointer = context.window.as_pointer()
        watching = pointer in rd.watching_windows
        if watching:
            self.ordertype = 'select'
        else:
            if self.ordertype == 'select':
                self.ordertype = 'default'
        self.smaller = rd.smaller
        self.number_pattern = rd.number_pattern

        wm = context.window_manager
        wm.invoke_props_dialog(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label('Python: (Format1+Format2).format(Values)')
        row = layout.row()
        row.prop(self, 'format', text='Format1')
        row.prop(self, 'use_format', text='')
        row = layout.row()
        row.prop(self, 'format2', text='Format2')
        row.prop(self, 'use_format2', text='')
        layout.prop(self, 'format_values', text='Values')
        layout.prop(self, 'replace_pattern', text='ReplacePattern')
        layout.prop(self, 'sortkey', text='SortKey')
        layout.prop(self, 'number_pattern', text='Number')
        sub = layout.row(align=True)
        sub.prop(self, 'replace', text='Replace', toggle=True)
        sub.prop(self, 'replace_count', text='Count')
        sub = layout.row(align=True)
        sub.prop(self, 'overwrite', text='Overwrite', toggle=True)
        sub.prop(self, 'smaller', text='Smaller', toggle=True)
        layout.prop(self, 'ordertype', text='Order Type', expand=True)


class OBJECT_OT_rename_objects(OBJECT_OT_rename_items, bpy.types.Operator):
    bl_description = 'Rename selected objects'
    bl_idname = 'object.rename_objects'
    bl_label = 'Rname Objects'

class ARMATURE_OT_rename_bones(OBJECT_OT_rename_items, bpy.types.Operator):
    bl_description = 'Rename selected bones'
    bl_idname = 'armature.rename_bones'
    bl_label = 'Rname Bones'


class VIEW3D_OT_rename_objects_set_template(bpy.types.Operator):
    bl_idname = 'view3d.rename_objects_set_template'
    bl_label = 'Set Rename Template'
    bl_description = 'Select Template. Default:Reset all values'
    bl_options = {'REGISTER'}

    template_name = bpy.props.StringProperty('Name')

    def execute(self, context):
        for attr, value in templates[self.template_name].items():
            setattr(rd, attr, value)
        return {'FINISHED'}


class VIEW3D_MT_rename_objects_template(bpy.types.Menu):
    bl_label = 'Template'

    def draw(self, contex):
        layout = self.layout
        names = [key for key in templates.keys()]
        for name in templates.keys():
            op = 'view3d.rename_objects_set_template'
            layout.operator(op, text=name).template_name = name


class VIEW3D_PT_rename_objects(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    bl_label = 'Rename Selections'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        modes = ('OBJECT', 'POSE', 'EDIT_ARMATURE')
        return context.area is not None and context.mode in modes

    def draw_header(self, context):
        if context.mode in ('POSE', 'EDIT_ARMATURE'):
            self.bl_label = 'Rename Bones'
        else:
            self.bl_label = 'Rename Objects'

    def draw(self, context):
        # running modal ?
        pointer = context.window.as_pointer()
        watching = pointer in rd.watching_windows

        layout = self.layout
        col = layout.column()

        if context.mode in ('POSE', 'EDIT_ARMATURE'):
            col.operator('armature.rename_bones')
        else:
            col.operator('object.rename_objects')

        row = col.row(align=True)
        if watching:
            row.label('', icon='REC')
            op = row.operator('view3d.watch_selected',
                              text='Observe')
            op.disable = True
        else:
            row.label('', icon='PAUSE')
            op = row.operator('view3d.watch_selected', text='Observe')
            op.disable = False
        row.prop(context.window_manager, 'rename_objects_update_redraw',
                 text='')
        col.menu('VIEW3D_MT_rename_objects_template', text='Template',
                 icon='TRIA_DOWN')


classes = [
    VIEW3D_OT_watch_selected,
    OBJECT_OT_rename_objects,
    ARMATURE_OT_rename_bones,
    VIEW3D_OT_rename_objects_set_template,
    VIEW3D_MT_rename_objects_template,
    VIEW3D_PT_rename_objects,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.rename_objects_update_redraw = \
        bpy.props.BoolProperty(
            name='Update when Redraw',
            description='Update ordered dict for each redraw '
                        '(e.g. Circle Select)')


def unregister():
    if bpy.context.window_manager.get('rename_objects_update_redraw') != None:
        del bpy.context.window_manager['rename_objects_update_redraw']
    if hasattr(bpy.types.WindowManager, 'rename_objects_update_redraw'):
        del bpy.types.WindowManager.rename_objects_update_redraw
    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
