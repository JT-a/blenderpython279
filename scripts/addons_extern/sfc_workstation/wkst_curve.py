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


###########  Menu  #######################

class CurveSmooth(bpy.types.Menu):
    """Curve Smooth"""
    bl_label = "Curve Smooth"
    bl_idname = "wkst.curvesmooth"

    def draw(self, context):
        layout = self.layout

        layout.operator("curve.smooth")
        layout.operator("curve.smooth_weight")
        layout.operator("curve.smooth_radius")
        layout.operator("curve.smooth_tilt")

bpy.utils.register_class(CurveSmooth)


class WKST_SplineType_Menu(bpy.types.Menu):
    """Curve Spline Type"""
    bl_label = "Curve Spline Type Menu"
    bl_idname = "wkst.splinetype_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("curve.to_poly", "Poly")
        layout.operator("curve.to_bezier", "Bezièr")
        layout.operator("curve.to_nurbs", "Nurbs")

        layout.separator()

        layout.operator("curve.handle_to_free", "Free")
        layout.operator("curve.handle_to_automatic", "Auto")
        layout.operator("curve.handle_to_vector", "Vector")
        layout.operator("curve.handle_to_aligned", "Aligned")


class WKST_CurveEdit_Menu(bpy.types.Menu):
    """Curve Edit"""
    bl_label = "Curve Edit Menu"
    bl_idname = "wkst.curve_edit_menu"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.object.data, "dimensions", "")

        layout.separator()

        if context.mode == 'OBJECT':
            layout.operator("curve.smoothspline", "Smooth", icon="SMOOTHCURVE")

            layout.separator()

            layout.operator("curve.switch_direction_obm", "Direction", icon="ARROW_LEFTRIGHT")
            layout.operator("curve.open_circle", text="Open / Close", icon="MOD_CURVE")

        else:
            layout.operator("curve.smooth", "Smooth", icon="SMOOTHCURVE")

            layout.operator("curve.normals_make_consistent", icon="SNAP_NORMAL")

            layout.separator()

            layout.operator("curve.switch_direction", text="Direction", icon="ARROW_LEFTRIGHT")
            layout.operator("curve.cyclic_toggle", text="Open / Close", icon="MOD_CURVE")

        if context.mode == 'OBJECT':
            layout.separator()

            layout.operator("curve.simplify", "Simplify", icon="IPO_EASE_IN_OUT")


class WKST_CT2D_Menu(bpy.types.Menu):
    """Curve Tools2 Delete"""
    bl_label = "Curve Tools2 Delete Menu"
    bl_idname = "wkst.ct2d_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("curvetools2.operatorsplinesjoinneighbouring", text="Join")
        layout.operator("curvetools2.operatorsplinesremoveshort", text="Remove Short")
        layout.operator("curvetools2.operatorsplinesremovezerosegment", text="Remove Zero")


class WKST_CT2_Menu(bpy.types.Menu):
    """Curve Tools2"""
    bl_label = "Curve Tools2 Menu"
    bl_idname = "wkst.ct2_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("curvetools2.operatorloftcurves", text="Loft")
        layout.operator("curvetools2.operatorsweepcurves", text="Sweep")

        layout.separator()

        layout.operator("curvetools2.operatorrevolvecurves", text="Revolver")
        layout.prop(context.scene.curvetools, "AngularResolution", text="Result")

        layout.separator()

        layout.operator("curvetools2.operatorbirail", text="Birail")
        layout.operator("curvetools2.operatorsweepandmorph", text="Morph")


class WKST_MiraExtrude_Menu(bpy.types.Menu):
    """Tools to create new Mesh"""
    bl_label = "Mira Extrude Menu"
    bl_idname = "wkst.miraextrude_menu"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_MESH'))

    def draw(self, context):
        layout = self.layout

        layout.operator("mira.poly_loop", text="Poly Loop", icon="MESH_GRID")
        layout.operator("mesh.retopomt", text="Retopo MT", icon="ORTHO")
        layout.separator()

        layout.operator("mira.curve_surfaces", text="Curve Surfaces", icon="SURFACE_NCURVE")
        layout.prop(context.scene.mi_cur_surfs_settings, "spread_loops_type", text='')

        layout.separator()

        layout.operator("mira.draw_extrude", text="Draw Extrude", icon="FORCE_MAGNETIC")

        layout.prop(context.scene.mi_extrude_settings, "extrude_step_type", text='')

        layout.separator()
        if context.scene.mi_extrude_settings.extrude_step_type == 'Asolute':
            layout.prop(context.scene.mi_extrude_settings, "absolute_extrude_step", text='')
        else:
            layout.prop(context.scene.mi_extrude_settings, "relative_extrude_step", text='')

        layout.separator()
        if context.scene.mi_settings.surface_snap is False:
            layout.prop(context.scene.mi_extrude_settings, "do_symmetry", text='Symmetry')

            if context.scene.mi_extrude_settings.do_symmetry:
                layout.prop(context.scene.mi_extrude_settings, "symmetry_axys", text='')


class WKST_MiraDeform_Menu(bpy.types.Menu):
    """Tools to Deform selected Mesh"""
    bl_label = "MiraDeform Menu"
    bl_idname = "wkst.miradeform_menu"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_MESH'))

    def draw(self, context):
        layout = self.layout

        layout.operator("mira.linear_deformer", text="Linear Deformer", icon="OUTLINER_OB_MESH")
        layout.prop(context.scene.mi_ldeformer_settings, "manual_update", text='ManualUpdate')

        layout.separator()

        layout.operator("mira.noise", text="NoiseDeform")
        layout.operator("mira.deformer", text="Deformer")


class WKST_MiraCurve_Menu(bpy.types.Menu):
    """Constraint Curve Tools for selected Loops"""
    bl_label = "MiraCurve Menu"
    bl_idname = "wkst.miracurve_menu"

    @classmethod
    def poll(cls, context):
        return ((context.mode == 'EDIT_MESH'))

    def draw(self, context):
        layout = self.layout

        layout.operator("mira.curve_stretch", text="Curve Stretch", icon="STYLUS_PRESSURE")
        layout.prop(context.scene.mi_cur_stretch_settings, "points_number", text='PointsNumber')

        layout.separator()

        layout.operator("mira.curve_guide", text="Curve Guide", icon="RNA")
        layout.prop(context.scene.mi_curguide_settings, "points_number", text='LoopSpread')
        layout.prop(context.scene.mi_curguide_settings, "deform_type", text='')


#######  Operators  ##################

class CurveToggle(bpy.types.Operator):
    """Make activ Curve closed or opened loop"""
    bl_idname = "curve.open_circle"
    bl_label = "Curve Cycle Toggle"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.curve.cyclic_toggle()
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


############  REGISTER  #################

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
