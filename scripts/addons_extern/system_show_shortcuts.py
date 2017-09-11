# -*- coding: utf8 -*-
# #  #  #  #  # BEGIN GPL LICENSE BLOCK #  #  #  #  #  #
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE..... See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# #  #  #  #  # END GPL LICENSE BLOCK #  #  #  #  #

# <pep8 compliant>

bl_info = {
    "name": "Show Shortcuts",
    "author": "Yardie (Greg Dickson)",
    "version": (1, 5, 4),
    "blender":
        (2, 7, 2),
    "location":
        "[Cmd+Shft+F1] User Prefs -> Input -> Window -> Show Shortcut Keys",
    "description":
        "Shows the currently active and enabled shortcuts in a popup.",
    "wiki_url": "https://github.com/Yardie-/show_shortcuts/wiki",
    "tracker_url": "http://blenderartists.org/forum/showthread.php?347589",
    "category": "System"}
import bpy
# import os
import string
import textwrap
# from datetime import datetime, date
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty
from bpy.types import Operator, AddonPreferences
from bpy_extras import keyconfig_utils
from bpy.app.translations import pgettext_tip as translate_

# Last release update
# 13 October 2014 7:37:53 AM AWST
# Last dev update
# 13 October 2014 7:37:44 AM AWST
# import pprint
DEBUG = False
# TODO
# Make a menu to show list of grouped keymaps
# Show Global shortcuts like Alt + A Seems to work everywhere
# needs to group shortcuts by identical shortcuts
# maybe duplicate a keymap-item then remove only the shortcut sections call sections
# solve error RNA Warning: Current value "0" matches no enum in 'GROUP_OT_objects_remove', '(null)', 'group'
# self.idname_py()
"""
add a pie menu for groups

ideally this will
list items by name
onmouse over of the name will show the
    keycombo
    alternative
    tooltip lines
each being a call to the full description popup
"""


def get_description(op_class):
    """Get the description of the Call this with C name not python name."""
    descr = ""
    if op_class:
        descr = op_class.bl_rna.description
        if not descr:
            descr = op_class.__doc__
        if not descr and hasattr(op_class, 'bl_label'):
            descr = op_class.bl_label
        if not descr and hasattr(op_class, 'name'):
            descr = op_class.name
    if not descr:
        return ""
    return translate_(descr) + "."


def kmi_compare_props(keymap_item_a, keymap_item_b):
    """Compare 2 keymap items if they have the same properties
        they are effectively the same just are alternative key combos.
        """
    # differs by keymap_item.properties.??
    # call menu -> name
    # context_enum -> data_path
    a_rna = getattr(keymap_item_a, 'properties', None)
    b_rna = getattr(keymap_item_b, 'properties', None)
    for a_prop in dir(a_rna):
        if not a_prop.startswith("_") and a_prop not in {"bl_rna", "rna_type"}:
            if getattr(a_rna, a_prop, False) != getattr(b_rna, a_prop, False):
                return False
    return True


def execute_string(opname):
    if not opname.startswith("bpy.ops."):
        opname = "bpy.ops." + opname
    op_name = opname.split(".", 4)
    op = getattr(getattr(bpy.ops, op_name[2]), op_name[3])
    if op.poll():
        return op()  # exec operator


def poll_op(opname):
    if not opname.startswith("bpy.ops."):
        opname = "bpy.ops." + opname
    op_name = opname.split(".", 4)
    op = getattr(getattr(bpy.ops, op_name[2]), op_name[3])
    if op.poll():
        return True
    if DEBUG:
        print("!!! Poll Failed for", op)
    return False


def map_operator_from_shortcut(op, op_class, keymap_item):
    for prop in dir(keymap_item.properties):
        if (prop in op_class.bl_rna.properties and
                not prop.startswith("_") and
                prop not in {"bl_rna", "rna_type", ""}):
            if (op_class.bl_rna.properties[prop].type == 'ENUM' and
                    len(op_class.bl_rna.properties[prop].enum_items) == 0):
                continue
            attr = getattr(keymap_item.properties, prop, None)
            if (op_class.bl_rna.properties[prop].type == 'ENUM' and
                    attr not in op_class.bl_rna.properties[prop].enum_items):
                continue
            if hasattr(op, prop) and getattr(op, prop) != attr:
                try:
                    setattr(op, prop, attr)
                except AttributeError:
                    pass
    return op


# def find_keymap(lookfor):
#    found = None
#    return found


def eval_attr(object, name):
    resolved = object
    for o in name.split("."):
        resolved = getattr(resolved, o)
    return resolved


