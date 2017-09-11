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


def idprop_to_py(prop):
    if isinstance(prop, list):
        return [idprop_to_py(p) for p in prop]
    elif hasattr(prop, "to_dict"):
        return prop.to_dict()
    elif hasattr(prop, "to_list"):
        return prop.to_list()
    else:
        return prop


class Registerable:
    _users = 0

    @classmethod
    def register_class(cls, rename=False):
        import re
        if issubclass(cls, bpy.types.Operator):
            mod, func = cls.bl_idname.split(".")
            class_name = mod.upper() + "_OT_" + func
        elif issubclass(cls, bpy.types.Menu):
            class_name = cls.bl_idname
        else:
            class_name = cls.__name__
        if rename:
            if cls._users == 0 or not hasattr(bpy.types, class_name):
                while hasattr(bpy.types, class_name):
                    base, num = re.match("([a-zA-Z_]+)(\d*)$", func).groups()
                    if num == "":
                        func = base + "0"
                    else:
                        func = base + str(int(num) + 1)
                    class_name = mod.upper() + "_OT_" + func
                cls.bl_idname = mod + "." + func
                bpy.utils.register_class(cls)
                cls._users = 1
            else:
                print("{} already registered".format(cls))
        else:
            if hasattr(bpy.types, class_name):
                getattr(bpy.types, class_name)._users += 1
            else:
                bpy.utils.register_class(cls)
                cls._users = 1

    @classmethod
    def unregister_class(cls, force=False):
        if issubclass(cls, bpy.types.Operator):
            mod, func = cls.bl_idname.split(".")
            class_name = mod.upper() + "_OT_" + func
        elif issubclass(cls, bpy.types.Menu):
            class_name = cls.bl_idname
        else:
            class_name = cls.__name__
        if hasattr(bpy.types, class_name):
            other_cls = getattr(bpy.types, class_name)
            if other_cls._users > 0:
                other_cls._users -= 1
            if force:
                other_cls._users = 0
            if other_cls._users == 0:
                if other_cls.is_registered:
                    bpy.utils.unregister_class(other_cls)
        # else:
        #     bpy.utils.unregister_class(cls)  # 例外を出させるため
