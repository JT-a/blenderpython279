import bpy
from bgl import *
import blf
from mathutils import Vector

def draw_horizontal_join_shape(sa, direction):
	
#	vec2f points[10];
#	short i;
#	float w, h;
	width = sa.width
	height = sa.height
	points = [Vector([0,0]) for i in range(10)]
	
	if height < width:
		h = height / 8
		w = height / 4
	
	else:
		h = width / 8
		w = width / 4
	
	#clockwise
	v1 = Vector((sa.x, sa.y))
	v2 = Vector((sa.x, sa.y + height))
	v3 = Vector((sa.x + width, sa.y + height))
	v4 = Vector((sa.x + width, sa.y))
	
#	points[0].x = sa->v1->vec.x;
#	points[0].y = sa->v1->vec.y + height / 2;
	points[0].x = v1.x
	points[0].y = v1.y + height / 2
	
#	points[1].x = sa->v1->vec.x;
#	points[1].y = sa->v1->vec.y;
	points[1].x = v1.x
	points[1].x = v1.y
	
#	points[2].x = sa->v4->vec.x - w;
#	points[2].y = sa->v4->vec.y;
	points[2].x = v4.x - w
	points[2].x = v4.y 
	
#	points[3].x = sa->v4->vec.x - w;
#	points[3].y = sa->v4->vec.y + height / 2 - 2 * h;
	points[3].x = v4.x - w
	points[3].x = v4.y + height / 2 - 2 * h
	
#	points[4].x = sa->v4->vec.x - 2 * w;
#	points[4].y = sa->v4->vec.y + height / 2;
	points[4].x = v4.x - 2 * w
	points[4].x = v4.y + height / 2
	
#	points[5].x = sa->v4->vec.x - w;
#	points[5].y = sa->v4->vec.y + height / 2 + 2 * h;
	points[5].x = v4.x -  w
	points[5].x = v4.y + height / 2 + 2 * h
	
#	points[6].x = sa->v3->vec.x - w;
#	points[6].y = sa->v3->vec.y;
	points[6].x = v3.x -  w
	points[6].x = v3.y

#	points[7].x = sa->v2->vec.x;
#	points[7].y = sa->v2->vec.y;
	points[7].x = v2.x 
	points[7].x = v2.y

#	points[8].x = sa->v4->vec.x;
#	points[8].y = sa->v4->vec.y + height / 2 - h;
	points[8].x = v4.x
	points[8].x = v4.y + height / 2 - h
	
#	points[9].x = sa->v4->vec.x;
#	points[9].y = sa->v4->vec.y + height / 2 + h;
	points[9].x = v4.x
	points[9].x = v4.y + height / 2 + h

	# if (dir == 'l') {
	# 	/* when direction is left, then we flip direction of arrow */
	# 	float cx = sa->v1->vec.x + width;
	# 	for (i = 0; i < 10; i++) {
	# 		points[i].x -= cx;
	# 		points[i].x = -points[i].x;
	# 		points[i].x += sa->v1->vec.x;
	# 	}
	# }
	if direction == "l":
		cx = v1.x + width
		for i in range(10):
			points[i].x -= cx
			points[i].x = -points[i].x
			points[i].x += v1.x


	glBegin(GL_POLYGON)
	#for (i = 0; i < 5; i++)
	for i in range(5):
		glVertex2f(points[i].x, points[i].y)
	glEnd()
	glBegin(GL_POLYGON)
	#for (i = 4; i < 8; i++)
	for i in range(4, 8):
		glVertex2f(points[i].x, points[i].y)
	glVertex2f(points[0].x, points[0].y)
	glEnd()

	glRectf(points[2].x, points[2].y, points[8].x, points[8].y)
	glRectf(points[6].x, points[6].y, points[9].x, points[9].y)


