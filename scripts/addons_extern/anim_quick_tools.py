bl_info = {'name': 'Keyframe QuickTools',
           'author': 'Joel Daniels',
           'version': (0, 1),
           'category': 'Animation',
           'location': '3D View -> UI panel',
           'description': 'A handful of quick-reference tools for keyframe manipulation'}


import bpy


def get_keyframe(fcurves, frame):
    '''Return first keyframe type found'''
    for fcu in fcurves:
        if fcu:
            for kp in fcu.keyframe_points:
                if kp.co.x == frame:
                    return kp


def type_name(keyframe):
    '''Return a string for the type of keyframe'''
    text = ""
    if keyframe:
        if keyframe.type == 'KEYFRAME':
            return "Key Pose"
        elif keyframe.type == 'EXTREME':
            return "Primary Breakdown"
        elif keyframe.type == 'BREAKDOWN':
            return "Secondary Breakdown"
        elif keyframe.type == 'JITTER':
            return "Moving Hold"
    else:
        return "(None)"

# ----------------------------------------------


class VIEW3D_OT_SetKeyTypeSBD(bpy.types.Operator):
    bl_idname = "keyframes.settype_sbd"
    bl_label = "S BD"
    bl_description = "Set keyframe type to secondary breakdown"

    def execute(self, context):
        scene = context.scene
        frame = scene.frame_current
        object = context.object
        fcurves = object.animation_data.action.fcurves

        for fcu in fcurves:
            if fcu:
                for kp in fcu.keyframe_points:
                    if kp.co.x == frame:
                        kp.type = 'BREAKDOWN'
        return {'FINISHED'}

# ----------------------------------------------


class VIEW3D_OT_SetKeyTypeMH(bpy.types.Operator):
    bl_idname = "keyframes.settype_mh"
    bl_label = "MH"
    bl_description = "Set keyframe type to moving hold"

    def execute(self, context):
        scene = context.scene
        frame = scene.frame_current
        object = context.object
        fcurves = object.animation_data.action.fcurves

        for fcu in fcurves:
            if fcu:
                for kp in fcu.keyframe_points:
                    if kp.co.x == frame:
                        kp.type = 'JITTER'
        return {'FINISHED'}

# ----------------------------------------------


class VIEW3D_OT_SetKeyTypeKP(bpy.types.Operator):
    bl_idname = "keyframes.settype_key"
    bl_label = "KEY"
    bl_description = "Set keyframe type to key pose"

    def execute(self, context):
        scene = context.scene
        frame = scene.frame_current
        object = context.object
        fcurves = object.animation_data.action.fcurves

        for fcu in fcurves:
            if fcu:
                for kp in fcu.keyframe_points:
                    if kp.co.x == frame:
                        kp.type = 'KEYFRAME'
        return {'FINISHED'}

# ----------------------------------------------


class VIEW3D_OT_SetKeyTypePBD(bpy.types.Operator):
    bl_idname = "keyframes.settype_pbd"
    bl_label = "P BD"
    bl_description = "Set keyframe type to primary breakdown"

    def execute(self, context):
        scene = context.scene
        frame = scene.frame_current
        object = context.object
        fcurves = object.animation_data.action.fcurves

        for fcu in fcurves:
            if fcu:
                for kp in fcu.keyframe_points:
                    if kp.co.x == frame:
                        kp.type = 'EXTREME'
        return {'FINISHED'}

# -----------------------------------------------


