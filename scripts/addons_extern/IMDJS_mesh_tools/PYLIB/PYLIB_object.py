
import bpy,sys,os,imp,random

from bpy.props import *
from mathutils import Matrix,Vector,Euler
from ctypes import*
from bpy_extras import object_utils
import bmesh
from math import*

#--------------------------------------------------------------------------
try:
    from .PYLIB_find import*
except:pass;    
try:
    from .PYLIB_attribute import*
except:pass;    


#////////////////////////////////////////////////
piΞ2=pi/2;
piΧ2=pi*2;

 #//////////////////////////////////////////////////
def oΔ建空物LIB(context,OBJECTPRESET):
    o=object_utils.object_data_add(context, None, operator=None).object;
    Δ字典赋予物体LIB(OBJECTPRESET,o,[]);
    return o;
#--------------------------------------------------------------------------
def oΔΔ建摄像机(context,OBJECTPRESET,id入):
    sID名=OBJECTPRESET["CAMERA_PROPERTY"].get("ID_NAME");
    id=None;
    if(id入):
        id=id入;
    else:
        id=idΔΔ找id场景相同LIB(s要找名=sID名,i点数=None,s类型="CAMERA");

    if(id==None):
        id = bpy.data.cameras.new(name=OBJECTPRESET["OBJECT_PROPERTY"]["name"]);
        Δ字典赋予物体LIB(OBJECTPRESET["CAMERA_PROPERTY"],id,[]);

    o=object_utils.object_data_add(context, id, operator=None).object;
    context.scene.camera=o;
    return o;

#--------------------------------------------------------------------------
def oΔΔ建晶格(context,OBJECTPRESET,s物名,id入):#最好保留s物名  参数 让其它用途可改名
    sID名=OBJECTPRESET["LATTICE_PROPERTY"].get("ID_NAME");
    i网点数=OBJECTPRESET["LATTICE_PROPERTY"].get("POINT_NUM");
    #----查找场景内的id-------------------------------------------------------
    id=None;
    if(id入):
        id=id入;
    else:
        id=idΔΔ找id场景相同LIB(s要找名=sID名,i点数=i网点数,s类型="LATTICE");
    #--------------------------------------------------------------------------
    if( id==None):
        id = bpy.data.lattices.new(name=s物名);#CURVE, SURFACE, FONT
        Δ字典赋予物体LIB(OBJECTPRESET["LATTICE_PROPERTY"],id,[]);
        Lp=id.points;
        for  i, D in  enumerate(OBJECTPRESET["LATTICE_PROPERTY"]["L_LATTICE_POINT"]):
            Δ字典赋予物体LIB(D,Lp[i],[])
    return object_utils.object_data_add(context, id, operator=None).object;
#--------------------------------------------------------------------------
def oΔΔ建灯光(context,OBJECTPRESET,s物名,id入):
    sID名=OBJECTPRESET["LAMP_PROPERTY"].get("ID_NAME");
    s类型=OBJECTPRESET["LAMP_PROPERTY"].get("LAMP_TYPE");
    if(id入):
        id=id入;
    else:
        id=None;
        for l in bpy.data.lamps:
            if(l.name==sID名):
                if(s类型==l.type):
                    id=l;
                    #print("FIND MESH==",mesh);
                    break;
    #--------------------------------------------------------------------------
    if(id==None):
        id = bpy.data.lamps.new(name=s物名,type=OBJECTPRESET["LAMP_PROPERTY"]["LAMP_TYPE"]);#POINT  SUN   SPOT  HEMI   AREA
        Δ字典赋予物体LIB(OBJECTPRESET["LAMP_PROPERTY"],id,[]);
    return object_utils.object_data_add(context, id, operator=None).object;

