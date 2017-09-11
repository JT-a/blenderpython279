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


import math

import string

import bpy
import bgl
import blf
from mathutils import Euler, Matrix, Quaternion, Vector
import mathutils.geometry as geom

from . import vamath as vam
from . import vaview3d as vav
from . import vagl as vagl
from . import manipulatormatrix
from . import unitsystem

from ..localutils.utils import xproperty


#==============================================================================
# InputExpression
#==============================================================================
class InputExpression(list):
    """
    in Operator.invoke
        self.ie = InputExpression3(["Dist", "X", "Y", "Z"])
    in Operator.modal
        retval = self.ie.modal(event)
        if retval.intersect('RUNNING_MODAL', 'FINISHED'):
            Operator.execute(context)
    in Operator.draw_callback
       self.ie.draw()
    
    input start:     press digits or poriod, Tab, Shift + Tab
    input start/end: {Ctrl, Alt, OSKey} + Tab
    finish:          Return, KP_Enter, button1
    cancel:          Escape, button3
    delete char:     BackSpace, Delete
    clear frame:     Ctrl + x
    clear all frame: Ctrl + Shift + x
    move cursor:     Up, Down, Left, Right, Home, End
    next frame:      Tab
    prev frame:      Shift + Tab
    
    self[index]: Get strings. e.g. "math.pi * 2"
    self(index): Get int or float generated eval().
                 If index is None(default), get list of all.
                 e.g. 6.283185307179586 (self[0] == "math.pi * 2")
    """

    def __init__(self, names=("Dist",),
                 unit_system=None,
                 font_id=0,
                 font_size=None,
                 color=(1.0, 1.0, 1.0, 1.0),
                 error_color=(1.0, 0.6, 0.5, 1.0),
                 draw_precisions={'default':".6f"}):
        """
        draw_precisions: self.activeが偽で、
        　　　　　　　　　文字列がそのままfloatに変換が可能な場合の
        　　　　　　　　　描画の精度を指定する。
                         'default'は初期値。
                         必要な分だけインデックス(int)をキーとして追加する。
        """
        self[:] = ["" for _ in range(len(names))]
        self.names = list(names)
        self.cursor = [0, 0]
        self.active = False
        self.unit_system = unit_system
        self.font_id = font_id
        self.font_size = font_size
        self.color = color
        self.error_color = error_color
        self.draw_precisions = draw_precisions


    def __call__(self, index=None, fallback=None):
        """
        self.active is Falseでもself.exp_stringsを計算して値を返す
        """
        if self.unit_system:
            if index is None:
                # return [self.unit_system.str_to_num(self[i], fallback)
                #         for i in range(len(self))]
                return [self.unit_system.unit_to_num(self[i],
                                                     fallback=fallback)
                        for i in range(len(self))]
            else:
                # return self.unit_system.str_to_num(self[index], fallback)
                return self.unit_system.unit_to_num(
                    self[index], fallback=fallback)
        else:
            if index is None:
                return [self._get_exp_value(i, fallback)
                        for i in range(len(self))]
            else:
                return self._get_exp_value(index, fallback)


    def _get_exp_value(self, index=0, fallback=None):
        if self[index]:
            try:
                value = eval(self[index])
            except:
                return fallback
            if isinstance(value, (int, float)):
                return float(value)
        return fallback


    def set_length(self, length):
        if length > len(self):
            n = length - len(self)
            self.extend([""] * n)
            self.names.extend([""] * n)
        elif length < len(self):
            self[:] = self[:length]
            self.names[:] = self.names[:length]
            if self.cursor[0] > length - 1:
                self.cursor[0] = length - 1
                self.cursor[1] = len(self[self.cursor[0]])


    def modal(self, event):
        """
        -> enum set in {'RUNNING_MODAL', 'CANCELLED', 'FINISHED',
                        'PASS_THROUGH'}
        """
        cursor = self.cursor
        exp_str = self[cursor[0]]

        event_move_cursor = {'LEFT_ARROW':-1, 'RIGHT_ARROW': 1,
                             'UP_ARROW':-999, 'DOWN_ARROW': 999,
                             'HOME':-999, 'END': 999}

        retval = {'PASS_THROUGH'}

        if event.value != 'PRESS':
            return retval

        if event.type in ('ESC', 'RIGHTMOUSE'):
            self.active = False
            retval = {'CANCELLED'}

        elif event.type in ('LEFTMOUSE', 'RET', 'NUMPAD_ENTER'):
            self.active = False
            retval = {'FINISHED'}

        elif self.active:
            if event.type in('TAB'):
                if len(self) == 1:
                    self.active = not self.active
                    retval = {'RUNNING_MODAL'}
                elif event.ctrl or event.alt or event.oskey:
                    self.active = False
                    # retval = {'FINISHED', 'RUNNING_MODAL'}
                    retval = {'RUNNING_MODAL'}
                else:
                    if event.shift:
                        cursor[0] -= 1
                        if cursor[0] < 0:
                            cursor[0] = len(self) - 1
                    else:
                        cursor[0] += 1
                        if cursor[0] > len(self) - 1:
                            cursor[0] = 0
                    cursor[1] = len(self[cursor[0]])
                    retval = {'RUNNING_MODAL'}

            elif event.type in event_move_cursor:
                cursor[1] += event_move_cursor[event.type]
                cursor[1] = min(max(cursor[1], 0), len(exp_str))
                retval = {'RUNNING_MODAL'}

            elif event.type == 'X' and event.ctrl:
                if event.shift:
                    cursor[:] = [0, 0]
                    for i in range(len(self)):
                        self[i] = ""
                else:
                    cursor[1] = 0
                    self[cursor[0]] = ""
                retval = {'RUNNING_MODAL'}

            elif event.type == 'BACK_SPACE':
                exp = exp_str[:max(0, cursor[1] - 1)] + exp_str[cursor[1]:]
                self[cursor[0]] = exp
                cursor[1] = max(0, cursor[1] - 1)
                retval = {'RUNNING_MODAL'}

            elif event.type == 'DEL':
                exp = exp_str[:cursor[1]] + exp_str[cursor[1] + 1:]
                self[cursor[0]] = exp
                retval = {'RUNNING_MODAL'}

            elif event.ascii:  # ソースのバグ潰しが必要。現在は修正済み？
                exp = exp_str[:cursor[1]] + event.ascii + exp_str[cursor[1]:]
                self[cursor[0]] = exp
                cursor[1] += 1
                retval = {'RUNNING_MODAL'}

        else:
            if event.type == 'SPACE':
                self.active = False
                retval = {'FINISHED'}

            elif event.ascii and event.ascii in "0123456789.":
                self[cursor[0]] = event.ascii
                cursor[1] = 1
                self.active = True
                retval = {'RUNNING_MODAL'}

            # elif event.type == 'TAB' and \
            #     (event.ctrl or event.alt or event.oskey):
            elif event.type == 'TAB':
                cursor[1] = len(self[cursor[0]])
                self.active = True
                retval = {'RUNNING_MODAL'}

        return retval

    def draw(self, context, ofsx, ofsy):
        """返り値は描画したテキストの終端
        None: 初期化時の値を使う
        """
        text_width_min = 40
        pertition = ',  '

        font_id = self.font_id
        font_size = self.font_size
        color = self.color
        error_color = self.error_color
        precisions = self.draw_precisions

        glcolor = vagl.Buffer('float', 4, bgl.GL_CURRENT_COLOR)
        if self.font_size is not None:
            dpi = context.user_preferences.system.dpi
            blf.size(font_id, font_size, dpi)

        ofsx_bak = ofsx
        _, text_height = blf.dimensions(font_id, string.printable)

        for i, exp_string in enumerate(self):
            # value = self(i)
            if self.unit_system:
                # value = self.unit_system.str_to_num(exp_string, None)
                value = self.unit_system.unit_to_num(exp_string)
            else:
                # value = UnitSystem.string_to_numeric(exp_string, 1.0, 'NONE')
                value = None
            if value is None:
                bgl.glColor4f(*error_color)
            else:
                bgl.glColor4f(*color)

            # 書式化
            try:
                float(exp_string)
                is_float = True
            except ValueError:
                is_float = False
            if is_float:
                if self.active:
                    text = exp_string
                else:
                    fmt = precisions.get(i, precisions['default'])
                    text = "{0:{1}}".format(value, fmt)
            else:
                if value is None:
                    text = exp_string
                else:
                    text = "{0} ({1:.6f})".format(exp_string, value)

            # 先頭に名前追加
            if self.names[i]:
                head = self.names[i] + ": "
            else:
                head = ""
            text = head + text

            # 区切り文字追加
            if len(self) > 1 and 0 <= i < len(self) - 1:
                text = text + pertition

            # 描画
            blf.position(font_id, ofsx, ofsy, 0)
            vagl.blf_draw(font_id, text)
            text_width, _ = blf.dimensions(font_id, text)
            text_width = max(text_width_min, text_width)

            # cursor描画
            if self.active and i == self.cursor[0]:
                bgl.glColor4f(*color)
                t = head + exp_string[:self.cursor[1]]
                t_width, _ = blf.dimensions(font_id, t)
                x = ofsx + t_width
                bgl.glRectf(x - 1, ofsy - 4, x + 1, ofsy + 14)

            ofsx += text_width

            if ofsx > context.region.width and i < len(self) - 1:
                ofsx = ofsx_bak
                ofsy += text_height

        bgl.glColor4f(*glcolor)

        return ofsx, ofsy


