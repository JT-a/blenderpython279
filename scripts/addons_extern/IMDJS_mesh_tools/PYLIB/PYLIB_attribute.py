
import bpy,sys,os
from math import*
from ctypes import*
import platform
if(platform.system()=="Windows"):  
    from ctypes.wintypes import *
from bpy.props import *
from mathutils import Matrix,Vector,Euler
from string import*


#////////////////////////////////////////////////
piΞ2=pi/2;
piΧ2=pi*2;
#//////////////////////////////////////////////////
Ls模块LIB=["PYLIB.PYLIB_main","PYLIB.PYLIB_math","PYLIB.PYLIB_object","PYLIB.PYLIB_mesh","PYLIB.PYLIB_attribute","PYLIB.PYLIB_algorithm","PYLIB.PYLIB_string","PYLIB.PYLIB_find","PYLIB.PYLIB_operator","PYLIB.PYLIB_print","PYLIB.PYLIB_draw","PYLIB.global_var"];
Ls类型物体网格曲线=["MESH","CURVE","LATTICE"];
Ls类型物体有DATA=["MESH","CURVE","LATTICE","FONT","CAMERA","META","LAMP","SPEAKER"];
Ls类型非MESH有DATA=["ARMATURE","CURVE","LATTICE","FONT","CAMERA","META","LAMP","SPEAKER"];
Ls整浮布字=["<class 'float'>","<class 'int'>","<class 'string'>","<class 'bool'>"];
Ls列元矢=["<class 'list'>","<class 'tuple'>","<class 'Vector'>","<class 'bpy_prop_array'>","<class 'Euler'>","<class'Quaternion'>"];
Ls忽略键=["TYPE","OBJECT_TYPE","ID_NAME","POINT_NUM","L_LATTICE_POINT","BEVEL_OBJECT_NAME","TAPER_OBJECT_NAME","PARENT_NAME","TEXTURE_NAME","SPLINE_TYPE","EDITBONE_PROPERTY","POSEBONE_PROPERTY","BONE_NUM","LAMP_TYPE","CHILDREN","EMPTY_PROPERTY","LATTICE_PROPERTY","CAMERA_PROPERTY","LAMP_PROPERTY","ARMATURE_PROPERTY","META_PROPERTY","CURVE_PROPERTY","SPLINE_PROPERTY","MODIFIER","CONSTRAINT","PARTICLE","OBJECT_PROPERTY","MESH_PROPERTY","","","","",""];

f3颜色黑=(0.0,0.0,0.0);f3颜色白=(1.0,1.0,1.0);
f3颜色红=(1.0, 0.0, 0.0);f3颜色蓝=(0.0, 0.0, 1.0);
f3颜色灰=(0.5, 0.5, 0.5);f3颜色绿=(0.0, 1.0, 0.0);
f3颜色紫=(1.0, 0.0, 1.0);
v零LIB=Vector((0.0,0.0,0.0));vZLIB=Vector((0.0,0.0,1.0));

#////此类用于被继承////////////////////////////////////
def bΔΔ已脏LIB(self, context,LL净脏):
    b是脏=False;
    for L净脏 in LL净脏:
        #print("L==",L净脏[0],L净脏[1]);
        #return b是脏;
        if(L净脏[0]!=L净脏[1]):
            #if(not b是脏):
            b是脏=True;print("DIFF",L净脏[0],L净脏[1]);
            L净脏[0]=L净脏[1];
    return b是脏;
    
