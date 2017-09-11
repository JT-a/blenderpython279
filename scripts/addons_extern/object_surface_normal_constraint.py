# Normal To Surface constraint
# Copyright (C) 2014  Stan Paillereau
# Modifications and fixes by italic
# ----------------------------------

'''
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
'''


bl_info = {
    "name": "Surface Normal Constraint",
    "author": "Stan Paillereau",
    "blender": (2, 7, 7),
    "version": (0, 0, 2),
    "location": "View3D > Tool panel > Create Normal To Constraint and View3D "
    "> UI panel > Custom Constraint",
    "description": "Add a normal to surface constraint to selected object",
    "category": "Object"
}

import bpy
import mathutils
import math
import bgl
from bpy.app.handlers import persistent


def createmeshlist(ob, context):
    '''create list of object of type 'MESH' to select in UI panel'''
    ob.meshlist.clear()
    for c in context.scene.objects:
        if c.type == 'MESH' and c != ob:
            ob.meshlist.add().name = c.name


def avail_meshs(self, context):
    '''create list of object of type 'MESH' to select when executing operator'''
    obj_active = context.active_object
    meshs = [
        (str(i), x.name, x.name)
        for i, x in enumerate(bpy.data.objects)
        if x.type == 'MESH' and x != obj_active
    ]
    return meshs


def RemoveCons(objs):
    '''remove custom properties and reset rotation'''
    for ob in objs:
        for p in ["flagEX", "meshlist", "flagIO", "infl", "consname", "meshname", "cvec"]:
            if ob.get(p) is not None:
                del ob[p]
        ob.delta_rotation_quaternion = mathutils.Quaternion((1.0, 0.0, 0.0, 0.0))
        ob.delta_rotation_euler = mathutils.Euler((0.0, 0.0, 0.0))
    return {'FINISHED'}


def draw_callback_px(self, context):
    oblist = [
        ob for ob in bpy.data.objects
        if ((ob.get('flagEX') is not None) or (ob.meshname != ""))
    ]
    for ob in oblist:
        vec = ob["cvec"]
        color = list(
            ((context.user_preferences.themes[0].view_3d.grid) / 4 +
             (context.user_preferences.themes[0].user_interface.axis_z) / 1.5)
        )
        color.append(1.0)

        bgl.glEnable(bgl.GL_LINE_STIPPLE)
        bgl.glColor4f(color[0], color[1], color[2], color[3])
        bgl.glLineWidth(1)

        bgl.glBegin(bgl.GL_LINES)
        bgl.glVertex3f(*ob.matrix_world.translation)
        bgl.glVertex3f(*vec)
        bgl.glEnd()

        # restore opengl defaults
        bgl.glLineWidth(1)
        bgl.glDisable(bgl.GL_LINE_STIPPLE)
        bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


@persistent
def DeclMesh(scene):
    '''declare variable mesh when loading file'''
    obj_active = bpy.context.active_object
    StoreGlobVar.mesh = bpy.data.objects.get(str(obj_active.meshname))
    return {'FINISHED'}


def FuncNormSurface(pvec, objName):
    '''caclulate the vector normal to the surface'''
    # set variables
    obj = bpy.data.objects[objName]
    faces = obj.data.polygons
    miniindv = [0]
    minidistv = [1000000.0]
    pvec_loc = pvec - obj.matrix_world.decompose()[0]

    # find closest point on mesh
    cveclist = obj.closest_point_on_mesh(pvec_loc, 1.84467e+19)
    cvec = obj.matrix_world * cveclist[1]
    nvecf = cveclist[2]
    f_ind = cveclist[3]
    f_loc = obj.matrix_world * faces[f_ind].center

    # set variables for the search of the closest
    # vertex to the object (not use yet)
    v_ind = faces[f_ind].vertices
    verts = obj.data.vertices

    # find the closest vertex (part of the closest face) to
    # the object and store in a list (not use yet)
    for v in range(0, faces[f_ind].loop_total):
        vloc = obj.matrix_world * verts[v_ind[v]].co
        dist = (cvec - vloc).length
        if dist < minidistv[0]:
            miniindv[0] = v_ind[v]
            minidistv[0] = dist

        else:
            miniindv[0] = miniindv[0]
            minidistv[0] = minidistv[0]

    # calculate the average normal (vector normal to
    # the surface) and return the result
    v_loc = obj.matrix_world * verts[miniindv[0]].co
    geom = mathutils.geometry.intersect_point_line(cvec, f_loc, v_loc)
    coef = geom[1]
    nvecv = verts[miniindv[0]].normal
    nvec = nvecf  # .lerp(nvecv,coef) to improve later
    result = [nvec, cvec]
    return (result)


