bl_info = {
    "name": "Modifiers Pie menu",
    "author": "TARDIS Maker",
    "version": (0, 0, 0),
    "blender": (2, 72, 2),
    "description": "A pie menu for adding modifiers to objects.",
    "location": "Hotkey: SHIFT + M",
    "category": "Pie Menu",}


import bpy
from bpy.types import Menu

##################
# Modify Submenu #
##################
class AddModifier_Modify(Menu):
    bl_idname = "modifier.modify"
    bl_label = "Add Modify Modifier"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("object.modifier_add", text="Mesh Cache", icon='MOD_MESHDEFORM').type='MESH_CACHE'
        pie.operator("object.modifier_add", text="UV Project", icon='MOD_UVPROJECT').type='UV_PROJECT'
        pie.operator("object.modifier_add", text="UV Warp", icon='MOD_UVPROJECT').type='UV_WARP'
        pie.operator("object.modifier_add", text="Vertex Weight Edit", icon='MOD_VERTEX_WEIGHT').type='VERTEX_WEIGHT_EDIT'
        pie.operator("object.modifier_add", text="Vertex Weight Mix", icon='MOD_VERTEX_WEIGHT').type='VERTEX_WEIGHT_MIX'
        pie.operator("object.modifier_add", text="Vertex Weight Proximity", icon='MOD_VERTEX_WEIGHT').type='VERTEX_WEIGHT_PROXIMITY'


####################
# Generate Submenu #
####################
class AddModifier_Generate(Menu):
	bl_idname = "modifier.generate"
	bl_label = "Add Generate Modifier"

	def draw(self, context):
		layout = self.layout

		pie = layout.menu_pie()
		pie.operator("object.modifier_add", text="SubSurf", icon='MOD_SUBSURF').type='SUBSURF'
		pie.operator("object.modifier_add", text="Mirror", icon='MOD_MIRROR').type='MIRROR'
		pie.operator("object.modifier_add", text="Array", icon='MOD_ARRAY').type='ARRAY'
		pie.operator("object.modifier_add", text="Solidify", icon='MOD_SOLIDIFY').type='SOLIDIFY'
		
		### INLINE PANEL ###
		box = pie.split().box().column()
		col = box.column(align=True)
		col.operator("object.modifier_add", text="Bevel", icon='MOD_BEVEL').type='BEVEL'
		col.operator("object.modifier_add", text="Boolean", icon='MOD_BOOLEAN').type='BOOLEAN'
		col.operator("object.modifier_add", text="Build", icon='MOD_BUILD').type='BUILD'
		
		### INLINE PANEL ###
		box = pie.split().box().column()
		col = box.column(align=True)
		col.operator("object.modifier_add", text="Decimate", icon='MOD_DECIM').type='DECIMATE'
		col.operator("object.modifier_add", text="Edge Split", icon='MOD_EDGESPLIT').type='EDGE_SPLIT'
		col.operator("object.modifier_add", text="Mask", icon='MOD_MASK').type='MASK'
		
		### INLINE PANEL ###
		box = pie.split().box().column()
		col = box.column(align=True)
		col.operator("object.modifier_add", text="Multiresolution", icon='MOD_MULTIRES').type='MULTIRES'
		col.operator("object.modifier_add", text="Remesh", icon='MOD_REMESH').type='REMESH'
		col.operator("object.modifier_add", text="Screw", icon='MOD_SCREW').type='SCREW'
		
		### INLINE PANEL ###
		box = pie.split().box().column()
		col = box.column(align=True)
		col.operator("object.modifier_add", text="Skin", icon='MOD_SKIN').type='SKIN'
		col.operator("object.modifier_add", text="Triangulate", icon='MOD_TRIANGULATE').type='TRIANGULATE'
		col.operator("object.modifier_add", text="Wireframe", icon='MOD_WIREFRAME').type='WIREFRAME'


