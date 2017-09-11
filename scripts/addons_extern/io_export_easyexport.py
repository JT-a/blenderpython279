bl_info = {
    "name": "Easy Export Panel",
    "description": "Adds a panel to the toolbar for easy exporting to .obj and .fbx. Includes batch functionality.",
    "author": "Digital-Joe",
    "version": (1, 0),
    "blender": (2, 76, 0),
    "location": "View3D > Toolbar > Easy Export Panel",
    "wiki_url": "",
    "category": "Import-Export",
}

import bpy

# AddPresetBase is used to access blender's standard function for Operator Presets
from bl_operators.presets import AddPresetBase
from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
    EnumProperty,
)
from bpy.types import Menu, Panel, UIList
import os

panelLabel = "Easy Export"  # used to set all UI elements inside the same panel

#------------------
# Scene Properties
#------------------
# Properties are variables that can be used to draw the UI using 'layout.' or accessed from an operator
# By using 'bpy.types.scene.' these properties are saved in the scene

#-----------
# Booleans
#-----------
bpy.types.Scene.sel_only = BoolProperty(
    description="Export selected objects only",
    default=True
)

bpy.types.Scene.apply_mods = BoolProperty(
    description="Apply Modifiers",
    default=True
)

bpy.types.Scene.write_smooth = BoolProperty(
    description="Write sharp edges as smooth groups",
    default=False
)

bpy.types.Scene.write_normals = BoolProperty(
    description="Write Normals",
    default=True
)

bpy.types.Scene.include_uv = BoolProperty(
    description="Include active UV coordinates",
    default=True
)

bpy.types.Scene.write_mat = BoolProperty(
    description="Write materials to .mtl file",
    default=True
)

bpy.types.Scene.triangulate = BoolProperty(
    description="Triangulate faces",
    default=False
)

bpy.types.Scene.objname_is_filename = BoolProperty(
    description="Set the object name as the file name",
    default=True
)

bpy.types.Scene.write_baked_anim = BoolProperty(
    description="Write baked animations",
    default=False
)

bpy.types.Scene.write_anim = BoolProperty(
    description="Export keyframe animations",
    default=True
)

bpy.types.Scene.batch = BoolProperty(
    description="Batch export",
    default=False
)

bpy.types.Scene.folder_per_file = BoolProperty(
    description="Create a seperate folder for each file",
    default=False
)

bpy.types.Scene.folder_per_scene = BoolProperty(
    description="Create a seperate folder for each file",
    default=True
)

bpy.types.Scene.path_is_project_folder = BoolProperty(
    description="Save to project folder",
    default=False
)

#---------
# Strings
#---------
bpy.types.Scene.filepath = StringProperty(
    # Using 'subtype' blender can recognize the purpose of 'special' strings
    # A directory in this case
    subtype="FILE_PATH",
    # default = bpy.path.abspath("//")
)

bpy.types.Scene.savedir = StringProperty(
    subtype="FILE_PATH",
)

bpy.types.Scene.filename = StringProperty(
    default="filename"
)

bpy.types.Scene.scenename = StringProperty(
    default="scenename"
)

bpy.types.Scene.currentSceneName = StringProperty()
#----------
# Floats
#----------
bpy.types.Scene.export_scale = FloatProperty(
    default=1.0
)

#--------------
# Enumerators
#--------------
# item -> (identifier, name, description)
bpy.types.Scene.file_format = EnumProperty(
    items=(('obj', ".obj", "Wavefront obj"),
           ('BIN7400', ".fbx - 7.4 binary", "Autodesk fbx, Version 7.4 Binary"),
           ('ASCII6100', ".fbx - 6.1 ASCII", "Autodesk fbx, Version 6.1 ASCII")
           ),
    default='obj',
)

bpy.types.Scene.axis_up = EnumProperty(
    items=(('X', "X Axis", ""),
           ('Y', "Y Axis", ""),
           ('Z', "Z Axis", ""),
           ('-X', "-X Axis", ""),
           ('-Y', "-Y Axis", ""),
           ('-Z', "-Z Axis", ""),
           ),
    default='Y',
)

bpy.types.Scene.axis_forward = EnumProperty(
    items=(('X', "X Axis", ""),
           ('Y', "Y Axis", ""),
           ('Z', "Z Axis", ""),
           ('-X', "-X Axis", ""),
           ('-Y', "-Y Axis", ""),
           ('-Z', "-Z Axis", ""),
           ),
    default='-Z',
)

