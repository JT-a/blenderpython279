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
	"name": "3DM Morph",
	"category": "Object",
	"author": "3DMish (Mish7913@gmail.com)",
	"version": (0, 1, 5),
	"blender": (2, 78, 0),
	"wiki_url": "",
	"tracker_url": "",
	"description": "Morphing image",
	}
	
import bpy
import bmesh
from bpy.props import *

class MishMorph(bpy.types.Panel):   
	bl_category 	= "3DMish"
	bl_label		= "3DM Morph"
	bl_space_type   = "VIEW_3D"
	bl_region_type  = "TOOLS"
	
	def draw(self, context):
		Tcol = self.layout.column(align=True)
		if bpy.data.objects.get("3DMish_Morph") == None:
			Xcol = Tcol.row(align=True)
			Xcol.prop(context.scene, 'MishMorphX')
			Xcol.prop(context.scene, 'MishMorphY')
			Ico1 = Tcol.row(align=True)
			Ico1.prop(context.scene, 'MishMorphImage1', icon="IMAGE_DATA")
			Ico1.operator("3dmish.morph_clear1", icon="X")
			Ico2 = Tcol.row(align=True)
			Ico2.prop(context.scene, 'MishMorphImage2', icon="IMAGE_DATA")
			Ico2.operator("3dmish.morph_clear2", icon="X")
			Tcol.operator("3dmish.morph_start", icon="NEW")
		else:
			Tcol.operator("3dmish.morph_cancel", icon="X")
			Rcol = Tcol.row(align=True)
			Rcol.operator("3dmish.add_points", icon="SPACE3")
			Rcol.operator("3dmish.delete_point")
			Tcol.prop(context.scene, "MishMorphQuality", text="Quality")
			Tcol.operator("3dmish.morph_generate", icon="IMAGE_COL")

