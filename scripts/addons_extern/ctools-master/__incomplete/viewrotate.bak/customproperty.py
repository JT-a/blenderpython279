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


import bpy


class _CollectionOperator:
    """CollectionPropertyに対する複数のオペレータを纏めて登録する。

    最初にregister_classでこのクラスを登録しておく。
    >>> bpy.utils.register_class(CollectionOperator)

    bpy.ops.wm.collection_add(data_path='', function='')
    bpy.ops.wm.collection_remove(data_path='', function='', index=0)
    bpy.ops.wm.collection_clear(data_path='', function='')
    bpy.ops.wm.collection_move(data_path='', function='', index_from=0,
                               index_to=0)

    data_path引数を指定するとcontext属性を参照する。
    function引数を使う場合は、事前にregister_functionクラスメソッドで関数を
    登録しておく。
    """

    class _Operator:
        bl_description = ''
        bl_options = {'REGISTER', 'INTERNAL'}

        _functions = None
        """:type: dict"""

        data_path = bpy.props.StringProperty(options={'SKIP_SAVE'})
        function = bpy.props.StringProperty(options={'SKIP_SAVE'})

        @classmethod
        def register_function(cls, key, func):
            cls._functions[key] = func

        @classmethod
        def register(cls):
            mod, func = cls.bl_idname.split('.')
            name = mod.upper() + '_OT_' + func.lower()
            cls_ = getattr(bpy.types, name)
            if cls == cls_:
                cls._functions = {}
            else:
                cls._functions = cls_._functions

        @classmethod
        def unregister(cls):
            cls._functions = None

    class _Add(_Operator):
        """
        hoge = []
        def add_item(context):
            hoge.append({'fuga': 1, 'piyo': 2})
        OperatorCollectionAdd.register_function('list_hoge', add_item)
        bpy.ops.wm.collection_add(function='list_hoge')
        """

        bl_idname = 'wm.collection_add'
        bl_label = 'Collection Add'

        def execute(self, context):
            if self.data_path:
                collection = eval('bpy.context.' + self.data_path)
                collection.add()
            if self.function:
                self._functions[self.function](context)
            return {'FINISHED'}

    class _Remove(_Operator):
        """
        hoge = []
        def remove_item(context, index):
            hoge[:] = hoge[:index] + hoge[index + 1:]
        OperatorCollectionAdd.register_function('list_hoge', remove_item)
        bpy.ops.wm.collection_remove(function='list_hoge')
        """

        bl_idname = 'wm.collection_remove'
        bl_label = 'Collection Remove'

        index = bpy.props.IntProperty(options={'SKIP_SAVE'})

        def execute(self, context):
            if self.data_path:
                collection = eval('bpy.context.' + self.data_path)
                collection.remove(self.index)
            if self.function:
                self._functions[self.function](context, self.index)
            return {'FINISHED'}

    class _Clear(_Operator):
        bl_idname = 'wm.collection_clear'
        bl_label = 'Collection Clear'

        def execute(self, context):
            if self.data_path:
                collection = eval('bpy.context.' + self.data_path)
                collection.clear()
            if self.function:
                self._functions[self.function](context)
            return {'FINISHED'}

    class _Move(_Operator):
        bl_idname = 'wm.collection_move'
        bl_label = 'Collection Move'

        index_from = bpy.props.IntProperty(options={'SKIP_SAVE'})
        index_to = bpy.props.IntProperty(options={'SKIP_SAVE'})

        def execute(self, context):
            if self.data_path:
                collection = eval('bpy.context.' + self.data_path)
                collection.move(self.index_from, self.index_to)
            if self.function:
                self._functions[self.function](context, self.index_from,
                                               self.index_to)
            return {'FINISHED'}

    class Add(_Add, bpy.types.Operator):
        pass
    class Remove(_Remove, bpy.types.Operator):
        pass
    class Clear(_Clear, bpy.types.Operator):
        pass
    class Move(_Move, bpy.types.Operator):
        pass

    @classmethod
    def _to_bl_idname(cls, name):
        """windowmanager/intern/wm_operators.c
        WM_operator_py_idname: SOME_OT_op -> some.op
        WM_operator_bl_idname: some.op -> SOME_OT_op
        :type name: str
        :rtype: str
        """
        mod, func = name.split('.')
        return mod.upper() + '_OT_' + func

    @classmethod
    def _increment(cls, name):
        import re
        m = re.match('(.*?)(\d*)$', name)
        return m.group(1) + str((int(m.group(2)) + 1) if m.group(2) else 1)

    @classmethod
    def register(cls):
        for c in [cls.Add, cls.Remove, cls.Clear, cls.Move]:
            while hasattr(bpy.types, cls._to_bl_idname(c.bl_idname)):
                c.bl_idname = cls._increment(c.bl_idname)
            bpy.utils.register_class(c)

    @classmethod
    def unregister(cls):
        for c in [cls.Add, cls.Remove, cls.Clear, cls.Move]:
            bpy.utils.unregister_class(c)

    @classmethod
    def new_class(cls):
        """:rtype: CollectionOperator"""
        name_space = {
            'Add': type('Add', (cls._Add, bpy.types.Operator), {}),
            'Remove': type('Remove', (cls._Remove, bpy.types.Operator), {}),
            'Clear': type('Clear', (cls._Clear, bpy.types.Operator), {}),
            'Move': type('Move', (cls._Move, bpy.types.Operator), {}),
        }
        return type('CollectionOperator',
                    (_CollectionOperator, bpy.types.PropertyGroup),
                    name_space)


