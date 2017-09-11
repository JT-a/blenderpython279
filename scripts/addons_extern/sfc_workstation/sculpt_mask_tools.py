#  ***** BEGIN GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  ***** END GPL LICENSE BLOCK *****

bl_info = {
    "name": "Mask Tools",
    "author": "Stanislav Blinov,Yigit Savtur",
    "version": (0, 35),
    "blender": (2, 7, 5),
    "location": "3d View > Tool shelf > Sculpt",
    "description": "Tools for Converting Sculpt Masks to Vertex groups",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sculpting"}

import bpy
import bmesh


class MaskToVertexGroup(bpy.types.Operator):
    '''Mask To Vertex Group'''
    bl_idname = "mesh.masktovgroup"
    bl_label = "Mask To Vertex Group"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT':

            if context.sculpt_object.use_dynamic_topology_sculpting:

                dynatopoEnabled = True

                bpy.ops.sculpt.dynamic_topology_toggle()

            # print(context.active_object.use_dynamic_topology_sculpting)

            bmeshContainer = bmesh.new()  # New bmesh container

            bmeshContainer.from_mesh(context.sculpt_object.data)  # Fill container with our object

            mask = bmeshContainer.verts.layers.paint_mask.verify()  # Set the active mask layer as custom layer

            newVertexGroup = context.sculpt_object.vertex_groups.new(name="Mask")  # Create an empty vgroup

            bmeshContainer.verts.ensure_lookup_table()  # Just incase > Remove if unneccessary

            for x in bmeshContainer.verts:  # itterate from bmesh.verts

                if x[mask] > 0:  # if x BMVert has mask weight

                    maskWeight = x[mask]  # assign float variable for weight from mask layer

                    newVertexGroup.add([x.index], maskWeight, "REPLACE")  # add it to vgroup, set mask weight
                else:

                    newVertexGroup.add([x.index], 0, "REPLACE")

            bmeshContainer.free()

            if dynatopoEnabled:

                bpy.ops.sculpt.dynamic_topology_toggle()

                #print("Mask Converted to Vertex Group")

        return {'FINISHED'}


# APPEND
class MaskToVertexGroupAppend(bpy.types.Operator):
    '''Append Mask To Vertex Group'''
    bl_idname = "mesh.masktovgroup_append"
    bl_label = "Append Mask To Vertex Group"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None:

            vGroupLocked = context.sculpt_object.vertex_groups.active.lock_weight

            if vGroupLocked == False:

                if context.sculpt_object.use_dynamic_topology_sculpting:

                    dynatopoEnabled = True

                    bpy.ops.sculpt.dynamic_topology_toggle()

                bmeshContainer = bmesh.new()  # New bmesh container

                bmeshContainer.from_mesh(context.sculpt_object.data)  # Fill container with our object

                activeVertexGroup = context.sculpt_object.vertex_groups.active  # Set active vgroup

                mask = bmeshContainer.verts.layers.paint_mask.verify()  # Set the active mask layer as custom layer

                bmeshContainer.verts.ensure_lookup_table()  # Just incase > Remove if unneccessary

                for x in bmeshContainer.verts:  # itterate from bmesh.verts

                    if x[mask] > 0:  # if x BMVERT has mask weight

                        maskWeight = x[mask]  # assign float variable for weight from mask layer

                        activeVertexGroup.add([x.index], maskWeight, "ADD")  # add it to vgroup, set mask weight

                bmeshContainer.free()

                if dynatopoEnabled:

                    bpy.ops.sculpt.dynamic_topology_toggle()

                    #print("Mask Added to Vertex Group")

        return {'FINISHED'}

# REMOVE


class MaskToVertexGroupRemove(bpy.types.Operator):
    '''Remove Mask From Vertex Group'''
    bl_idname = "mesh.masktovgroup_remove"
    bl_label = "Remove Mask From Vertex Group"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None:

            vGroupLocked = context.active_object.vertex_groups.active.lock_weight

            if vGroupLocked == False:

                if context.sculpt_object.use_dynamic_topology_sculpting:

                    dynatopoEnabled = True

                    bpy.ops.sculpt.dynamic_topology_toggle()

                bmeshContainer = bmesh.new()  # New bmesh container

                bmeshContainer.from_mesh(context.sculpt_object.data)  # Fill container with our object

                activeVertexGroup = context.sculpt_object.vertex_groups.active  # Set active vgroup

                mask = bmeshContainer.verts.layers.paint_mask.verify()  # Set the active mask layer as custom layer

                bmeshContainer.verts.ensure_lookup_table()  # Just incase > Remove if unneccessary

                for x in bmeshContainer.verts:  # itterate from bmesh.verts

                    if x[mask] > 0:  # if x BMVert has mask weight

                        maskWeight = x[mask]  # assign float variable for weight from mask layer

                        activeVertexGroup.add([x.index], maskWeight, "SUBTRACT")  # add it to vgroup, set mask weight

                bmeshContainer.free()

                if dynatopoEnabled:

                    bpy.ops.sculpt.dynamic_topology_toggle()

                    #print("Mask Removed from Vertex Group")

        return {'FINISHED'}


class VertexGroupToMask(bpy.types.Operator):
    '''Vertex Group To Mask'''
    bl_idname = "mesh.vgrouptomask"
    bl_label = "Vertex Group To Mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None:

            vGroupLocked = context.active_object.vertex_groups.active.lock_weight

            if vGroupLocked == False:

                if context.sculpt_object.use_dynamic_topology_sculpting:

                    dynatopoEnabled = True

                    bpy.ops.sculpt.dynamic_topology_toggle()

                bmeshContainer = bmesh.new()  # New bmesh container

                bmeshContainer.from_mesh(context.active_object.data)  # Fill container with our object

                activeVertexGroup = context.active_object.vertex_groups.active  # Set active vgroup

                mask = bmeshContainer.verts.layers.paint_mask.verify()  # get active mask layer

                bmeshContainer.verts.ensure_lookup_table()  # Update vertex lookup table

                for x in context.active_object.data.vertices:  # For each x vert

                    bmeshContainer.verts[x.index][mask] = 0.0  # Set mask to 0 weight

                    if len(x.groups) > 0:  # if vert is a member of a vgroup

                        for y in x.groups:  # For each y vgroup in group list

                            if y.group == activeVertexGroup.index:  # if y is active group x belongs to

                                if activeVertexGroup.weight(x.index) > 0:  # and x vert weight is not zero

                                    currVert = bmeshContainer.verts[x.index]  # current vert is x bmesh vert

                                    maskWeight = activeVertexGroup.weight(x.index)  # set weight from active vgroup

                                    currVert[mask] = maskWeight  # assign weight to custom data layer

                bmeshContainer.to_mesh(context.active_object.data)  # Fill obj data with bmesh data

                bmeshContainer.free()  # Release bmesh

                if dynatopoEnabled:

                    bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}

