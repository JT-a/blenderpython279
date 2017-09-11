bl_info = {
    'name': 'Transform op',
    'author': 'Jakub Belcik',
    'version': (1, 0),
    'blender': (2, 7, 3),
    'location': '3D View > Tools > ',
    'description': '',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'category': '3D View'
}


import bpy
from bpy.props import StringProperty, FloatProperty, BoolProperty, EnumProperty, IntProperty
from bpy_extras.io_utils import ImportHelper

import mathutils


def f_clear_loc(self, context):
    obj_name = context.object.name

    if context.object.type != 'MESH':
        return None

    if context.object.mode != 'OBJECT':
        return None

    if context.object.hide:
        return None

    for i in bpy.data.objects:
        if i.name != obj_name:
            i.select = False

    bpy.ops.object.location_clear()

    return None


def f_delta_scale_xyz(self, context):
    if context.object.mode != 'OBJECT':
        return None

    if context.object.hide:
        return None

    obj_name = context.object.name
    obj = bpy.data.objects[obj_name]

    obj.delta_scale.xyz = obj.delta_scale_xyz

    return None


class ClearLoc(bpy.types.Operator):
    bl_idname = 'opr.clear_loc'
    bl_label = 'Reset Location'
    bl_description = 'Reset the object\'s location'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.location_clear()

        return {'FINISHED'}


class ApplyLoc(bpy.types.Operator):
    bl_idname = 'opr.apply_loc'
    bl_label = 'Apply Location'
    bl_description = 'Apply the object\'s location'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

        return {'FINISHED'}


class ClearRot(bpy.types.Operator):
    bl_idname = 'opr.clear_rot'
    bl_label = 'Reset Rotation'
    bl_description = 'Reset the object\'s rotation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.rotation_clear()

        return {'FINISHED'}


class ApplyRot(bpy.types.Operator):
    bl_idname = 'opr.apply_rot'
    bl_label = 'Apply Rotation'
    bl_description = 'Apply the object\'s rotation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        return {'FINISHED'}


class ClearScl(bpy.types.Operator):
    bl_idname = 'opr.clear_scl'
    bl_label = 'Reset Scale'
    bl_description = 'Reset the object\'s scale'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.scale_clear()

        context.scene.objects[obj_name].delta_scale.xyz = 1.0
        obj.delta_scale.xyz = 1.0
        context.object.delta_scale.xyz = 1.0

        return {'FINISHED'}


class ApplyScl(bpy.types.Operator):
    bl_idname = 'opr.apply_scl'
    bl_label = 'Apply Scale'
    bl_description = 'Apply the object\'s scale'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object == None:
            self.report({'ERROR'}, 'Cannot perform this operation on NoneType objects')
            return {'CANCELLED'}

        if context.object.type != 'MESH':
            self.report({'ERROR'}, 'This operation can be performed only on MeshType objects')
            return {'CANCELLED'}

        if context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'This operation can be performed only in object mode')
            return {'CANCELLED'}

        if context.object.hide:
            self.report({'ERROR'}, 'Cannot perform this operation on hidden objects')
            return {'CANCELLED'}

        obj_name = context.object.name
        obj = bpy.data.objects[obj_name]

        if not obj.select:
            self.report({'ERROR'}, 'Select active object')
            return {'CANCELLED'}

        for i in bpy.data.objects:
            if i.name != obj_name:
                i.select = False

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        context.scene.objects[obj_name].delta_scale.xyz = 1.0
        obj.delta_scale.xyz = 1.0
        context.object.delta_scale.xyz = 1.0

        return {'FINISHED'}


