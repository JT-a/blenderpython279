#
# Apart from some edits, this is really the work of Stanislav Blinov, Yigit Savtur
# THANKS FOR WORKIN THIS OUT!
#

import bpy, bmesh
from bpy.types import Operator
from mathutils import Vector

class VertexGroupToMask(bpy.types.Operator):
    '''Replaces the current sculpting mask with the currently active vertex group.'''
    bl_idname = "mesh.vgrouptomask"
    bl_label = "Vertex Group To Mask"
    bl_options = {'REGISTER', 'UNDO'}

    index = bpy.props.IntProperty(
        default = -1
    )

    @classmethod

    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None :
            vGroupLocked = context.active_object.vertex_groups.active.lock_weight

            if vGroupLocked == False :
               if context.sculpt_object.use_dynamic_topology_sculpting :
                  dynatopoEnabled = True
                  bpy.ops.sculpt.dynamic_topology_toggle()

               bmeshContainer = bmesh.new() # New bmesh container
               bmeshContainer.from_mesh(context.active_object.data) # Fill container with our object

               activeVertexGroup = context.active_object.vertex_groups.active  # Set active vgroup

               if self.index is not -1:
                   activeVertexGroup = context.active_object.vertex_groups[self.index]

               mask = bmeshContainer.verts.layers.paint_mask.verify() # get active mask layer
               bmeshContainer.verts.ensure_lookup_table() # Update vertex lookup table

               for x in context.active_object.data.vertices: # For each x vert
                   bmeshContainer.verts[x.index] [mask] = 0.0 # Set mask to 0 weight

                   if len(x.groups) > 0: # if vert is a member of a vgroup
                    for y in x.groups: # For each y vgroup in group list
                       if y.group == activeVertexGroup.index: # if y is active group x belongs to
                          if activeVertexGroup.weight(x.index) > 0 :  # and x vert weight is not zero

                             currVert = bmeshContainer.verts[x.index]  # current vert is x bmesh vert
                             maskWeight = activeVertexGroup.weight(x.index) # set weight from active vgroup
                             currVert[mask] = maskWeight # assign weight to custom data layer


               bmeshContainer.to_mesh(context.active_object.data) # Fill obj data with bmesh data
               bmeshContainer.free() # Release bmesh

               if dynatopoEnabled :
                   bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}

# APPEND
class VertexGroupToMaskAppend(bpy.types.Operator):
    '''(! EXPERIMENTAL !) Adds the currently active vertex group on top of the current sculpting mask.'''
    bl_idname = "mesh.vgrouptomask_append"
    bl_label = "Append Vertex Group To Mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod

    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None :
            vGroupLocked = context.active_object.vertex_groups.active.lock_weight

            if vGroupLocked == False :
               if context.sculpt_object.use_dynamic_topology_sculpting :
                    dynatopoEnabled = True
                    bpy.ops.sculpt.dynamic_topology_toggle()

               bmeshContainer = bmesh.new() # New bmesh container
               bmeshContainer.from_mesh(context.active_object.data) # Fill container with our object
               activeVertexGroup = context.active_object.vertex_groups.active  # Set active vgroup
               mask = bmeshContainer.verts.layers.paint_mask.verify() # get active mask layer
               bmeshContainer.verts.ensure_lookup_table() # Update vertex lookup table

               for x in context.active_object.data.vertices: # For each x vert
                   if len(x.groups) > 0: # if vert is a member of a vgroup
                    for y in x.groups: # For each y vgroup in group list
                       if y.group == activeVertexGroup.index: # if y is active group x belongs to
                           if activeVertexGroup.weight(x.index) > 0 :  # and x vert weight is not zero

                             currVert = bmeshContainer.verts[x.index]  # current vert is x bmesh vert
                             maskWeight = activeVertexGroup.weight(x.index) # set weight from active vgroup
                             currVert[mask] = (maskWeight + currVert[mask]) # add current mask weight to maskweight and assign
                             if currVert[mask] > 1.0 : # is current mask weight greater than 0-1 range
                                 currVert[mask] = 1.0 # then Normalize mask weight


               bmeshContainer.to_mesh(context.active_object.data) # Fill obj data with bmesh data
               bmeshContainer.free() # Release bmesh

               if dynatopoEnabled :
                   bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}

