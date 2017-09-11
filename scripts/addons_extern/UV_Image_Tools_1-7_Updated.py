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
    'name': "UV Tools",
    'author': "MKB",
    'version': (1, 0, 7),
    'blender': (2, 7, 2),
    'location': "IMAGE_EDITOR > TAB > TOOLS / IMAGE",
    'description': "UV IMAGE TOOL",
    'category': 'UV'}

# changes by russcript:tested 2.7 RC windows and linux
# added tabs organization (line 46)
# toolbar now shows only in uv edit modes and not uv sculpt(line 51)
# changed a few tooltips and labels, for clarity
# made the Islands tools button show only in uv edit mode(line 622)
# hope this helps, thanks for the addon


import bpy
import bmesh
import mathutils
import time
from bpy.props import BoolProperty, IntProperty, FloatProperty, EnumProperty
from collections import defaultdict
from math import radians, hypot

############----------------------############
############  Props for DROPDOWN  ############
############----------------------############


class DropdownUVToolProps(bpy.types.PropertyGroup):
    """
    Fake module like class
    bpy.context.window_manager.uvwindow
    """
    display_uvtransform = bpy.props.BoolProperty(name="Transform", description="Display UV Transfrom Tools", default=False)
    display_uvalign = bpy.props.BoolProperty(name="Align", description="Display UV Align Tools", default=False)
    display_uvselection = bpy.props.BoolProperty(name="Selection", description="Display UV Selection Tools", default=False)
    display_uvediting = bpy.props.BoolProperty(name="Editing", description="Display UV Editing Tools", default=False)
    display_uvisland = bpy.props.BoolProperty(name="Island", description="Display UV Island Tools", default=False)
    display_uvhide = bpy.props.BoolProperty(name="Hidden", description="Display UV Hide Tools", default=False)


bpy.utils.register_class(DropdownUVToolProps)
bpy.types.WindowManager.uvwindow = bpy.props.PointerProperty(type=DropdownUVToolProps)

############-----------------------------############
############  DROPDOWN Layout for PANEL  ############
############-----------------------------############


class uvtools(bpy.types.Panel):
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_label = "UV Tools"

    @classmethod
    def poll(cls, context):
        sima = context.space_data
        return sima.show_uvedit and not context.tool_settings.use_uv_sculpt

    def draw(self, context):
        lt = context.window_manager.uvwindow
        scn = context.scene
        layout = self.layout


# -------------------------------------------------------
# Selections  #######-------------------------------------------------------
# Selections  #######-------------------------------------------------------
# -------------------------------------------------------

        ###space1###
        # col = layout.column(align=True)
        if lt.display_uvselection:
            ###space2###
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvselection", text="", icon='TRIA_DOWN')

        else:
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvselection", text="", icon='TRIA_RIGHT')

        row.label("Selection...")
        row.operator("uv.select_border", text="", icon="BORDER_RECT").pinned = False

        ###space1###
        if lt.display_uvselection:
            ###space2###
            system = context.user_preferences.system
            inputs = context.user_preferences.inputs
            edit = context.user_preferences.edit

            # col = layout.column(align=True)
            ###space2###
            # box = col.column(align=True).box().column()

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.prop(inputs, "select_mouse", expand=True)

            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("uv.select_all", text="All").action = 'TOGGLE'
            row.operator("uv.select_all", text="Invert").action = 'INVERT'

            row = col_top.row(align=True)
            row.operator("uv.select_linked", text="Linked")
            row.operator("uv.select_split", text="Split")

            row = col_top.row(align=True)
            row.operator("uv.select_pinned", text="Pinned")
            row.operator("uv.select_border", text="Box Pinned").pinned = True

#--Snap-------------------------------------------------------------------------------------

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("uv.snap_selected", text="Selected > Cursor").target = "CURSOR"
            row.operator("uv.snap_selected", text="-> Cursor Offset").target = "CURSOR_OFFSET"

            row = col_top.row(align=True)
            row.operator("uv.snap_selected", text="Selected > Pixel").target = "PIXELS"
            row.operator("uv.snap_selected", text="-> Adjacent").target = "ADJACENT_UNSELECTED"

            row = col_top.row(align=True)
            row.operator("uv.snap_cursor", text="Cursor > Selected").target = "SELECTED"
            row.operator("uv.snap_cursor", text="Cursor > Pixel").target = "PIXELS"


# -------------------------------------------------------
# Transform  #######-------------------------------------------------------
# Transform  #######-------------------------------------------------------
# -------------------------------------------------------

        ###space1###
        if lt.display_uvtransform:
            ###space2###
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvtransform", text="", icon='TRIA_DOWN')

        else:
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvtransform", text="", icon='TRIA_RIGHT')

        row.label("Transform...")
        # row.prop(context.scene, "AutoMirror_orientation", "", icon = "ARROW_LEFTRIGHT")

        ###space1###
        if lt.display_uvtransform:
            ###space2###

            # col = layout.column(align=True)
            # box = col.column(align=True).box().column()

            # row = col_top.row(align=True)
            # row.operator("transform.translate",text="(G)", icon="MAN_TRANS")
            # row.operator("transform.rotate", text="(R)", icon="MAN_ROT")
            # row.operator("transform.resize", text="(S)", icon="MAN_SCALE")

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("transform.mirror", text="Mirror X", icon="ARROW_LEFTRIGHT").constraint_axis = (True, False, False)
            row.operator("transform.mirror", text="Mirror Y", icon="ARROW_LEFTRIGHT").constraint_axis = (False, True, False)

            row = col_top.row(align=True)
            row.operator("uv.rotateoneeighty", text="Rot 180", icon="FILE_REFRESH")
            row = col_top.row(align=True)
            row.operator("uv.rotatednineminus", text="Rot -90°", icon="FILE_REFRESH")
            row.operator("uv.rotatednine", text="Rot 90°", icon="FILE_REFRESH")

# -------------------------------------------------------
# Island  #######-------------------------------------------------------
# Island  #######-------------------------------------------------------
# -------------------------------------------------------

        ###space1###
        # col = layout.column(align=True)
        if lt.display_uvisland:
            ###space2###
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvisland", text="", icon='TRIA_DOWN')

        else:
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvisland", text="", icon='TRIA_RIGHT')

        row.label("Island...")
        row.operator("uv.reset", text="", icon="RECOVER_AUTO")
        row.operator("uv.pack_islands", text="", icon="GRID")

        ###space1###
        if lt.display_uvisland:
            ###space2###
            # col = layout.column(align=True)

            # box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("mesh.faces_mirror_uv", text="Copy Mirror UV")

            row = col_top.row(align=True)
            row.operator("uv.unwrap", text="Unwrap [E]")

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("uv.minimize_stretch", text="Reduce Stretch")
            row.operator("uv.average_islands_scale", text="Average Scale")

            row = col_top.row(align=True)
            row.operator("uv.mark_seam", text="Mark Seams")
            row.operator("uv.seams_from_islands", text="> from Islands")