class VIEW3D_OT_PushKeys(bpy.types.Operator):
    bl_idname = "keyframes.push_keys"
    bl_label = "Push Keys"
    bl_description = "Push current and subsequent keys by a set number of frames"

    def execute(self, context):
        scene = context.scene
        obj = context.object
        fcurves = obj.animation_data.action.fcurves
        current_frame = scene.frame_current

        def push(fcurves):
            for fcu in fcurves:
                for kp in fcu.keyframe_points:
                    if scene.push_keys_mode == 'after':
                        if kp.co.x >= current_frame:
                            kp.co.x += scene.push_keys_int
                            kp.handle_left.x += scene.push_keys_int
                            kp.handle_right.x += scene.push_keys_int
                    elif scene.push_keys_mode == 'before':
                        if kp.co.x <= current_frame:
                            kp.co.x += scene.push_keys_int
                            kp.handle_left.x += scene.push_keys_int
                            kp.handle_right.x += scene.push_keys_int
                    elif scene.push_keys_mode == 'only_after':
                        if kp.co.x > current_frame:
                            kp.co.x += scene.push_keys_int
                            kp.handle_left.x += scene.push_keys_int
                            kp.handle_right.x += scene.push_keys_int
                    elif scene.push_keys_mode == 'only_before':
                        if kp.co.x < current_frame:
                            kp.co.x += scene.push_keys_int
                            kp.handle_left.x += scene.push_keys_int
                            kp.handle_right.x += scene.push_keys_int
                    # All
                    else:
                        kp.co.x += scene.push_keys_int
                        kp.handle_left.x += scene.push_keys_int
                        kp.handle_right.x += scene.push_keys_int

        push(fcurves)

        if obj.data.animation_data is not None and obj.data.animation_data.action is not None:
            data_fcurves = obj.data.animation_data.action.fcurves
            push(data_fcurves)

        return {'FINISHED'}

# -----------------------------------------------


class VIEW3D_OT_AutoClampedHandles(bpy.types.Operator):
    bl_idname = "keyframes.to_autoclamped"
    bl_label = "Auto-Clamped"
    bl_description = "Set handle types to auto-clamped"

    def execute(self, context):
        scene = context.scene
        fcurves = context.object.animation_data.action.fcurves
        current_frame = scene.frame_current

        for fcu in fcurves:
            for kp in fcu.keyframe_points:
                if scene.handle_mode == 'current':
                    if kp.co.x == current_frame:
                        kp.handle_right_type = 'AUTO_CLAMPED'
                        kp.handle_left_type = 'AUTO_CLAMPED'
                else:
                    kp.handle_right_type = 'AUTO_CLAMPED'
                    kp.handle_left_type = 'AUTO_CLAMPED'

        return {'FINISHED'}

# -----------------------------------------------


class VIEW3D_OT_AlignedHandles(bpy.types.Operator):
    bl_idname = "keyframes.to_aligned"
    bl_label = "Aligned"
    bl_description = "Set handle types to aligned"

    def execute(self, context):
        scene = context.scene
        fcurves = context.object.animation_data.action.fcurves
        current_frame = scene.frame_current

        for fcu in fcurves:
            for kp in fcu.keyframe_points:
                if scene.handle_mode == 'current':
                    if kp.co.x == current_frame:
                        kp.handle_right_type = 'ALIGNED'
                        kp.handle_left_type = 'ALIGNED'
                else:
                    kp.handle_right_type = 'ALIGNED'
                    kp.handle_left_type = 'ALIGNED'

        return {'FINISHED'}

# -----------------------------------------------


class VIEW3D_OT_VectorHandles(bpy.types.Operator):
    bl_idname = "keyframes.to_vector"
    bl_label = "Vector"
    bl_description = "Set handle types to vector"

    def execute(self, context):
        scene = context.scene
        fcurves = context.object.animation_data.action.fcurves
        current_frame = scene.frame_current

        for fcu in fcurves:
            for kp in fcu.keyframe_points:
                if scene.handle_mode == 'current':
                    if kp.co.x == current_frame:
                        kp.handle_right_type = 'VECTOR'
                        kp.handle_left_type = 'VECTOR'
                else:
                    kp.handle_right_type = 'VECTOR'
                    kp.handle_left_type = 'VECTOR'

        return {'FINISHED'}

# -----------------------------------------------


class VIEW3D_OT_FreeHandles(bpy.types.Operator):
    bl_idname = "keyframes.to_free"
    bl_label = "Free"
    bl_description = "Set handle types to free"

    def execute(self, context):
        scene = context.scene
        fcurves = context.object.animation_data.action.fcurves
        current_frame = scene.frame_current

        for fcu in fcurves:
            for kp in fcu.keyframe_points:
                if scene.handle_mode == 'current':
                    if kp.co.x == current_frame:
                        kp.handle_right_type = 'FREE'
                        kp.handle_left_type = 'FREE'
                else:
                    kp.handle_right_type = 'FREE'
                    kp.handle_left_type = 'FREE'

        return {'FINISHED'}

# -----------------------------------------------