def nice_text(punc):
    """Convert the ugly string name into the actual character
    Stolen from node_effciency_tools adapted to user prefs"""
    user_prefs = get_user_prefs()
    pairs = (
        ('LEFTMOUSE', "Left Mouse"),
        ('MIDDLEMOUSE', "Middle Mouse"),
        ('RIGHTMOUSE', "Right Mouse"),
        ('SELECTMOUSE', "Select Mouse"),
        ('ACTIONMOUSE', "Action Mouse"),
        ('WHEELUPMOUSE', "Wheel Up"),
        ('WHEELDOWNMOUSE', "Wheel Down"),
        ('WHEELINMOUSE', "Wheel In"),
        ('WHEELOUTMOUSE', "Wheel Out"),
        ('LEFT_ARROW', user_prefs.leftarrow_text),
        ('RIGHT_ARROW', user_prefs.rightarrow_text),
        ('UP_ARROW', user_prefs.uparrow_text),
        ('DOWN_ARROW', user_prefs.downarrow_text),
        ('ZERO', "0"),
        ('ONE', "1"),
        ('TWO', "2"),
        ('THREE', "3"),
        ('FOUR', "4"),
        ('FIVE', "5"),
        ('SIX', "6"),
        ('SEVEN', "7"),
        ('EIGHT', "8"),
        ('NINE', "9"),
        ('OSKEY', "Cmd"),
        ('RET', "Return"),
        ('ESC', "Esc"),
        ('TAB', "Tab"),
        ('DEL', "Delete"),
        ('SEMI_COLON', ";"),
        ('PERIOD', "."),
        ('COMMA', ","),
        ('QUOTE', "\""),
        ('ACCENT_GRAVE', "`"),
        ('MINUS', "-"),
        ('BACK_SLASH', "\\"),
        ('EQUAL', "="),
        ('LEFT_BRACKET', "("),
        ('RIGHT_BRACKET', ")"),
        ('LINE_FEED', "Return"),
        ('SLASH', "/"),
        ('BACK_SLASH', "\\"),
        ('EQUAL', "="),
        ('NDOF_ISO1', "NDOF Isometric 1"),
        ('NDOF_ISO2', "NDOF Isometric 2"),
        ('NUMPAD_PERIOD', "Numpad" + " ."),
        ('NUMPAD_SLASH', "Numpad" + " /"),
        ('NUMPAD_ASTERIX', "Numpad" + " *"),
        ('NUMPAD_MINUS', "Numpad" + " -"),
        ('NUMPAD_ENTER', "Numpad" + " Enter"),
        ('NUMPAD_PLUS', "Numpad" + " +"),
    )
    punc = punc.strip()
    nice_punc = False
    for (ugly, nice) in pairs:
        if punc == ugly:
            nice_punc = nice
            break
    if not nice_punc:
        nice_punc = punc.replace("_", " ").title().replace('Ccw', 'CCW').replace('Cw', 'CW').replace('Ndof', 'NDOF').replace('Ccw', 'CCW')

    # String replace ndof to NDOF Cw CW Ccw CCW then nearly all the NDOF strings will translate
    # NDOF_ISO1 -> NDOF Isometric 1
    return translate_(nice_punc)


def get_user_prefs():
    """simply returns the current prefs for this addon """
    return bpy.context.user_preferences.addons[__name__].preferences


def get_input_types():
    input_type = []
    addon_prefs = get_user_prefs()
    if addon_prefs.KEYBOARD:
        input_type.append('KEYBOARD')
    if addon_prefs.MOUSE:
        input_type.append('MOUSE')
    if addon_prefs.NDOF:
        input_type.append('NDOF')
    if addon_prefs.TWEAK:
        input_type.append('TWEAK')
    if addon_prefs.TEXTINPUT:
        input_type.append('TEXTINPUT')
    return input_type


def keymap_guess_opname(context, opname):
    """ Pythonised vesion of
        file blender/windowmanager/intern/wm_keymap.c
        My version also uses path to determine context
        - -  find in wm_keymap.c line 1413+
        ingroup wm
        Blender 2.71 will need to be kept up to date with that so
        I will try to make it as similar as possible
    #  /* Guess an appropriate keymap from the operator name */
    #  /* Needs to be kept up to date with Keymap and Operator naming */
    #  wmKeyMap *WM_keymap_guess_opname(const bContext *C, const char *opname)
    #  {
    #  ....wmKeyMap *km = NULL;
    #  /* Op types purposely skipped  for now:
     *     BRUSH_OT
     *     BOID_OT
     *     BUTTONS_OT
     *     CONSTRAINT_OT
     *     DPAINT_OT
     *     ED_OT
     *     FLUID_OT
     *     TEXTURE_OT
     *     UI_OT
     *     VIEW2D_OT
     *     WORLD_OT
     */
    """
    # km = False
    map = (
        # /* Window */
        ("WM_", "Window", 0, 0),
        # /* Screen & Render */
        ("SCREEN_", "Screen", 0, 0),
        ("RENDER_", "Screen", 0, 0),
        ("SOUND_", "Screen", 0, 0),
        ("SCENE_", "Screen", 0, 0),
        # /* Grease Pencil */
        ("GPENCIL_", "Grease Pencil", 0, 0),
        # /* Markers */
        ("MARKER_", "Markers", 0, 0),
        # /* Import/Export*/
        ("IMPORT_", "Window", 0, 0),
        ("EXPORT_", "Window", 0, 0),
        # /* 3D View */
        ("VIEW3D_", "3D View", context.space_data.type, 0),
        ("OBJECT__mode_set", "Object Non-modal", 0, 0),
        ("OBJECT_", "Object Mode", 0, 0),
        # /* Object mode related */
        ("GROUP_", "Object Mode", 0, 0),
        ("MATERIAL_", "Object Mode", 0, 0),
        ("PTCACHE_", "Object Mode", 0, 0),
        ("RIGIDBODY_", "Object Mode", 0, 0),
        # /* Editing Modes */
        ("MESH_",
            "Object Mode" if context.mode == 'OBJECT' else "Mesh", 0, 0),
        ("CURVE_",
            "Object Mode" if context.mode == 'OBJECT' else "Curve", 0, 0),
        ("SURFACE_",
            "Object Mode" if context.mode == 'OBJECT' else "Curve", 0, 0),
        ("ARMATURE_", "Armature", 0, 0),
        ("SKETCH_", "Armature", 0, 0),
        ("POSE_", "Pose", 0, 0),
        ("POSELIB_", "Pose", 0, 0),
        ("SCULPT_",
            "Sculpt" if context.mode == 'SCULPT' else "UV Sculpt", 0, 0),
        ("LATTICE_", "Lattice", 0, 0),
        ("PARTICLE_", "Particle", 0, 0),
        ("FONT_", "Font", 0, 0),
        ("PAINT__face_select", "Face Mask", 0, 0),
        ("PAINT_",
            "Weight Paint" if context.mode == 'PAINT_WEIGHT' else
            "Vertex Paint" if context.mode == 'PAINT_VERTEX' else
            "Image Paint" if context.mode == 'PAINT_TEXTURE' else None, 0, 0),
        # /* Timeline */
        ("TIME_", "Timeline", context.space_data.type, 0),
        # /* Image Editor */
        ("IMAGE_", "Image", context.space_data.type, 0),
        # /* Clip Editor */
        ("CLIP_", "Clip", context.space_data.type, 0),
        ("MASK_", "Mask Editing", 0, 0),
        # /* UV Editor */
        ("UV_", "UV Editor", context.space_data.type, 0),
        # /* Node Editor */
        ("NODE_", "Node Editor", context.space_data.type, 0),
        # /* Animation Editor Channels */
        ("ANIM__channels", "Animation Channels", context.space_data.type, 0),
        # /* Animation Generic - after channels */
        ("ANIM_", "Animation", 0, 0),
        # /* Graph Editor */
        ("GRAPH_", "Graph Editor", context.space_data.type, 0),
        # /* Dopesheet Editor */
        ("ACTION_", "Dopesheet", context.space_data.type, 0),
        # /* NLA Editor */
        ("NLA_", "NLA Editor", context.space_data.type, 0),
        # /* Script */
        ("SCRIPT_", "Script", context.space_data.type, 0),
        # /* Text */
        ("TEXT_", "Text", context.space_data.type, 0),
        # /* Sequencer */
        ("SEQUENCER_", "Sequencer", context.space_data.type, 0),
        # /* Console */
        ("CONSOLE_", "Console", context.space_data.type, 0),
        # /* Console */
        ("INFO_", "Info", context.space_data.type, 0),
        # /* File browser */
        ("FILE_", "File Browser", context.space_data.type, 0),
        # /* Logic Editor */
        ("LOGIC_", "Logic Editor", context.space_data.type, 0),
        # /* Outliner */
        ("OUTLINER_", "Outliner", context.space_data.type, 0),
        ("TRANSFORM_",
            "3D View" if context.space_data.type == 'VIEW_3D' else
            "Graph Editor" if context.space_data.type == 'GRAPH_EDITOR' else
            "Dopesheet" if context.space_data.type == 'DOPESHEET_EDITOR' else
            "NLA Editor" if context.space_data.type == 'NLA_EDITOR' else
            "UV Editor" if context.space_data.type == 'IMAGE_EDITOR' else
            "Node Editor" if context.space_data.type == 'NODE_EDITOR' else
            "Sequencer" if context.space_data.type == 'SEQUENCE_EDITOR' else None, context.space_data.type, 0),
    )
    # context.space_data.type ['EMPTY', 'VIEW_3D', 'TIMELINE', 'GRAPH_EDITOR', 'DOPESHEET_EDITOR', 'NLA_EDITOR', 'IMAGE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'TEXT_EDITOR',
    # 'NODE_EDITOR', 'LOGIC_EDITOR', 'PROPERTIES', 'OUTLINER', 'USER_PREFERENCES', 'INFO', 'FILE_BROWSER', 'CONSOLE'],
    # default 'EMPTY',
    # names in C are different than python """
    # the [0] returns just the first match
    # so "ANIM_OT_channels" being before "ANIM_OT" works == a switch statement
    for k, v, s, r in map:
        if opname.startswith(k):
            return (k, v, s, r)
    return (False, False, False, False)


