bl_info = {
    "name": "Sequencer Motion Blur",
    "author": "SayPRODUCTIONS",
    "version": (2, 0),
    "blender": (2, 6, 9),
    "description": "Sequencer Motion Blur",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sequencer"}
import bpy
from bpy.props import *
class svemotionblur(bpy.types.Panel):
    bl_space_type ="SEQUENCE_EDITOR"
    bl_region_type="UI"
    bl_label      ="Motion Blur"  
    def draw(self, context):
        layout = self.layout
        row=layout.row();row.prop(context.window_manager,'H');row.prop(context.window_manager,'M')
        row=layout.row();row.prop(context.window_manager,'F');row.operator('sve.motion_blur',icon='FORCE_HARMONIC')
class MotionBlur(bpy.types.Operator) :
    bl_idname ='sve.motion_blur'
    bl_label  ='Motion Blur'
    def invoke(self,context,event):
        seq = bpy.context.scene.sequence_editor
        sve = bpy.ops.sequencer

        H = context.window_manager.H
        M = context.window_manager.M
        F = context.window_manager.F

        S = [seq.active_strip]
        if  S[0]!=None:
            s = S[0].frame_start
            m = S[0].animation_offset_start
            n = S[0].animation_offset_end
            c = S[0].channel
            if  S[0].type=='MOVIE':
                for i in range(1,M):
                    sve.movie_strip_add(filepath =S[0].filepath ,frame_start=s,channel=c+i,sound=False)
                    v=seq.active_strip
                    v.animation_offset_start=m+(i*F)
                    v.animation_offset_end  =n-(i*F)
                    v.blend_alpha=1/(i+1)
                    S.append(v)
            if  S[0].type=='IMAGE':
                Files=[]
                for e in S[0].elements:Files.append({'name':e.filename,'name':e.filename})
                for i in range(1,M):
                    sve.image_strip_add(directory=S[0].directory,frame_start=s,channel=c+i,files=Files)
                    v=seq.active_strip
                    v.animation_offset_start=m+(i*F)
                    v.animation_offset_end  =n-(i*F)
                    v.blend_alpha=1/(i+1)
                    S.append(v)
            for i in S:i.select=True
            bpy.ops.sequencer.meta_make()        
            m=seq.active_strip
            m.channel=c
            m.frame_offset_end=round(m.frame_final_duration*((H-1)/H))
            if  H!=1:
                sve.effect_strip_add(type='SPEED')
                S=seq.active_strip
                m.select=True
        return {"FINISHED"}
def register()  :
    bpy.utils.register_class(  svemotionblur);bpy.utils.register_class(  MotionBlur)
    bpy.types.WindowManager.H=FloatProperty(name='Speed'   ,min=0.1,max=32,default=3,description='Multply Speed'  ,options={'SKIP_SAVE'})
    bpy.types.WindowManager.M=IntProperty(  name='Blur'    ,min=  0,max=32,default=3,description='Duplicate Strip',options={'SKIP_SAVE'})
    bpy.types.WindowManager.F=IntProperty(  name='Distance',min=  1,max=64,default=1,description='Frame Distance' ,options={'SKIP_SAVE'})
def unregister():
    bpy.utils.unregister_class(svemotionblur);bpy.utils.unregister_class(MotionBlur)
    del bpy.types.WindowManager.H
    del bpy.types.WindowManager.M
    del bpy.types.WindowManager.F
if __name__ == "__main__":register()