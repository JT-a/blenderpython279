bl_info = {
    "name": "Snippet System for Text Editor",
    "author": "CoDEmanX",
    "version": (1, 0),
    "blender": (2, 67, 0),
    "location": "Text Editor (> Templates) > Snippets",
    "description": "Create snippets from text selection easily",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"}

import bpy
from os.path import isfile, sep, exists, basename
from os import makedirs, remove

user_snippets = bpy.utils.user_resource('SCRIPTS') + "snippets" + sep


class TEXT_OT_snippet_load(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "text.snippet_load"
    bl_label = "Insert Snippet"

    filepath = bpy.props.StringProperty(name="Filepath", subtype='FILE_PATH')

    @classmethod
    def poll(cls, context):
        # context.area.type == 'TEXT_EDITOR'
        return bpy.ops.text.insert.poll()

    def execute(self, context):
        if self.filepath and isfile(self.filepath):
            file = open(self.filepath, "r")
            bpy.ops.text.insert(text=file.read())

            # places the cursor at the end without scrolling -.-
            # context.space_data.text.write(file.read())
            file.close()
        return {'FINISHED'}


class TEXT_OT_snippet_save(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "text.snippet_save"
    bl_label = "Save Snippet"

    name = bpy.props.StringProperty(name="Name")
    # TODO: where to store?!

    @classmethod
    def poll(cls, context):
        text = context.space_data.text
        return (context.area.type == 'TEXT_EDITOR' and
                text is not None and not
                (text.current_line == text.select_end_line and
                 text.current_character == text.select_end_character))

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name")
        col = layout.column(True)
        col.label("Note that special chars will be replaced ", icon='INFO')
        col.label("and a sequence number added if necessary.", icon='BLANK1')

    def execute(self, context):
        name = bpy.path.clean_name(self.name).lower()
        ext = ".py"

        if not exists(user_snippets):
            makedirs(user_snippets)

        out = user_snippets + name + ext
        if isfile(out):
            for i in range(2, 100):
                out = user_snippets + name + "_" + str(i) + ext
                if not isfile(out):
                    break
            else:
                self.report('ERROR', "Couldn't save snippet, try a different name!")
                return {'CANCELLED'}

        try:
            file = open(out, "w")
            file.write(get_selected_text(context.space_data.text))
            file.close()
        except:
            self.report({'ERROR'}, "Couldn't save to file.")
        else:
            self.report({'INFO'}, "Saved as " + basename(out))
        finally:
            return {'FINISHED'}


class TEXT_OT_snippet_delete(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "text.snippet_delete"
    bl_label = "Delete Snippet"

    filepath = bpy.props.StringProperty(name="Filepath", subtype='FILE_PATH')

    def execute(self, context):

        snippet_paths = bpy.utils.script_paths("snippets")

        if (not self.filepath or not self.filepath.endswith(".py")
                or not isfile(self.filepath) or not
                any(self.filepath.startswith(p) for p in snippet_paths)
            ):
            self.report({'WARNING'}, "Invalid path to snippet.")
            return({'CANCELLED'})

        try:
            remove(self.filepath)
        except:
            self.report({'ERROR'}, "Couldn't delete file.")
        else:
            self.report({'INFO'}, "Deleted " + basename(self.filepath))
        finally:
            return {'FINISHED'}

# Code by Dalai Felinto


def get_selected_text(text):
    """"""
    current_line = text.current_line
    select_end_line = text.select_end_line

    current_character = text.current_character
    select_end_character = text.select_end_character

    # if there is no selected text return None
    if current_line == select_end_line:
        if current_character == select_end_character:
            return None
        else:
            return current_line.body[min(current_character, select_end_character):max(current_character, select_end_character)]

    text_return = None
    writing = False
    normal_order = True  # selection from top to bottom

    for line in text.lines:
        if not writing:
            if line == current_line:
                text_return = current_line.body[current_character:] + "\n"
                writing = True
                continue
            elif line == select_end_line:
                text_return = select_end_line.body[select_end_character:] + "\n"
                writing = True
                normal_order = False
                continue
        else:
            if normal_order:
                if line == select_end_line:
                    text_return += select_end_line.body[:select_end_character]
                    break
                else:
                    text_return += line.body + "\n"
                    continue
            else:
                if line == current_line:
                    text_return += current_line.body[:current_character]
                    break
                else:
                    text_return += line.body + "\n"
                    continue

    return text_return


class TEXT_MT_snippet_delete(bpy.types.Menu):
    bl_label = "Delete Snippet"
    bl_idname = "TEXT_MT_snippet_delete"

    def draw(self, context):
        self.path_menu(bpy.utils.script_paths("snippets"),
                       "text.snippet_delete",
                       #{"internal": True},
                       )


class TEXT_MT_snippets(bpy.types.Menu):
    bl_label = "Snippets"
    bl_idname = "TEXT_MT_snippets"

    def draw(self, context):
        self.layout.operator("text.snippet_save", icon='ZOOMIN')
        self.layout.menu("TEXT_MT_snippet_delete", icon='ZOOMOUT')
        prop = self.layout.operator("wm.path_open", text="Open folder", icon='FILE_FOLDER')
        prop.filepath = user_snippets
        self.layout.separator()
        self.path_menu(bpy.utils.script_paths("snippets"),
                       "text.snippet_load",
                       #{"internal": True},
                       )


def draw_item(self, context):
    layout = self.layout
    layout.menu(TEXT_MT_snippets.bl_idname)


class DrawFuncStore:
    bpy_type = "TEXT_HT_header"
    bpy_type_class = getattr(bpy.types, bpy_type)
    draw = None


def insert_menu():
    insert_after = 'row.menu("TEXT_MT_templates")'
    insert_code  = '        row.menu("TEXT_MT_snippets")\n' \
                   '        from bpy.app.translations import pgettext_iface as iface_\n'  # meh...
    DrawFuncStore.draw = DrawFuncStore.bpy_type_class.draw
    # module = bpy_type_class.__module__

    filepath = DrawFuncStore.bpy_type_class.draw.__code__.co_filename
    if filepath == "<string>":
        return
    try:
        file = open(filepath, "r")
        lines = file.readlines()
    except:
        append_menu()
        return

    line_start = DrawFuncStore.bpy_type_class.draw.__code__.co_firstlineno - 1

    for i in range(line_start, len(lines)):
        line = lines[i]
        if not line[0].isspace() and line.lstrip()[0] not in ("#", "\n", "\r"):
            break

    line_end = i

    # Unindent draw func by one level, since it won't sit inside a class
    lines = [l[4:] for l in lines[line_start:line_end]]

    for i, line in enumerate(lines, 1):
        if insert_after in line:
            # print("FOUND INSERT LINE")
            lines.insert(i, insert_code)
            break
    else:
        append_menu()
        return

    # Debug output
    # f = open("D:\\s.txt", "w").writelines(lines)

    l = {}
    exec("".join(lines), {}, l)
    # print(l)

    # bpy_type_class.draw.__code__ = code_object # Doesn't work, since a single func is not a module

    DrawFuncStore.bpy_type_class.draw = l['draw']  # exec defined our custom draw() func!


def append_menu():
    bpy.types.TEXT_MT_templates.prepend(draw_item)


def remove_menu():
    if DrawFuncStore.draw is not None:
        DrawFuncStore.bpy_type_class.draw = DrawFuncStore.draw
        DrawFuncStore.draw = None

    else:
        bpy.types.TEXT_MT_templates.remove(draw_item)


def register():
    bpy.utils.register_module(__name__)
    insert_menu()


def unregister():
    bpy.utils.unregister_module(__name__)
    remove_menu()
if __name__ == "__main__":
    register()

    # The menu can also be called from scripts
    # bpy.ops.wm.call_menu(name=CustomMenu.bl_idname)