#==============================================================================
# ModalMouse
#==============================================================================
class ModalMouse:
    """
    オペレータのmodalメソッドの中でマウスの移動量からdistanceなどの数値を得る。
    使用法:
        基本的に、オペレータ毎にこれを継承したクラスを作る。
        オペレータのinvokeメソッドでインスタンスを生成。
        modal中でmodal()を実行。
    各要素:
        current: Vector (region coordinates)
                 現在のマウス座標 (event.mouse_region_x, event.mouse_region_y)
        origin: Vector (region coordinates)
                インスタンス生成時のマウス座標。後で変更可能。
        relative: Vecto (region coordinates)r
                  originからの相対座標。shiftとlockの補正を受けている。
        shift: Vector or None (region coordinates)
               shiftキーが押されたマウス座標を格納。これ以降の移動量は10分の1の値で反映される。
        lock: Vector or None (region coordinates)
              中クリックの際のマウス座標を格納。
              relativeの方向を制限して、distanceで負の値を有効にする。
        snap: bool
              ctrlキーを押しているか。真ならdistanceとfactorの値をスナップ。
        distance: float
                  各要素から算出した最終的な移動量(BlenderUnit)。
        factor: float
                各要素から算出した最終的な値(0.0-1.0を基本とする値)。
        master: クラスインスタンス。
                実行中のオペレータ。self。
        callback: 関数。 callback(context)。
            modal()中で実行する。目的はオペレータの要素をdistance等で変更する事。
    算出方法:
        origin, current, shiftからrelativeを求める。
        lockが有効なら、relativeを(origin -> lock)のベクトルに正射影する。
        ctrlキーを押しているならrelativeをスナップする。
    """

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'


    # properties --------------------------------------------------------------
    # 参照の度に新規リストを返す
    CONSTX = xproperty(lambda self: [True, False, False])
    CONSTY = xproperty(lambda self: [False, True, False])
    CONSTZ = xproperty(lambda self: [False, False, True])
    CONSTXY = xproperty(lambda self: [True, True, False])
    CONSTXZ = xproperty(lambda self: [True, False, True])
    CONSTYZ = xproperty(lambda self: [False, True, True])
    CONSTALL = xproperty(lambda self: [True, True, True])
    CONSTNONE = xproperty(lambda self: [False, False, False])

    ANGLE_LIMIT = math.radians(5.0)

    def _exp_get(self):
        if self.mode == 'DISTANCE':
            return self.exp_distance
        elif self.mode == 'FACTOR':
            return self.exp_factor
        elif self.mode == 'TRANSLATION':
            return self.exp_translation
        elif self.mode == 'ROTATION':
            return self.exp_rotation
        elif self.mode == 'RESIZE':
            return self.exp_resize
        elif self.mode == 'TRACKBALL':
            return self.exp_trackball
        else:
            return self.exp_default
    exp = xproperty(_exp_get)


    def get_region_header(self, context):
        """現在のAreaのHeaderタイプのRegionを返す"""
        for region in context.area.regions:
            if region.type == 'HEADER':
                return region
        return None

    # key: name, value: exec string
    callback_exec_strings = {
        'value':
            'try:                                               \n' \
            '    master.value = self.value                      \n' \
            'except:                                            \n' \
            '    if isinstance(self.value, (int, float)):       \n' \
            '        master.value[0] = self.value               \n' \
            '    else:                                          \n' \
            '        master.value[:len(self.value)] = self.value',
        'mode':
            'master.mode = self.mode',
        'distance':
            'master.distance = self.distance',
        'factor':
            'master.factor = self.factor',
        'translation':
            'master.translation = self.translation',
        'rotation':
            'master.rotation = self.rotation \n' \
            'master.rotation_axis = self.rotation_axis \n' \
            'master.rotation_angle = self.rotation_angle',
        'resize':
            'master.resize = self.resize',
        'trackball':
            'master.trackball = self.trackball \n' \
            'master.trackball_x = self.trackball_x \n' \
            'master.trackball_y = self.trackball_y',
        'orientation':
            'master.orientation = self.manipulator_matrix.orientation',
        'orientation_matrix':
            'mmat = self.manipulator_matrix                     \n' \
            'try:                                               \n' \
            '    master.orientation_matrix = mmat               \n' \
            'except:                                            \n' \
            '    arr = list(chain(*[c for c in mmat.col]))      \n' \
            '    try:                                           \n' \
            '        master.orientation_matrix = arr            \n' \
            '    except:                                        \n' \
            '        mmat3 = mmat.to_3x3()                      \n' \
            '        arr = list(chain(*[c for c in mmat3.col])) \n' \
            '        master.orientation_matrix = arr',
        'use_current_orientation':
            'master.use_current_orientation = self.use_current_orientation',
        'use_local_coords':
            'master.use_local_coords = ' \
            '    not self.use_normalized_orientation and ' \
            '    self.manipulator_matrix.orientation == "LOCAL"',
        'axis':
            'master.constraint_axis = self.axis',
    }

    mode = 'NONE'  # 開始時のモード
    modes = ('DISTANCE', 'FACTOR',
             'TRANSLATION', 'ROTATION', 'RESIZE', 'TRACKBALL')
    if mode not in modes:
        modes = modes + (mode,)

    shortcuts = {'lock': 'MIDDLEMOUSE',
                 'reset': 'O',
                 'distance': 'D',
                 'factor': 'F',
                 'translation': 'G',
                 'rotation': 'R',
                 'resize': 'S',
                 'axis': 'MIDDLEMOUSE',
                 'x': 'X',
                 'y': 'Y',
                 'z': 'Z'}

    ignore_keys = set()  # 無視するキー

    exp_args = {'NONE': {'names': ('Value',)},
                'DISTANCE': {'names': ('Dist',)},
                'FACTOR': {'names': ('Fac',)},
                'TRANSLATION': {'names': ('Dx', 'Dy', 'Dz')},
                'ROTATION': {'names': ('Rot', 'X', 'Y', 'Z'),
                             'draw_precisions': {'default': '.6f', 0: '.2f'}},
                'RESIZE': {'names': ('Scale X', 'Y', 'Z')},
                'TRACKBALL': {'names': ('Tracxball X', 'Y'),
                              'draw_precisions': {'default': '.2f'}}}
    dpf = 200

    # 描画させたくない場合は除く
    draw_items = {'origin', 'relative', 'lock', 'factor'}

    def __init__(self, context, event, master,
                 view_location=None,
                 use_normalized_orientation=True):
        """
        master: Operator
        view_location:
            perspectiveViewの場合に使う、数値の基準となるworld座標
        use_normalized_orientation:
            self.orientationを正規化する。
            これが実際に影響を受けるのはDISTANCEとTRANSLATIONのみ。
            実質的にLOCALでのみ有効
        """
        # 引数の処理 ----------------------------------------------------------
        self.context = context
        self.event = event
        self.master = master
        self.view_location = view_location
        self.use_normalized_orientation = use_normalized_orientation

        # UnitSystem ----------------------------------------------------------
        self.unit_system = unitsystem.UnitSystem(
            context, {'view_location': view_location})

        # InputExpression -----------------------------------------------------
        self.exp_default = InputExpression(unit_system=self.unit_system,
                                           **self.exp_args['NONE'])
        self.exp_distance = InputExpression(unit_system=self.unit_system,
                                            **self.exp_args['DISTANCE'])
        self.exp_factor = InputExpression(unit_system=self.unit_system,
                                          **self.exp_args['FACTOR'])
        self.exp_translation = InputExpression(unit_system=self.unit_system,
                                               **self.exp_args['TRANSLATION'])
        self.exp_rotation = InputExpression(unit_system=self.unit_system,
                                            **self.exp_args['ROTATION'])
        self.exp_resize = InputExpression(unit_system=self.unit_system,
                                          **self.exp_args['RESIZE'])
        self.exp_trackball = InputExpression(unit_system=self.unit_system,
                                             **self.exp_args['TRACKBALL'])

        # Manipulator Matrix --------------------------------------------------
        self.manipulator_matrix = manipulatormatrix.ManipulatorMatrix(
            context, default_location=context.space_data.cursor_location,
            use_normalized=use_normalized_orientation)
        self.use_current_orientation = False  # False: Global, True: manipul
        self.axis = self.CONSTNONE  # 全て真 == 全て偽

        # Vector --------------------------------------------------------------
        self.mco = Vector((event.mouse_region_x, event.mouse_region_y))
        self.origin = self.mco.copy()
        self.relative = Vector((0, 0))
        self.relative_draw = self.relative.copy()  # 描画用
        self.shift = None  # Vector (2D)  (precision mode)
        self.lock = None  # Vector (2D)
        self.snap = False
        self.middlemouse = None  # Vector (2D)
        self.locked_when_middlemouse = False  # MiddleMouseを押した時、既にLock

        # 計算結果の格納 -------------------------------------------------------
        self.value = 0.0
        self.distance = 0.0
        self.factor = 0.0
        self.translation = Vector((0, 0, 0))
        self.rotation = Quaternion()
        self.rotation_axis = Vector((0, 0, 1))
        self.rotation_angle = 0.0
        self.resize = Vector((0, 0, 0))
        self.trackball = Quaternion()
        self.trackball_x = 0.0  # 描画に必要
        self.trackball_y = 0.0  # 描画に必要

        self.callback_exec_strings = dict(self.callback_exec_strings)
        self.draw_items = set(self.draw_items)

        self.update(context, event)

        # Callback, Draw Handler ----------"-----------------------------------
        context.window_manager.modal_handler_add(master)
        self.region_id = context.region.id
        self.draw_handler_add(context)


    def draw_handler_add(self, context):
        v3d = context.space_data
        self._handle = v3d.draw_handler_add(self.draw, (context,),
                                            'WINDOW', 'POST_PIXEL')
        header_region = self.get_region_header(context)
        if header_region:
            self.header_region_id = header_region.id
            self._header_handle = v3d.draw_handler_add(
                                    self.draw_header, (context,),
                                    'HEADER', 'POST_PIXEL')
        else:
            self.header_region_id = -1
            self._header_handle = None


    def draw_handler_remove(self, context):
        v3d = context.space_data
        v3d.draw_handler_remove(self._handle, 'WINDOW')
        if self._header_handle:
            v3d.draw_handler_remove(self._header_handle, 'HEADER')


    def is_axis_valid(self, context, index, orientation_matrix=None):
        """
        self.manipulator_matrix.to_3x3().col[index]と
        視点との角度が閾値以下ならFalseを返す
        """
        rv3d = context.region_data
        if orientation_matrix:
            omat = orientation_matrix
        else:
#             omat = self.orientation.to_3x3()
            omat = self.manipulator_matrix.to_3x3()
        viewvec = -rv3d.view_matrix.to_3x3().inverted().col[2]  # world
        axis = omat.col[index].normalized()
        val = axis.cross(viewvec).length
        val = max(0.0, min(val, 1.0))
        angle = math.asin(val)
        return angle >= self.ANGLE_LIMIT


    def update(self, context, event, update_unit_system=True):
        """
        各値の計算
        """
        region = context.region
        rv3d = context.region_data
#         v3d = context.space_data

        # Calc Mouse Coords
        current = Vector((event.mouse_region_x, event.mouse_region_y))
        if self.shift:
            relative = self.shift - self.origin + (current - self.shift) * 0.1
        else:
            relative = current - self.origin
        if self.lock:
            origin_lock = self.lock - self.origin
            if origin_lock.length < 1.0:
                self.lock = None
            elif relative.length > 0.0:
                relative = relative.project(origin_lock)

        # Update UnitSystem
        unit_system = self.unit_system
        if update_unit_system:
            unit_system.view_location = self.view_location
            unit_system.update(context)

        if self.snap:
            if self.shift:
                precision = True
                scalar = 0.01
            else:
                precision = False
                scalar = 0.1
        else:
            # 不要だけど一応
            precision = False
            scalar = 0.1

        # Update Orientation
        self.manipulator_matrix.use_normalized = self.use_normalized_orientation
        orient = self.manipulator_matrix.transform_orientation(
            context, self.use_current_orientation)
        self.manipulator_matrix.orientation = orient
        omat = self.manipulator_matrix.to_3x3()
        oimat = omat.inverted()

        # Calc World Coords
        if self.view_location is None:
            depth_location = rv3d.view_location
        else:
            depth_location = self.view_location
        originW = vav.unproject(region, rv3d, self.origin, depth_location)
        mouseR = self.origin + relative
        mouseW = vav.unproject(region, rv3d, mouseR, depth_location)

        relative_draw = None

        # Distance ------------------------------------------------------------
