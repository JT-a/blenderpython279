'''
BEGIN GPL LICENSE BLOCK

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

END GPL LICENSE BLOCK

#============================================================================

tp_arch_tool_v000.py  (Three Point Arch Tool)

Install instructions:
1) Save the tp_arch_tool_v000.py file to your computer.
2) In Blender, go to File > User Preferences > Add-ons
3) Press Install From File and select the tp_arch_tool_v000.py file you
    just downloaded.
4) Enable the Add-On by clicking on the box to the left of Add-On's name

#============================================================================

Stage 0 = Add-on just launched, no points placed
Stage 1 = 1st point placed
Stage 2 = 2nd point placed (1st to 2nd point is arc width)
Stage 3 = 3rd point placed (to create planar surface to align arc to)
Stage 4 = 1st arch edge created
Stage 5 = Make faces from 1st arch (with extrude > scale)
Stage 6 = Make arch faces into solid (by extruding faces from Stage 5)
Stage 7 = Exit add-on

Extras
* Option to change edges on arch (pause with space to break modal?)
* Option to manually set distance between arch edges (spacebar pause menu?)
* Option to "roll back" arch distance?
* Option to add "base/support wall" before creating arch?
* Option to change arch types (circular, equilateral, parabolic, etc)
* Use curves instead of vertex plotting?
'''

bl_info = {
    "name": "Three Point Arch Tool",
    "author": "nBurn",
    "version": (0, 0, 0),
    "blender": (2, 7, 7),
    "location": "View3D",
    "description": "Tool for creating arches",
    "category": "Mesh"
}

import bpy
import bmesh
import bgl
import blf

from copy import deepcopy
from math import pi, sqrt, degrees, radians, sin, cos
from mathutils import geometry, Euler, Quaternion, Vector
from mathutils.geometry import intersect_line_line_2d
from bpy_extras import view3d_utils
#from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy_extras.view3d_utils import location_3d_to_region_2d as loc_3d_to_2d

#print("\n\n  Loaded: Arc Tool\n")  # debug

(
    X,
    Y,
    Z,
    XO_SLOW3DTO2D,
    XO_GRABONLY,
) = range(5)

reg_rv3d = ()
pt_store = ()


def getreg_rv3d():
    global reg_rv3d
    region = bpy.context.region
    rv3d = bpy.context.region_data
    reg_rv3d = (region, rv3d)


class Colr:
    red   = 1.0, 0.0, 0.0, 0.5
    green = 0.0, 1.0, 0.0, 0.5
    blue  = 0.0, 0.0, 1.0, 0.5
    white = 1.0, 1.0, 1.0, 1.0
    grey  = 1.0, 1.0, 1.0, 0.4


class RotationData:
    def __init__( self, ax=None, piv_norm=() ):
        self.axis_lk = ax
        self.piv_norm = piv_norm


def backup_snap_settings():
    backup = [
        deepcopy(bpy.context.tool_settings.use_snap),
        deepcopy(bpy.context.tool_settings.snap_element),
        deepcopy(bpy.context.tool_settings.snap_target)]
    return backup


def restore_snap_settings(backup):
    bpy.context.tool_settings.use_snap = deepcopy(backup[0])
    bpy.context.tool_settings.snap_element = deepcopy(backup[1])
    bpy.context.tool_settings.snap_target = deepcopy(backup[2])
    return


def get_rotated_pt(piv_co, mov_co, ang_diff_rad, rot_dat):
    axis_lk = ''
    #axis_lk = rot_dat.axis_lk
    mov_aligned = mov_co - piv_co
    rot_val = []
    if   axis_lk == '':  # arbitrary axis / spherical rotations
        rot_val = Quaternion(rot_dat.piv_norm, ang_diff_rad)
    elif axis_lk == 'X':
        rot_val = Euler((ang_diff_rad, 0.0, 0.0), 'XYZ')
    elif axis_lk == 'Y':
        rot_val = Euler((0.0, ang_diff_rad, 0.0), 'XYZ')
    elif axis_lk == 'Z':
        rot_val = Euler((0.0, 0.0, ang_diff_rad), 'XYZ')
    mov_aligned.rotate(rot_val)
    return mov_aligned + piv_co


def draw_pt_2D(pt_co, pt_color):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glPointSize(10)
    bgl.glColor4f(*pt_color)
    bgl.glBegin(bgl.GL_POINTS)
    bgl.glVertex2f(*pt_co)
    bgl.glEnd()
    return


def draw_line_2D(pt_co_1, pt_co_2, pt_color):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glPointSize(7)
    bgl.glColor4f(*pt_color)
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex2f(*pt_co_1)
    bgl.glVertex2f(*pt_co_2)
    bgl.glEnd()
    return


