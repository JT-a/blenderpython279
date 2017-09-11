import bpy
#import bgl
from bgl import *
import blf
from mathutils import Vector

def poly(points):
	if len(points):
		glBegin(GL_POLYGON)
		for p in points:
			glVertex2f(p.x, p.y)
		glEnd()

# /* draw vertical shape visualizing future joining (up/down direction) */
# static void draw_vertical_join_shape(sa *sa, char dir)
def draw_vertical_join_shape(sa, direction = "u"):

	# vec2f points[10];
	# short i;
	# float w, h;
	# float width = sa->v3->vec.x - sa->v1->vec.x;
	# float height = sa->v3->vec.y - sa->v1->vec.y;
	points = [Vector([0,0]) for i in range(10)]
	width = sa.width
	height = sa.height

	if (height < width):
		h = height / 4
		w = height / 8
	else:
		h = width / 4
		w = width / 8

	#clockwise
	v1 = Vector([sa.x, sa.y])
	v2 = Vector([sa.x, sa.y + height])
	v3 = Vector([sa.x + width, sa.y + height])
	v4 = Vector([sa.x + width, sa.y])
	
	# points[0].x = sa->v1->vec.x + width / 2;
	# points[0].y = sa->v3->vec.y;
	points[0].x  = v1.x + width / 2
	points[0].y  = v3.y

	# points[1].x = sa->v2->vec.x;
	# points[1].y = sa->v2->vec.y;
	points[1].x  = v2.x 
	points[1].y  = v2.y

	# points[2].x = sa->v1->vec.x;
	# points[2].y = sa->v1->vec.y + h;
	points[2].x  = v1.x 
	points[2].y  = v1.y + h

	# points[3].x = sa->v1->vec.x + width / 2 - 2 * w;
	# points[3].y = sa->v1->vec.y + h;
	points[3].x  = v1.x + width / 2 - 2 * w
	points[3].y  = v1.y + h

	# points[4].x = sa->v1->vec.x + width / 2;
	# points[4].y = sa->v1->vec.y + 2 * h;
	points[4].x  = v1.x + width / 2
	points[4].y  = v1.y + 2 * h

	# points[5].x = sa->v1->vec.x + width / 2 + 2 * w;
	# points[5].y = sa->v1->vec.y + h;
	points[5].x  = v1.x + width / 2 + 2 * w
	points[5].y  = v1.y + h

	# points[6].x = sa->v4->vec.x;
	# points[6].y = sa->v4->vec.y + h;
	points[6].x  = v4.x 
	points[6].y  = v4.y + h

	# points[7].x = sa->v3->vec.x;
	# points[7].y = sa->v3->vec.y;
	points[7].x  = v3.x 
	points[7].y  = v3.y

	# points[8].x = sa->v1->vec.x + width / 2 - w;
	# points[8].y = sa->v1->vec.y;
	points[8].x  = v1.x + width / 2 - w
	points[8].y  = v1.y
	
	# points[9].x = sa->v1->vec.x + width / 2 + w;
	# points[9].y = sa->v1->vec.y;
	points[9].x  = v1.x + width / 2 + w
	points[9].y  = v1.y

	# if (dir == 'u') {
	# 	# /* when direction is up, then we flip direction of arrow */
	# 	float cy = sa->v1->vec.y + height;
	# 	for (i = 0; i < 10; i++) {
	# 		points[i].y -= cy;
	# 		points[i].y = -points[i].y;
	# 		points[i].y += sa->v1->vec.y;
	# 	}
	# }
	if direction == "u":
		cy = v1.y + height
		for i in range(10):
			points[i].y -= cy
			points[i].y  = -points[i].y
			points[i].y += v1.y

	# glBegin(GL_POLYGON);
	# for (i = 0; i < 5; i++)
	# 	glVertex2f(points[i].x, points[i].y);
	# glEnd();
	glBegin(GL_POLYGON)
	for i in range(5):
		glVertex2f(points[i].x, points[i].y)
	glEnd()

	# glBegin(GL_POLYGON);
	# for (i = 4; i < 8; i++)
	# 	glVertex2f(points[i].x, points[i].y);
	# glVertex2f(points[0].x, points[0].y);
	# glEnd();
	glBegin(GL_POLYGON)
	for i in range(4, 8):
		glVertex2f(points[i].x, points[i].y)
	glVertex2f(points[0].x, points[0].y)
	glEnd()

	glRectf(points[2].x, points[2].y, points[8].x, points[8].y)
	glRectf(points[6].x, points[6].y, points[9].x, points[9].y)


def draw_callback_px(self, context):
	area = context.area
	#direction = "u"
	#draw_horizontal_join_shape(sa, direction)
	print("drawing")
	draw_vertical_join_shape(area, "u")
	

class ModalDrawOperator(bpy.types.Operator):
	"""Draw a line with the mouse"""
	bl_idname = "view3d.modal_operator"
	bl_label = "Simple Modal View3D Operator"

	def modal(self, context, event):
		context.area.tag_redraw()

		if event.type == 'MOUSEMOVE':
			self.mouse_path.append((event.mouse_region_x, event.mouse_region_y))

		elif event.type == 'LEFTMOUSE':
			bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
			return {'FINISHED'}

		elif event.type in {'RIGHTMOUSE', 'ESC'}:
			bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		if context.area.type == 'VIEW_3D':
			# the arguments we pass the the callback
			args = (self, context)
			# Add the region OpenGL drawing callback
			# draw in view space with 'POST_VIEW' and 'PRE_VIEW'
			self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

			self.mouse_path = []

			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		else:
			self.report({'WARNING'}, "View3D not found, cannot run operator")
			return {'CANCELLED'}


def register():
	bpy.utils.register_class(ModalDrawOperator)


def unregister():
	bpy.utils.unregister_class(ModalDrawOperator)

if __name__ == "__main__":
	register()
