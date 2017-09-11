bl_info = {
    'name': 'Select Tools',
    'author': 'Jakub Bełcik',
    'version': (1, 0, 1),
    'blender': (2, 7, 3),
    'location': '3D View > Tools',
    'description': 'Selection Tools',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Panel'
}

import bpy
from bpy.props import StringProperty, FloatProperty, BoolProperty, EnumProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
import mathutils
from mathutils import Vector
from .utils import AddonPreferences, SpaceProperty, operator_call


def rendershowselected():
    for ob in bpy.data.objects:
        if ob.select == True:
            ob.hide_render = False


def renderhideselected():
    for ob in bpy.data.objects:
        if ob.select == True:
            ob.hide_render = True


class ShowHideObject(bpy.types.Operator):
    bl_idname = 'opr.show_hide_object'
    bl_label = 'Show/Hide Object'
    bl_description = 'Show/hide selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.select:
                if i.hide:
                    i.hide = False
                    i.hide_select = False
                    i.hide_render = False
                else:
                    i.hide = True
                    i.select = False

                    if i.type not in ['CAMERA', 'LAMP']:
                        i.hide_render = True
        return {'FINISHED'}


class ShowAllObjects(bpy.types.Operator):
    bl_idname = 'opr.show_all_objects'
    bl_label = 'Show All Objects'
    bl_description = 'Show all objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for i in bpy.data.objects:
            i.hide = False
            i.hide_select = False
            i.hide_render = False
        return {'FINISHED'}


class HideAllObjects(bpy.types.Operator):
    bl_idname = 'opr.hide_all_objects'
    bl_label = 'Hide All Objects'
    bl_description = 'Hide all inactive objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            for i in bpy.data.objects:
                i.hide = True
                i.select = False

                if i.type not in ['CAMERA', 'LAMP']:
                    i.hide_render = True
        else:
            obj_name = context.object.name

            for i in bpy.data.objects:
                if i.name != obj_name:
                    i.hide = True
                    i.select = False

                    if i.type not in ['CAMERA', 'LAMP']:
                        i.hide_render = True

        return {'FINISHED'}


class SelectAll(bpy.types.Operator):
    bl_idname = 'opr.select_all'
    bl_label = '(De)select All'
    bl_description = '(De)select all objects, verticies, edges or faces'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            bpy.ops.object.select_all(action='TOGGLE')
        elif context.object.mode == 'EDIT':
            bpy.ops.mesh.select_all(action='TOGGLE')
        elif context.object.mode == 'OBJECT':
            bpy.ops.object.select_all(action='TOGGLE')
        else:
            self.report({'ERROR'}, 'Cannot perform this operation in this mode')
            return {'CANCELLED'}

        return {'FINISHED'}


class InverseSelection(bpy.types.Operator):
    bl_idname = 'opr.inverse_selection'
    bl_label = 'Inverse Selection'
    bl_description = 'Inverse selection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            bpy.ops.object.select_all(action='INVERT')
        elif context.object.mode == 'EDIT':
            bpy.ops.mesh.select_all(action='INVERT')
        elif context.object.mode == 'OBJECT':
            bpy.ops.object.select_all(action='INVERT')
        else:
            self.report({'ERROR'}, 'Cannot perform this operation in this mode')
            return {'CANCELLED'}

        return {'FINISHED'}


class LoopMultiSelect(bpy.types.Operator):
    bl_idname = 'opr.loop_multi_select'
    bl_label = 'Edge Loop Select'
    bl_description = 'Select a loop of connected edges'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.loop_multi_select(ring=False)
        return {'FINISHED'}


class DeleteVerts(bpy.types.Operator):
    bl_idname = 'opr.delete_verts'
    bl_label = 'Delete Vertices'
    bl_description = 'Delete selected vertices'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='VERT')
        return {'FINISHED'}


class DeleteEdges(bpy.types.Operator):
    bl_idname = 'opr.delete_edges'
    bl_label = 'Delete Edges'
    bl_description = 'Delete selected edges'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='EDGE')
        return {'FINISHED'}


class DeleteFaces(bpy.types.Operator):
    bl_idname = 'opr.delete_faces'
    bl_label = 'Delete Faces'
    bl_description = 'Delete selected faces'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'}


class DeleteOnlyFaces(bpy.types.Operator):
    bl_idname = 'opr.delete_only_faces'
    bl_label = 'Delete Only Faces'
    bl_description = 'Delete only selected faces'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='ONLY_FACE')
        return {'FINISHED'}


class DeleteOnlyEdgesFaces(bpy.types.Operator):
    bl_idname = 'opr.delete_only_edges_faces'
    bl_label = 'Delete Only Edges & Faces'
    bl_description = 'Delete only selected edges & faces'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != 'EDIT':
            self.report({'ERROR'}, 'This operation can be performed only in edit mode')
            return {'CANCELLED'}

        bpy.ops.mesh.delete(type='EDGE_FACE')
        return {'FINISHED'}


