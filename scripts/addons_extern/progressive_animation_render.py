bl_info = {
    "name": "Progressive Animation Render",
    "description": "Render the animation repeatedly with different noise patterns and merge it all together for a clean image at the end.",
    "author": "Greg Zaal",
    "version": (0, 3),
    "blender": (2, 67, 1),
    "location": "Properties > Render > Progressive Render panel",
    "warning": "Requires ImageMagick to merge the images! Download it here: www.imagemagick.org",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render"}

import bpy
from os import system, sep, path, makedirs, remove, chmod, path as ospath, listdir
import stat
from shutil import copyfile, rmtree
from random import random

'''
    TODO:
*Force absolute paths
*Merge every n number of frames
'''

def _redraw_yasiamevil(): # taken from Campbell's Cell Fracture addon. This black magic works.
    _redraw_yasiamevil.opr(**_redraw_yasiamevil.arg)
_redraw_yasiamevil.opr = bpy.ops.wm.redraw_timer
_redraw_yasiamevil.arg = dict(type='DRAW_WIN_SWAP', iterations=1)
   
class RenderAnimProg(bpy.types.Operator):
    """Render the Animation multiple times with a different seed each time"""
    bl_idname = "progressive.render_anim"
    bl_label = "Progressive Animation"
    animation=bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine=='CYCLES'

    def execute(self, context):
        animation=self.animation
        usedseedlist=[]
        index=1
        scn=context.scene        
        original_seed=scn.cycles.seed 
        original_samples=scn.cycles.samples
        original_render_path=scn.render.filepath
        original_frame_current=scn.frame_current
        original_folder_struct=scn.ProgAnimFolderStruct
        scn.ProgAnimProgress="Starting Progressive Animation Render..."
        self.report({'INFO'}, scn.ProgAnimProgress)
        scn.ProgAnimFrameProgress=0
        scn.cycles.samples=scn.ProgAnimSamples
        i=1    
        if animation:
            range_start=scn.frame_start
            range_end=scn.frame_end+1
            numframes=((scn.frame_end-scn.frame_start+1)*scn.ProgAnimRepeats+1)
        else:
            range_start=scn.frame_current
            range_end=scn.frame_current+1
            numframes=scn.ProgAnimRepeats+1
            scn.ProgAnimFolderStruct='frames'
             
        for loop in range(0,scn.ProgAnimRepeats):
            for frame in range(range_start, range_end):                
                scn.frame_current=frame
                scn.render.filepath=original_render_path
                pathonly=""
                if scn.ProgAnimFolderStruct=='frames':
                    path=scn.render.filepath+sep+"frame_"+str(frame)+sep+"seed_"+str(scn.cycles.seed)
                    pathonly=scn.render.filepath+sep+"frame_"+str(frame)
                else:
                    path=scn.render.filepath+sep+"seed_set_"+str(index)+sep+"frame_"+str(frame)
                    pathonly=scn.render.filepath+sep+"seed_set_"+str(index)
                scn.render.filepath=path
                
                if not ospath.exists(pathonly):
                    makedirs(pathonly)
                
                numfilesindir=0
                for f in listdir(pathonly.replace(sep, "/")):
                    if ospath.isfile(pathonly.replace(sep, "/")+'/'+f) and (f.startswith("seed") or f.startswith("frame")):
                        numfilesindir+=1
                print (pathonly.replace(sep, "/")+" - "+str(numfilesindir))
                
                
                if (not ospath.exists (path+scn.render.file_extension) and numfilesindir<scn.ProgAnimRepeats) or scn.ProgAnimOverwrite:
                    if scn.ProgAnimSeedType=='incremental':
                        scn.cycles.seed=i
                    elif scn.ProgAnimSeedType=='random':
                        scn.cycles.seed=int(random()*1000000000)
                        while scn.cycles.seed in usedseedlist:          # ensure the same seed is never used twice... probably dangerous since it's physyically possible to render tonnes of frames a ton of times
                            scn.cycles.seed=int(random()*1000000000)
                        usedseedlist.append(scn.cycles.seed)
                        
                    scn.ProgAnimFrameProgress+=1
                    scn.ProgAnimProgress="Progress: ("+str(int(scn.ProgAnimFrameProgress/numframes*100))+"%) Rendering frame "+str(frame)+', seed '+str(index)
                    self.report({'INFO'}, scn.ProgAnimProgress)
                    _redraw_yasiamevil() # redraw window to show progress
                    
                    bpy.ops.render.render(write_still=True) # render image
                else:
                    scn.ProgAnimFrameProgress+=1
                    scn.ProgAnimProgress="Progress: ("+str(int(scn.ProgAnimFrameProgress/numframes*100))+"%) Skipping frame "+str(frame)+', seed '+str(index)
                    self.report({'INFO'}, scn.ProgAnimProgress)
                    _redraw_yasiamevil() # redraw window to show progress
                    
                i=i+1
            index+=1
        scn.render.filepath = original_render_path
        scn.cycles.seed = original_seed        
        scn.cycles.samples = original_samples
        scn.frame_current = original_frame_current
        scn.ProgAnimProgress="Idle"
        self.report({'INFO'}, "Progressive Render Complete!")
        if scn.ProgAnimMergeWhenDone:
            bpy.ops.progressive.merge_anim(animation=animation)
        if not animation:
            scn.ProgAnimFolderStruct=original_folder_struct
        return {'FINISHED'}
    
class MergeProgAnim(bpy.types.Operator):
    """Merge images of a progressively rendered animation"""
    bl_idname = "progressive.merge_anim"
    bl_label = "Merge Seeds"
    animation=bpy.props.BoolProperty()
        
    def execute(self, context):
        animation=self.animation
        scn=context.scene
        ext=scn.render.file_extension
        original_folder_struct=scn.ProgAnimFolderStruct
        if not animation:
            scn.ProgAnimFolderStruct='frames'
        
        scn.ProgAnimProgress="Merging images..."
        self.report({'INFO'}, scn.ProgAnimProgress)
        _redraw_yasiamevil() # redraw window to show progress
        
        if animation:
            range_start=scn.frame_start
            range_end=scn.frame_end+1
        else:
            range_start=scn.frame_current
            range_end=scn.frame_current+1
        
        if scn.ProgAnimFolderStruct=='seeds':
            for seedset in range (1,scn.ProgAnimRepeats+1):
                for frame in range(range_start, range_end):
                    if ospath.exists(scn.render.filepath+"/seed_set_"+str(seedset)+'/frame_'+str(frame)+ext):
                        if not ospath.exists(scn.render.filepath+"/temp_merge/frame_"+str(frame)):
                            makedirs(scn.render.filepath+"/temp_merge/frame_"+str(frame))
                        copyfile(scn.render.filepath+"/seed_set_"+str(seedset)+'/frame_'+str(frame)+ext, scn.render.filepath+"/temp_merge/frame_"+str(frame)+"/seed_set_"+str(seedset)+ext)
        
        # create merger script
        f = open(scn.render.filepath+sep+"merge.bat", 'w+')
        for frame in range(range_start, range_end):
            if scn.ProgAnimFolderStruct=='frames':
                f.write('convert "'+scn.render.filepath+sep+"frame_"+str(frame)+sep+'*'+ext+'" -evaluate-sequence mean "'+scn.render.filepath+str(frame)+scn.render.file_extension+'"\n')
            else:
                f.write('convert "'+scn.render.filepath+sep+"temp_merge"+sep+"frame_"+str(frame)+sep+'*'+ext+'" -evaluate-sequence mean "'+scn.render.filepath+str(frame)+scn.render.file_extension+'"\n')
        f.close()
        chmod(scn.render.filepath+sep+"merge.bat", stat.S_IRWXU) #make sure the script is executable
        
        m=system(scn.render.filepath+sep+"merge.bat") # run merger script, returns 0 if successful and 1 if not (i.e. if imagemagick is not installed or something is wrong with the path)
        if m==0:
            scn.ProgAnimImageMagickError=False
                
            remove(scn.render.filepath+sep+"merge.bat")
            if scn.ProgAnimFolderStruct=='seeds':
                rmtree(scn.render.filepath+"/temp_merge")
            if scn.ProgAnimDeleteSeeds:
                rmtree(scn.render.filepath)
                
            scn.ProgAnimProgress="Idle"
            self.report({'INFO'}, "Finished!")
        else:
            scn.ProgAnimProgress="Idle"
            scn.ProgAnimImageMagickError=True
            self.report({'ERROR'}, "Could not merge images! ImageMagick may not be installed properly or the path is invalid")
        
        if not animation:
            scn.ProgAnimFolderStruct=original_folder_struct
        return {'FINISHED'}
    
    
class RENDER_PT_progressive_render(bpy.types.Panel):
    bl_label = "Progressive Render"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine=='CYCLES'

    def draw(self, context):
        layout=self.layout
        scene=context.scene

        col=layout.column(align=False)
        row=col.row(align=True)
        row.prop(scene, "ProgAnimRepeats")
        row.prop(scene, "ProgAnimSamples")
        col.prop(scene.render, "filepath", text="Output Path")
        row=col.row(align=True)
        row.prop(scene, "ProgAnimFolderStruct", text="Folder Layout")
        row.operator("wm.url_open", text="", icon="QUESTION").url="http://adaptivesamples.wordpress.com/2013/07/22/progressive-animation-render-addon-and-image-stacking/"
        col.prop(scene, "ProgAnimSeedType", text="Seed Variance")
        col.prop(scene, "ProgAnimOverwrite")
        box=layout.box()
        col=box.column(align=True)
        if scene.ProgAnimProgress == "Idle":
            col.label(text="    Info:")
            col.label(text="Total Samples per frame: "+str(scene.ProgAnimSamples*scene.ProgAnimRepeats))
            if scene.ProgAnimFolderStruct=='frames':
                col.label(text="Seed Path: "+scene.render.filepath+sep+'frame_'+str(scene.frame_start)+sep+'seed_1'+scene.render.file_extension)
            else:
                col.label(text="Seed Path: "+scene.render.filepath+sep+'seed_set_1'+sep+'frame_'+str(scene.frame_start)+scene.render.file_extension)
            col.label(text="Final Path: "+scene.render.filepath+str(scene.frame_start)+scene.render.file_extension)
        else:
            col.label(text=scene.ProgAnimProgress)
            col.label(text="    To stop/cancel the render, kill the blender")
            col.label(text="    process or wait for it to finish")
        
        
        col=layout.column(align=True)
        col.prop(scene, "ProgAnimMergeWhenDone")
        col.prop(scene, "ProgAnimDeleteSeeds")
        row=col.row(align=True)
        row.operator("progressive.render_anim", icon="RENDER_STILL", text="Progressive Render").animation=False
        row.operator("progressive.render_anim", icon="RENDER_ANIMATION").animation=True
        row=col.row(align=True)
        row.operator("progressive.merge_anim", icon="IMAGE_ZDEPTH", text="Merge Seeds (frame)").animation=False
        row.operator("progressive.merge_anim", icon="IMAGE_ZDEPTH", text="Merge Seeds (anim)").animation=True
        
        if scene.ProgAnimImageMagickError:
            box=layout.box()
            col=box.column(align=True)
            col.label(text="Warning!", icon="ERROR")
            col.label(text="    ImageMagick might not be installed correctly!")
            col.separator()
            col.label(text="ImageMagick is an external program used to merge")
            row=col.row()
            row.label(text="the images together")
            row.operator("wm.url_open", text="Why you need this", icon="URL").url="http://adaptivesamples.wordpress.com/install-imagemagick/"
            col.separator()
            # http://adaptivesamples.wordpress.com/install-imagemagick/
            # http://www.imagemagick.org/script/binary-releases.php
            col.operator("wm.url_open", text="Download ImageMagick", icon="URL").url="http://www.imagemagick.org/script/binary-releases.php"
            col.operator("wm.url_open", text="How to install ImageMagick properly", icon="URL").url="http://adaptivesamples.wordpress.com/install-imagemagick/"
    
def register():

    bpy.types.Scene.ProgAnimRepeats = bpy.props.IntProperty(
            name="Repeats",
            default=5,
            min=2,
            description="The number of times to render the whole animation with different seeds")
    bpy.types.Scene.ProgAnimProgress = bpy.props.StringProperty(
            name="Progress",
            default='Idle',
            description="Progress of Render")
    bpy.types.Scene.ProgAnimFrameProgress = bpy.props.IntProperty(
            name="FrameProgress",
            default=0,
            description="Frame progress")
    bpy.types.Scene.ProgAnimMergeWhenDone = bpy.props.BoolProperty(
            name="Merge on Completion",
            default=True,
            description="When the animation finishes rendering, merge the seeds together. Cancelling the render will cancel this too.")
    bpy.types.Scene.ProgAnimDeleteSeeds = bpy.props.BoolProperty(
            name="Delete Seeds",
            default=True,
            description="Delete the seeds after merging them")
    bpy.types.Scene.ProgAnimSamples = bpy.props.IntProperty(
            name="Samples per seed",
            default=100,
            min=1,
            description="The number of samples to render for each image")
    bpy.types.Scene.ProgAnimImageMagickError = bpy.props.BoolProperty(
            name="Nothingtoseeherefolks",
            default=False,
            description="doobydoobydoobydobayeh")
    bpy.types.Scene.ProgAnimSeedType = bpy.props.EnumProperty(
            name="Seeds",
            items=(("incremental","Incremental","Increase the seed for every image"),("random","Random","Use a random seed (between 0 and 1000000000)")),
            default='random',
            description="How to vary the seed for each render")
    bpy.types.Scene.ProgAnimFolderStruct = bpy.props.EnumProperty(
            name="Folder Structure",
            items=(("frames","Frames","Have a folder for each frame (eg: /frame_15/seed_5.jpg)"),("seeds","Seeds","Have a folder for each seed (eg: /seed_5/frame_15.jpg)")),
            default='seeds',
            description="The folder layout (folders for frames or folders for seed sets)")
    bpy.types.Scene.ProgAnimOverwrite = bpy.props.BoolProperty(
            name="Overwrite",
            default=False,
            description="Rerender frames that have already been rendered (i.e: if the image file exists, or there are enough seeds for that frame)")

    bpy.utils.register_module(__name__)


def unregister():
    
    del bpy.types.Scene.ProgAnimRepeats
    del bpy.types.Scene.ProgAnimProgress
    del bpy.types.Scene.ProgAnimFrameProgress
    del bpy.types.Scene.ProgAnimMergeWhenDone
    del bpy.types.Scene.ProgAnimDeleteSeeds
    del bpy.types.Scene.ProgAnimSamples
    del bpy.types.Scene.ProgAnimImageMagickError
    del bpy.types.Scene.ProgAnimSeedType
    del bpy.types.Scene.ProgAnimFolderStruct
    del bpy.types.Scene.ProgAnimOverwrite
    
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()