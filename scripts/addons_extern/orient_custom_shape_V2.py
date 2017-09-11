# <pep8 compliant>
#
# orient_custom_shape.py
#
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
    "name": "Orient Custom Shape",
    "author": "Gilles Pagia & Ron Tarrant",
    "version": (0,1),
    "blender": (2, 6, 3),
    "api": 46487,
    "location": "Properties > Bone > Orient Custom Shape (visible in pose mode only)",
    "description": "Rotates, scales and translates a custom bone shape to match rotation, scale and translation of its bone",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"}

"""
Orient Custom Shape
This script orients the translation, rotation and scale of a bone's custom shape
to match the rotation, translation and scaling of the bone itself. Once orientation
is matched, editing the mesh to put the bone 'handle' where it's needed is far
easier.
This script takes the opposite approach to that of Auto Custom Shape. Auto
Custom Shape creates a new mesh object each time. Orient Custom Shape uses
whatever pre-built mesh object you'd care to use.

Usage:
1) Install and activate the script in the Add-Ons tab of User Preferences,
2) build a rig,
3) load or build a set of custom shape meshes,
4) go to Pose Mode,
5) for each bone that will have a Custom Shape, set the custom shape using
   the drop-down menu in Bone Properties -> Display,
6) click on the Orient Bone Shape button,

This is continued Usage just for version 1:
7) Select the shape mesh (the mesh assigned to the bone in Step 5),
8) switch to Edit Mode,
9) select all vertices, and
10) reposition/rotation/whatever until you're happy with the placement.


The "Orient Bone Shape" panel and button will only be visible in pose mode.

Version history:
v0.1 - Initial revision.
"""
# version 2 - updated by Michael B : There is no need to set the pivot point of the custom shape object in advance
#        or apply transformation & steps 7-10 were removed :)
#        It can also detete the original picked custom shape with a checkbox and extract it back when needed with a click of a button
#        (the custom shape should be a mesh object so if you use a text change it with Alt C to a mesh)



import bpy
from mathutils import *
from bpy.props import BoolProperty

# version 2 update functions start (part 1/9) ------------------------------------------------------------------------
def areas_tuple():
    res = {}
    count = 0
    for area in bpy.context.screen.areas:
        res[area.type] = count
        count += 1
    return res

def get_override(area_type, region_type):
    '''Returns a dictionary which can be used to override certain bpy operators'''

    for area in bpy.context.screen.areas:
        if area.type == area_type:
            for region in area.regions:
                if region.type == region_type:
                    override = {'area': area, 'region': region}
                    return override
    #error message if the area or region wasn't found
    raise RuntimeError("Wasn't able to find", region_type," in area ", area_type,
                        "\n Make sure it's open while executing script.")









class BONE_OT_extract_custom_shape(bpy.types.Operator):
    '''Extract the bone's selected custom shape as a new object'''
    bl_idname = "object.extract_custom_shape"
    bl_label = "Extract custom shape"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        armatureName = bpy.context.active_object.name
        armature = bpy.data.objects[armatureName]

        activePoseBone = bpy.context.active_pose_bone
        boneName = bpy.context.active_pose_bone.name
        bone = armature.data.bones[boneName]

        # If the user didn't pick a custom_shape return
        if not activePoseBone.custom_shape:
            return {'CANCELLED'}

        objectName = activePoseBone.custom_shape.name
        shapeObject = bpy.data.objects[objectName]

        # get the scene
        bpy.context.window.screen.scene = bpy.data.scenes['Scene']
        # Create new mesh
        name = objectName
        mesh = bpy.data.meshes.new(name)
        # Create new object associated with the mesh
        ob_new = bpy.data.objects.new(name, mesh)
 
        # Copy data block from the old object into the new object
        ob_new.data = shapeObject.data.copy()
        ob_new.scale = shapeObject.scale
        ob_new.rotation_euler = shapeObject.rotation_euler
        ob_new.location = shapeObject.location
        
        # Link new object to the given scene and select it
        bpy.context.window.screen.scene.objects.link(ob_new)

        # switch from Pose mode to Object mode & select the new duplicated custom shape
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        ob_new.select = True
 
        return {'FINISHED'}

# version 2 update functions end (part 1/9) ------------------------------------------------------------------------