#         distance = relative.length / unit_system.dpbu
        distance = (oimat * mouseW - oimat * originW).length
        if self.lock and relative.dot(origin_lock) < 0.0:
            distance = -distance
        if self.snap:
            distance = unit_system.snap_grid(distance, precision)
        if self.mode == 'DISTANCE':
            distance_global = (mouseW - originW).length
            relative_draw = relative.normalized() * abs(distance_global) * \
                            unit_system.dpbu

        # Factor --------------------------------------------------------------
        factor = relative.length / self.dpf
        if self.lock and relative.dot(origin_lock) < 0.0:
            factor = -factor
        if self.snap:
            factor = unit_system.snap_value(factor, scalar)
        if self.mode == 'FACTOR':
            relative_draw = relative.normalized() * abs(factor) * self.dpf

        # Translation ---------------------------------------------------------
        viewvec = -rv3d.view_matrix.to_3x3().inverted().col[2]  # world

        # if self.axes == self.AXISALL:
        if self.axis.count(True) == 3 or \
           self.axis.count(False) == 3:
            translation = oimat * mouseW - oimat * originW

        else:
            def const_axis(index):
                axis = omat.col[index].normalized()
                axisR = vav.project(region, rv3d, originW + axis).to_2d() \
                        - self.origin
                vR = relative.project(axisR) + self.origin
                nearW = vav.unproject(region, rv3d, vR, depth_location)
                farW = vav.unproject(region, rv3d, vR, depth_location + viewvec)
                v5, _ = geom.intersect_line_line(originW, originW + axis,
                                                 nearW, farW)
                return oimat * v5 - oimat * originW

            def const_plane(index):
                axis = omat.col[index].normalized()
                plane = vam.PlaneVector(originW, axis)
                v3 = vav.unproject(region, rv3d, self.origin + relative,
                                   depth_location + viewvec)
                v4 = plane.intersect(mouseW, v3)
                return oimat * v4 - oimat * originW

            if self.axis.count(True) == 1:
                i = self.axis.index(True)
                if self.is_axis_valid(context, i):
                    # 角度は様子見て調節する必要あり
                    translation = const_axis(i)
                else:
                    f = -relative[1] * self.unit_system.bupd
                    translation = Vector((0, 0, 0))
                    translation[i] = f
            else:
                if self.axis == self.CONSTXY:
                    if not self.is_axis_valid(context, 0):
                        translation = const_axis(1)
                    elif not self.is_axis_valid(context, 1):
                        translation = const_axis(0)
                    else:
                        translation = const_plane(2)
                elif self.axis == self.CONSTXZ:
                    if not self.is_axis_valid(context, 0):
                        translation = const_axis(2)
                    elif not self.is_axis_valid(context, 2):
                        translation = const_axis(0)
                    else:
                        translation = const_plane(1)
                elif self.axis == self.CONSTYZ:
                    if not self.is_axis_valid(context, 1):
                        translation = const_axis(2)
                    elif not self.is_axis_valid(context, 2):
                        translation = const_axis(1)
                    else:
                        translation = const_plane(0)

        if self.snap:
            translation = unit_system.snap_grid(translation, precision)

        if self.mode == 'TRANSLATION':
            v1 = vav.unproject(region, rv3d, self.origin, self.view_location)
            v1 += omat * translation
            v2 = vav.project(region, rv3d, v1).to_2d()
            relative_draw = v2 - self.origin

        # Rotation ------------------------------------------------------------
        location = self.manipulator_matrix.to_translation()
        pivot = vav.project(region, rv3d, location).to_2d()

        vec1 = self.origin - pivot
        vec2 = mouseR - pivot
        oquat = omat.to_quaternion()

        if vec1.length == 0.0:
            rotation_angle = -vam.vecs_angle(Vector((1, 0)), vec2)
        elif vec2.length == 0.0:
            rotation_angle = 0.0
        else:
            rotation_angle = -vam.vecs_angle(vec1, vec2)  # 時計回りが正
        if self.snap:
            scalar = math.radians(1.0 if self.shift else 5.0)
            rotation_angle = unit_system.snap_value(rotation_angle, scalar)
        angle = rotation_angle
        if len(set(self.axis)) == 1:
            # 必ずself.use_local_coordsが偽であること
            # 2/14 ↑コメントの意味不明
            rotation_axis = viewvec
            quat = Quaternion(rotation_axis, rotation_angle)
            rotation = oquat.inverted() * quat * oquat
        else:
            if self.axis == self.CONSTX or self.axis == self.CONSTYZ:
                axisW = omat.col[0].normalized()
                rotation_axis = Vector((1, 0, 0))
            elif self.axis == self.CONSTY or self.axis == self.CONSTXZ:
                axisW = omat.col[1].normalized()
                rotation_axis = Vector((0, 1, 0))
            else:
                axisW = omat.col[2].normalized()
                rotation_axis = Vector((0, 0, 1))
            if axisW.dot(viewvec) < -1e-5:
                rotation_angle = -rotation_angle
            rotation = Quaternion(rotation_axis, rotation_angle)

        if self.mode == 'ROTATION':
            l = (self.origin + relative - pivot).length
            v1 = self.origin - pivot
            v1.normalize()
            q = Quaternion(Vector((0, 0, -1)), angle)
            v2 = (q * v1.to_3d()).to_2d() * l
            relative_draw = v2 + pivot - self.origin

        # Trackball -----------------------------------------------------------
        # 160dot == math.pi / 2
        trackball_x = relative[0] * (math.pi / 320)
        trackball_y = relative[1] * (math.pi / 320)
        if self.axis == self.CONSTX:
            trackball_y = 0.0
        elif self.axis == self.CONSTY:
            trackball_x = 0.0
        if self.snap:
            scalar = math.radians(1.0 if self.shift else 5.0)
            trackball_x = unit_system.snap_value(trackball_x, scalar)
            trackball_y = unit_system.snap_value(trackball_y, scalar)
        viewxvec = rv3d.view_matrix.to_3x3().inverted().col[0]  # world
        viewyvec = rv3d.view_matrix.to_3x3().inverted().col[1]  # world
        roty = Quaternion(viewyvec, trackball_x)
        rotx = Quaternion(viewxvec, -trackball_y)
        trackball = oquat.inverted() * rotx * roty * oquat
        if self.mode == 'TRACKBALL':
            relative_draw = Vector((trackball_x / (math.pi / 320),
                                    trackball_y / (math.pi / 320)))

        # Resize --------------------------------------------------------------
        l1 = vec1.length
        l2 = vec2.length
        if l1 != 0.0:
            size = l2 / l1
            if vec1.dot(vec2) < 0.0:
                size = -size
        else:
            size = 1.0
        if self.snap:
            scalar = 0.01 if self.shift else 0.1
            size = unit_system.snap_value(size, scalar)
        if len(set(self.axis)) == 1:
            resize = Vector.Fill(3, size)
        elif self.axis == self.CONSTX:
            resize = Vector((size, 1, 1))
        elif self.axis == self.CONSTY:
            resize = Vector((1, size, 1))
        elif self.axis == self.CONSTZ:
            resize = Vector((1, 1, size))
        elif self.axis == self.CONSTXY:
            resize = Vector((size, size, 1))
        elif self.axis == self.CONSTXZ:
            resize = Vector((size, 1, size))
        elif self.axis == self.CONSTYZ:
            resize = Vector((1, size, size))

        if self.mode == 'RESIZE':
            relative_draw = vec2.normalized() * l1 * abs(size) \
                            + pivot - self.origin

        # Set attributes ------------------------------------------------------
        self.mco = current
        self.relative = relative
        self.relative_draw = relative_draw

        self.distance = distance
        self.factor = factor
        self.translation = translation
        self.rotation = rotation
        self.rotation_axis = rotation_axis
        self.rotation_angle = rotation_angle
        self.trackball = trackball
        self.trackball_x = trackball_x
        self.trackball_y = trackball_y
        self.resize = resize

    # Callbacks ---------------------------------------------------------------
    def callback_default(self, context):
        """modeがNoneの場合"""
        pass

    def callback_distance(self, context):
        if self.exp.active:
            # value = float(self.unit_system.str_to_num(self.exp[0], 0.0))
            value = float(self.unit_system.unit_to_num(self.exp[0],
                                                       fallback=0.0))
        else:
            # self.exp[0] = self.unit_system.num_to_str(self.distance, 'bu')
            self.exp[0] = self.unit_system.num_to_unit(self.distance)
            value = self.distance
        self.value = value

    def callback_factor(self, context):
        if self.exp.active:
            value = self.exp(0, 0.0)  # systemを無視する
        else:
            self.exp[0] = str(self.factor)
            value = self.factor
        self.value = value

    def callback_translation(self, context):
        value = Vector((0, 0, 0))
        for i in range(3):
            if self.exp.active:
                # value[i] = float(self.unit_system.str_to_num(self.exp[i], 0.0))
                value[i] = float(self.unit_system.unit_to_num(self.exp[i],
                                                              fallback=0.0))
            else:
                value[i] = self.translation[i]
                # self.exp[i] = self.unit_system.num_to_str(value[i], 'bu')
                self.exp[i] = self.unit_system.num_to_unit(value[i])
        self.value = value

    def callback_rotation(self, context):
        if self.exp.active:
            if self.exp.cursor[0] == 0:
                angle = math.radians(self.exp(0, 0.0))
                if len(set(self.axis)) == 1:
                    rv3d = context.region_data
                    viewvec = -rv3d.view_matrix.to_3x3().inverted().col[2]
                    quat = Quaternion(viewvec, angle)