def draw_circ_seg_3D(steps, pts, orig, ang_meas, rot_dat, pt_color):
    global reg_rv3d
    orig2d = loc_3d_to_2d(reg_rv3d[0], reg_rv3d[1], orig)
    # todo figure out why above sometimes returns None in Perspective mode...
    # returns None when 3d point is not inside active 3D View
    if orig2d is not None:
        draw_pt_2D(orig2d, Colr.white)
    rad_incr = abs(ang_meas / steps)
    bgl.glColor4f(*pt_color)
    bgl.glBegin(bgl.GL_LINE_STRIP)
    curr_ang = 0.0
    while curr_ang <= ang_meas:
        new_pt = get_rotated_pt(orig, pts[0], curr_ang, rot_dat)
        new_pt2d = loc_3d_to_2d(reg_rv3d[0], reg_rv3d[1], new_pt)
        if new_pt2d is not None:
            bgl.glVertex2f(new_pt2d[X], new_pt2d[Y])
        curr_ang = curr_ang + rad_incr
    new_pt2d = loc_3d_to_2d(reg_rv3d[0], reg_rv3d[1], pts[1])
    if new_pt2d is not None:
        bgl.glVertex2f(new_pt2d[X], new_pt2d[Y])
    bgl.glEnd()
    return


# Refreshes mesh drawing in 3D view and updates mesh coordinate
# data so ref_pts are drawn at correct locations.
# Using editmode_toggle to do this seems hackish, but editmode_toggle seems
# to be the only thing that updates both drawing and coordinate info.
def editmode_refresh(ed_type):
    if ed_type == "EDIT_MESH":
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()


# === PointFind code ===


def create_snap_pt(msLoc, EdType):
    global reg_rv3d, pt_store
    #sel_backup.update(EdType)
    region, rv3d = reg_rv3d[0], reg_rv3d[1]
    v_u = view3d_utils  # shorthand
    perspMdFix = v_u.region_2d_to_vector_3d(region, rv3d, msLoc) / 5
    enterloc = v_u.region_2d_to_origin_3d(region, rv3d, msLoc) + perspMdFix
    if EdType == 'OBJECT':
        bpy.ops.object.add(type = 'MESH', location = enterloc)
        pt_store = bpy.context.object
    # todo : move below to backup_snap_settings ?
    bpy.context.tool_settings.use_snap = False
    bpy.context.tool_settings.snap_element = 'VERTEX'
    #bpy.context.tool_settings.snap_target = 'ACTIVE'
    bpy.ops.transform.translate('INVOKE_DEFAULT')


# Makes sure only the "guide point" object or vert
# added with create_snap_pt is grabbed.
def grab_snap_pt(ms_loc, ed_type, sel_backup):
    global reg_rv3d, pt_store
    #sel_backup.update(ed_type)
    region, rv3d = reg_rv3d[0], reg_rv3d[1]
    v_u = view3d_utils  # shorthand
    persp_md_fix = v_u.region_2d_to_vector_3d(region, rv3d, ms_loc) / 5
    enterloc = v_u.region_2d_to_origin_3d(region, rv3d, ms_loc) + persp_md_fix
    #if ed_type == 'OBJECT':
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects[0].select = True
    #    #bpy.context.scene.objects[0].location = enterloc
    '''
    elif ed_type == 'EDIT_MESH':
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
        bm.verts[-1].select = True
        inver_mw = bpy.context.edit_object.matrix_world.inverted()
        local_co = inver_mw * enterloc
        #bm.verts[-1].co = local_co
        editmode_refresh(ed_type)
    '''
    bpy.ops.transform.translate('INVOKE_DEFAULT')


# Makes sure only the "guide point" object or vert
# added with create_snap_pt is deleted.
def remove_snap_pt(ed_type, sel_backup):
    if ed_type == 'OBJECT':
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects[0].select = True
        bpy.ops.object.delete()
    elif ed_type == 'EDIT_MESH':
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
        bm.verts[-1].select = True
        editmode_refresh(ed_type)
        bpy.ops.mesh.delete(type='VERT')
    #sel_backup.restore_selected(ed_type)
    #print("removsadf")


def step_decrm(self):
    if self.step_cnt > 2:
        self.step_cnt -= 1


def exit_addon(self):
    if self.pt_cnt < 5:
        remove_snap_pt(self.curr_ed_type, self.sel_backup)
    '''
    #if self.pt_find_md == XO_GRABONLY:
        remove_snap_pt(self.curr_ed_type, self.sel_backup)
        self.pt_find_md = XO_SLOW3DTO2D
        if self.curr_ed_type == 'EDIT_MESH':
            for i in self.sel_backup.sel_msh_objs:
                self.sel_backup.obj[i].select = True
    for i in self.sel_backup.sel_nm_objs:
        self.sel_backup.obj[i].select = True
    '''
    if self.curr_ed_type == 'EDIT_MESH':
        bpy.ops.object.editmode_toggle()
    restore_snap_settings(self.settings_backup)
    #print("\n\n\n  Add-On Exited!\n")  # debug