# APPEND


class VertexGroupToMaskAppend(bpy.types.Operator):
    '''Append Vertex Group To Mask'''
    bl_idname = "mesh.vgrouptomask_append"
    bl_label = "Append Vertex Group To Mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None:

            vGroupLocked = context.active_object.vertex_groups.active.lock_weight

            if vGroupLocked == False:

                if context.sculpt_object.use_dynamic_topology_sculpting:

                    dynatopoEnabled = True

                    bpy.ops.sculpt.dynamic_topology_toggle()

                bmeshContainer = bmesh.new()  # New bmesh container

                bmeshContainer.from_mesh(context.active_object.data)  # Fill container with our object

                activeVertexGroup = context.active_object.vertex_groups.active  # Set active vgroup

                mask = bmeshContainer.verts.layers.paint_mask.verify()  # get active mask layer

                bmeshContainer.verts.ensure_lookup_table()  # Update vertex lookup table

                for x in context.active_object.data.vertices:  # For each x vert

                    if len(x.groups) > 0:  # if vert is a member of a vgroup

                        for y in x.groups:  # For each y vgroup in group list

                            if y.group == activeVertexGroup.index:  # if y is active group x belongs to

                                if activeVertexGroup.weight(x.index) > 0:  # and x vert weight is not zero

                                    currVert = bmeshContainer.verts[x.index]  # current vert is x bmesh vert

                                    maskWeight = activeVertexGroup.weight(x.index)  # set weight from active vgroup

                                    currVert[mask] = (maskWeight + currVert[mask])  # add current mask weight to maskweight and assign
                                    if currVert[mask] > 1.0:  # is current mask weight greater than 0-1 range

                                        currVert[mask] = 1.0  # then Normalize mask weight

                bmeshContainer.to_mesh(context.active_object.data)  # Fill obj data with bmesh data

                bmeshContainer.free()  # Release bmesh

                if dynatopoEnabled:

                    bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}