class MishMorphGenerate(bpy.types.Operator):
	bl_idname   	= '3dmish.morph_generate'
	bl_label		= 'Generate'
	bl_description  = 'Generate morph'
	
	def execute(self, context):
		bpy.ops.object.select_all(action='DESELECT'); Xre = -1; Yre = 1;
		for i in range(21):
			Pn1, Pn2 = MishMorphAddPoint();
			Pn1.location = (Xre, 1, 0); Pn2.location = (Xre, 1, 0);
			Xre += 0.1;
		Xre = -1;
		for i in range(21):
			Pn1, Pn2 = MishMorphAddPoint();
			Pn1.location = (Xre, -1, 0); Pn2.location = (Xre, -1, 0);
			Xre += 0.1;
		for i in range(21):
			Pn1, Pn2 = MishMorphAddPoint();
			Pn1.location = (1, Yre, 0); Pn2.location = (1, Yre, 0);
			Yre -= 0.1;
		Yre = 1;
		for i in range(21):
			Pn1, Pn2 = MishMorphAddPoint();
			Pn1.location = (-1, Yre, 0); Pn2.location = (-1, Yre, 0);
			Yre -= 0.1;
		bpy.ops.object.select_all(action='DESELECT'); 
		bpy.data.objects["MishMorphImg_1"].hide_select = False; bpy.data.objects["MishMorphImg_2"].hide_select = False;
		
		bpy.data.objects["MishMorphImg_1"].select = True; bpy.context.scene.objects.active = bpy.data.objects["MishMorphImg_1"];
		bpy.ops.object.modifier_add(type='SUBSURF');	  bpy.context.object.modifiers["Subsurf"].subdivision_type = 'SIMPLE';
		bpy.context.object.modifiers["Subsurf"].levels = (bpy.context.scene.MishMorphQuality);
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf");
		
		bpy.data.objects["MishMorphImg_2"].select = True;  bpy.context.scene.objects.active = bpy.data.objects["MishMorphImg_2"];
		bpy.ops.object.modifier_add(type='SUBSURF');	   bpy.context.object.modifiers["Subsurf"].subdivision_type = 'SIMPLE';
		bpy.context.object.modifiers["Subsurf"].levels = (bpy.context.scene.MishMorphQuality);
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf");
		
		LocCur = bpy.context.scene.cursor_location; bpy.ops.view3d.snap_cursor_to_center();
		bpy.ops.object.select_all(action='DESELECT'); NumB = 0;
		bpy.ops.object.armature_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0))
		bpy.context.scene.objects.active.name ="MishMorphArmat";
		bpy.context.scene.objects.active.parent = bpy.data.objects['3DMish_Morph'];
		for child in bpy.data.objects['MishMorphImg_1'].children:
			bpy.ops.object.mode_set(mode='EDIT');
			Xm1, Ym1, Zm1 = bpy.data.objects['MishMorphImg_1'].location;  Xd1, Yd1, Zd1 = bpy.data.objects['MishMorphImg_1'].dimensions;
			Xm2, Ym2, Zm2 = bpy.data.objects['MishMorphImg_2'].location;  Xd2, Yd2, Zd2 = bpy.data.objects['MishMorphImg_2'].dimensions;
			X1, Y1, Z1 = bpy.data.objects[child.name].location;  X2, Y2, Z2 = bpy.data.objects[child.name.replace("_L", "_R")].location;
			NumB += 1;
			bpy.ops.armature.bone_primitive_add(name='Bone.L'); bpy.ops.armature.select_more();
			bpy.ops.transform.translate(value=((X1*(Xd1/2))+Xm1, (Y1*(Yd1/2))+Ym1, 0));
			bpy.ops.object.mode_set(mode='POSE');
			bpy.ops.transform.translate(value=BoMeDD(((X2*(Xd2/2))+Xm2, (Y2*(Yd2/2))+Ym2, 0), ((X1*(Xd1/2))+Xm1, (Y1*(Yd1/2))+Ym1, 0)))
			bpy.ops.transform.translate(value=(-bpy.context.scene.MishMorphX-1, 0, 0))
			bpy.ops.object.mode_set(mode='EDIT');
			bpy.ops.armature.bone_primitive_add(name='Bone.R'); bpy.ops.armature.select_more();
			bpy.ops.transform.translate(value=((X2*(Xd2/2))+Xm2, (Y2*(Yd2/2))+Ym2, 0));
			bpy.ops.object.mode_set(mode='POSE');
			bpy.ops.transform.translate(value=BoMeDD(((X1*(Xd1/2))+Xm1, (Y1*(Yd1/2))+Ym1, 0), ((X2*(Xd2/2))+Xm2, (Y2*(Yd2/2))+Ym2, 0)))
			bpy.ops.transform.translate(value=(bpy.context.scene.MishMorphX+1, 0, 0))
		bpy.context.scene.cursor_location = LocCur;
		
		bpy.ops.object.mode_set(mode='OBJECT'); 		  bpy.ops.object.select_all(action='DESELECT');
		bpy.data.objects['MishMorphImg_1'].select = True; bpy.data.objects['MishMorphImg_2'].select = True;
		bpy.data.objects['MishMorphArmat'].select = True; bpy.ops.object.parent_set(type='ARMATURE_AUTO');
		bpy.context.space_data.show_relationship_lines = True;
		bpy.ops.object.select_all(action='DESELECT');
		bpy.data.objects["MishMorphImg_1"].select = True; bpy.context.scene.objects.active = bpy.data.objects["MishMorphImg_1"];
		bpy.ops.object.modifier_apply(apply_as='SHAPE', modifier="Armature"); bpy.ops.object.vertex_group_remove(all=True);
		bpy.data.objects["MishMorphImg_1"].location = 0, 0, 0; bpy.data.objects["MishMorphImg_1"].active_shape_key_index = 1;
		bpy.context.object.data.shape_keys.key_blocks["Armature"].name = 'Anim1';
		bpy.data.objects["MishMorphImg_2"].select = True; bpy.context.scene.objects.active = bpy.data.objects["MishMorphImg_2"];
		bpy.ops.object.modifier_apply(apply_as='SHAPE', modifier="Armature"); bpy.ops.object.vertex_group_remove(all=True);
		bpy.data.objects["MishMorphImg_2"].location = 0, 0, -0.01; bpy.data.objects["MishMorphImg_2"].active_shape_key_index = 1;
		bpy.context.object.data.shape_keys.key_blocks["Armature"].name = 'Anim2';
		bpy.ops.object.select_all(action='DESELECT'); Names = set();
		def get_child_names(obj):
			for child in obj.children:
				Names.add(child.name);
		get_child_names(bpy.data.objects['MishMorphImg_1']);
		get_child_names(bpy.data.objects['MishMorphImg_2']);
		objects = bpy.data.objects; [setattr(objects[n], 'select', True) for n in Names];
		bpy.ops.object.delete();
		bpy.data.objects["MishMorphImg_1"].select = True; bpy.data.objects["MishMorphImg_2"].select = True;
		bpy.context.scene.objects.active = bpy.data.objects["MishMorphImg_1"]; bpy.ops.object.join();
		bpy.context.object.name = "MorphImage"; bpy.context.object.parent = None;
		obj = bpy.context.scene.objects.active;
		drv1 = obj.data.shape_keys.key_blocks['Anim1'].driver_add("value")
		drv2 = obj.data.shape_keys.key_blocks['Anim2'].driver_add("value")
		obj["_RNA_UI"] = {}; obj['Anim'] = 0.0;
		obj["_RNA_UI"]['Anim'] = {"min":0.0, "max":1.0, "soft_min":0.0, "soft_max":1.0, "description":"Try to drag me past my bounds!"}
		
		drv1.driver.type="AVERAGE"
		var = drv1.driver.variables.new()
		var.name='var'
		var.type='SINGLE_PROP'
		target = var.targets[0]
		target.id = bpy.data.objects[obj.name]
		target.data_path = '["Anim"]'
		
		drv2.driver.type="AVERAGE"
		var = drv2.driver.variables.new()
		var.name='var'
		var.type='SINGLE_PROP'
		target = var.targets[0]
		target.id = bpy.data.objects[obj.name]
		target.data_path = '["Anim"]'
		modg = drv2.modifiers[0]
		modg.coefficients[0] = 1.0
		modg.coefficients[1] = -1.0
		
		bpy.data.objects['3DMish_Morph'].hide = False;
		bpy.ops.object.select_all(action='DESELECT'); Names = set([bpy.data.objects['3DMish_Morph'].name]);
		def get_child_names(obj):
			for child in obj.children:
				Names.add(child.name);
				if child.children: get_child_names(child)
		get_child_names(bpy.data.objects['3DMish_Morph'])
		objects = bpy.data.objects; [setattr(objects[n], 'select', True) for n in Names]; bpy.ops.object.delete()
		bpy.context.scene.update(); bpy.context.area.tag_redraw()
		
		if (bpy.context.scene.render.engine == 'CYCLES'):
			ob = bpy.data.objects[obj.name];
			ob.active_material_index = 0
			for i in range(len(ob.material_slots)):
				bpy.ops.object.material_slot_remove({'object': ob})
			MaterialImg1 = MishMorphMaterialCycles('3DMish_Morph_Tex', bpy.context.scene.MishMorphImage1, bpy.context.scene.MishMorphImage2)
			MishMorphSetMaterial(obj, MaterialImg1);

			nodes = MaterialImg1.node_tree.nodes
			mx = nodes.get("Mix")
			drvo = mx.inputs[0].driver_add("default_value")
			drvo.driver.type="AVERAGE"
			var = drvo.driver.variables.new()
			var.name='var'
			var.type='SINGLE_PROP'
			target = var.targets[0]
			target.id = bpy.data.objects[obj.name]
			target.data_path = '["Anim"]'
		elif (bpy.context.scene.render.engine == 'BLENDER_RENDER'):
			ob = bpy.data.objects[obj.name];
			ob.active_material_index = 0
			ob.active_material.use_transparency = True
			drvo = ob.active_material.driver_add("alpha")
			drvo.driver.type="AVERAGE"
			var = drvo.driver.variables.new()
			var.name='var'
			var.type='SINGLE_PROP'
			target = var.targets[0]
			target.id = bpy.data.objects[obj.name]
			target.data_path = '["Anim"]'
			modg = drvo.modifiers[0]
			modg.coefficients[0] = 1.0
			modg.coefficients[1] = -1.0

		return {'FINISHED'}

