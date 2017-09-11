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

from ._misc import Registerable

iface = bpy.app.translations.pgettext_iface


def _get_base_class(cls):
    for base in cls.__bases__:
        if issubclass(base, bpy.types.bpy_struct):
            return base
    return None


class OperatorShowClassDetails(Registerable, bpy.types.Operator):
    bl_idname = "wm.addonprefs_show_class_details"
    bl_label = "Show Class Details"
    bl_description = ""
    bl_options = {'REGISTER', 'INTERNAL'}

    WIDTH = 1000

    module = bpy.props.StringProperty()
    id_value = bpy.props.StringProperty()

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        classes = bpy.utils._bpy_module_classes(
            self.module, is_registered=True)
        for c in classes:
            if id(c) == int(self.id_value):
                break
        else:
            return

        base = _get_base_class(c)

        def indent(layout):
            sp = layout.split(0.05)
            sp.row()
            return sp.row()
        layout = self.layout
        row = layout.row()
        col1 = row.column()
        col1.alignment = 'LEFT'
        col2 = row.column()

        if base:
            col1.label(iface("Type") + ":", translate=False)
            col2.label(base.__name__, translate=False)
        col1.label(iface("RNA Name") + ":", translate=False)
        col2.label(c.bl_rna.name, translate=False)
        if hasattr(c, "bl_idname"):
            idname = getattr(c, "bl_idname")
            if idname != c.bl_rna.name:
                col1.label(iface("ID Name") + ":", translate=False)
                col2.label(idname, translate=False)
        col1.label(iface("Label") + ":", translate=False)
        col2.label(getattr(c, "bl_label", ""))
        col1.label(iface("Description") + ":", translate=False)
        col2.label(getattr(c, "bl_description", ""))
        if issubclass(c, bpy.types.Operator):
            col1.label(iface("Options") + ":", translate=False)
            col2.label(str(getattr(c, "bl_options", {'REGISTER'})),
                       translate=False)

    def invoke(self, context, event):
        wm = context.window_manager
        width = min(context.window.width, self.WIDTH)
        return wm.invoke_popup(self, width=width)


class AddonClasses:
    owner_class = None

    show_classes = bpy.props.BoolProperty(
        name='Show Classes',
    )

    def draw(self, context, layout, box=True):
        if not self.show_classes:
            return

        if box:
            col = layout.column().box()
        else:
            col = layout.column()

        row = col.row()

        # NOTE: register可能なクラスはRNA_def_struct_register_funcs()で
        #       regメンバに代入しているもの
        # registerable_classes = [
        #     bpy.types.AddonPreferences,
        #     bpy.types.Panel,
        #     bpy.types.UIList,
        #     bpy.types.Menu,
        #     bpy.types.Header,
        #     bpy.types.Operator,
        #     bpy.types.Macro,
        #     bpy.types.KeyingSetInfo,
        #     bpy.types.RenderEngine,
        #     bpy.types.PropertyGroup,
        #     bpy.types.Node,
        #     bpy.types.NodeCustomGroup,
        #     bpy.types.ShaderNode,
        #     bpy.types.CompositorNode,
        #     bpy.types.TextureNode,
        #     bpy.types.NodeSocket,
        #     bpy.types.NodeSocketInterface,
        #     bpy.types.NodeTree,
        # ]
        classes = []
        for c in self.owner_class._classes_[self.name]:
            if not c.is_registered:
                continue
            name = c.bl_rna.name
            base = _get_base_class(c)
            classes.append((c, name, base))
        classes.sort(key=lambda x: (getattr(x[2], "__name__", ""), x[1]))

        split = row.split(0.2)
        col1 = split.column()
        col_ = split.split(0.5)
        col2 = col_.column()
        col3 = col_.column()
        for class_type, class_name, base_class in classes:
            col1.label(base_class.__name__, translate=False)
            col2.label(class_type.bl_rna.name, translate=False)
            row = col3.row()
            txt = getattr(class_type, "bl_label", "")
            if not isinstance(txt, str):
                txt = ""
            row.label(txt)

            op = row.operator(OperatorShowClassDetails.bl_idname, text="",
                              icon="INFO", emboss=False)
            op.module = self.owner_class.bl_idname.split(".")[0]
            op.id_value = str(id(class_type))

    @classmethod
    def new_class(cls, owner_class):
        namespace = {
            "owner_class": owner_class,
        }
        return type("AddonClasses",
                    (cls, bpy.types.PropertyGroup),
                    namespace)

    @classmethod
    def init_collection(cls):
        addon_prefs = cls.owner_class.get_instance()
        info_classes = addon_prefs.info_classes
        if "" not in info_classes:
            item = info_classes.add()
            item.name = ""
        mod_names = [mod.__name__.split(".")[-1]
                     for mod in cls.owner_class._fake_submodules_.values()]
        for mod_name in mod_names:
            if mod_name not in info_classes:
                item = info_classes.add()
                item.name = mod_name
        for item in list(info_classes):
            if item.name != "" and item.name not in mod_names:
                info_classes.remove(info_classes.find(item.name))

    @classmethod
    def register(cls):
        classes = [
            OperatorShowClassDetails
        ]
        for c in classes:
            c.register_class()

    @classmethod
    def unregister(cls):
        classes = [
            OperatorShowClassDetails
        ]
        for c in classes[::-1]:
            c.unregister_class()
