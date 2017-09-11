from time import time
import bpy


bl_info = {
    'name': 'Leader Key',
    'location': ('Add shortcut to ui.leaderkey '
                 'or access through search menu.'),
    'description': 'Vim like <leader> key functionality for blender',
    'author': 'Adam Wolski(miniukof@gmail.com)',
    'wiki_url': 'https://github.com/miniukof/bl-leader_key',
    'version': (0, 0, 1),
    'blender': (2, 76, 11),
    'category': 'Development',
}


# Haven't found good way for dynamically creating settings in user-prefs.
# So on start create fixed number of properties.
BINDINGS_MAX = 25


# All of the events that can be used when writing Key String for bindings.
EVENTS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
          'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'ZERO',
          'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT',
          'NINE', 'LEFT_CTRL', 'LEFT_ALT', 'LEFT_SHIFT', 'RIGHT_ALT',
          'RIGHT_CTRL', 'RIGHT_SHIFT', 'OSKEY', 'GRLESS', 'ESC', 'TAB', 'RET',
          'SPACE', 'LINE_FEED', 'BACK_SPACE', 'DEL', 'SEMI_COLON', 'PERIOD',
          'COMMA', 'QUOTE', 'ACCENT_GRAVE', 'MINUS', 'SLASH', 'BACK_SLASH',
          'EQUAL', 'LEFT_BRACKET', 'RIGHT_BRACKET', 'LEFT_ARROW', 'DOWN_ARROW',
          'RIGHT_ARROW', 'UP_ARROW', 'NUMPAD_2', 'NUMPAD_4', 'NUMPAD_6',
          'NUMPAD_8', 'NUMPAD_1', 'NUMPAD_3', 'NUMPAD_5', 'NUMPAD_7',
          'NUMPAD_9', 'NUMPAD_PERIOD', 'NUMPAD_SLASH', 'NUMPAD_ASTERIX',
          'NUMPAD_0', 'NUMPAD_MINUS', 'NUMPAD_ENTER', 'NUMPAD_PLUS', 'F1',
          'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
          'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'PAUSE', 'INSERT',
          'HOME', 'PAGE_UP', 'PAGE_DOWN', 'END', 'MEDIA_PLAY', 'MEDIA_STOP',
          'MEDIA_FIRST', 'MEDIA_LAST', 'TEXTINPUT', 'WINDOW_DEACTIVATE',
          'TIMER', 'TIMER0', 'TIMER1', 'TIMER2', 'TIMER_JOBS',
          'TIMER_AUTOSAVE', 'TIMER_REPORT', 'TIMERREGION', 'NDOF_MOTION',
          'NDOF_BUTTON_MENU', 'NDOF_BUTTON_FIT', 'NDOF_BUTTON_TOP',
          'NDOF_BUTTON_BOTTOM', 'NDOF_BUTTON_LEFT', 'NDOF_BUTTON_RIGHT',
          'NDOF_BUTTON_FRONT', 'NDOF_BUTTON_BACK', 'NDOF_BUTTON_ISO1',
          'NDOF_BUTTON_ISO2', 'NDOF_BUTTON_ROLL_CW', 'NDOF_BUTTON_ROLL_CCW',
          'NDOF_BUTTON_SPIN_CW', 'NDOF_BUTTON_SPIN_CCW', 'NDOF_BUTTON_TILT_CW',
          'NDOF_BUTTON_TILT_CCW', 'NDOF_BUTTON_ROTATE', 'NDOF_BUTTON_PANZOOM',
          'NDOF_BUTTON_DOMINANT', 'NDOF_BUTTON_PLUS', 'NDOF_BUTTON_MINUS',
          'NDOF_BUTTON_ESC', 'NDOF_BUTTON_ALT', 'NDOF_BUTTON_SHIFT',
          'NDOF_BUTTON_CTRL', 'NDOF_BUTTON_1', 'NDOF_BUTTON_2',
          'NDOF_BUTTON_3', 'NDOF_BUTTON_4', 'NDOF_BUTTON_5', 'NDOF_BUTTON_6',
          'NDOF_BUTTON_7', 'NDOF_BUTTON_8', 'NDOF_BUTTON_9', 'NDOF_BUTTON_10',
          'NDOF_BUTTON_A', 'NDOF_BUTTON_B', 'NDOF_BUTTON_C']