class VIEW3D_OT_InterpType(bpy.types.Operator):
    bl_idname = "keyframes.set_interp_type"
    bl_label = "Set Interpolation"

    def execute(self, context):
        scene = context.scene
        fcurves = context.object.animation_data.action.fcurves
        current_frame = scene.frame_current

        for fcu in fcurves:
            for kp in fcu.keyframe_points:
                # Spline
                if scene.interp_type == 'spline':
                    if scene.interp_mode == 'current':
                        if kp.co.x == current_frame:
                            kp.interpolation = 'BEZIER'
                    else:
                        kp.interpolation = 'BEZIER'

                # Linear
                elif scene.interp_type == 'linear':
                    if scene.interp_mode == 'current':
                        if kp.co.x == current_frame:
                            kp.interpolation = 'LINEAR'
                    else:
                        kp.interpolation = 'LINEAR'

                # Stepped
                elif scene.interp_type == 'stepped':
                    if scene.interp_mode == 'current':
                        if kp.co.x == current_frame:
                            kp.interpolation = 'CONSTANT'
                    else:
                        kp.interpolation = 'CONSTANT'

        return {'FINISHED'}

# -----------------------------------------------


class VIEW3D_OT_ScaleKeys(bpy.types.Operator):
    bl_idname = "keyframes.scale_keys"
    bl_label = "Scale Keyframes"
    bl_description = "Scale subsequent keyframes around current frame"

    def execute(self, context):
        scene = context.scene
        current_frame = scene.frame_current
        fcurves = context.object.animation_data.action.fcurves

        for fcu in fcurves:
            for i in reversed(range(1, fcu.keyframe_points.__len__())):
                #            for kp in fcu.keyframe_points:
                #                if kp.co.x > current_frame:
                #                    kp.co.x *= scene.scale_amt
                if fcu.keyframe_points[i].co.x > current_frame:
                    mult = scene.scale_amt * (fcu.keyframe_points[i].co.x - fcu.keyframe_points[i - 1].co.x)
                    fcu.keyframe_points[i].co.x *= mult

        return {'FINISHED'}

# -----------------------------------------------


class VIEW3D_OT_SetToStacked(bpy.types.Operator):
    bl_idname = "keyframes.to_stacked"
    bl_label = "Stack Keys"
    bl_description = "Set all subsequent keyframes to stacked position - separated by only one frame each)"

    def execute(self, context):
        sce = bpy.context.scene
        ob = bpy.context.object

        if ob.animation_data is None or ob.animation_data.action is None:
            raise ValueError
        fcurves = ob.animation_data.action.fcurves

        def stack(fcurves):
            inverse_index = {}
            for fcu in fcurves:
                for point in fcu.keyframe_points:
                    f = round(point.co.x)
                    if f < sce.frame_current:
                        continue
                    try:
                        inverse_index[f].append(point)
                    except KeyError:
                        inverse_index[f] = [point]

            i = sce.frame_current
            for f, points in sorted(inverse_index.items()):
                for point in points:
                    point.co.x = i
                i += 1

        stack(fcurves)

        if ob.data.animation_data is not None and ob.data.animation_data.action is not None:
            data_fcurves = ob.data.animation_data.action.fcurves
            stack(data_fcurves)

        return {'FINISHED'}

# ----------------------------------------------


class VIEW3D_OT_NudgeKeys(bpy.types.Operator):
    bl_idname = "keyframes.nudge_keys"
    bl_label = "Nudge Keys"
    bl_description = "Nudge keys one frame at a time"

    forward = bpy.props.BoolProperty(default=True)

    def execute(self, context):
        scene = context.scene
        current_frame = scene.frame_current
        fcurves = context.object.animation_data.action.fcurves
        obj = context.object

        def nudge(fcurves):
            if self.forward == True:
                for fcu in fcurves:
                    for kp in fcu.keyframe_points:
                        if kp.co.x == current_frame:
                            kp.co.x += 1
                            kp.handle_left.x += 1
                            kp.handle_right.x += 1

            else:
                for fcu in fcurves:
                    for kp in fcu.keyframe_points:
                        if kp.co.x == current_frame:
                            kp.co.x -= 1
                            kp.handle_left.x -= 1
                            kp.handle_right.x -= 1

        nudge(fcurves)
        if obj.data.animation_data is not None and obj.data.animation_data.action is not None:
            data_fcurves = obj.data.animation_data.action.fcurves
            nudge(data_fcurves)

        if self.forward:
            scene.frame_current += 1
        else:
            scene.frame_current -= 1

        return {'FINISHED'}