#static void draw_vertical_join_shape(ScrArea *sa, char dir)
def draw_vertical_join_shape(sa, direction):

	# vec2f points[10];
	# short i;
	# float w, h;
	# float width = sa->v3->vec.x - sa->v1->vec.x;
	# float height = sa->v3->vec.y - sa->v1->vec.y;

	points = [Vector([0,0]) for i in range(10)]
	width = sa.width
	height = sa.height

	#clockwise
	v1 = Vector((sa.x, sa.y))
	v2 = Vector((sa.x, sa.y + height))
	v3 = Vector((sa.x + width, sa.y + height))
	v4 = Vector((sa.x + width, sa.y))

	if height < width:
		h = height / 4
		w = height / 8
	else:
		h = width / 4
		w = width / 8

	points[0].x = v1.x
	points[0].y = v1.y
	# points[0].x = sa->v1->vec.x + width / 2;
	# points[0].y = sa->v3->vec.y;

	# points[1].x = sa->v2->vec.x;
	# points[1].y = sa->v2->vec.y;
	points[1].x = v1.x
	points[1].y = v1.y

	# points[2].x = sa->v1->vec.x;
	# points[2].y = sa->v1->vec.y + h;
	points[2].x = v1.x
	points[2].y = v1.y + h

	# points[3].x = sa->v1->vec.x + width / 2 - 2 * w;
	# points[3].y = sa->v1->vec.y + h;
	points[3].x = v1.x + width / 2 - 2 * w
	points[3].y = v1.y + h

	# points[4].x = sa->v1->vec.x + width / 2;
	# points[4].y = sa->v1->vec.y + 2 * h;
	points[4].x = v1.x + width / 2
	points[4].y = v1.y + 2 *  h

	# points[5].x = sa->v1->vec.x + width / 2 + 2 * w;
	# points[5].y = sa->v1->vec.y + h;
	points[5].x = v1.x + width / 2 + 2 * w
	points[5].y = v1.y + h

	# points[6].x = sa->v4->vec.x;
	# points[6].y = sa->v4->vec.y + h;
	points[6].x = v4.x
	points[6].y = v4.y + h
	
	# points[7].x = sa->v3->vec.x;
	# points[7].y = sa->v3->vec.y;
	points[7].x = v3.x
	points[7].y = v3.y

	# points[8].x = sa->v1->vec.x + width / 2 - w;
	# points[8].y = sa->v1->vec.y;
	points[8].x = v1.x + width / 2 - w
	points[8].y = v1.y

	# points[9].x = sa->v1->vec.x + width / 2 + w;
	# points[9].y = sa->v1->vec.y;
	points[9].x = v1.x + width / 2 + w
	points[9].y = v1.y

	# if (dir == 'u') {
	# 	/* when direction is up, then we flip direction of arrow */
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
			points[i].y = -points[i]
			points[i].y += v1.y

	glBegin(GL_POLYGON)
	#for (i = 0; i < 5; i++)
	for i in range(5):
		glVertex2f(points[i].x, points[i].y)
	glEnd()
	glBegin(GL_POLYGON)
	#for (i = 4; i < 8; i++)
	for i in range(4,8):
		glVertex2f(points[i].x, points[i].y)
	glVertex2f(points[0].x, points[0].y)
	glEnd()

	glRectf(points[2].x, points[2].y, points[8].x, points[8].y)
	glRectf(points[6].x, points[6].y, points[9].x, points[9].y)

# static void draw_join_shape(ScrArea *sa, char dir)
# {
# 	if (dir == 'u' || dir == 'd')
# 		draw_vertical_join_shape(sa, dir);
# 	else
# 		draw_horizontal_join_shape(sa, dir);
# }

def draw_join_shape(sa, direction):
	if direction == "u" or direction == "d":
		draw_vertical_join_shape(sa, direction)
	else:
		draw_horizontal_join_shape(sa, direction)

# static void scrarea_draw_shape_dark(ScrArea *sa, char dir)
def scrarea_draw_shape_dark(sa, direction):
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glColor4ub(0, 0, 0, 50)
	draw_join_shape(sa, direction)
	glDisable(GL_BLEND)