##################
# Deform Submenu #
##################
class AddModifier_Deform(Menu):
	bl_idname = "modifier.deform"
	bl_label = "Add Deform Modifier"

	def draw(self, context):
		layout = self.layout

		pie = layout.menu_pie()
		pie.operator("object.modifier_add", text="Armature", icon='MOD_ARMATURE').type='ARMATURE'
		pie.operator("object.modifier_add", text="Curve", icon='MOD_CURVE').type='CURVE'
		pie.operator("object.modifier_add", text="Displace", icon='MOD_DISPLACE').type='DISPLACE'
		pie.operator("object.modifier_add", text="Shrinkwrap", icon='MOD_SHRINKWRAP').type='SHRINKWRAP'
		pie.operator("object.modifier_add", text="Hook", icon='HOOK').type='HOOK'
		pie.operator("object.modifier_add", text="Lattice", icon='MOD_LATTICE').type='LATTICE'
		
		### INLINE PANEL ###
		box = pie.split().box().column()
		col = box.column(align=True)
		col.operator("object.modifier_add", text="Cast", icon='MOD_CAST').type='CAST'
		col.operator("object.modifier_add", text="Laplacian Smooth", icon='MOD_SMOOTH').type='LAPLACIANSMOOTH'
		col.operator("object.modifier_add", text="Laplacian Deform", icon='MOD_MESHDEFORM').type='LAPLACIANDEFORM'
		col.operator("object.modifier_add", text="Mesh Deform", icon='MOD_MESHDEFORM').type='MESH_DEFORM'
		
		### INLINE PANEL ###
		box = pie.split().box().column()
		col = box.column(align=True)
		col.operator("object.modifier_add", text="Simple Deform", icon='MOD_SIMPLEDEFORM').type='SIMPLE_DEFORM'
		col.operator("object.modifier_add", text="Smooth", icon='MOD_SMOOTH').type='SMOOTH'
		col.operator("object.modifier_add", text="Warp", icon='MOD_WARP').type='WARP'
		col.operator("object.modifier_add", text="Wave", icon='MOD_WAVE').type='WAVE'




##################
# Pie Menu Class #
##################
class AddModifier(Menu):
    bl_idname = "modifier.add"
    bl_label = "Add Modifier"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("wm.call_menu_pie", text="Modify", icon='PLUS').name="modifier.modify"
        pie.operator("wm.call_menu_pie", text="Generate", icon='PLUS').name="modifier.generate"
        pie.operator("wm.call_menu_pie", text="Deform", icon='PLUS').name="modifier.deform"
        pie.operator("object.modifier_add", text="SubSurf", icon='MOD_SUBSURF').type='SUBSURF'
        pie.operator("object.modifier_add", text="Mirror", icon='MOD_MIRROR').type='MIRROR'
        pie.operator("object.modifier_add", text="Array", icon='MOD_ARRAY').type='ARRAY'
        pie.operator("object.modifier_add", text="Solidify", icon='MOD_SOLIDIFY').type='SOLIDIFY'
        pie.operator("object.modifier_add", text="Ocean", icon='MOD_OCEAN').type='OCEAN'



############
# Register #
############
addon_keymaps = []
def register():
	bpy.utils.register_class(AddModifier)
	bpy.utils.register_class(AddModifier_Modify)
	bpy.utils.register_class(AddModifier_Generate)
	bpy.utils.register_class(AddModifier_Deform)

	### Keymap ###
	wm = bpy.context.window_manager

	km = wm.keyconfigs.addon.keymaps.new(name="Screen")
	kmi = km.keymap_items.new("wm.call_menu_pie", "M", "PRESS", shift=True)
	kmi.properties.name="modifier.add"
	addon_keymaps.append(km)


##############
# Unregister #
##############
def unregister():
	bpy.utils.unregister_class(AddModifier)
	bpy.utils.unregister_class(AddModifier_Modify)
	bpy.utils.unregister_class(AddModifier_Generate)
	bpy.utils.unregister_class(AddModifier_Deform)

	### Keymap ###
	for km in addon_keymaps:
		for kmi in km.keymap_items:
			km.keymap_items.remove(kmi)

	wm.keyconfigs.addon.keymaps.remove(km)

	# clear the list
	del addon_keymaps[:]


if __name__ == "__main__":
    register()

    #bpy.ops.wm.call_menu_pie(name="modifier.add")