class MishMorphStart(bpy.types.Operator):
	bl_idname   	= '3dmish.morph_start'
	bl_label		= 'New morph'
	bl_description  = 'Create new morph'
			
	def execute(self, context):
		bpy.context.space_data.show_relationship_lines = False;
		EmSt = bpy.data.objects.new("3DMish_Morph", None); scene = bpy.context.scene;  scene.objects.link(EmSt);
		scene.update();  EmSt.empty_draw_type = 'SPHERE';  EmSt.empty_draw_size = 0.5; EmSt.hide = True;
		
		MishMorphImg_1 = MishMorphCreatePolyPlane("MishMorphImg_1"); MishMorphImg_o1 = MishMorphImg_1;
		MishMorphImg_1.dimensions = (bpy.context.scene.MishMorphX,   bpy.context.scene.MishMorphY, 0);
		MishMorphImg_1.location = (-(bpy.context.scene.MishMorphX/2)-0.5, 0, 0); GenX = bpy.context.scene.MishMorphX;
		bpy.ops.object.select_all(action='DESELECT'); MishMorphImg_1.select; bpy.ops.mesh.uv_texture_add();
		MishMorphImg_1.hide_select = True;
		MishMorphImg_2 = MishMorphCreatePolyPlane("MishMorphImg_2"); MishMorphImg_o2 = MishMorphImg_2;
		MishMorphImg_2.dimensions = (bpy.context.scene.MishMorphX,   bpy.context.scene.MishMorphY, 0);
		MishMorphImg_2.location = ( (bpy.context.scene.MishMorphX/2)+0.5, 0, 0); GenY = bpy.context.scene.MishMorphY;
		bpy.ops.object.select_all(action='DESELECT'); MishMorphImg_2.select; bpy.ops.mesh.uv_texture_add();
		MishMorphImg_2.hide_select = True;
		
		bpy.ops.object.select_all(action='DESELECT');
		MishMorphImg_1.parent = EmSt;
		MishMorphImg_2.parent = EmSt;
		
		if (bpy.context.scene.render.engine == 'CYCLES'):
			if not bpy.context.scene.MishMorphImage1 == '':
				MaterialImg1 = MishMorphMakeMaterialCycles('MishMorphMaterialImage1', bpy.context.scene.MishMorphImage1)
				MishMorphSetMaterial(MishMorphImg_1, MaterialImg1);
			if not bpy.context.scene.MishMorphImage2 == '':
				MaterialImg2 = MishMorphMakeMaterialCycles('MishMorphMaterialImage2', bpy.context.scene.MishMorphImage2)
				MishMorphSetMaterial(MishMorphImg_2, MaterialImg2);
		elif (bpy.context.scene.render.engine == 'BLENDER_RENDER'):
			if not bpy.context.scene.MishMorphImage1 == '':
				MaterialImg1 = MishMorphMakeMaterial('MishMorphMaterialImage1', (1, 1, 1), (1, 1, 1), 1);
				MishMorphSetMaterial(MishMorphImg_1, MaterialImg1);
				MishMorphTexture1 = bpy.data.textures.new('MishMorphTextureImage1', type = 'IMAGE');
				MishMorphTexture1.image = bpy.data.images.load(bpy.context.scene.MishMorphImage1);
				MaterialImg1.texture_slots.add().texture = MishMorphTexture1;
			if not bpy.context.scene.MishMorphImage2 == '':
				MaterialImg2 = MishMorphMakeMaterial('MishMorphMaterialImage2', (1, 1, 1), (1, 1, 1), 1);
				MishMorphSetMaterial(MishMorphImg_2, MaterialImg2);
				MishMorphTexture2 = bpy.data.textures.new('MishMorphTextureImage2', type = 'IMAGE');
				MishMorphTexture2.image = bpy.data.images.load(bpy.context.scene.MishMorphImage2);
				MaterialImg2.texture_slots.add().texture = MishMorphTexture2;
		return {'FINISHED'}