def get_flat_keymap_hierarchy_as_dict():
    """ Recurse through the key map hierarchy and flatten it into one straight
        list in the correct vertical order
        bpy.type.KeyMap: (km.name, km.space_type, km.region_type, [...])"""
    result = {}

    def testEntry(entry, parent_space=""):
        idname, spaceid, regionid, children = entry
        if spaceid == 'EMPTY' and parent_space != "":
            spaceid = parent_space
        result[idname] = (spaceid, regionid)
        for child in children:
            testEntry(child, spaceid)
    for entry in keyconfig_utils.KM_HIERARCHY:
        testEntry(entry)
    return result


def check_context_keymap(context, keymap, km_hierarchy, addon_prefs):
    mode_ = mode_map(keymap.name)
    if (mode_ and context.mode != mode_):
        if DEBUG:
            print("!!! Keymap:", keymap.name, "not available in mode", context.mode)
        return False
    if DEBUG:
        print("Key map name =", keymap.name, "is available in", context.mode)
    entry = get_kmh_entry(keymap.name)
    idname = spaceid = regionid = children = False
    if entry:
        idname, spaceid, regionid, children = entry
        if ((keymap.name in km_hierarchy and km_hierarchy[keymap.name][0] == context.space_data.type) or
            (context.region.type == keymap.region_type and
                (keymap.space_type == context.space_data.type and
                    context.space_data.type == spaceid)) or
                (keymap.name == "Screen" and addon_prefs.show_screen) or
                (keymap.name.startswith("Anim") and addon_prefs.show_animation) or
                (keymap.name == "Frames" and addon_prefs.show_frames) or
                (keymap.name == "Grease Pencil" and addon_prefs.grease_pencil) or
                (keymap.name == "Markers" and addon_prefs.show_markers) or
                (keymap.name == "Window" and addon_prefs.show_window)):
            if DEBUG:
                print(">>> Context OK:", keymap.name)
            return True
    return False


def check_context_keymap_item(context, item):
    return False


def check_context_operator(context, op_name, km_hierarchy, addon_prefs, context_map=[]):
    op_prefix, space_name, region_id, dunno = keymap_guess_opname(context, op_name)
    context_map.append(context.space_data.type)
    mode_ = mode_map(space_name)
    if (mode_ and context.mode != mode_):
        return False
    if (addon_prefs.show_screen or
            addon_prefs.show_animation or
            addon_prefs.show_frames or
            addon_prefs.grease_pencil or
            addon_prefs.show_markers or
            addon_prefs.show_window):
        context_map.append('EMPTY')
    if space_name in km_hierarchy and km_hierarchy[space_name][0] in context_map:
        return True
    if DEBUG:
        print("!!! Operator:", op_name, "not available in context", context.area.type)
    return False