# -----------------------------------------------
# 3D View UI panels


class VIEW3D_PT_KeyTypes(bpy.types.Panel):
    bl_label = "Keyframe QuickTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Animate"

    @classmethod
    def poll(cls, context):
        return (context.object is not None and context.object.animation_data is not None)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        action = context.object.animation_data.action
        if action:
            fcurves = action.fcurves
            current_frame = scene.frame_current
            keyframes = get_keyframe(fcurves, current_frame)
            type = type_name(keyframes)

            layout.label("Current keyframe type:")
            layout.label(type, icon="SPACE2" if type != "(None)" else "ERROR")
            # row = layout.row()
            # row.enabled = False
            # row.prop(keyframes, "type", text = "", toggle = True)

            layout.label("Set keyframe type:")
            row = layout.row(align=True)
            row.operator("keyframes.settype_key")
            row.operator("keyframes.settype_pbd")
            row.operator("keyframes.settype_sbd")
            row.operator("keyframes.settype_mh")

            row = layout.row()
            row.alignment = 'CENTER'
            row.label("_______________________________________")

            layout.label("Push keys:")
            layout.operator("keyframes.push_keys", text="Push Keys")
            layout.prop(scene, "push_keys_mode")
            layout.prop(scene, "push_keys_int")

            layout.separator()

            layout.label("Nudge keys:")
            row = layout.row()
            row.alignment = 'CENTER'
            row.operator("keyframes.nudge_keys", text="", icon="TRIA_LEFT", emboss=False).forward = False
            row.label("Nudge")
            row.operator("keyframes.nudge_keys", text="", icon="TRIA_RIGHT", emboss=False).forward = True

            # layout.label("Scale keys:")
            # layout.operator("keyframes.scale_keys")
            # layout.prop(scene, "scale_amt")

            layout.separator()

            layout.label("Set keys to stacked:")
            layout.operator("keyframes.to_stacked")

            row = layout.row()
            row.alignment = 'CENTER'
            row.label("_______________________________________")

            layout.label("Keyframe handle types:")

            row = layout.row()

            row.operator("keyframes.to_autoclamped")
            row.operator("keyframes.to_aligned")
            row = layout.row()
            row.operator("keyframes.to_vector")
            row.operator("keyframes.to_free")
            layout.label("Apply to:")
            layout.prop(scene, "handle_mode")

            row = layout.row()
            row.alignment = 'CENTER'
            row.label("_______________________________________")

            layout.label("Keyframe interpolation:")
            layout.operator("keyframes.set_interp_type")
            row = layout.row()
            row.prop(scene, "interp_type")
            row.prop(scene, "interp_mode")

        else:
            layout.label("Active object has no animation data.")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.push_keys_int = bpy.props.IntProperty(name="Frames", description="Push keyframes by this number of frames", default=0)
    bpy.types.Scene.push_keys_mode = bpy.props.EnumProperty(items=[
        ('only_after', "After Only", "Push only keys after current frame"),
        ('only_before', "Before Only", "Push only keys before current frame"),
        ('after', "Current and After", "Push current and subsequent keys"),
        ('before', "Current and Before", "Push current and previous keys"),
        ('all', "All Keys", "Push all keys")],
        name="",
        description="",
        default='only_after')
    bpy.types.Scene.handle_mode = bpy.props.EnumProperty(items=[
        ('current', "Current Frame", "Apply handles only to the current frame"),
        ('all', "All Frames", "Apply handles to all frames")],
        name="",
        description="",
        default='all')

    bpy.types.Scene.interp_mode = bpy.props.EnumProperty(items=[
        ('current', "Current Frame", "Apply handles only to the current frame"),
        ('all', "All Frames", "Apply handles to all frames")],
        name="",
        description="",
        default='all')

    bpy.types.Scene.interp_type = bpy.props.EnumProperty(items=[
        ('spline', "Spline", "Apply bezier interpolation"),
        ('linear', "Linear", "Apply linear interpolation"),
        ('stepped', "Stepped", "Apply stepped interpolation")],
        name="",
        description="",
        default='spline')
    bpy.types.Scene.scale_amt = bpy.props.FloatProperty(name="Scale Amount", description="Amount by which to scale keyframes around current frame", default=1.0, min=0.0)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
