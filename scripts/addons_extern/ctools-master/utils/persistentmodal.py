# 未使用

import itertools

import bpy


"""
Window.cursor_warp()を呼ぶ度に再起動される事に注意

invoke の event は 'MOUSEMOVE' にはならない. キー・ボタン変更があるまでtypeはそのまま
"""


class PersistentModal:
    def __init__(self, operator, args=None, kwargs=None,
                 area_type=None, region_type=None,
                 compare={'MOUSE', 'TYPE', 'VALUE', 'MODIFIER'},
                 persistent=False):
        """
        :param operator: ModalOperator: bpy.ops.mod.function
        :type operator: Operator
        :param args: operator実行時に渡す引数
        :param kwargs: operator実行時に渡す引数
        :param area_type: 自動起動・再起動時のAreaの種類を指定する。
        :type area_type: str
        :param region_type: 自動起動・再起動時のRegionの種類を指定する。
        :type region_type: str
        :param compare: invoke()でのeventとmodal()でのeventの値を比較し
            有効な差があるようならoperatorを再起動する。
            但し event.type が 'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE',
            'WINDOW_DEACTIVATE', 'TIMER*' の場合は無視する。
            'MOUSE': event.mouse_x, event.mouse_y
            'TYPE': event.type
            'VALUE': event.value
            'MODIFIER': event.shift, event.ctrl, event.alt, event.oskey
        :param compare: set
        :param persistent: 別のファイルを読み込んだ時でも終了しない
        :type persistent: bool
        """

        self._operator = operator
        self.args = args
        self.kwargs = kwargs
        self.area_type = area_type
        self.region_type = region_type
        self.persistent = persistent

        # invoke()でのeventとmodal()でのeventの値を比較し
        # 有効な差があるようならoperatorを再起動する
        self.compare = compare

        # {Window.as_pointer(): Event, ...}
        self.events = {}

        # {Window.as_pointer(): event_to_dict(), ...}
        self.event_values = {}

        # {Window.as_pointer(): Operator, ...}
        self.operators = {}

        # 再起動指定されたものがoperatorsからこちらへ移る
        # {Window.as_pointer(): [Operator, ...], ...}
        self.unnecessary_operators = {}

        # 各operatorの状態
        self.operator_flags = {}  # RESTART, AUTO_START, UNNECESSARY

        # 終了時に各Windowへ送ったTimer
        # {Window.as_pointer(): Timer, ...}
        self.exit_timers = {}

        # # Pythonオブジェクトが破棄されないように一時的に確保しておく
        # self.trash = []

        self._flag = self.DEFAULT

    DEFAULT = 0
    AUTO_START = 1
    RESTART = 1 << 1
    UNNECESSARY = 1 << 2

    @property
    def operator(self):
        if isinstance(self._operator, str):
            mod, func = self._operator.split('.')
            return getattr(getattr(bpy.ops, mod), func)
        else:
            return self._operator

    @staticmethod
    def event_to_dict(event):
        """eventの属性を辞書にして返す
        :rtype: dict
        """
        # WARNING:
        #     win->eventstate->tablet_dataの安全は保証されない
        #     window生成時によく落ちる
        keys = [
            'alt',
            # 'ascii',
            'ctrl',
            # 'is_tablet',
            # 'mouse_prev_x',
            # 'mouse_prev_y',
            # 'mouse_region_x',
            # 'mouse_region_y',
            'mouse_x',
            'mouse_y',
            'oskey',
            # 'pressure',
            'shift',
            # 'tilt',
            'type',
            # 'unicode',
            'value'
        ]
        return {key: getattr(event, key) for key in keys}

    @staticmethod
    def operator_call(op, args=None, kwargs=None, scene_update=True):
        """
        :rtype: set
        """
        from _bpy import ops as ops_module

        BPyOpsSubModOp = op.__class__
        op_call = ops_module.call
        context = bpy.context

        # Get the operator from blender
        wm = context.window_manager

        # run to account for any rna values the user changes.
        if scene_update:
            BPyOpsSubModOp._scene_update(context)

        if not args:
            args = ()
        if not kwargs:
            kwargs = {}
        if args:
            C_dict, C_exec, C_undo = BPyOpsSubModOp._parse_args(args)
            ret = op_call(op.idname_py(), C_dict, kwargs, C_exec, C_undo)
        else:
            ret = op_call(op.idname_py(), None, kwargs)

        if 'FINISHED' in ret and context.window_manager == wm:
            if scene_update:
                BPyOpsSubModOp._scene_update(context)

        return ret

    def invoke(self, context, event, operator):
        """invoke で modal operator を開始する時に呼ぶ。CANCELLED や FINISHED
        では呼ばない事。
        再起動した場合は取得し損ねたEventの値を返す。
        """
        window = context.window
        addr = window.as_pointer()
        if addr in self.operators:
            return False
        self._add_handler()
        self.operators[addr] = operator
        self.events[addr] = event
        if operator not in self.operator_flags:
            self.operator_flags[operator] = self.DEFAULT
        else:
            self.operator_flags[operator] = self._flag
        self.event_values[addr] = self.event_to_dict(event)
        return True

    def get_lost_event(self, context, operator):
        window = context.window
        addr = window.as_pointer()
        if self.is_restart(operator):
            return self.event_values[addr]
        else:
            return None

    def is_auto_start(self, operator):
        """operatorが自動起動したものなら真を返す
        """
        if operator in self.operator_flags:
            return self.operator_flags[operator] & self.AUTO_START != 0
        else:
            return False

    def is_unnecessary(self, operator):
        """operatorが再起動及びexit_all()により不要となったものなら真を返す
        """
        if operator in self.operator_flags:
            return self.operator_flags[operator] & self.UNNECESSARY != 0
        else:
            return False

    def _exit_unnecessary(self, context, operator):
        """modal先頭で呼んで真を返すならすぐmodalを修了する"""
        removed = False
        wm = context.window_manager
        window = context.window
        addr = window.as_pointer()
        # Operator削除
        if addr in self.unnecessary_operators:
            ops = self.unnecessary_operators[addr]
            if operator in ops:
                ops.remove(operator)
                removed = True
            if not ops:
                del self.unnecessary_operators[addr]

        # Timer削除
        if addr in self.exit_timers:
            if (addr not in self.operators or
                    addr not in self.unnecessary_operators):
                wm.event_timer_remove(self.exit_timers[addr])
        # Handler削除
        if not self.is_modal_running_any(context):
            self._remove_handler()
        return removed

    def exit_all(self, context, operator=None):
        """'modal operator 終了時に呼ぶ'"""
        wm = context.window_manager

        # operator削除
        if operator:
            if not self._exit_unnecessary(context, operator):
                addr = context.window.as_pointer()
                if addr in self.operators:
                    del self.operators[addr]
                # Timer削除
                if addr in self.exit_timers:
                    if addr not in self.unnecessary_operators:
                        wm.event_timer_remove(self.exit_timers[addr])

        # Handler削除
        self._remove_handler()

        # 全windowに対してイベントを発生させそのオペレータに
        # UNNECESSARYフラグを付ける
        for window in wm.windows:
            addr = window.as_pointer()
            if addr in self.operators:
                op = self.operators.pop(addr)
                ops = self.unnecessary_operators.setdefault(addr, [])
                ops.append(op)
                self.operator_flags[op] |= self.UNNECESSARY
                timer = wm.event_timer_add(0.0, window)
                self.exit_timers[addr] = timer

    def modal(self, context, event, operator):
        """modalで呼ぶ"""
        if self._exit_unnecessary(context, operator):
            return False
        else:
            window = context.window
            addr = window.as_pointer()
            self.event_values[addr] = self.event_to_dict(event)
            return True

    def is_restart(self, operator):
        """operatorが再起動により開始されたものなら真を返す"""
        if operator in self.operator_flags:
            return self.operator_flags[operator] & self.RESTART != 0
        else:
            return self._flag & self.RESTART

    def is_modal_running(self, context, window=None):
        """有効なoperatorが実行中なら真を返す。
        handlerの有無は確認しない。
        """
        if window:
            if window not in context.window_manager.windows:
                return False
        else:
            window = context.window
        return window.as_pointer() in self.operators

    def is_modal_running_any(self, context):
        """全てのWindowで一つでも有効なoperatorが実行中ならなら真を返す。
        handlerの有無は確認しない。
        """
        wm = context.window_manager
        win_addr = {win.as_pointer() for win in wm.windows}
        op_addr = set(self.operators)
        return bool(win_addr & op_addr)

    def _test_compare(self, modal_ev, window_ev):
        """再起動が必要なら真を返す"""
        model_event_type = modal_ev['type']

        if 'MOUSE' in self.compare:
            if (window_ev['mouse_x'] != modal_ev['mouse_x'] or
                    window_ev['mouse_y'] != modal_ev['mouse_y']):
                return True

        if model_event_type in ('MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'):
            return False
        # if model_event_type.startswith('EVT_TWEAK'):
        #     return False
        if model_event_type == 'WINDOW_DEACTIVATE':
            return False
        if model_event_type.startswith('TIMER'):
            return False

        if 'TYPE' in self.compare:
            if model_event_type != window_ev['type']:
                return True
        if 'VALUE' in self.compare:
            if modal_ev['value'] != window_ev['value']:
                return True
        if 'MODIFIER' in self.compare:
            for mod in ('shift', 'ctrl', 'alt', 'oskey'):
                if modal_ev[mod] != window_ev[mod]:
                    return True
        return False

    # FIXME
    @bpy.app.handlers.persistent
    def scene_update_pre(self, scene):
        """新規windowへの起動、再起動"""
        context = bpy.context
        if not self.is_modal_running_any(context) and not self.persistent:
            self._remove_handler()
            print('Remove >>>>>>>>>>>>>>>>>>>>>>>>')
            return

        for window in context.window_manager.windows:
            if window.screen.scene != scene:
                continue
            addr = window.as_pointer()
            auto_start = restart = False

            # Auto Start (new window created)
            if addr not in self.operators:
                auto_start = True

            # Restart (other modal operator started)
            else:
                modal_ev = self.event_values[addr]
                window_ev = self.event_to_dict(self.events[addr])
                restart = self._test_compare(modal_ev, window_ev)
                if restart:
                    op = self.operators.pop(addr)
                    ops = self.unnecessary_operators.setdefault(addr, [])
                    ops.append(op)
                    self.operator_flags[op] |= self.UNNECESSARY
                    for key in window_ev:
                        v1 = modal_ev[key]
                        v2 = window_ev[key]
                        if v1 != v2:
                            print(key, v1, v2)
                    print(modal_ev)
                    print(window_ev)
                    print('do restart')

            # Call operator
            if auto_start or restart:
                override = op_context = undo = None
                if self.args:
                    for arg in self.args:
                        if isinstance(arg, dict):
                            override = arg
                        elif isinstance(arg, str):
                            op_context = arg
                        elif isinstance(arg, bool):
                            undo = arg

                # override context
                if self.area_type or self.region_type:
                    if override is not None:
                        override = dict(override)
                    else:
                        override = context.copy()
                    area = None
                    if self.area_type:
                        for sa in window.screen.areas:
                            if sa.type == self.area_type:
                                override['area'] = area = sa
                                break
                    if self.region_type:
                        if not area:
                            area = window.screen.areas[0]
                        for region in area.regions:
                            if region.type == self.region_type:
                                override['region'] = region
                                break

                # operator context
                if not op_context or not op_context.startswith('INVOKE'):
                    op_context = 'INVOKE_DEFAULT'
                # merge
                args = []
                for value in (override, op_context, undo):
                    if value is not None:
                        args.append(value)

                # Call invoke()
                self._flag = self.AUTO_START if auto_start else self.RESTART
                self.operator_call(self.operator, args, self.kwargs,
                                   scene_update=False)
                self._flag = self.DEFAULT

    def _add_handler(self):
        handlers = bpy.app.handlers.scene_update_pre
        if self.scene_update_pre not in handlers:
            handlers.append(self.scene_update_pre)
            return True
        else:
            return False

    def _remove_handler(self):
        handlers = bpy.app.handlers.scene_update_pre
        if self.scene_update_pre in handlers:
            handlers.remove(self.scene_update_pre)
            return True
        else:
            return False


