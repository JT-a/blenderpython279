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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#
# ***** END GPL LICENCE BLOCK *****


import bpy
from bpy import*


#######  Menus Snap to  ##########

class SnaptoCursor(bpy.types.Menu):
    """Snap Cursor to..."""
    bl_label = "Snap to Menu"
    bl_idname = "wkst.snaptocursor"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.label("Snap Cursor to...")
        layout.separator()
        layout.operator("view3d.snap_cursor_to_grid", text="Grid")
        layout.operator("view3d.snap_cursor_to_active", text="Active")
        layout.operator("view3d.snap_cursor_to_center", text="Center")
        layout.operator("view3d.snap_cursor_to_selected", text="Selected")

        obj = context
        if obj and obj.mode == "EDIT_MESH":
            layout.separator()
            layout.operator("mesh.circlecentercursor", "3Point Circle")
            layout.operator("view3d.snap_cursor_to_edge_intersection", text="Edge Intersection")

bpy.utils.register_class(SnaptoCursor)


class SnaptoSelect(bpy.types.Menu):
    """Snap Selection to..."""
    bl_label = "Snap to Menu"
    bl_idname = "wkst.snaptoselect"

    def draw(self, context):

        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.label("Snap Selection to...")
        layout.separator()

        layout.operator("view3d.snap_selected_to_grid", text="Grid")
        layout.operator("view3d.snap_selected_to_cursor", text="Cursor")
        layout.operator("view3d.snap_selected_to_cursor", "Cursor (offset)").use_offset = True
        layout.operator("mesh.snapcenteroffset", "Center (offset)")

bpy.utils.register_class(SnaptoSelect)


#######  Menus Snap Setting ###

class SnapType(bpy.types.Menu):
    bl_label = "Snap Type"
    bl_idname = "wkst.snaptype"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mesh = context.active_object.data

        settings = context.tool_settings
        view = context.space_data
        toolsettings = context.tool_settings

        snap_meta = toolsettings.use_snap

        layout.operator("snape.increment", "Increment", icon="SNAP_INCREMENT")
        layout.operator("snape.vertex", "Vertex", icon="SNAP_VERTEX")
        layout.operator("snape.edge", "Edge", icon="SNAP_EDGE")
        layout.operator("snape.face", "Face", icon="SNAP_FACE")
        layout.operator("snape.volume", "Volume", icon="SNAP_VOLUME")

bpy.utils.register_class(SnapType)


class SnapTarget(bpy.types.Menu):
    bl_label = "Snap Target"
    bl_idname = "wkst.snaptarget"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mesh = context.active_object.data

        settings = context.tool_settings
        view = context.space_data
        toolsettings = context.tool_settings

        snap_meta = toolsettings.use_snap

        layout.operator("snap.closest", "Closest")
        layout.operator("snap.center", "Center")
        layout.operator("snap.median", "Median")
        layout.operator("snap.active", "Active")

bpy.utils.register_class(SnapTarget)


class SnapOption(bpy.types.Menu):
    bl_label = "Snap Option"
    bl_idname = "wkst.snapoption"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mesh = context.active_object.data

        settings = context.tool_settings
        view = context.space_data
        toolsettings = context.tool_settings

        snap_meta = toolsettings.use_snap

        if snap_meta == False:
            layout.operator("wm.context_toggle", text="Snap on/off", icon="CHECKBOX_DEHLT").data_path = "tool_settings.use_snap"
        else:
            layout.operator("wm.context_toggle", text="Snap on/off", icon="CHECKBOX_HLT").data_path = "tool_settings.use_snap"

        if obj and obj.mode == 'EDIT':
            layout.prop(toolsettings, "use_mesh_automerge", text="Auto-Merge", icon='AUTOMERGE_ON')

        if obj and obj.mode == 'OBJECT':
            layout.prop(toolsettings, "use_snap_align_rotation", text="Snap Normal", icon="SNAP_NORMAL")

        if obj and obj.mode == 'EDIT':
            layout.prop(toolsettings, "use_snap_self", text="Snap Self", icon="ORTHO")
            layout.prop(toolsettings, "use_snap_project", text="Snap Projection", icon="RETOPO")

bpy.utils.register_class(SnapOption)


# -------------------------------------------------------

def abs(val):
    if val > 0:
        return val
    return -val


def edgeIntersect(context, operator):
    from mathutils.geometry import intersect_line_line

    obj = context.active_object

    if (obj.type != "MESH"):
        operator.report({'ERROR'}, "Object must be a mesh")
        return None

    edges = []
    mesh = obj.data
    verts = mesh.vertices

    is_editmode = (obj.mode == 'EDIT')
    if is_editmode:
        bpy.ops.object.mode_set(mode='OBJECT')

    for e in mesh.edges:
        if e.select:
            edges.append(e)

            if len(edges) > 2:
                break

    if is_editmode:
        bpy.ops.object.mode_set(mode='EDIT')

    if len(edges) != 2:
        operator.report({'ERROR'},
                        "Operator requires exactly 2 edges to be selected")
        return

    line = intersect_line_line(verts[edges[0].vertices[0]].co,
                               verts[edges[0].vertices[1]].co,
                               verts[edges[1].vertices[0]].co,
                               verts[edges[1].vertices[1]].co)

    if line is None:
        operator.report({'ERROR'}, "Selected edges do not intersect")
        return

    point = line[0].lerp(line[1], 0.5)
    context.scene.cursor_location = obj.matrix_world * point


class VIEW3D_OT_CursorToEdgeIntersection(bpy.types.Operator):
    "Finds the mid-point of the shortest distance between two edges"
    bl_idname = "view3d.snap_cursor_to_edge_intersection"
    bl_label = "Cursor to Edge Intersection"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj != None and obj.type == 'MESH'

    def execute(self, context):
        edgeIntersect(context, self)
        return {'FINISHED'}


class VIEW3D_OT_CursorToEdgeIntersection(bpy.types.Operator):
    "Finds the mid-point of the shortest distance between two edges"
    bl_idname = "view3d.snap_cursor_to_edge_intersection"
    bl_label = "Cursor to Edge Intersection"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj != None and obj.type == 'MESH'

    def execute(self, context):
        edgeIntersect(context, self)
        return {'FINISHED'}

# bpy.utils.register_class(VIEW3D_OT_CursorToEdgeIntersection)


# REGISTER

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