class Transform(bpy.types.Panel):
    bl_idname = 'pan.transform'
    bl_label = 'Transform'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Analyse DICOM'
    bl_options = {'DEFAULT_CLOSED'}

    bpy.types.Object.delta_scale_xyz = FloatProperty(options={'HIDDEN'}, name='XYZ', min=0.0, max=20.0, step=1, default=1.0, update=f_delta_scale_xyz,
                                                     description='Proportional scaling in every direction')

    def draw(self, context):
        layout = self.layout

        if context.object != None:
            obj_name = context.object.name
            obj = bpy.data.objects[obj_name]

            if	obj_name[-12 : -2] != '.Intersection'	and obj_name[-16 : -5] != '.Intersection.'		and obj_name[-17 : -6] != '.Intersection.' \
                    and obj_name[-13: -2] != '.Dissection' and obj_name[-17: -5] != '.Dissection.' and obj_name[-18: -6] != '.Dissection.':
                box = layout.box()
                col = box.column()
                col.label(text='Name:')
                col.prop(obj, 'name', text='')

            if not context.object.hide:
                if context.object.mode != 'EDIT':
                    box = layout.box()
                    col = box.column()
                    col.prop(context.object, 'location')

                    col = box.column()
                    spl = col.split(0.5)
                    col = spl.column()
                    col.operator('opr.clear_loc', text='Reset')

                    if context.object.type == 'MESH':
                        col = spl.column()
                        col.operator('opr.apply_loc', text='Apply')

                    box = layout.box()
                    col = box.column()
                    col.prop(context.object, 'rotation_euler')

                    col = box.column()
                    spl = col.split(0.5)
                    col = spl.column()
                    col.operator('opr.clear_rot', text='Reset')

                    if context.object.type == 'MESH':
                        col = spl.column()
                        col.operator('opr.apply_rot', text='Apply')

                    box = layout.box()
                    col = box.column()
                    col.label(text='Delta Scale:')
                    col.prop(obj, 'delta_scale_xyz')
                    col = box.column()
                    col.prop(context.object, 'scale')

                    col = box.column()
                    spl = col.split(0.5)
                    col = spl.column()
                    col.operator('opr.clear_scl', text='Reset')

                    if context.object.type == 'MESH':
                        col = spl.column()
                        col.operator('opr.apply_scl', text='Apply')


def register():
    bpy.utils.register_class(OrbitUpView)
    bpy.utils.register_class(OrbitLeftView)
    bpy.utils.register_class(OrbitRightView)
    bpy.utils.register_class(OrbitDownView)
    bpy.utils.register_class(PanUpView)
    bpy.utils.register_class(PanLeftView)
    bpy.utils.register_class(PanRightView)
    bpy.utils.register_class(PanDownView)
    bpy.utils.register_class(ZoomInView)
    bpy.utils.register_class(ZoomOutView)
    bpy.utils.register_class(RollLeftView)
    bpy.utils.register_class(RollRightView)
    bpy.utils.register_class(LeftViewpoint)
    bpy.utils.register_class(RightViewpoint)
    bpy.utils.register_class(FrontViewpoint)
    bpy.utils.register_class(BackViewpoint)
    bpy.utils.register_class(TopViewpoint)
    bpy.utils.register_class(BottomViewpoint)
    bpy.utils.register_class(ShowHideObject)
    bpy.utils.register_class(ShowAllObjects)
    bpy.utils.register_class(HideAllObjects)
    bpy.utils.register_class(SelectAll)
    bpy.utils.register_class(InverseSelection)
    bpy.utils.register_class(LoopMultiSelect)
    bpy.utils.register_class(DeleteVerts)
    bpy.utils.register_class(DeleteEdges)
    bpy.utils.register_class(DeleteFaces)
    bpy.utils.register_class(DeleteOnlyFaces)
    bpy.utils.register_class(DeleteOnlyEdgesFaces)
    bpy.utils.register_class(ImportPlyObject)
    bpy.utils.register_class(ImportStlObject)
    bpy.utils.register_class(EnterEditMode)
    bpy.utils.register_class(EnterObjectMode)
    bpy.utils.register_class(FixOrigin)
    bpy.utils.register_class(AddDecimateModifier)
    bpy.utils.register_class(MoveUpDecimateModifier)
    bpy.utils.register_class(MoveDownDecimateModifier)
    bpy.utils.register_class(RemoveDecimateModifier)
    bpy.utils.register_class(ApplyDecimateModifier)
    bpy.utils.register_class(AddSmoothModifier)
    bpy.utils.register_class(MoveUpSmoothModifier)
    bpy.utils.register_class(MoveDownSmoothModifier)
    bpy.utils.register_class(RemoveSmoothModifier)
    bpy.utils.register_class(ApplyAsShapeSmoothModifier)
    bpy.utils.register_class(ApplySmoothModifier)
    bpy.utils.register_class(TrimExpand)
    bpy.utils.register_class(SaveTrimmed)
    bpy.utils.register_class(TrimObject)
    bpy.utils.register_class(IntersectExpand)
    bpy.utils.register_class(ShowPrevIntersection)
    bpy.utils.register_class(ShowNextIntersection)
    bpy.utils.register_class(SaveIntersection)
    bpy.utils.register_class(IntersectObject)
    bpy.utils.register_class(DissectExpand)
    bpy.utils.register_class(ShowPrevDissection)
    bpy.utils.register_class(ShowNextDissection)
    bpy.utils.register_class(DissectObject)
    bpy.utils.register_class(ClearLoc)
    bpy.utils.register_class(ApplyLoc)
    bpy.utils.register_class(ClearRot)
    bpy.utils.register_class(ApplyRot)
    bpy.utils.register_class(ClearScl)
    bpy.utils.register_class(ApplyScl)
    bpy.utils.register_class(Navigation)
    bpy.utils.register_class(Selection)
    bpy.utils.register_class(Tools)
    bpy.utils.register_class(Transform)