##########################################
pm = PersistentModal('view3d.modal_test', persistent=True)


class ModalTest(bpy.types.Operator):
    bl_idname = "view3d.modal_test"
    bl_label = "Modal Test"

    def __init__(self):
        self.mco = (0, 0)

    def modal(self, context, event):
        if not pm.modal(context, event, self):
            return {'CANCELLED', 'PASS_THROUGH'}

        mco = (event.mouse_x, event.mouse_y)
        if event.type in ('MOUSEMOVE', 'INBETWEEN_MOUSEMOVE'):
            if mco == self.mco:
                return {'PASS_THROUGH'}
        self.mco = mco

        import time
        print(time.time(), context.window, context.screen,
              context.area, context.region, event.type, event.value,
              (event.mouse_x, event.mouse_y))

        if event.type in {'ESC'}:  # Cancel
            pm.exit_all(context, self)
            print('Exit')
            return {'CANCELLED', 'PASS_THROUGH'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if pm.is_restart(self):
            print('invoke: restart')
        else:
            print('invoke: new')
        self.mco = (event.mouse_x, event.mouse_y)
        if pm.invoke(context, event, self):
            context.window_manager.modal_handler_add(self)
            lost_event_value = pm.get_lost_event(context, self)
            return {'RUNNING_MODAL'}
        else:
            return {'CANCELLED'}


bpy.utils.register_class(ModalTest)

###############################################################################
import ctypes
from ctypes import *


class ListBase(Structure):
    """source/blender/makesdna/DNA_listBase.h: 59"""
    _fields_ = [
        ('first', c_void_p),
        ('last', c_void_p)
    ]


class wmEvent(Structure):
    """source/blender/windowmanager/WM_types.h: 427"""
    pass

wmEvent._fields_ = [
    ('next', POINTER(wmEvent)),
    ('prev', POINTER(wmEvent)),
    ('type', c_short),
    ('val', c_short),
    ('click_type', c_short),
    ('x', c_int),
    ('y', c_int),
    ('click_time', c_double),
    ('mval', c_int * 2),
    ('utf8_buf', c_char * 6),

    ('ascii', c_char),
    ('pad', c_char),

    ('is_key_pressed', c_bool),

    ('prevtype', c_short),
    ('prevval', c_short),
    ('prevx', c_int),
    ('prevy', c_int),
    ('prevclick_time', c_double),
    ('prevclickx', c_int),
    ('prevclicky', c_int),

    ('shift', c_short),
    ('ctrl', c_short),
    ('alt', c_short),
    ('oskey', c_short),
    ('keymodifier', c_short),

    ('keymap_idname', c_char_p),

    ('tablet_data', c_void_p),  # struct wmTabletData

    ('custom', c_short),
    ('customdatafree', c_short),
    ('pad2', c_int),

    ('customdata', c_void_p),
]


class wmWindow(Structure):
    """source/blender/makesdna/DNA_windowmanager_types.h: 173"""
    pass

wmWindow._fields_ = [
    ('next', POINTER(wmWindow)),
    ('prev', POINTER(wmWindow)),
    ('ghostwin', c_void_p),

    ('screen', c_void_p),  # struct bScreen
    ('newscreen', c_void_p),  # struct bScreen
    ('screenname', c_char * 64),

    ('posx', c_short),
    ('posy', c_short),
    ('sizex', c_short),
    ('sizey', c_short),
    ('windowstate', c_short),
    ('monitor', c_short),
    ('active', c_short),
    ('cursor', c_short),
    ('lastcursor', c_short),
    ('modalcursor', c_short),
    ('grabcursor', c_short),
    ('addmousemove', c_short),

    ('winid', c_int),

    ('lock_pie_event', c_short),
    ('last_pie_event', c_short),

    ('eventstate', ctypes.POINTER(wmEvent)),  # struct wmEvent

    ('curswin', c_void_p),  # struct wmSubWindow

    ('tweak', c_void_p),  # struct wmGesture

    ('ime_data', c_void_p),  # struct wmIMEData

    ('drawmethod', c_int),
    ('drawfail', c_int),

    ('drawdata', c_void_p),

    ('queue', ListBase),  # ListBase
    ('handlers', ListBase),  # ListBase
    ('modalhandlers', ListBase),  # ListBase

    ('subwindows', ListBase),  # ListBase
    ('gesture', ListBase),  # ListBase
]


class wmOperatorType(Structure):
    """source/blender/windowmanager/WM_types.h: 515"""
    _fields_ = [
        ('name', c_char_p),
        ('idname', c_char_p),
        ('translation_context', c_char_p),
        ('description', c_char_p),
    ]


class wmOperator(Structure):
    """source/blender/makesdna/DNA_windowmanager_types.h: 341"""
    pass

wmOperator._fields_ = [
    ('next', POINTER(wmOperator)),
    ('prev', POINTER(wmOperator)),

    ('idname', c_char * 64),
    ('properties', c_void_p),  # IDProperty

    ('type', POINTER(wmOperatorType)),  # wmOperatorType
    ('customdata', c_void_p),
    ('py_instance', c_void_p),

    ('ptr', c_void_p),  # PointerRNA
    ('reports', c_void_p),  # ReportList

    ('macro', ListBase),
    ('opm', POINTER(wmOperator)),
    ('layout', c_void_p),  # uiLayout
    ('flag', c_short),
    ('pad', c_short * 3)
]


class wmEventHandler(Structure):
    """source/blender/windowmanager/wm_event_system.h: 45"""
    pass

wmEventHandler._fields_ = [
    ('next', POINTER(wmEventHandler)),
    ('prev', POINTER(wmEventHandler)),  # struct wmEventHandler

    ('type', c_int),
    ('flag', c_int),

    ('keymap', c_void_p),
    ('bblocal', c_void_p),
    ('bbwin', c_void_p),  # const rcti

    ('op', POINTER(wmOperator)),
    ('op_area', c_void_p),  # struct ScrArea
    ('op_region', c_void_p),  # struct ARegion

    # /* ui handler */
    # wmUIHandlerFunc ui_handle;          /* callback receiving events */
    # wmUIHandlerRemoveFunc ui_remove;    /* callback when handler is removed */
    # void *ui_userdata;                  /* user data pointer */
    # struct ScrArea *ui_area;            /* for derived/modal handlers */
    # struct ARegion *ui_region;          /* for derived/modal handlers */
    # struct ARegion *ui_menu;            /* for derived/modal handlers */
    #
    # /* drop box handler */
    # ListBase *dropboxes;
]


def print_modal_handlers(context):
    window = context.window
    addr = window.as_pointer()
    ptr = c_void_p(addr)
    win = ctypes.cast(ptr, POINTER(wmWindow)).contents

    handlers = []

    ptr = ctypes.cast(win.modalhandlers.first, POINTER(wmEventHandler))
    while ptr:
        handler = ptr.contents
        handlers.append(handler)
        ptr = handler.next

    print('Modal Handlers: {}'.format(window))
    for handler in handlers:
        if handler.op:
            ot = handler.op.contents.type
            print(handler, ot.contents.idname)
        else:
            print(handler)
    return handlers


print_modal_handlers(bpy.context)