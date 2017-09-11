import bpy
import mathutils
from bpy.types import Operator
from bpy.props import *



def get_prefs(context):
    return context.user_preferences.addons[__package__].preferences


class Options():
    pass


class add_mesh_tree(Operator):
    """"""
    bl_idname = "mesh.tree_add"
    bl_label = "Add Tree"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    bl_description = "adds low poly tree"

    def draw(self, context):
        prefs = get_prefs(context)
        layout = self.layout
        layout.prop(prefs, 'lp_Tree_Type')
        layout.prop(prefs, 'lp_Tree_Setting')
        if prefs.lp_Tree_Setting == 'lp_Tree_Trunk':
            box = layout.box()
            if prefs.lp_Tree_Type == 'lp_Tree_Palm':
                box.label("Segments")
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Segments_Min')
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Segments_Max')
                box.label("Stages")
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Stages_Min')
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Stages_Max')
                box.label("Stage Length")
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Stage_Length_Min')
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Stage_Length_Max')
                box.label("Stage Diameter")
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Diameter1_Min')
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Diameter1_Max')
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Diameter2_Min')
                box.prop(prefs, 'lp_Tree_Palm_Trunk_Diameter2_Max')
            else:
                box.label("Segments")
                box.prop(prefs, 'lp_Tree_Trunk_Segments_Min')
                box.prop(prefs, 'lp_Tree_Trunk_Segments_Max')
                box.label("Length")
                box.prop(prefs, 'lp_Tree_Trunk_Length_Min')
                box.prop(prefs, 'lp_Tree_Trunk_Length_Max')
                box.label("Diameter")
                box.prop(prefs, 'lp_Tree_Trunk_Diameter1_Min')
                box.prop(prefs, 'lp_Tree_Trunk_Diameter1_Max')
                box.prop(prefs, 'lp_Tree_Trunk_Diameter2_Min')
                box.prop(prefs, 'lp_Tree_Trunk_Diameter2_Max')

        if prefs.lp_Tree_Setting == 'lp_Tree_Top':
            box = layout.box()
            if prefs.lp_Tree_Type == 'lp_Tree_Oak':
                box.prop(prefs, 'lp_Tree_Top_Subdivisions')
                box.label("Scale Min")
                box.prop(prefs, 'lp_Tree_Top_Scale_Min')
                box.label("Scale Max")
                box.prop(prefs, 'lp_Tree_Top_Scale_Max')

                box.label("Dispalce Strength")
                box.prop(prefs, 'lp_Tree_Top_Strength_Min')
                box.prop(prefs, 'lp_Tree_Top_Strength_Max')

                box.label("Dispalce Scale")
                box.prop(prefs, 'lp_Tree_Top_NScale_Min')
                box.prop(prefs, 'lp_Tree_Top_NScale_Max')

                box.label("Dispalce Weights")
                box.prop(prefs, 'lp_Tree_Top_Weight1')
                box.prop(prefs, 'lp_Tree_Top_Weight2')
                box.prop(prefs, 'lp_Tree_Top_Weight3')
            elif prefs.lp_Tree_Type == 'lp_Tree_Pine':
                box.label("Stages")
                box.prop(prefs, 'lp_Tree_Top_Stages_Min')
                box.prop(prefs, 'lp_Tree_Top_Stages_Max')
                box.label("Stage Size Min")
                box.prop(prefs, 'lp_Tree_Top_Stage_Size_Min')
                box.label("Stage Size Max")
                box.prop(prefs, 'lp_Tree_Top_Stage_Size_Max')
                # box.prop(prefs, 'lp_Tree_Top_Stage_Diameter')
                box.prop(prefs, 'lp_Tree_Top_Stage_Shrink')
                box.prop(prefs, 'lp_Tree_Top_Stage_Shrink_Multiplier')
                box.label("Stage Step")
                box.prop(prefs, 'lp_Tree_Top_Stage_Step_Min')
                box.prop(prefs, 'lp_Tree_Top_Stage_Step_Max')
                box.label("Stage Segments")
                box.prop(prefs, 'lp_Tree_Top_Stage_Segments_Min')
                box.prop(prefs, 'lp_Tree_Top_Stage_Segments_Max')
                box.prop(prefs, 'lp_Tree_Top_Rotate_Stages')
            elif prefs.lp_Tree_Type == 'lp_Tree_Palm':
                box.label("Leaves")
                box.prop(prefs, 'lp_Tree_Palm_Top_Leaves_Min')
                box.prop(prefs, 'lp_Tree_Palm_Top_Leaves_Max')
                box.label("Leaf Length")
                box.prop(prefs, 'lp_Tree_Palm_Top_Leaf_Length_Min')
                box.prop(prefs, 'lp_Tree_Palm_Top_Leaf_Length_Max')
                box.label("Leaf Size")
                box.prop(prefs, 'lp_Tree_Palm_Top_Leaf_Size_Min')
                box.prop(prefs, 'lp_Tree_Palm_Top_Leaf_Size_Max')
                box.label("Coconuts")
                box.prop(prefs, 'lp_Tree_Palm_Top_Coconuts_Min')
                box.prop(prefs, 'lp_Tree_Palm_Top_Coconuts_Max')

        layout.label("")
        layout.prop(prefs, 'lp_Tree_Keep_Modifiers')

    @classmethod
    def poll(cls, context):
        return (context.scene is not None)

    def get_options(context):
        return get_prefs(context)

    def execute(self, context):
        create_tree_object(self, context, add_mesh_tree.get_options(context))
        return {'FINISHED'}

    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}
