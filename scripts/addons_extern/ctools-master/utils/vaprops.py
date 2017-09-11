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


from collections import OrderedDict
import logging as _logging
import pickle as _pickle
import shelve as _shelve

import bpy as bpy


_logger = _logging.getLogger(__name__)
# logger.setLevel(_logging.ERROR)
_logger.setLevel(_logging.INFO)
_handler = _logging.StreamHandler()
_handler.setLevel(_logging.NOTSET)
_formatter = _logging.Formatter(
    '[%(levelname)s: %(name)s.%(funcName)s()]: %(message)s')
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)


INT_MIN = -2 ** (4 * 8 - 1)  # -2147483648
INT_MAX = 2 ** (4 * 8 - 1) - 1  # 2147483647
FLT_MIN = 1.175494e-38
FLT_MAX = 3.402823e+38
# DBL_MIN = 2.225074e-308
# DBL_MAX = 1.797693e+308


###############################################################################
# Convert Property
###############################################################################
def bl_prop_to_py_prop(prop, modify_enum=False):
    """bl_rnaのプロパティーをbpy.props.***()の返り値の形式に変換する
    :param prop: 例: bpy.types.Object.bl_rna.properties['type']
    :type prop: bpy.types.Property
    :param modify_enum: ENUMのitemsが空なら関数と見做し、StringPropertyに
        変更する
    :type modify_enum: bool
    :return: bpy.props.***()の返り値
    :rtype: (T, dict)
    """
    if prop.type == 'BOOLEAN':
        if prop.is_array:
            prop_type = bpy.props.BoolVectorProperty
        else:
            prop_type = bpy.props.BoolProperty
    elif prop.type == 'COLLECTION':
        prop_type = bpy.props.CollectionProperty
    elif prop.type == 'ENUM':
        prop_type = bpy.props.EnumProperty
    elif prop.type == 'FLOAT':
        if prop.is_array:
            prop_type = bpy.props.FloatVectorProperty
        else:
            prop_type = bpy.props.FloatProperty
    elif prop.type == 'INT':
        if prop.is_array:
            prop_type = bpy.props.IntVectorProperty
        else:
            prop_type = bpy.props.IntProperty
    elif prop.type == 'STRING':
        prop_type = bpy.props.StringProperty
    else:
        return None

    attrs = {
        "name": prop.name,
        "description": prop.description,
        # "icon": prop.icon,
    }
    if prop.type in {'BOOLEAN', 'FLOAT', 'INT'}:
        if prop.is_array:
            attrs["default"] = prop.default_array
            attrs["size"] = prop.array_length
        else:
            attrs["default"] = prop.default
    elif prop.type == 'ENUM':
        if prop.is_enum_flag:
            attrs["default"] = prop.default_flag
        else:
            attrs["default"] = prop.default
    elif prop.type == 'STRING':
        attrs["default"] = prop.default

    if prop.type in {'BOOLEAN', 'FLOAT', 'INT'}:
        subtype = prop.subtype
        if subtype == 'LAYER_MEMBERSHIP':
            subtype = 'LAYER_MEMBER'
        if prop.is_array:
            if subtype == 'UNSIGNED':  # Object.parent_vertices
                subtype = 'NONE'
        attrs["subtype"] = subtype
    elif prop.type == 'STRING':
        attrs["subtype"] = prop.subtype

    if prop.type == 'COLLECTION':
        if issubclass(prop.fixed_type.__class__, bpy.types.PropertyGroup):
            attrs["type"] = prop.fixed_type.__class__
        else:
            return None
    elif prop.type == 'ENUM':
        items = attrs["items"] = []
        for enum_item in prop.enum_items:
            items.append((enum_item.identifier,
                          enum_item.name,
                          enum_item.description,
                          enum_item.icon,
                          enum_item.value))
        if not items and modify_enum:
            prop_type = bpy.props.StringProperty
            if prop.is_enum_flag:
                attrs["default"] = str(attrs["default"])
            del attrs["items"]
    elif prop.type in {'INT', 'FLOAT'}:
        attrs["min"] = prop.hard_min
        attrs["max"] = prop.hard_max
        attrs["soft_min"] = prop.soft_min
        attrs["soft_max"] = prop.soft_max
        attrs["step"] = prop.step
        if prop.type == 'FLOAT':
            attrs["precision"] = prop.precision
            attrs["unit"] = prop.unit
    elif prop.type == 'STRING':
        attrs["maxlen"] = prop.length_max

    table = {
        "is_animatable": 'ANIMATABLE',
        "is_enum_flag": 'ENUM_FLAG',
        "is_hidden": 'HIDDEN',
        "is_library_editable": 'LIBRARY_EDITABLE',
        "is_skip_save": 'SKIP_SAVE',
        # "": 'PROPORTIONAL',
        # "": 'TEXTEDIT_UPDATE',
    }
    options = attrs["options"] = set()
    for key, value in table.items():
        if getattr(prop, key):
            options.add(value)

    return prop_type(**attrs)


