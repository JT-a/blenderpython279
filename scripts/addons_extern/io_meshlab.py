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

bl_info = {
    "name": "MeshLab Applink",
    "author": "Joel Daniels",
    "version": (0, 1),
    "blender": (2, 67, 1),
    "location": "Properties > Scene",
    "description": "Export selected object to MeshLab for decimation and re-import",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}


import bpy
from subprocess import Popen
import os
from extensions_framework import util as efutil


def realpath(path):
    return os.path.realpath(efutil.filesystem_path(path))

original_objects = []

#-------------------------------------------


class SCENE_OT_MLExport(bpy.types.Operator):
    bl_idname = "export_applink.meshlab"
    bl_label = "Export to MeshLab"
    bl_description = "Export selected objects to MeshLab."
    bl_options = {'UNDO'}

    def execute(self, context):
        scene = context.scene

        export_path = realpath(scene.ML_export_path)
        if not os.path.exists(export_path):
            os.mkdir(export_path)
        print("Exporting mesh to ", export_path)
        # save list of original objects for later
        global original_objects
        for i in bpy.context.selected_objects:
            original_objects.append(i.name)

        # MeshLab executable path
        ML_exec_path = scene.ML_exec_path
        obj_export_name = os.path.join(export_path, context.object.name) + '.obj'
        bpy.ops.export_scene.obj(filepath=obj_export_name, use_selection=True, use_mesh_modifiers=True, use_edges=True, use_normals=True, use_materials=True, path_mode='ABSOLUTE')

        # commands for opening MeshLab
        args = (ML_exec_path, obj_export_name)

        try:
            Popen(args, cwd=export_path, bufsize=-1, shell=False)
        except PermissionError:
            self.report({'INFO'}, "Darn. Couldn't open MeshLab.")
            pass

        return {'FINISHED'}

#-------------------------------------------


class SCENE_OT_MLImport(bpy.types.Operator):
    bl_idname = "import_applink.meshlab"
    bl_label = "Import from MeshLab"
    bl_description = "Import selected objects from MeshLab."
    bl_options = {'UNDO'}

    def execute(self, context):
        import_path = realpath(scene.ML_export_path)

        import_obj = ""
        for obj in os.listdir(import_path):
            if obj[-4:] == '.obj':
                import_obj = obj
                break

        import_objs = os.path.join(import_path, import_obj)

        # move the object to the last render layer rather than deleting,
        # in case the operations in ML didn't go as expected
        bpy.ops.object.move_to_layer(layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))

        bpy.ops.import_scene.obj(filepath=import_obj)

        return {'FINISHED'}

#----------------------------------------------


class SCENE_OT_Delete_Orig(bpy.types.Operator):
    bl_idname = "del_orig.meshlab"
    bl_label = "Delete Original Objects"
    bl_description = "Delete the original high poly objects from the scene."
    bl_options = {'UNDO'}

    def execute(self, context):
        for object in scene.objects:
            object.select = False
        for obj in original_objects:
            if bpy.data.objects[obj] in list(bpy.data.objects):
                print('deleting ', bpy.data.objects[obj])
                bpy.data.objects[obj].select = True
            bpy.ops.object.delete()

        import_path = realpath(scene.ML_export_path)

        # clean-up
        for i in os.listdir(import_path):
            os.remove(import_path + '\\' + i)

        return {'FINISHED'}

#--------------------------------------


class SCENE_PT_MLPanel(bpy.types.Panel):
    bl_idname = "MeshLab_Panel"
    bl_label = "MeshLab Import - Export"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Export the mesh to MeshLab:")
        layout.operator("export_applink.meshlab", icon='MESHLAB')

        split = layout.split()
        col = split.column()
        col.label(text="Import the mesh from MeshLab:")
        col.operator("import_applink.meshlab", icon='BLENDER')

        col = split.column()
        col.label(text="Delete original meshes:")
        col.operator("del_orig.meshlab", icon='CANCEL')

        layout.separator()
        layout.prop(scene, "ML_exec_path")
        layout.prop(scene, "ML_export_path")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.ML_exec_path = bpy.props.StringProperty(name="MeshLab Path", subtype="FILE_PATH")
    bpy.types.Scene.ML_export_path = bpy.props.StringProperty(name="MeshLab Export Path", subtype="DIR_PATH")


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