#REMOVE
class VertexGroupToMaskRemove(bpy.types.Operator):
    '''(! EXPERIMENTAL !) Subtracts the currently active vertex group from the current sculpting mask.'''
    bl_idname = "mesh.vgrouptomask_remove"
    bl_label = "Remove Vertex Group From Mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod

    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False
        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None :

            vGroupLocked = context.active_object.vertex_groups.active.lock_weight
            if vGroupLocked == False :
               if context.sculpt_object.use_dynamic_topology_sculpting :

                    dynatopoEnabled = True
                    bpy.ops.sculpt.dynamic_topology_toggle()

               bmeshContainer = bmesh.new() # New bmesh container
               bmeshContainer.from_mesh(context.active_object.data) # Fill container with our object
               activeVertexGroup = context.active_object.vertex_groups.active  # Set active vgroup
               mask = bmeshContainer.verts.layers.paint_mask.verify()  # get active mask layer
               bmeshContainer.verts.ensure_lookup_table() # Update vertex lookup table

               for x in context.active_object.data.vertices: # For each x vert
                   if len(x.groups) > 0: # if vert is a member of a vgroup
                    for y in x.groups: # For each y vgroup in group list
                       if y.group == activeVertexGroup.index: # if y is active group x belongs to
                           if activeVertexGroup.weight(x.index) > 0 :  # and x vert weight is not zero

                             currVert = bmeshContainer.verts[x.index]  # current vert is x bmesh vert
                             maskWeight = activeVertexGroup.weight(x.index) # set weight from active vgroup
                             currVert[mask] -= (maskWeight * currVert[mask]) # multiply current mask with maskweight and subtract
                             if currVert[mask] < 0 : # is current mask weight less than 0
                                 currVert[mask] = 0 # then Normalize mask weight


               bmeshContainer.to_mesh(context.active_object.data) # Fill obj data with bmesh data
               bmeshContainer.free() # Release bmesh

               if dynatopoEnabled :
                   bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}

# CREATE NEW
class MaskToVertexGroup(bpy.types.Operator):
    '''Saves the current mask as a vertex group.'''
    bl_idname = "mesh.masktovgroup"
    bl_label = "Mask To Vertex Group"
    bl_options = {'REGISTER'}

    new_group = bpy.props.BoolProperty(default=True)

    @classmethod

    def poll(cls, context):

        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):

        dynatopoEnabled = False
        if context.active_object.mode == 'SCULPT' :
           if context.sculpt_object.use_dynamic_topology_sculpting :
               dynatopoEnabled = True
               bpy.ops.sculpt.dynamic_topology_toggle()

           #print(context.active_object.use_dynamic_topology_sculpting)

           bmeshContainer = bmesh.new() # New bmesh container
           bmeshContainer.from_mesh(context.sculpt_object.data) # Fill container with our object

           mask = bmeshContainer.verts.layers.paint_mask.verify() # Set the active mask layer as custom layer

           newVertexGroup = context.active_object.vertex_groups.active
           if self.new_group is True:
               newVertexGroup = context.sculpt_object.vertex_groups.new(name = "Mask") # Create an empty vgroup
           bmeshContainer.verts.ensure_lookup_table() # Just incase > Remove if unneccessary

           for x in bmeshContainer.verts:  # itterate from bmesh.verts
               if x[mask] > 0 : # if x BMVert has mask weight

                   maskWeight = x[mask] # assign float variable for weight from mask layer
                   newVertexGroup.add([x.index], maskWeight, "REPLACE") # add it to vgroup, set mask weight
               else :
                   newVertexGroup.add([x.index], 0, "REPLACE")

           bmeshContainer.free()

           if dynatopoEnabled :
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

        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None :
            vGroupLocked = context.sculpt_object.vertex_groups.active.lock_weight

            if vGroupLocked == False :
               if context.sculpt_object.use_dynamic_topology_sculpting :
                    dynatopoEnabled = True
                    bpy.ops.sculpt.dynamic_topology_toggle()

               bmeshContainer = bmesh.new() # New bmesh container
               bmeshContainer.from_mesh(context.sculpt_object.data) # Fill container with our object
               activeVertexGroup = context.sculpt_object.vertex_groups.active  # Set active vgroup
               mask = bmeshContainer.verts.layers.paint_mask.verify() # Set the active mask layer as custom layer
               bmeshContainer.verts.ensure_lookup_table() # Just incase > Remove if unneccessary

               for x in bmeshContainer.verts:  # itterate from bmesh.verts
                   if x[mask] > 0 : # if x BMVERT has mask weight
                       maskWeight = x[mask] # assign float variable for weight from mask layer
                       activeVertexGroup.add([x.index],maskWeight,"ADD") # add it to vgroup, set mask weight

               bmeshContainer.free()

               if dynatopoEnabled :
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

        if context.active_object.mode == 'SCULPT'and context.active_object.vertex_groups.active is not None :
            vGroupLocked = context.active_object.vertex_groups.active.lock_weight

            if vGroupLocked == False :
               if context.sculpt_object.use_dynamic_topology_sculpting :
                   dynatopoEnabled = True
                   bpy.ops.sculpt.dynamic_topology_toggle()

               bmeshContainer = bmesh.new() # New bmesh container
               bmeshContainer.from_mesh(context.sculpt_object.data) # Fill container with our object
               activeVertexGroup = context.sculpt_object.vertex_groups.active  # Set active vgroup
               mask = bmeshContainer.verts.layers.paint_mask.verify() # Set the active mask layer as custom layer
               bmeshContainer.verts.ensure_lookup_table() # Just incase > Remove if unneccessary

               for x in bmeshContainer.verts:  # itterate from bmesh.verts
                   if x[mask] > 0 : # if x BMVert has mask weight
                       maskWeight = x[mask] # assign float variable for weight from mask layer
                       activeVertexGroup.add([x.index], maskWeight,"SUBTRACT") # add it to vgroup, set mask weight

               bmeshContainer.free()

               if dynatopoEnabled :
                   bpy.ops.sculpt.dynamic_topology_toggle()

                    #print("Mask Removed from Vertex Group")

        return {'FINISHED'}

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
