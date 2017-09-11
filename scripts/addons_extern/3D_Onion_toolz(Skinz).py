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
#
#
#  Author: bossco ( aka DeepPurple72 )
#
#  Update: Aug/2017
#
#  tested with:
#  Blender 2.78c 
#  
# *****************************************************************************
#


bl_info = {
    'name': "3D Onion Skin Toolz (Blender 2.78c/2.79)",
    'author': "BOSSCO (DeepPurple72)",
    'version': (2, 0, 5),
    'blender': (2, 7, 8),
    'api': 44136,
    'location': "Addon appears in Render Properites tab",
    'description': "3D Onion Skinning Toolz for Blender Animations",
    'warning': "BETA VERSION", 
    'wiki_url': "",
    'tracker_url': "",
    'category': "Render"}



import bpy
import mathutils
from math import *
from bpy.props import *
from bpy.types import Menu, Panel

# active_obj = ""
#
# GUI (Panel)
#
class OBJECT_PT_onion_toolz(bpy.types.Panel):

    bl_label = "3D Onion Toolz addon (Beta1)"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_icon = "IMAGE_RGB_ALPHA"


#    bl_idname = "onion_toolz"
#    bl_description = "3D Onion Toolz (Skinning)"
#    bl_options = {'REGISTER', 'UNREGISTER'}
    #
    # ADD-ON will show up under CAMERA PROPERTIES
    # and only if a camera is selected


    # show this add-on only in the RENDER properties
    # and only if selected OBJECT is a MESH or ARMATURE

    @classmethod
    def poll(self, context):
        #active_obj=""
        if (context.active_object.type  == 'MESH') or (context.active_object.type  == 'ARMATURE'):
            active_obj = context.active_object
            return context.active_object

    #
    # Add some custom properties for OBJECT
    #
    bpy.types.Object.is_otoolz = bpy.props.BoolProperty(
        attr="is_otoolz",
        name='is_ottolz',
        description='Is OBJECT using 3D Onion Toolz',
       default=False) 

    bpy.types.Scene.otoolz_arm = bpy.props.BoolProperty(
        attr="otoolz_arm",
        name='otoolz_arm',
        description='Armature: Use Mesh(es) for Skinz?',
       default=False) 

    bpy.types.Scene.otoolz_wire = bpy.props.BoolProperty(
        attr="otoolz_wire",
        name='otoolz_wire',
        description='Mesh: Use Wireframe too',
       default=False) 

    bpy.types.Scene.otoolz_silh = bpy.props.BoolProperty(
        attr="otoolz_silh",
        name='otoolz_silh',
        description='Use Silhouettes? (No=Use original Materials)',
       default=True) 
   
    bpy.types.Scene.otoolz_fr_start = bpy.props.IntProperty(
        attr="otoolz_fr_start",
        name="otoolz_frames", 
        description='Start @ FRAME#', 
        min=0, soft_min=0, max=10000, soft_max=10000, default=0) 

    bpy.types.Scene.otoolz_fr_end = bpy.props.IntProperty(
        attr="otoolz_fr_end",
        name="otoolz_fr_end", 
        description='End @ FRAME#', 
        min=0, soft_min=0, max=10000, soft_max=10000, default=0)   

    bpy.types.Scene.otoolz_fr_sc = bpy.props.BoolProperty(
        attr="otoolz_fr_sc",
        name='otoolz_fr_sc',
        description='Use Scene START/END Frames?',
       default=True) 
 
    bpy.types.Scene.otoolz_skip = bpy.props.IntProperty(
        attr="otoolz_skip",
        name="otoolz_frames", 
        description='Frames to skip', 
        min=0, soft_min=0, max=100, soft_max=100, default=20) 

    bpy.types.Scene.otoolz_color_a = bpy.props.FloatProperty(
        attr="otoolz_color_a",
        name="otoolz_color_a", 
        description='ALPHA (0-255)', 
        min=0, soft_min=0, max=1, soft_max=1, default=1)

    bpy.types.Scene.otoolz_color_b = bpy.props.FloatProperty(
        attr="otoolz_color_b",
        name="otoolz_color_b", 
        description='ALPHA (0-255)', 
        min=0, soft_min=0, max=1, soft_max=1, default=1)

    bpy.types.Scene.otoolz_dec = bpy.props.IntProperty(
        attr="otoolz_dec",
        name="otoolz_dec", 
        description='Decimate Meshes (0=NONE, or 1 to 8 iterations', 
        min=0, soft_min=0, max=8, soft_max=8, default=0) 

    def __init(self):
        objx = bpy.context.selected_objects[0]
        scenex = bpy.context.scene

        scenex.otoolz_fr_start = bpy.context.scene.frame_start
        scenex.otoolz_fr_end = bpy.context.scene.frame_end

        try:
            if (scenex.otoolz_fr_start<1):
                scenex.otoolz_fr_start = bpy.context.scene.frame_start
                scenex.otoolz_fr_end = bpy.context.scene.frame_end
        except:
            pass

    # Code to display the ADDON's PANEL (gui)


    def draw(self, context):
        layout = self.layout

        obj1 = bpy.context.selected_objects[0]
        sc=bpy.context.scene
        otoolz = obj1.is_otoolz
        try:
            mat1 = bpy.data.materials["onion_toolz_Skinz_a"]
            mat2 = bpy.data.materials["onion_toolz_Skinz_b"]
        except:
            pass

        try:
            row = layout.row()
            row.prop(mat1, "diffuse_color", text="Skinz Color A")
            row.prop(mat1, "alpha", text="A:")
            row = layout.row()
            row.prop(mat2, "diffuse_color", text="Skinz Color B")
            row.prop(mat2, "alpha", text="A:")

            row = layout.row()
        except:
            pass



        # find children 
        ch=0
        try:
            for ob in obj1.parent.children:
                if (ob.type=="MESH"):
                    ch=ch+1
        except:
            pass  


        row = layout.row()
        if (obj1.parent):
            row.label(icon='ERROR', text="* WILL USE PARENT: "+str(obj1.parent.type)+" : "+str(obj1.parent.name))
            row = layout.row()
        else:
            if (obj1.is_otoolz==True):
                row.label(icon='NONE', text=str(obj1.type)+" Selected = "+str(obj1.name))
                row = layout.row()
            else:
                row.label(icon='NONE', text=str(obj1.type)+" Selected = "+str(obj1.name))

        # check is mesh / armature has any actions assigned
        acts=1
        try:
            x = bpy.data.objects[obj1.name].animation_data.action
        except:
            # No actions detected
            acts=0
            pass

        #IF MESH IS SELECTED, CHECK PARENT FOR ANIM DATA
        try:
            if (acts<1) and (obj1.parent.animation_data.action):
                acts=1
        except:
            pass
  
        
        if (ch>0):
            row = layout.row()  
            row.label(icon="NONE", text=obj1.parent.type+" has "+str(ch)+" Skinnable Meshes")
            row = layout.row()
    
        if (acts<1):
            row = layout.row()
            row.label(icon="CANCEL", text="No animation data:")
            row = layout.row()
            row.label(text="Add an Action or Select another object")
        else:
            row = layout.row()
            row.label(icon='OUTLINER_OB_ARMATURE', text="animation detected")

        if(acts>0) and (otoolz<1):
            #row = layout.row()
            row.label(icon="CANCEL", text="Not using Skinz.")
        if(acts>0) and (otoolz>0):
            #row = layout.row()
            row.label(icon='OUTLINER_OB_ARMATURE', text="Using Skinz.")       
        try:
            if(acts>0):
                #row = layout.row()
                #row.label(text="***  SKINz Options ***")
                row = layout.row()
                #if (obj1.type=="ARMATURE"):
                #    row.prop(obj1, "otoolz_arm", text="Use Armature's Meshes?")                

                col = layout.column(align=True)
                row = layout.row()
                split = layout.split()

                row.prop(sc,"otoolz_dec", text="Decimate Skinz ")
                row = layout.row()

                row.label(icon="NONE", text="FRAMES SETTINGS:")
                row = layout.row()
                row.prop(sc, "otoolz_fr_sc", text="Use Scene's START/END Frames?")
                #row.label(icon='NONE', text="FRAMES:")
                col = layout.column(align=True)
                split = layout.split()
                row = layout.row()


                if (sc.otoolz_fr_sc>0):
                    row.prop(sc, "otoolz_skip", text="Skip Frame count")
                    row = layout.row()
                    row.label(icon="NONE", text ="(AUTO) USING SCENE ("+str(bpy.context.scene.frame_start)+"-"+str(bpy.context.scene.frame_end)+")")
                else:
                    row.label(icon="NONE", text ="* USING MANUAL MODE: Selected Above")

                    row = layout.row()
                    row = split.row(align=True)
                    row.prop(sc, "otoolz_fr_start", text="Start")
                    row.prop(sc, "otoolz_fr_end", text="End")
                    row.prop(sc, "otoolz_skip", text="Skip")
                row = layout.row()
        except:
            pass

        row.prop(sc, "otoolz_silh", text ="Use Silhouettes?")
        row.prop(sc, "otoolz_wire", text ="Add Wire?")

        # display stuff if obj has anim, but not using otoolz yet (ie... CREATE new skinz)
        if(acts>0) and (otoolz<1):
            row = layout.row()
            row.operator('onion_toolz.op1')
        # display stuff if obj has anim, and is using otoolz ( ie... UPDATE or DELETE Skinz )
        if(acts>0) and (otoolz>0):
            row = layout.row()
            row.operator('onion_toolz.op2') # UPDATE SKINz
            row.operator('onion_toolz.op3')  # REMOVE/DELETE SKINz

        