class ShowRenderAllSelected(bpy.types.Operator):  # nb: CamelCase
    bl_idname = "op.render_show_all_selected"  # nb underscore_case
    bl_label = "Render On"
    bl_description = 'Render all objects'
    trigger = BoolProperty(default=False)
    mode = BoolProperty(default=False)

    def execute(self, context):
        rendershowselected()
        return {'FINISHED'}


class HideRenderAllSelected(bpy.types.Operator):
    bl_idname = "op.render_hide_all_selected"
    bl_label = "Render Off"
    bl_description = 'Hide Selected Object(s) from Render'
    trigger = BoolProperty(default=False)
    mode = BoolProperty(default=False)

    def execute(self, context):
        renderhideselected()
        return {'FINISHED'}


class Selection(bpy.types.Panel):
    bl_idname = 'pan.selection'
    bl_label = 'Selection'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.alignment = 'LEFT'
        if context.object != None:
            if context.object.mode == 'OBJECT':
                layout.operator('opr.show_hide_object', text='Show/Hide', icon='GHOST_ENABLED')

        layout.operator('opr.show_all_objects', text='Show All', icon='RESTRICT_VIEW_OFF')
        layout.operator('opr.hide_all_objects', text='Hide All', icon='RESTRICT_VIEW_ON')
        row = layout.row(align=True)
        row.operator("op.render_show_all_selected", icon='RESTRICT_VIEW_OFF')
        row.operator("op.render_hide_all_selected", icon='RESTRICT_VIEW_ON')
        row = layout.row(align=True)
        if context.object != None:
            if context.object.mode == 'OBJECT':
                layout.operator('opr.select_all', icon='MOD_MESHDEFORM')
                layout.operator('opr.inverse_selection', icon='MOD_REMESH')
                row = layout.row(align=True)
                row.operator('view3d.select_border', icon='MESH_PLANE')
                row.operator('view3d.select_circle', icon='MESH_CIRCLE')
                row = layout.row(align=True)
                row.operator('object.duplicate_move', text='Duplicate', icon='MOD_ARRAY')
                row.operator('object.delete', text='Delete', icon='X')

            if context.object.type == 'MESH':
                if context.object.mode == 'EDIT':
                    layout.operator('opr.select_all', icon='MOD_MESHDEFORM')
                    layout.operator('opr.inverse_selection', icon='MOD_REMESH')
                    layout.operator('view3d.select_border', icon='MESH_PLANE')
                    layout.operator('view3d.select_circle', icon='MESH_CIRCLE')
                    layout.operator('mesh.select_linked', icon='ROTATECOLLECTION')
                    layout.operator('opr.loop_multi_select', icon='OUTLINER_DATA_MESH')
                    layout.operator('mesh.fill', icon='MOD_TRIANGULATE')
                    layout.operator('mesh.duplicate_move', text='Duplicate', icon='MOD_ARRAY')
                    layout.operator('opr.delete_verts', icon='VERTEXSEL')
                    layout.operator('opr.delete_edges', icon='EDGESEL')
                    layout.operator('opr.delete_faces', icon='FACESEL')
                    layout.operator('opr.delete_only_faces', icon='SNAP_FACE')
                    layout.operator('opr.delete_only_edges_faces', icon='SNAP_VOLUME')
        else:
            layout.operator('opr.select_all', icon='MOD_MESHDEFORM')
            layout.operator('opr.inverse_selection', icon='MOD_REMESH')
            layout.operator('view3d.select_border', icon='MESH_PLANE')
            layout.operator('view3d.select_circle', icon='MESH_CIRCLE')

# register


def register():

    bpy.utils.register_class(ShowHideObject)
    bpy.utils.register_class(ShowAllObjects)
    bpy.utils.register_class(HideAllObjects)
    bpy.utils.register_class(ShowRenderAllSelected)
    bpy.utils.register_class(HideRenderAllSelected)
    bpy.utils.register_class(SelectAll)
    bpy.utils.register_class(InverseSelection)
    bpy.utils.register_class(LoopMultiSelect)
    bpy.utils.register_class(DeleteVerts)
    bpy.utils.register_class(DeleteEdges)
    bpy.utils.register_class(DeleteFaces)
    bpy.utils.register_class(DeleteOnlyFaces)
    bpy.utils.register_class(DeleteOnlyEdgesFaces)
    bpy.utils.register_class(Selection)


def unregister():
    bpy.utils.unregister_class(ShowHideObject)
    bpy.utils.unregister_class(ShowAllObjects)
    bpy.utils.unregister_class(HideAllObjects)
    bpy.utils.unregister_class(ShowRenderAllSelected)
    bpy.utils.unregister_class(HideRenderAllSelected)
    bpy.utils.unregister_class(SelectAll)
    bpy.utils.unregister_class(InverseSelection)
    bpy.utils.unregister_class(LoopMultiSelect)
    bpy.utils.unregister_class(DeleteVerts)
    bpy.utils.unregister_class(DeleteEdges)
    bpy.utils.unregister_class(DeleteFaces)
    bpy.utils.unregister_class(DeleteOnlyFaces)
    bpy.utils.unregister_class(DeleteOnlyEdgesFaces)
    bpy.utils.unregister_class(Selection)


if __name__ == '__main__':
    register()