CTYPE_ENUM = [('VIEW_3D', 'VIEW_3D', ''),
              ('TIMELINE', 'TIMELINE', ''),
              ('GRAPH_EDITOR', 'GRAPH_EDITOR', ''),
              ('DOPESHEET_EDITOR', 'DOPESHEET_EDITOR', ''),
              ('NLA_EDITOR', 'NLA_EDITOR', ''),
              ('IMAGE_EDITOR', 'IMAGE_EDITOR', ''),
              ('SEQUENCE_EDITOR', 'SEQUENCE_EDITOR', ''),
              ('CLIP_EDITOR', 'CLIP_EDITOR', ''),
              ('TEXT_EDITOR', 'TEXT_EDITOR', ''),
              ('NODE_EDITOR', 'NODE_EDITOR', ''),
              ('LOGIC_EDITOR', 'LOGIC_EDITOR', ''),
              ('PROPERTIES', 'PROPERTIES', ''),
              ('OUTLINER', 'OUTLINER', ''),
              ('USER_PREFERENCES', 'USER_PREFERENCES', ''),
              ('INFO', 'INFO', ''),
              ('FILE_BROWSER', 'FILE_BROWSER', ''),
              ('CONSOLE', 'CONSOLE', ''),
              ('All', 'All', '')]

CMODE_ENUM = [('EDIT_MESH', 'EDIT_MESH', ''),
              ('EDIT_CURVE', 'EDIT_CURVE', ''),
              ('EDIT_SURFACE', 'EDIT_SURFACE', ''),
              ('EDIT_TEXT', 'EDIT_TEXT', ''),
              ('EDIT_ARMATURE', 'EDIT_ARMATURE', ''),
              ('EDIT_METABALL', 'EDIT_METABALL', ''),
              ('EDIT_LATTICE', 'EDIT_LATTICE', ''),
              ('POSE', 'POSE', ''),
              ('SCULPT', 'SCULPT', ''),
              ('PAINT_WEIGHT', 'PAINT_WEIGHT', ''),
              ('PAINT_VERTEX', 'PAINT_VERTEX', ''),
              ('PAINT_TEXTURE', 'PAINT_TEXTURE', ''),
              ('PARTICLE', 'PARTICLE', ''),
              ('OBJECT', 'OBJECT', ''),
              ('All', 'All', '')]

KEYSTR_DESC = ('String of characters to be used as key binding. For ex: '
               '"A B C" would mean that after pressing leader key pressing'
               ' in A, B, C keys in sequence would lead to calling bound '
               'function. You can use all the keys that blender outputs in '
               'event.type, except mouse movement:\n{}'
               ).format(' '.join(EVENTS))
FUNC_DESC = 'Function to be used by this key binding.'
CTYPE_DESC = 'Type of area in which this key binding is to be used in.'
CMODE_DESC = 'Mode in which this key binding is to be used in.'


class LeaderKey(bpy.types.Operator):
    """Main function call"""
    bl_idname = 'ui.leaderkey'
    bl_label = 'Launch leader key'

    # Timer from blender so modal method updates on 'TIMER' events
    _timer = None
    key_string = ''
    timeout = 0
    timenext = 0
    timestart = 0
    binding = None

    def execute(self, context):
        return self.invoke(context, None)

    def invoke(self, context, event):
        addon_prefs = context.user_preferences.addons[__name__].preferences
        self.key_string = ''
        self.timeout = addon_prefs.timeout
        self.timenext = addon_prefs.time_for_next
        self.bindings = Bindings()
        for i in range(addon_prefs.bindings_number):
            exec(('self.bindings.append({0}.kstr{1},'
                  '{0}.func{1}, {0}.ctype{1}, {0}.cmode{1})'
                  ).format('addon_prefs', i))
        self.timestart = time()
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.001, context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'ESC':
            context.area.header_text_set()
            return {'CANCELLED'}
        if event.type in EVENTS and event.value == 'PRESS':
            self.key_string += event.type + ' '

        # Go through possible functions trying different contexts.
        # Try first with current context and then try to find functions
        # that are correct for all contexts.
        func = self.bindings.get(kstr=self.key_string,
                                 ctype=context.area.type,
                                 cmode=context.mode)
        if not func:
            func = self.bindings.get(kstr=self.key_string,
                                     ctype='All',
                                     cmode=context.mode)
        if not func:
            func = self.bindings.get(kstr=self.key_string,
                                     ctype=context.area.type,
                                     cmode='All')
        if not func:
            func = self.bindings.get(kstr=self.key_string,
                                     ctype='All',
                                     cmode='All')

        context.area.header_text_set(self.key_string)

        if func and (time() - self.timestart) >= self.timenext:
            exec(func)
            context.area.header_text_set()
            return {'FINISHED'}

        if (time() - self.timestart) >= self.timeout:
            context.area.header_text_set()
            return {'FINISHED'}

        return {'RUNNING_MODAL'}