class BONE_OT_orient_custom_shape(bpy.types.Operator):
    '''Matches the bone's selected custom shape to the bone's orientation'''
    bl_idname = "object.orient_custom_shape"
    bl_label = "Orient custom shape"
    bl_options = {'REGISTER', 'UNDO'}





    def execute(self, context):

        armatureName = bpy.context.active_object.name
        armature = bpy.data.objects[armatureName]

        activePoseBone = bpy.context.active_pose_bone
        boneName = bpy.context.active_pose_bone.name
        bone = armature.data.bones[boneName]

        # version 2 update start (part 2/9) ------------------------------------------------------------------------------------------------------
        # If the user didn't pick a custom_shape return
        if not activePoseBone.custom_shape:
            return {'CANCELLED'}
        # version 2 update start (part 2/9) ------------------------------------------------------------------------------------------------------

        objectName = activePoseBone.custom_shape.name
        shapeObject = bpy.data.objects[objectName]


        # version 2 update start (part 3/9) ------------------------------------------------------------------------------------------------------

        # here we set the pivot point of the shape object to the head of the selected bone position
        # and we apply rotation & scale transformation to the shape object before we begin using it

        #override the rotate operator - this is needed to really change the pivot center
        override = get_override('VIEW_3D', 'WINDOW')
        # change the pivot center
        areas = areas_tuple()
        view3d = bpy.context.screen.areas[areas['VIEW_3D']].spaces[0]
        old_pivot_point_center = view3d.pivot_point
        old_cursor_location = view3d.cursor_location

        head_of_bone_location = bpy.data.objects[armatureName].location + context.active_pose_bone.head

        # switching from Pose mode to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # switching from selected armature to selected shapeObject
        bpy.ops.object.select_all(action='DESELECT')
        shapeObject.select = True
        bpy.context.scene.objects.active = shapeObject

        # give 3dcursor new coordinates
        bpy.context.scene.cursor_location = head_of_bone_location
        # set the origin on the current object to the 3dcursor location
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # apply object transformation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        #restore object selection & mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        # version 2 update end (part 3/9) -----------------------------------------------------------------------------------------------------











        bpy.context.active_object.name = armatureName
        armature = bpy.data.objects[armatureName]

        #bpy.context.active_pose_bone = activePoseBone
        boneName = bpy.context.active_pose_bone.name
        bone = armature.data.bones[boneName]

        objectName = activePoseBone.custom_shape.name
        shapeObject = bpy.data.objects[objectName]

        # Rotate shape object to match bone local rotation in the armature.
        shapeObject.rotation_euler = (0.0, 0.0, 0.0)
        boneChain = bone.parent_recursive
        boneChain.insert(0, bone)

        bone.show_wire = True

        for boneRotation in boneChain:
            rotationMatrix = Matrix((boneRotation.x_axis, boneRotation.y_axis, boneRotation.z_axis)).transposed()
            shapeObject.rotation_euler.rotate(rotationMatrix)

        # Same with translation and scaling.
        shapeObject.location = bone.head_local
        shapeObject.scale = bone.length * Vector((1.0, 1.0, 1.0))

        # Move object to armature coordinates system (except scaling, see below).
        rotationMatrix = armature.rotation_euler
        shapeObject.rotation_euler.rotate(rotationMatrix)
        shapeObject.location.rotate(rotationMatrix)
        shapeObject.location += armature.location


        # Display warning message if the armature has scaling different to one.
        scale = armature.scale

        if(scale.x != 1) or (scale.y != 1) or (scale.z != 1):
            self.report({'Warning'}, "Armature should have a scale factor of 1.0 to match bone shape properly")





        # version 2 update start (part 4/9) ------------------------------------------------------------------------
        # here we transform the shape object in Edit mode back into its original place
        # by using scaling & rotation in Edit mode around the head of the bone position

        # switching from Pose mode to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # switching from selected armature to selected shapeObject
        bpy.ops.object.select_all(action='DESELECT')
        shapeObject.select = True
        # switching from Object mode to Edit mode and selecting all vertices
        bpy.context.scene.objects.active = shapeObject
        # checking if the poll() function let as switch to Edit mode (sometimes it doesn't want to)
        if bpy.ops.object.editmode_toggle.poll():
            bpy.ops.object.editmode_toggle()
        else:
            #restore object selection & mode
            bpy.context.scene.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')
            #restore old cursor position
            view3d.pivot_point = old_pivot_point_center
            view3d.cursor_location = old_cursor_location
            return {'CANCELLED'}

        bpy.ops.mesh.select_all(action='SELECT')

        # this will cause the scale to be around the cursor position which is currently at the bone position
        old_pivot_point_center = view3d.pivot_point
        old_cursor_location = view3d.cursor_location
        # set the pivot center mode to 3dCursor and set the cursor
        view3d.pivot_point='CURSOR'
        view3d.cursor_location = shapeObject.location

	# scaling the shapeObject back into place in Edit mode with the pivot point as the 3dcursor
        bpy.ops.transform.resize(override,value=((1/ shapeObject.scale.x),(1/ shapeObject.scale.y),(1/ shapeObject.scale.z)))
        # rotating the shapeObject back into place in Edit mode with the pivot point as the 3dcursor
        bpy.ops.transform.rotate(override, value=(-1 * shapeObject.rotation_euler[2]), axis=(0, 0, 1))
        bpy.ops.transform.rotate(override, value=(-1 * shapeObject.rotation_euler[1]), axis=(0, 1, 0))
        bpy.ops.transform.rotate(override, value=(-1 * shapeObject.rotation_euler[0]), axis=(1, 0, 0))

        # if the "Delete original custom shape" checkbox in the properties panel is checked then select & delete the custom shape
        if context.scene.deleteOriginalCustomShape:
              # delete the shapeObject
              bpy.ops.object.mode_set(mode='OBJECT')
              # switching from selected armature to selected shapeObject
              bpy.ops.object.select_all(action='DESELECT')
              shapeObject.select = True
              bpy.context.scene.objects.active = shapeObject
              # remove all selected.
              bpy.ops.object.delete()

        #restore object selection & mode
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = armature
        bpy.ops.object.mode_set(mode='POSE')
        #restore old cursor position
        view3d.pivot_point = old_pivot_point_center
        view3d.cursor_location = old_cursor_location
        # version 2 update end (part 4/9) ------------------------------------------------------------------------




        return {'FINISHED'}