#                     oquat = self.orientation.to_quaternion()
                    oquat = self.manipulator_matrix.to_quaternion()
                    value = oquat.inverted() * quat * oquat
                else:
                    if self.axis == self.CONSTX or self.axis == self.CONSTYZ:
                        rotation_axis = Vector((1, 0, 0))
                    elif self.axis == self.CONSTY or self.axis == self.CONSTXZ:
                        rotation_axis = Vector((0, 1, 0))
                    else:
                        rotation_axis = Vector((0, 0, 1))
                    value = Quaternion(rotation_axis, angle)
            else:
                eul = Euler([math.radians(self.exp(i + 1, 0.0))
                             for i in range(3)])
                value = eul.to_quaternion()
            self.value = value
        else:
            eul = self.rotation.to_euler()
            self.exp[0] = str(math.degrees(self.rotation_angle))
            for i in range(3):
                self.exp[i + 1] = str(math.degrees(eul[i]))
            self.value = self.rotation.copy()

    def callback_trackball(self, context):
        if self.exp.active:
            rv3d = context.region_data
#             oquat = self.orientation.to_quaternion()
            oquat = self.manipulator_matrix.to_quaternion()
            viewxvec = rv3d.view_matrix.to_3x3().inverted().col[0]  # world
            viewyvec = rv3d.view_matrix.to_3x3().inverted().col[1]  # world
            trackball_x = math.radians(self.exp(0, 0.0))
            trackball_y = math.radians(self.exp(1, 0.0))
            roty = Quaternion(viewyvec, trackball_x)
            rotx = Quaternion(viewxvec, -trackball_y)
            trackball = oquat.inverted() * rotx * roty * oquat
            self.value = trackball
        else:
            self.exp[0] = str(math.degrees(self.trackball_x))
            self.exp[1] = str(math.degrees(self.trackball_y))
            self.value = self.trackball.copy()

    def callback_resize(self, context):
        if self.exp.active:
            value = Vector([self.exp(i, 1.0) for i in range(3)])
        else:
            for i in range(3):
                self.exp[i] = str(self.resize[i])
            value = self.resize.copy()
        self.value = value

    def callback(self, context):
        """他のcallbackの後、modeに関係なく常に呼ばれる"""
        master = self.master
        for exec_string in self.callback_exec_strings.values():
            exec(exec_string, globals(), locals())

    # Modal -------------------------------------------------------------------
    def modal(self, context, event, view_location=None):
        """
        -> enum set in {'RUNNING_MODAL', 'CANCELLED', 'FINISHED',
                        'PASS_THROUGH'}
        """
        self.context = context
        self.event = event

        mco = Vector((event.mouse_region_x, event.mouse_region_y))

        # キャンセル、終了の判定もexpが行う。
        retval = self.exp.modal(event)

        # 終了ならコールバックを呼ばずに終える
        if retval == {'FINISHED'} or retval == {'CANCELLED'}:
            self.draw_handler_remove(context)
            context.area.tag_redraw()
            return retval

        def middlemouse_transform():
            """中ボタンで軸固定"""
            vmat3 = context.region_data.view_matrix.to_3x3()

            if self.mode == 'TRACKBALL':
                omat = vmat3.inverted()
            else:
                omat = self.manipulator_matrix.to_3x3()
            axis_ls = []
            for i in range(3):
                if self.is_axis_valid(context, i, omat):
                    axis_ls.append(omat.col[i])
                else:
                    axis_ls.append(None)

            vals = []
            for i in range(3):
                if axis_ls[i]:
                    v = (vmat3 * axis_ls[i]).to_2d().normalized()
                    vals.append(abs(vam.dot2d(v, self.relative)))
                else:
                    vals.append(0.0)

            i = vals.index(max(vals))
            if i == 0:
                self.axis = self.CONSTX
            elif i == 1:
                self.axis = self.CONSTY
            else:
                if self.mode != 'TRACKBALL':
                    self.axis = self.CONSTZ

        if retval == {'PASS_THROUGH'}:
            retval = {'RUNNING_MODAL'}

            if event.type in self.ignore_keys:
                retval = {'PASS_THROUGH'}

            elif event.type == 'MOUSEMOVE':
                if self.middlemouse:
                    if self.mode in ('NONE', 'DISTANCE', 'FACTOR'):
                        self.lock = mco.copy()
                    else:
                        middlemouse_transform()

            elif event.value == 'PRESS':
                if event.type in ('LEFT_SHIFT', 'RIGHT_SHIFT'):
                    self.shift = mco.copy()
                elif event.type in ('LEFT_CTRL', 'RIGHT_CTRL'):
                    self.snap = True

                elif event.type == self.shortcuts.get('reset', ''):
                    if self.lock:
                        self.lock = mco + (self.lock - self.origin)
                    self.origin = mco.copy()

                elif (event.type == self.shortcuts.get('lock') and
                      self.mode in ('NONE', 'DISTANCE', 'FACTOR')):
                    self.middlemouse = mco.copy()
                    self.locked_when_middlemouse = self.lock is not None
                    self.lock = mco.copy()

                elif (event.type == self.shortcuts.get('axis') and
                      self.mode in ('TRANSLATION', 'ROTATION', 'RESIZE',
                                    'TRACKBALL')):
                    self.middlemouse = mco.copy()
                    self.locked_when_middlemouse = len(set(self.axis)) != 1
                    middlemouse_transform()

                elif event.type == self.shortcuts.get('distance') and \
                     'DISTANCE' in self.modes:
                    if self.mode == 'DISTANCE':
                        self.use_current_orientation ^= True
                    else:
                        self.mode = 'DISTANCE'
                        self.use_current_orientation = False
                        self.origin = mco.copy()

                elif event.type == self.shortcuts.get('factor') and \
                     'FACTOR' in self.modes:
                    if self.mode != 'FACTOR':
                        self.mode = 'FACTOR'
                        self.origin = mco.copy()
                    self.use_current_orientation = False

                elif event.type == self.shortcuts.get('translation') and \
                     'TRANSLATION' in self.modes:
                    if self.mode == 'TRANSLATION':
                        self.use_current_orientation ^= True
                    else:
                        self.use_current_orientation = False
                        self.origin = mco.copy()
                    self.mode = 'TRANSLATION'
                    self.lock = None
                    self.middlemouse = None

                elif event.type == self.shortcuts.get('rotation') and \
                     ('ROTATION' in self.modes or 'TRACKBALL' in self.modes):
                    changed = False
                    if self.mode == 'ROTATION':
                        if 'TRACKBALL' in self.modes:
                            self.mode = 'TRACKBALL'
                            if self.axis == self.CONSTZ:
                                self.axis = self.CONSTNONE
                            changed = True
                    else:
                        if 'ROTATION' in self.modes:
                            self.mode = 'ROTATION'
                        else:
                            self.mode = 'TRACKBALL'
                            if self.axis == self.CONSTZ:
                                self.axis = self.CONSTNONE
                        changed = True
                    if changed:
                        self.use_current_orientation = False
                        self.origin = mco.copy()
                        self.lock = None
                        self.middlemouse = None

                elif event.type == self.shortcuts.get('resize') and \
                     'RESIZE' in self.modes:
                    if self.mode != 'RESIZE':
                        self.mode = 'RESIZE'
                        self.origin = mco.copy()
                    self.use_current_orientation = False
                    self.lock = None
                    self.middlemouse = None

                elif event.type in (self.shortcuts.get('x'),
                                    self.shortcuts.get('y'),
                                    self.shortcuts.get('z')):
                    if event.type == self.shortcuts.get('x'):
                        axs = self.CONSTX
                        naxs = self.CONSTYZ
                    elif event.type == self.shortcuts.get('y'):
                        axs = self.CONSTY
                        naxs = self.CONSTXZ
                    else:
                        axs = self.CONSTZ
                        naxs = self.CONSTXY

                    if self.axis == axs or self.axis == naxs:
                        if (self.use_current_orientation or
                            self.mode == 'TRACKBALL'):
                            # local軸制限から制限無しへ
                            self.axis = self.CONSTNONE
                            self.use_current_orientation = False
                        else:
                            # global軸制限からlocal軸制限へ
                            if event.shift:
                                self.axis = naxs
                            else:
                                self.axis = axs
                            self.use_current_orientation = True
                    else:
                        # 制限無しからglobal軸の制限へ
                        if self.mode == 'TRACKBALL':
                            if axs == self.CONSTX or axs == self.CONSTY:
                                self.axis = axs
                        else:
                            if event.shift:
                                self.axis = naxs
                            else:
                                self.axis = axs
                        self.use_current_orientation = False

                else:
                    retval = {'PASS_THROUGH'}

            elif event.value == 'RELEASE':
                if event.type in ('LEFT_SHIFT', 'RIGHT_SHIFT'):
                    self.shift = None
                elif event.type in ('LEFT_CTRL', 'RIGHT_CTRL'):
                    self.snap = False

                elif (event.type == self.shortcuts.get('lock') and
                      self.mode in ('NONE', 'DISTANCE', 'FACTOR')):
                    if self.middlemouse:
                        if self.locked_when_middlemouse:
                            if (mco - self.middlemouse).length < 1:
                                self.lock = None
                    self.middlemouse = None
                elif (event.type == self.shortcuts.get('axis') and
                      self.mode in ('TRANSLATION', 'ROTATION', 'RESIZE',
                                    'TRACKBALL')):
                    if self.middlemouse:
                        if self.locked_when_middlemouse:
                            if (mco - self.middlemouse).length < 1:
                                self.axis = self.CONSTNONE
                                self.use_current_orientation = False
                    self.middlemouse = None

                else:
                    retval = {'PASS_THROUGH'}

            else:
                retval = {'PASS_THROUGH'}

        self.update(context, event, view_location)

        # Callback
        # self.valueに代入する
        if self.mode == 'DISTANCE':
            self.callback_distance(context)
        elif self.mode == 'FACTOR':
            self.callback_factor(context)
        elif self.mode == 'TRANSLATION':
            self.callback_translation(context)
        elif self.mode == 'ROTATION':
            self.callback_rotation(context)
        elif self.mode == 'RESIZE':
            self.callback_resize(context)
        elif self.mode == 'TRACKBALL':
            self.callback_trackball(context)
        else:
            self.callback_default(context)

        # selfの値をself.masterに代入する
        self.callback(context)

        return retval

    # Draw --------------------------------------------------------------------
    def draw(self, context, color=(1.0, 1.0, 1.0, 1.0)):
        region = context.region
        rv3d = context.region_data

        if region.id != self.region_id:
            return

        color_half = list(color)
        color_half[3] /= 2
        x, y = self.origin

        is_line_smooth = vagl.Buffer('bool', 0, bgl.GL_LINE_SMOOTH)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        is_blend = vagl.Buffer('bool', 0, bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_BLEND)
        glcolor = vagl.Buffer('double', 4, bgl.GL_CURRENT_COLOR)

        omat = self.manipulator_matrix.to_3x3()
        oloc = self.manipulator_matrix.to_translation()
        vmat = rv3d.view_matrix
        vimat = vmat.inverted()

        # Lock Axis
        if self.mode in ('TRANSLATION', 'ROTATION', 'RESIZE', 'TRACKBALL'):
            if self.axis not in (self.CONSTALL, self.CONSTNONE):
                for i in range(3):
                    if self.axis[i]:
                        if self.mode == 'TRACKBALL':
                            v = vimat.col[i].to_3d() * 1000
                        else:
                            v = omat.col[i] * 1000
                        v1 = vav.project(region, rv3d, oloc + v).to_2d()
                        v2 = vav.project(region, rv3d, oloc - v).to_2d()
                        col = [0.5, 0.5, 0.5, 1.0]
                        col[i] = 1.0
                        bgl.glColor4f(*col)
                        bgl.glBegin(bgl.GL_LINES)
                        bgl.glVertex2f(*v1)
                        bgl.glVertex2f(*v2)
                        bgl.glEnd()

        bgl.glColor4f(*color)

        # Origin
        if 'origin' in self.draw_items:
            vagl.draw_sun(x, y, 5, 16, [0, math.pi], [10, 10])

        # Relative
        if 'relative' in self.draw_items:
            if self.relative_draw:
                relative_draw = self.relative_draw
            else:
                relative_draw = self.relative

            if self.exp.active and self.mode != 'NONE':
                if self.relative.length:
                    relative = self.relative.normalized()
                else:
                    relative = Vector((1, 0))
                vec = Vector((0, 0))
                if self.mode == 'DISTANCE':
                    if self.exp(0):
                        vec = relative * self.exp(0) * self.unit_system.dpbu
                elif self.mode == 'FACTOR':
                    if self.exp(0):
                        vec = relative * self.exp(0) * self.dpf
                elif self.mode == 'TRANSLATION':
                    v = vav.unproject(region, rv3d, self.origin,
                                      self.view_location)
                    v += omat * Vector(self.exp(fallback=0.0))
                    vec = vav.project(region, rv3d, v).to_2d() - self.origin
                vagl.draw_circle(x + vec[0], y + vec[1], 5, 16)

            elif not self.exp.active:
                rx, ry = relative_draw
                vagl.draw_circle(x + rx, y + ry, 5, 16)

        # Lock Arrow
        if 'lock' in self.draw_items:
            if self.mode not in ('TRANSLATION', 'ROTATION', 'RESIZE',
                                 'TRACKBALL'):
                if self.lock is not None:
                    bgl.glColor4f(*color)
                    vec = (self.origin - self.lock).normalized() * 20
                    vecn = self.lock + vec
                    vagl.draw_arrow(vecn[0], vecn[1],
                                    self.lock[0], self.lock[1],
                                    headlength=10, headangle=math.radians(110),
                                    headonly=True)

        # 点線, 円
        if not self.exp.active and self.mode in ('ROTATION', 'RESIZE'):
            pivot = vav.project(region, rv3d, oloc).to_2d()
            flag = vagl.Buffer('bool', 0, bgl.GL_LINE_STIPPLE)
            bgl.glEnable(bgl.GL_LINE_STIPPLE)
            bgl.glLineStipple(8, int(0b101010101010101))
            bgl.glBegin(bgl.GL_LINES)
            bgl.glVertex2f(*pivot)
            bgl.glVertex2f(*self.origin)
            if self.mode == 'ROTATION':
                bgl.glVertex2f(*pivot)
                bgl.glVertex2f(*(self.origin + relative_draw))
            bgl.glEnd()
            vagl.glSwitch(bgl.GL_LINE_STIPPLE, flag)
            if self.mode == 'RESIZE':
                bgl.glColor4f(*color_half)
                r = (self.origin - pivot).length
                vagl.draw_circle(pivot[0], pivot[1], r, 64)

        # Factor
        if 'factor' in self.draw_items:
            if self.mode == 'FACTOR':
                bgl.glColor4f(*color_half)
                vagl.draw_circle(x, y, self.dpf, 64)

        vagl.glSwitch(bgl.GL_LINE_SMOOTH, is_line_smooth)
        vagl.glSwitch(bgl.GL_BLEND, is_blend)
        bgl.glColor4f(*glcolor)


    def header_text(self, context):
        return ''

    def draw_header(self, context, font_id=0, font_size=None,
                    color=(1.0, 1.0, 1.0, 1.0),
                    error_color=(1.0, 0.6, 0.5, 1.0)):

        if context.region.id != self.header_region_id:
            return

        glcolor = vagl.Buffer('double', 4, bgl.GL_CURRENT_COLOR)

        # Background
        theme = context.user_preferences.themes['Default']
        backcol = theme.view_3d.space.header
        bgl.glColor3f(*backcol)
        bgl.glRecti(0, 0, context.region.width, context.region.height)

        if font_size:
            dpi = context.user_preferences.system.dpi
            blf.size(font_id, font_size, dpi)

        space = 10

        ofsx = space
        ofsy = 10

        ofsx_r, ofsy_r = self.exp.draw(context, ofsx, ofsy)

        text = ""
        if self.mode in ('TRANSLATION', 'ROTATION', 'RESIZE'):
            text = self.manipulator_matrix.name
        if len(set(self.axis)) != 1:
            ls = []
            for flag, name in zip(self.axis, ("X", "Y", "Z")):
                if flag:
                    ls.append(name)
            if text:
                text += " "
            text += "-".join(ls)
        if text:
            text = "[" + text + "]"
        blf.position(font_id, ofsx_r + space, ofsy_r, 0)
        bgl.glColor4f(*color)
        blf.draw(font_id, text)

        tail_text = self.header_text(context)
        if tail_text:
            ofsx_r += blf.dimensions(font_id, text)[0] + space
            blf.position(font_id, ofsx_r, ofsy_r, 0)
            blf.draw(font_id, tail_text)

        bgl.glColor4f(*glcolor)


