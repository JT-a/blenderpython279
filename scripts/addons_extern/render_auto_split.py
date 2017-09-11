# BEGIN GPL LICENSE BLOCK #####
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
# END GPL LICENSE BLOCK #####

import bpy
from math import radians

bl_info = {
    "name": "AutoSplit",
    "author": "Ted VjBros",
    "version": (0, 1, 0),
    "blender": (2, 72, 0),
    "location": "Scene > AutoSplit",
    "description": "Split Objects in 2 renders",
    "category": "Render"}


def layerAdd(array1, array2):
    returnArray = [False] * 20
    for i in range(20):
        returnArray[i] = array1[i] or array2[i]
    return returnArray


def layerSubstract(array1, array2):
    returnArray = [False] * 20
    for i in range(20):
        returnArray[i] = array1[i] ^ array2[i]
    return returnArray


class AutoSplit(bpy.types.Operator):
    bl_idname = "scene.autosplit"
    bl_label = "AutoSplit"

    @classmethod
    def poll(cls, context):
        if (context.selected_objects):
            return True
        return False

    def execute(self, context):
        # Save Selection
        selectedObjects = context.selected_objects

        # Move other objects to layer
        layer5 = [False] * 20
        layer5[4] = True

        bpy.ops.object.select_all(action='INVERT')
        context.scene.layers = layerAdd(context.scene.layers, layer5)
        bpy.ops.object.move_to_layer(layers=layer5)
        bpy.ops.object.select_all(action='INVERT')

        # Move Selected to layer 1
        layer1 = [False] * 20
        layer1[0] = True

        context.scene.layers = layerAdd(context.scene.layers, layer1)
        # bpy.ops.object.move_to_layer('INVOKE_DEFAULT', layers = layer1)
        bpy.ops.object.move_to_layer(layers=layer1)
        context.scene.layers = layerAdd(context.scene.layers, layer1)

        # Duplicate
        duplicatePoll = []
        for sel in selectedObjects:
            if "Split" not in sel:
                sel["Split"] = "Front"
                duplicatePoll.append(sel)
            else:
                if sel["Split"] != "Front":
                    sel["Split"] = "Front"

        if len(duplicatePoll):
            override = {'selected_object': list(duplicatePoll)}
            bpy.ops.object.duplicate(override, 'INVOKE_DEFAULT', linked=True)

        # Save Duplicate Selection
        duplicatedObjects = context.selected_objects
        # Split prop to "Back"
        for Dupli in duplicatedObjects:
            Dupli["Split"] = "Back"

        # Move Duplicates to layer 11
        layer11 = [False] * 20
        layer11[10] = True
        context.scene.layers = layerAdd(context.scene.layers, layer11)
        bpy.ops.object.move_to_layer(layers=layer11)

        # Add Splitting Plane for boolean
        if "SplitPlane" not in context.scene.objects:
            bpy.ops.mesh.primitive_plane_add(radius=10, view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(radians(90.0), 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            SplitPlane = context.scene.objects.active
            SplitPlane.name = "SplitPlane"
            SplitPlane.draw_type = 'WIRE'
        SplitPlane = context.scene.objects["SplitPlane"]

        # Apply Front Boolean
        for obj in selectedObjects:
            bpy.context.scene.objects.active = obj
            modifiers = obj.modifiers
            if "Split" not in modifiers:
                bpy.ops.object.modifier_add('INVOKE_DEFAULT', type='BOOLEAN')
                obj.modifiers["Boolean"].name = "Split"
                obj.modifiers["Split"].object = SplitPlane
            obj.modifiers["Split"].operation = 'DIFFERENCE'

        # Apply Back Boolean
        for obj in duplicatedObjects:
            bpy.context.scene.objects.active = obj
            modifiers = obj.modifiers
            if "Split" not in modifiers:
                bpy.ops.object.modifier_add(type='BOOLEAN')
                obj.modifiers["Boolean"].name = "Split"
                obj.modifiers["Split"].object = SplitPlane
            obj.modifiers["Split"].operation = 'INTERSECT'

        # Create Render Setup
        #  Create RenderLayers
        RenderLayers = context.scene.render.layers
        if "FrontRender" and "BackRender" not in RenderLayers:
            for layer in RenderLayers:
                layer.use = False
            FrontLayer = RenderLayers.new("FrontRender")
            BackLayer = RenderLayers.new("BackRender")
            FrontLayer.layers = layerSubstract(context.scene.layers, layer11)
            BackLayer.layers = layerSubstract(context.scene.layers, layer1)

        #  Create Node Setup
        context.scene.use_nodes = True
        tree = context.scene.node_tree
        tree.nodes.clear()

        FrontRL = tree.nodes.new('CompositorNodeRLayers')
        FrontRL.location = 0, 0
        FrontRL.name = "Front"
        FrontRL.label = "Front"
        FrontRL.layer = "FrontRender"

        BackRL = tree.nodes.new('CompositorNodeRLayers')
        BackRL.location = 0, -300
        BackRL.name = "Back"
        BackRL.label = "Back"
        BackRL.layer = "BackRender"

        RenderZ = tree.nodes.new('CompositorNodeZcombine')
        RenderZ.location = 200, 0
        RenderZ.use_alpha = True

        FrontFile = tree.nodes.new('CompositorNodeOutputFile')
        FrontFile.location = 200, -250
        FrontFile.name = "FrontFile"
        FrontFile.label = "FrontFile"
        FrontFile.base_path = "//Front/"

        BackFile = tree.nodes.new('CompositorNodeOutputFile')
        BackFile.location = 200, -400
        BackFile.name = "BackFile"
        BackFile.label = "BackFile"
        BackFile.base_path = "//Back/"

        Composite = tree.nodes.new('CompositorNodeComposite')
        Composite.location = 400, 0
        Composite.use_alpha = True

        tree.links.new(FrontRL.outputs[0], FrontFile.inputs[0])
        tree.links.new(BackRL.outputs[0], BackFile.inputs[0])

        tree.links.new(FrontRL.outputs[0], RenderZ.inputs[0])
        tree.links.new(FrontRL.outputs[2], RenderZ.inputs[1])
        tree.links.new(BackRL.outputs[0], RenderZ.inputs[2])
        tree.links.new(BackRL.outputs[2], RenderZ.inputs[3])

        tree.links.new(RenderZ.outputs[0], Composite.inputs[0])
        tree.links.new(RenderZ.outputs[1], Composite.inputs[2])

        return {'FINISHED'}


def register():
    bpy.utils.register_class(AutoSplit)


def unregister():
    bpy.utils.unregister_class(AutoSplit)

if __name__ == "__main__":
    register()