def squash_keymap_hierarchy():
    """ Recurse through the key map hierarchy and
        flatten it into one straight list in the correct vertical order
        bpy.type.KeyMap: (km.name, km.space_type, km.region_type, [...])
        if the space type is empty then assign the space type to
        that of the parent
    """
    result = {}

    def testEntry(entry, parent_space="EMPTY"):
        idname, spaceid, regionid, children = entry
        #    print (idname)
        if spaceid == 'EMPTY' and parent_space != "EMPTY":
            spaceid = parent_space
        result[idname] = (spaceid, regionid)
        for child in children:
            testEntry(child, spaceid)
    for entry in keyconfig_utils.KM_HIERARCHY:
        testEntry(entry)
    return result


def get_kmh_entry(k):
    for entry in keyconfig_utils.KM_HIERARCHY:
        idname, spaceid, regionid, children = entry
        if idname == k:
            return entry
    return False

# redundant see import line
# def translate(text):
#    txt = bpy.app.translations.pgettext_tip(text)
#    if txt != text:
#        return txt
#    return text


def mode_map(find_):
    return{
        "Pose": "POSE",
        "Object Mode": "OBJECT",
        "Paint Curve": "PAINT_CURVE",
        "Curve": "EDIT_CURVE",
        "Image Paint": "PAINT_TEXTURE",
        "Vertex Paint": "PAINT_VERTEX",
        "Weight Paint": "PAINT_WEIGHT",
        "Sculpt": "SCULPT",
        "Mesh": "EDIT_MESH",
        "Armature": "EDIT_ARMATURE",
        "Metaball": "EDIT_METABALL",
        "Lattice": "EDIT_LATTICE",
        "Particle": "PARTICLE"}.get(find_, False)