#==============================================================================
# ModalMouse Test
#==============================================================================
class OT_modal_mouse(bpy.types.Operator):
    bl_description = ""
    bl_idname = 'view3d.modal_mouse'
    bl_label = "Modal Mouse"
    bl_options = {'REGISTER', 'UNDO', 'GRAB_CURSOR', 'BLOCKING'}

    distasce = bpy.props.FloatProperty(
        name="Dist",
        default=0.0)
    factor = bpy.props.FloatProperty(
        name="Fac",
        default=0.0,
        min=0.0,
        max=1.0,
        soft_min=0.0,
        soft_max=1.0)

    value = bpy.props.FloatVectorProperty(
        name="Value",
        default=(0.0, 0.0, 0.0, 0.0),
        size=4)
    use_local_orientation = bpy.props.BoolProperty(
        name="Use Local Orientation",
        default=False)
    use_current_orientation = bpy.props.BoolProperty(
        name="Use Local Orientation",
        default=False)

    @classmethod
    def poll(cls, context):
        area = context.area
        region = context.region
        return area.type == 'VIEW_3D'  # and region.type == 'WINDOW'


    def execute(self, context):
        actob = context.active_object
        # restore
        actob.matrix_world = self.mat.copy()
        actob.rotation_quaternion = self.rotation_quaternion
        actob.scale = self.scale

        modal_mouse = self.modal_mouse
        omat = modal_mouse.manipulator_matrix.to_3x3()
        oquat = omat.to_quaternion()

        obmat = actob.matrix_world.copy()
        mode = modal_mouse.mode
        if mode == 'TRANSLATION':
            loc = actob.matrix_world.col[3].to_3d()
            v = Vector(self.value[:3])
            loc = oquat * ((oquat.inverted() * loc) + v)
