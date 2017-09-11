#
# Thanks to pitiwazou and meta-androcto's pie menu plugin, which helped me
# structure this!
#


import bpy
from bpy.types import Menu

class SculptMaskClear(bpy.types.Operator):
    '''Clears the current mask.'''
    bl_idname = "sculpt.mask_clear"
    bl_label = "Clear Mask"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        return {'FINISHED'}

class SculptMaskInvert(bpy.types.Operator):
    '''Clears the current mask.'''
    bl_idname = "sculpt.mask_invert"
    bl_label = "Clear Mask"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.paint.mask_flood_fill(mode='INVERT')
        return {'FINISHED'}

class SculptMaskHide(bpy.types.Operator):
    '''Hides parts of the mesh with a mask.'''
    bl_idname = "sculpt.mask_hide"
    bl_label = "Hide Mask"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        return {'FINISHED'}

class SculptMaskShow(bpy.types.Operator):
    '''Hides parts of the mesh with a mask.'''
    bl_idname = "sculpt.mask_show"
    bl_label = "Hide Mask"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        return {'FINISHED'}

class SculptMaskLasso(bpy.types.Operator):
    '''Hides parts of the mesh with a mask.'''
    bl_idname = "sculpt.mask_lasso"
    bl_label = "Hide Mask"
    bl_options = {'REGISTER', 'UNDO'}


class PieSculptMaskSelect(Menu):
    bl_idname = "pie.maskfromgroup"
    bl_label = "Select Mask"

    def draw(self, context):
        print("Drawing Pie")
        layout = self.layout
        pie = layout.menu_pie()

        ob = context.object
        group = ob.vertex_groups.active
        i = 0

        if ob:
            for group in ob.vertex_groups:
                if i > 7:
                    break
                pie.operator("mesh.vgrouptomask", text=group.name, icon="GROUP_VERTEX").index = i
                i += 1

class PieSculptMaskStandard(Menu):
    bl_idname = "pie.maskstandard"
    bl_label = "Mask Tools"

    def draw(self, context):
        print("Drawing Pie")
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("sculpt.mask_clear", text="Clear Mask")
        # 6 - RIGHT
        pie.operator("sculpt.mask_invert", text="Invert Mask")
        # 2 - BOTTOM
        pie.operator("sculpt.mask_hide", text="Hide Mask")
        # 8 - TOP
        pie.operator("sculpt.mask_show", text="Show All")
        # 7 - TOP - LEFT
        pie.operator("view3d.select_border", text="Box Mask", icon="BORDER_RECT")
        # 1 - BOTTOM - LEFT
        pie.operator("mesh.masktovgroup", text="Create Group from Mask", icon="GROUP_VERTEX")
        # 9 - TOP - RIGHT
        pie.operator("paint.mask_lasso_gesture", text="Lasso Mask", icon="BORDER_LASSO")
        # 3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text="Replace Mask with Group", icon="MOD_MASK").name = "pie.maskfromgroup"