class MishMorphCancel(bpy.types.Operator):
	bl_idname   	= '3dmish.morph_cancel'
	bl_label		= 'Cancel'
	bl_description  = 'Cancel morph'
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT');
		bpy.data.objects['3DMish_Morph'].hide = False;
		if bpy.data.objects.get("MishMorphImg_1") is not None: bpy.data.objects['MishMorphImg_1'].hide_select = False;
		if bpy.data.objects.get("MishMorphImg_2") is not None: bpy.data.objects['MishMorphImg_2'].hide_select = False;
		bpy.ops.object.select_all(action='DESELECT'); Names = set([bpy.data.objects['3DMish_Morph'].name]);
		def get_child_names(obj):
			for child in obj.children:
				Names.add(child.name);
				if child.children: get_child_names(child)
		get_child_names(bpy.data.objects['3DMish_Morph'])
		objects = bpy.data.objects; [setattr(objects[n], 'select', True) for n in Names]; bpy.ops.object.delete()
		return {'FINISHED'}
		
class MishMorphAddPoints(bpy.types.Operator):
	bl_idname   	= '3dmish.add_points'
	bl_label		= 'Add Point'
	bl_description  = 'Add Point'
	
	def execute(self, context):
		MishMorphAddPoint();
		return {'FINISHED'}