@persistent
def NormalCons(scene):
    '''recalculate the normal when scene updates'''
    if (bpy.context.active_object) and \
            (bpy.context.active_object.get('flagEX') is not None):
        # set variables
        obj_active = bpy.context.active_object
        rot_mode = obj_active.rotation_mode
        pvec = obj_active.matrix_world.to_translation()
        createmeshlist(obj_active, bpy.context)

        mshlst = [str(l[0]) for l in obj_active.meshlist.items()]

        if (obj_active.meshname in mshlst) or (obj_active.meshname == ""):
            StoreGlobVar.mesh = bpy.data.objects.get(str(obj_active.meshname))
            target = obj_active.meshname
        else:
            obj_active.meshname = StoreGlobVar.mesh.name
            target = obj_active.meshname

        # set Track to and Up axis
        AXTT = obj_active.track_axis
        if AXTT[0] == 'N':
            AXTTN = '-' + AXTT[4]
        else:
            AXTTN = AXTT[4]
        AXUP = obj_active.up_axis

        # apply the rotation if there is no error on the constraint panel
        if (obj_active.track_axis[4] == obj_active.up_axis) or \
                (target == '') or \
                (obj_active.flagIO == False):
            error = 0.0
            nrot = mathutils.Quaternion((1.0, 0.0, 0.0, 0.0))
        else:
            # calculate the vector normal to the surface
            result = FuncNormSurface(pvec, target)
            nvec = result[0]
            obj_active["cvec"] = result[1]

            # calculate the rotation (and substract the
            # local rotation) to apply to the object
            obj_active.rotation_mode = 'QUATERNION'
            obj_rot = obj_active.rotation_quaternion
            nrot_quat = nvec.to_track_quat(AXTTN, AXUP)
            nrot = nrot_quat * obj_rot.inverted()

            # apply the rotation
            error = 1.0
            nrot = nrot.slerp(obj_rot, (1 - obj_active.infl * error))
        obj_active.delta_rotation_quaternion = nrot
        obj_active.delta_rotation_euler = nrot.to_euler(rot_mode)
        obj_active.rotation_mode = rot_mode


class StoreGlobVar:
    '''help store global variable'''
    pass


class CreateNormalToConsPanel(bpy.types.Panel):
    '''draw panel/buttons in the tool panel to add/remove the constraint'''
    bl_label = "Create Normal To Surface constraint"
    bl_idname = "create_normto_cons_pan"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "constraint"

    @classmethod
    def poll(cls, context):
        return (context.object)

    def draw(self, context):
        layout = self.layout
        layout.label("Add / Remove constraint:")

        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("object.add_cons", text="Add")
        row.operator("object.rem_cons", text="Remove")


class NormalToConsPanel(bpy.types.Panel):
    '''draw constraint UI panel'''
    bl_label = "Custom Constraints"
    bl_idname = "normto_cons_pan"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "constraint"

    @classmethod
    def poll(cls, context):
        '''poll to draw the panel'''
        obj_active = context.active_object
        return (obj_active.get('flagEX') is not None)

    def draw(self, context):
        # set variables
        layout = self.layout
        obj_active = context.active_object
        if obj_active.flagIO == True:  # icon for the enable/disable eye button
            con = 'VISIBLE_IPO_ON'
        else:
            con = 'VISIBLE_IPO_OFF'
        box = layout.box()
        row = box.row()

        # draw 1st row (Constraint name / enable/disable button / delete constraint button)
        row.label(text="Normal To")
        AXTT = obj_active.track_axis
        AXUP = obj_active.up_axis
        if (AXTT[4] == AXUP) or (obj_active.meshname == ""):
            # draw alert constraint name if track axis and
            # up axis are equal or if target is missing
            row.alert = True
        row.prop(obj_active, 'consname', text="")
        row.alert = False
        row.prop(obj_active, 'flagIO', icon=con, icon_only=True, emboss=False)
        row.operator("object.rem_cons", text="", icon='X', emboss=False)

        # draw 2nd row (target)
        row = box.row()
        row.prop_search(
            obj_active, "meshname", obj_active, "meshlist",
            text="Target", icon='OBJECT_DATA'
        )
        row = box.row(align=True)

        # draw 3rd row (track to axis)
        row.label(text="To:")
        row.prop(obj_active, "track_axis", expand=True)

        # draw 4th row (up axis)
        row = box.row()
        row.prop(obj_active, "up_axis", text="Up")

        # draw 5th row (influence slider)
        row = box.row()
        row.prop(obj_active, 'infl', slider=True, text="Influence")