# -------------------------------------------------------
# Align UV  #######-------------------------------------------------------
# Align UV  #######-------------------------------------------------------
# -------------------------------------------------------

        ###space1###
        # col = layout.column(align=True)
        if lt.display_uvalign:
            ###space2###
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvalign", text="", icon='TRIA_DOWN')

        else:
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvalign", text="", icon='TRIA_RIGHT')

        row.label("Align...")
        # row.prop(context.scene, "AutoMirror_orientation", "", icon = "ARROW_LEFTRIGHT")

        #
        ###space1###
        if lt.display_uvalign:
            ###space2###
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("uv.uv_squares_by_shape", text="Shape Grid")
            row.operator("uv.uv_squares", text="Square Grid")

            col = layout.column(align=True)

            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("uv.align", text="Flatten X").axis = 'ALIGN_X'
            row.operator("uv.align", text="Flatten Y").axis = 'ALIGN_Y'

            row = col_top.row(align=True)
            row.operator("uv.align", text="AutoAlign").axis = 'ALIGN_AUTO'
            row.operator("uv.align", text="Straighten").axis = 'ALIGN_S'

            row = col_top.row(align=True)
            row.operator("uv.align", text="Straighten X").axis = 'ALIGN_T'
            row.operator("uv.align", text="StraightenY").axis = 'ALIGN_U'

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("uv.uv_snap_to_axis", text="Snap to X/Y-Axis")
            row = col_top.row(align=True)
            row.operator("uv.uv_snap_to_axis_and_equal", text="Snap with Equal Distance")
            row = col_top.row(align=True)
            row.operator("uv.uv_face_join", text="Snap to Closest Unselected")

            col = layout.column(align=True)
            box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.label(text="Align to Square...")

            row = col_top.row(align=True)
            row.operator("uv.align_left_margin", "Left")
            row.operator("uv.align_vertical_axis", "VAxis")
            row.operator("uv.align_right_margin", "Right")

            row = col_top.row(align=True)
            row.operator("uv.align_top_margin", "Top")
            row.operator("uv.align_horizontal_axis", "HAxis")
            row.operator("uv.align_low_margin", "Low")

            row = col_top.row(align=True)
            row.prop(scn, "relativeItems")
            row = box.row(True)
            row.prop(scn, "selectionAsGroup")


# -------------------------------------------------------
# Editing  #######-------------------------------------------------------
# Editing  #######-------------------------------------------------------
# -------------------------------------------------------

        ###space1###
        # col = layout.column(align=True)
        if lt.display_uvediting:
            ###space2###
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvediting", text="", icon='TRIA_DOWN')

        else:
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvediting", text="", icon='TRIA_RIGHT')

        row.label("Editing...")
        row.operator("uv.remove_doubles", text="", icon="PANEL_CLOSE")

        ###space1###
        if lt.display_uvediting:
            ###space2###
            # col = layout.column(align=True)

            # box = col.column(align=True).box().column()
            col_top = box.column(align=True)
            row = col_top.row(align=True)

            row.operator("uv.weld", text="Weld [W]", icon="AUTOMERGE_ON")
            row.operator("uv.stitch", text="Stitch [V]")

            row = col_top.row(align=True)
            row.operator("uv.uv_face_join", text="Join Faces")
            row.operator("uv.uv_face_rip", text="Rip UV")
            row = col_top.row(align=True)

            col_top = box.column(align=True)
            row = col_top.row(align=True)
            row.operator("uv.pin", text="Pin", icon="PINNED").clear = False
            row.operator("uv.pin", text="UnPin", icon="UNPINNED").clear = True

            row = col_top.row(align=True)
            row.label(text="[CTRL+I] = Toggle Islands")

# -------------------------------------------------------
# Hidden  #######-------------------------------------------------------
# Hidden  #######-------------------------------------------------------
# -------------------------------------------------------

        ###space1###
        # col = layout.column(align=True)
        if lt.display_uvhide:
            ###space2###
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvhide", text="", icon='TRIA_DOWN')

        else:
            box = layout.box()
            row = box.row()
            row.prop(lt, "display_uvhide", text="", icon='TRIA_RIGHT')

        # row.label("History...")
        row.operator("ed.redo", text="Redo", icon="LOOP_FORWARDS")
        row.operator("ed.undo", text="Undo", icon="LOOP_BACK")

        ###space1###
        if lt.display_uvhide:
            ###space2###
            # col = layout.column(align=True)

            # box = col.column(align=True).box().column()
            col_top = box.column(align=True)

            row = col_top.row(align=True)
            row.operator("uv.reveal", text="Show All", icon="VISIBLE_IPO_ON")
            row.operator("ed.undo_history", text="History", icon="SCRIPTPLUGINS")

            row = col_top.row(align=True)
            row.operator("uv.hide", text="UnHide", icon="RESTRICT_VIEW_OFF").unselected = True
            row.operator("uv.hide", text="Hide", icon="RESTRICT_VIEW_ON").unselected = False


#--Save---------------------------------------------------------------------------------

        col = layout.column(align=True)
        row = col.row(align=True)

        row.operator("uv.export_layout", text="Export UV Layout")
        row.operator("wm.save_mainfile", text="", icon="FILE_TICK")
        row.operator("wm.save_as_mainfile", text="", icon="SAVE_AS")


#-------------------------------------------------------------------------------------


class imagetools(bpy.types.Panel):
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Image'
    bl_label = "Image Tools"

    def draw(self, context):
        layout = self.layout


#--Image---------------------------------------------------------------------------------

        col = layout.column(align=True)
        col.label(text="Image...")

        row = col.row(align=True)
        row.operator("image.open", text="Open", icon="FILESEL")
        row.operator("image.new", text="New")

        row = col.row(align=True)
        row.operator("image.reload", text="Reload")
        row.operator("image.replace", text="Replace")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("image.external_edit", text="Edit Image External")


#--Image Pack---------------------------------------------------------------------------

        col = layout.column(align=True)
        col.label(text="Pack into File...")

        row = col.row(align=True)
        row.operator("image.pack", text="Pack", icon="PACKAGE")
        row.operator("image.pack", text="Pack as PNG").as_png = True


#--Save-------------------------------------------------------------------------------

        col = layout.column(align=True)
        col.label(text="Save...")

        row = col.row(align=True)
        row.operator("image.save", text="Save", icon="FILE_TICK")
        row.operator("image.save_as", text="Save as", icon="SAVE_AS")
        row.operator("image.save_as", text="Save Copy").copy = True


#--Small Operator-------------------------------------------------------------------------------
#--Small Operator-------------------------------------------------------------------------------
#--Small Operator-------------------------------------------------------------------------------
#--Small Operator-------------------------------------------------------------------------------