#static void scrarea_draw_shape_light(ScrArea *sa, char UNUSED(dir))
def scrarea_draw_shape_light(sa, direction):
	
	v1 = Vector((sa.x, sa.y))
	v2 = Vector((sa.x, sa.y + height))
	v3 = Vector((sa.x + width, sa.y + height))
	v4 = Vector((sa.x + width, sa.y))
	
	glBlendFunc(GL_DST_COLOR, GL_SRC_ALPHA)
	glEnable(GL_BLEND)
	# /* value 181 was hardly computed: 181~105 */
	glColor4ub(255, 255, 255, 50)
	# /* draw_join_shape(sa, dir); */
	#glRecti(sa->v1->vec.x, sa->v1->vec.y, sa->v3->vec.x, sa->v3->vec.y)
	glRecti(v1.x, v1.y, v3.x, v3.y)
	glDisable(GL_BLEND)

#/* only for edge lines between areas, and the blended join arrows */
#void ED_screen_draw(wmWindow *win)
# def ED_screen_draw(win):

# {
# 	const int winsize_x = WM_window_pixels_x(win);
# 	const int winsize_y = WM_window_pixels_y(win);

# 	ScrArea *sa;
# 	ScrArea *sa1 = NULL;
# 	ScrArea *sa2 = NULL;
# 	ScrArea *sa3 = NULL;
# 	int dir = -1;
# 	int dira = -1;

# 	wmSubWindowSet(win, win->screen->mainwin);
	
# 	for (sa = win->screen->areabase.first; sa; sa = sa->next) {
# 		if (sa->flag & AREA_FLAG_DRAWJOINFROM) sa1 = sa;
# 		if (sa->flag & AREA_FLAG_DRAWJOINTO) sa2 = sa;
# 		if (sa->flag & (AREA_FLAG_DRAWSPLIT_H | AREA_FLAG_DRAWSPLIT_V)) sa3 = sa;
# 		drawscredge_area(sa, winsize_x, winsize_y, 0);
# 	}
# 	for (sa = win->screen->areabase.first; sa; sa = sa->next)
# 		drawscredge_area(sa, winsize_x, winsize_y, 1);
	
# 	/* blended join arrow */
# 	if (sa1 && sa2) {
# 		dir = area_getorientation(sa1, sa2);
# 		if (dir != -1) {
# 			switch (dir) {
# 				case 0: /* W */
# 					dir = 'r';
# 					dira = 'l';
# 					break;
# 				case 1: /* N */
# 					dir = 'd';
# 					dira = 'u';
# 					break;
# 				case 2: /* E */
# 					dir = 'l';
# 					dira = 'r';
# 					break;
# 				case 3: /* S */
# 					dir = 'u';
# 					dira = 'd';
# 					break;
# 			}
# 		}
# 		scrarea_draw_shape_dark(sa2, dir);
# 		scrarea_draw_shape_light(sa1, dira);
# 	}
	
# 	/* splitpoint */
# 	if (sa3) {
# 		glEnable(GL_BLEND);
# 		glColor4ub(255, 255, 255, 100);
		
# 		if (sa3->flag & AREA_FLAG_DRAWSPLIT_H) {
# 			sdrawline(sa3->totrct.xmin, win->eventstate->y, sa3->totrct.xmax, win->eventstate->y);
# 			glColor4ub(0, 0, 0, 100);
# 			sdrawline(sa3->totrct.xmin, win->eventstate->y + 1, sa3->totrct.xmax, win->eventstate->y + 1);
# 		}
# 		else {
# 			sdrawline(win->eventstate->x, sa3->totrct.ymin, win->eventstate->x, sa3->totrct.ymax);
# 			glColor4ub(0, 0, 0, 100);
# 			sdrawline(win->eventstate->x + 1, sa3->totrct.ymin, win->eventstate->x + 1, sa3->totrct.ymax);
# 		}
		
# 		glDisable(GL_BLEND);
# 	}
	
# 	win->screen->do_draw = false;
# }