### End of PANEL UI code

##############################################################################

#
# Operator - Template
#
class OBJECT_OT_op1(bpy.types.Operator):
    bl_label = 'Apply 3D Onion Toolz Skinz'
    bl_idname = 'onion_toolz.op1'
    bl_description = "Apply 3D ONION TOOLz Skinz to this object"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

    # SETUP a Special 'empty' to use as a parent for SKINz
        obj1 = bpy.context.selected_objects[0]
        sc = bpy.context.scene

        try:
            x = bpy.data.objects["3D_Onion_Toolz"]
        except:
            #x = bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0))
            bpy.ops.object.add(type="EMPTY")
            x = bpy.context.selected_objects[0]
            x.name="3D_Onion_Toolz"
            x.hide=1
            x.hide_render=1
            x.hide_select=1
            x.select=0

       # Setup the MATERIALS for SKINz ( BEFORE current frame Color )
        try:
            x = bpy.data.materials["onion_toolz_Skinz_a"]
            x.use_transparency = 1
            x.alpha = sc.otoolz_color_a*255
        except:
            bpy.data.materials.new("onion_toolz_Skinz_a")
            x = bpy.data.materials["onion_toolz_Skinz_a"]
            x = bpy.data.materials["onion_toolz_Skinz_a"]
            x.use_transparency = 1
            x.alpha = sc.otoolz_color_a*255
            x.diffuse_color = (255,0,0)
            x.use_shadeless = 1

       # Setup the MATERIALS for SKINz ( ATFER current frame Color )
        try:
            x = bpy.data.materials["onion_toolz_Skinz_b"]
            x.use_transparency = 1
            x.alpha = sc.otoolz_color_a*255
        except:
            bpy.data.materials.new("onion_toolz_Skinz_b")
            x = bpy.data.materials["onion_toolz_Skinz_b"]
            x = bpy.data.materials["onion_toolz_Skinz_b"]
            x.use_transparency = 1
            x.alpha = sc.otoolz_color_a*255
            x.diffuse_color = (0,255,0)
            x.use_shadeless = 1