class uvrotatedA(bpy.types.Operator):
    """uv rotate 90°"""
    bl_label = "UV Rotate 90°"
    bl_idname = "uv.rotatednine"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.rotate(value=1.5708, axis=(-0, -0, -1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1.61051)

        return {"FINISHED"}


class uvrotatedB(bpy.types.Operator):
    """uv rotate -90°"""
    bl_label = "UV Rotate -90°"
    bl_idname = "uv.rotatednineminus"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.rotate(value=-1.5708, axis=(-0, -0, -1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1.61051)

        return {"FINISHED"}


class uvrotatedC(bpy.types.Operator):
    """uv rotate 180°"""
    bl_label = "UV Rotate 180°"
    bl_idname = "uv.rotateoneeighty"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.transform.rotate(value=-3.14159, axis=(-0, -0, -1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        return {"FINISHED"}


#--Small Operator-------------------------------------------------------------------------------
#--Small Operator-------------------------------------------------------------------------------
#--Small Operator-------------------------------------------------------------------------------
#--Small Operator-------------------------------------------------------------------------------


# bl_info = {
#    "name": "UV Align\Distribute",
#    "author": "Rebellion (Luca Carella)",
#    "version": (0, 9),
#    "blender": (2, 7, 0),
#    "location": "UV/Image editor > Tool Panel, UV/Image editor UVs > menu",
#    "description": "Set of tools to help UV alignment\distribution",
#    "warning": "",
#    "wiki_url": "",
#    "category": "UV"}


# Globals:

bpy.types.Scene.relativeItems = EnumProperty(items=[('UV_SPACE', 'Uv Space', 'Align to UV space'), ('ACTIVE', 'Active Face', 'Align to active face\island'), ('CURSOR', 'Cursor', 'Align to cursor')], name="Relative to")
bpy.types.Scene.selectionAsGroup = BoolProperty(name="Selection as group", description="Treat selection as group", default=False)

bm = None
uvlayer = None


def initBmesh():
    global bm
    global uvlayer
    bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
    uvlayer = bm.loops.layers.uv.active


def update():
    bmesh.update_edit_mesh(bpy.context.edit_object.data, False, False)
    # bm.to_mesh(bpy.context.object.data)
    # bm.free()


def GBBox(islands):
    minX = +1000
    minY = +1000
    maxX = -1000
    maxY = -1000
    for island in islands:
        # print(island)
        for face_id in island:
            face = bm.faces[face_id]
            for loop in face.loops:
                minX = min(loop[uvlayer].uv.x, minX)
                minY = min(loop[uvlayer].uv.y, minY)
                maxX = max(loop[uvlayer].uv.x, maxX)
                maxY = max(loop[uvlayer].uv.y, maxY)

    return mathutils.Vector((minX, minY)), mathutils.Vector((maxX, maxY))


def GBBoxCenter(islands):
    minX = +1000
    minY = +1000
    maxX = -1000
    maxY = -1000
    for island in islands:
        for face_id in island:
            face = bm.faces[face_id]
            for loop in face.loops:
                minX = min(loop[uvlayer].uv.x, minX)
                minY = min(loop[uvlayer].uv.y, minY)
                maxX = max(loop[uvlayer].uv.x, maxX)
                maxY = max(loop[uvlayer].uv.y, maxY)

    return (mathutils.Vector((minX, minY)) + mathutils.Vector((maxX, maxY))) / 2


def BBox(island):
    minX = +1000
    minY = +1000
    maxX = -1000
    maxY = -1000
    # for island in islands:
    # print(island)
    for face_id in island:
        face = bm.faces[face_id]
        for loop in face.loops:
            minX = min(loop[uvlayer].uv.x, minX)
            minY = min(loop[uvlayer].uv.y, minY)
            maxX = max(loop[uvlayer].uv.x, maxX)
            maxY = max(loop[uvlayer].uv.y, maxY)

    return mathutils.Vector((minX, minY)), mathutils.Vector((maxX, maxY))


def BBoxCenter(island):
    minX = +1000
    minY = +1000
    maxX = -1000
    maxY = -1000
    # for island in islands:
    for face_id in island:
        face = bm.faces[face_id]
        for loop in face.loops:
            minX = min(loop[uvlayer].uv.x, minX)
            minY = min(loop[uvlayer].uv.y, minY)
            maxX = max(loop[uvlayer].uv.x, maxX)
            maxY = max(loop[uvlayer].uv.y, maxY)

    return (mathutils.Vector((minX, minY)) + mathutils.Vector((maxX, maxY))) / 2


def moveIslands(vector, island):
        # for island in islands:
    print(vector)
    for face_id in island:
        print(face_id)
        face = bm.faces[face_id]
        # print(face_id)
        for loop in face.loops:
            # print(loop[uvlayer].uv)
            loop[bm.loops.layers.uv.active].uv += vector
            # print(loop[bm.loops.layers.uv.active].uv)


class MakeIslands():

    def __init__(self):
        # self.bm = bmesh.new()
        initBmesh()
        global bm
        global uvlayer

        self.face_to_verts = defaultdict(set)
        self.vert_to_faces = defaultdict(set)
        self.selectedIsland = set()

        for face in bm.faces:
            for loop in face.loops:
                # if loop[uvlayer].select :
                # floating point error! keep it low
                id = '{0[0]:.5} {0[1]:.5} {1}'.format(loop[uvlayer].uv, loop.vert.index)
                self.face_to_verts[face.index].add(id)
                self.vert_to_faces[id].add(face.index)
                if loop[uvlayer].select:
                    self.selectedIsland.add(face.index)

        # print(self.selectedIsland)
    def addToIsland(self, face_id):
        if face_id in self.faces_left:
            # add the face itself
            self.current_island.append(face_id)
            # print(face_id)
            self.faces_left.remove(face_id)
            # and add all faces that share uvs with this face
            verts = self.face_to_verts[face_id]
            for vert in verts:
                # print('looking at vert {}'.format(vert))
                connected_faces = self.vert_to_faces[vert]
                if connected_faces:
                    for face in connected_faces:
                        self.addToIsland(face)

    def getIslands(self):
        self.islands = []
        self.faces_left = set(self.face_to_verts.keys())
        while len(self.faces_left) > 0:
            face_id = list(self.faces_left)[0]
            self.current_island = []
            # print(self.faces_left)
            self.addToIsland(face_id)
            self.islands.append(self.current_island)

        return self.islands

    def newIsland(self):
        self.islands = []
        faces_left = set(self.face_to_verts.keys())
        for face_id in faces_left:
            verts = self.face_to_verts[face_id]
            for vert in verts:
                connected_vert = self.vert_to_faces[vert]
                if connected_vert:
                    self.islands.append(face_id)
        return self.islands

    def activeIsland(self):
        for island in self.islands:
            if bm.faces.active.index in island:
                return island

    def selectedIslands(self):
        _selectedIslands = []
        # print('selectedIslands()')
        # print(self.selectedIsland)
        for island in self.islands:
            # print(island)
            if not self.selectedIsland.isdisjoint(island):
                _selectedIslands.append(island)
                # print('True')
        return _selectedIslands


def getTargetPoint(context, islands):
    if context.scene.relativeItems == 'UV_SPACE':
        return mathutils.Vector((0.0, 0.0)), mathutils.Vector((1.0, 1.0))
    elif context.scene.relativeItems == 'ACTIVE':
        return BBox(islands.activeIsland())
    elif context.scene.relativeItems == 'CURSOR':
        return context.space_data.cursor_location, context.space_data.cursor_location
######################
# OPERATOR
######################


class AlignSXMargin(bpy.types.Operator):
    """Align left margin"""
    bl_idname = "uv.align_left_margin"
    bl_label = "Align left margin"
    bl_options = {'REGISTER', 'UNDO'}

#    @classmethod
#    def poll(cls, context):
#        return (context.mode == 'EDIT_MESH')
    def execute(self, context):

        makeIslands = MakeIslands()
        islands = makeIslands.getIslands()
        selectedIslands = makeIslands.selectedIslands()

        targetElement = getTargetPoint(context, makeIslands)[0]
        print(targetElement[0])

        if context.scene.selectionAsGroup:
            groupBox = GBBox(selectedIslands)
            if context.scene.relativeItems == 'ACTIVE':
                selectedIslands.remove(makeIslands.activeIsland())
            for island in selectedIslands:
                vector = mathutils.Vector((targetElement.x - groupBox[0].x, 0.0))
                moveIslands(vector, island)

        else:
            for island in selectedIslands:
                vector = mathutils.Vector((targetElement.x - BBox(island)[0].x, 0.0))
                moveIslands(vector, island)

        # print(targetElement)
        update()
        return {'FINISHED'}


class AlignRxMargin(bpy.types.Operator):
    """Align right margin"""
    bl_idname = "uv.align_right_margin"
    bl_label = "Align right margin"
    bl_options = {'REGISTER', 'UNDO'}
#    @classmethod
#    def poll(cls, context):
#        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        makeIslands = MakeIslands()
        islands = makeIslands.getIslands()
        selectedIslands = makeIslands.selectedIslands()

        targetElement = getTargetPoint(context, makeIslands)[1]

        # print(targetElement)
        if context.scene.selectionAsGroup:
            groupBox = GBBox(selectedIslands)
            if context.scene.relativeItems == 'ACTIVE':
                selectedIslands.remove(makeIslands.activeIsland())
            for island in selectedIslands:
                vector = mathutils.Vector((targetElement.x - groupBox[1].x, 0.0))
                moveIslands(vector, island)

        else:
            for island in selectedIslands:
                vector = mathutils.Vector((targetElement.x - BBox(island)[1].x, 0.0))
                moveIslands(vector, island)

        # print(targetElement)
        update()
        return {'FINISHED'}


class AlignVAxis(bpy.types.Operator):
    """Align vertical axis"""
    bl_idname = "uv.align_vertical_axis"
    bl_label = "Align vertical axis"
    bl_options = {'REGISTER', 'UNDO'}
#    @classmethod
#    def poll(cls, context):
#        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        makeIslands = MakeIslands()
        islands = makeIslands.getIslands()
        selectedIslands = makeIslands.selectedIslands()

        targetElement = getTargetPoint(context, makeIslands)
        targetCenter = (targetElement[0] + targetElement[1]) / 2
        # print(targetElement[0])
        if context.scene.selectionAsGroup:
            groupBoxCenter = GBBoxCenter(selectedIslands)
            if context.scene.relativeItems == 'ACTIVE':
                selectedIslands.remove(makeIslands.activeIsland())
            for island in selectedIslands:
                vector = mathutils.Vector((targetCenter.x - groupBoxCenter.x, 0.0))
                moveIslands(vector, island)

        else:
            for island in selectedIslands:
                vector = mathutils.Vector((targetCenter.x - BBoxCenter(island).x, 0.0))
                moveIslands(vector, island)

        # print(targetElement)
        update()
        return {'FINISHED'}
##################################################


class AlignTopMargin(bpy.types.Operator):
    """Align top margin"""
    bl_idname = "uv.align_top_margin"
    bl_label = "Align top margin"
    bl_options = {'REGISTER', 'UNDO'}

#    @classmethod
#    def poll(cls, context):
#        return (context.mode == 'EDIT_MESH')

    def execute(self, context):

        makeIslands = MakeIslands()
        islands = makeIslands.getIslands()
        selectedIslands = makeIslands.selectedIslands()

        targetElement = getTargetPoint(context, makeIslands)[1]
        # print(targetElement[1])
        if context.scene.selectionAsGroup:
            groupBox = GBBox(selectedIslands)
            if context.scene.relativeItems == 'ACTIVE':
                selectedIslands.remove(makeIslands.activeIsland())
            for island in selectedIslands:
                vector = mathutils.Vector((0.0, targetElement.y - groupBox[1].y))
                moveIslands(vector, island)

        else:
            for island in selectedIslands:
                vector = mathutils.Vector((0.0, targetElement.y - BBox(island)[1].y))
                moveIslands(vector, island)

        # print(targetElement)
        update()
        return {'FINISHED'}


class AlignLowMargin(bpy.types.Operator):
    """Align low margin"""
    bl_idname = "uv.align_low_margin"
    bl_label = "Align low margin"
    bl_options = {'REGISTER', 'UNDO'}
#    @classmethod
#    def poll(cls, context):
#        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        makeIslands = MakeIslands()
        islands = makeIslands.getIslands()
        selectedIslands = makeIslands.selectedIslands()

        targetElement = getTargetPoint(context, makeIslands)[0]
        if context.scene.selectionAsGroup:
            groupBox = GBBox(selectedIslands)
            if context.scene.relativeItems == 'ACTIVE':
                selectedIslands.remove(makeIslands.activeIsland())
            for island in selectedIslands:
                vector = mathutils.Vector((0.0, targetElement.y - groupBox[0].y))
                moveIslands(vector, island)

        else:
            for island in selectedIslands:
                vector = mathutils.Vector((0.0, targetElement.y - BBox(island)[0].y))
                moveIslands(vector, island)

        # print(targetElement)
        update()
        return {'FINISHED'}


class AlignHAxis(bpy.types.Operator):
    """Align horizontal axis"""
    bl_idname = "uv.align_horizontal_axis"
    bl_label = "Align horizontal axis"
    bl_options = {'REGISTER', 'UNDO'}
#    @classmethod
#    def poll(cls, context):
#        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        makeIslands = MakeIslands()
        islands = makeIslands.getIslands()
        selectedIslands = makeIslands.selectedIslands()

        targetElement = getTargetPoint(context, makeIslands)
        targetCenter = (targetElement[0] + targetElement[1]) / 2
        # print(targetElement[0])

        if context.scene.selectionAsGroup:
            groupBoxCenter = GBBoxCenter(selectedIslands)
            if context.scene.relativeItems == 'ACTIVE':
                selectedIslands.remove(makeIslands.activeIsland())
            for island in selectedIslands:
                vector = mathutils.Vector((0.0, targetCenter.y - groupBoxCenter.y))
                moveIslands(vector, island)

        else:
            for island in selectedIslands:
                vector = mathutils.Vector((0.0, targetCenter.y - BBoxCenter(island).y))
                moveIslands(vector, island)

        # print(targetElement)
        update()
        return {'FINISHED'}


#########################################################################################################################################
#########################################################################################################################################
##############  Uv Squares  #############################################################################################################
##############  Uv Squares  #############################################################################################################


# bl_info = {
#    "name": "Uv Squares",
#    "description": "Reshapes UV faces to a grid of equivalent squares, "
#    "aligns vertices on axis with equal vertex distance, "
#    "rips/joins faces.",
#    "author": "Reslav Hollos",
#    "version": (1, 4, 21),
#    "blender": (2, 71, 0),
#    "category": "Mesh"
    #"location": "UV Image Editor > UVs > UVs to grid of squares",
    #"warning": "",
    #"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
    #"Scripts/UV/Uv_Squares",
    #}


import bpy
import bmesh
from collections import defaultdict
from math import radians, hypot
import time

precision = 3

# todo: make joining radius scale with editor zoom rate or average unit length
# todo: align to axis by respect to vert distance
# todo: snap 2dCursor to closest selected vert (when more vertices are selected
# todo: rip different vertex on each press


def main(context, operator, square=False, snapToClosest=False):
    startTime = time.clock()
    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    uv_layer = bm.loops.layers.uv.verify()
    bm.faces.layers.tex.verify()  # currently blender needs both layers.

    face_act = bm.faces.active
    targetFace = face_act

    # if len(bm.faces) > allowedFaces:
    #    operator.report({'ERROR'}, "selected more than " +str(allowedFaces) +" allowed faces.")
    #   return

    edgeVerts, filteredVerts, selFaces, nonQuadFaces, vertsDict, noEdge = ListsOfVerts(uv_layer, bm)

    if len(filteredVerts) is 0:
        return
    if len(filteredVerts) is 1:
        SnapCursorToClosestSelected(filteredVerts)
        return

    cursorClosestTo = CursorClosestTo(filteredVerts)
    # line is selected

    if len(selFaces) is 0:
        if snapToClosest is True:
            SnapCursorToClosestSelected(filteredVerts)
            return

        VertsDictForLine(uv_layer, bm, filteredVerts, vertsDict)

        if AreVectsLinedOnAxis(filteredVerts) is False:
            ScaleTo0OnAxisAndCursor(filteredVerts, vertsDict, cursorClosestTo)
            return SuccessFinished(me, startTime)

        MakeEqualDistanceBetweenVertsInLine(filteredVerts, vertsDict, cursorClosestTo)
        return SuccessFinished(me, startTime)

    # else:

    # active face checks
    if targetFace is None or targetFace.select is False or len(targetFace.verts) is not 4:
        targetFace = selFaces[0]
    else:
        for l in targetFace.loops:
            if l[uv_layer].select is False:
                targetFace = selFaces[0]
                break

    ShapeFace(uv_layer, operator, targetFace, vertsDict, square)

    for nf in nonQuadFaces:
        for l in nf.loops:
            luv = l[uv_layer]
            luv.select = False

    if square:
        FollowActiveUV(operator, me, targetFace, selFaces, 'EVEN')
    else:
        FollowActiveUV(operator, me, targetFace, selFaces)

    if noEdge is False:
        # edge has ripped so we connect it back
        for ev in edgeVerts:
            key = (round(ev.uv.x, precision), round(ev.uv.y, precision))
            if key in vertsDict:
                ev.uv = vertsDict[key][0].uv
                ev.select = True

    return SuccessFinished(me, startTime)

'''def ScaleSelection(factor, pivot = 'CURSOR'):
    last_pivot = bpy.context.space_data.pivot_point
    bpy.context.space_data.pivot_point = pivot
    bpy.ops.transform.resize(value=(factor, factor, factor), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.context.space_data.pivot_point = last_pivot
    return'''


def ShapeFace(uv_layer, operator, targetFace, vertsDict, square):
    corners = []
    for l in targetFace.loops:
        luv = l[uv_layer]
        corners.append(luv)

    if len(corners) is not 4:
        # operator.report({'ERROR'}, "bla")
        return

    lucv, ldcv, rucv, rdcv = Corners(corners)

    cct = CursorClosestTo([lucv, ldcv, rdcv, rucv])
    if cct is None:
        cct.x, cct.y = lucv.x, lucv.y

    MakeUvFaceEqualRectangle(vertsDict, lucv, rucv, rdcv, ldcv, cct, square)
    return


def MakeUvFaceEqualRectangle(vertsDict, lucv, rucv, rdcv, ldcv, startv, square=False):
    ratioX, ratioY = ImageRatio()
    ratio = ratioX / ratioY

    if startv is None:
        startv = lucv.uv
    elif AreVertsQuasiEqual(startv, rucv):
        startv = rucv.uv
    elif AreVertsQuasiEqual(startv, rdcv):
        startv = rdcv.uv
    elif AreVertsQuasiEqual(startv, ldcv):
        startv = ldcv.uv
    else:
        startv = lucv.uv

    lucv = lucv.uv
    rucv = rucv.uv
    rdcv = rdcv.uv
    ldcv = ldcv.uv

    if (startv == lucv):
        finalScaleX = hypotVert(lucv, rucv)
        finalScaleY = hypotVert(lucv, ldcv)
        currRowX = lucv.x
        currRowY = lucv.y

    elif (startv == rucv):
        finalScaleX = hypotVert(rucv, lucv)
        finalScaleY = hypotVert(rucv, rdcv)
        currRowX = rucv.x - finalScaleX
        currRowY = rucv.y

    elif (startv == rdcv):
        finalScaleX = hypotVert(rdcv, ldcv)
        finalScaleY = hypotVert(rdcv, rucv)
        currRowX = rdcv.x - finalScaleX
        currRowY = rdcv.y + finalScaleY

    else:
        finalScaleX = hypotVert(ldcv, rdcv)
        finalScaleY = hypotVert(ldcv, lucv)
        currRowX = ldcv.x
        currRowY = ldcv.y + finalScaleY

    if square:
        finalScaleY = finalScaleX * ratio
    # lucv, rucv
    x = round(lucv.x, precision)
    y = round(lucv.y, precision)
    for v in vertsDict[(x, y)]:
        v.uv.x = currRowX
        v.uv.y = currRowY

    x = round(rucv.x, precision)
    y = round(rucv.y, precision)
    for v in vertsDict[(x, y)]:
        v.uv.x = currRowX + finalScaleX
        v.uv.y = currRowY

    # rdcv, ldcv
    x = round(rdcv.x, precision)
    y = round(rdcv.y, precision)
    for v in vertsDict[(x, y)]:
        v.uv.x = currRowX + finalScaleX
        v.uv.y = currRowY - finalScaleY

    x = round(ldcv.x, precision)
    y = round(ldcv.y, precision)
    for v in vertsDict[(x, y)]:
        v.uv.x = currRowX
        v.uv.y = currRowY - finalScaleY

    return


def SnapCursorToClosestSelected(filteredVerts):
    # TODO: snap to closest selected
    if len(filteredVerts) is 1:
        SetAll2dCursorsTo(filteredVerts[0].uv.x, filteredVerts[0].uv.y)

    return


def ListsOfVerts(uv_layer, bm):
    edgeVerts = []
    allEdgeVerts = []
    filteredVerts = []
    selFaces = []
    nonQuadFaces = []
    vertsDict = defaultdict(list)  # dict

    for f in bm.faces:
        isFaceSel = True
        facesEdgeVerts = []
        if (f.select == False):
            continue

        # collect edge verts if any
        for l in f.loops:
            luv = l[uv_layer]
            if luv.select is True:
                facesEdgeVerts.append(luv)
            else:
                isFaceSel = False

        allEdgeVerts.extend(facesEdgeVerts)
        if isFaceSel:
            if len(f.verts) is not 4:
                nonQuadFaces.append(f)
                edgeVerts.extend(facesEdgeVerts)
            else:
                selFaces.append(f)

                for l in f.loops:
                    luv = l[uv_layer]
                    x = round(luv.uv.x, precision)
                    y = round(luv.uv.y, precision)
                    vertsDict[(x, y)].append(luv)

        else:
            edgeVerts.extend(facesEdgeVerts)

    noEdge = False
    if len(edgeVerts) is 0:
        noEdge = True
        edgeVerts.extend(allEdgeVerts)

    if len(selFaces) is 0:
        for ev in edgeVerts:
            if ListQuasiContainsVect(filteredVerts, ev) is False:
                filteredVerts.append(ev)
    else:
        filteredVerts = edgeVerts

    return edgeVerts, filteredVerts, selFaces, nonQuadFaces, vertsDict, noEdge


def ListQuasiContainsVect(list, vect):
    for v in list:
        if AreVertsQuasiEqual(v, vect):
            return True
    return False

# modified ideasman42's uvcalc_follow_active.py


def FollowActiveUV(operator, me, f_act, faces, EXTEND_MODE='LENGTH_AVERAGE'):
    bm = bmesh.from_edit_mesh(me)
    uv_act = bm.loops.layers.uv.active

    # our own local walker
    def walk_face_init(faces, f_act):
        # first tag all faces True (so we dont uvmap them)
        for f in bm.faces:
            f.tag = True
        # then tag faces arg False
        for f in faces:
            f.tag = False
        # tag the active face True since we begin there
        f_act.tag = True

    def walk_face(f):
        # all faces in this list must be tagged
        f.tag = True
        faces_a = [f]
        faces_b = []

        while faces_a:
            for f in faces_a:
                for l in f.loops:
                    l_edge = l.edge
                    if (l_edge.is_manifold is True) and (l_edge.seam is False):
                        l_other = l.link_loop_radial_next
                        f_other = l_other.face
                        if not f_other.tag:
                            yield (f, l, f_other)
                            f_other.tag = True
                            faces_b.append(f_other)
            # swap
            faces_a, faces_b = faces_b, faces_a
            faces_b.clear()

    def walk_edgeloop(l):
        """
        Could make this a generic function
        """
        e_first = l.edge
        e = None
        while True:
            e = l.edge
            yield e

            # don't step past non-manifold edges
            if e.is_manifold:
                # welk around the quad and then onto the next face
                l = l.link_loop_radial_next
                if len(l.face.verts) == 4:
                    l = l.link_loop_next.link_loop_next
                    if l.edge is e_first:
                        break
                else:
                    break
            else:
                break

    def extrapolate_uv(fac,
                       l_a_outer, l_a_inner,
                       l_b_outer, l_b_inner):
        l_b_inner[:] = l_a_inner
        l_b_outer[:] = l_a_inner + ((l_a_inner - l_a_outer) * fac)

    def apply_uv(f_prev, l_prev, f_next):
        l_a = [None, None, None, None]
        l_b = [None, None, None, None]

        l_a[0] = l_prev
        l_a[1] = l_a[0].link_loop_next
        l_a[2] = l_a[1].link_loop_next
        l_a[3] = l_a[2].link_loop_next

        #  l_b
        #  +-----------+
        #  |(3)        |(2)
        #  |           |
        #  |l_next(0)  |(1)
        #  +-----------+
        #        ^
        #  l_a   |
        #  +-----------+
        #  |l_prev(0)  |(1)
        #  |    (f)    |
        #  |(3)        |(2)
        #  +-----------+
        #  copy from this face to the one above.

        # get the other loops
        l_next = l_prev.link_loop_radial_next
        if l_next.vert != l_prev.vert:
            l_b[1] = l_next
            l_b[0] = l_b[1].link_loop_next
            l_b[3] = l_b[0].link_loop_next
            l_b[2] = l_b[3].link_loop_next
        else:
            l_b[0] = l_next
            l_b[1] = l_b[0].link_loop_next
            l_b[2] = l_b[1].link_loop_next
            l_b[3] = l_b[2].link_loop_next

        l_a_uv = [l[uv_act].uv for l in l_a]
        l_b_uv = [l[uv_act].uv for l in l_b]

        if EXTEND_MODE == 'LENGTH_AVERAGE':
            fac = edge_lengths[l_b[2].edge.index][0] / edge_lengths[l_a[1].edge.index][0]
        elif EXTEND_MODE == 'LENGTH':
            a0, b0, c0 = l_a[3].vert.co, l_a[0].vert.co, l_b[3].vert.co
            a1, b1, c1 = l_a[2].vert.co, l_a[1].vert.co, l_b[2].vert.co

            d1 = (a0 - b0).length + (a1 - b1).length
            d2 = (b0 - c0).length + (b1 - c1).length
            try:
                fac = d2 / d1
            except ZeroDivisionError:
                fac = 1.0
        else:
            fac = 1.0

        extrapolate_uv(fac,
                       l_a_uv[3], l_a_uv[0],
                       l_b_uv[3], l_b_uv[0])

        extrapolate_uv(fac,
                       l_a_uv[2], l_a_uv[1],
                       l_b_uv[2], l_b_uv[1])

    # -------------------------------------------
    # Calculate average length per loop if needed

    if EXTEND_MODE == 'LENGTH_AVERAGE':
        bm.edges.index_update()
        edge_lengths = [None] * len(bm.edges)  # NoneType times the length of edges list

        for f in faces:
            # we know its a quad
            l_quad = f.loops[:]
            l_pair_a = (l_quad[0], l_quad[2])
            l_pair_b = (l_quad[1], l_quad[3])

            for l_pair in (l_pair_a, l_pair_b):
                if edge_lengths[l_pair[0].edge.index] is None:

                    edge_length_store = [-1.0]
                    edge_length_accum = 0.0
                    edge_length_total = 0

                    for l in l_pair:
                        if edge_lengths[l.edge.index] is None:
                            for e in walk_edgeloop(l):
                                if edge_lengths[e.index] is None:
                                    edge_lengths[e.index] = edge_length_store
                                    edge_length_accum += e.calc_length()
                                    edge_length_total += 1

                    edge_length_store[0] = edge_length_accum / edge_length_total

    # done with average length
    # ------------------------

    walk_face_init(faces, f_act)
    for f_triple in walk_face(f_act):
        apply_uv(*f_triple)

    bmesh.update_edit_mesh(me, False)

'''----------------------------------'''


def SuccessFinished(me, startTime):
    # use for backtrack of steps
    # bpy.ops.ed.undo_push()
    bmesh.update_edit_mesh(me)
    # elapsed = round(time.clock()-startTime, 2)
    # if (elapsed >= 0.05): operator.report({'INFO'}, "UvSquares finished, elapsed:", elapsed, "s.")
    return


def SymmetrySelected(axis, pivot="MEDIAN"):
    last_pivot = bpy.context.space_data.pivot_point
    bpy.context.space_data.pivot_point = pivot
    bpy.ops.transform.mirror(constraint_axis=(True, False, False), constraint_orientation='GLOBAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    bpy.context.space_data.pivot_point = last_pivot
    return


def AreVectsLinedOnAxis(verts):
    areLinedX = True
    areLinedY = True
    allowedError = 0.0009
    valX = verts[0].uv.x
    valY = verts[0].uv.y
    for v in verts:
        if abs(valX - v.uv.x) > allowedError:
            areLinedX = False
        if abs(valY - v.uv.y) > allowedError:
            areLinedY = False
    return areLinedX or areLinedY


def MakeEqualDistanceBetweenVertsInLine(filteredVerts, vertsDict, startv=None):
    verts = filteredVerts
    verts.sort(key=lambda x: x.uv[0])  # sort by .x

    first = verts[0].uv
    last = verts[len(verts) - 1].uv

    horizontal = True
    if ((last.x - first.x) > 0.0009):
        slope = (last.y - first.y) / (last.x - first.x)
        if (slope > 1) or (slope < -1):
            horizontal = False
    else:
        horizontal = False

    if horizontal is True:
        length = hypot(first.x - last.x, first.y - last.y)

        if startv is last:
            currentX = last.x - length
            currentY = last.y
        else:
            currentX = first.x
            currentY = first.y
    else:
        verts.sort(key=lambda x: x.uv[1])  # sort by .y
        verts.reverse()  # reverse because y values drop from up to down
        first = verts[0].uv
        last = verts[len(verts) - 1].uv

        length = hypot(first.x - last.x, first.y - last.y)  # we have to call length here because if it is not Hor first and second can not actually be first and second

        if startv is last:
            currentX = last.x
            currentY = last.y + length

        else:
            currentX = first.x
            currentY = first.y

    numberOfVerts = len(verts)
    finalScale = length / (numberOfVerts - 1)

    if horizontal is True:
        first = verts[0]
        last = verts[len(verts) - 1]

        for v in verts:
            v = v.uv
            x = round(v.x, precision)
            y = round(v.y, precision)

            for vert in vertsDict[(x, y)]:
                vert.uv.x = currentX
                vert.uv.y = currentY

            currentX = currentX + finalScale
    else:
        for v in verts:
            x = round(v.uv.x, precision)
            y = round(v.uv.y, precision)

            for vert in vertsDict[(x, y)]:
                vert.uv.x = currentX
                vert.uv.y = currentY

            currentY = currentY - finalScale
    return


def VertsDictForLine(uv_layer, bm, selVerts, vertsDict):
    for f in bm.faces:
        for l in f.loops:
            luv = l[uv_layer]
            if luv.select is True:
                x = round(luv.uv.x, precision)
                y = round(luv.uv.y, precision)

                vertsDict[(x, y)].append(luv)
    return


def ScaleTo0OnAxisAndCursor(filteredVerts, vertsDict, startv=None, horizontal=None):

    verts = filteredVerts
    verts.sort(key=lambda x: x.uv[0])  # sort by .x

    first = verts[0]
    last = verts[len(verts) - 1]

    if horizontal is None:
        horizontal = True
        if ((last.uv.x - first.uv.x) > 0.0009):
            slope = (last.uv.y - first.uv.y) / (last.uv.x - first.uv.x)
            if (slope > 1) or (slope < -1):
                horizontal = False
        else:
            horizontal = False

    if horizontal is True:
        if startv is None:
            startv = first

        SetAll2dCursorsTo(startv.uv.x, startv.uv.y)
        # scale to 0 on Y
        ScaleTo0('Y')
        return

    else:
        verts.sort(key=lambda x: x.uv[1])  # sort by .y
        verts.reverse()  # reverse because y values drop from up to down
        first = verts[0]
        last = verts[len(verts) - 1]
        if startv is None:
            startv = first

        SetAll2dCursorsTo(startv.uv.x, startv.uv.y)
        # scale to 0 on X
        ScaleTo0('X')
        return


def ScaleTo0(axis):
    last_area = bpy.context.area.type
    bpy.context.area.type = 'IMAGE_EDITOR'
    last_pivot = bpy.context.space_data.pivot_point
    bpy.context.space_data.pivot_point = 'CURSOR'

    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            if axis is 'Y':
                bpy.ops.transform.resize(value=(1, 0, 1), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
            else:
                bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    bpy.context.space_data.pivot_point = last_pivot
    return


def hypotVert(v1, v2):
    hyp = hypot(v1.x - v2.x, v1.y - v2.y)
    return hyp


def Corners(corners):
    firstHighest = corners[0]
    for c in corners:
        if c.uv.y > firstHighest.uv.y:
            firstHighest = c
    corners.remove(firstHighest)

    secondHighest = corners[0]
    for c in corners:
        if (c.uv.y > secondHighest.uv.y):
            secondHighest = c

    if firstHighest.uv.x < secondHighest.uv.x:
        leftUp = firstHighest
        rightUp = secondHighest
    else:
        leftUp = secondHighest
        rightUp = firstHighest
    corners.remove(secondHighest)

    firstLowest = corners[0]
    secondLowest = corners[1]

    if firstLowest.uv.x < secondLowest.uv.x:
        leftDown = firstLowest
        rightDown = secondLowest
    else:
        leftDown = secondLowest
        rightDown = firstLowest

    return leftUp, leftDown, rightUp, rightDown


def ImageRatio():
    ratioX, ratioY = 256, 256
    for a in bpy.context.screen.areas:
        if a.type == 'IMAGE_EDITOR':
            img = a.spaces[0].image
            if img is not None and img.size[0] is not 0:
                ratioX, ratioY = img.size[0], img.size[1]
            break
    return ratioX, ratioY


def CursorClosestTo(verts, allowedError=0.025):
    ratioX, ratioY = ImageRatio()

    # any length that is certantly not smaller than distance of the closest
    min = 1000
    minV = verts[0]
    for v in verts:
        if v is None:
            continue
        for area in bpy.context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                loc = area.spaces[0].cursor_location
                hyp = hypot(loc.x / ratioX - v.uv.x, loc.y / ratioY - v.uv.y)
                if (hyp < min):
                    min = hyp
                    minV = v

    if min is not 1000:
        return minV
    return None


def SetAll2dCursorsTo(x, y):
    last_area = bpy.context.area.type
    bpy.context.area.type = 'IMAGE_EDITOR'

    bpy.ops.uv.cursor_set(location=(x, y))

    bpy.context.area.type = last_area
    return


def RotateSelected(angle, pivot=None):
    if pivot is None:
        pivot = "MEDIAN"

    last_area = bpy.context.area.type
    bpy.context.area.type = 'IMAGE_EDITOR'

    last_pivot = bpy.context.space_data.pivot_point
    bpy.context.space_data.pivot_point = pivot

    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            bpy.ops.transform.rotate(value=radians(angle), axis=(-0, -0, -1), constraint_axis=(False, False, False), constraint_orientation='LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
            break

    bpy.context.space_data.pivot_point = last_pivot
    bpy.context.area.type = last_area

    return


def AreVertsQuasiEqual(v1, v2, allowedError=0.0009):
    if abs(v1.uv.x - v2.uv.x) < allowedError and abs(v1.uv.y - v2.uv.y) < allowedError:
        return True
    return False


def RipUvFaces(context, operator):
    startTime = time.clock()

    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    uv_layer = bm.loops.layers.uv.verify()
    bm.faces.layers.tex.verify()  # currently blender needs both layers.

    selFaces = []

    for f in bm.faces:
        isFaceSel = True
        for l in f.loops:
            luv = l[uv_layer]
            if luv.select is False:
                isFaceSel = False
                break

        if isFaceSel is True:
            selFaces.append(f)

    if len(selFaces) is 0:
        target = None
        for f in bm.faces:
            for l in f.loops:
                luv = l[uv_layer]
                if luv.select is True:
                    target = luv
                    break
            if target is not None:
                break

        for f in bm.faces:
            for l in f.loops:
                luv = l[uv_layer]
                luv.select = False

        target.select = True
        return SuccessFinished(me, startTime)

    DeselectAll()

    for sf in selFaces:
        for l in sf.loops:
            luv = l[uv_layer]
            luv.select = True
    return SuccessFinished(me, startTime)


def JoinUvFaces(context, operator):
    startTime = time.clock()

    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    uv_layer = bm.loops.layers.uv.verify()
    bm.faces.layers.tex.verify()  # currently blender needs both layers.

    vertsDict = defaultdict(list)  # dict

    # TODO: radius by image scale
    radius = 0.02

    for f in bm.faces:
        for l in f.loops:
            luv = l[uv_layer]
            if luv.select is True:
                x = round(luv.uv.x, precision)
                y = round(luv.uv.y, precision)
                vertsDict[(x, y)].append(luv)

    for key in vertsDict:
        min = 1000
        minV = None

        for f in bm.faces:
            for l in f.loops:
                luv = l[uv_layer]
                if luv.select is False:
                    hyp = hypot(vertsDict[(key[0], key[1])][0].uv.x - luv.uv.x, vertsDict[(key[0], key[1])][0].uv.y - luv.uv.y)
                    if (hyp <= min) and hyp < radius:
                        min = hyp
                        minV = luv
                        minV.select = True

            if min is not 1000:
                for v in vertsDict[(key[0], key[1])]:
                    v = v.uv
                    v.x = minV.uv.x
                    v.y = minV.uv.y

    return SuccessFinished(me, startTime)


def DeselectAll():
    bpy.ops.uv.select_all(action='DESELECT')
    return


class UvSquares(bpy.types.Operator):
    """Reshapes UV faces to a grid of equivalent squares"""
    bl_idname = "uv.uv_squares"
    bl_label = "UVs to grid of squares"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        main(context, self, True)
        return {'FINISHED'}


class UvSquaresByShape(bpy.types.Operator):
    """Reshapes UV faces to a grid with respect to shape by length of edges around selected corner"""
    bl_idname = "uv.uv_squares_by_shape"
    bl_label = "UVs to grid with respect to shape"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        main(context, self)
        return {'FINISHED'}


class RipFaces(bpy.types.Operator):
    """Rip UV faces and vertices apart / press [G] to move"""
    bl_idname = "uv.uv_face_rip"
    bl_label = "UV face rip"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        RipUvFaces(context, self)
        return {'FINISHED'}


class JoinFaces(bpy.types.Operator):
    """Join selected UV faces to closest nonselected vertices"""
    bl_idname = "uv.uv_face_join"
    bl_label = "UV face join"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        JoinUvFaces(context, self)
        return {'FINISHED'}


class SnapToAxis(bpy.types.Operator):
    """Snap sequenced vertices to Axis"""
    bl_idname = "uv.uv_snap_to_axis"
    bl_label = "UV snap vertices to axis"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        main(context, self)
        return {'FINISHED'}


class SnapToAxisWithEqual(bpy.types.Operator):
    """Snap sequenced vertices to Axis with Equal Distance between"""
    bl_idname = "uv.uv_snap_to_axis_and_equal"
    bl_label = "UV snap vertices to axis with equal distance between"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')

    def execute(self, context):
        main(context, self)
        main(context, self)
        return {'FINISHED'}

addon_keymaps = []


def menu_func_uv_squares(self, context): self.layout.operator(UvSquares.bl_idname)


def menu_func_uv_squares_by_shape(self, context): self.layout.operator(UvSquaresByShape.bl_idname)


def menu_func_face_rip(self, context): self.layout.operator(RipFaces.bl_idname)


def menu_func_face_join(self, context): self.layout.operator(JoinFaces.bl_idname)
"""
class UvSquaresPanel(bpy.types.Panel):
    # UvSquares Panel
    bl_label = "UV Squares"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Select Sequenced Vertices to:")
        split = layout.split()
        col = split.column(align=True)
        col.operator(SnapToAxis.bl_idname, text="Snap to Axis (X or Y)", icon = "ARROW_LEFTRIGHT")
        col.operator(SnapToAxisWithEqual.bl_idname, text="Snap with Equal Distance", icon = "ALIGN")

        row = layout.row()
        row.label(text="Convert \"Rectangle\" (4 corners):")
        split = layout.split()
        col = split.column(align=True)
        col.operator(UvSquaresByShape.bl_idname, text="To Grid By Shape", icon = "GRID")
        col.operator(UvSquares.bl_idname, text="To Square Grid", icon = "UV_FACESEL")

        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True)

        row = layout.row()

        row.label(text="Select Faces or Vertices to:")
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True)

        row.operator(RipFaces.bl_idname, text="Rip Vertex", icon = "LAYER_ACTIVE")
        row.operator(RipFaces.bl_idname, text="Rip Faces", icon = "UV_ISLANDSEL")
        col.operator(JoinFaces.bl_idname, text="Snap to Closest Unselected", icon = "SNAP_INCREMENT")
        row = layout.row()
        row.label(text="V - Join (Stitch), I -Toggle Islands")

"""
#############------------------------------------------------------------------------------------------######################
#############------------------------------------------------------------------------------------------######################
#############------------------------------------------------------------------------------------------######################
#############------------------------------------------------------------------------------------------######################
#############################################################################################################################
#############################################################################################################################


def register():

    bpy.utils.register_class(uvtools)
    bpy.utils.register_class(imagetools)

    bpy.utils.register_class(AlignSXMargin)
    bpy.utils.register_class(AlignRxMargin)
    bpy.utils.register_class(AlignVAxis)
    bpy.utils.register_class(AlignTopMargin)
    bpy.utils.register_class(AlignLowMargin)
    bpy.utils.register_class(AlignHAxis)

    # bpy.utils.register_class(UvSquaresPanel)
    bpy.utils.register_class(UvSquares)
    bpy.utils.register_class(UvSquaresByShape)
    bpy.utils.register_class(RipFaces)
    bpy.utils.register_class(JoinFaces)
    bpy.utils.register_class(SnapToAxis)
    bpy.utils.register_class(SnapToAxisWithEqual)

    # menu
    bpy.types.IMAGE_MT_uvs.append(menu_func_uv_squares)
    bpy.types.IMAGE_MT_uvs.append(menu_func_uv_squares_by_shape)
    bpy.types.IMAGE_MT_uvs.append(menu_func_face_rip)
    bpy.types.IMAGE_MT_uvs.append(menu_func_face_join)

    # handle the keymap
    wm = bpy.context.window_manager

    km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
    kmi = km.keymap_items.new(UvSquaresByShape.bl_idname, 'E', 'PRESS', alt=True)
    addon_keymaps.append((km, kmi))

    km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
    kmi = km.keymap_items.new(RipFaces.bl_idname, 'V', 'PRESS', alt=True)
    addon_keymaps.append((km, kmi))

    km = wm.keyconfigs.addon.keymaps.new(name='UV Editor', space_type='EMPTY')
    kmi = km.keymap_items.new(JoinFaces.bl_idname, 'V', 'PRESS', alt=True, shift=True)
    addon_keymaps.append((km, kmi))

    bpy.utils.register_module(__name__)
    pass


def unregister():

    bpy.utils.unregister_class(uvtools)
    bpy.utils.unregister_class(imagetools)

    bpy.utils.unregister_class(AlignSXMargin)
    bpy.utils.unregister_class(AlignRxMargin)
    bpy.utils.unregister_class(AlignVAxis)
    bpy.utils.unregister_class(AlignTopMargin)
    bpy.utils.unregister_class(AlignLowMargin)

    # bpy.utils.unregister_class(UvSquaresPanel)
    bpy.utils.unregister_class(UvSquares)
    bpy.utils.unregister_class(UvSquaresByShape)
    bpy.utils.unregister_class(RipFaces)
    bpy.utils.unregister_class(JoinFaces)
    bpy.utils.unregister_class(SnapToAxis)
    bpy.utils.unregister_class(SnapToAxisWithEqual)

    bpy.types.IMAGE_MT_uvs.remove(menu_func_uv_squares)
    bpy.types.IMAGE_MT_uvs.remove(menu_func_uv_squares_by_shape)
    bpy.types.IMAGE_MT_uvs.remove(menu_func_face_rip)
    bpy.types.IMAGE_MT_uvs.remove(menu_func_face_join)

    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    # clear the list
    addon_keymaps.clear()

    bpy.utils.unregister_module(__name__)
    pass
    try:
        del bpy.types.WindowManager.retopowindowtool
    except:
        pass

if __name__ == "__main__":
    register()
