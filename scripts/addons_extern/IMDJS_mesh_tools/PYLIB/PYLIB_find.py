

import bpy,sys,os,imp,random



#////找///////////////////////////////////////////
def idΔΔ找id场景相同LIB(s要找名,i点数,s类型):
    id要找的=None;
    if(s类型=="MESH"):
        for id in bpy.data.meshes:
            #print("MESH NAME==",id.name,s网格名);
            if(id.name==s要找名):
                if(i点数==len(id.vertices)):
                    id要找的=id;
                    #print("FIND MESH==",id);
                    break;

    elif(s类型=="CURVE"):
        for id in bpy.data.curves:
            #print("MESH NAME==",id.name,s网格名);
            if(id.name==s要找名):
                s样条类型=id.splines[0].type;
                if(s样条类型=="BEZIER"):
                    i点数曲线=len(id.splines[0].bezier_points);
                else:
                    i点数曲线=len(id.splines[0].points);

                if(i点数==i点数曲线):
                    id要找的=id;
                    #print("FIND MESH==",id);
                    break;

    elif(s类型=="LATTICE"):
        for id in bpy.data.lattices:
            #print("MESH NAME==",id.name,s网格名);
            if(id.name==s要找名):
                if(i点数==len(id.points)):
                    id要找的=id;
                    #print("FIND MESH==",id);
                    break;

    elif(s类型=="ARMATURE"):
        for arm in bpy.data.armatures:
            if(arm.name==s要找名):
                if(i点数==len(arm.bones)):
                    id=arm;
                    #print("FIND MESH==",mesh);
                    break;

    elif(s类型=="CAMERA"):
        for cam in bpy.data.cameras:
            if(cam.name==s要找名):
                #if(i点数==len(arm.bones)):
                    id=cam;
                    #print("FIND MESH==",mesh);
                    break;

    elif(s类型=="FONT"):
        for f in bpy.data.fonts:
            if(f.body==s要找名):
                id=f;
                #print("FIND MESH==",mesh);
                break;

    return id要找的;

#==============================================================
def oΔΔ找物按名LIB(D字典,s属性键,s类型): #接受方必须是个物体
    if(s属性键 not in D字典.keys()):
        print("NO KEY",s属性键);
        return None;
    try:
        if(s类型=="OBJECT"):
            return bpy.data.objects[ D字典[s属性键]];
        if(s类型=="ARMATURE"):
            return bpy.data.armatures[ D字典[s属性键]];
        elif(s类型=="CURVE"):
            return bpy.data.curves[ D字典[s属性键]];
        elif(s类型=="GROUP"):
            return bpy.data.groups[ D字典[s属性键]];
        elif(s类型=="IMAGE"):
            return bpy.data.images[ D字典[s属性键]];
        elif(s类型=="LAMP"):
            return bpy.data.lamps[ D字典[s属性键]];
        elif(s类型=="LATTICE"):
            return bpy.data.lattices[ D字典[s属性键]];
        elif(s类型=="MATERIAL"):
            return bpy.data.materials[ D字典[s属性键]];
        elif(s类型=="MESH"):
            return bpy.data.meshes[ D字典[s属性键]];
        elif(s类型=="PARTICLE"):
            return bpy.data.particles[ D字典[s属性键]];
        elif(s类型=="TEXTURE"):
            return bpy.data.textures[ D字典[s属性键]];
            #print("FIND TEX", bpy.data.textures[ D字典[s属性键]],接受方);
        elif(s类型=="NODETREE"):
            return bpy.data.nodegroups[ D字典[s属性键]];
        elif(s类型=="ACTION"):
            return bpy.data.actions[ D字典[s属性键]];
        elif(s类型=="TEXT"):
            return bpy.data.texts[ D字典[s属性键]];
        elif(s类型=="CAMERA"):
            return bpy.data.cameras[ D字典[s属性键]];
        elif(s类型=="SOUND"):
            return bpy.data.sounds[ D字典[s属性键]];

        #return True;
    except:
        return None;
        print("FIND NO OBJ",);

#==============================================================
def bΔΔ找物按名给左接受方(接受方,D字典,s类型):
    try:
        if(s类型=="OBJECT"):
            接受方= bpy.data.objects[ D字典];
        elif(s类型=="ARMATURE"):
            接受方= bpy.data.armatures[ D字典];
        elif(s类型=="CURVE"):
            接受方= bpy.data.curves[ D字典];
        elif(s类型=="GROUP"):
            接受方= bpy.data.groups[ D字典];
        elif(s类型=="IMAGE"):
            接受方= bpy.data.images[ D字典];
        elif(s类型=="LAMP"):
            接受方= bpy.data.lamps[ D字典];
        elif(s类型=="MATERIAL"):
            接受方= bpy.data.materials[ D字典];
        elif(s类型=="MESH"):
            接受方= bpy.data.meshes[ D字典];
        elif(s类型=="PARTICLE"):
            接受方= bpy.data.particles[ D字典];
        elif(s类型=="TEXTURE"):
            接受方= bpy.data.textures[ D字典];
        elif(s类型=="NODETREE"):
            接受方= bpy.data.nodegroups[ D字典];
        return True;
    except:return False;

#==============================================================
def nΔΔ找节点LIB(self,context,event,s节点树类型,s节点类型):
    region=context.region;v2d=region.view2d;
    f2鼠屏位=(event.mouse_region_x,event.mouse_region_y);
    space=context.space_data;
    bpy.context.space_data.tree_type =s节点树类型;
    for nt in bpy.data.node_groups:
        if(nt.bl_idname==s节点树类型):
            space.node_tree=nt;#激活IMDJS_NodeTree
            #nt.tag=True;
            print("TAG==",nt.tag);
            for n in nt.nodes:
                print("NODE ID NAME==",n.bl_idname,s节点类型);
                if (n.bl_idname == s节点类型):#如果是群组节点
                    v2节位=n.location;
                    #f宽=n.width;f高=n.height;
                    #f宽小=n.bl_width_min;f高小=n.bl_height_min;
                    #f宽=n.bl_width_max;f高=n.bl_height_max;
                    v2宽高=n.dimensions;
                    #print("NODE MAX MIN==",f宽小,f宽,f高小,f高,n.bl_height_default,n.bl_width_default,n.width,n.height);
                    f2节屏位左上=v2d.view_to_region(v2节位.x, v2节位.y, clip=True);
                    f2节屏位右下=v2d.view_to_region(v2节位.x+v2宽高.x, v2节位.y-v2宽高.y, clip=True);
                    #print("NODE width height==",f2节屏位左上,f2节屏位右下,);print("F2 MOUSE==",f2鼠屏位);
                    if(f2鼠屏位[0]>=f2节屏位左上[0] and f2鼠屏位[0]<=f2节屏位右下[0]):
                        if(f2鼠屏位[1]>=f2节屏位右下[1] and f2鼠屏位[1]<=f2节屏位左上[1]):
                            print("FIND NODE==",n.name);
                            return n;
                    #break;