#########################################################################3

      ###############################   
      ### Code to create SKINz ######
      ###############################

        # Check to see if object is a parent or a child
        is_par=0
        # children count
        ch=0
 
        obj2=obj1.parent
        try:
            tst=obj2.name
            is_par=1
            # find children 
            try:
                for ob in obj1.parent.children:
                    if (ob.type=="MESH"):
                        ch=ch+1
            except:
                pass  


        except:
            obj2=obj1

            #obj2.otoolz_silh=obj1.otoolz_silh
            #obj2.otoolz_wire=obj1.otoolz_wire
            #obj2.otoolz_skip=obj1.otoolz_skip
            #obj2.otoolz_fr_sc=obj1.otoolz_fr_sc
            #obj2.otoolz_fr_start=obj1.otoolz_fr_start
            #obj2.otoolz_fr_end=obj1.otoolz_fr_end

        # Create an EMPTY using ottolz + Parent object's name
        try:
            x = bpy.data.objects["otoolz_" + obj2.name]
        except:
            #x = bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0))
            bpy.ops.object.add(type="EMPTY")
            x = bpy.context.selected_objects[0]
            x.name="otoolz_" + obj2.name
            x.hide=1
            x.hide_render=1
            x.hide_select=1
            x.select=0
            # make the EMPTY a child of the main empty "3D_Onion_Toolz"
            x.parent=bpy.data.objects["3D_Onion_Toolz"]

        # EMPTY to use as a PARENT for skinz
        emp1=bpy.data.objects["otoolz_" + obj2.name]

        # Skinz count
        sk=1

        # de-select main object before routine
        obj1.select=0

        # Range of FRAMES to skin
        fs=sc.otoolz_fr_start
        fe=sc.otoolz_fr_end
        skip=sc.otoolz_skip
        # use scene's frame range?
        if (sc.otoolz_fr_sc>0):
            fs=bpy.context.scene.frame_start
            fe=bpy.context.scene.frame_end         
        # fix start & end if entered wrong
        if (fe<fs):
            a=fs
            fs=fe
            fe=a
        #if (fs+sk<fe):
        #    fe=fs+sk

        scene=bpy.context.scene
        curframe=scene.frame_current
        silh=scene.otoolz_silh

        # start at frame start (fs)
        frame1=fs

        lp=int((fe-fs)/skip)+3

        print ("FS= "+str(fs)+" , FE= "+str(fe)+" , LOOP= "+str(lp))

        for zz in range(lp):
            frame1=fs+((zz-1)*skip)
            #bpy.context.scene.frame_current=frame1
            bpy.context.scene.frame_set(frame1)
            print("otoolz FRAME "+str(frame1))
            #frame1=frame1+sk 
            #bpy.context.scene.update()

            # Create SKINz Part 1 ( Duplicate Meshes )

            # first do the parent
            obj2.select=1      
            # Duplicate Meshes
            if (obj2.type=="MESH"):
                bpy.ops.object.duplicate()
                #obj1.select=0
                obj2.select=0
                skinz = bpy.context.selected_objects[0]
                # make skin a child of the EMPTY
                skinz.parent=emp1
                skinz.animation_data_clear()
                # apply silouettes
                if (silh>0):
                    try:
                        if (frame1<curframe):
                            skinz.data.materials[0]=bpy.data.materials["onion_toolz_Skinz_a"]
                        else:
                            skinz.data.materials[0]=bpy.data.materials["onion_toolz_Skinz_b"]
                        skinz.draw_type="SOLID"
                        skinz.show_transparent=1
                        skinz.hide_select=1
                        skinz.hide_render=1
                    except:
                        pass
                 # apply wireframe
                if (scene.otoolz_wire>0):
                    skinz.show_wire=1



               # Apply Modifiers
                print("Shapekeys from "+str(bpy.context.scene.objects.active))
                # Remove SHAPE KEYS before ARMATURE modifier can be applied
                try:
                    bpy.context.scene.objects.active=skinz
                    bpy.ops.object.shape_key_remove(all=True)
                    print("otoolz: Shape Keys removed for ARMATURE modifier")
                except:
                    pass
                # Apply ALL ARMATURE modifiers to SKINz
                #bpy.context.scene.objects.active=skinz
                bpy.ops.object.modifier_apply(modifier="ARMATURE")
                # Decimate (simplify) Meshes ( for performance)     
                if (scene.otoolz_dec>0):    
                    t=skinz.modifiers.new("DECIMATE", type="DECIMATE")
                    t.decimate_type="UNSUBDIV"
                    t.iterations=scene.otoolz_dec   
                    bpy.ops.object.modifier_apply(modifier="DECIMATE")

            #  de-select skinz
                skinz.select=0
                sk=sk+1
            obj2.select=0
  
            w=scene.otoolz_wire
            silh=scene.otoolz_silh
            # do children ( if they exists )
            try:
                for ob in obj2.children:
                    if (ob.type=="MESH"):
                        ob.select=1
                        # Duplicate Meshes
                        bpy.ops.object.duplicate()
                        skinz = bpy.context.selected_objects[0]
                        # make skin a child of the EMPTY
                        skinz.parent=emp1
                        skinz.hide_render=1
                        skinz.hide_select=1
                        # add wireframe
                        if (w>0):
                            skinz.show_wire=1
                # apply silouettes
                        if (silh>0):
                            print("otoolz-- silh")
                            try:
                                if (frame1 < curframe):
                                    skinz.data.materials[0]=bpy.data.materials["onion_toolz_Skinz_a"]
                                else:
                                    skinz.data.materials[0]=bpy.data.materials["onion_toolz_Skinz_b"]
                                skinz.draw_type="SOLID"
                                skinz.show_transparent=1
                            except:
                                pass

               # Apply Modifiers
                        print("Shapekeys from "+str(bpy.context.scene.objects.active))
                # Remove SHAPE KEYS before ARMATURE modifier can be applied
                        try:                    
                            for k in skinz.data.shape_keys.key_blocks:
                                skinz.shape_key_remove(k)
                        except:
                            pass

                        #bpy.context.scene.objects.active=skinz
                        #bpy.ops.object.shape_key_remove(all=True)

                        print("otoolz: Shape Keys removed for ARMATURE modifier")

                # Apply ALL ARMATURE modifiers to SKINz
                #bpy.context.scene.objects.active=skinz
                        try:
                            bpy.context.scene.objects.active=skinz
                            bpy.ops.object.modifier_apply(modifier="ARMATURE")
                        except:
                            pass
                # Decimate (simplify) Meshes ( for performance)     
                        if (scene.otoolz_dec>0):    
                            t=skinz.modifiers.new("DECIMATE", type="DECIMATE")
                            t.decimate_type="UNSUBDIV"
                            t.iterations=scene.otoolz_dec   
                            bpy.ops.object.modifier_apply(modifier="DECIMATE")


                    #  de-select skinz
                        skinz.select=0
                        # Increment skinz count
                        sk=sk+1
            except:
                pass


      # Make the Original Selected Mesh/Armature Active again
        # since bpy.ops changes the context (ie. active object)
        bpy.context.scene.frame_set(curframe)
        obj1.select=1
        bpy.context.scene.objects.active=obj1
        # set object custom property ( ie... Object is using Onion Toolz)
        obj1.is_otoolz = 1


        #update scene & objects
        bpy.data.objects.update
        bpy.data.scenes.update
       
        
        msg = "3D ONION TOOLZ Skinz (Applied to Selected Object)"
        self.report( { 'INFO' }, msg  )

        return {'FINISHED'}