def unregister():
    bpy.utils.unregister_class(OrbitUpView)
    bpy.utils.unregister_class(OrbitLeftView)
    bpy.utils.unregister_class(OrbitRightView)
    bpy.utils.unregister_class(OrbitDownView)
    bpy.utils.unregister_class(PanUpView)
    bpy.utils.unregister_class(PanLeftView)
    bpy.utils.unregister_class(PanRightView)
    bpy.utils.unregister_class(PanDownView)
    bpy.utils.unregister_class(ZoomInView)
    bpy.utils.unregister_class(ZoomOutView)
    bpy.utils.unregister_class(RollLeftView)
    bpy.utils.unregister_class(RollRightView)
    bpy.utils.unregister_class(LeftViewpoint)
    bpy.utils.unregister_class(RightViewpoint)
    bpy.utils.unregister_class(FrontViewpoint)
    bpy.utils.unregister_class(BackViewpoint)
    bpy.utils.unregister_class(TopViewpoint)
    bpy.utils.unregister_class(BottomViewpoint)
    bpy.utils.unregister_class(ShowHideObject)
    bpy.utils.unregister_class(ShowAllObjects)
    bpy.utils.unregister_class(HideAllObjects)
    bpy.utils.unregister_class(SelectAll)
    bpy.utils.unregister_class(InverseSelection)
    bpy.utils.unregister_class(LoopMultiSelect)
    bpy.utils.unregister_class(DeleteVerts)
    bpy.utils.unregister_class(DeleteEdges)
    bpy.utils.unregister_class(DeleteFaces)
    bpy.utils.unregister_class(DeleteOnlyFaces)
    bpy.utils.unregister_class(DeleteOnlyEdgesFaces)
    bpy.utils.unregister_class(ImportPlyObject)
    bpy.utils.unregister_class(ImportStlObject)
    bpy.utils.unregister_class(EnterEditMode)
    bpy.utils.unregister_class(EnterObjectMode)
    bpy.utils.unregister_class(FixOrigin)
    bpy.utils.unregister_class(AddDecimateModifier)
    bpy.utils.unregister_class(MoveUpDecimateModifier)
    bpy.utils.unregister_class(MoveDownDecimateModifier)
    bpy.utils.unregister_class(RemoveDecimateModifier)
    bpy.utils.unregister_class(ApplyDecimateModifier)
    bpy.utils.unregister_class(AddSmoothModifier)
    bpy.utils.unregister_class(MoveUpSmoothModifier)
    bpy.utils.unregister_class(MoveDownSmoothModifier)
    bpy.utils.unregister_class(RemoveSmoothModifier)
    bpy.utils.unregister_class(ApplyAsShapeSmoothModifier)
    bpy.utils.unregister_class(ApplySmoothModifier)
    bpy.utils.unregister_class(TrimExpand)
    bpy.utils.unregister_class(SaveTrimmed)
    bpy.utils.unregister_class(TrimObject)
    bpy.utils.unregister_class(IntersectExpand)
    bpy.utils.unregister_class(ShowPrevIntersection)
    bpy.utils.unregister_class(ShowNextIntersection)
    bpy.utils.unregister_class(SaveIntersection)
    bpy.utils.unregister_class(IntersectObject)
    bpy.utils.unregister_class(DissectExpand)
    bpy.utils.unregister_class(ShowPrevDissection)
    bpy.utils.unregister_class(ShowNextDissection)
    bpy.utils.unregister_class(DissectObject)
    bpy.utils.unregister_class(ClearLoc)
    bpy.utils.unregister_class(ApplyLoc)
    bpy.utils.unregister_class(ClearRot)
    bpy.utils.unregister_class(ApplyRot)
    bpy.utils.unregister_class(ClearScl)
    bpy.utils.unregister_class(ApplyScl)
    bpy.utils.unregister_class(Navigation)
    bpy.utils.unregister_class(Selection)
    bpy.utils.unregister_class(Tools)
    bpy.utils.unregister_class(Transform)

if __name__ == '__main__':
    register()