bpy.types.Scene.object_types = EnumProperty(
    options={'ENUM_FLAG'},
    items=(('EMPTY', "Empty", ""),
           ('CAMERA', "Camera", ""),
           ('LAMP', "Lamp", ""),
           ('ARMATURE', "Armature", ""),
           ('MESH', "Mesh", ""),
           ('OTHER', "Other", ""),
           ),
    description="Types of objects to export",
    default={'EMPTY', 'CAMERA', 'LAMP', 'ARMATURE', 'MESH', 'OTHER'},
)

bpy.types.Scene.mesh_smooth_type = EnumProperty(
    items=(('OFF', "Normals (default)", "Write normals smoothing"),
           ('FACE', "Face", "Write face smoothing"),
           ('EDGE', "Edge", "Write edge smoothing"),
           ),
    description="Smoothing export",
    default='FACE',
)

bpy.types.Scene.batch_mode = EnumProperty(
    items=(('OBJECT', "Object", "Export objects to seperate files"),
           ('GROUP', "Group", "Export groups to seperate files"),
           ('SCENE', "Scene", "Export scenes to seperate files"),
           ('SCENE_OBJECT', "Scene object", "Export all objects from all scenes seperately"),
           ),
    description="Choose what to create the seperate files of",
    default='OBJECT',
)

#----------------
# Panel Class
#----------------
# Create the panel in the toolbar of the 3D View
# Shortcut "t"


class View3DPanel:
    bl_space_type = 'VIEW_3D'  # Draw in the 3D View
    bl_region_type = 'TOOLS'  # Draw in the Toolbar

#-------------
# Custom I/O
#-------------
# Create a collapseable panel in the specified toolbar tab


class CustomExportPanel(View3DPanel, Panel):
    bl_label = "Easy Export"  # Panel label
    bl_context = "objectmode"  # The panel is only accesible when in object mode
    bl_category = panelLabel  # Draw the panel in the parent panel

    # Draw the panel
    def draw(self, context):
        scene = bpy.context.scene
        obj = scene.objects.active
        layout = self.layout
        savePath = bpy.path.abspath("//")
        # '.prop' automatically draws the correct UI element based on the input property type
        # '.operator' draws a button calling the specified operator
        # '.menu' draws a menu based on a class

        row = layout.column_flow(align=True).row(align=True)
        row.menu("Presets_Menu", text="Presets")
        row.operator("ct.preset_add", text="", icon='ZOOMIN')
        row.operator("ct.preset_delete", text="", icon='ZOOMOUT')
        layout.separator()

        layout.prop(scene, "file_format", text="File Format")
        layout.separator()

        # Context sensitive layout
        layout.label("Format specific options", icon='TRIA_RIGHT')
        if scene.file_format == 'obj':
            layout.prop(scene, "write_smooth", text="Write Smooth Groups")
            layout.prop(scene, "write_normals", text="Write Normals")
            layout.prop(scene, "include_uv", text="Include UV's")
            layout.prop(scene, "write_mat", text="Write Materials")

        elif scene.file_format == 'BIN7400' or 'ASCII6100':
            layout.prop(scene, "object_types")
            layout.prop(scene, "write_anim", text="Export keyframe animations")
            layout.prop(scene, "write_baked_anim", text="Export baked animations")
            layout.prop(scene, "mesh_smooth_type", text="Smoothing")
        layout.separator()

        layout.label("General options", icon='TRIA_RIGHT')
        layout.prop(scene, "sel_only", text="Selected only")
        layout.prop(scene, "apply_mods", text="Apply Modifiers")
        layout.prop(scene, "triangulate", text="Triangulate")
        if (scene.batch_mode == 'SCENE' and scene.batch == True) and scene.file_format == ('BIN7400' or 'ASCII6100'):
            layout.label("FBX triangulate only works for:", icon='ERROR')
            layout.label("- Object or Scene Object batch mode")

        layout.prop(scene, "axis_up", text="Up Axis")
        layout.prop(scene, "axis_forward", text="Forward Axis")
        layout.prop(scene, "export_scale", text="Scale")
        layout.prop(scene, "batch", text="Batch")
        if scene.batch == True:
            layout.prop(scene, "batch_mode", text="Batch Mode")
        if scene.batch_mode == 'GROUP' and scene.batch == True:
            layout.prop(scene, "objname_is_filename", text="File name is name of first obj in group")
        else:
            layout.prop(scene, "objname_is_filename", text="Object name is file name")
        if scene.objname_is_filename == False:
            if scene.batch == True:
                layout.label("Batch will add sequence number to name", icon='ERROR')
            layout.prop(scene, "filename", text="File name")
            if scene.filename == "":
                layout.label("Please set filename", icon='ERROR')
        if scene.batch_mode == "SCENE_OBJECT":
            layout.prop(scene, "folder_per_scene", text="Create a folder for each scene")
            layout.prop(scene, "folder_per_file", text="Create a subfolder for each object")
        else:
            layout.prop(scene, "folder_per_file", text="Create a folder for each file")
        layout.prop(scene, "path_is_project_folder", text="Save to project folder")
        if scene.path_is_project_folder == False:
            layout.prop(scene, "filepath", text="")
        if scene.filepath != "":
            layout.operator("ct.export_custom", text=CustomExport.bl_label, icon='EXPORT')
        else:
            layout.label("Please set export directory", icon='ERROR')