class CollectionOperator(_CollectionOperator, bpy.types.PropertyGroup):
    pass


class _CustomProperty:
    class _Data:
        class Prop:
            def __init__(self, prop):
                self.prop = prop
                self.users = set()

        def __init__(self):
            self.wm_attribute = 'custom_property'

            # {id(obj)/obj.as_pointer(): {attr: Prop, ...}, ...}
            self.custom_properties = {}
            self.dynamic_properties = {}  # property()用
            # {id(obj)/obj.as_pointer(): obj, ...}
            self.key_object = {}  # property()用

            # {wm_attr: [obj, attr, ob, prop], ...}
            # 現在、値はpropしか利用していない
            self.attribute_property = {}

            self.temporary_data = None

        def key_props(self, obj, dynamic, create=True):
            """obj用のキーとその辞書を返す"""
            if dynamic:
                properties = self.dynamic_properties
            else:
                properties = self.custom_properties
            if isinstance(obj, bpy.types.bpy_struct):
                key = obj.as_pointer()
            else:
                key = id(obj)
            if create and key not in properties:
                properties[key] = {}
            return key, properties

        def add_property(self, obj, attr, prop, dynamic):
            key, properties = self.key_props(obj, dynamic)
            ob_props = properties[key]
            if attr in ob_props:
                ob_props[attr].prop = prop
            else:
                ob_props[attr] = self.Prop(prop)
            if dynamic:
                self.key_object[key] = obj

        def remove_property(self, obj, attr, dynamic):
            key, properties = self.key_props(obj, dynamic)
            del properties[key][attr]
            if not properties[key]:
                del properties[key]
                if dynamic:
                    del self.key_object[key]

    _data = _Data()

    class _Utils:
        def __get__(self, instance, owner):
            self._cls = owner
            return self

        def __init__(self):
            self._cls = None
            """:type: _CustomProperty"""

        space_types = {
            'EMPTY': bpy.types.Space,
            'NONE': bpy.types.Space,
            'CLIP_EDITOR': bpy.types.SpaceClipEditor,
            'CONSOLE': bpy.types.SpaceConsole,
            'DOPESHEET_EDITOR': bpy.types.SpaceDopeSheetEditor,
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

        def _space_porperty_id_prop_key(self, obj, attr):
            return 'space_property_{}_{}'.format(obj.__name__, attr)

        def register_space_property(self, obj, attr, prop):
            import inspect
            if not inspect.isclass(obj):
                raise ValueError()

            if obj not in self.space_types.values():
                raise ValueError()

            cls = self._cls

            cls.dynamic_property(obj, attr, prop)

            idprop_key = self._space_porperty_id_prop_key(obj, attr)

            @bpy.app.handlers.persistent
            def saev_pre(scene):
                for screen in bpy.data.screens:
                    data = []
                    data_used = []
                    for area in screen.areas:
                        for space in area.spaces:
                            if isinstance(space, obj):
                                value = cls.prop_to_py(space, attr, True)
                                if value is None:
                                    data_used.append(False)
                                else:
                                    data.append(value)
                                    data_used.append(True)
                    screen[idprop_key] = data
                    screen['_' + idprop_key] = data_used

            saev_pre.key = idprop_key
            bpy.app.handlers.save_pre.append(saev_pre)

            @bpy.app.handlers.persistent
            def load_post(scene):
                custom_prop = cls.active()
                for screen in bpy.data.screens:
                    data = screen.get(idprop_key)
                    data_used = screen.get('_' + idprop_key)
                    if data and data_used:
                        i = j = 0
                        try:
                            for area in screen.areas:
                                for space in area.spaces:
                                    if isinstance(space, obj):
                                        a = cls.attribute(space, attr, True)
                                        if data_used[i]:
                                            custom_prop[a] = data[j]
                                            j += 1
                                        i += 1
                        except:
                            import traceback
                            traceback.print_exc()
                    if data is not None:
                        del screen[idprop_key]
                    if data_used is not None:
                        del screen['_' + idprop_key]

            load_post.key = idprop_key
            bpy.app.handlers.load_post.append(load_post)

        def unregister_space_property(self, obj, attr):
            import inspect
            if not inspect.isclass(obj):
                raise ValueError()

            if obj not in self.space_types.values():
                raise ValueError()

            cls = self._cls

            idprop_key = self._space_porperty_id_prop_key(obj, attr)

            cls.dynamic_property_delete(obj, attr)

            for func in bpy.app.handlers.save_pre:
                if getattr(func, 'key', None) == idprop_key:
                    bpy.app.handlers.save_pre.remove(func)
            for func in bpy.app.handlers.load_post:
                if getattr(func, 'key', None) == idprop_key:
                    bpy.app.handlers.load_post.remove(func)

    utils = _Utils()  # registerの時に初期化するからNoneは仮

    def _fget(self):
        return False

    def _fset(self, value):
        cls = self.__class__
        data = cls._data
        if data.temporary_data is not None:
            attr, prop = data.temporary_data
            setattr(cls, attr, prop)
            data.temporary_data = None
    attribute_set_trigger = bpy.props.BoolProperty(get=_fget, set=_fset)

    def _fget(self):
        return False

    def _fset(self, value):
        cls = self.__class__
        data = cls._data
        if data.temporary_data is not None:
            attr = data.temporary_data
            delattr(cls, attr)
            data.temporary_data = None

    attribute_delete_trigger = bpy.props.BoolProperty(get=_fget, set=_fset)
    del _fget, _fset

    # # bpy.app.handlers.persistentで関数に追加される属性。値はNone。
    # PERMINENT_CB_ID = '_bpy_persistent'

    @classmethod
    def active(cls):
        """PointerPropertyとしてのPyCustomPropertyを返す。
        :rtype: _CustomProperty
        """
        return getattr(bpy.context.window_manager, cls._data.wm_attribute)

    @classmethod
    def attribute(cls, obj, attr, dynamic):
        """PyCustomPropertyの属性名を返す
        :type obj: T
        :type attr: str
        :type dynamic: bool
        :rtype: str
        """
        import inspect
        if inspect.isclass(obj):
            if issubclass(obj, bpy.types.bpy_struct):
                name = 'bpy_struct_' + obj.__name__
            else:
                name = obj.__name__
        else:
            name = obj.__class__.__name__
        if isinstance(obj, bpy.types.bpy_struct):
            id_value = obj.as_pointer()
        else:
            id_value = id(obj)
        if dynamic:
            head = 'dyn'
        else:
            head = 'cus'
        return '{}_{}_{}_{}'.format(head, name, id_value, attr)

    @classmethod
    def _gen_dynamic_property(cls, attr):
        """property()用のget,set関数を作って、それをproperty()に渡して
        結果を返す
        """
        def fget(self):
            wm_attr = cls.attribute(self, attr, True)
            cls.ensure(self, attr)
            wm_custom_prop = cls.active()
            return getattr(wm_custom_prop, wm_attr)

        def fset(self, value):
            wm_attr = cls.attribute(self, attr, True)
            cls.ensure(self, attr)
            wm_custom_prop = cls.active()
            setattr(wm_custom_prop, wm_attr, value)

        return property(fget, fset)

    @classmethod
    def dynamic_property(cls, obj, attr, prop):
        """プロパティを登録する
        :param obj: クラス
        :type obj: T
        :param attr: 属性名の文字列
        :type attr: str
        :param prop: (bpy.props.BoolProperty, {'name': 'Test', ...})
        :type prop: tuple
        """
        import inspect
        if not inspect.isclass(obj):
            raise ValueError()

        cls._data.add_property(obj, attr, prop, True)

        setattr(obj, attr, cls._gen_dynamic_property(attr))

    @classmethod
    def _property_delete(cls, obj, attr, dynamic):
        wm_custom_prop = cls.active()
        key, properties = cls._data.key_props(obj, dynamic)
        ob_prop = properties[key][attr]
        for wm_attr in ob_prop.users:
            cls._data.temporary_data = wm_attr
            wm_custom_prop.attribute_delete_trigger = True
        cls._data.remove_property(obj, attr, dynamic)

    @classmethod
    def dynamic_property_delete(cls, obj, attr):
        import inspect
        if not inspect.isclass(obj):
            raise ValueError()

        cls._property_delete(obj, attr, True)
        delattr(obj, attr)

    @classmethod
    def custom_property(cls, obj, attr, prop, ensure=True):
        """プロパティを登録する
        :param obj: インスタンスかそのクラス
        :type obj: T
        :param attr: 属性名の文字列。コンテナのキー等の場合は角括弧で囲む。
            例: 'hoge', '["key"]', '[2]', 'collection[5]', 'foo.bar.baz'
        :type attr: str
        :param prop: (bpy.props.BoolProperty, {'name': 'Test', ...})
        :type prop: tuple
        :type ensure: bool
        """

        cls._data.add_property(obj, attr, prop, False)

        if ensure:
            return cls.ensure(obj, attr)[attr]

    @classmethod
    def custom_property_delete(cls, obj, attr):
        cls._property_delete(obj, attr, False)
        delattr(obj, attr)

    @classmethod
    def _gen_dynamic_property_functions(cls, obj, attr, wm_attr, prop):
        """objはインスタンス"""
        # get function ----------------------------------------------
        if 'get' in prop[1]:
            def fget(self, func=prop[1]['get']):
                return func(obj)
            fget._get = prop[1]['get']
        else:
            fget = None

        # set function ----------------------------------------------
        if 'set' in prop[1]:
            def fset(self, value, func=prop[1]['set']):
                func(obj, value)
            fset._set = prop[1]['set']
        else:
            fset = None

        # update function -------------------------------------------
        if 'update' in prop[1]:
            def update(self, context, func=prop[1]['update']):
                func(obj, context)
            update._update = prop[1]['update']
        else:
            update = None

        return fget, fset, update

    @classmethod
    def _gen_custom_property_functions(cls, obj, attr, wm_attr, prop):
        def get_value():
            try:
                if attr.startswith('['):
                    return eval('obj' + attr, {'obj': obj})
                else:
                    return eval('obj.' + attr, {'obj': obj})
            except:
                # クラスを登録していてインスタンスのみensureしている状態で
                # コンソールで補完した時に警告がうるさいのでコメントアウト
                # import traceback
                # print("{} Error: {} '{}' '{}'".format(
                #       cls.__name__, obj, attr, wm_attr))
                # traceback.print_exc()
                return None

        def set_value(value):
            import traceback
            try:
                if attr.startswith('['):
                    code = 'obj{} = value'.format(attr)
                else:
                    code = 'obj.{} = value'.format(attr)
                exec(code, {'obj': obj, 'value': value})
            except:
                print("{} Error: '{}'".format(
                      cls.__name__, attr, wm_attr))
                traceback.print_exc()

        # get function ----------------------------------------------
        if 'get' in prop[1]:
            def fget(self, func=prop[1]['get']):
                return func(obj)

            fget._get = prop[1]['get']

        else:
            def fget(self):
                import inspect
                import traceback
                bl_rna = self.__class__.bl_rna
                p = bl_rna.properties[wm_attr]

                if prop[0] == bpy.props.EnumProperty:
                    items = prop[1]['items']
                    is_function = inspect.isfunction(items)
                    if is_function:
                        items = items(obj, bpy.context)

                    value = get_value()

                    if p.is_enum_flag:
                        def set_to_int(value):
                            r = 0
                            for i, (identifier, *_) in enumerate(items):
                                try:
                                    if identifier in value:
                                        r += 1 << i
                                except:
                                    print("{} Error: '{}'".format(
                                        cls.__name__, attr, wm_attr))
                                    traceback.print_exc()
                                    return -1
                            return r

                        if value is None:
                            int_value = -1
                        else:
                            int_value = set_to_int(value)
                        if int_value == -1:
                            if is_function:
                                int_value = 0
                            else:
                                int_value = set_to_int(p.default_flag)
                        return int_value

                    else:
                        def str_to_int(value):
                            for i, (identifier, *_) in enumerate(items):
                                if identifier == value:
                                    return i
                            return -1

                        if value is None:
                            int_value = -1
                        else:
                            int_value = str_to_int(value)
                        if int_value == -1:
                            if is_function:
                                int_value = 0
                            else:
                                int_value = str_to_int(p.default)
                        return int_value
                else:
                    value = get_value()
                    t = {'BOOLEAN': bool, 'INT': int, 'FLOAT': float,
                         'STRING': str}
                    if getattr(p, 'is_array', False):
                        if value is not None and p.type in t:
                            invalid = False
                            try:
                                ls = list(value)
                                for elem in ls:
                                    if not isinstance(elem, t[p.type]):
                                        invalid = True
                                        break
                                if not invalid:
                                    if len(value) != p.array_length:
                                        invalid = True
                            except:
                                invalid = True
                            if invalid:
                                print("{} error: get function of '{}'".format(
                                    cls.__name__, wm_attr))
                                print('Expected <type: {}, length: {}>, '
                                      'got {} {}'.format(
                                    p.type, p.array_length, type(value),
                                    value))
                                value = None
                        if value is None:
                            value = tuple(p.default_array)
                    else:
                        if value is not None and p.type in t:
                            invalid = False
                            try:
                                if not isinstance(value, t[p.type]):
                                    invalid = True
                            except:
                                invalid = True
                            if invalid:
                                print("{} error: get function of '{}'".format(
                                    cls.__name__, wm_attr))
                                print('Expected <type: {}>, '
                                      'got {} {}'.format(p.type, type(value),
                                                         value))
                                value = None
                        if value is None:
                            value = p.default
                    return value

        # set function ----------------------------------------------
        if 'set' in prop[1]:
            def fset(self, value, func=prop[1]['set']):
                func(obj, value)
            fset._set = prop[1]['set']

        else:
            def fset(self, value):
                import inspect
                bl_rna = self.__class__.bl_rna
                p = bl_rna.properties[wm_attr]

                if prop[0] == bpy.props.EnumProperty:
                    items = prop[1]['items']
                    if inspect.isfunction(items):
                        items = items(obj, bpy.context)
                    if p.is_enum_flag:
                        identifiers = []
                        for i, (identifier, *_) in enumerate(items):
                            if (1 << i) & value:
                                identifiers.append(identifier)
                        # 型を合わせる
                        prev_value = get_value()
                        if isinstance(prev_value, tuple):
                            set_value(tuple(identifiers))
                        elif isinstance(prev_value, set):
                            set_value(set(identifiers))
                        else:
                            set_value(identifiers)
                    else:
                        for i, (identifier, *_) in enumerate(items):
                            if i == value:
                                set_value(identifier)
                                break
                else:
                    if getattr(p, 'is_array', False):
                        # 型を合わせる
                        prev_value = get_value()
                        if isinstance(prev_value, tuple):
                            set_value(tuple(value))
                        else:
                            set_value(list(value))
                    else:
                        set_value(value)

                # IDPropertyへの適用
                wm_custom_prop = cls.active()
                wm_custom_prop[wm_attr] = value

        # update function -------------------------------------------
        if 'update' in prop[1]:
            def update(self, context, func=prop[1]['update']):
                func(obj, context)
            update._update = prop[1]['update']
        else:
            update = None

        return fget, fset, update

    @classmethod
    def ensure(cls, obj, *attributes):
        """各オブジェクト用のプロパティを追加する
        attrが空なら登録済みの属性を全て適用する
        :return: 属性名をキー、それが使用するカスタムプロパティの属性名を値と
            した辞書を返す。
            ただしcustomとdynamic両方が登録されていて共に有効なら
            辞書の値は (customの属性名, dynamicの属性名) となる。
        :rtype: dict
        """
        from collections import OrderedDict

        attr_mapping = {}

        wm_custom_prop = cls.active()
        data = cls._data

        attr_prop = OrderedDict()
        for ob in [obj, obj.__class__]:
            for dynamic in (False, True):
                key, properties = data.key_props(ob, dynamic)
                ob_props = properties[key]
                for attr in (attributes or ob_props.keys()):
                    if attr in ob_props and (attr, dynamic) not in attr_prop:
                        if dynamic and ob is obj:
                            continue
                        attr_prop[(attr, dynamic)] = [ob, ob_props]

        for (attr, dynamic), (ob, ob_props) in attr_prop.items():
            ob_prop = ob_props[attr]
            prop = ob_prop.prop
            wm_attr = cls.attribute(obj, attr, dynamic)

            # 変更が無ければ飛ばす
            if wm_attr in data.attribute_property:
                obj_, attr_, ob_, prop_ = data.attribute_property[wm_attr]
                if prop_ == prop:
                    if attr in attr_mapping:
                        attr_mapping[attr] = (attr_mapping[attr], wm_attr)
                    else:
                        attr_mapping[attr] = wm_attr
                    continue

                # これを利用してるものを消す
                for wm_attr_ in ob_prop.users:
                    if hasattr(cls, wm_attr_):
                        data.temporary_data = wm_attr_
                        wm_custom_prop.attribute_delete_trigger = True
                        del data.attribute_property[wm_attr_]
                ob_prop.users.clear()

            if dynamic:
                fget, fset, update = cls._gen_dynamic_property_functions(
                    obj, attr, wm_attr, prop)
            else:
                fget, fset, update = cls._gen_custom_property_functions(
                    obj, attr, wm_attr, prop)
            prop_new = (prop[0], prop[1].copy())
            if fget:
                prop_new[1]['get'] = fget
            if fset:
                prop_new[1]['set'] = fset
            if update:
                prop_new[1]['update'] = update

            # 属性追加の為の関数を呼び出す
            data.temporary_data = [wm_attr, prop_new]
            wm_custom_prop.attribute_set_trigger = True

            data.attribute_property[wm_attr] = [obj, attr, ob, prop]
            ob_props[attr].users.add(wm_attr)
            if attr in attr_mapping:
                attr_mapping[attr] = (attr_mapping[attr], wm_attr)
            else:
                attr_mapping[attr] = wm_attr

        return attr_mapping

    @classmethod
    def _increment(cls, name):
        import re
        m = re.match('(.*?)(\d*)$', name)
        return m.group(1) + str((int(m.group(2)) + 1) if m.group(2) else 1)

    @classmethod
    def idprop_to_py(cls, prop):
        if isinstance(prop, list):
            return [cls.idprop_to_py(p) for p in prop]
        elif hasattr(prop, 'to_dict'):
            return prop.to_dict()
        elif hasattr(prop, 'to_list'):
            return prop.to_list()
        else:
            return prop

    @classmethod
    def prop_to_py(cls, obj, attr, dynamic=None):
        """IDPropertyをpythonの組み込み型に変換して返す
        :type obj: T
        :type attr: str
        :param dynamic: Noneなら両方
        :type dynamic: bool | None
        :return: dynamicがNoneでcustomとdynamic両方あるなら
            (customのプロパティ, dynamicのプロパティ) を返す。
            dynamicが真か偽ならそれぞれのプロパティを返す。
            存在しないならNoneを返す
        """
        wm_custom_prop = cls.active()
        prop_custom = prop_dynamic = None
        if dynamic is None or not dynamic:
            attr = cls.attribute(obj, attr, False)
            if attr in wm_custom_prop:
                prop_custom = cls.idprop_to_py(wm_custom_prop[attr])
        if dynamic is None or dynamic:
            attr = cls.attribute(obj, attr, True)
            if attr in wm_custom_prop:
                prop_dynamic = cls.idprop_to_py(wm_custom_prop[attr])
        if dynamic is None:
            if prop_custom is not None and prop_dynamic is not None:
                return prop_custom, prop_dynamic
            elif prop_custom is not None:
                return prop_custom
            else:
                return prop_dynamic
        elif dynamic:
            return prop_dynamic
        else:
            return prop_custom

    @classmethod
    def register(cls):
        data = cls._data = cls._Data()
        cls.utils = cls._Utils()

        while hasattr(bpy.types.WindowManager, data.wm_attribute):
            data.wm_attribute = cls._increment(data.wm_attribute)
        setattr(bpy.types.WindowManager, data.wm_attribute,
                bpy.props.PointerProperty(type=cls))

    @classmethod
    def unregister(cls):
        data = cls._data

        for ob_key, ob_props in data.dynamic_properties.items():
            if ob_key in data.key_object:
                obj = data.key_object[ob_key]
            for attr in ob_props:
                if hasattr(obj, attr):
                    delattr(obj, attr)

        custom_prop = cls.active()
        for attr in data.attribute_property:
            # delete custom property
            if hasattr(cls, attr):
                delattr(cls, attr)
            # delete ID Property
            if attr in custom_prop:
                del custom_prop[attr]

        delattr(bpy.types.WindowManager, data.wm_attribute)

        cls._data = cls._Data()
        cls.utils = cls._Utils()

    @classmethod
    def new_class(cls):
        """:rtype: CustomProperty"""
        return type('CustomProperty',
                    (_CustomProperty, bpy.types.PropertyGroup), {})


class CustomProperty(_CustomProperty, bpy.types.PropertyGroup):
    pass


def test():
    """実行すると3DViewのPropertiesパネルにCustomPanelが表示され、
    端末にpython objectの各属性の値が出力される。
    >>> import customproperty
    >>> customproperty.test()
    """

    CP = CustomProperty.new_class()
    bpy.utils.register_class(CP)
    OP = CollectionOperator.new_class()
    bpy.utils.register_class(OP)

    class CustomItem:
        def __init__(self):
            self.a = 1

    class CustomGroup:
        def __init__(self):
            self.int_value = 1
            self.float_value = 1.0
            self.bool_value = True
            self.str_value = '100'

            self.int_array = [1,2,3]
            self.float_array = [1.0, 2.0, 3.0]
            self.bool_array = [True, False, True]

            self.enum = 'A'
            self.enum_flag = ['A', 'B']
            self.enum_flag_func = {'invalidvalue', 'B'}  # わざと不正な値を含めている

            self.item_list = []

    group = CustomGroup()

    class CustomPanel(bpy.types.Panel):
        bl_label = 'Custom Panel'
        bl_idname = 'CustomPanel'
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'

        def draw(self, context):
            # プロパティの登録
            wm_custom_prop = CP.active()
            wm_custom_prop.custom_property(
                CustomGroup, 'int_value', bpy.props.IntProperty())
            wm_custom_prop.custom_property(
                CustomGroup, 'float_value', bpy.props.FloatProperty())
            wm_custom_prop.custom_property(
                CustomGroup, 'bool_value', bpy.props.BoolProperty())
            wm_custom_prop.custom_property(
                CustomGroup, 'str_value', bpy.props.StringProperty())

            wm_custom_prop.custom_property(
                CustomGroup, 'int_array',
                bpy.props.IntVectorProperty(size=3))
            wm_custom_prop.custom_property(
                CustomGroup, 'float_array',
                bpy.props.FloatVectorProperty(size=3))
            wm_custom_prop.custom_property(
                CustomGroup, 'bool_array',
                bpy.props.BoolVectorProperty(size=3))

            wm_custom_prop.custom_property(
                CustomGroup, 'bool_array[1]',
                bpy.props.BoolProperty()
            )

            wm_custom_prop.custom_property(
                CustomGroup, 'enum',
                bpy.props.EnumProperty(
                    items=[('A', 'A', ''), ('B', 'B', ''), ('C', 'C', '')]))
            wm_custom_prop.custom_property(
                CustomGroup, 'enum_flag',
                bpy.props.EnumProperty(
                    items=[('A', 'A', ''), ('B', 'B', ''), ('C', 'C', '')],
                    options={'ENUM_FLAG'}))
            def items_get(self, context):
                items = [('A', 'A', ''), ('B', 'B', ''), ('C', 'C', '')]
                items_get._items = items
                return items
            wm_custom_prop.custom_property(
                CustomGroup, 'enum_flag_func',
                bpy.props.EnumProperty(items=items_get, options={'ENUM_FLAG'}))

            layout = self.layout

            # 描画
            attrs = wm_custom_prop.ensure(group)
            layout.prop(wm_custom_prop, attrs['int_value'])
            layout.prop(wm_custom_prop, attrs['float_value'])
            layout.prop(wm_custom_prop, attrs['bool_value'])
            layout.prop(wm_custom_prop, attrs['str_value'])

            layout.prop(wm_custom_prop, attrs['int_array'])
            layout.prop(wm_custom_prop, attrs['float_array'])
            layout.prop(wm_custom_prop, attrs['bool_array'])

            layout.prop(wm_custom_prop, attrs['bool_array[1]'])

            layout.prop(wm_custom_prop, attrs['enum'])
            layout.prop(wm_custom_prop, attrs['enum_flag'])
            layout.prop(wm_custom_prop, attrs['enum_flag_func'])

            # group.item_listの登録と描画

            # CustomGroup.item_listへの要素を追加するオペレータの登録
            identifier = str(id(group)) + '_collection'
            def item_add_func(context, group=group):
                group.item_list.append(CustomItem())
            OP.Add.register_function(
                identifier, item_add_func)
            # ボタン描画
            op = layout.operator(OP.Add.bl_idname, text='Add')
            op.function = identifier

            def draw_item(layout, obj):
                wm_custom_prop.custom_property(
                    CustomItem, 'a', bpy.props.IntProperty())
                attrs = wm_custom_prop.ensure(obj)
                layout.prop(wm_custom_prop, attrs['a'])

            column = layout.column()

            # group.item_listの個々の要素に対しての処理
            for i, item in enumerate(group.item_list):
                row = column.box().row()

                # Draw CustomItem
                draw_item(row.column(), item)

                sub = row.row(align=True)

                identifier = str(id(item))

                # Register Up / Down
                def item_move_func(context, index_from, index_to, group=group):
                    item = group.item_list[index_from]
                    group.item_list[index_from: index_from + 1] = []
                    group.item_list.insert(index_to, item)
                OP.Move.register_function(
                    identifier, item_move_func)
                # Up
                op = sub.operator(OP.Move.bl_idname, text='',
                                  icon='TRIA_UP')
                op.function = identifier
                op.index_from = i
                op.index_to = max(0, i - 1)
                # Down
                op = sub.operator(OP.Move.bl_idname, text='',
                                  icon='TRIA_DOWN')
                op.function = identifier
                op.index_from = i
                op.index_to = min(i + 1, len(group.item_list) - 1)

                # Register Delete
                def item_remove_func(context, index, group=group):
                    group.item_list[index: index + 1] = []

                OP.Remove.register_function(
                    identifier, item_remove_func)
                # Delete
                op = sub.operator(OP.Remove.bl_idname, text='',
                                  icon='X')
                op.function = identifier
                op.index = i

            for attr in ['int_value', 'float_value', 'bool_value',
                         'int_array', 'float_array', 'bool_array',
                         'enum', 'enum_flag', 'enum_flag_func']:
                print("'{}': {}".format(attr, getattr(group, attr)))
            for i, item in enumerate(group.item_list):
                print("{}: 'a': {}".format(i, item.a))
            print()

    if hasattr(bpy.types, CustomPanel.__name__):
        bpy.utils.unregister_class(getattr(bpy.types, CustomPanel.__name__))
    bpy.utils.register_class(CustomPanel)


"""
NOTE: RNA_def_struct_idprops_func()でidproperに値を指定しているものがIDPropertyを持つ
% grep -rn RNA_def_struct_idprops_func
blender/makesrna/intern/rna_sequencer.c:1420:	RNA_def_struct_idprops_func(srna, "rna_Sequence_idprops");
blender/makesrna/intern/rna_constraint.c:899:	RNA_def_struct_idprops_func(srna, "rna_PythonConstraint_idprops");
blender/makesrna/intern/rna_nodetree.c:6889:	RNA_def_struct_idprops_func(srna, "rna_NodeSocket_idprops");
blender/makesrna/intern/rna_nodetree.c:7013:	RNA_def_struct_idprops_func(srna, "rna_NodeSocketInterface_idprops");
blender/makesrna/intern/rna_nodetree.c:7653:	RNA_def_struct_idprops_func(srna, "rna_Node_idprops");
blender/makesrna/intern/rna_define.c:936:void RNA_def_struct_idprops_func(StructRNA *srna, const char *idproperties)
blender/makesrna/intern/rna_ui.c:1041:	RNA_def_struct_idprops_func(srna, "rna_UIList_idprops");
blender/makesrna/intern/rna_pose.c:795:	RNA_def_struct_idprops_func(srna, "rna_PoseBone_idprops");
blender/makesrna/intern/rna_userdef.c:3262:	RNA_def_struct_idprops_func(srna, "rna_AddonPref_idprops");
blender/makesrna/intern/rna_ID.c:796:	RNA_def_struct_idprops_func(srna, "rna_PropertyGroup_idprops");
blender/makesrna/intern/rna_ID.c:933:	RNA_def_struct_idprops_func(srna, "rna_ID_idprops");
blender/makesrna/intern/rna_armature.c:715:	RNA_def_struct_idprops_func(srna, "rna_Bone_idprops");
blender/makesrna/intern/rna_armature.c:811:	RNA_def_struct_idprops_func(srna, "rna_EditBone_idprops");
blender/makesrna/intern/rna_wm.c:1556:	RNA_def_struct_idprops_func(srna, "rna_OperatorProperties_idprops");
blender/makesrna/RNA_define.h:62:void RNA_def_struct_idprops_func(StructRNA *srna, const char *refine);
"""