def draw_callback_px(self, context):
    getreg_rv3d()
    stp_cnt = self.step_cnt
    global pt_store, reg_rv3d
    if self.left_click:
        self.left_click = False
        t_loc = None
        if self.pt_cnt < 3:
            t_loc = pt_store.location.copy()
            if t_loc != None:
                dup = False
                for i in self.pts:
                    if t_loc == i:
                        dup = True
                if dup == False:
                    self.pts.append( t_loc.copy() )
                    self.pt_cnt += 1
            if self.pt_cnt < 2:    
                bpy.ops.transform.translate('INVOKE_DEFAULT')
            elif self.pt_cnt == 2:
                # move snap point to arch center before turning grab mode back on
                bpy.context.scene.objects[0].location = self.pts[0].lerp(self.pts[1], 0.5)
                bpy.ops.transform.translate('INVOKE_DEFAULT')
        elif self.pt_cnt == 3 and self.buff != None:
            self.pt_cnt += 1
            bpy.context.scene.objects[0].location = self.buff[2].copy()
            #if self.curr_ed_type != 'EDIT_MESH':
            #    bpy.ops.object.editmode_toggle()
            bpy.ops.object.editmode_toggle()
            inv_mw = bpy.context.scene.objects[0].matrix_world.inverted()
            piv_cent = inv_mw * self.buff[2]
            bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
            bm.verts.new( inv_mw * self.buff[1][0] )
            # Spin and deal with geometry on side 'a'
            edges_start_a = bm.edges[:]
            geom_start_a = bm.verts[:] + edges_start_a
            ret = bmesh.ops.spin(
                bm,
                geom=geom_start_a,
                angle=self.buff[3],
                steps=stp_cnt,
                axis=self.rdat.piv_norm,
                cent=piv_cent)
            edges_end_a = [ele for ele in ret["geom_last"]
                    if isinstance(ele, bmesh.types.BMEdge)]
            del ret

            bpy.context.scene.cursor_location = self.buff[2].copy()
            bpy.context.tool_settings.snap_target = 'ACTIVE'
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.context.space_data.transform_orientation = 'GLOBAL'
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.extrude_region_move()
            bpy.ops.transform.resize('INVOKE_DEFAULT', constraint_orientation = 'GLOBAL')
        elif self.pt_cnt == 4:
            self.pt_cnt += 1
            if self.buff != None:
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.view3d.edit_mesh_extrude_move_normal('INVOKE_DEFAULT')
            self.exitCheck = True
    #print("self.pt_cnt", self.pt_cnt)  # debug


    # Draw UI: setup 2d data for drawing on screen
    pts2d, pts_str2d = [], []
    if self.pt_cnt > 0:
        pts2d = [loc_3d_to_2d(reg_rv3d[0], reg_rv3d[1], i) for i in self.pts]
        pts_str2d = loc_3d_to_2d(reg_rv3d[0], reg_rv3d[1], pt_store.location)
    
    if self.pt_cnt == 1:
        draw_line_2D(pts2d[0], pts_str2d, Colr.white)
        
    elif self.pt_cnt == 2:
        cent = self.pts[0].lerp(self.pts[1], 0.5)
        self.rdat.piv_norm = geometry.normal(self.pts[0], cent, pt_store.location)
        pivNorm = self.rdat.piv_norm.copy()
        movAligned = self.pts[0] - cent
        rot_pos, rot_neg = movAligned.copy(), movAligned.copy()
        hgt = (pt_store.location - cent).length
        wid = (self.pts[0] - self.pts[1]).length
        rad = None
        if hgt != 0:
            rad = (hgt / 2) + (wid * wid) / (8 * hgt)
        else:
            rad = 0
        cen_to_piv = rad - hgt
        # find points perp to starting two
        rot_pos.rotate( Quaternion(pivNorm, radians(90)) )
        rot_neg.rotate( Quaternion(pivNorm,-radians(90)) )
        rot_pos = rot_pos + cent
        rot_neg = rot_neg + cent
        old_dis = wid / 2
        scale = cen_to_piv / old_dis
        circ_cen_p = cent.lerp(rot_pos, scale)
        circ_cen_n = cent.lerp(rot_neg, scale)

        # workaround to avoid division by zero
        algnAco = self.pts[0] - circ_cen_p
        algnCco = self.pts[1] - circ_cen_p
        ang_meas = algnAco.angle(algnCco)
        if ang_meas == 0.0:
            self.buff = None
            draw_line_2D(pts2d[0], pts2d[1], Colr.white)
            return
        
        if rad > wid/2 and hgt > rad:
            ang_meas = 2 * pi - ang_meas

        rot_pos_2d = loc_3d_to_2d(reg_rv3d[0], reg_rv3d[1], rot_pos)
        rot_neg_2d = loc_3d_to_2d(reg_rv3d[0], reg_rv3d[1], rot_neg)
        
        msToPtP_dis = (rot_pos_2d - pts_str2d).length
        msToPtN_dis = (rot_neg_2d - pts_str2d).length
        
        if   msToPtP_dis > msToPtN_dis:  # closer to negative
            new_pts = self.pts[1], self.pts[0]
            draw_circ_seg_3D(stp_cnt, new_pts, circ_cen_p, ang_meas, self.rdat, Colr.green)
            self.buff = 'neg', new_pts, circ_cen_p, ang_meas
        elif msToPtP_dis < msToPtN_dis:  # closer to positive
            draw_circ_seg_3D(stp_cnt, self.pts, circ_cen_n, ang_meas, self.rdat, Colr.green)
            self.buff = 'pos', self.pts, circ_cen_n, ang_meas

    elif self.pt_cnt == 3:
        if self.buff == None:
            pts2d = [loc_3d_to_2d(reg_rv3d[0], reg_rv3d[1], i) for i in self.pts]
            draw_line_2D(pts2d[0], pts2d[1], Colr.white)
        else:
            draw_circ_seg_3D(stp_cnt, self.buff[1], self.buff[2], self.buff[3], self.rdat, Colr.green)

    for i in pts2d:
        draw_pt_2D(i, Colr.white)


