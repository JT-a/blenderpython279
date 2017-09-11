import bpy
import math
import mathutils

# Caltulate kd-tree.
def _kdFind(data, point):
    size = len(data)
    kd = mathutils.kdtree.KDTree(size)
    
    for i, d in enumerate(data):
        kd.insert(d, i)

    kd.balance()
    
    co, index, dist = kd.find(point)
    
    return [co, index, dist]

# kd-tree for vertex and a point.
def _kdFindNearestPoint(obj, point=(0,0,0)):
    if obj.type == 'FONT':
        world_verts = [obj.location]
    else:
        # Change into world coordinate.
        world_verts = [obj.matrix_world * v.co for v in obj.data.vertices]
    result = _kdFind(world_verts, point)
    result.append(obj)
    # return [coordinate, vertex index, distance, object].
    return result

# kd-tree looping through objects and a point.
def _addNearestObject(objects, point):
    nearest = {'distance': 10000, 'object': None, 'coordinate': None, 'vertex_index': None}
    for obj in objects:
        near_result = _kdFindNearestPoint(obj=obj, point=point)
        if near_result[2] < nearest['distance']:
            nearest['distance'] = near_result[2]
            nearest['object'] = near_result[3]
            nearest['coordinate'] = near_result[0]
            nearest['vertex_index'] = near_result[1]
    return nearest

# Make list of 3 valued location vector.
def _makeCurveLocVector(active_curve):
    curve_points = []
    if active_curve.data.splines[0].type == 'BEZIER':
        for p in active_curve.data.splines[0].bezier_points:
            world_point = active_curve.matrix_world * p.co
            curve_points.append(world_point)
    
    if active_curve.data.splines[0].type == 'NURBS':
        for p in active_curve.data.splines[0].points:
            world_point = active_curve.matrix_world * mathutils.Vector(p.co[:3])
            curve_points.append(world_point)
    
    return curve_points

# Sort object by nearer vertex to curve's point.
def _sortObjectAlongCurve(objects, active_curve):
        
        # Make list of 3 valued location vector.
        curve_points = _makeCurveLocVector(active_curve)
    
        # Index of curve's point for correspoinding object.
        step = len(curve_points) / len(objects)
        curve_points_index = [math.floor(step*i) for i in range(len(objects))]
        
        sorted_objects = []
        sorted_objects_info = []
        
        # Make list in order of nearest object to a curve's point.curve.
        for i in curve_points_index:
            point_co = curve_points[i]
            
            # Nearest object to the curve's point.
            nearest_object = _addNearestObject(objects=objects, point=point_co)
            
            objects.remove(nearest_object['object'])

            sorted_objects.append(nearest_object['object'])
            sorted_objects_info.append(nearest_object)
            
        return sorted_objects, sorted_objects_info

def sortSelectedObjectAlongCurve(active_object, selected_objects):
    if active_object.type == 'CURVE':
        active_curve = active_object
        
        # Remove active_curve and sort selected_objects:
        selected_objects.remove(active_curve)
        sorted_objects, sorted_objects_info = _sortObjectAlongCurve(selected_objects, active_curve)
        return sorted_objects
        
        # Sort vertex in order of nearer curve's point.
        '''
        if sort_along_curve == True:
            for obj_info in sorted_objects_info:
                curveSort(obj=obj_info['object'], location=obj_info['coordinate'])
        '''

# Divide frame by the number of selected objects.
def divideFrame(objects, frame_range):
    frame_duration = (frame_range[1] + 1) - frame_range[0]
    frame_step = math.floor(frame_duration / len(objects))
    return frame_step
