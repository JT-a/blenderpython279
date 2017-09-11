bl_info = {
    "name": "Alpha Mesher",
    "description": "Tools to help with producing Alpha Quality Meshes for Games. Helps with High Poly creation, Low Poly Creation and export and baking processes. Designed with Substance Designer in Mind",
    "author": "Alex Downham - Defaultsound",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "location": "View3D > Tools > Alpha Mesher",
    "warning": "Proof of Concept, Pontentially Buggy",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "Mesh"}

import bpy
import bmesh
import random


class AlphaMesherPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Alpha Mesher"
    bl_label = "Alpha Mesher"

    def draw(self, context):
        layout = self.layout.column(align=True)

        row = layout.row()
        row.label(text="Hard Surface Tools")

        split = layout.split()
        col = layout.column(align=True)

        col.operator("mesh.easy_edges", text="High Poly/Remeshing")
        col.operator("mesh.easy_edges_add", text="Apply High Poly/Remeshing")
        col.operator("mesh.cleanup", text="Clean Up Meshes")
        col.operator("mesh.colourid", text="Apply Colour ID")
        # col.operator("mesh.dirty_edges", text="Dirty Edges (WIP)")

        col.separator()
        col.label(text="Low Poly Tools")
        col.operator("mesh.lowpolymaker", text="Make Low Poly")
        col.operator("mesh.quickunwrap", text="Quick Unwrap")
        col.operator("mesh.cagemaker", text="Make Cage")
        col.operator("mesh.marksharp", text="Mark Split Edges")

        col.separator()
        col.label(text="Naming Tools")
        col.operator("mesh.autoname", text="Quick Rename Parts")


class EasyEdges(bpy.types.Operator):
    bl_idname = "mesh.easy_edges"
    bl_label = "Easy Edges"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        objname = bpy.context.object.name
        scene = bpy.context.scene
        bpy.ops.object.duplicate_move()
        bpy.context.object.name = objname + "_Shrink"
        bpy.ops.object.duplicate_move()
        bpy.context.object.name = objname + "_HP"
        for ob in scene.objects:
            if ob.type == 'MESH' and ob.name.startswith(objname + "_HP"):
                ob.select = True
            else:
                ob.select = False
        bpy.ops.object.modifier_add(type='REMESH')
        bpy.context.object.modifiers["Remesh"].mode = 'BLOCKS'
        bpy.context.object.modifiers["Remesh"].octree_depth = 5
        bpy.context.object.modifiers["Remesh"].use_smooth_shade = True
        bpy.ops.object.modifier_add(type='SHRINKWRAP')
        bpy.context.object.modifiers["Shrinkwrap"].target = (bpy.data.objects[objname + "_Shrink"])
        bpy.context.object.modifiers["Shrinkwrap"].wrap_method = 'PROJECT'
        bpy.context.object.modifiers["Shrinkwrap"].use_negative_direction = True
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers["Subsurf"].levels = 2

        return {"FINISHED"}


class EasyEdgesAdd(bpy.types.Operator):
    bl_idname = "mesh.easy_edges_add"
    bl_label = "Easy Edges"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Remesh")
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].decimate_type = 'UNSUBDIV'
        bpy.context.object.modifiers["Decimate"].iterations = 4
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")

        return {"FINISHED"}


class CleanUp(bpy.types.Operator):
    bl_idname = "mesh.cleanup"
    bl_label = "Clean Up"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        scene = bpy.context.scene
        for ob in scene.objects:
            if ob.type == 'MESH' and ob.name.endswith("_Shrink"):
                ob.select = True
            else:
                ob.select = False
        bpy.ops.object.delete()
        return {"FINISHED"}


class ColourID(bpy.types.Operator):
    bl_idname = "mesh.colourid"
    bl_label = "Colour ID"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):

        r = random.random()
        g = random.random()
        b = random.random()

        object = bpy.context.scene.objects.active

        idnum = 0

        if not object.material_slots.values():
            name = object.name + "_ID" + str(idnum + 1)
            material = bpy.data.materials.new(name)
            material.use_shadeless = True
            object.data.materials.append(material)
        else:
            material = object.material_slots[0].material

        material.diffuse_color = (r, g, b)
        return {"FINISHED"}