# REMOVE


class VertexGroupToMaskRemove(bpy.types.Operator):
    '''Remove Vertex Group From Mask'''
    bl_idname = "mesh.vgrouptomask_remove"
    bl_label = "Remove Vertex Group From Mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None:

            vGroupLocked = context.active_object.vertex_groups.active.lock_weight

            if vGroupLocked == False:

                if context.sculpt_object.use_dynamic_topology_sculpting:

                    dynatopoEnabled = True

                    bpy.ops.sculpt.dynamic_topology_toggle()

                bmeshContainer = bmesh.new()  # New bmesh container

                bmeshContainer.from_mesh(context.active_object.data)  # Fill container with our object

                activeVertexGroup = context.active_object.vertex_groups.active  # Set active vgroup

                mask = bmeshContainer.verts.layers.paint_mask.verify()  # get active mask layer

                bmeshContainer.verts.ensure_lookup_table()  # Update vertex lookup table

                for x in context.active_object.data.vertices:  # For each x vert

                    if len(x.groups) > 0:  # if vert is a member of a vgroup

                        for y in x.groups:  # For each y vgroup in group list

                            if y.group == activeVertexGroup.index:  # if y is active group x belongs to

                                if activeVertexGroup.weight(x.index) > 0:  # and x vert weight is not zero

                                    currVert = bmeshContainer.verts[x.index]  # current vert is x bmesh vert

                                    maskWeight = activeVertexGroup.weight(x.index)  # set weight from active vgroup

                                    currVert[mask] -= (maskWeight * currVert[mask])  # multiply current mask with maskweight and subtract
                                    if currVert[mask] < 0:  # is current mask weight less than 0

                                        currVert[mask] = 0  # then Normalize mask weight

                bmeshContainer.to_mesh(context.active_object.data)  # Fill obj data with bmesh data

                bmeshContainer.free()  # Release bmesh

                if dynatopoEnabled:

                    bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}


class MaskFromCavity(bpy.types.Operator):
    ''' Mask From Cavity'''
    bl_idname = "mesh.mask_from_cavity"
    bl_label = "Mask From Cavity"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    # A Property for cavity angle
    mask_cavity_angle = bpy.props.IntProperty(name="Cavity Angle", default=82, min=45, max=90)

    # A Property for cavity mask strength
    mask_cavity_strength = bpy.props.FloatProperty(name="Mask Strength", default=1.0, min=0.1, max=1.0)

    def execute(self, context):

        mask_cavity_angle = context.window_manager.mask_cavity_angle  # update property from user input

        mask_cavity_strength = context.window_manager.mask_cavity_strength  # update property from user input

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT':

            if context.sculpt_object.use_dynamic_topology_sculpting:

                dynatopoEnabled = True

                bpy.ops.sculpt.dynamic_topology_toggle()

            bmeshContainer = bmesh.new()  # New bmesh container

            bmeshContainer.from_mesh(context.active_object.data)  # Fill container with our object

            mask = bmeshContainer.verts.layers.paint_mask.verify()  # get active mask layer

            bmeshContainer.faces.ensure_lookup_table()  # Update vertex lookup table

            mask_cavity_angle *= (3.14 * 0.0055556)  # Convert angle to radians (approx)

            maskWeight = 1.0 * mask_cavity_strength

            for face in bmeshContainer.faces:

                for vert in face.verts:  # for each x face

                    vert[mask] = 0.0  # Clear any mask beforehand

                    for loop in vert.link_loops:

                        loopTan = loop.calc_tangent()

                        angleFace = (face.normal.angle(loopTan, 0.0))

                        angleDiff = (vert.normal.angle(loopTan, 0.0))  # get the angle between the vert normal to loop edge Tangent