def bl_props_to_py_props(bl_rna, modify_enum=False):
    """bl_rnaの全てのプロパティーをbpy.props.***()の返り値の形式に変換して
    OrderedDictで返す。変換に失敗したプロパティーの値はNoneになる。
    :type bl_rna: T
    :param modify_enum: ENUMのitemsが空なら関数と見做し、StringPropertyに
        変更する
    :type modify_enum: bool
    :return: OrderedDict
    :rtype: dict[str, T | None]
    """
    properties = OrderedDict()
    for name, prop in bl_rna.properties.items():
        if name == "rna_type":
            continue
        properties[name] = bl_prop_to_py_prop(prop, modify_enum)
    return properties


###############################################################################
# bpy_struct <-> dict
###############################################################################
ADDRESS = '_ADDRESS'
ID_PROPERTY = '_ID_PROPERTY'
NAMESPACE = '__dict__'

_converted_props = {}


# bpy_struct -> dict ----------------------------------------------------------
def _dump_namespace(obj, r_dict):
    """__dict__属性。pickle化可能な物のみ追加する"""
    if not hasattr(obj, '__dict__'):
        return

    r_dict[NAMESPACE] = dic = {}
    for k, v in obj.__dict__.items():
        try:
            _pickle.dumps(v)
        except _pickle.PicklingError as e:
            _logger.warning(str(e))
            continue
        dic[k] = v
    return dic


def _dump_id_property(obj, r_dict):
    """IDProperty
    Only bpy.types.ID, bpy.types.Bone and bpy.types.PoseBone classes support
    custom properties.
    ↑ PropertyGroup も
    """
    try:
        obj.keys()
    except TypeError:
        # 'bpy_struct.keys(): this type doesn't support IDProperties'
        return

    bl_rna = obj.bl_rna
    keys = list(bl_rna.properties.keys())
    r_dict[ID_PROPERTY] = dic = {}
    for key in obj.keys():
        if key not in keys:
            id_prop = obj[key]
            if not isinstance(id_prop, (int, float, str)):  # boolはint扱い
                cls_name = id_prop.__class__.__name__
                if cls_name == 'IDPropertyArray':
                    id_prop = id_prop.to_list()
                elif cls_name == 'IDPropertyGroup':
                    id_prop = id_prop.to_dict()
            dic[key] = id_prop
    return dic


def _dump_pointer(obj, attr, r_dict):
    bl_rna = obj.bl_rna
    prop = bl_rna.properties[attr]
    prop_obj = getattr(obj, attr)

    if prop_obj is None:
        r_dict[attr] = (prop.type, None, prop.fixed_type.identifier)
        return

    elif prop_obj in _converted_props:
        address = prop_obj.as_pointer()
        r_dict[attr] = _converted_props[address]
        return

    address = prop_obj.as_pointer()
    dic = {ADDRESS: address}
    prop_data = (prop.type, dic, prop.fixed_type.__class__.__name__)
    r_dict[attr] = _converted_props[address] = prop_data

    _dump(prop_obj, None, dic)

    return prop_data