def get_available_keymaps(self, context, search_name=False):
    available_keymaps = {}
    location = ""
    # simple test for 3D View available
    if bpy.ops.view3d.select.poll():
        x, y, z = context.scene.cursor_location
        location = "x {:.1}, y {:.1}, z {:.1}".format(x, y, z)
    addon_prefs = get_user_prefs()
    show_window = addon_prefs.show_window
    show_screen = addon_prefs.show_screen
    mode = False
    km_hierarchy = squash_keymap_hierarchy()
    if DEBUG:
        print("Space type", context.space_data.type)
    for keymap in bpy.context.window_manager.keyconfigs.user.keymaps:
        # Remove region specific stuff and get the similar space type or empty
        # this should be possible in a straight table lookup but not sure how
        if not check_context_keymap(context, keymap, km_hierarchy, addon_prefs):
            continue
        for keymap_item in keymap.keymap_items:
            name = keymap_item.name
            if DEBUG:
                print("???", name)
            # ***************** move on if we are only called with one name
            if search_name and search_name != name:
                continue
            # some have no idname skip them also skip inactive
            if not keymap_item.active or not keymap_item.idname:
                continue
            if (keymap_item.map_type in get_input_types() and poll_op(keymap_item.idname)):
                if DEBUG:
                    print(">>> Available:", keymap_item.idname)
                # Only show the input types selected
                mod, opname = keymap_item.idname.split(".")
                idname_c = "{!s}_OT_{!s}".format(mod.upper(), opname)
                show_wm = False
                # ***************** move on if context is wrong
                if not check_context_operator(context, idname_c, km_hierarchy, addon_prefs, context_map=[]):
                    continue
                # TODO Needs to check mode for some ops
                description = ""
                # remove the Context Set Enum key items for now TODO reenable to get this working
                # if name.startswith('Context Set'):
                #    if DEBUG:
                #        print ("-> Fix Me! Skipping", name)
                #    continue
                # use the idname to check for Call Menu to allow for name changes in prefs
                op_map = keymap_guess_opname(context, idname_c)
                if op_map:
                    op = op_map[1]
                else:
                    op = False
                if keymap_item.idname == "wm.call_menu":
                    if hasattr(keymap_item.properties, "name"):
                        c_op = getattr(keymap_item.properties, "name")
                        if DEBUG:
                            print(keymap_item.idname, c_op)
                        if not check_context_operator(context, c_op, km_hierarchy, addon_prefs, ['INFO']):
                            continue
                        else:
                            description = get_description(getattr(bpy.types, c_op, False))
                            op_class = getattr(bpy.types, c_op, False)
                            pre, called = c_op.split("_MT_")
                            name = translate_("Call Menu") + " (" + called.replace('_', ' ').title() + ")"
                            # if op_class:
                            #    if (type(op_class.__doc__) is str and
                            #            len(op_class.__doc__.strip()) > 0):
                            #        if DEBUG:
                            #            description += "doc: "
                            #        description += translate_(op_class.__doc__) + ". "
                            #    if (type(op_class.bl_rna.description) is str and
                            #            len(op_class.bl_rna.description.strip()) > 0):
                            #        description += translate_(op_class.bl_rna.description) + ". "
                            #    if (type(op_class.bl_label) is str and
                            #            len(op_class.bl_label.strip()) > 0):
                            #        description += translate_(op_class.bl_label) + ". "
                # http://blenderartists.org/forum/showthread.php?348582-collect-quot-quot-quot-tooltips-quot-quot-quot-in-python&p=2726119&viewfull=1#post2726119
                # http://blenderartists.org/forum/showthread.php?348582-collect-quot-quot-quot-tooltips-quot-quot-quot-in-python&p=2726048&viewfull=1#post2726048
                if (op and
                    op in km_hierarchy and
                    (km_hierarchy[op][0] == context.space_data.type or
                        (op == "Object Mode" and context.mode is 'OBJECT') or
                        (op == "Screen" and addon_prefs.show_screen) or
                        (op.startswith("Anim") and addon_prefs.show_animation) or
                        (op == "Frames" and addon_prefs.show_frames) or
                        (op == "Markers" and addon_prefs.show_markers) or
                        (op == "Window" and addon_prefs.show_window))):
                    # and keymap.space_type != "EMPTY":
                    # now the final test
                    # print ("Operator = ", op, (op is "Window"))
                    op_class = getattr(bpy.types, idname_c)
                    # bpy.ops.wm.context_set_enum(data_path="", value="")
                    # bpy.ops.wm.call_menu(name="")
                    # If there is __doc__ info that should precede others
                    description = get_description(op_class)
                    #
                    # if (type(op_class.__doc__) is str and
                    #        len(op_class.__doc__.strip()) > 0):
                    #    # is str is not None and:
                    #    if DEBUG:
                    #        description += "doc: "
                    #    description += translate_(op_class.__doc__) + ". "
                    # if (type(op_class.bl_rna.description) is str and
                    #        len(op_class.bl_rna.description.strip()) > 0):
                    #    description += translate_(op_class.bl_rna.description) + ". "
                    # if len(description) > 0:
                    #    description = "\nTooltips\n" + description
                    args = []
                    props = ""
                    args_description = ""
                    refine = ""
                    for prop in dir(keymap_item.properties):
                        if (prop in op_class.bl_rna.properties and
                                not prop.startswith("_") and
                                prop not in {"bl_rna", "rna_type"}):
                            attr = getattr(keymap_item.properties, prop, False)
                            if DEBUG and attr:
                                args_description += "\n{} {} {!r}".format(prop, op_class.bl_rna.properties[prop].type, attr)
                            # RNA Warning: Current value "0" matches no enum in 'GROUP_OT_objects_remove', '(null)', 'group'
                            # if (op_class.bl_rna.properties[prop].type == 'ENUM' and
                            #        len(op_class.bl_rna.properties[prop].enum_items) == 0):
                            #    continue
                            property_description = getattr(op_class.bl_rna.properties[prop], "description", prop).strip()
                            if property_description == "":
                                property_description = nice_text(prop)
                            property_description = translate_(property_description)
                            # ________needs work to make Vectors and the like more readable
                            if attr:  # str(attr).strip() !="":
                                # might fix RNA Warning: Current value "0" matches no enum in 'GROUP_OT_objects_remove', '(null)', 'group'
                                if (op_class.bl_rna.properties[prop].type == 'ENUM' and
                                        attr not in op_class.bl_rna.properties[prop].enum_items):
                                    if DEBUG:
                                        print(attr, "not found in", prop)
                                    continue
                                if op_class.bl_rna.properties[prop].type == 'BOOLEAN':
                                    # A BOOLEAN that is False will not reach here as attr is False and dealt with above.
                                    args_description += "\n{}".format(property_description)
                                    refine += " (" + nice_text(prop) + ")"
                                # elif op_class.bl_rna.properties[prop].type == 'FLOAT':
                                #    args_description += "\n{} @ {}".format(
                                #        translate_(op_class.bl_rna.properties[prop].description),
                                #        ", ".join(map(str, getattr(keymap_item.properties, prop))))
                                elif prop == "location" and location != "":
                                    # po "3D cursor location"
                                    # args_description += op_class.bl_rna.properties[prop].type + "\n{:} set to {} {}.".format(op_class.bl_rna.properties[prop].description, attr[0], attr[0])
                                    args_description += "\nUsing current {}".format(property_description)
                                    # , location)
                                else:
                                    if (op_class.bl_rna.properties[prop].type == 'ENUM' and
                                            len(op_class.bl_rna.properties[prop].enum_items) > 0 and
                                            attr in op_class.bl_rna.properties[prop].enum_items):
                                        refine += " (" + nice_text(attr) + ")"
                                        enum_ = getattr(op_class.bl_rna.properties[prop].enum_items, attr, False)
                                        desc = False
                                        if enum_:
                                            desc = getattr(enum_, "description", False)
                                        if desc and len(desc.strip()) > 0:
                                            desc = desc.strip()
                                        else:
                                            desc = "{}".format(nice_text(attr))
                                        # attr in op_class.bl_rna.properties[prop].enum_items and
                                        #     op_class.bl_rna.properties[prop].enum_items[attr].description is not None and
                                        #     len(op_class.bl_rna.properties[prop].enum_items[attr].description.strip()) > 0):
                                        args_description += "\n{}: '{}'.".format(
                                            translate_(property_description),
                                            nice_text(desc))
                                    else:
                                        args_description += "\n{}: {}.".format(
                                            property_description,
                                            nice_text("{!r}".format(attr)))
                                    if op_class.bl_rna.properties[prop].type == 'INT' and prop == "delta":
                                        refine += " (" + nice_text(str(attr)) + ")"

                                # if attr != "":  # Would be cool to remove defaults if the keymap = default
                                args.append("{!s}={!r}".format(prop, attr))

                    if args_description != "":
                        # args_description = "\nSettings:\n" + args_description
                        description += args_description
                    # if description.find("editmode only") > 0:
                    #     name += " EDITONLY"
                    # continue

                    text_args = ",\n\t".join(args).strip()
                    args = ", ".join(args)
                    if len(args) > 0:
                        text_args = "\n\t" + text_args
                    function_call_text = "bpy.ops.{:}({:})".format(keymap_item.idname, text_args)
                    function_call = "bpy.ops.{:}({:})".format(keymap_item.idname, args)

                    modifiers = ""
                    if keymap_item.any:
                        modifiers = addon_prefs.any_text
                    else:
                        modifier_key = []
                        if keymap_item.shift:
                            modifier_key.append(addon_prefs.shft_text)
                        if keymap_item.ctrl:
                            modifier_key.append(addon_prefs.ctrl_text)
                        if keymap_item.alt:
                            modifier_key.append(addon_prefs.alt_text)
                        if keymap_item.oskey:
                            modifier_key.append(addon_prefs.oskey_text)
                        modifiers = " + ".join(modifier_key)
                    # sortable key for dict
                    if modifiers != "":
                        key_combo = " + ".join([modifiers, nice_text(keymap_item.type)])
                    else:
                        key_combo = nice_text(keymap_item.type)
                    """
                    TODO
                    Unique key for keymaps
                    This groups them by name as per visual expectation
                    and function to allow for alternative keys
                    needs to have menu_enum to work correctly
                    """
                    # if search_name:
                    #    sort_key = key_combo  # keymap_item.name + keymap_item.type + modifiers
                    #    print('line 610', sort_key)
                    # else:
                    sort_key = name + refine  # function_call
                    # key_combo = "[ " + key_combo + " ]"
                    # If there is already a keymap with the same name and
                    # function then add the key as an alternative only.
                    if sort_key in available_keymaps:
                        # TODO
                        if kmi_compare_props(keymap_item, available_keymaps[sort_key]['keymap_item']):
                            if (available_keymaps[sort_key]["alternate keys"].find(key_combo) == -1 and
                                    available_keymaps[sort_key]["key combo"] != key_combo):
                                prespace = "".ljust(len(translate_("Shortcut: %s")), " ")
                                available_keymaps[sort_key]["alternate keys"] += "{}\t{}\n".format(prespace, key_combo)
                        # if an existing description is empty but this one is not
                        # then use this one.
                        if (len(available_keymaps[sort_key]["description"]) == 0 and
                                len(description) > 0):
                            available_keymaps[sort_key]["description"] = description
                    else:
                        if key_combo != "None":
                            if sort_key in available_keymaps:
                                sort_key += " "  # add a space to the end to distinguish them
                                name += " "
                            #    modifiers += " + "
                            if description == name or description == "":
                                description = "{}:\n{}".format(translate_("Operator"), function_call)
                            available_keymaps[sort_key] = {
                                "name": name,
                                "refine": refine,
                                "idname": keymap_item.idname,
                                "key combo": key_combo,
                                "modifiers": modifiers,
                                "function call": function_call,
                                "function call text": function_call_text,
                                "description": description,
                                "alternate keys": "",
                                "region": keymap.region_type,
                                "space": keymap.space_type,
                                "keymap_item": keymap_item,
                                "op_class": op_class,
                                "is modal": keymap.is_modal,
                                "seen": 0,
                            }
    return available_keymaps