class MishMorphDeletePoint(bpy.types.Operator):
	bl_idname   	= '3dmish.delete_point'
	bl_label		= 'Delete Point'
	bl_description  = 'Delete Point'
	
	def execute(self, context):
		NamePoint1 = bpy.context.active_object; bpy.ops.object.delete()
		if not NamePoint1.name.find("_L") == -1: NamePoint2 = bpy.data.objects[NamePoint1.name.replace("_L", "_R")]
		else: NamePoint2 = bpy.data.objects[NamePoint1.name.replace("_R", "_L")]
		NamePoint2.select = True; bpy.ops.object.delete()
		return {'FINISHED'}

class MishMorphClear1(bpy.types.Operator):
	bl_idname   	= '3dmish.morph_clear1'
	bl_label		= ''
	bl_description  = 'Clear'
	
	def execute(self, context):
		bpy.context.scene.MishMorphImage1 = ''
		return {'FINISHED'}

class MishMorphClear2(bpy.types.Operator):
	bl_idname   	= '3dmish.morph_clear2'
	bl_label		= ''
	bl_description  = 'Clear'
	
	def execute(self, context):
		bpy.context.scene.MishMorphImage2 = ''
		return {'FINISHED'}

def BoMeDD(Vector1, Vector2):
	if Vector1[0] > Vector2[0]: X = (Vector1[0]-Vector2[0])
	else: X = -(Vector2[0]-Vector1[0])
	if Vector1[1] > Vector2[1]: Y = (Vector1[1]-Vector2[1])
	else: Y = -(Vector2[1]-Vector1[1])
	if Vector1[2] > Vector2[2]: Z = (Vector1[2]-Vector2[2])
	else: Z = -(Vector2[2]-Vector1[2])
	return (X, Y, Z)

