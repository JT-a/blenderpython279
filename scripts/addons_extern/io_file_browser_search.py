# file_brower_search.py Copyright (C) 2012, Jakub Zolcik
#
# Relaxes selected vertices while retaining the shape as much as possible
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "File Browser Search",
    "author": "Jakub Zolcik",
    "version": (0, 1, 1),
    "blender": (2, 6, 2),
    "api": 35622,
    "location": "File Browser",
    "description": "Allows You to find files in File Browser by name.",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/User:Sftd/Extensions:2.6/Py/Scripts/Import-Export/File_Browser_Search",
    "tracker_url": "http://projects.blender.org/tracker/?func=detail&aid=30386&group_id=153&atid=467",
    "category": "Import-Export"}

"""
Usage:

Launches in File Browser

"""

import bpy
import os
import re


class FilteredFileItem(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="File name", default="")
    dname = bpy.props.StringProperty(name="Display name", default="")


def fileSearch(self, context):

    # print("file")

    filter = context.window_manager.filtered_search_prop
    directory = context.window_manager.last_directory_prop

    filecol = context.window_manager.filtered_files_prop

    for fname in filecol:
        filecol.remove(0)

    if filter == "":
        return None

    pattern = ""

    special = ('\\', '.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '|', '(', ')')

    for c in special:
        filter = filter.replace(c, '\\' + c)

    if ('*' in filter):
        filter = filter.replace('\*', '.*')
        pattern = ('^' + filter.lower() + '$')
    else:
        if(len(filter) < 3):
            pattern = ('^' + filter.lower() + r".*\..*" + '$')
        else:
            pattern = ('^' + r".*" + filter.lower() + r".*\..*" + '$')
    prog = re.compile(pattern)

    maxf = 100
    cf = 0
    dlen = len(directory)

    maxd = 100
    cd = 0

    if context.window_manager.file_searchtree:
        for path, dirs, files in os.walk(directory):
            cd += 1
            if cd > maxd:
                break
            for filename in files:
                filename = (os.path.join(path, filename))[dlen:]
                # rfilename = (os.path.join(path, filename))[dlen:]
                if prog.match(filename.lower()) != None:
                    p = context.window_manager.filtered_files_prop.add()
                    # p.name = rfilename
                    p.name = filename
                    if context.blend_data.scenes[0].file_hideextensions:
                        ind = filename.rfind(".")
                        if ind > -1:
                            filename = filename[0:ind]
                    p.dname = filename
                    cf += 1
                if(cf >= maxf):
                    break
            if(cf >= maxf):
                break

    else:
        filesList = os.listdir(directory)
        for filename in filesList:
            if prog.match(filename.lower()) != None:
                p = context.window_manager.filtered_files_prop.add()
                p.name = filename
                if context.blend_data.scenes[0].file_hideextensions:
                    ind = filename.rfind(".")
                    if ind > -1:
                        filename = filename[0:ind]
                p.dname = filename

    return None


def blendDataFromFile(file, part):
    with bpy.data.libraries.load(file) as (data_from, data_to):
        if (part == "Action"):
            return data_from.actions
        elif part == "Armature":
            return data_from.brushes
        elif part == "Brush":
            return data_from.brushes
        elif part == "Camera":
            return data_from.cameras
        elif part == "Curve":
            return data_from.curves
        elif part == "Font":
            return data_from.fonts
        elif part == "Group":
            return data_from.groups
        elif part == "Image":
            return data_from.images
        elif part == "Lamp":
            return data_from.lamps
        elif part == "Lattice":
            return data_from.lattices
        elif part == "Library":
            return data_from.libraries
        elif part == "FreestyleLineStyle":
            return data_from.linestyles
        elif part == "Mask":
            return data_from.masks
        elif part == "Material":
            return data_from.materials
        elif part == "Mesh":
            return data_from.meshes
        elif part == "NodeTree":
            return data_from.node_groups
        elif part == "Object":
            return data_from.objects
        elif part == "Particle":
            return data_from.particles
        elif part == "Scene":
            return data_from.scenes
        elif part == "Screen":
            return data_from.screens
        elif part == "Script":
            return data_from.scripts
        elif part == "Sound":
            return data_from.sounds
        elif part == "Speaker":
            return data_from.speakers
        elif part == "Text":
            return data_from.texts
        elif part == "Texture":
            return data_from.textures
        elif part == "World":
            return data_from.worlds
        else:
            return None


def notFileSearch(self, context):

    # print("not file")

    filter = context.window_manager.filtered_search_prop
    directory = context.window_manager.last_directory_prop

    filecol = context.window_manager.filtered_files_prop

    for fname in filecol:
        filecol.remove(0)

    if filter == "":
        return None

    ind_e = directory.find(".blend")

    if(ind_e == -1):
        return None

    ind_e = ind_e + 6

    file = directory[0:ind_e]

    part = directory[ind_e + 1:-1]

    if (part == ""):
        return None

    data = None

    data = blendDataFromFile(file, part)

    pattern = ""
    if(len(filter) < 3):
        pattern = (filter.lower() + r".*")
    else:
        pattern = (r".*" + filter.lower() + r".*")
    prog = re.compile(pattern)

    for name in data:
        if prog.match(name.lower()) != None:
            p = context.window_manager.filtered_files_prop.add()
            p.name = name
            p.dname = name

    return None


def filteredSearchFunc(self, context):

    if(context.active_operator.bl_idname == "WM_OT_link_append"):
        return notFileSearch(self, context)
    else:
        return fileSearch(self, context)


class FilteredFileSelectOperator(bpy.types.Operator):
    bl_idname = "file.filtered_file_select"
    bl_label = "Select File"

    fname = bpy.props.StringProperty()
    fexec = bpy.props.BoolProperty()

    def execute(self, context):
        context.space_data.params.filename = self.fname
        if self.fexec:
            bpy.ops.file.execute('INVOKE_DEFAULT')
        return {'FINISHED'}


class FilteredSearchPanel(bpy.types.Panel):

    bl_idname = "FILE_PT_filteredsearch"

    bl_label = "Search:"

    bl_space_type = 'FILE_BROWSER'

    bl_region_type = 'CHANNELS'

    @classmethod
    def poll(cls, context):
        return (context.space_data.params is not None)

    def draw(self, context):

        layout = self.layout

        directory = context.space_data.params.directory

        if context.window_manager.last_directory_prop != directory:
            context.window_manager.last_directory_prop = directory
            filteredSearchFunc(self, context)

        layout.prop(context.window_manager, "filtered_search_prop", "")
        box = layout.box()
        length = len(context.window_manager.filtered_files_prop)
        incolumn = int(length / context.blend_data.scenes[0].file_columnsnumber)
        r = length % context.blend_data.scenes[0].file_columnsnumber
        row = box.row()
        col = row.column()
        it = 0
        tr = 0

        for f in context.window_manager.filtered_files_prop:
            op = col.operator("file.filtered_file_select", text=f.dname, emboss=False)
            op.fname = f.name
            op.fexec = context.blend_data.scenes[0].file_autoexecute
            it += 1
            if tr < r:
                if it % (incolumn + 1) == 0:
                    tr += 1
                    if(it < length):
                        col = row.column()
            else:
                if (it - tr) % incolumn == 0:
                    if(it < length):
                        col = row.column()

        layout.prop(context.blend_data.scenes[0], "file_autoexecute")
        layout.prop(context.window_manager, "file_searchtree")
        layout.prop(context.blend_data.scenes[0], "file_hideextensions")
        layout.prop(context.blend_data.scenes[0], "file_columnsnumber")


def register():

    bpy.utils.register_module(__name__)

    bpy.types.WindowManager.filtered_search_prop = bpy.props.StringProperty(update=filteredSearchFunc)
    bpy.types.WindowManager.last_directory_prop = bpy.props.StringProperty()
    bpy.types.Scene.file_autoexecute = bpy.props.BoolProperty(name="Open Automatically", default=True)
    bpy.types.Scene.file_hideextensions = bpy.props.BoolProperty(name="Hide Extensions", update=filteredSearchFunc)
    bpy.types.WindowManager.file_searchtree = bpy.props.BoolProperty(name="Search Subdirectories", update=filteredSearchFunc)
    bpy.types.Scene.file_columnsnumber = bpy.props.IntProperty(name="Number of Columns", default=2, min=1, max=15, update=filteredSearchFunc)
    bpy.types.WindowManager.filtered_files_prop = bpy.props.CollectionProperty(type=FilteredFileItem)


def unregister():

    del bpy.types.WindowManager.filtered_search_prop
    del bpy.types.WindowManager.last_directory_prop
    del bpy.types.Scene.file_autoexecute
    del bpy.types.WindowManager.filtered_files_prop
    del bpy.types.WindowManager.file_searchtree
    del bpy.types.Scene.file_hideextensions
    del bpy.types.Scene.file_columnsnumber

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