#                            # if the name occurs more than once make a menu flag
#                            seen[keymap_item.name] = {
#                                "seen": True,
#                                "sort_key": sort_key
#                            }
#                            scn = False
#                            if keymap_item.name in seen:
#                                scn = True
#                            seen[keymap_item.name] = {
#                                "seen": True,
#                                "sort_key": sort_key
#                            }


def get_biggest_window_dimensions():
    width = 0
    height = 0
    for i in range(len(bpy.context.window_manager.windows)):
        old_height = getattr(bpy.context.window_manager.windows[i], 'height')
        if old_height > height:
            height = old_height
        old_width = getattr(bpy.context.window_manager.windows[i], 'width')
        if old_width > width:
            width = old_width
    return [width, height]


# _________________________User Prefs
class ShowShortcutsPrefs(AddonPreferences):
    """User Prefs for Show Shortcuts Popup"""
    bl_idname = __name__
    filename_ext = ".html"
    check_existing = True
    out_dir = ""
    window_dim = get_biggest_window_dimensions()
    # Allow me for my hires screen
    import sys
    cmd_key = "Cmd"
    if sys.platform[:3] == "win":
        cmd_key = "Super"
    elif sys.platform == "darwin":
        cmd_key = "⌘"
    if DEBUG:
        divisor = 1
    else:
        divisor = 2
    show_run = BoolProperty(
        name="Show Run Button",
        default=False)
    show_function = BoolProperty(
        name="Show Operator",
        default=DEBUG)
    KEYBOARD = BoolProperty(
        name="Keyboard",
        default=True)
    TWEAK = BoolProperty(
        name="Tweak",
        default=True)
    MOUSE = BoolProperty(
        name="Mouse:",
        default=True)
    NDOF = BoolProperty(
        name="NDOF Device:",
        default=False)
    TEXTINPUT = BoolProperty(
        name="Text",
        default=False)
    TIMER = BoolProperty(
        name="Timer",
        default=False)
    show_window = BoolProperty(
        name="Window",
        default=True)
    show_animation = BoolProperty(
        name="Animation",
        default=DEBUG)
    show_markers = BoolProperty(
        name="Markers",
        default=DEBUG)
    show_frames = BoolProperty(
        name="Frames",
        default=DEBUG)
    show_screen = BoolProperty(
        name="Screen",
        default=DEBUG)
    grease_pencil = BoolProperty(
        name="Grease Pencil",
        default=DEBUG)
    popup_width = IntProperty(
        name="Width of the box",
        default=window_dim[0] // divisor,
        min=1,
        max=window_dim[0] * 2,
        step=10)
    info_width = IntProperty(
        name="Width of the box",
        default=window_dim[0] // 2,
        min=1,
        max=window_dim[0] * 2,
        step=10)
    popup_columns = IntProperty(
        name="Show column",
        default=3 if DEBUG else 2,
        min=1,
        max=6,
        step=1)
    characters_per_line = IntProperty(
        name="Characters",
        default=54,
        min=10,
        max=180,
        step=1)
    popup_infill = StringProperty(
        name="Button fill character",
        default=" ",
        maxlen=2)
    oskey_text = StringProperty(
        name="Command/Super key text.",
        default="⌘",
        maxlen=15)
    ctrl_text = StringProperty(
        name="Control",
        default="Ctl",
        maxlen=15)
    shft_text = StringProperty(
        name="Shift",
        default="Shft",
        maxlen=20)
    alt_text = StringProperty(
        name="Alt",
        default="Alt",
        maxlen=15)
    any_text = StringProperty(
        name="Any modifier",
        default="Any mod",
        maxlen=15)
    # numpad_text = StringProperty(
    #    name="Numpad",
    #    default="Numpad",
    #    maxlen=15)
    uparrow_text = StringProperty(
        name="Up arrow",
        default="↑",
        maxlen=15)
    downarrow_text = StringProperty(
        name="Down arrow",
        default=" ↓",
        maxlen=15)
    leftarrow_text = StringProperty(
        name="Left arrow",
        default="←",
        maxlen=15)
    rightarrow_text = StringProperty(
        name="Right arrow.",
        default="→",
        maxlen=15)

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=False)
        box1 = row.box()
        row = box1.row()
        row = row.split(.5)
        col = row.column()
        box = col.box()
        box.label(text="Input")
        box.prop(self, "KEYBOARD")
        box.prop(self, "MOUSE")
        box.prop(self, "NDOF")
        box.prop(self, "TWEAK")
        box.prop(self, "TEXTINPUT")
        box = col.box()
        box.label(text="Display Settings")
        # box.label(text="Preferences")
        #  box.prop(self, "show_wm")
        #  box.label(text="Character used to right justify button text.")
        #  row1= box.row()
        #  left = row1.split(.8)
        #  left.label("Maximum 2 characters")
        #  left.prop(self, "popup_infill", text = "")
        box.prop(self, "popup_width", slider=True)
        #  box.prop(self, "popup_height", slider=True)
        box.prop(self, "popup_columns", slider=True)
        box = col.box()
        box.label(text="Information")
        box.prop(self, "info_width", slider=True)
        box.prop(self, "characters_per_line", slider=True)
        # box.prop(self, "show_run")
        box.label(text="Python " + translate_("Tooltip:"))
        box.prop(self, "show_function")
        box = row.box()
        box.label(text="Key")
        row = box.row()
        left = row.split(.7)
        left.label(text="Operating system key pressed")
        row = box.row()
        left.prop(self, "oskey_text", text="")
        left = row.split(.7)
        left.label(text="Control key pressed")
        left.prop(self, "ctrl_text", text="")
        row = box.row()
        left = row.split(.7)
        left.label(text="Shift key pressed")
        left.prop(self, "shft_text", text="")
        row = box.row()
        left = row.split(.7)
        left.label(text="Alt key pressed")
        left.prop(self, "alt_text", text="")
        row = box.row()
        left = row.split(.7)
        left.label(text="Any modifier keys pressed")
        left.prop(self, "any_text", text="")
        # row = box.row()
        # left = row.split(.7)
        # left.label(text="Numpad")
        # left.prop(self, "numpad_text", text="")
        row = box.row()
        row.label(text="Arrows")
        row = box.row()
        left = row.split(.7)
        left.label(text="    " + translate_("Up"))
        left.prop(self, "uparrow_text", text="")
        row = box.row()
        left = row.split(.7)
        left.label(text="    " + translate_("Down"))
        left.prop(self, "downarrow_text", text="")
        row = box.row()
        left = row.split(.7)
        left.label(text="    " + translate_("Left"))
        left.prop(self, "leftarrow_text", text="")
        row = box.row()
        left = row.split(.7)
        left.label(text="    " + translate_("Right"))
        left.prop(self, "rightarrow_text", text="")
        box = box.box()
        box.label(text="Show:")
        row = box.row()
        row.prop(self, "show_window")
        row.prop(self, "show_screen")
        row = box.row()
        row.prop(self, "show_animation")
        row.prop(self, "show_markers")
        # row = box.row()
        # row.prop(self, "show_frames")
        # row.prop(self, "grease_pencil")
        layout.label(text="Current biggest window width is {:} and height is {:}".format(self.window_dim[0], self.window_dim[1]))