#-----------------
# Export Operator
#-----------------


class CustomExport(bpy.types.Operator):
    bl_idname = "ct.export_custom"  # Used to call the operator
    bl_label = "Export"  # Label to use in UI Button
    bl_options = {'PRESET'}
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        scene = bpy.context.scene
        obj = scene.objects.active
        selection = obj
        count = 1

        if scene.objname_is_filename == True:
            scene.filename = obj.name

        # Batch Export
        if scene.batch == True:

            # Object batch
            #####################################################
            if scene.batch_mode == 'OBJECT':
                # If selected only -> list only selected, otherwise list all visible objects
                if scene.sel_only == True:
                    selection = bpy.context.selected_objects
                else:
                    selection = bpy.context.visible_objects

                # Deselect all objects and set 'selection only' to true
                # Every object to be exported will be selected in the loop and exported seperately
                bpy.ops.object.select_all(action='DESELECT')
                scene.sel_only = True

                for obj in selection:
                    # Add sequence to name if != object name
                    if scene.objname_is_filename == False:
                        scene.filename += "_" + str(count)
                        count += 1
                    else:
                        scene.filename = obj.name

                    # Select the current object in the loop
                    obj.select = True
                    scene.objects.active = obj

                    # Create folder per file
                    SetSaveDir(scene)

                    # Run export operator
                    if scene.file_format == 'obj':
                        ExportOBJ(scene)

                    elif scene.file_format == 'BIN7400' or 'ASCII6100':
                        ExportFBX(scene, scene.file_format)

                    # Remove sequence from name
                    if scene.objname_is_filename == False:
                        scene.filename = scene.filename[0: len(scene.filename) - len(str(count)) - 1]

                    obj.select = False

                for obj in selection:
                    obj.select = True

            # Group batch
            #####################################################
            if scene.batch_mode == 'GROUP':
                # If selected only -> list only selected, otherwise list all visible objects
                if scene.sel_only == True:
                    selection = bpy.context.selected_objects
                    selected = bpy.context.selected_objects
                    for obj in selected:
                        bpy.ops.object.select_grouped(type='GROUP')
                        selection += selected
                else:
                    selection = bpy.context.visible_objects

                # Deselect all objects and set 'selection only' to true
                # Every object to be exported will be selected in the loop and exported seperately
                bpy.ops.object.select_all(action='DESELECT')
                scene.sel_only = True

                for obj in selection:
                    # Select the current object in the loop
                    obj.select = True
                    scene.objects.active = obj
                    bpy.ops.object.select_grouped(type='GROUP')
                    selected = bpy.context.selected_objects

                    # Add sequence to name if != object name
                    if scene.objname_is_filename == False:
                        scene.filename += "_" + str(count)
                        count += 1
                    else:
                        scene.filename = obj.name

                    # Create folder per file
                    SetSaveDir(scene)

                    # Run export operator
                    if scene.file_format == 'obj':
                        ExportOBJ(scene)

                    elif scene.file_format == 'BIN7400' or 'ASCII6100':
                        ExportFBX(scene, scene.file_format)

                    # Remove sequence from name
                    if scene.objname_is_filename == False:
                        scene.filename = scene.filename[0: len(scene.filename) - len(str(count)) - 1]

                    for obj in selected:
                        obj.select = False

                    for selected in selection:
                        selection.remove(selected)

                    print("SELECTION" + str(selection))
                    print("SELECTION" + str(selection))
                    print("SELECTION" + str(selection))

            # Scene batch
            #####################################################
            elif scene.batch_mode == 'SCENE':
                # List all scenes
                selection = bpy.data.scenes
                # Store current scene
                originalScene = bpy.context.scene

                for scenes in selection:
                    # Set scene in loop as ective scene
                    bpy.context.screen.scene = scenes

                    # Check whether anything is selected, if not -> skip loop
                    if scene.sel_only == True:
                        testSelection = bpy.context.selected_objects
                        if not testSelection:
                            continue

                    # Add sequence to name if != object name
                    if scene.objname_is_filename == False:
                        scene.filename += "_" + str(count)
                        count += 1
                    else:
                        scene.filename = scenes.name

                    SetSaveDir(scene)

                    if scene.file_format == 'obj':
                        ExportOBJ(scene)

                    elif scene.file_format == 'BIN7400' or 'ASCII6100':
                        ExportFBX(scene, scene.file_format)

                    # Remove sequence from name
                    if scene.objname_is_filename == False:
                        scene.filename = scene.filename[0: len(scene.filename) - len(str(count)) - 1]

                else:
                    # Set original scene active
                    bpy.context.screen.scene = originalScene

            # Scene Object batch
            #####################################################
            elif scene.batch_mode == 'SCENE_OBJECT':
                # List all scenes
                selection = bpy.data.scenes
                # Store current scene
                originalScene = bpy.context.scene
                exportCount = 0
                sceneCount = 0
                useSelectionOnly = scene.sel_only

                for scenes in selection:
                    scene.scenename = scenes.name
                    bpy.context.screen.scene = scenes
                    scenes.filepath = originalScene.filepath

                    # Make selection array, if nothing selected -> skip loop
                    if useSelectionOnly == True:
                        newselection = bpy.context.selected_objects
                        if not newselection:
                            continue
                    else:
                        newselection = bpy.context.visible_objects

                    # Deselect all objects and set 'selection only' to true
                    # Every object to be exported will be selected in the loop and exported seperately
                    bpy.ops.object.select_all(action='DESELECT')
                    scene.sel_only = True

                    for obj in newselection:
                        # Add sequence to name if != object name
                        if scene.objname_is_filename == False:
                            scene.filename += "_" + str(count)
                            count += 1
                        else:
                            scene.filename = obj.name

                        obj.select = True
                        scenes.objects.active = obj

                        SetSaveDir(scene)

                        # Run export operator
                        if scene.file_format == 'obj':
                            ExportOBJ(scene)

                        elif scene.file_format == 'BIN7400' or 'ASCII6100':
                            ExportFBX(scene, scene.file_format)

                        # Remove sequence from name
                        if scene.objname_is_filename == False:
                            scene.filename = scene.filename[0: len(scene.filename) - len(str(count)) - 1]

                        obj.select = False
                else:
                    # Set original scene active
                    bpy.context.screen.scene = originalScene

        else:
            # Save the selection to a single file

            SetSaveDir(scene)

            # if obj.type == 'MESH':
            if scene.file_format == 'obj':
                ExportOBJ(scene)

            elif scene.file_format == 'BIN7400' or 'ASCII6100':
                ExportFBX(scene, scene.file_format)

        return {'FINISHED'}