##############################################################################

class OBJECT_OT_op2(bpy.types.Operator):
    bl_label = 'UPDATE 3D Onion Toolz Skinz'
    bl_idname = 'onion_toolz.op2'
    bl_description = "Update 3D ONION TOOLz Skinz to this object"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):


        obj1 = bpy.context.selected_objects[0]

      ###############################   
      ### Code to REMOVE SKINz #####
      ###############################

 
        obj2=obj1.parent
        try:
            tst=obj2.name
            is_par=1
        except:
            obj2=obj1
        try:
            tree=bpy.data.objects["otoolz_"+obj2.name]
            print("otoolz: Delete Tree = "+str(tree.name))
            print (str(tree.children))
        except:
            pass

        try:
            #bpy.ops.outliner.object_operation(type="DELETE_HIERARCHY")
            chx=0
            for x in tree.children:
                #bpy.objects.remove(childn.name, do_unlink=True)
                print("Otoolz: Removed SKIN for "+str(x.name))
                bpy.data.objects.remove(tree.children[0], True)
                #bpy.data.objects.remove(tree.children[chx], True)
                #bpy.data.objects.update()
                #bpy.context.scene.update()

                #bpy.objects.remove(tree.children[x], do_unlink=True)
                chx=chx+1
                print("Otoolz: Removed SKIN for "+str(x.name))
        except:
            pass
        try:
            bpy.objects.remove(tree, True)
        except:
            pass
        bpy.context.scene.objects.update()
        bpy.context.scene.update()
        bpy.data.screens.update()


    # SETUP a Special 'empty' to use as a parent for SKINz
        obj1 = bpy.context.selected_objects[0]
        sc = bpy.context.scene

        try:
            x = bpy.data.objects["3D_Onion_Toolz"]
        except:
            #x = bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0))
            bpy.ops.object.add(type="EMPTY")
            x = bpy.context.selected_objects[0]
            x.name="3D_Onion_Toolz"
            x.hide=1
            x.hide_render=1
            x.hide_select=1
            x.select=0

       # Setup the MATERIALS for SKINz ( BEFORE current frame Color )
        try:
            x = bpy.data.materials["onion_toolz_Skinz_a"]
            x.use_transparency = 1
            x.alpha = sc.otoolz_color_a*255
        except:
            bpy.data.materials.new("onion_toolz_Skinz_a")
            x = bpy.data.materials["onion_toolz_Skinz_a"]
            x = bpy.data.materials["onion_toolz_Skinz_a"]
            x.use_transparency = 1
            x.alpha = sc.otoolz_color_a*255
            x.diffuse_color = (255,0,0)
            x.use_shadeless = 1

       # Setup the MATERIALS for SKINz ( ATFER current frame Color )
        try:
            x = bpy.data.materials["onion_toolz_Skinz_b"]
            x.use_transparency = 1
            x.alpha = sc.otoolz_color_a*255
        except:
            bpy.data.materials.new("onion_toolz_Skinz_b")
            x = bpy.data.materials["onion_toolz_Skinz_b"]
            x = bpy.data.materials["onion_toolz_Skinz_b"]
            x.use_transparency = 1
            x.alpha = sc.otoolz_color_a*255
            x.diffuse_color = (0,255,0)
            x.use_shadeless = 1