#                        print ("Angle Diff: %f" % (angleDiff))
#                        print ("Cav Angle : %f" % (mask_cavity_angle))
#                        print ("Angle Face : %f" % (angleFace))
#                        print ("AD - AF : %f" % (angleDiff + angleFace))
#                        print ("Loop Tangent : [%s] " % loopTan)

                        if (angleFace + angleDiff) <= (1.57 + mask_cavity_angle):  # if the difference is greater then input

                            vert[mask] = maskWeight  # mask it with input weight

            bmeshContainer.to_mesh(context.active_object.data)  # Fill obj data with bmesh data

            bmeshContainer.free()  # Release bmesh

            if dynatopoEnabled:

                bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}


class MaskFromEdges(bpy.types.Operator):
    ''' Mask From Edges'''
    bl_idname = "mesh.mask_from_edges"
    bl_label = "Mask From Edges"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    # A Property for cavity angle
    mask_edge_angle = bpy.props.IntProperty(name="Sharp Angle", default=82, min=45, max=90)

    # A Property for cavity mask strength
    mask_edge_strength = bpy.props.FloatProperty(name="Mask Strength", default=1.0, min=0.1, max=1.0)

    def execute(self, context):

        mask_edge_angle = context.window_manager.mask_edge_angle  # update property from user input

        mask_edge_strength = context.window_manager.mask_edge_strength  # update property from user input

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT':

            if context.sculpt_object.use_dynamic_topology_sculpting:

                dynatopoEnabled = True

                bpy.ops.sculpt.dynamic_topology_toggle()

            bmeshContainer = bmesh.new()  # New bmesh container

            bmeshContainer.from_mesh(context.active_object.data)  # Fill container with our object

            mask = bmeshContainer.verts.layers.paint_mask.verify()  # get active mask layer

            bmeshContainer.faces.ensure_lookup_table()  # Update vertex lookup table

            mask_edge_angle *= (3.14 * 0.0055556)  # Convert angle to radians (approx)

            maskWeight = 1.0 * mask_edge_strength

            for face in bmeshContainer.faces:

                for vert in face.verts:  # for each x face

                    vert[mask] = 0.0  # Clear any mask beforehand

                    for loop in vert.link_loops:

                        loopTan = loop.calc_tangent()

                        angleFace = (face.normal.angle(-loopTan, 0.0))

                        angleDiff = (vert.normal.angle(-loopTan, 0.0))  # get the angle between the vert normal to loop edge Tangent

#                        print ("Angle Diff: %f" % (angleDiff))
#                        print ("Cav Angle : %f" % (mask_cavity_angle))
#                        print ("Angle Face : %f" % (angleFace))
#                        print ("AD - AF : %f" % (angleDiff + angleFace))
#                        print ("Loop Tangent : [%s] " % loopTan)

                        if (angleFace + angleDiff) <= (1.57 + mask_edge_angle):  # if the difference is greater then input

                            vert[mask] = maskWeight  # mask it with input weight

            bmeshContainer.to_mesh(context.active_object.data)  # Fill obj data with bmesh data

            bmeshContainer.free()  # Release bmesh

            if dynatopoEnabled:

                bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}


class MaskSmoothAll(bpy.types.Operator):
    ''' Mask Smooth All'''
    bl_idname = "mesh.mask_smooth_all"
    bl_label = "Mask Smooth All"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    mask_smooth_strength = bpy.props.FloatProperty(name="Mask Smooth Strength", default=0.25, min=0.1, max=1.0)

    def execute(self, context):

        mask_smooth_strength = context.window_manager.mask_smooth_strength  # update property from user input

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT':

            if context.sculpt_object.use_dynamic_topology_sculpting:

                dynatopoEnabled = True

                bpy.ops.sculpt.dynamic_topology_toggle()

            bmeshContainer = bmesh.new()  # New bmesh container

            bmeshContainer.from_mesh(context.active_object.data)  # Fill container with our object

            mask = bmeshContainer.verts.layers.paint_mask.active  # get active mask layer

            bmeshContainer.verts.ensure_lookup_table()  # Update vertex lookup table

            for vert in bmeshContainer.verts:

                for edge in vert.link_edges:

                    if vert[mask] < (edge.other_vert(vert)[mask] * abs(vert[mask] - mask_smooth_strength)):

                        vert[mask] = (edge.other_vert(vert)[mask] * abs(vert[mask] - mask_smooth_strength))

                    if vert[mask] < 0.0:

                        vert[mask] = 0.0

                    elif vert[mask] > 1.0:

                        vert[mask] = 1.0

            bmeshContainer.to_mesh(context.active_object.data)  # Fill obj data with bmesh data

            bmeshContainer.free()  # Release bmesh

            if dynatopoEnabled:

                bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}


