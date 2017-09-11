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


import re
from collections import OrderedDict
import traceback

import bpy


def get_operator(string):
    m = re.match('(bpy\.ops\.)?(\w+)\.(\w+)(|\(.*\))$', string.rstrip())
    op = None
    if m:
        try:
            op = getattr(getattr(bpy.ops, m.group(2)), m.group(3))
        except:
            pass
    return op


def get_operator_arguments(string):
    """
    :param string:
        e.g.
          'bpy.ops.wm.splash', 'bpy.ops.wm.splash()'
          'wm.splash', "wm.splash('INVOKE_DEFAULT')"
    :return: (T, T)
    """
    m = re.match('(bpy\.ops\.)?(\w+)\.(\w+)(|\(.*\))$', string.rstrip())
    op = args = None
    if m:
        try:
            op = getattr(getattr(bpy.ops, m.group(2)), m.group(3))
            args = m.group(4)
            if not args:
                args = '()'
        except:
            pass

    if op and args:
        code = [
            'import inspect',
            'def func(*args, **kwargs):',
            '    pass',
            'sig = inspect.signature(func)',
            'ba = sig.bind({})'.format(args[1:-1]),
        ]
        d = {'bpy': bpy}
        try:
            exec('\n'.join(code), d)
        except:
            traceback.print_exc()
            return None, None
        ba = d['ba']

        # kwargsをソート
        kwargs = ba.kwargs
        rna_keys = list(op.get_rna().bl_rna.properties.keys())
        keys = sorted(kwargs.keys(), key=rna_keys.index)
        kwargs = OrderedDict([(key, kwargs[key]) for key in keys])

        return op, (ba.args, kwargs)
    else:
        return None, None


def format_execute_string(string, as_description=False, use_return=False):
    op, args_kwargs = get_operator_arguments(string)

    if op and args_kwargs:
        args, kwargs = args_kwargs
        op_context = 'INVOKE_DEFAULT'
        has_op_context = False
        op_undo = True
        for arg in args:
            if isinstance(arg, str):
                op_context = arg
                has_op_context = True
            elif isinstance(arg, bool):
                op_undo = arg
        ls_args = ["'" + op_context + "'", str(op_undo)]
        ls_kwargs = []
        for key, val in kwargs.items():
            if isinstance(val, str):
                ls_kwargs.append("{}='{}'".format(key, val))
            else:
                ls_kwargs.append('{}={}'.format(key, val))

        if as_description:
            if has_op_context:
                code = 'bpy.ops.{}({})'.format(
                    op.idname_py(), ', '.join([ls_args[0]] + ls_kwargs))
            else:
                code = 'bpy.ops.{}({})'.format(
                    op.idname_py(), ', '.join(ls_kwargs))
        else:
            code = 'bpy.ops.{}({})'.format(
                op.idname_py(), ', '.join(ls_args + ls_kwargs))
        if use_return:
            return 'return ' + code
        else:
            return code
    else:
        return string


def execute(string, kwargs, use_return=False):
    """文字列を実行してその結果を返す
    :param string: 実行する文字列。
    :type string: str
    :param kwargs: 関数に渡すキーワード引数。この関数では位置引数は使えない。
    :type kwargs: dict
    :param use_return: 真の場合、'bpy.ops.mod.func()'等の場合にその結果
        ({'FINISHED'} 等)を返すようにする。偽ならNoneを返す。
    :type use_return: bool
    """
    head = 'def func({}):\n'.format(', '.join(kwargs))
    execute_string = format_execute_string(string, use_return=use_return)
    lines = ['    ' + s for s in execute_string.split('\n')]
    d = {'bpy': bpy, 'context': bpy.context}
    try:
        exec(head + '\n'.join(lines), d)
    except:
        traceback.print_exc()
        return None
    func = d['func']
    try:
        return func(**kwargs)
    except:
        traceback.print_exc()