#--------------------------------------------------------------------------
def oΔΔ建骨架(context,OBJECTPRESET,s物名,id入):
    sID名=OBJECTPRESET["ARMATURE_PROPERTY"].get("ID_NAME");
    i骨数=OBJECTPRESET["ARMATURE_PROPERTY"].get("BONE_NUM");

    if(id入):
        id=id入;
    else:
        id=idΔΔ找id场景相同LIB(s要找名=sID名,i点数=i骨数,s类型="ARMATURE");
    #----找不到----------------------------------------------------------------
    if(id==None):
        id = bpy.data.armatures.new(name=s物名);#CURVE, SURFACE, FONT
        #bpy.ops.object.mode_set(mode="EDIT");#编辑骨只在编辑状态下才有数据
        #----新建骨架----------------------------------------------------------------
        o骨= bpy.data.objects.new(s物名,id);
        bpy.context.scene.objects.link(o骨);
        
        #o骨.data.name="HAIRBONE";
            #bpy.data.meshes.remove(id);
        #----EB要在编辑模式下----------------------------------------------
        if(context.scene.objects.active!=o骨):
            context.scene.objects.active=o骨;
        if(o骨.mode!="EDIT"):
            bpy.ops.object.mode_set(mode="EDIT");
        #----增加eb----------------------------------------------------------------
        Ceb=id.edit_bones;
        for s骨名,D属性 in OBJECTPRESET["ARMATURE_PROPERTY"]["EDITBONE_PROPERTY"].items():
            eb = Ceb.new(name=s骨名);
            Δ字典赋予物体LIB(D属性,eb,[]);
            if("tail" in D属性):
                print("apply tail",D属性["tail"]);

        for s骨名,D属性 in OBJECTPRESET["ARMATURE_PROPERTY"]["EDITBONE_PROPERTY"].items():#赋予父骨
            s骨父名=D属性.get("PARENT_NAME");
            if(s骨父名!=None):
                Ceb[s骨名].parent= Ceb[D属性["PARENT_NAME"]];

        if(o骨.mode!='OBJECT'):
            bpy.ops.object.mode_set(mode='OBJECT');#只在POSE模式 或物体下才能赋值posebone
        Lpb=o骨.pose.bones;
        for s骨名,D属性 in OBJECTPRESET["ARMATURE_PROPERTY"]["POSEBONE_PROPERTY"].items():
            Δ字典赋予物体LIB(D属性,Lpb[s骨名],[]);
        
        return o骨;
    
    return object_utils.object_data_add(context, id, operator=None).object;
 #--------------------------------------------------------------------------
def oΔΔ建融球(context,OBJECTPRESET,s物名):
    #meta= bpy.data.metaballs.new(name=s物名);#用这种方式创建的 不能显示 ??
    bpy.ops.object.metaball_add(type='BALL', radius=1.0, view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0),
    );#layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    oA=bpy.context.active_object;
    id=oA.data;
    """"""
    #Δ字典赋予物体LIB(OBJECTPRESET["META_PROPERTY"],meta,[]);
    Lme=id.elements;
    for  i, D in  enumerate(OBJECTPRESET["META_PROPERTY"]["L_META_ELEMENTS"]):
        me=Lme.new(type='BALL');
        Δ字典赋予物体LIB(D,me,[]);

    return oA;
    return object_utils.object_data_add(context, meta, operator=None).object;

#==============================================================
def oΔΔ建字体(context,OBJECTPRESET,s物名,sBody,id入):
    if(id入):
        id=id入;
    else:
        id=idΔΔ找id场景相同LIB(s要找名=sBody,i点数=None,s类型="FONT");
    #--------------------------------------------------------------------------
    if(id==None):
        bpy.ops.object.add(radius=1.0, type='FONT', view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), );#layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
        oA=bpy.context.active_object;
        oA.name=s物名;oA.data.body=sBody;
        Δ字典赋予物体LIB(OBJECTPRESET["FONT_PROPERTY"],oA.data,[]);
        return oA;
    else:
        return object_utils.object_data_add(context, id, operator=None).object;