#             loc += oquat.inverted() * v
            actob.matrix_world.col[3][:3] = loc

        elif mode in ('ROTATION', 'TRACKBALL'):
            quat = Quaternion(self.value)
            q = oquat * quat * oquat.inverted()
            # actob.rotation_quaternion = q * actob.rotation_quaternion

            mat = (q.to_matrix() * obmat.to_3x3()).to_4x4()
            mat[3][:3] = obmat[3][:3]
            actob.matrix_world = mat

        elif mode == 'RESIZE':
            m = Matrix.Identity(3)
            m[0][0], m[1][1], m[2][2] = self.value[:3]
            s = omat * m * omat.inverted()
            mat = (s * obmat.to_3x3()).to_4x4()
            mat[3][:3] = obmat[3][:3]
            actob.matrix_world = mat


        return {'FINISHED'}


    def modal(self, context, event):
        actob = context.active_object
        # restore
        actob.matrix_world = self.mat.copy()
        actob.rotation_quaternion = self.rotation_quaternion
        actob.scale = self.scale

        retval = self.modal_mouse.modal(context, event)

        print("Dist", self.modal_mouse.distance)
        print("Fac", self.modal_mouse.factor)
        print("Translation", self.modal_mouse.translation)
        print("Rotation", self.modal_mouse.rotation,
              self.modal_mouse.rotation.to_euler())
        print("Resize", self.modal_mouse.resize)
        print("Trackbass", self.modal_mouse.trackball)

        actob = context.active_object

        if retval == {'PASS_THROUGH'}:
            self.execute(context)
            context.area.tag_redraw()
            retval = {'RUNNING_MODAL'}

        elif retval == {'RUNNING_MODAL'}:
            self.execute(context)
            context.area.tag_redraw()

        elif retval == {'CANCELLED'}:
            actob.rotation_quaternion = self.rotation_quaternion

        return retval


    def invoke(self, context, event):
#        region = context.region
#        context.window_manager.modal_handler_add(self)


        class ModalMouse2(ModalMouse):
            mode = 'TRANSLATION'

        self.modal_mouse = ModalMouse2(context, event, self,
                 view_location=None,
                 use_normalized_orientation=True)

        actob = context.active_object
        self.mat = actob.matrix_world.copy()
        self.rotation_quaternion = actob.rotation_quaternion.copy()
        self.scale = actob.scale.copy()
        return {'RUNNING_MODAL'}

bpy.utils.register_class(OT_modal_mouse)