def _dump_collection(obj, attr, r_dict):
    bl_rna = obj.bl_rna
    prop = bl_rna.properties[attr]

    ls = []
    prop_data = (prop.type, ls, prop.fixed_type.__class__.__name__)
    r_dict[attr] = prop_data

    for elem in getattr(obj, attr):
        if elem is None:
            ls.append(None)
        else:
            address = elem.as_pointer()
            if address in _converted_props:
                ls.append(_converted_props[address])
            else:
                dic = {ADDRESS: address}
                ls.append(dic)
                _converted_props[address] = dic
                _dump(elem, None, dic)

    return prop_data


def _dump(obj, attr=None, r_dict=None):
    # NOTE: bl_rna.name == bl_label
    #       bl_rna.identifier == bl_idname == bpy.typesでの属性名
    #
    #       bl_rna.__class__ == bpy.types.Hoge
    #       bl_rna == bpy.types.Hoge.bl_rna

    if r_dict is None:
        r_dict = {}
    # if not obj or not hasattr(obj, 'bl_rna'):
    #     return r_dict
    if not issubclass(obj.__class__, bpy.types.ID.__base__):  # <bpy_struct>
        return r_dict

    bl_rna = obj.bl_rna

    if attr is None:
        _dump(obj, NAMESPACE, r_dict)
        _dump(obj, ID_PROPERTY, r_dict)
        for key in bl_rna.properties.keys():
            if key != 'rna_type':
                _dump(obj, key, r_dict)
        return r_dict

    elif attr == ID_PROPERTY:
        _dump_id_property(obj, r_dict)
        return r_dict

    elif attr == NAMESPACE:
        _dump_namespace(obj, r_dict)
        return r_dict

    # # bug: segmentation fault
    # if isinstance(obj, bpy.types.ParticleEdit):
    #     if attr in ('is_editable', 'is_hair', 'object'):
    #         return r_dict

    prop = bl_rna.properties[attr]
    prop_obj = getattr(obj, attr)

    if prop.type == 'POINTER':
        _dump_pointer(obj, attr, r_dict)

    elif prop.type == 'COLLECTION':
        _dump_collection(obj, attr, r_dict)

    elif prop.type in ('BOOLEAN', 'ENUM', 'FLOAT', 'INT', 'STRING'):
        if hasattr(prop, 'array_length') and prop.array_length > 0:
            if prop.subtype == 'MATRIX':
                r_dict[attr] = (prop.type, [list(x) for x in prop_obj])
            else:
                r_dict[attr] = (prop.type, list(prop_obj))
        else:
            if isinstance(prop_obj, set):  # ENUM: options={'ENUM_FLAG', ...}
                r_dict[attr] = (prop.type, set(prop_obj))
            else:
                r_dict[attr] = (prop.type, prop_obj)

    return r_dict


def dump(obj, attr=None):
    """PropertyGroupを再帰的に辿って辞書に変換する。bpy_structに対しても可。
    ('BOOLEAN', True) or ('BOOLEAN', [True, False, ...])
    ('INT', 1) or ('INT', [0, 1, ...])
    ('FLOAT', 1.0) or ('FLOAT', [0.0, 1.0, ...])
    ('ENUM', 'A') or ('ENUM', {'A', 'B', ...})
    ('STRING', 'abc')
    ('POINTER', {}, type_identifier)
    ('COLLECTION', [{}, ...], type_identifier)
    :type obj: PropertyGroup | bpy_struct
    :param attr: 対象の属性。Noneで全ての属性を辿る。NAMESPACEで__dict__属性、
        ID_PROPERTYではIDPropertyを取得する。
    :type attr: list | tuple | str
    :rtype: dict
    """
    _converted_props.clear()
    if attr is None:
        return _dump(obj)
    elif not attr:
        return {}
    else:
        if isinstance(attr, str):
            return _dump(obj, attr)[attr]
        else:
            dic = {}
            for a in attr:
                _dump(obj, a, dic)
            return dic


# dict -> bpy_struct ----------------------------------------------------------
def _undump_namespace(prop_data, obj):
    try:
        obj.__dict__.clear()
        obj.__dict__.update(prop_data)
    except Exception as err:
        _logger.error(str(err))


def _undump_id_property(prop_data, obj):
    try:
        obj.keys()
    except TypeError as err:
        _logger.error(str(err))
        return

    for k in list(obj.keys()):
        del obj[k]
    for k, v in prop_data.items():
        try:
            obj[k] = v
        except Exception as err:
            _logger.error(str(err))