def MishMorphAddPoint():
	MishMorphPointL = bpy.data.objects.new("3DMish_Morph_Point_L", None); scene = bpy.context.scene; scene.objects.link(MishMorphPointL);
	MishMorphPointL.empty_draw_type = 'PLAIN_AXES'; 			 MishMorphPointL.empty_draw_size = 0.05;
	MishMorphPointL.parent = bpy.data.objects['MishMorphImg_1']; bpy.ops.object.select_all(action='DESELECT'); MishMorphPointL.select = True;
	bpy.context.scene.objects.active = MishMorphPointL; 		 bpy.ops.object.constraint_add(type='LIMIT_LOCATION'); 
	bpy.context.object.constraints["Limit Location"].use_min_x = True;  	bpy.context.object.constraints["Limit Location"].min_x = -1.0; 
	bpy.context.object.constraints["Limit Location"].use_max_x = True;  	bpy.context.object.constraints["Limit Location"].max_x =  1.0;
	bpy.context.object.constraints["Limit Location"].use_min_y = True;  	bpy.context.object.constraints["Limit Location"].min_y = -1.0;
	bpy.context.object.constraints["Limit Location"].use_max_y = True;  	bpy.context.object.constraints["Limit Location"].max_y =  1.0; 
	bpy.context.object.constraints["Limit Location"].use_min_z = True;  	bpy.context.object.constraints["Limit Location"].min_z =  0.0; 
	bpy.context.object.constraints["Limit Location"].use_max_z = True;  	bpy.context.object.constraints["Limit Location"].max_z =  0.0;
	bpy.context.object.constraints["Limit Location"].owner_space = 'LOCAL'; bpy.context.object.constraints["Limit Location"].use_transform_limit = True
	scene.update();
	
	MishMorphPointR = bpy.data.objects.new("3DMish_Morph_Point_R", None); scene = bpy.context.scene; scene.objects.link(MishMorphPointR);
	MishMorphPointR.empty_draw_type = 'PLAIN_AXES'; 			 MishMorphPointR.empty_draw_size = 0.05;
	MishMorphPointR.parent = bpy.data.objects['MishMorphImg_2']; bpy.ops.object.select_all(action='DESELECT'); MishMorphPointR.select = True;
	bpy.context.scene.objects.active = MishMorphPointR; 		 bpy.ops.object.constraint_add(type='LIMIT_LOCATION'); 
	bpy.context.object.constraints["Limit Location"].use_min_x = True;  	bpy.context.object.constraints["Limit Location"].min_x = -1.0; 
	bpy.context.object.constraints["Limit Location"].use_max_x = True;  	bpy.context.object.constraints["Limit Location"].max_x =  1.0;
	bpy.context.object.constraints["Limit Location"].use_min_y = True;  	bpy.context.object.constraints["Limit Location"].min_y = -1.0;
	bpy.context.object.constraints["Limit Location"].use_max_y = True;  	bpy.context.object.constraints["Limit Location"].max_y =  1.0; 
	bpy.context.object.constraints["Limit Location"].use_min_z = True;  	bpy.context.object.constraints["Limit Location"].min_z =  0.0; 
	bpy.context.object.constraints["Limit Location"].use_max_z = True;  	bpy.context.object.constraints["Limit Location"].max_z =  0.0;
	bpy.context.object.constraints["Limit Location"].owner_space = 'LOCAL'; bpy.context.object.constraints["Limit Location"].use_transform_limit = True
	scene.update();
	
	bpy.ops.object.select_all(action='DESELECT'); MishMorphPointL.select = True; bpy.context.scene.objects.active = MishMorphPointL;
	return MishMorphPointL, MishMorphPointR

def MishMorphCreatePolyPlane(name): 
	me = bpy.data.meshes.new(name+"_Mesh"); ob = bpy.data.objects.new(name, me); scn = bpy.context.scene; scn.objects.link(ob);
	scn.objects.active = ob; ob.select = True; gV = [(-1.0, -1.0, 0.0),(1.0, -1.0, 0.0),(-1.0, 1.0, 0.0),(1.0, 1.0, 0.0)];
	gF = [(0, 1, 3, 2)]; me.from_pydata(gV, [], gF); me.update();
	return ob

def MishMorphSetMaterial(obj, material): mt = obj.data; mt.materials.append(material)