class BONE_PT_orient_custom_shape(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "bone"
    bl_label = "Orient the custom shape to match the bone"

    # version 2 update start (part 5/9) ------------------------------------------------------------------------
    # add your custom property to the Scene type
    bpy.types.Scene.deleteOriginalCustomShape = BoolProperty(
    name="Delete original custom shape",
    description="Delete the original custom shape",
    default = True)
    # version 2 update end (part 5/9) ------------------------------------------------------------------------
    @classmethod
    def poll(cls, context):
        if context.edit_bone:
            return True

        ob = context.object
        return ob and ob.mode == 'POSE' and context.bone

    def draw(self, context):
        layout = self.layout
        bone = context.bone
        if not bone:
            bone = context.edit_bone
        # version 2 update start (part 6/9) ------------------------------------------------------------------------
        # draw the checkbox (implied from property type = bool)
        layout.prop(context.scene, "deleteOriginalCustomShape")
        # version 2 update end (part 6/9) ------------------------------------------------------------------------
        row = layout.row()
        # version 2 update start (part 7/9) ------------------------------------------------------------------------
        split = row.split(percentage=0.7)
        col_left = split.column()
        col_right = split.column()
        col_left.operator("object.orient_custom_shape", text="Orient Custom Shape", icon='BONE_DATA')
        col_right.operator("object.extract_custom_shape", text="Extract Shape", icon='BONE_DATA')



def render_panel(self, context):
    layout = self.layout
    bone = context.bone
    if not bone:
        bone = context.edit_bone
    row = layout.row()
    split = row.split(percentage=0.4)
    col_left = split.column()
    col_right = split.column()
    col_left.operator("object.extract_custom_shape", text="Extract Shape") #, icon='MESH_CUBE'
    col_right.operator("object.orient_custom_shape", text="Orient Custom Shape") #, icon='BONE_DATA'
    # draw the checkbox (implied from property type = bool)
    layout.prop(context.scene, "deleteOriginalCustomShape")

    # version 2 update end (part 7/9) ------------------------------------------------------------------------

def register():
    bpy.utils.register_class(BONE_OT_orient_custom_shape)
    # version 2 update start (part 8/9) ------------------------------------------------------------------------
    bpy.utils.register_class(BONE_OT_extract_custom_shape)
    #bpy.utils.register_class(BONE_PT_orient_custom_shape)
    # here we append the render_panel function to the Display part of the bone 
    bpy.types.BONE_PT_display.append(render_panel)
    # version 2 update end (part 8/9) ------------------------------------------------------------------------

def unregister():
    bpy.utils.unregister_class(BONE_OT_orient_custom_shape)
    # version 2 update start (part 9/9) ------------------------------------------------------------------------
    bpy.utils.unregister_class(BONE_OT_extract_custom_shape)
    #bpy.utils.unregister_class(BONE_PT_orient_custom_shape)
    bpy.types.BONE_PT_display.remove(render_panel)
    # version 2 update end (part 9/9) ------------------------------------------------------------------------

if __name__ == "__main__":
    register()

