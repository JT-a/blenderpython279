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
	"name": "VertexCoordsColor",
	"author": "Jim Hazevoet",
	"version": (0,0,1),
	"blender": (2, 66, 0),
	"location": "View3D > VertexPaint > Paint",
	"description": "Vertex paint based on vertex coordinate and normal values",
	"warning": "", # used for warning icon and text in addons panel
	"category": "Paint"}

import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, IntProperty, BoolProperty


def applyCoordsColor(me, vert_mode, normalise_val, z_val):

	# color layer data
	active_col_layer = None
	if len(me.vertex_colors):
		for lay in me.vertex_colors:
			if lay.active:
				active_col_layer = lay.data
	else:
		bpy.ops.mesh.vertex_color_add()
		me.vertex_colors[0].active = False
		active_col_layer = me.vertex_colors[0].data
	
	if not active_col_layer:
	   return

	use_paint_mask = me.use_paint_mask

	for i, p in enumerate(me.polygons):
		if not use_paint_mask or p.select:
			for loop_index in p.loop_indices:
				loop = me.loops[loop_index]
				v = loop.vertex_index

				# value from vertex normals
				if vert_mode == "NORMALS":
					if z_val == True:
						n = me.vertices[v].normal[2]
						rgb = n, n, n
					else:
						rgb = me.vertices[v].normal

				# value from vertex coords
				else:
					if z_val == True:
						c = me.vertices[v].co[2]
						rgb = c, c, c
					else:
						rgb = me.vertices[v].co

				if normalise_val == True:
					r = rgb[0] * 0.5 + 0.5
					g = rgb[1] * 0.5 + 0.5
					b = rgb[2] * 0.5 + 0.5
					rgb = r, g, b

				# apply vertex colors
				col = active_col_layer[loop_index].color
				col[0] = rgb[0] * col[0]
				col[1] = rgb[1] * col[1]
				col[2] = rgb[2] * col[2]

	me.update()
	return {'FINISHED'}


class VertexCoordsColor(Operator):
	bl_idname = "paint.vertex_coords_color"
	bl_label = "Vertex Coords Colors"
	bl_options = {'REGISTER', 'UNDO', 'PRESET'}
	bl_description = "Vertex colors from coordinates"

	VertMode = EnumProperty(
            name="Vertex",
			description="Vertex: Coordinates or normals.",
			default="NORMALS",
			items=[ ("COORDS", "Coordinates", "Coordinates"), ("NORMALS", "Normals", "Normals") ] )

	Normalise = BoolProperty(
            name="Normalise",
			description="Normalise: Normalise value.",
			default=True)

	ZValue = BoolProperty(
            name="Z value",
			description="Z value: Greyscale dirtmap or heightmap.",
			default=False)

	# Draw
	def draw(self, context):
		self.layout.prop(self, "VertMode" )
		self.layout.prop(self, "Normalise" )
		self.layout.prop(self, "ZValue" )

	# Execute
	def execute(self, context):
		import time

		obj = context.object
		if obj.type == 'MESH':
			me = obj.data
			t = time.time()
			re = applyCoordsColor(me, self.VertMode, self.Normalise, self.ZValue)
			print('VertexCoordsColors calculated in %.6f' % (time.time() - t))
			return re
		else:
			print("WARNING: Object type is not mesh.")

# Register
def menu_func_coordscolor(self, context):
	self.layout.operator(VertexCoordsColor.bl_idname, text="Vertex Coords Colors", icon="PLUGIN")

def register():
	bpy.utils.register_module(__name__)
	bpy.types.VIEW3D_MT_paint_vertex.append(menu_func_coordscolor)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.VIEW3D_MT_paint_vertex.remove(menu_func_coordscolor)

if __name__ == "__main__":
	register()