def _undump_pointer(prop_data, obj, attr):
    # prop_dataはgetattr(obj, attr)のもの
    prop = obj.bl_rna.properties.get(attr)

    if prop_data[0] != 'POINTER':
        _logger.error("'{}.{} is 'POINTER' property, not '{}'".format(
            str(type(obj)), attr, prop_data[0]))

    _type, dic, _class_name = prop_data

    if dic is None:
        try:
            setattr(obj, attr, None)
        except Exception as err:
            _logger.error(str(err))

    elif not dic:
        pass

    elif issubclass(prop.fixed_type.__class__, bpy.types.PropertyGroup):
        prop_obj = getattr(obj, attr)
        _undump(dic, prop_obj)

    elif (dic.get(ADDRESS) not in _converted_props and
          str(id(dic)) not in _converted_props):
        if ADDRESS in dic:
            _converted_props[dic[ADDRESS]] = True
        else:
            msg = "'{}' not in {}.{} property data".format(
                ADDRESS, str(type(obj)), attr)
            _logger.warning(msg)
        _converted_props[str(id(dic))] = True

        if prop.is_readonly:
            _undump(dic, getattr(obj, attr))
        else:
            # bpy.dataの中から探す
            # NOTE: bpy.data: rna_type, filepath, is_dirty, is_saved,
            #       use_autopack, version 以外は全てIDのサブクラス
            for attr_, prop_ in bpy.data.bl_rna.properties.items():
                if (prop_.type == 'POINTER' and
                        prop_.fixed_type == prop.fixed_type):
                    if 'name' in dic:
                        ob_name = dic['name']
                        prop_obj = getattr(bpy.data, attr_)[ob_name]
                        try:
                            setattr(obj, attr, prop_obj)
                        except Exception as err:  # 例外はあり得るか？
                            _logger.error(str(err))
                    else:
                        msg = "'name' not in {}.{} property data".format(
                            str(type(obj)), attr)
                        _logger.warning(msg)
                        prop_obj = getattr(obj, attr)
                    _undump(dic, prop_obj)

                    break
            else:
                _undump(dic, getattr(obj, attr))


def _undump_collection(prop_data, obj, attr):
    if prop_data[0] != 'COLLECTION':
        _logger.error("'{}.{} is 'COLLECTION' property, not '{}'".format(
            str(type(obj)), attr, prop_data[0]))

    _type, ls, _class_name = prop_data

    prop = obj.bl_rna.properties.get(attr)
    # if hasattr(prop_obj, 'clear') and hasattr(prop_obj, 'add'):
    if issubclass(prop.fixed_type.__class__, bpy.types.PropertyGroup):
        collection = getattr(obj, attr)
        collection.clear()
        for dic in ls:
            elem = collection.add()
            _undump(dic, elem)
    else:
        # TODO: Object.material_slots, Scene.objects等々
        pass


def _undump(prop_dict, obj):
    if obj is None:
        return

    for attr, prop_data in sorted(prop_dict.items(), key=lambda x: x[0]):
        if attr == ADDRESS:
            continue

        if attr == NAMESPACE:
            _undump_namespace(prop_data, obj)
            continue

        if attr == ID_PROPERTY:
            _undump_id_property(prop_data, obj)
            continue

        prop = obj.bl_rna.properties.get(attr)

        if not prop:
            _logger.error("{} has no property '{}'".format(obj, attr))
            continue

        if prop.type == 'POINTER':
            _undump_pointer(prop_data, obj, attr)

        elif prop.type == 'COLLECTION':
            _undump_collection(prop_data, obj, attr)

        elif not prop.is_readonly:
            # is_readonlyが偽でも実行時に
            # bpy_prop "***" is read-only と出る場合がある
            t, val = prop_data
            try:
                if hasattr(prop, 'array_length') and prop.array_length > 0:
                    # matrix_world等は、スライスを使わないと勝手に値を
                    # 修正してしまう
                    getattr(obj, attr)[:] = val
                else:
                    setattr(obj, attr, val)
            except Exception as err:
                _logger.error(str(err))