#  _______________________Info Popup______________________________________
class ShowShortcutsInfo(bpy.types.Operator):
    bl_idname = "screen.shortcut_info"
    bl_label = "Shortcut Information"
    bl_description = "Shortcut Information"
    #  bl_options={'INTERNAL'}
    show_info_on = bpy.props.StringProperty()
    info = bpy.props.StringProperty()
    #  bpy.utils.register_class(KeyMapItem)
    #  from bpy.types import KeyMapItem
    #  keymap_item =  bpy.props.CollectionProperty(type=bpy.types.KeyMapItem)

    def execute(self, context):
        return {'RUNNING_MODAL'}

#    def execute(self, context):
#        return context.window_manager.invoke_popup(self, width=get_user_prefs().info_width)
#        #  return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=get_user_prefs().info_width)
        # return self.execute(context)

    def draw(self, context):
        layout = self.layout
        paragraphs = self.info.expandtabs(3).split('\n')
        wrapped_lines = []
        for para in paragraphs:
            if len(para) > 0:
                # para = translate(para)
                # para = bpy.app.translations.pgettext_tip(para ,para)
                wrapped_lines.extend(textwrap.wrap(para, get_user_prefs().characters_per_line))
        for row in wrapped_lines:
            layout.label(row, translate=False)
        # for row in paragraphs:
        #     layout.label(row)


#  _________________________List of members within the same name group

class ShowShortcutGroup(bpy.types.Operator):
    bl_label = "Shortcuts"
    bl_idname = "screen.show_shortcut_group"
    keymaps = []
    description = "Tooltips"
    show_info_on = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.region is not None

    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        self.key_maps = get_available_keymaps(self, context)
        return context.window_manager.invoke_popup(self, width=get_user_prefs().popup_width)
        # return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(show_info_on)