class LowPolyMaker(bpy.types.Operator):
    bl_idname = "mesh.lowpolymaker"
    bl_label = "Lowpoly Maker"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.object.duplicate_move()
        bpy.context.object.name = bpy.context.object.name.replace("_HP.001", "_LP")
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = 0.006
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")
        bpy.ops.object.editmode_toggle()
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        for face in bm.faces:
            if face.select == False:
                face.select = True
            elif face.select == True:
                face.select = True
                continue
        bpy.ops.uv.smart_project(island_margin=0.005)
        bpy.ops.uv.seams_from_islands()
        bpy.context.tool_settings.mesh_select_mode = (False, True, False)
        bpy.ops.mesh.select_all()
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        for edge in bm.edges:
            if edge.seam == 1:
                edge.select = True
                continue
        bpy.ops.mesh.mark_sharp()
        bpy.ops.mesh.mark_seam(clear=True)
        bpy.ops.object.editmode_toggle()

        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].use_edge_angle = False

        return {"FINISHED"}


class QuickUnwrap(bpy.types.Operator):
    bl_idname = "mesh.quickunwrap"
    bl_label = "Quick Unwrap"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.object.editmode_toggle()
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        for face in bm.faces:
            if face.select == False:
                face.select = True
            elif face.select == True:
                face.select = True
                continue
        bpy.ops.uv.smart_project(island_margin=0.005)
        bpy.ops.uv.seams_from_islands()
        bpy.context.tool_settings.mesh_select_mode = (False, True, False)
        bpy.ops.mesh.select_all()
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        for edge in bm.edges:
            if edge.seam == 1:
                edge.select = True
                continue
        bpy.ops.mesh.mark_sharp()
        bpy.ops.mesh.mark_seam(clear=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].use_edge_angle = False

        return {"FINISHED"}


class MarkSharp(bpy.types.Operator):
    bl_idname = "mesh.marksharp"
    bl_label = "Quick Unwrap"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.object.editmode_toggle()
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        for face in bm.faces:
            if face.select == False:
                face.select = True
            elif face.select == True:
                face.select = True
                continue
        bpy.ops.uv.seams_from_islands()
        bpy.context.tool_settings.mesh_select_mode = (False, True, False)
        bpy.ops.mesh.select_all()
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        for edge in bm.edges:
            if edge.seam == 1:
                edge.select = True
                continue
        bpy.ops.mesh.mark_sharp()
        bpy.ops.mesh.mark_seam(clear=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].use_edge_angle = False
        return {"FINISHED"}


class CageMaker(bpy.types.Operator):
    bl_idname = "mesh.cagemaker"
    bl_label = "Cage Maker"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.object.duplicate_move()
        bpy.context.object.name = bpy.context.object.name.replace("_LP.001", "_Cage")
        bpy.ops.object.modifier_remove(modifier="EdgeSplit")
        bpy.ops.object.modifier_add(type='DISPLACE')
        bpy.context.object.modifiers["Displace"].strength = 0.02
        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].use_edge_angle = False
        return {"FINISHED"}


class AutoNamer(bpy.types.Operator):
    bl_idname = "mesh.autoname"
    bl_label = "Auto Namer"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        partname = "Part"

        # bpy.ops.object.select_all()
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH' and obj.name != "Part_":
                obj.name = partname

        return {"FINISHED"}


class DirtyEdges(bpy.types.Operator):
    bl_idname = "mesh.dirty_edges"
    bl_label = "Dirty Edges"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        bpy.ops.paint.vertex_color_dirt(dirt_only=True)
        bpy.ops.paint.vertex_color_dirt(dirt_only=True)
        bpy.ops.paint.vertex_color_dirt()
        bpy.ops.paint.vertex_color_dirt()
        bpy.ops.object.vertex_colors_to_vertex_groups()
        dTex = bpy.data.textures.new(name='DisplaceTex', type='CLOUDS')
        dTex.noise_type = 'HARD_NOISE'
        dTex.noise_scale = 0.10
        dTex.noise_depth = 0
        dTex.noise_basis = 'VORONOI_F2'
        bpy.ops.object.modifier_add(type='DISPLACE')
        bpy.context.object.modifiers["Displace"].strength = 0.04
        bpy.context.object.modifiers["Displace"].texture = bpy.data.textures['DisplaceTex']
        bpy.context.object.modifiers["Displace"].vertex_group = "Col_value"
        return {"FINISHED"}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