def undump(prop_dict, obj):
    """dump()で得た辞書でPropertyGroupを更新する。
    一応はbpy_structに対しても有効だが、COLLECTIONプロパティは非対応。
    適用する必要の無い不要なPOINTERプロパティは削除又は修正しておくこと。
    e.g.)
    Object.active_materialを変更したいが、そのMaterialの属性については変更を
    加えたくない場合は、ADDRESSと'name'を残して消す。
    ADDRESSは変更済みのオブジェクトを記録しておいて同オブジェクトに対して
    複数回変更を加えないようにする為のものなので必須ではない。
    {'active_material':
          ('POINTER',
           {ADDRESS: 140195969897480, 'name': 'Material.001'},
           'Material'),
     ...
    }
    :type prop_dict: dict
    :type obj: PropertyGroup | bpy_struct
    """
    _converted_props.clear()
    _undump(prop_dict, obj)


###############################################################################
# save / load
###############################################################################
def save(file_path, prop_obj, include=None, exclude=None, clear=True):
    """
    :type file_path: str
    :type prop_obj: dict | object
    :type include: dict
    :type exclude: list | tuple
    :type clear: bool
    """
    if isinstance(prop_obj, dict):
        d = prop_obj
    else:
        d = dump(prop_obj)
    if include:
        if isinstance(prop_obj, dict):
            d = dict(d)
        d.update(include)
    if exclude:
        for key in exclude:
            if key in d:
                del d[key]
    try:
        shelf = _shelve.open(file_path)
    except Exception as err:
        _logger.error(str(err))
        return False
    if clear:
        shelf.clear()
    shelf.update(d)
    shelf.close()
    _logger.info("saved to '{}'".format(file_path))
    return True


def load(file_path, prop_obj, include=None, exclude=None):
    """
    :type file_path: str
    :type prop_obj: dict | object
    :type include: dict
    :type exclude: list | tuple
    """
    try:
        shelf = _shelve.open(file_path)
    except Exception as err:
        _logger.error(str(err))
        return False
    d = dict(shelf)
    shelf.close()
    if include:
        d.update(include)
    if exclude:
        for key in exclude:
            if key in d:
                del d[key]
    if isinstance(prop_obj, dict):
        prop_obj.update(d)
    else:
        undump(d, prop_obj)
    _logger.info("loaded from '{}'".format(file_path))
    return True


"""
NOTE:

属性一覧:
PointerProperty:
    as_pointer(), bl_rna, driver_add(), driver_remove(), get(), id_data,
    is_property_hidden(), is_property_set(), items(), keyframe_delete(),
    keyframe_insert(), keys(), name, path_from_id(), path_resolve(),
    property_unset(), rna_type, type_recast(), values()
    dir: ['__dict__', '__doc__', '__module__', '__weakref__', 'bl_rna', 'name',
          'rna_type']
CollectionProperty:
    add(), as_bytes(), clear(), data, find(), foreach_get(), foreach_set(),
    get(), id_data, items(), keys(), move(), path_from_id(), remove(),
    rna_type(), values()
    dir: ['__doc__', 'add', 'clear', 'move', 'remove']


PyObject *obj;
if (BPy_StructRNA_Check(obj)) {  # bpy_rna.h
    BPy_StructRNA *py_srna = (BPy_StructRNA *)obj;
    PointerRNA *ptr = &py_srna->ptr;
    StructRNA *srna = ptr->data;
    if (RNA_struct_is_a(ptr->type, &RNA_Object)) {
        Object *ob = ptr->data;
        ...
    }
    if (RNA_struct_is_ID(ptr->type)) {
        ID *id = ptr->id.data;
        ...
    }
}

/* since this is least common case, handle it last */
if (BPy_PropertyRNA_Check(self)) {
    BPy_PropertyRNA *self_prop = (BPy_PropertyRNA *)self;
    if (RNA_property_type(self_prop->prop) == PROP_COLLECTION) {
"""


def idprop_to_py(prop):
    if isinstance(prop, list):
        return [idprop_to_py(p) for p in prop]
    elif hasattr(prop, 'to_dict'):
        return prop.to_dict()
    elif hasattr(prop, 'to_list'):
        return prop.to_list()
    else:
        return prop