class ModalArchTool(bpy.types.Operator):
    '''Draw a line with the mouse'''
    bl_idname = "view3d.modal_arch_tool"
    bl_label = "Three Point Arch Tool"

    # Only launch Add-On from OBJECT or EDIT modes
    @classmethod
    def poll(self, context):
        return context.mode == 'OBJECT' or context.mode == 'EDIT_MESH'

    def modal(self, context, event):
        context.area.tag_redraw()
        self.curr_ed_type = context.mode

        if event.type in {'MIDDLEMOUSE', 'NUMPAD_1', 'NUMPAD_2', 'NUMPAD_3',
        'NUMPAD_4', 'NUMPAD_6', 'NUMPAD_7', 'NUMPAD_8', 'NUMPAD_9', 'NUMPAD_5'}:
            return {'PASS_THROUGH'}

        if event.type == 'MOUSEMOVE':
            self.mouse_loc = Vector((event.mouse_region_x, event.mouse_region_y))

        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            self.left_click = True
            self.left_click_loc = Vector((event.mouse_region_x, event.mouse_region_y))

        if event.type == 'SPACE' and event.value == 'RELEASE':
            self.left_click = True
            self.left_click_loc = Vector((event.mouse_region_x, event.mouse_region_y))

        if self.pt_cnt == 3:
            if event.type == 'WHEELUPMOUSE':
                self.step_cnt += 1

            if event.type == 'WHEELDOWNMOUSE':
                step_decrm(self)

            if event.type == 'UP_ARROW' and event.value == 'RELEASE':
                self.step_cnt += 1

            if event.type == 'DOWN_ARROW' and event.value == 'RELEASE':
                step_decrm(self)

        #if event.type == 'D' and event.value == 'RELEASE':
        #    # call debugger
        #    __import__('code').interact(local=dict(globals(), **locals()))

        if event.type in {'ESC', 'RIGHTMOUSE'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            exit_addon(self)
            return {'CANCELLED'}

        if self.exitCheck:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            exit_addon(self)
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = (self, context)

            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px,
                    args, 'WINDOW', 'POST_PIXEL')

            if context.mode == 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
            bpy.ops.object.select_all(action='DESELECT')
            
            self.curr_ed_type = context.mode  # current Blender Editor Type
            self.mouse_loc = Vector((event.mouse_region_x, event.mouse_region_y))
            self.left_click_loc = []
            self.left_click = False
            self.rdat = RotationData('')
            self.step_cnt = 8
            self.pt_cnt = 0
            self.pts = []
            self.buff = None
            self.settings_backup = backup_snap_settings()
            self.sel_backup = None  # place holder
            self.exitCheck = False

            context.window_manager.modal_handler_add(self)
            
            getreg_rv3d()
            create_snap_pt(self.mouse_loc, self.curr_ed_type)
            #print("Add-on started!")

            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalArchTool)

def unregister():
    bpy.utils.unregister_class(ModalArchTool)

if __name__ == "__main__":
    register()