#--------------
# Set File Path
#--------------


def SetSaveDir(scene):
    scene = scene

    if scene.path_is_project_folder == True:
        scene.filepath = bpy.path.abspath("//")

    if scene.folder_per_scene == True and scene.batch_mode == 'SCENE_OBJECT':
        saveDir = os.path.join(scene.filepath, scene.scenename)
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
        if scene.folder_per_file == True:
            saveDir = os.path.join(saveDir, scene.filename)
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
        scene.savedir = saveDir
    elif scene.folder_per_file == True:
        saveDir = os.path.join(scene.filepath, scene.filename)
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
        scene.savedir = saveDir
    else:
        scene.savedir = scene.filepath

#---------------
# Export Obj
#---------------


def ExportOBJ(scene):
    scene = scene
    """
    if scene.folder_per_scene == True and scene.folder_per_file == True and scene.batch_mode == 'SCENE_OBJECT':
        savePath=str(scene.filepath + scene.scenename + scene.filename + "\\" + scene.filename + '.obj')
    elif scene.folder_per_scene == True and scene.batch_mode == 'SCENE_OBJECT':
        savePath=str(scene.filepath + scene.scenename + "\\" + scene.filename + '.obj')
    elif scene.folder_per_file == True:
        savePath=str(scene.filepath + scene.filename + "\\" + scene.filename + '.obj')
    else:"""
    savePath = str(scene.savedir + "\\" + scene.filename + '.obj')

    bpy.ops.export_scene.obj(
        filepath=savePath,
        use_selection=scene.sel_only,
        use_mesh_modifiers=scene.apply_mods,
        use_smooth_groups=scene.write_smooth,
        use_normals=scene.write_normals,
        use_uvs=scene.include_uv,
        use_materials=scene.write_mat,
        use_triangles=scene.triangulate,
        axis_forward=scene.axis_forward,
        axis_up=scene.axis_up,
        global_scale=scene.export_scale
    )