"""
class MaskToolsPanel(bpy.types.Panel):
    ###Creates a Mask Tool Box in the Viewport Tool Panel
    bl_category = "Sculpt"
    bl_label = "Mask Tools"
    bl_idname = "MESH_OT_masktools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'


    def draw(self, context):
        layout = self.layout

        vgroupHeader = layout.row(align = True)
        vgroupHeader.label(text = "Vertex Group :", icon = 'GROUP_VERTEX')
        
        vGroupButtons = layout.row()
        vGroupButtons.operator("mesh.masktovgroup", text = "Create VGroup", icon = 'NONE')
        vGroupButtons.operator("mesh.masktovgroup_append", text = "Add", icon = 'DISCLOSURE_TRI_RIGHT')
        vGroupButtons.operator("mesh.masktovgroup_remove", text = "Remove", icon = 'DISCLOSURE_TRI_DOWN')
        
        space = layout.row()
        
        maskHeader = layout.row(align = True)
        maskHeader.label(text = "Mask :", icon = 'MOD_MASK')
        
        maskButtons = layout.row()
        maskButtons.operator("mesh.vgrouptomask", text = "Create Mask", icon='NONE')
        maskButtons.operator("mesh.vgrouptomask_append", text = "Add", icon = 'DISCLOSURE_TRI_RIGHT')
        maskButtons.operator("mesh.vgrouptomask_remove", text = "Remove", icon = 'DISCLOSURE_TRI_DOWN')

        space = layout.row()
        space = layout.row()

        maskEdgesHeader = layout.row(align = True)
        maskEdgesHeader.label(text = "Mask by Edges :", icon = 'MOD_MASK')
        maskEdgesHeader.operator("mesh.mask_from_edges", text = "Create", icon = 'NONE')
        
        maskEdges = layout.row(align = True)
        maskEdges.prop(bpy.context.window_manager,"mask_edge_angle", text = "Edge Angle",icon='MOD_MASK',slider = True)
        maskEdges.prop(bpy.context.window_manager,"mask_edge_strength", text = "Mask Strength", icon='MOD_MASK',slider = True)
        
        space = layout.row()
        space = layout.row()

        maskCavityHeader = layout.row(align = True)
        maskCavityHeader.label(text = "Mask by Cavity:", icon = 'MOD_MASK')
        maskCavityHeader.operator("mesh.mask_from_cavity", text = "Create", icon = 'NONE')
        
        maskCavity = layout.row(align = True)
        maskCavity.prop(bpy.context.window_manager,"mask_cavity_angle", text = "Cavity Angle",icon='MOD_MASK',slider = True)
        maskCavity.prop(bpy.context.window_manager,"mask_cavity_strength", text = "Mask Strength", icon='MOD_MASK',slider = True)
        
        space = layout.row()
        space = layout.row()

        maskCavityHeader = layout.row(align = True)
        maskCavityHeader.label(text = "Mask Smooth", icon = 'MOD_MASK')
        maskCavityHeader.operator("mesh.mask_smooth_all", text = "Smooth", icon = 'NONE')
        
        maskCavity = layout.row(align = False)
        maskCavity.prop(bpy.context.window_manager,"mask_smooth_strength", text = "Mask Smooth Strength", icon='MOD_MASK',slider = True)

"""


def register():

    bpy.types.WindowManager.mask_edge_angle = MaskFromEdges.mask_edge_angle

    bpy.types.WindowManager.mask_edge_strength = MaskFromEdges.mask_edge_strength

    bpy.types.WindowManager.mask_cavity_angle = MaskFromCavity.mask_cavity_angle

    bpy.types.WindowManager.mask_cavity_strength = MaskFromCavity.mask_cavity_strength

    bpy.types.WindowManager.mask_smooth_strength = MaskSmoothAll.mask_smooth_strength

    bpy.utils.register_module(__name__)


def unregister():

    bpy.types.WindowManager.mask_edge_angle

    bpy.types.WindowManager.mask_edge_strength

    bpy.types.WindowManager.mask_cavity_angle

    bpy.types.WindowManager.mask_cavity_strength

    bpy.types.WindowManager.mask_smooth_strength

    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