###############################################################################
###############################################################################
class ModalMouse2:
    """
    origin, relative, shift
    mco, precision_mco, snap_increment
    
    """
    ANGLE_LIMIT = math.radians(5.0)

    def __init__(self, context, event, master, depth_location=None):
        self.depth_location = depth_location

    # Calc --------------------------------------------------------------------
    def get_depth_location(self, context):
        if self.depth_location is None:
            return context.region_data.view_location
        else:
            return self.depth_location

    def valid_axis(self, rv3d, axis):
        viewvec = -rv3d.view_matrix.to_3x3().inverted().col[2]  # world
        axis = axis.normalized()
        f = axis.cross(viewvec).length
        f = max(0.0, min(f, 1.0))
        angle = math.asin(f)
        return angle >= self.ANGLE_LIMIT

    def calc_distance(self, context):
        region = context.region
        rv3d = context.region_data
        depth_location = self.get_depth_location(context)
        originW = vav.unproject(region, rv3d, self.origin, depth_location)
        mcoW = vav.unproject(region, rv3d, self.mco, depth_location)
        distance = (mcoW - originW).length
        
        # Set variables
        self.distance = distance

    def calc_factor(self, context):
        factor = (self.mco - self.origin).length / self.dpf
        
        # Set variables
        self.factor = factor

    def calc_translation(self, context):
        """返り値はGlobal座標系"""
        region = context.region
        rv3d = context.region_data
        depth_location = self.get_depth_location(context)
        origin = self.origin
        mco = self.mco
        omat = self.orientation_matrix.to_3x3()
        oimat = omat.inverted()
        constraint_axis = tuple(self.constraint_axis)
        relative = mco - origin
        # view vec: world coords, 手前から奥に向かう
        viewvec = -rv3d.view_matrix.to_3x3().inverted().col[2]
        originW = vav.unproject(region, rv3d, origin, depth_location)
        mcoW = vav.unproject(region, rv3d, mco, depth_location)
        if all(constraint_axis) or not any(constraint_axis):
            translation = mcoW - originW
        else:
            def const_1d(index):
                axis = omat.col[index].normalized()
                axisR = (vav.project(region, rv3d, originW + axis).to_2d()
                         - origin).normalized()
                mco_const = relative.project(axisR) + origin
                nearW = vav.unproject(region, rv3d, mco_const, depth_location)
                farW = vav.unproject(region, rv3d, mco_const,
                                     depth_location + viewvec)
                isect, _ = geom.intersect_line_line(originW, originW + axis,
                                                 nearW, farW)
                return isect - originW
            def const_2d(index):
                axis = omat.col[index].normalized()
                plane = vam.PlaneVector(originW, axis)
                mcoW_far = vav.unproject(region, rv3d, mco,
                                         depth_location + viewvec)
                isect = plane.intersect(mcoW, mcoW_far)
                return isect - originW
            # Constraint 1D
            if constraint_axis.count(True) == 1:
                i = constraint_axis.index(True)
                if self.valid_axis(rv3d, omat.col[i]):
                    # 角度は様子見て調節する必要あり
                    translation = const_1d(i)
                else:
                    # Region Y+ : Axis -, Region Y-: Axis +
                    f = -relative[1] * self.unit_system.bupd
                    vec = Vector((0, 0, 0))
                    vec[i] = f
                    translation = omat * vec
            # Constraint 2D
            else:
                if constraint_axis == (True, True, False):
                    if not self.valid_axis(rv3d, omat.col[0]):
                        translation = const_1d(1)
                    elif not self.valid_axis(rv3d, omat.col[1]):
                        translation = const_1d(0)
                    else:
                        translation = const_2d(2)
                elif constraint_axis == (True, False, True):
                    if not self.valid_axis(rv3d, omat.col[0]):
                        translation = const_1d(2)
                    elif not self.valid_axis(rv3d, omat.col[2]):
                        translation = const_1d(0)
                    else:
                        translation = const_2d(1)
                elif constraint_axis == (False, True, True):
                    if not self.valid_axis(rv3d, omat.col[1]):
                        translation = const_1d(2)
                    elif not self.valid_axis(rv3d, omat.col[2]):
                        translation = const_1d(1)
                    else:
                        translation = const_2d(0)
        
        # Set variables
        self.translation = translation

    def calc_rotation(self, context):
        """返り値はGlobal座標系"""
        region = context.region
        rv3d = context.region_data
        omat = self.orientation_matrix.to_3x3()
        oimat = omat.inverted()
        constraint_axis = tuple(self.constraint_axis)
        # view vec: world coords, 手前から奥に向かう
        viewvec = -rv3d.view_matrix.to_3x3().inverted().col[2]
        pivotR = vav.project(region, rv3d, self.pivot).to_2d()
        vec1 = self.origin - pivotR
        if vec1.length == 0.0:
            vec1 = Vector((1, 0))
        vec2 = self.mco - pivotR
        if vec2.length == 0.0:
            rotation_angle = 0.0
        else:
            rotation_angle = -vam.vecs_angle(vec1, vec2)  # 時計回りが正

        if all(constraint_axis) or not any(constraint_axis):
            rotation_axis = viewvec
            rotation = Quaternion(rotation_axis, rotation_angle)
        else:
            if constraint_axis.count(True) == 1:
                i = constraint_axis.index(True)
            else:
                i = constraint_axis.index(False)
            if viewvec.dot(omat.col[i].normalized()) < -1e-5:
                rotation_angle = -rotation_angle
            rotation_axis = Vector((0, 0, 0))
            rotation_axis[i] = 1.0
            quat = Quaternion(rotation_axis, rotation_angle)
            rotation = omat * quat * oimat
        
        # Set variables
        self.rotation = rotation

    def calc_trackball(self, context):
        """返り値はGlobal座標系"""
#         region = context.region
        rv3d = context.region_data
        constraint_axis = tuple(self.constraint_axis[:2])
        relative = self.mco - self.origin
        trackball_x = relative[1] * (math.pi / 320)
        trackball_y = relative[0] * (math.pi / 320)
        if constraint_axis == (True, False):
            trackball_x = 0.0
        elif constraint_axis == (False, True):
            trackball_y = 0.0
        vimat = rv3d.view_matrix.to_3x3().inverted()
        viewxvec = vimat.col[0]  # world
        viewyvec = vimat.col[1]  # world
        rotx = Quaternion(viewxvec, -trackball_x)
        roty = Quaternion(viewyvec, trackball_y)
        trackball = rotx * roty
        
        # Set variables
        self.trackball = trackball

    def calc_scale(self, context):
        """返り値はGlobal座標系"""
        region = context.region
        rv3d = context.region_data
        omat = self.orientation_matrix.to_3x3()
        oimat = omat.inverted()
        constraint_axis = tuple(self.constraint_axis)
        # view vec: world coords, 手前から奥に向かう
        viewvec = -rv3d.view_matrix.to_3x3().inverted().col[2]
        pivotR = vav.project(region, rv3d, self.pivot).to_2d()
        vec1 = self.origin - pivotR
        vec2 = self.mco - pivotR
        if vec1.length == 0.0:
            return Vector((1, 1, 1))
        f = vec2.length / vec1.length
        if vec1.dot(vec2) < 0.0:
            f *= -1
        if constraint_axis.count(True) == 0:
            constraint_axis = (True, True, True)
        scale = Vector([f if b else 0 for b in constraint_axis])
        scale = omat * scale * oimat
        
        # Set variables
        self.scale = scale

    def calc_radial(self, context):
        
        # Set variables
        self.radial = 'scale, angle'
    
    def calc(self, context):
        """返り値はWorld座標系"""
        self.calc_distance(context)
        self.calc_factor(context)
        self.calc_translation(context)
        self.calc_rotation(context)
        self.calc_trackball(context)
        self.calc_scale(context)

    # Draw Callback -----------------------------------------------------------
    def get_header_region(self, context):
        """現在のAreaのHeaderタイプのRegionを返す"""
        for region in context.area.regions:
            if region.type == 'HEADER':
                return region
        return None

    def draw_handler_add(self, context):
        v3d = context.space_data
        self._handle = v3d.draw_handler_add(self.draw, (context,),
                                            'WINDOW', 'POST_PIXEL')
        header_region = self.get_header_region(context)
        if header_region:
            self.header_region_id = header_region.id
            self._header_handle = v3d.draw_handler_add(
                                    self.draw_header, (context,),
                                    'HEADER', 'POST_PIXEL')
        else:
            self.header_region_id = -1
            self._header_handle = None

    def draw_handler_remove(self, context):
        v3d = context.space_data
        v3d.draw_handler_remove(self._handle, 'WINDOW')
        if self._header_handle:
            v3d.draw_handler_remove(self._header_handle, 'HEADER')