#--------------------------------------------------------------------------
def oΔΔ建曲线(context,OBJECTPRESET,id入):
    scene = bpy.context.scene;
    s样条类型 = OBJECTPRESET["CURVE_PROPERTY"]["SPLINE_TYPE"];    # output s样条类型 "POLY" "NURBS" "BEZIER"
    print("OBJECTPRESET",OBJECTPRESET.keys());
    s物名 = OBJECTPRESET["OBJECT_PROPERTY"]["name"] ;
    #--------------------------------------------------------------------------
    sID名=OBJECTPRESET["CURVE_PROPERTY"].get("ID_NAME");
    
    i网点数=OBJECTPRESET["CURVE_PROPERTY"].get("POINT_NUM");
    if(id入):
        id=id入;
    else:
        id=idΔΔ找id场景相同LIB(s要找名=sID名,i点数=i网点数,s类型="CURVE");
    
    #--------------------------------------------------------------------------
    b存在id=False;
    if(id):
        newCurve =id;
        Lspline = newCurve.splines;
        b存在id=True;
    #----新建id-------------------------------------------------------------
    else:
        newCurve = bpy.data.curves.new(name=s物名, type = "CURVE") ;
    #--------------------------------------------------------------------------
    Ls排除键=["texspace_location","texspace_size","",""];
    Δ字典赋予物体LIB(OBJECTPRESET["CURVE_PROPERTY"],newCurve,Ls排除键);    
    
    #----应用spline 属性--------------------------------------------------------------
    for i段数, 属性s in enumerate(OBJECTPRESET["L_SPLINE"]):
        if(b存在id==False):
            newSpline = newCurve.splines.new(type = s样条类型);
        else:
            newSpline = Lspline[i段数];
        #----算出 Lv曲线点---------------------------------------------------------
        if (s样条类型 == "BEZIER"):
            newSpline.bezier_points.add(len(OBJECTPRESET["L_SPLINE"][i段数]["L_SPLINE_BZ_POINT"])-1);
        else:
            newSpline.points.add(len(OBJECTPRESET["L_SPLINE"][i段数]["L_SPLINE_POINT"])-1);
            #print("add point",OBJECTPRESET["POINT_COUNT"],len(OBJECTPRESET["L_SPLINE"]));
            
        
        #print("SPLINE",属性s.keys());
        if(OBJECTPRESET["CURVE_PROPERTY"]["SPLINE_TYPE"]=="BEZIER"):
            #pass ;
            for i, 属性sp in  enumerate(OBJECTPRESET["L_SPLINE"][i段数]["L_SPLINE_BZ_POINT"]):
                Δ字典赋予物体LIB(属性sp,newSpline.bezier_points[i],[]);
        else:
            for i, 属性sp in  enumerate(OBJECTPRESET["L_SPLINE"][i段数]["L_SPLINE_POINT"]):
                #print("len point",len(newSpline.points),len(OBJECTPRESET["L_SPLINE"][i段数]["L_SPLINE_POINT"]));
                Δ字典赋予物体LIB(属性sp,newSpline.points[i],[]);#spline point属性
                #print("POINT",属性sp["co"]);
                
    #----必须全部新建后才能赋spline属性???--------------------------------------------------------
    for i段数, 属性s in enumerate(OBJECTPRESET["L_SPLINE"]):
        Spline = newCurve.splines[i段数];
        Δ字典赋予物体LIB(属性s["SPLINE_PROPERTY"],Spline,[]);#spline属性
    #--------------------------------------------------------------------------
    new_obj = bpy.data.objects.new(name=s物名, object_data=newCurve); # object
    scene.objects.link(new_obj); # place in active scene

    return new_obj;
    return object_utils.object_data_add(context, newCurve, operator=None).object;#第二种创建方式

#——————————————————————————————————————————————————————
def oΔΔ建物(context,oA, L点序ξf3位, L边序i2边点ξ, L面序i4面点ξ序, s物名,b覆盖,b重参数化,meshLINK):
    #if(str(type(L点序ξf3位)) in["<class "int">"]):print("",);
    if(b覆盖):
        mesh新= bpy.data.meshes.new(s物名);
        bm=bmesh.new();

        mesh新.from_pydata(L点序ξf3位, L边序i2边点ξ, L面序i4面点ξ序);#Make a mesh from a list of
        mesh新.validate(clean_customdata=False);
        mesh新.update(calc_edges=True, calc_tessface=True);
        bm.from_mesh(mesh新, face_normals=True, use_shape_key=False, shape_key_index=0);#把mesh新转成bm

        mesh=oA.data;
        #----清除-------------------------------------------------------------
        if(oA.vertex_groups):
            oA.vertex_groups.clear();
        if(mesh.shape_keys):#有shapekey
            bpy.ops.object.shape_key_remove(all=True);#执行删除选中sk动作
        for muvll in mesh.uv_layers:
            bpy.ops.mesh.uv_texture_remove();

        bm.to_mesh(mesh);#把bm转成oA.data

        bm.free();
        bpy.data.meshes.remove(mesh新);

    #----全局---------------------------------------------------------------
    else:
        if(meshLINK):
            mesh新 = meshLINK;
            print("HAVE LINK",);
        else:
            mesh新 = bpy.data.meshes.new(s物名);
            mesh新.from_pydata(L点序ξf3位, L边序i2边点ξ, L面序i4面点ξ序);#Make a mesh from a list of vertices/edges/L面ξL顶ξ面点L底ξ面点 Until we have a nicer way to make geometry, use this
            mesh新.validate(clean_customdata=False);
            mesh新.update(calc_edges=True, calc_tessface=True);
            print("NEW MESH DATA",);
        """"""
        if(oA and b重参数化):
            if(oA.data !=None):#自己
                bm=bmesh.new();
                bm.from_mesh(mesh新, face_normals=True, use_shape_key=False, shape_key_index=0);#把mesh新转成bm

                bm.to_mesh(oA.data);#把bm转成oA.data

                bm.free();
                bpy.data.meshes.remove(mesh新);
                return oA;
        else:
            #return None;
            print("NEW MESH",mesh新.name);
            return object_utils.object_data_add(context, mesh新, operator=None).object;