def MishMorphMakeMaterial(name, diffuse, specular, alpha):
	mat = bpy.data.materials.new(name); mat.diffuse_color  = diffuse;  mat.diffuse_shader  = 'LAMBERT';
	mat.diffuse_intensity  = 1.0;   	mat.specular_color = specular; mat.specular_shader = 'COOKTORR';
	mat.specular_intensity = 0; 		mat.alpha = alpha;  		   mat.use_shadeless   = 1; mat.ambient = 1;
	return mat

def MishMorphMakeMaterialCycles(name, img1):
	mat = bpy.data.materials.new(name); mat.use_nodes = True;
	nodes = mat.node_tree.nodes
	links = mat.node_tree.links

	while(nodes): nodes.remove(nodes[0])
	
	out  = nodes.new("ShaderNodeOutputMaterial")
	out.location = 200, 0
	nodeD = nodes.new("ShaderNodeBsdfDiffuse")
	nodeD.location = 0, 0
	nodeT = nodes.new("ShaderNodeTexImage")
	nodeT.location = -200, 0

	links.new(nodeD.inputs['Color'], nodeT.outputs['Color'])
	links.new(out.inputs['Surface'], nodeD.outputs['BSDF'])
	
	nodeT.image = bpy.data.images.load(img1)
	return mat


def MishMorphMaterialCycles(name, img1, img2):
	mat = bpy.data.materials.new(name); mat.use_nodes = True;
	nodes = mat.node_tree.nodes
	links = mat.node_tree.links

	while(nodes): nodes.remove(nodes[0])
	
	out  = nodes.new("ShaderNodeOutputMaterial"); out.location = 200, 0;
	nodeD = nodes.new("ShaderNodeBsdfDiffuse");   nodeD.location = 0, 0;
	mrgb = nodes.new("ShaderNodeMixRGB");   	  mrgb.location = -200, 0;
	nodeT1 = nodes.new("ShaderNodeTexImage");     nodeT1.location = -400, 150;
	nodeT2 = nodes.new("ShaderNodeTexImage");     nodeT2.location = -400, -150;

	links.new(mrgb.inputs['Color1'], nodeT1.outputs['Color'])
	links.new(mrgb.inputs['Color2'], nodeT2.outputs['Color'])
	links.new(nodeD.inputs['Color'], mrgb.outputs['Color'])
	links.new(out.inputs['Surface'], nodeD.outputs['BSDF'])
	
	nodeT1.image = bpy.data.images.load(img1)
	nodeT2.image = bpy.data.images.load(img2)
	return mat

def initSceneProperties(X=0, Y=0, Z=0):
	bpy.types.Scene.MishMorphX = bpy.props.IntProperty(name = "X", default = 16);
	bpy.types.Scene.MishMorphY = bpy.props.IntProperty(name = "Y", default = 9);
	bpy.types.Scene.MishMorphImage1 = StringProperty(name="", subtype="FILE_PATH", description='Start Image / Video');
	bpy.types.Scene.MishMorphImage2 = StringProperty(name="", subtype="FILE_PATH", description='Final Image / Video');
	bpy.types.Scene.MishMorphQuality = IntProperty(name="", default = 5, min = 0, max = 10)
	return
initSceneProperties()

def register():
	bpy.utils.register_class(MishMorph);		   bpy.utils.register_class(MishMorphStart);	  bpy.utils.register_class(MishMorphCancel);
	bpy.utils.register_class(MishMorphGenerate);   bpy.utils.register_class(MishMorphAddPoints);   bpy.utils.register_class(MishMorphDeletePoint);
	bpy.utils.register_class(MishMorphClear1);     bpy.utils.register_class(MishMorphClear2);

def unregister():
	bpy.utils.unregister_class(MishMorph);  	   bpy.utils.unregister_class(MishMorphStart);    bpy.utils.unregister_class(MishMorphCancel);
	bpy.utils.unregister_class(MishMorphGenerate); bpy.utils.unregister_class(MishMorphAddPoints); bpy.utils.unregister_class(MishMorphDeletePoint);
	bpy.utils.unregister_class(MishMorphClear1);   bpy.utils.unregister_class(MishMorphClear2);

if __name__ == "__main__":
	register()
