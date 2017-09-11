# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#  Code by Koilz @ http://wiki.blender.org/ 2014
#
# ##### END GPL LICENSE BLOCK #####

# Key Error for red driver target id's.

# ----------------------------------------------------------------
# Header

bl_info = {
    "name": "Replace Driver Targets",
    "author": "koilz",
    "version": (1, 3),
    "blender": (2, 72, 0),
    "location": "3D View > Object Mode > Tools > RDT",
    "description": "Replace driver variable target id's.",
    "warning": "",
    "wiki_url": "http://blenderartists.org/forum/showthread.php?356354-wip-Addon-replace-driver-targets",
    "category": "Rigging"}

import bpy

DD = ['actions',
      'armatures',
      'brushes',
      'cameras',
      'curves',
      'fonts',
      'grease_pencil',
      'groups',
      'images',
      'shape_keys',
      'lamps',
      'libraries',
      'linestyles',
      'lattices',
      'materials',
      'metaballs',
      'meshes',
      'node_groups',
      'objects',
      'particles',
      'scenes',
      'screens',
      'speakers',
      'sounds',
      'texts',
      'textures',
      'worlds',
      'window_managers']

IDT = [('ACTION', 'Action', 'Action', 'ACTION', 0),
       ('ARMATURE', 'Armature', 'Armature', 'ARMATURE_DATA', 1),
       ('BRUSH', 'Brush', 'Brush', 'BRUSH_DATA', 2),
       ('CAMERA', 'Camera', 'Camera', 'CAMERA_DATA', 3),
       ('CURVE', 'Curve', 'Curve', 'CURVE_DATA', 4),
       ('FONT', 'Font', 'Font', 'FILE_FONT', 5),
       ('GREASEPENCIL', 'Grease Pencil', 'Grease Pencil', 'GREASEPENCIL', 6),
       ('GROUP', 'Group', 'Group', 'GROUP', 7),
       ('IMAGE', 'Image', 'Image', 'FILE_IMAGE', 8),
       ('KEY', 'Key', 'Key', 'SHAPEKEY_DATA', 9),
       ('LAMP', 'Lamp', 'Lamp', 'LAMP_DATA', 10),
       ('LIBRARY', 'Library', 'Library', 'LIBRARY_DATA_DIRECT', 11),
       ('LINESTYLE', 'Line Style', 'Line Style', 'LINE_DATA', 12),
       ('LATTICE', 'Lattice', 'Lattice', 'LATTICE_DATA', 13),
       ('MATERIAL', 'Material', 'Material', 'MATERIAL_DATA', 14),
       ('META', 'Meta', 'Meta', 'META_DATA', 15),
       ('MESH', 'Mesh', 'Mesh', 'MESH_DATA', 16),
       ('NODETREE', 'Node Tree', 'Node Tree', 'NODETREE', 17),
       ('OBJECT', 'Object', 'Object', 'OBJECT_DATA', 18),
       ('PARTICLE', 'Particle', 'Particle', 'PARTICLE_DATA', 19),
       ('SCENE', 'Scene', 'Scene', 'SCENE_DATA', 20),
       ('SCREEN', 'Screen', 'Screen', 'SPLITSCREEN', 21),
       ('SPEAKER', 'Speaker', 'Speaker', 'SPEAKER', 22),
       ('SOUND', 'Sound', 'Sound', 'SOUND', 23),
       ('TEXT', 'Text', 'Text', 'TEXT', 24),
       ('TEXTURE', 'Texture', 'Texture', 'TEXTURE_DATA', 25),
       ('WORLD', 'World', 'World', 'WORLD_DATA', 26),
       ('WINDOWMANAGER', 'Window Manager', 'Window Manager', 'DOT', 27)]

LMT = [('ASC', 'Active Scene', 'Active Scene'),
       ('AOB', 'Active Object', 'Active Object')]

# Driver Tools PropertyGroup


class DT_props(bpy.types.PropertyGroup):
    limit = bpy.props.EnumProperty(items=LMT, name="Limit", description="Limit operator to active Scene or Object.", default='ASC')
    didtr = bpy.props.EnumProperty(items=IDT, name="Driver Target ID Type", default='OBJECT')
    didr = bpy.props.StringProperty(name="Driver Target ID Replace", description="Driver Target ID Replace", default='')
    didw = bpy.props.StringProperty(name="Driver Target ID With", description="Driver Target ID With", default='')

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Replace Driver Targets