#########################################################################3

      ###############################   
      ### Code to create SKINz ######
      ###############################

        # Check to see if object is a parent or a child
        is_par=0
        # children count
        ch=0
 
        obj2=obj1.parent
        try:
            tst=obj2.name
            is_par=1
            # find children 
            try:
                for ob in obj1.parent.children:
                    if (ob.type=="MESH"):
                        ch=ch+1
            except:
                pass  


        except:
            obj2=obj1

            #obj2.otoolz_silh=obj1.otoolz_silh
            #obj2.otoolz_wire=obj1.otoolz_wire
            #obj2.otoolz_skip=obj1.otoolz_skip
            #obj2.otoolz_fr_sc=obj1.otoolz_fr_sc
            #obj2.otoolz_fr_start=obj1.otoolz_fr_start
            #obj2.otoolz_fr_end=obj1.otoolz_fr_end

        # Create an EMPTY using ottolz + Parent object's name
        try:
            x = bpy.data.objects["otoolz_" + obj2.name]
        except:
            #x = bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0))
            bpy.ops.object.add(type="EMPTY")
            x = bpy.context.selected_objects[0]
            x.name="otoolz_" + obj2.name
            x.hide=1
            x.hide_render=1
            x.hide_select=1
            x.select=0
            # make the EMPTY a child of the main empty "3D_Onion_Toolz"
            x.parent=bpy.data.objects["3D_Onion_Toolz"]

        # EMPTY to use as a PARENT for skinz
        emp1=bpy.data.objects["otoolz_" + obj2.name]

        # Skinz count
        sk=1

        # de-select main object before routine
        obj1.select=0

        # Range of FRAMES to skin
        fs=sc.otoolz_fr_start
        fe=sc.otoolz_fr_end
        skip=sc.otoolz_skip
        # use scene's frame range?
        if (sc.otoolz_fr_sc>0):
            fs=bpy.context.scene.frame_start
            fe=bpy.context.scene.frame_end         
        # fix start & end if entered wrong
        if (fe<fs):
            a=fs
            fs=fe
            fe=a
        #if (fs+sk<fe):
        #    fe=fs+sk

        scene=bpy.context.scene
        curframe=scene.frame_current
        silh=scene.otoolz_silh

        # start at frame start (fs)
        frame1=fs

        lp=int((fe-fs)/skip)+3

        print ("FS= "+str(fs)+" , FE= "+str(fe)+" , LOOP= "+str(lp))

        for zz in range(lp):
            frame1=fs+((zz-1)*skip)
            #bpy.context.scene.frame_current=frame1
            bpy.context.scene.frame_set(frame1)
            print("otoolz FRAME "+str(frame1))
            #frame1=frame1+sk 
            #bpy.context.scene.update()

            # Create SKINz Part 1 ( Duplicate Meshes )

            # first do the parent
            obj2.select=1      
            # Duplicate Meshes
            if (obj2.type=="MESH"):
                bpy.ops.object.duplicate()
                #obj1.select=0
                obj2.select=0
                skinz = bpy.context.selected_objects[0]
                # make skin a child of the EMPTY
                skinz.parent=emp1
                skinz.animation_data_clear()
                # apply silouettes
                if (silh>0):
                    try:
                        if (frame1<curframe):
                            skinz.data.materials[0]=bpy.data.materials["onion_toolz_Skinz_a"]
                        else:
                            skinz.data.materials[0]=bpy.data.materials["onion_toolz_Skinz_b"]
                        skinz.draw_type="SOLID"
                        skinz.show_transparent=1
                        skinz.hide_select=1
                        skinz.hide_render=1
                    except:
                        pass
                 # apply wireframe
                if (scene.otoolz_wire>0):
                    skinz.show_wire=1



               # Apply Modifiers
                print("Shapekeys from "+str(bpy.context.scene.objects.active))
                # Remove SHAPE KEYS before ARMATURE modifier can be applied
                try:
                    bpy.context.scene.objects.active=skinz
                    bpy.ops.object.shape_key_remove(all=True)
                    print("otoolz: Shape Keys removed for ARMATURE modifier")
                except:
                    pass
                # Apply ALL ARMATURE modifiers to SKINz
                #bpy.context.scene.objects.active=skinz
                bpy.ops.object.modifier_apply(modifier="ARMATURE")
                # Decimate (simplify) Meshes ( for performance)     
                if (scene.otoolz_dec>0):    
                    t=skinz.modifiers.new("DECIMATE", type="DECIMATE")
                    t.decimate_type="UNSUBDIV"
                    t.iterations=scene.otoolz_dec   
                    bpy.ops.object.modifier_apply(modifier="DECIMATE")

            #  de-select skinz
                skinz.select=0
                sk=sk+1
            obj2.select=0
  
            w=scene.otoolz_wire
            silh=scene.otoolz_silh
            # do children ( if they exists )
            try:
                for ob in obj2.children:
                    if (ob.type=="MESH"):
                        ob.select=1
                        # Duplicate Meshes
                        bpy.ops.object.duplicate()
                        skinz = bpy.context.selected_objects[0]
                        # make skin a child of the EMPTY
                        skinz.parent=emp1
                        skinz.hide_render=1
                        skinz.hide_select=1
                        # add wireframe
                        if (w>0):
                            skinz.show_wire=1
                # apply silouettes
                        if (silh>0):
                            print("otoolz-- silh")
                            try:
                                if (frame1 < curframe):
                                    skinz.data.materials[0]=bpy.data.materials["onion_toolz_Skinz_a"]
                                else:
                                    skinz.data.materials[0]=bpy.data.materials["onion_toolz_Skinz_b"]
                                skinz.draw_type="SOLID"
                                skinz.show_transparent=1
                            except:
                                pass

               # Apply Modifiers
                        print("Shapekeys from "+str(bpy.context.scene.objects.active))
                # Remove SHAPE KEYS before ARMATURE modifier can be applied
                        try:                    
                            for k in skinz.data.shape_keys.key_blocks:
                                skinz.shape_key_remove(k)
                        except:
                            pass

                        #bpy.context.scene.objects.active=skinz
                        #bpy.ops.object.shape_key_remove(all=True)

                        print("otoolz: Shape Keys removed for ARMATURE modifier")

                # Apply ALL ARMATURE modifiers to SKINz
                #bpy.context.scene.objects.active=skinz
                        try:
                            bpy.context.scene.objects.active=skinz
                            bpy.ops.object.modifier_apply(modifier="ARMATURE")
                # Decimate (simplify) Meshes ( for performance)     
                            if (scene.otoolz_dec > 0):    
                                t=skinz.modifiers.new("DECIMATE", type="DECIMATE")
                                t.decimate_type="UNSUBDIV"
                                t.iterations=scene.otoolz_dec   
                                bpy.ops.object.modifier_apply(modifier="DECIMATE")
         
                        except:
                            pass



                    #  de-select skinz
                        skinz.select=0
                        # Increment skinz count
                        sk=sk+1
            except:
                pass


      # Make the Original Selected Mesh/Armature Active again
        # since bpy.ops changes the context (ie. active object)
        bpy.context.scene.frame_set(curframe)
        obj1.select=1
        bpy.context.scene.objects.active=obj1
        # set object custom property ( ie... Object is using Onion Toolz)
        obj1.is_otoolz = 1


        #update scene & objects
        bpy.data.objects.update
        bpy.data.scenes.update
       
        
        msg = "3D ONION TOOLZ Skinz UPDATED"
        self.report( { 'INFO' }, msg  )

        return {'FINISHED'}