#——————————————————————————————————————————————————————
def  oΔ新建物LIB(s物名,L点序ξf3位, L边序i2边点ξ, L面序i4面点ξ序):
    mesh新= bpy.data.meshes.new(s物名);
    mesh新.from_pydata(L点序ξf3位, L边序i2边点ξ, L面序i4面点ξ序);
    #mesh新.update();
    return object_utils.object_data_add(context, mesh新, operator=None).object;

def oΔ新建空物LIB(context,s类型,b是群组,g群组):
    o=object_utils.object_data_add(context, None, operator=None).object;
    if(s类型!=""):
        o.empty_draw_type=s类型;
    else:
        o.empty_draw_type="SINGLE_ARROW";# [‘PLAIN_AXES’, ‘ARROWS’, ‘SINGLE_ARROW’, ‘CIRCLE’, ‘CUBE’, ‘SPHERE’, ‘CONE’, ‘IMAGE’], default ‘PLAIN_AXES
    if(b是群组):
        o.dupli_type="GROUP";#[‘NONE’, ‘FRAMES’, ‘VERTS’, ‘FACES’, ‘GROUP’], default ‘NONE
        if(g群组):
            try:o.dupli_group=g群组#bpy.data.groups[s群组名];
            except:print("!!!no this group",g群组);
            
    return o;
    
def Δ删除物LIB(scene,o,b是层级):
    Lo要删除物=[];
        
    #----删除子级-------------------------------------------------------------
    if(b是层级):
        def  Δ收集子(o父):
            for o子 in  o父.children:
                Lo要删除物.append(o子);
                Δ收集子(o子);
        Δ收集子(o);
        for o子 in  Lo要删除物:
            if(o子!=None):
                scene.objects.unlink(o子);o子.user_clear();bpy.data.objects.remove(o子); 
                
    if(o!=None):
        scene.objects.unlink(o);o.user_clear();bpy.data.objects.remove(o);     
    
def Δ删除层级子物LIB(o):
    bpy.ops.object.select_all(action='DESELECT');
    for o子 in o.children:
        o子.select=True;
        for o孙 in o子.children:
            o孙.select=True;
            for o孙2 in o孙.children:
                o孙2.select=True;       
    bpy.ops.object.delete(False);
    
#==============================================================
def oΔ复制物LIB(o物源,b是复制data):#●假设o物源是selected
    Co场景=bpy.context.scene.objects;
    if(not o物源):
        #o物源=bpy.context.active_object;
        print("!!!o ==",o物源);return None;

    o子=o物源.copy();Co场景.link(o子);
    
    if(o物源.data!=None):
        print("data==",o物源.data);
        if(b是复制data):
            o子.data=o物源.data.copy();
        o子.data.name=o子.name;
    
    return o子;
    
def Δ复制物LIB(b是复制data):#●假设o物源是selected
    bpy.ops.object.duplicate(linked=not b是复制data, mode='TRANSLATION');#DUMMY 新建后激活新物

    
def Δ隐显物LIB(o,b是层级,b要隐):
    Lo要隐藏物=[];
    #----删除子级-------------------------------------------------------------
    if(b是层级):
        def  Δ收集子(o父):
            for o子 in  o父.children:
                Lo要隐藏物.append(o子);
                Δ收集子(o子);
        Δ收集子(o);
        for o子 in  Lo要隐藏物:
            if(o子!=None):
                if(o子.hide!=b要隐):
                    o子.hide=o子.hide_render= b要隐;
                
    if(o!=None):
        if(o.hide!=b要隐):
            o.hide=o.hide_render= b要隐;
    #print("Lo要隐藏物==",Lo要隐藏物);
#============================================================
def fΔ物体尺寸LIB(o):
    return sum(o.dimensions)/3;
        



#////////////////////////////////////////////////













#////end////end////end////end////end////end////end////end////








