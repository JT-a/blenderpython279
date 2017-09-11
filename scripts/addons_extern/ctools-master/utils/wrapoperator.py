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
import ctypes as ct

import bpy

from . import structures as st
from . import vaprops


def get_operator_type(idname_py):
    """wmOperatorTypeを返す
    :param idname_py: 'mod.func'
    :type idname_py: str
    :rtype: wmOperatorType
    """
    mod, func = idname_py.split('.')
    pyop = getattr(getattr(bpy.ops, mod), func)
    opinst = pyop.get_instance()
    pyrna = st.BPy_StructRNA.cast(id(opinst))
    op = st.wmOperator.cast(pyrna.ptr.data)
    return op.type.contents


def convert_ot_flag(ot):
    """wmOperatorType.flag(int)をbl_options用のsetに変換する
    :type ot: wmOperatorType
    :rtype: set
    """
    bl_options = set()
    table = {
        st.OPTYPE_REGISTER: 'REGISTER',
        st.OPTYPE_UNDO: 'UNDO',
        st.OPTYPE_BLOCKING: 'BLOCKING',
        st.OPTYPE_MACRO: 'MACRO',
        st.OPTYPE_GRAB_CURSOR: 'GRAB_CURSOR',
        st.OPTYPE_PRESET: 'PRESET',
        st.OPTYPE_INTERNAL: 'INTERNAL',
        # st.OPTYPE_LOCK_BYPASS = '',
    }
    flag = ot.flag
    for key, value in table.items():
        if flag & key:
            bl_options.add(value)
    return bl_options


def convert_return_flag(flag):
    """各関数の返り値(int)をsetに変換する
    :type flag: int
    :rtype: set
    """
    result = set()
    table = {
        st.OPERATOR_RUNNING_MODAL: 'RUNNING_MODAL',
        st.OPERATOR_CANCELLED: 'CANCELLED',
        st.OPERATOR_FINISHED: 'FINISHED',
        st.OPERATOR_PASS_THROUGH: 'PASS_THROUGH',
        # st.OPERATOR_HANDLED: '',
        st.OPERATOR_INTERFACE: 'INTERFACE',
    }
    for key, value in table.items():
        if flag & key:
            result.add(value)
    return result


def gen_execute(ot):
    if ot.exec:
        py_class = get_py_class(ot)
        if py_class:
            execute_ = py_class.execute
            def execute(self, context):
                result = execute_(self, context)
                return result
        else:
            def execute(self, context):
                result = ot.exec(context.as_pointer(), self.as_pointer())
                return convert_return_flag(result)
    else:
        execute = None
    return execute


def gen_check(ot):
    if ot.check:
        py_class = get_py_class(ot)
        if py_class:
            check_ = py_class.check
            def check(self, context):
                result = check_(self, context)
                return result
        else:
            def check(self, context):
                result = ot.check(context.as_pointer(), self.as_pointer())
                return result
    else:
        check = None
    return check


def gen_invoke(ot):
    if ot.invoke:
        py_class = get_py_class(ot)
        if py_class:
            invoke_ = py_class.invoke
            def invoke(self, context, event):
                result = invoke_(self, context, event)
                return result
        else:
            def invoke(self, context, event):
                result = ot.invoke(context.as_pointer(), self.as_pointer(),
                                   event.as_pointer())
                return convert_return_flag(result)
    else:
        invoke = None
    return invoke


def gen_modal(ot):
    if ot.modal:
        py_class = get_py_class(ot)
        if py_class:
            modal_ = py_class.modal
            def modal(self, context, event):
                result = modal_(self, context, event)
                return result
        else:
            def modal(self, context, event):
                result = ot.modal(context.as_pointer(), self.as_pointer(),
                                  event.as_pointer())
                return convert_return_flag(result)
    else:
        modal = None
    return modal


def gen_cancel(ot):
    if ot.cancel:
        py_class = get_py_class(ot)
        if py_class:
            cancel_ = py_class.cancel
            def cancel(self, context):
                result = cancel_(self, context)
                return result
        else:
            def cancel(self, context):
                ot.cancel(context.as_pointer(), self.as_pointer())
    else:
        cancel = None
    return cancel


def gen_poll(ot):
    """WM_operator_pollより"""
    if ot.pyop_poll:
        py_class = get_py_class(ot)
        poll_ = py_class.poll
        @classmethod
        def poll(cls, context):
            result = poll_(context)
            return result

    elif ot.poll:
        @classmethod
        def poll(cls, context):
            result = ot.poll(context.as_pointer())
            return bool(result)
    else:
        poll = None

    return poll


def gen_draw(ot):
    if ot.ui:
        py_class = get_py_class(ot)
        if py_class:
            draw_ = py_class.draw
            def draw(self, context):
                draw_(self, context)
        else:
            def draw(self, context):
                ot.ui(context.as_pointer(), self.as_pointer())
    else:
        draw = None
    return draw


def get_py_class(ot):
    """python/intern/bpy_rna.c: pyrna_register_class や
    makesrna/intern/rna_wm.c: rna_Operator_register 参照
    """
    if 1:  # どっちでも可
        if ot.ext.srna:
            srna = ot.ext.srna.contents
            return ct.cast(srna.py_type, ct.py_object).value
    else:
        if ot.ext.data:
            return ct.cast(ot.ext.data, ct.py_object).value
    return None


def convert_operator_attributes(idname_py):
    """クラス定義に必要なオペレーターの属性を作成してOrderedDictで返す。マクロは不可。
    :param idname_py: 'mod.func'
    :type idname_py: str
    :return: 属性の辞書。変換に失敗したプロパティーの値はNone。
    :rtype: dict[str, T | None]
    """
    mod, func = idname_py.split('.')
    pyop = getattr(getattr(bpy.ops, mod), func)
    bl_rna = pyop.get_rna().bl_rna

    ot = get_operator_type(idname_py)

    namespace = OrderedDict()

    # namespace['_operator_type'] = ot

    namespace['bl_idname'] = idname_py
    namespace['bl_label'] = bl_rna.name
    namespace['bl_description'] = bl_rna.description
    # ↓Debugビルドだとこれを指定していた場合にassertで落とされる。
    # namespace['bl_translation_context'] = bl_rna.translation_context
    namespace['bl_options'] = convert_ot_flag(ot)
    if ot.prop:
        namespace['bl_property'] = ot.prop.contents.identifier.decode()

    execute = gen_execute(ot)
    if execute:
        namespace['execute'] = execute

    check = gen_check(ot)
    if check:
        namespace['check'] = check

    invoke = gen_invoke(ot)
    if invoke:
        namespace['invoke'] = invoke

    modal = gen_modal(ot)
    if modal:
        namespace['modal'] = modal

    cancel = gen_cancel(ot)
    if cancel:
        namespace['cancel'] = cancel

    poll = gen_poll(ot)
    if poll:
        namespace['poll'] = poll

    draw = gen_draw(ot)
    if draw:
        namespace['draw'] = draw

    properties = vaprops.bl_props_to_py_props(bl_rna)
    namespace.update(properties)

    return namespace
