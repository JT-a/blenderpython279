"""
未使用
"""

import ctypes as ct

import bpy

from ..utils import structures


RGN_TYPE_WINDOW = 0
RGN_TYPE_HEADER = 1
RGN_TYPE_CHANNELS = 2
RGN_TYPE_TEMPORARY = 3
RGN_TYPE_UI = 4
RGN_TYPE_TOOLS = 5
RGN_TYPE_TOOL_PROPS = 6
RGN_TYPE_PREVIEW = 7

# DNA_space_types.h: 210: enum eSpaceButtons_Align
BUT_FREE = 0
BUT_HORIZONTAL = 1
BUT_VERTICAL = 2
BUT_AUTO = 3

# DNA_space_types.h: 1350: enum eSpace_Type
SPACE_BUTS = 4
SPACE_FILE = 5
SPACE_IMAGE = 6
SPACE_USERPREF = 19


def panel_aligned(area, region):
    sa = structures.ScrArea.cast(area)
    ar = structures.ARegion.cast(region)

    if sa.spacetype == SPACE_BUTS and ar.regiontype == RGN_TYPE_WINDOW:
        sbuts = structures.SpaceButs.cast(sa.spacedata.first)
        return sbuts.align
    elif sa.spacetype == SPACE_USERPREF and ar.regiontype == RGN_TYPE_WINDOW:
        return BUT_VERTICAL
    elif sa.spacetype == SPACE_FILE and ar.regiontype == RGN_TYPE_CHANNELS:
        return BUT_VERTICAL
    elif sa.spacetype == SPACE_IMAGE and ar.regiontype == RGN_TYPE_PREVIEW:
        return BUT_VERTICAL
    elif ar.regiontype in {RGN_TYPE_UI, RGN_TYPE_TOOLS, RGN_TYPE_TOOL_PROPS}:
        return BUT_VERTICAL

    return 0


def toggle_panel_close(area, region, idname):
    """ui_handler_panel_region()を参考にする"""
    PNL_NO_HEADER = 2

    PNL_CLOSEDX = 1 << 1
    PNL_CLOSEDY = 1 << 2
    PNL_CLOSED = PNL_CLOSEDX | PNL_CLOSEDY

    PNL_SNAP_BOTTOM = 4

    align = panel_aligned(area, region)

    ar = structures.ARegion.cast(region)

    for block in ar.uiblocks.to_list(structures.uiBlock):
        pa_p = block.panel
        if not pa_p:
            continue
        pa = pa_p.contents
        if pa.paneltab:
            continue
        if pa.type and pa.type.contents.flag & PNL_NO_HEADER:
            continue

        # print(pa.panelname, pa.type.contents.idname)
        # if pa.panelname != idname.encode('utf-8'):
        #     continue
        if pa.type.contents.idname != idname.encode('utf-8'):
            continue

        if pa.flag & PNL_CLOSED:
            pa.flag = (pa.flag | PNL_CLOSED) ^ PNL_CLOSED
            if pa.snap & PNL_SNAP_BOTTOM:
                pa.ofsy = 0
        elif align == BUT_HORIZONTAL:
            pa.flag |= PNL_CLOSEDX
        else:
            pa.flag |= PNL_CLOSEDY
            if pa.snap & PNL_SNAP_BOTTOM:
                pa.ofsy = -pa.sizey

        pa.flag = (pa.flag | 1) ^ 1

        for pa_ in ar.panels.to_list(structures.Panel):
            if ct.addressof(pa_.paneltab) == ct.addressof(pa):
                if pa.flag & PNL_CLOSED:
                    pa_.flag |= PNL_CLOSED
                else:
                    pa_.flag = (pa_.flag | PNL_CLOSED) ^ PNL_CLOSED

    region.tag_redraw()


class TogglePanelClose(bpy.types.Operator):
    bl_idname = 'screen.toggle_panel_close'
    bl_label = 'Toggle Panel Close'
    bl_options = {'REGISTER'}

    idname = bpy.props.StringProperty(
        name='ID Name',
        default='VIEW3D_PT_tools_transform',
    )
    region_type = bpy.props.EnumProperty(
        name='Region Type',
        items=(('TOOLS', 'Tools', ''),
               ('UI', 'UI', '')),
        default='TOOLS'
    )

    def modal(self, context, event):
        bpy.context.user_preferences.system.dpi += 1
        context.window_manager.event_timer_remove(self.timer)
        return {'FINISHED'}

    def invoke(self, context, event):
        area = context.area
        for region in area.regions:
            if region.type == self.region_type:
                break
        else:
            return {'CANCELLED'}
        toggle_panel_close(area, region, self.idname)
        # # UI_panel_category_active_set(bpy.context, region, 'ToolProps')
        # # context.area.tag_redraw()
        ctx = context.copy()
        ctx['area'] = area
        ctx['region'] = region
        # bpy.ops.view2d.zoom_in(ctx, 'INVOKE_DEFAULT')
        # bpy.ops.view2d.zoom_out(ctx, 'INVOKE_DEFAULT')

        bpy.context.user_preferences.system.dpi -= 1

        context.window_manager.modal_handler_add(self)
        self.timer = context.window_manager.event_timer_add(0.0, context.window)
        return {'RUNNING_MODAL'}