def op_rdt(self, context):

    OK = True

    # ----------------------------------------------------------------
    # animation data

    AD_dir = []
    if context.scene.DT.limit == 'ASC':                                # compile animation_data list based on active scene
        if hasattr(context.scene, 'animation_data'):                   # ad check
            AD_dir.append(context.scene.animation_data)                # ad scene
        for ob in context.scene.objects:                               # loop obs
            # print(ob)                                                 # debug
            if hasattr(ob, 'animation_data'):                          # ad check
                AD_dir.append(ob.animation_data)                       # ad object
            if hasattr(ob.data, 'animation_data'):                     # ad check
                AD_dir.append(ob.data.animation_data)                  # ad data
            if hasattr(ob.data, 'shape_keys'):                         # shape_keys check
                if hasattr(ob.data.shape_keys, 'animation_data'):      # ad check
                    AD_dir.append(ob.data.shape_keys.animation_data)   # ad shape_keys
            if hasattr(ob.data, 'materials'):                          # material check
                for m in ob.data.materials:                            # loop mats
                    if hasattr(m, 'animation_data'):                   # ad check
                        AD_dir.append(m.animation_data)                # ad material
    else:                                                          # compile animation_data list based on active object
        ob = context.active_object                                 # active_object
        if hasattr(ob, 'animation_data'):                          # ad check
            AD_dir.append(ob.animation_data)                       # ad object
        if hasattr(ob.data, 'animation_data'):                     # ad check
            AD_dir.append(ob.data.animation_data)                  # ad data
        if hasattr(ob.data, 'shape_keys'):                         # shape_keys check
            if hasattr(ob.data.shape_keys, 'animation_data'):      # ad check
                AD_dir.append(ob.data.shape_keys.animation_data)   # ad shape_keys
        if hasattr(ob.data, 'materials'):                          # material check
            for m in ob.data.materials:                            # loop mats
                if hasattr(m, 'animation_data'):                   # ad check
                    AD_dir.append(m.animation_data)                # ad material

    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # set driver target id based on type

    didtr = context.scene.DT.didtr

    didr = None
    didw = None

    DDD = [bpy.data.actions,
           bpy.data.armatures,
           bpy.data.brushes,
           bpy.data.cameras,
           bpy.data.curves,
           bpy.data.fonts,
           bpy.data.grease_pencil,
           bpy.data.groups,
           bpy.data.images,
           bpy.data.shape_keys,
           bpy.data.lamps,
           bpy.data.libraries,
           bpy.data.linestyles,
           bpy.data.lattices,
           bpy.data.materials,
           bpy.data.metaballs,
           bpy.data.meshes,
           bpy.data.node_groups,
           bpy.data.objects,
           bpy.data.particles,
           bpy.data.scenes,
           bpy.data.screens,
           bpy.data.speakers,
           bpy.data.sounds,
           bpy.data.texts,
           bpy.data.textures,
           bpy.data.worlds,
           bpy.data.window_managers]

    for i in range(28):
        if didtr == IDT[i][0]:
            if context.scene.DT.didr != '':
                didr = DDD[i][context.scene.DT.didr]
            if context.scene.DT.didw != '':
                didw = DDD[i][context.scene.DT.didw]

    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # replace driver targets

    if OK:

        dvc = 1      # driver variable continue
        dvr = 0      # driver variable targets replaced
        dvs = 0      # driver variable targets counted

        if dvc:
            for ad in AD_dir:
                if hasattr(ad, 'drivers'):
                    for d in ad.drivers:
                        for dv in d.driver.variables:
                            for dt in dv.targets:
                                dvs += 1                                       # targets processed count
                                if dt.id_type == didtr and dt.id == didr:    # compare IDT and ID
                                    dt.id = didw                             # replace ID
                                    dvr += 1                                   # targets replaced count
                                    print("")
                                    print("Replaced Driver Target: " + str(d.id_data))
                                    print(str(d.data_path) + ": " + str(d.array_index))

            print("")
            self.report({"INFO"}, "Replaced " + str(dvr) + " of " + str(dvs) + " driver targets. See console for more info.")

    # ----------------------------------------------------------------


class OT_RDT(bpy.types.Operator):
    """Replace Driver Target ID's"""
    bl_idname = "scene.replace_driver_targets"
    bl_label = "Replace Driver Targets"
    bl_options = {'REGISTER', 'UNDO'}
    # bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        op_rdt(self, context)
        return {'FINISHED'}

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Panel


class PT_RDT(bpy.types.Panel):

    bl_label = "Replace Driver Targets"
    bl_idname = "VIEW3D_PT_RDT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "RDT"
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return (context.active_object and (context.mode == 'OBJECT'))

    def draw(self, context):
        layout = self.layout

        # operator + settings
        row = layout.row(align=True)
        col = row.column(align=True)
        col.row(align=True).prop(context.scene.DT, 'limit', expand=True)
        col.operator('scene.replace_driver_targets')

        # id type
        row = layout.row(align=True)
        col = row.column(align=True)
        col.label('ID Type:')
        col.prop(context.scene.DT, 'didtr', text='')

        # replace
        row = layout.row(align=True)
        col = row.column(align=True)
        col.label('Replace:')
        for i in range(28):
            if context.scene.DT.didtr == IDT[i][0]:
                col.prop_search(context.scene.DT, 'didr', bpy.data, DD[i], text='')

        # with
        row = layout.row(align=True)
        col = row.column(align=True)
        col.label('With:')
        for i in range(28):
            if context.scene.DT.didtr == IDT[i][0]:
                col.prop_search(context.scene.DT, 'didw', bpy.data, DD[i], text='')

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Register


def register():
    bpy.utils.register_class(DT_props)
    bpy.types.Scene.DT = bpy.props.PointerProperty(type=DT_props)
    bpy.utils.register_class(OT_RDT)
    bpy.utils.register_class(PT_RDT)


def unregister():
    bpy.utils.unregister_class(PT_RDT)
    bpy.utils.unregister_class(OT_RDT)
    del bpy.types.Scene.DT
    bpy.utils.unregister_class(DT_props)

if __name__ == "__main__":
    register()

# ----------------------------------------------------------------
