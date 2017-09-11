####################################
# Look at it
#       v.1.0
#  (c)ishidourou 2013
####################################
#    "name": "Look at it",
#    "author": "ishidourou",
#    "version": (1, 0),
#    "blender": (2, 65, 0),
#    "description": "LookatIt"


import bpy

class TP_Display_Look_at_Menu(bpy.types.Menu):
    bl_label = "Look at Menu"
    bl_idname = "tp_display.look_at_menu"    

    def draw(self, context):
        layout = self.layout 

        layout.label(text="Add Constraint:", icon ="CONSTRAINT_DATA")

        layout.operator("track.to", text="Track To")
        layout.operator("damped.track", text="Damped Track")
        layout.operator("lock.track", text="Lock Track")

        layout.separator()

        layout.label(text="Add Const & Empty at CursorPos:", icon ="OUTLINER_OB_EMPTY")

        layout.operator("track.toempty", text="Track To")
        layout.operator("damped.trackempty", text="Damped Track")
        layout.operator("lock.trackempty", text="Lock Track")



def objselect(objct,selection):
    if (selection == 'ONLY'):
        bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = objct
    objct.select = True


class TP_Display_Look_at_It(bpy.types.Operator):
    bl_idname = "tp_display.look_at_it"
    bl_label = "Look at it"
    def execute(self, context):
        cobj = bpy.context.object
        if bpy.context.mode != 'OBJECT':
            return{'FINISHED'}
        if cobj == None:
            return{'FINISHED'}
        slist = bpy.context.selected_objects
        ct = 0
        for i in slist:
            ct += 1
        if ct == 1:
            return{'FINISHED'}
        bpy.ops.object.track_set(type='TRACKTO')
        bpy.ops.object.track_clear(type='CLEAR_KEEP_TRANSFORM')
        return{'FINISHED'}

class TP_Display_Look_at_Cursor(bpy.types.Operator):
    bl_idname = "tp_display.look_at_cursor"
    bl_label = "Look at Cursor"
    def execute(self, context):
        lookatempty('cursor')
        return{'FINISHED'}


def lookatempty(mode):
    if bpy.context.mode != 'OBJECT':
        return
    cobj = bpy.context.object
    slist = bpy.context.selected_objects
    ct = 0
    for i in slist:
        ct += 1
    if ct == 0:
        return            
    bpy.ops.object.empty_add(type='PLAIN_AXES', view_align=False)
    bpy.context.object.empty_draw_size = 3.00
    target = bpy.context.object
    for i in slist:
        i.select = True
    if mode == 'cursor' or 'damptrackempty':
        bpy.ops.object.track_set(type='DAMPTRACK')
    if mode == 'tracktoempty':
        bpy.ops.object.track_set(type='TRACKTO')
    if mode == 'locktrackempty':
        bpy.ops.object.track_set(type='LOCKTRACK')
    if mode == 'cursor':
        bpy.ops.object.track_clear(type='CLEAR_KEEP_TRANSFORM')
        objselect(target,'ONLY')
        bpy.ops.object.delete(use_global=False)
        objselect(cobj,'ADD')
        for i in slist:
            i.select = True



class TrackTo(bpy.types.Operator):
    bl_idname = "track.to"
    bl_label = "TrackTo"
    def execute(self, context):
        if bpy.context.mode != 'OBJECT':
            return{'FINISHED'}
        bpy.ops.object.track_set(type='TRACKTO')
        return{'FINISHED'}

class DampedTrack(bpy.types.Operator):
    bl_idname = "damped.track"
    bl_label = "DampedTrack"
    def execute(self, context):
        if bpy.context.mode != 'OBJECT':
            return{'FINISHED'}
        bpy.ops.object.track_set(type='DAMPTRACK')
        return{'FINISHED'}

class LockTrack(bpy.types.Operator):
    bl_idname = "lock.track"
    bl_label = "LockTrack"
    def execute(self, context):
        if bpy.context.mode != 'OBJECT':
            return{'FINISHED'}
        bpy.ops.object.track_set(type='LOCKTRACK')
        return{'FINISHED'}

class TrackToEmpty(bpy.types.Operator):
    bl_idname = "track.toempty"
    bl_label = "TrackTo"
    def execute(self, context):
        lookatempty('tracktoempty')
        return{'FINISHED'}

class DampedTrackEmpty(bpy.types.Operator):
    bl_idname = "damped.trackempty"
    bl_label = "DampedTrack"
    def execute(self, context):
        lookatempty('damptrackempty')
        return{'FINISHED'}

class LockTrackEmpty(bpy.types.Operator):
    bl_idname = "lock.trackempty"
    bl_label = "LockTrack"
    def execute(self, context):
        lookatempty('locktrackempty')
        return{'FINISHED'}



def register():
    bpy.utils.register_class(TP_Display_Look_at_It)
    bpy.utils.register_class(TP_Display_Look_at_Cursor)
    bpy.utils.register_class(TP_Display_Look_at_Menu)
    bpy.utils.register_class(TrackTo)
    bpy.utils.register_class(DampedTrack)
    bpy.utils.register_class(LockTrack)
    bpy.utils.register_class(TrackToEmpty)
    bpy.utils.register_class(DampedTrackEmpty)
    bpy.utils.register_class(LockTrackEmpty)

def unregister():

    bpy.utils.unregister_class(TP_Display_Look_at_It)
    bpy.utils.unregister_class(TP_Display_Look_at_Cursor)
    bpy.utils.unregister_class(TP_Display_Look_at_Menu)
    bpy.utils.unregister_class(TrackTo)
    bpy.utils.unregister_class(DampedTrack)
    bpy.utils.unregister_class(LockTrack)
    bpy.utils.unregister_class(TrackToEmpty)
    bpy.utils.unregister_class(DampedTrackEmpty)
    bpy.utils.unregister_class(LockTrackEmpty)

if __name__ == "__main__":
    register()

