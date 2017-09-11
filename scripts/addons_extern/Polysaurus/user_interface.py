import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
from bpy.types import Menu, Panel, AddonPreferences, PropertyGroup, UIList
from rna_prop_ui import PropertyPanel

class PS_UL_VertexGroups(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

            layout.prop(item, "name", icon="GROUP_VERTEX", text="", emboss=False)

class PS_Collection(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "sculpt_mode"
    bl_label = "Collection"
    bl_category = "Layers"

    def draw(self, context):
        layout = self.layout

        ob = context.object
        group = ob.vertex_groups.active

        vg = layout.column(align=True)
        vg.label("Vertex Groups")

        vg_list = vg.column(align=True)
        vg_list_box = vg_list.row(align=True)
        vg_list_box.template_list("PS_UL_VertexGroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=3)

        vg_list_options = vg_list_box.column(align=True)
        vg_list_options.operator("object.vertex_group_add", icon='ZOOMIN', text="")
        vg_list_options.operator("object.vertex_group_remove", icon='ZOOMOUT', text="").all = False
        if group:
            vg_list_options.separator()
            vg_list_options.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
            vg_list_options.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'
        vg_list.separator()
        vg_list.separator()

        vg_groups = vg.column(align=True)
        vg_groups.label("Vertex Group Tools", icon="GROUP_VERTEX")
        vg_groups.separator()
        vg_groups.operator("mesh.vgrouptomask", icon='FORWARD', text="Replace Mask with Group")#.index = -1
        vg_groups_bool = vg_groups.row(align=True)
        vg_groups_bool.operator("mesh.vgrouptomask_append", icon='ZOOMIN', text="Add")
        vg_groups_bool.operator("mesh.vgrouptomask_remove", icon='ZOOMOUT', text="Subtract")
        vg_groups.separator()
        vg_groups.separator()

        vg_mask = vg.column(align=True)
        vg_mask.label("Mask Tools", icon='MOD_MASK')
        vg_mask.separator()
        vg_mask.operator("mesh.masktovgroup", icon='ZOOMIN', text="Create New Group")
        vg_mask.operator("mesh.masktovgroup", icon='BACK', text="Replace Selected Group").new_group = False
        vg_mask.separator()
        vg_mask.separator()

#class PS_Tools(Panel):
    #bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOLS"
    #bl_context = "sculpt_mode"
    #bl_label = "Tools"
    #bl_category = "Polysaurus"

    #def draw(self, context):
        #layout = self.layout

        #ob = context.object
        #group = ob.vertex_groups.active

        #vg = layout.column(align=True)
        #vg.label("Vertex Groups")