#////////////////////////////////////////////////      
class 卐动力学卐PropertyGroup(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty();
    bp已初始化布料=BoolProperty(name='',description='',default=False,options={'ANIMATABLE'},subtype='NONE',update=None,get=None,set=None);
bpy.utils.register_class(卐动力学卐PropertyGroup);

class 卐缓存PSR卐PropertyGroup(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty();
    ip组ID = bpy.props.IntProperty(min = 0);
    #----缓存--------------------------------------------------------------
    fvp3位置缓存 = bpy.props.FloatVectorProperty(size=3, );
    fvp3旋转缓存 = bpy.props.FloatVectorProperty(size=3, );
    fvp4旋转缓存 = bpy.props.FloatVectorProperty(size=4,default=(0.0, 0.0, 0.0,1.0) );
    fvp3缩放缓存 = bpy.props.FloatVectorProperty(size=3, default=(1.0, 1.0, 1.0));
bpy.utils.register_class(卐缓存PSR卐PropertyGroup);
#==============================================================
class 卐物体PSR设定卐PropertyGroup(bpy.types.PropertyGroup):
    spMT名 = bpy.props.StringProperty(description = "---", update=None);#ΔUPDATE_初始化
    
    bp是初始化了PSR=bpy.props.BoolProperty(default=False);
    fvp3位置初始 = bpy.props.FloatVectorProperty(size=3, );#fvp3位置初始
    fvp3旋转初始 = bpy.props.FloatVectorProperty(size=3, );#fvp3旋转初始
    fvp4旋转初始 = bpy.props.FloatVectorProperty(size=4,default=(0.0, 0.0, 0.0,1.0) );#fvp4旋转初始
    fvp3缩放初始 = bpy.props.FloatVectorProperty(size=3, default=(1.0, 1.0, 1.0));#fvp3缩放初始
    fvp16矩阵子对父初始L=bpy.props.FloatVectorProperty(size=16,);
    
    fvp16矩阵父动态初始=bpy.props.FloatVectorProperty(size=16,);
    fvp16矩阵父前帧=bpy.props.FloatVectorProperty(size=16,);
    #----LOD--------------------------------------------------------------
    bp是LOD = bpy.props.BoolProperty(default=False);
    bp已应用修改器 = bpy.props.BoolProperty();
    ip细分级数=bpy.props.IntProperty(default=0);
    iip当前段数=bpy.props.IntProperty(default=0);
    
    #----缓存-------------------------------------------------------------
    bp开始了 = BoolProperty(name='',description='',default=False,options={'ANIMATABLE'},subtype='NONE',update=None,get=None,set=None);
    bp是隐藏动画 = BoolProperty(name='是隐藏动画',description='是隐藏动画',default=False,options={'ANIMATABLE'},subtype='NONE',update=None,get=None,set=None);
    ip时刻成为父子=bpy.props.IntProperty(default=-1);
    iip长度当前缓存=bpy.props.IntProperty(default=0);#1,2,3,4
    cp缓存PSR=bpy.props.CollectionProperty(type=卐缓存PSR卐PropertyGroup);
bpy.utils.register_class(卐物体PSR设定卐PropertyGroup);



#////////////////////////////////////////////////
def Δtry5属性LIB(物,sID0,sID1,sID2,sID3,sID4):
    try:
        物[sID0];
    except:
        物[sID0]={};
    if(sID1!=""):
        try:
            物[sID0][sID1];
        except:
            物[sID0][sID1]={};
        if(sID2!=""):
            try:
                物[sID0][sID1][sID2];
            except:
                物[sID0][sID1][sID2]={};
            if(sID3!=""):
                try:
                    物[sID0][sID1][sID2][sID3]
                except:
                    物[sID0][sID1][sID2][sID3]={};
                if(sID4!=""):
                    try:
                        物[sID0][sID1][sID2][sID3][sID4];
                    except:
                        物[sID0][sID1][sID2][sID3][sID4]={}; 
                        
#==============================================================
def Δtry5键属性LIB(s物,s键,s键1,s键2,s键3,s键4):#Χ
    try:
        eval(s物+s键);    
    except:    
        eval(s物+s键+"={}");
    if(s键1!=""):
        try:
            eval(s物+s键+s键1);    
        except:    
            eval(s物+s键+s键1+"={}");        
        if(s键2!=""):
            try:
                eval(s物+s键+s键1+s键2);    
            except:    
                eval(s物+s键+s键1+s键2+"={}");    
            if(s键3!=""):
                try:
                    eval(s物+s键+s键1+s键2+s键3);    
                except:    
                    eval(s物+s键+s键1+s键2+s键3+s键4+"={}");    
                if(s键4!=""):
                    try:
                        eval(s物+s键+s键1+s键2+s键3+s键5);    
                    except:    
                        eval(s物+s键+s键1+s键2+s键3+s键4+s键5+"={}");

                
        
#////////////////////////////////////////////////
def Δ清除临时属性(Ls属性名,Ls类型):
    if("OBJECT" in Ls类型):
        for o in bpy.data.objects:
            for s in Ls属性名:
                if(s in o.keys()):
                    del o[s];
                    
    if("MATERIAL" in Ls类型):
        for mat in bpy.data.materials:
            for s in Ls属性名:
                if(s in mat.keys()):
                    del mat[s];    
                    
    if("MESH" in Ls类型):
        for mesh in bpy.data.meshes:
            for s in Ls属性名:
                if(s in mesh.keys()):
                    del mesh[s];    
    

#////键名改了//////////////////////////////////////
def  Δ字典替换键LIB(D属性,s键原来,s键替换):
    if(s键原来 in D属性.keys() and s键原来!=s键替换):
        值=D属性[s键原来];
        D属性[s键替换]=值;
        #D属性.setdefault(s键替换,值);
        #print("VALUE==",D属性[s键替换]);
        try:
            D属性.pop(s键原来);#删除键只能pop,如果只改变值可以不用pop
        except:
            del D属性[s键原来];


#//////////////////////////////////////////////////
L默认值=[None,(0.0, 0.0),(0,0,0),(0.0,0.0,0.0),(1.0, 0.0, 0.0, 0.0),(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),"POS_X","QUATERNION","PLAIN_AXES","FREE"];#零也是值

def Δ复制类型属性LIB(m3A, m3S, s属性键=""):
    print("m3A==",m3A);
    for S属性键 in dir(m3A):
        print("ATTR==",S属性键);
        if (S属性键.find(s属性键) > -1):#找到属性 #如果找到从第几个字符相符 就返回几  如果找不到或 超过 返回-1 找到返回0
            try:
                setattr(m3S, s属性键, getattr(m3A, S属性键))
            except:
                pass;


def Δ物体不赋值予字典LIB(物体,Ls只含属性,Ls要排除的属性,D字典):
    Ls默认要排除的属性=["copy","user_clear","users_material","users_object_modifier","animation_data_create","animation_data_clear","animation_data","update_tag","library","is_updated_data","is_updated","is_library_indirect","users","link","unlink","__module__","__slots__","bl_rna","rna_type"];
    Ls要排除的属性.extend(Ls默认要排除的属性);
    for s属性 in dir(物体):
        #print("S KEY==",s属性);
        if(s属性 not in Ls要排除的属性):
            if(s属性 in Ls只含属性 or Ls只含属性==[]):
                try:
                    值=getattr(物体, s属性);
                    #print("VALUE==",值);
                    if(值 not in L默认值):
                        D字典[s属性]=值;
                        #setattr(D字典, s属性,值 );#字典不能用这个赋值 否则会出错
                        #print("SET ATTR==",D字典,s属性);
                except:pass;


 #--------------------------------------------------------------------------
def Δ赋值给字典LIB(物体,s键,D字典): #如果不是太多数据要保存 尽量不要用这个函数
    #print("DOT GIVE DICT==",物体,s键);
    值=getattr(物体,s键,"not find attr");
    if(值==None):
        print("NOT THIS ATTR",物体.name,s键);
        return ;

    D字典[s键]=值;

def Δ强制赋值给字典LIB(物体,s键,D字典): #如果不是太多数据要保存 尽量不要用这个函数
    #print("DOT GIVE DICT==",物体,s键);
    值=getattr(物体,s键,"not find attr");

    D字典[s键]=值;

def Δ不赋值给字典LIB(物体,s键,D字典): #如果不是太多数据要保存 尽量不要用这个函数
    #print("DOT GIVE DICT==",物体,s键);
    值=getattr(物体,s键,"not find attr");
    if(值==None):
        #print("NOT THIS ATTR",);
        return ;
    if(值 not in L默认值):
        D字典[s键]=值;

def Δ不赋值给左字典(D字典,s键,值): #如果不是太多数据要保存 尽量不要用这个函数
    if(值 not in L默认值):
        D字典[s键]=值;

#//////////////////////////////////////////////////
def Δ字典强制赋予物体LIB(D字典,物体__):
    for s键,值 in D字典.items():
        try:
            #if(值!=getattr(物体,s键,"not find attr")):
            setattr(物体__,s键,值);
        except:#pass;
            print("!!ERROR==",s键,值);

def Δ字典赋予物体LIB(D字典,物体__,Ls排除键):
    for s键,值 in D字典.items():
        #if(s键=="dupli_type"):print("dupli_type FIND---",值);#√
        #try:
        if(s键 not in Ls排除键):
            if(值 not in L默认值):
                物值=getattr(物体__,s键,"NONE");
                
                if(物值!="NONE"):#有可能有值 就是等于 NONE
                    #if(s键=="dupli_type"):print("dupli_type SET---",物值);
                    #print("GATATTR==",物体__,s键,物值,str(type(物值)),值);
                    if(str(type(物值))   in Ls整浮布字 and 物值!=值):
                        print("物值",物值,str(type(物值)));#,list(物值)
                        setattr(物体__,s键,值);#print("SETATTR==",物体__,s键,值);
                    #--------------------------------------------------------------------------
                    elif(str(type(物值))  in Ls列元矢 ):
                        try:
                            #print("LIST==",s键,物值);
                            if(s键 in ["lock_location","lock_rotation","lock_scale"]):
                                物值=[int(物值[0]),int(物值[1]),int(物值[2])];
                                print("LOCK==",s键,物值,值);

                            else:
                                物值=list(物值);

                        except:
                            print("!!!error set attri",s键);
                        if(物值!=值):

                            if(s键 in ["lock_location"]):
                                print("LOCK值得22",物值);
                                物体__.lock_location=(bool(值[0]),bool(值[1]),bool(值[2]));
                            elif(s键 in ["lock_rotation"]):
                                物体__.lock_rotation=(bool(值[0]),bool(值[1]),bool(值[2]));
                            elif(s键 in ["lock_scale"]):
                                物体__.lock_scale=(bool(值[0]),bool(值[1]),bool(值[2]));
                            else:
                                setattr(物体__,s键,值);
                    #--------------------------------------------------------------------------
                    elif(物值!=值):
                        #if(s键 not in Ls忽略键):
                        try:
                            setattr(物体__,s键,值);
                        except:    
                            print("!!! 物值!=值 error set attri",s键);
                        #if(s键=="dupli_type"):print("dupli_type SET---",物值);
                #----当当前物体值等于NONE-----------------------------------------------------
                else:
                    #if(s键 not in Ls忽略键):
                    try:
                        setattr(物体__,s键,值);
                    except:pass;    
                    
            
        #except:pass;

def ΔΔ字典赋予左物体(物体,D字典):
    for s键,值 in D字典.items():
        try:
            if(值 not in L默认值):
                值得=getattr(物体,s键,"NONE");
                if(值得!="NONE" and 值得!=值):
                    setattr(物体,s键,值);
        except:pass;

        
#======================================================
def Δ复制类型属性LIB(o,o_):
    #print("m3A==",m3A);
    for 属性 in dir(o):
        #print("ATTR==",属性);
        #try:
            setattr(o_, 属性, getattr(o, 属性))
        #except:pass;
            
#//////////////////////////////////////////////////

def cmp_f3(f3,F3):
    if(f3[0]==F3[0]):
        if(f3[1]==F3[1]):     
            if(f3[2]==F3[2]):        
                return True;
    else:
        return False;
#==============================================================
def SWAP(i位置1,i位置2,LD):
    if(str(type(LD)) in["<class 'list'>"]):
        #print("str(type(LD)",type(LD));
        if(len(LD)>i位置1 and len(LD)>i位置2):
            temp=LD[i位置1];LD[i位置1]=LD[i位置2];LD[i位置2]=temp;
    elif(str(type(LD)) in["<class 'dict'>"]):
        if(i位置1 in LD.keys() and i位置2 in LD.keys() ):
            temp=LD[i位置1];LD[i位置1]=LD[i位置2];LD[i位置2]=temp;      

    else:
        print("wrong type to swap!!!");
    
    #print("LD==",LD);
        
def p2cf_(cfIJ):#Ψcf_,Lpcf,
    Ψcf_ = POINTER(c_float);
    i维=len(cfIJ);#j维=len(cfIJ[0]);
    Lpcf=[None]*i维;
    for i in range(i维):
        Lpcf[i维]=cast(cfIJ[i], Ψcf_);#两个一级指针
    return (Ψcf_*i维)(*Lpcf);
    
def p2cf(cfIJ):#pCf_,LpCf,
    pCf_ = POINTER(c_float);
    i维=len(cfIJ);#j维=len(cfIJ[0]);
    LpCf=[cfIJ[0]]*i维;#填充●为了快速初始化
    for i in range(i维):
        LpCf[i]=cfIJ[i];#两个一级指针
    return (pCf_*i维)(*LpCf);
    
def Ψ2cf(cfIJ):#Ψcf_,Lpcf,
    Ψcf_ = POINTER(c_float);
    i维=len(cfIJ);#j维=len(cfIJ[0]);
    #Lpcf=[cfIJ[0]]*i维;#填充●为了快速初始化
    #for i in range(i维):Lpcf[i]=cfIJ[i];#两个一级指针
    #Lpcf=cfIJ;
    return (Ψcf_*i维)(*cfIJ);

""""""
def Ψ3cf2(cfIJk):
    Ψcf_ = POINTER(c_float);Ψ2cf_=POINTER( POINTER(c_float));
    #LTf =[((116.0,34.0,20.3), (118.5, 34.0,55.2)),((116.0,34.0,20.3), (118.5, 34.0,55.2))];
    i维=len(cfIJk);j维=len(cfIJk[0]);#k维=len(cfIJk[0][0]);
    
    Lp2cf=[None]*i维;Lpcf=[None]*j维;
    for i in range(i维):
        for j in range(j维):
            Lpcf[j]=cast(cfIJk[i][j], Ψcf_);#√一级指针 #●●地址保存在第一个参数,映射为第二个类型
        Lp2cf[i]=(Ψcf_*j维)(*Lpcf);#√p2就是二级指针

    return (Ψ2cf_*i维)(*Lp2cf);#(p2Cf,p2Cf);√ 就是三级指针
    
def Ψ3cf33(cfIJk):
    Ψcf_ = POINTER(c_float);Ψ2cf_=POINTER( POINTER(c_float));
    #LTf =[((116.0,34.0,20.3), (118.5, 34.0,55.2)),((116.0,34.0,20.3), (118.5, 34.0,55.2))];
    i维=len(cfIJk);j维=len(cfIJk[0]);#k维=len(cfIJk[0][0]);
    Lpcf=[None]*j维;
    
    Lp2cf=[None]*i维;#填充
    for i in range(i维):
        for j in range(j维):
            Lpcf[j]=cfIJk[i][j];#√一级指针 #●●地址保存在第一个参数,映射为第二个类型
        p2Cf=(Ψcf_*j维)(*Lpcf);#√p2就是二级指针
        Lp2cf[i]=p2Cf;
    print("Ψ3cfLIB2+++",);
    return (Ψ2cf_*i维)(*Lp2cf);#(p2Cf,p2Cf);√ 就是三级指针
    
def Ψ3cf(cfIJk):#LP_LP_c_float_Array_i维
    i维=len(cfIJk);j维=len(cfIJk[0]);
    #C=cast(cfIJk[0][0], POINTER(c_float));
    Ψcf_ = POINTER(c_float);#ΨcfC_=cast((c_float*3)(), Ψcf_);
    Ψ2cf_=POINTER(Ψcf_);#Ψ2cfC_=cast((c_float*3*j维)(), Ψ2cf_);
    #Ψ3cf_=POINTER(Ψ2cf_);C=cast(cfIJk, Ψ3cf_);
    #C=cast(cfIJk, Ψ2cf_);
    #for i in range(i维):
        #for j in range(j维):
            #print("C",C.contents[i][j]);
   #Ψcf_.from_param(byref(pointer(cfIJk[0][0][0])));
    """
    #Lp2cf=[(Ψcf_*j维)(*cfIJk[i]) for i in range(i维)];#[[Ψcf_,Ψcf_,...],[Ψcf_,Ψcf_,...],...]
    print("Ψ3cfLIB+++",);
    #return (Ψ2cf_*i维)(*Lp2cf);#(p2Cf,p2Cf);√ 就是三级指针
    Ψcf_.from_param(byref(pointer(cfIJk[0][0][0])));
    P=(Ψcf_*j维)();
    #P=(Ψcf_*j维)(*cfIJk[0]);
    #print("for ==",[(Ψcf_*j维)(*cfIJk[i]) for i in range(i维)]);
    """
    print("cfIJk==",*cfIJk)
    print("cfIJk==",*[*cfIJk])
    print("cfIJk==",*[*[*cfIJk]]);
    #return (Ψ2cf_*i维)(*[(Ψcf_*j维)(*cfIJk)]);#Χ
    return (Ψ2cf_*i维)(*[(Ψcf_*j维)(*cfIJk[i]) for i in range(i维)]);#√
    
    #return C;
    #return  (C*i维)();
    #return (Ψ2cf_*i维)(*[cast(cfIJk[i], Ψ2cf_) for i in range(i维)]);
    
def Ψ3f(i维,j维,k维):
    Ψcf_ = POINTER(c_float);C=cast((c_float * 3)(), POINTER(c_float));
    print("C==",C);
    #Ψcf_ = POINTER(c_float*k维);
    Ψ2cf_=POINTER( Ψcf_);Ψ3cf_=POINTER(Ψ2cf_);
    #Ψ2cf_=POINTER( Ψcf_*k维);Ψ3cf_=POINTER(Ψ2cf_*j维);
    #p1=pointer(cfIJk[0][0]);
    Ψcf_.from_param(byref(c_float(-1.0)));print("Ψcf_",Ψcf_);print("Ψcf_*k维",(Ψcf_*k维)());
    
    #Ψ3cf_.from_param(byref((c_float*k维*j维*i维)());
    #Ψ2cf_.from_param(byref(pointer((Ψcf_*k维)())));
    #Ψ3cf_.from_param(byref(pointer((Ψ2cf_*j维)())));
    print("Ψ2cf_",Ψ2cf_);
    #Ψ2cf_=(Ψcf_*j维)();
    #Ψ3cf_=(Ψ2cf_*j维)();
    #print("Ψ2cf_",Ψ3cf_);
    print("*==",[(Ψcf_*j维)()]*i维);
    return (Ψ2cf_*i维)(*[(Ψcf_*j维)()]*i维);#(p2Cf,p2Cf);√ 就是三级指针
    #return (Ψ2cf_*i维)((pointer((Ψcf_*j维)())*i维)());
    
def Ψ4cf(cfIJkl):
    Ψcf_ = POINTER(c_float);Ψ2cf_=POINTER( POINTER(c_float));Ψ3cf_=POINTER(POINTER( POINTER(c_float)));
    i维=len(cfIJkl);j维=len(cfIJkl[0]);k维=len(cfIJkl[0][0]);#l维=len(cfIJkl[0][0][0]);
    
    Lp3Cf=[];
    for i in range(i维):
        Lp2cf=[];
        for j in range(j维):
            Lpcf=[];
            for k in range(k维):
                Lpcf.append(cast(cfIJkl[i][j][k], Ψcf_));#√一级指针 #●●地址保存在第一个参数,映射为第二个类型
            p2Cf=(Ψcf_*k维)(*Lpcf);#√p2就是二级指针
            Lp2cf.append(p2Cf);
        p3Cf=(Ψ2cf_*j维)(*Lp2cf);#(p2Cf,p2Cf);√ 就是三级指针
        Lp3Cf.append(p3Cf);#四级指针
    return (Ψ3cf_*i维)(*Lp3Cf);
        
def Ψ2ci2(ciIJ):#ciIJ=(c_int*3*2)(*[ci3LIB]*2);
    pCi_ = POINTER(c_int);
    i维=len(ciIJ);
    LpCi=[];
    for i in range(i维):
        LpCi.append(cast(ciIJ[i], pCi_));
        #print("cast== ",cast(ciIJ[i], pCi_));
        #print("ciIJ== ",pointer(ciIJ[i]),ciIJ[i]);
    return (pCi_*i维)(*LpCi);#p2d就是二级指针
    
def Ψ2ci(ciIJ):#ciIJ=(c_int*3*2)(*[ci3LIB]*2);
    ΨCi_ = POINTER(c_int);
    i维=len(ciIJ);
    """
    LpCi=[ciIJ[0]]*i维;#填充●为了快速初始化
    for i in range(i维):
        LpCi[i]=ciIJ[i];
    """
    print("ciIJ==",*ciIJ);
    #print("ciIJ==",*[*ciIJ]);
    return (ΨCi_*i维)(*ciIJ);#√
    #return (ΨCi_*i维)(*[*ciIJ]);#√
    
def Ψ2ci2(ciIJ):#ciIJ=(c_int*3*2)(*[ci3LIB]*2);
    ΨCi_ = POINTER(c_int);
    i维=len(ciIJ);
    """"""
    LpCi=[ciIJ[0]]*i维;#填充●为了快速初始化
    for i in range(i维):
        LpCi[i]=ciIJ[i];
    return (ΨCi_*i维)(*LpCi);#p2d就是二级指针
#////////////////////////////////////////////////
def dllΔ载入dllLIB(_卐DLL,s键,dllpath1,dllpath2,dllpath3):   
    DLL=getattr(_卐DLL,s键,"none");
    if(DLL==None):
        try:
            DLL= CDLL(dllpath1);
            print("ok",);
        except:
            try:
                DLL= CDLL(dllpath2);
                print("not susses",);            
            except:    
                DLL= CDLL(dllpath3);
                print("not susses",);
                
    return DLL;

def dllΔ卸载dllLIB(_卐DLL,s键):   
    DLL=getattr(_卐DLL,s键,"none");
    if(platform.system()=="Windows"):  
        while(DLL):
            windll.kernel32.FreeLibrary.argtypes = [HMODULE];
            windll.kernel32.FreeLibrary(DLL._handle);#释放dll
            print("delete DLL~  //////////////////////////////////////////\n",);
            DLL=None;
    return DLL;
           
#--------------------------------------------------------------------------


#////////////////////////////////////////////////
def Δ载入模块LIB(Ls模块名):
    for s模块名 in Ls模块名:
        eval("from"+ s模块名+" import *" );


def Δ删除模块LIB(Ls模块名):
    for s in Ls模块名:
        try:
            if(s in sys.modules):
                del sys.modules[s];
                print("DEL MODULE==",s);
        except:
            print("ERROR DEL MODULE==",s);    

#////end////end////end////end////end////end////end////end////          
                
                
                
                