#  _________________________Main Popup __________________________________
#  This will need to be the base which houses the menu list with all the shortcuts
#
#
class ShowShortcuts(bpy.types.Operator):
    """Show shortcuts available in the current context in a UI list."""
    bl_idname = "screen.show_shortcuts"
    bl_label = "Show Shortcut Keys"
    group_name = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return context.region is not None

    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        if self.group_name is not "":
            self.key_maps = get_available_keymaps(self, context, self.group_name)
        else:
            self.key_maps = get_available_keymaps(self, context)
        return context.window_manager.invoke_popup(self, width=get_user_prefs().popup_width)

    def draw(self, context):
        layout = self.layout
        #  layout.label("Blender {:} ".format(bpy.app.version_string))
        if len(self.key_maps) > 0:
            col = layout.box()
            r = col.row()
            if self.group_name is not "":
                r.label(translate_(self.group_name))
            else:
                note = "{} shortcuts for {} {}/{}. {:} :)"
                r.label(note.format(translate_("Active Operator"),
                                    translate_(nice_text(context.space_data.type)),
                                    translate_(nice_text(context.region.type)),
                                    translate_(nice_text(context.mode)),
                                    len(self.key_maps)))
            draw_list(self)
        else:
            layout.label("{} {} {}.".format(translate_("No Active Action"), nice_text(context.space_data.type), nice_text(context.region.type)))


# It only makes sense to show one instance of the same name initially
def make_name_list(key_maps):
    output = {}
    for key_info_key in sorted(key_maps):
        name = key_maps[key_info_key]["name"]
        # name += key_maps[key_info_key]["refine"]
        if name in output:
            output[name]["seen"] += 1
        else:
            output[name] = key_maps[key_info_key]
    return output


# group by name and function call
# need to add uniq element to name
# like Call Menu (Add)
def make_name_label_list(key_maps):
    output = {}
    for key_info_key in sorted(key_maps):
        name = key_maps[key_info_key]["name"]
        name += key_maps[key_info_key]["op_class"].bl_label
        if name in output:
            output[name]["seen"] += 1
        else:
            output[name] = key_maps[key_info_key]
    return output


def draw_list(self):
    user_prefs = get_user_prefs()
    layout = self.layout
    main_row = layout.row()
    # r = col.row()
    main_row.alignment = 'RIGHT'
    main_row.label(text="Show Info", icon='QUESTION')
    if self.group_name == "":
        main_row.label(text="Select Grouped", icon='RIGHTARROW_THIN')
        if user_prefs.show_run:
            main_row.label(text="Run Immediately!", icon='COLOR_GREEN')
    # layout.label("Click on a button to show the description.")
    # // equals floor division
    main_row = layout.row()
    col = main_row.box()
    if self.group_name is not "":
        key_maps = self.key_maps
    else:
        key_maps = make_name_list(self.key_maps)
    num_rows = (len(key_maps) // user_prefs.popup_columns)
    mod_char_count = 0
    #  go through each find the longest and pad the rest to that
    # left justify hack
    for key_info_key in key_maps:
        out = key_maps[key_info_key]
        old_mod_char_count = len(out["name"])
        if old_mod_char_count > mod_char_count:
            mod_char_count = old_mod_char_count
    i = 0
    for key_info_key in sorted(key_maps):
        out = key_maps[key_info_key]
        key_combo = translate_("Shortcut: %s") % "\t{}\n".format(out["key combo"])
        if out["alternate keys"] != "":
            key_combo += out["alternate keys"]
        description = "{}\n{}\n{}".format(out["name"], key_combo, out["description"])
        if user_prefs.show_function:
            #  add a line ?character long to seperate the description and the function call
            #  for i in range(1, user_prefs.characters_per_line):
            #    description += user_prefs.popup_infill
            description += "\n{}:\n{}".format(translate_("Operator"), out["function call text"])
        col.scale_x = 1.6
        r = col.row()
        if out["seen"] > 1:
            # Seen multiple time so show menu
            # operator (string, (never None)) – Identifier of the operator
            # property (string, (never None)) – Identifier of property in operator
            op = r.operator(
                ShowShortcuts.bl_idname,
                text=out["name"],
                icon='RIGHTARROW_THIN').group_name = out["name"]
            # op = r.menu(
            #    ShowShortcutsMenu.bl_idname,
            #    text=" " + out["name"].ljust(mod_char_count, " "),
            #    icon='RIGHTARROW_THIN').show_info_on = out["name"]
        else:
            if self.group_name is "":
                txt = " " + out["name"].ljust(mod_char_count, " ")
            else:
                txt = " " + (out["name"] + out["refine"]).ljust(mod_char_count, " ")
            op = r.operator(
                ShowShortcutsInfo.bl_idname,
                text=txt,
                icon='QUESTION')
            op.info = description
            # op.bl_description = out["key combo"] # can't assign this here
            op.show_info_on = out["name"]
            # TODO call menu for a group COLLAPSEMENU FILE_TICK
            # use r.c menu(menu, text="", text_ctxt="", translate=True, icon='RIGHTARROW_THIN')
            #  Disable run button for modal Mouse Tweak and NDOF keymaps they don't make sense to use
            #        self.group_name is "" and
            if (user_prefs.show_run and
                    not out["is modal"] and
                    out["keymap_item"].map_type not in {'MOUSE', 'NDOF', 'TWEAK'}):
                run_button = r.operator(out["idname"], text="", icon='COLOR_GREEN')
                run_button = map_operator_from_shortcut(op, out["op_class"], out["keymap_item"])
            # ####
            #  op.keymap_item = out["keymap_item"]
            #  Add a single entry enum with all the info you want or a list with Keys: Alternative: Etc: or just catch the mouse over stuff
            #  layout.operator_menu_enum("object.constraint_add", "type", text="Add Constraint" )
        i += 1
        if i > num_rows:
            i = 0
            col = main_row.box()


addon_keymaps = []


def register():
    bpy.utils.register_module(__name__)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(
        name='Window',
        space_type='EMPTY',
        region_type='WINDOW')
    kmi = km.keymap_items.new(
        "screen.show_shortcuts",
        'F1',
        'PRESS',
        oskey=True,
        shift=True,)
    addon_keymaps.append(km)


def unregister():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