##############################################################################
class OBJECT_OT_op3(bpy.types.Operator):
    bl_label = 'Remove Skinz'
    bl_idname = 'onion_toolz.op3'
    bl_description = "Delete 3D ONION TOOLz Skinz (for selected Object)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj1 = bpy.context.selected_objects[0]

      ###############################   
      ### Code to REMOVE SKINz #####
      ###############################

 
        obj2=obj1.parent
        try:
            tst=obj2.name
            is_par=1
        except:
            obj2=obj1
        try:
            tree=bpy.data.objects["otoolz_"+obj2.name]
            print("otoolz: Delete Tree = "+str(tree.name))
            print (str(tree.children))
        except:
            pass

        try:
            #bpy.ops.outliner.object_operation(type="DELETE_HIERARCHY")
            chx=0
            for x in tree.children:
                #bpy.objects.remove(childn.name, do_unlink=True)
                print("Otoolz: Removed SKIN for "+str(x.name))
                bpy.data.objects.remove(tree.children[0], True)
                #bpy.data.objects.remove(tree.children[chx], True)
                #bpy.data.objects.update()
                #bpy.context.scene.update()

                #bpy.objects.remove(tree.children[x], do_unlink=True)
                chx=chx+1
                print("Otoolz: Removed SKIN for "+str(x.name))
        except:
            pass
        try:
            bpy.objects.remove(tree, True)
        except:
            pass
        bpy.context.scene.objects.update()
        bpy.context.scene.update()
        bpy.data.screens.update()
        bpy.context.scene.objects.active=obj1
        obj1.is_otoolz=0
        obj2.is_otoolz=0
        msg = "3D ONION TOOLZ Skinz Removed from Object"
        self.report( { 'INFO' }, msg  )

        return {'FINISHED'}

###############################################

bpy.utils.register_class(OBJECT_OT_op1)
#
# Register
#
def register():
    bpy.utils.register_module(__name__)
	
def unregister():
    bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
    register()