class NORMTOCONS_ADD_Button(bpy.types.Operator):
    '''create constraint'''
    bl_idname = "object.add_cons"
    bl_label = "Add Normal To Surface constraint"
    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(cls, context):
        '''poll to activate/desactivate button'''
        obj_active = context.active_object
        objs_sel = [o for o in context.selected_objects]
        poll_v = (obj_active.get('flagEX') is None) and (len(objs_sel) == 1)
        return poll_v

    # declare variables
    bpy.types.Object.meshlist = bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup
    )
    bpy.types.Object.meshname = bpy.props.StringProperty()
    bpy.types.Object.flagEX = bpy.props.BoolProperty(
        default=False
    )
    bpy.types.Object.flagIO = bpy.props.BoolProperty(
        default=True, description="Enable/Disable Constraint"
    )
    bpy.types.Object.infl = bpy.props.FloatProperty(
        min=0.000, max=1.000, default=1.000,
        description="Amount of influence constraint will have on the final solution"
    )
    bpy.types.Object.consname = bpy.props.StringProperty(
        default="Normal To", description="Constraint name"
    )

    def execute(self, context):
        '''create/set custom properties default values'''
        obj_active = context.active_object
        rot_mode = obj_active.rotation_mode

        obj_active.rotation_mode = "QUATERNION"
        createmeshlist(obj_active, context)
        obj_active.meshname = bpy.data.objects[int(self.target)].name
        StoreGlobVar.mesh = bpy.data.objects.get(str(obj_active.meshname))
        obj_active.flagEX = True
        obj_active.flagIO = True
        obj_active.infl = 1.000
        obj_active.consname = "Normal To"
        obj_active.track_axis = 'POS_Y'
        obj_active.up_axis = 'Z'
        obj_active.rotation_mode = rot_mode
        self.report({'INFO'}, "Constraint created")
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                bpy.ops.view3d.modal_operator({'area': area}, 'INVOKE_DEFAULT')
                break
        return {'FINISHED'}

    target = bpy.props.EnumProperty(items=avail_meshs, name="Target:")

    def invoke(self, context, event):
        self.target
        return {'FINISHED'}


class NORMTOCONS_REM_Button(bpy.types.Operator):
    '''define remove constraint button'''
    bl_idname = "object.rem_cons"
    bl_label = "Remove Normal To Surface constraint"
    bl_description = "Remove constraint"
    bl_options = {'UNDO', 'REGISTER'}

    @classmethod
    def poll(cls, context):
        '''poll to activate/desactivate button'''
        ob = context.active_object
        return (ob.get('flagEX') is not None)

    def execute(self, context):
        '''delete custom properties and reset rotation'''
        objs = context.selected_objects
        RemoveCons(objs)
        self.report({'INFO'}, "Constraint removed")
        return {'FINISHED'}


class ModalDrawOperator(bpy.types.Operator):
    """draw relationship line in viewport"""
    bl_idname = "view3d.modal_operator"
    bl_label = "Simple Modal View3D Operator"

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback_px, args, 'WINDOW', 'POST_VIEW'
            )
            self.mouse_path = []
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_module(__name__)
    bpy.app.handlers.scene_update_pre.clear()
    bpy.app.handlers.scene_update_pre.append(NormalCons)
    bpy.app.handlers.load_post.clear()
    bpy.app.handlers.load_post.append(DeclMesh)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.app.handlers.scene_update_pre.remove(NormalCons)
    bpy.app.handlers.load_post.remove(DeclMesh)
    RemoveCons(bpy.context.scene.objects.values())

if __name__ == "__main__":
    register()