class Bindings:
    """Class containing all the bindings."""
    _bindings = {}

    def append(self,
               kstr,
               func,
               ctype='All',
               cmode='All'):
        """
        Append binding for key combination string 'kstr' and bind it with
        function 'func'.
        Constrain that binding to context_area_type 'ctype' and context_mode
        'cmode'
        """
        # Blenders event.type has all the keys in upper case.
        kstr = kstr.upper().strip()
        if self._bindings.get(ctype):
            if self._bindings[ctype].get(cmode):
                self._bindings[ctype][cmode][kstr] = func
            else:
                self._bindings[ctype][cmode] = {kstr: func}
        else:
            self._bindings[ctype] = {cmode: {kstr: func}}

    def get(self, kstr, ctype='All', cmode='All'):
        """
        Get function for key_string 'kstr' bound by context type and mode:
        'ctype', 'cmode'
        """
        try:
            return self._bindings[ctype][cmode][kstr.upper().strip()]
        except KeyError:
            return None


class LeaderKeyPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    timeout = \
        bpy.props.FloatProperty(name="Timeout",
                                description=("Amount of time for typing keys. "
                                             "In seconds."),
                                default=1.0,
                                soft_min=0.01)

    time_for_next = \
        bpy.props.FloatProperty(name="Wait for next",
                                description=("Amount of time for which to wait"
                                             " for next key if matching key is"
                                             " already found. In seconds."),
                                default=0.5,
                                soft_min=0.01)

    # This one should deal with both creating and displaying set number of
    # bindings, but couldn't get all values to initialize at same time.
    bindings_number = bpy.props.IntProperty(name="Bindings number",
                                            default=1,
                                            soft_min=1,
                                            soft_max=BINDINGS_MAX)

    # Preinitialize all the bindings. This ideally should be bound by
    # bindings_number but couldn't get it to work.
    for i in range(BINDINGS_MAX):
        exec(('kstr{}'
              ' = bpy.props.StringProperty(name="Key String",'
              'description=KEYSTR_DESC)').format(i))
        exec(('func{}'
              ' = bpy.props.StringProperty(name="Function",'
              'description=FUNC_DESC)').format(i))
        exec(('ctype{}'
              ' = bpy.props.EnumProperty(items=CTYPE_ENUM,'
              'name="Context area type",'
              'description=CTYPE_DESC,'
              'default="All")').format(i))
        exec(('cmode{}'
              ' = bpy.props.EnumProperty(items=CMODE_ENUM,'
              'name="Context mode",'
              'description=CTYPE_DESC,'
              'default="All")').format(i))

    def draw(self, context):
        layout = self.layout
        layout.label(text="Leader Key Preferences")
        layout.prop(self, "bindings_number")
        layout.prop(self, "timeout")
        layout.prop(self, "time_for_next")
        for i in range(self.bindings_number):
            layout.label(text="Binding {}".format(i))
            layout.prop(self, "kstr{}".format(i))
            layout.prop(self, "func{}".format(i))
            row = layout.row()
            row.prop(self, "ctype{}".format(i))
            row.prop(self, "cmode{}".format(i))


def register():
    bpy.utils.register_class(LeaderKeyPreferences)
    bpy.utils.register_class(LeaderKey)


def unregister():
    bpy.utils.unregister_class(LeaderKey)
    bpy.utils.unregister_class(LeaderKeyPreferences)