#----------------
# Export Fbx
#----------------
def ExportFBX(scene, version):
    scene = scene
    selection = scene.objects.active
    """
    if scene.folder_per_scene == True and scene.folder_per_file == True and scene.batch_mode == 'SCENE_OBJECT':
        savePath=str(scene.filepath + scene.scenename + scene.filename + "\\" + scene.filename + '.fbx')
    elif scene.folder_per_scene == True and scene.batch_mode == 'SCENE_OBJECT':
        savePath=str(scene.filepath + scene.scenename + "\\" + scene.filename + '.fbx')
    elif scene.folder_per_file == True:
        savePath=str(scene.filepath + scene.filename + "\\" + scene.filename + '.fbx')
    else:
        savePath=str(scene.filepath + scene.filename + '.fbx')"""

    savePath = str(scene.savedir + "\\" + scene.filename + '.fbx')

    if scene.triangulate == True:
        TriangulateMesh()

    bpy.ops.export_scene.fbx(
        filepath=savePath,
        version=version,
        use_selection=scene.sel_only,
        object_types=scene.object_types,
        use_mesh_modifiers=scene.apply_mods,
        mesh_smooth_type=scene.mesh_smooth_type,
        bake_anim=scene.write_baked_anim,
        use_anim=scene.write_anim,
        axis_forward=scene.axis_forward,
        axis_up=scene.axis_up,
        global_scale=scene.export_scale
    )

    # Delete duplicated trianlge mesh
    if scene.triangulate == True:
        bpy.ops.object.delete(use_global=True)

    # selection.select = True

#-----------------
# Triangulate Mesh
#-----------------


def TriangulateMesh():
    bpy.ops.object.duplicate(linked=False, mode='INIT')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')

#----------------
# Preset Function
#----------------


class Preset_add(AddPresetBase, bpy.types.Operator):
    bl_idname = 'ct.preset_add'
    bl_label = 'Add Easy Export Preset'
    bl_options = {'REGISTER', 'UNDO'}
    preset_menu = 'Presets_Menu'
    preset_subdir = 'Easy_Export_Presets'

    preset_defines = [
        "scene  = bpy.context.scene",
        "obj = scene.objects.active"
    ]

    preset_values = [
        "scene.sel_only",
        "scene.apply_mods",
        "scene.write_smooth",
        "scene.write_normals",
        "scene.include_uv",
        "scene.write_mat",
        "scene.triangulate",
        "scene.objname_is_filename",
        "scene.write_baked_anim",
        "scene.write_anim",
        "scene.batch",
        "scene.folder_per_file",
        "scene.filepath",
        "scene.filename",
        "scene.export_scale",
        "scene.file_format",
        "scene.axis_up",
        "scene.axis_forward",
        "scene.object_types",
        "scene.mesh_smooth_type",
        "scene.batch_mode"
    ]


class Preset_load(bpy.types.Operator):
    bl_idname = "ct.preset_load"
    bl_label = "Load Easy Export Preset"
    bl_options = {'REGISTER'}
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        filepath = self.filepath
        bpy.context.scene.currentSceneName = filepath
        bpy.ops.script.python_file_run(filepath=filepath)
        return {'FINISHED'}


class Preset_Delete(bpy.types.Operator):
    bl_idname = "ct.preset_delete"
    bl_label = "Delete Easy Export Preset"
    bl_options = {'REGISTER'}

    def execute(self, context):
        os.remove(bpy.context.scene.currentSceneName)
        return {'FINISHED'}


class Presets_Menu(bpy.types.Menu):
    bl_label = 'Easy Export Presets'
    bl_idname = "Presets_Menu"
    preset_subdir = "Easy_Export_Presets"
    preset_operator = "ct.preset_load"

    draw = bpy.types.Menu.draw_preset

#--------------
# Classic I/O
#--------------
# Just some easy access buttons for the standard I/O


class ClassicIOPanel(View3DPanel, Panel):
    bl_label = "Classic I/O"
    bl_context = "objectmode"
    bl_category = panelLabel

    def draw(self, context):
        layout = self.layout
        layout.operator("export_scene.fbx", text="Export FBX", icon='EXPORT')
        layout.operator("export_scene.obj", text="Export OBJ", icon='EXPORT')
        layout.operator("export_scene.autodesk_3ds", text="Export 3ds", icon='EXPORT')
        row = layout.row()
        box = layout.box()
        row = layout.row()
        layout.operator("import_scene.fbx", text="Import FBX", icon='IMPORT')
        layout.operator("import_scene.obj", text="Import OBJ", icon='IMPORT')
        layout.operator("import_scene.autodesk_3ds", text="Import 3ds", icon='IMPORT')

#---------------
# Register
#---------------


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
