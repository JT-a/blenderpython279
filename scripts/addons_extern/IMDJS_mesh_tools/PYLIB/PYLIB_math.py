

import bpy,sys,os,imp,random

from bpy.props import *
from mathutils import Matrix,Vector,Euler,Quaternion
from ctypes import*
from bpy_extras import object_utils
import bmesh
from math import*


#////////////////////////////////////////////////
piΞ2=pi/2;
piΧ2=pi*2;

try:
    from .PYLIB_draw import*
except:pass;    


#////////////////////////////////////////////////
global iG;iG=0;#global Ds名o物G;Ds名o物G={};


#--------数学公式--------------------------------------------------------------------------
def  atan3LIB(x, y):#出360度内正弧度
    z=pow(x,2)+pow(y,2);
    if(z==0):
        return 0;
        #z==0.00001;

    if(y>=0 ):#在↑
        return acos(x/sqrt(z));
    else:#(y<0and x<=0)#在↙
        #print("y<=0\n");
        c=acos(x/sqrt(z));
        return c+(pi-c)*2;

def f2巜f2十f2(f2一,  f2二):   return [f2一[0]+f2二[0],f2一[1]+f2二[1]];
def f2十f2_f2(f2一,  f2二,f2三):  f2三[0]=f2一[0]+f2二[0];f2三[1]=f2一[1]+f2二[1];
def f3巜f3十f3(f3一,  f3二):   return [f3一[0]+f3二[0],f3一[1]+f3二[1],f3一[2]+f3二[2]];
def v巜f3十f3(f3一,  f3二):   return Vector((f3一[0]+f3二[0],f3一[1]+f3二[1],f3一[2]+f3二[2]));

def f3十f3_f3(f3一,  f3二,f3三):   f3三[0]=f3一[0]+f3二[0];f3三[1]=f3一[1]+f3二[1];f3三[2]=f3一[2]+f3二[2];
def f3十f3_(f3一,  f3二):   f3二[0]=f3一[0]+f3二[0];f3二[1]=f3一[1]+f3二[1];f3二[2]=f3一[2]+f3二[2];
def f2巜f2十f2Ξ2(f2一,  f2二):  return  [(f2一[0]+f2二[0])/2,(f2一[1]+f2二[1])/2];
def f3巜f3十f3Ξ2(f3一,  f3二):   return  [(f3一[0]+f3二[0])/2,(f3一[1]+f3二[1])/2,(f3一[2]+f3二[2])/2];

def f2巜f2一f2(f2一,  f2二):   return [f2一[0]-f2二[0],f2一[1]-f2二[1]];
def f3巜f3一f3(f3一,  f3二):   return [f3一[0]-f3二[0],f3一[1]-f3二[1],f3一[2]-f3二[2]];
def v巜f3一f3(f3一,  f3二):   return Vector((f3一[0]-f3二[0],f3一[1]-f3二[1],f3一[2]-f3二[2]));


def f2一f2_f2(f2一,  f2二,f2三):f2三[0]=f2一[0]-f2二[0];f2三[1]=f2一[1]-f2二[1];

def f3一f3_f3(f3一,  f3二,  f3三): f3三[0]=f3一[0]-f3二[0];f3三[1]=f3一[1]-f3二[1];f3三[2]=f3一[2]-f3二[2];

def f2Χf_f2(f2一,  f,  f2三): f2三[0]=f2一[0]*f;f2三[1]=f2一[1]*f;
def f3Χf_f3(f3一,  f,  f2三): f2三[0]=f3一[0]*f;f2三[1]=f3一[1]*f;f2三[2]=f3一[2]*f;
def f3巜f3Χf(f3一,  f): return [f3一[0]*f,f3一[1]*f,f3一[2]*f];

def f巜f3λf3(f3点X, f3点Y):
    print("----",f3点X[0]* f3点Y[0],f3点X[1]* f3点Y[1],f3点X[2]* f3点Y[2]);
    print("--",f3点X[2],f3点Y[2]);
    return f3点X[0]* f3点Y[0]+f3点X[1]* f3点Y[1]+f3点X[2]* f3点Y[2];
def f巜f3Γf3(f3点X, f3点Y): # 两乛 的垂线乛  #等同 f3点X.cross(f3点Y)
    return (f3点X[1]*f3点Y[2]-f3点X[2]*f3点Y[1]  ,  f3点X[2]*f3点Y[0]-f3点X[0]*f3点Y[2]  ,  f3点X[0]*f3点Y[1]-f3点X[1]*f3点Y[0]);
    
def f3Γf3_f3(f3点X, f3点Y,f3点Z_):
    #print("F",f3点X, f3点Y,f3点Z_);
    f3点Z_[0]=f3点X[1]*f3点Y[2]-f3点X[2]*f3点Y[1];  
    f3点Z_[1]=f3点X[2]*f3点Y[0]-f3点X[0]*f3点Y[2]; 
    f3点Z_[2]=f3点X[0]*f3点Y[1]-f3点X[1]*f3点Y[0];
    
def f巜vΓv(f3点X, f3点Y): # 两乛 的垂线乛  #等同 f3点X.cross(f3点Y)
    return Vector((f3点X[1]*f3点Y[2]-f3点X[2]*f3点Y[1]  ,  f3点X[2]*f3点Y[0]-f3点X[0]*f3点Y[2]  ,  f3点X[0]*f3点Y[1]-f3点X[1]*f3点Y[0]));

    
def f巜f2乛f2(f2一,  f2二):
    f2三=[None,None];f2三[0]=f2一[0]-f2二[0];f2三[1]=f2一[1]-f2二[1];
    fUV距离=sqrt(pow(f2三[0],2)+pow(f2三[1],2));
    return fUV距离;
    
def length1(f3长):
    f对角线长=sqrt(pow(f3长[0],2)+pow(f3长[1],2)+pow(f3长[2],2));
    return f对角线长;
 
def sum(f3):
    return f3[0]+f3[1]+f3[2];
    
def length(f3一,  f3二):
    f3长=[None,None,None];f3长[0]=f3一[0]-f3二[0];f3长[1]=f3一[1]-f3二[1];f3长[2]=f3一[2]-f3二[2];
    f对角线长=sqrt(pow(f3长[0],2)+pow(f3长[1],2)+pow(f3长[2],2));
    return f对角线长;


#====万能加减===================================================
def TΔΔ减LIB(T1,T2):
    T结果=[];#print("--Type==",type(T1),type(T2));
    if(str(type(T1)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
        if(str(type(T2)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
            T结果=T1-T2;
        elif(str(type(T2)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
            for i in range(len(T2)):
                T结果.append(T1-T2[i]);


    elif(str(type(T1)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
        if(str(type(T2)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
            for i in range(len(T2)):
                T结果.append(T1[i]-T2[i]);
        elif(str(type(T2)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
            for i in range(len(T1)):
                T结果.append(T1[i]-T2);

    elif(str(type(T1)) in["<class 'bool'>","<class 'string'>"] and str(type(T2)) in["<class 'bool'>","<class 'string'>"]):
        return T2;

    return T结果;

#--------------------------------------------------------------------------
def TΔΔ加LIB(T1,T2):
    T结果=[];#print("++Type==",type(T1),type(T2));//"<class 'dict'>"
    if(str(type(T1)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
        if(str(type(T2)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
            T结果=T1+T2;
        elif(str(type(T2)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
            for i in range(len(T2)):
                T结果.append(T1+T2[i]);


    elif(str(type(T1)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
        if(str(type(T2)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
            for i in range(len(T2)):
                T结果.append(T1[i]+T2[i]);
        elif(str(type(T2)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
            for i in range(len(T1)):
                T结果.append(T1[i]+T2);

    elif(str(type(T1)) in["<class 'bool'>","<class 'string'>"] and str(type(T2)) in["<class 'bool'>","<class 'string'>"]):
        return T2;

    return T结果;

#--------------------------------------------------------------------------
def TΔΔ乘LIB(T1,T2):
    T结果=[];#print("**Type==",type(T1),type(T2));
    if(str(type(T1)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
        if(str(type(T2)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
            T结果=T1*T2;
        elif(str(type(T2)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
            for i in range(len(T2)):
                T结果.append(T1*T2[i]);


    elif(str(type(T1)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
        if(str(type(T2)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
            for i in range(len(T2)):
                T结果.append(T1[i]*T2[i]);
        elif(str(type(T2)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
            for i in range(len(T1)):
                T结果.append(T1[i]*T2);
    elif(str(type(T1)) in["<class 'bool'>","<class 'string'>"] and str(type(T2)) in["<class 'bool'>","<class 'string'>"]):
        return T2;

    return T结果;

#--------------------------------------------------------------------------
def TΔΔ除LIB(T1,T2):
    T结果=[];
    if(str(type(T1)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
        if(str(type(T2)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
            T结果=T1/T2;
        elif(str(type(T2)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
            for i in range(len(T2)):
                T结果.append(T1/T2[i]);


    elif(str(type(T1)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
        if(str(type(T2)) in["<class 'list'>","<class 'tuple'>","<class 'IDPropertyArray'>","<class 'Vector'>","<class 'Euler'>"]):
            for i in range(len(T2)):
                T结果.append(T1[i]/T2[i]);
        elif(str(type(T2)) in["<class 'int'>","<class 'float'>","<class 'IntProperty'>","<class 'FloatProperty'>"]):
            for i in range(len(T1)):
                T结果.append(T1[i]/T2);

    elif(str(type(T1)) in["<class 'bool'>","<class 'string'>"] and str(type(T2)) in["<class 'bool'>","<class 'string'>"]):
        return T2;

    return T结果;

#==============================================================
def fΔΔ两f2夹角弧正LIB(f2点一, f2点二):#这个夹角是小于180度
    # f2圆心=0.0f,0.0f; f2头
    f对弧一=atan3LIB(f2点一[0],f2点一[1]);#  Y#X
    f对弧二=atan3LIB(f2点二[0],f2点二[1]);
    return abs(f对弧二-f对弧一);

def fΔΔ两f3夹角弧LIB(f3点一, f3点二):#这个夹角是小于180度 正
    #double c, d;
    c = f3点一[0]*f3点二[0] + f3点一[1]*f3点二[1] + f3点一[2]*f3点二[2];#点积
    d = sqrt(f3点一[0]*f3点一[0] + f3点一[1]*f3点一[1] + f3点一[2]*f3点一[2]) * sqrt(f3点二[0]*f3点二[0] + f3点二[1]*f3点二[1] + f3点二[2]*f3点二[2]);#这两个乛长相乘
    if(d==0):d=0.0001;
    #print("ACOS==",acos(c/d));
    return acos(c/d);

def fΔΔ两m夹角弧LIB(m一, m二,s轴):
    if(s轴=="X"):
        v一=m一[0][0],m一[1][0],m一[2][0];
        v二=m二[0][0],m二[1][0],m二[2][0];
    elif(s轴=="Y"):
        v一=m一[0][1],m一[1][1],m一[2][1];
        v二=m二[0][1],m二[1][1],m二[2][1];
    elif(s轴=="Z"):
        v一=m一[0][2],m一[1][2],m一[2][2];
        v二=m二[0][2],m二[1][2],m二[2][2];
    return fΔΔ两f3夹角弧LIB(v一, v二);


def ΔΔ角对边乛LIB(f2邻边乛, f2斜边乛, f2对边乛):#得对边的乛
    f夹角弧=fΔΔ两f2夹角弧正LIB(f2邻边乛,f2斜边乛);
    f邻边长=sqrt(pow(f2邻边乛[0],2)+pow(f2邻边乛[1],2));
    f斜边长=sqrt(pow(f2斜边乛[0],2)+pow(f2斜边乛[1],2));
    f对边长=f斜边长*cos(f夹角弧);
    f邻边比例=f对边长/f邻边长;
    f2对边乛[0]=f2邻边乛[0]*f邻边比例;f2对边乛[1]=f2邻边乛[1]*f邻边比例;

def f3ΔΔ角对边乛LIB(f3邻边乛, f3斜边乛):#得对边的乛
    f3对边乛=[None,None,None];
    f夹角弧=fΔΔ两f3夹角弧LIB(f3邻边乛,f3斜边乛);
    f邻边长=sqrt(pow(f3邻边乛[0],2)+pow(f3邻边乛[1],2)+pow(f3邻边乛[2],2));
    f斜边长=sqrt(pow(f3斜边乛[0],2)+pow(f3斜边乛[1],2)+pow(f3斜边乛[2],2));
    f对边长=f斜边长*cos(f夹角弧);
    f邻边比例=f对边长/f邻边长;
    f3对边乛[0]=f3邻边乛[0]*f邻边比例;f3对边乛[1]=f3邻边乛[1]*f邻边比例;f3对边乛[2]=f3邻边乛[2]*f邻边比例;

    #memcpy(f2对边乛,Lf2uv选序[i序真],sizeof(f2对边乛));


def v巜f3(f3):
    return Vector(f3);


#////几何////////////////////////////////////////
#☐☐☐☐☐●f3高☐☐☐☐
#☐☐☐☐┆\☐☐☐☐☐
#☐☐☐☐│☐┊\☐☐☐☐
#☐☐☐┆☐☐●☐\☐☐☐
#☐☐☐│☐☐☐┊☐\☐☐
#☐☐┆☐☐☐☐┇☐☐\
#☐☐●━━━━●━━→●
#☐f3底1 ☐☐f3中点底        f3底2
def vΔΔ三角形中心LIB(f3底1,f3底2,f3高):
    return Vector(((f3底1[0]+f3底2[0]+f3高[0])/3,(f3底1[1]+f3底2[1]+f3高[1])/3,(f3底1[2]+f3底2[2]+f3高[2])/3));

def vΔΔ修正垂线LIB(v乛X,v乛共法Z):
    #f点积=v乛共法Z.dot(v乛X);
    #f点积=f巜f3λf3(v乛共法Z,v乛X);
    f夹角=fΔΔ两f3夹角弧LIB(v乛共法Z,v乛X);
    print("WRONG==",v乛共法Z);
    print("ANGLE==",f夹角);
    if(f夹角<1.5706 or f夹角>1.5708):#不垂直

        #f夹角=fΔΔ两f3夹角弧LIB(v乛X,v乛共法Z);
        f共法长=v乛共法Z.length;fX长=v乛X.length;
        f邻边长=f共法长*cos(f夹角);
        f邻边ΞX=f邻边长/fX长;
        v乛邻边=v乛X*f邻边ΞX;#可以是十一方向
        v乛修十共法Z=v乛共法Z-v乛邻边;#修十
        print("CORRECT==",v乛修十共法Z);

        return v乛修十共法Z;
    return None;
    #☐☐☐☐v乛修十共法Z☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    #v乛共法Z☐ ☐  ↑☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    #☐☐☐☐☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    #☐☐↑┊☐☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    #☐☐┃┇☐☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    #☐☐┃☐┊☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    #☐☐┃☐┇☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    #☐☐┃☐☐┊┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    #☐☐   cos ( ┇┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
    #☐☐←━━━╋━━━━━━━→v乛X☐☐☐☐☐☐☐
    #☐v乛邻边


#////////////////////////////////////////////////
def fΔΔ从f2一逆到f2二弧十(f2点一, f2点二):#这个角可以大于180度
    f对弧一=atan3LIB(f2点一[0],f2点一[1]);#  Y#X
    f对弧二=atan3LIB(f2点二[0],f2点二[1]);
    if(f对弧一<f对弧二):
        return f对弧二-f对弧一;
    elif(f对弧一>f对弧二):
        return 360-(f对弧一-f对弧二);
    elif(f对弧一==f对弧二):
        return 0.0;

def f2ΔΔ从乛一逆弧后的乛(f2点一, f逆弧度):#这个角可以大于180度
    f弧一=atan3LIB(f2点一[0],f2点一[1]);#  Y#X
    f最终弧=(f弧一+f逆弧度)%piΧ2;
    f线长=sqrt(pow(f2点一[0],2)+pow(f2点一[1],2));

    f2结果=[None,None];
    f2结果[0]=f线长*cos(f最终弧);f2结果[1]=f线长*sin(f最终弧);
    return f2结果;
    
#////CTYPES/////////////////////////////////////////
def ΔΔcf33一反m二LIB(cf33,m):
    m[0][0]=cf33[0][0];m[0][1]=cf33[1][0];m[0][2]=cf33[2][0];m[0][3]=0;
    m[1][0]=cf33[0][1];m[1][1]=cf33[1][1];m[1][2]=cf33[2][1];m[1][3]=0;
    m[2][0]=cf33[0][1];m[2][1]=cf33[1][2];m[2][2]=cf33[2][2];m[2][3]=0;
    m[3][0]=0;m[3][1]=0;m[3][2]=0;m[3][3]=1;
def ΔΔcf44一反m二LIB(cf33,m):
    m[0][0]=cf33[0][0];m[0][1]=cf33[1][0];m[0][2]=cf33[2][0];m[0][3]=cf33[3][0];
    m[1][0]=cf33[0][1];m[1][1]=cf33[1][1];m[1][2]=cf33[2][1];m[1][3]=cf33[3][1];
    m[2][0]=cf33[0][1];m[2][1]=cf33[1][2];m[2][2]=cf33[2][2];m[2][3]=cf33[3][2];
    m[3][0]=cf33[0][3];m[3][1]=cf33[1][3];m[3][2]=cf33[2][3];m[3][3]=cf33[3][3];
def ΔΔcf44一反f44二LIB(cf33,m):
    m[0][0]=cf33[0][0];m[0][1]=cf33[1][0];m[0][2]=cf33[2][0];m[0][3]=cf33[3][0];
    m[1][0]=cf33[0][1];m[1][1]=cf33[1][1];m[1][2]=cf33[2][1];m[1][3]=cf33[3][1];
    m[2][0]=cf33[0][1];m[2][1]=cf33[1][2];m[2][2]=cf33[2][2];m[2][3]=cf33[3][2];
    m[3][0]=cf33[0][3];m[3][1]=cf33[1][3];m[3][2]=cf33[2][3];m[3][3]=cf33[3][3];
    
def  Lci巜Li(Li):
    return (c_int*len(Li))(*Li);

def  Lcf巜Lf(Lf):
    return (c_float*len(Lf))(*Lf);
    
def  cf2巜f2(v2):
    return (c_float*2)(v2[0],v2[1]);
    
def  cf3巜f3(v3):
    return (c_float*3)(v3[0],v3[1],v3[2]);

def  cf33巜m3(m3):
    cf33=(c_float*3*3)();
    for i in range(3):
        for j in range(3):
            cf33[i][j]=m3[i][j];
    return cf33;

def  f2巜cf2(v2):
    return [v2[0],v2[1]];
    
def  f3巜cf3(v3):
    return [v3[0],v3[1],v3[2]];
    
def v_f3_(v,f3_):
    for i,f in enumerate(v):
        f3_[i]=f;

def Lcf3巜Lf3(Lv):
    Lcf3=(c_float*3*len(Lv))();
    for i,v in enumerate(Lv):
        for j,f in enumerate(v):
            Lcf3[i][j]=f;
        
    return Lcf3;
    
"""
def Lv巜Lf3(Lv):
    Lcf3=((c_float*3)*len(Lv))();
    for j毛点数应,v in enumerate(Lv):
        for i,f in enumerate(v):
            Lcf3[j毛点数应][i]=f;
        
    return Lcf3;
"""

    
def Lf3巜Lcf3(L序cf3位):
    Lf3=[];
    for i序,cf3位 in enumerate(L序cf3位):
        Lf3.append([]);
        #for i,f in enumerate(cf3位):
        Lf3[i序]=[*cf3位];
    return Lf3;
    
def Lv巜Lcf3(L序cf3位):
    Lv=[];
    for i序,cf3位 in enumerate(L序cf3位):
        Lv.append(Vector(cf3位));
    return Lv;
    
def LLcf3巜LLf3(i最多点数,LLv):
    LLcf3=(c_float*3*i最多点数*len(LLv))();
    for i,Lv in enumerate(LLv):
        i长=len(Lv);
        for j in range(i最多点数):
            if(j<i长):
                v=Lv[j];
                LLcf3[i][j][0]=v[0];LLcf3[i][j][1]=v[1];LLcf3[i][j][0]=v[2];
            else:
                LLcf3[i][j][0]=-11111111;LLcf3[i][j][1]=-11111111;LLcf3[i][j][0]=-11111111;
                
    return LLcf3;
    
#====MV=====================================================
def f3ΔΔm得f3位LIB(m):
    f3=[];
    for i,v4 in enumerate(m):
        if(i==3):break;
        f3.append(m[i][3]);
    return f3;

def vΔΔm得v位LIB(m):
    v位=Vector();
    v位.x,v位.y,v位.z=m[0][3],m[1][3],m[2][3];
    #v位.x=m[0][3];v位.y=m[1][3];v位.z=m[2][3];
    #print("M",m[0][3],m[1][3],m[2][3]);
    return v位;
    

        
#--------------------------------------------------------------------------
def ΔΔm移位LIB(v位,m结果):
    m结果[0][3]=v位.x;
    m结果[1][3]=v位.y;
    m结果[2][3]=v位.z;

def mΔΔm移位LIB(m,v位):
    m结果=Matrix();
    m结果[0][0]=m[0][0];m结果[0][1]=m[0][1];m结果[0][2]=m[0][2];m结果[0][3]=v位.x;
    m结果[1][0]=m[1][0];m结果[1][1]=m[1][1];m结果[1][2]=m[1][2];m结果[1][3]=v位.y;
    m结果[2][0]=m[2][0];m结果[2][1]=m[2][1];m结果[2][2]=m[2][2];m结果[2][3]=v位.z;
    m结果[3][0]=m[3][0];m结果[3][1]=m[3][1];m结果[3][2]=m[3][2];m结果[3][3]=m[3][3];#位
    return m结果;
#==============================================================
def m巜m3_m(m3旋,m):
    m结果=Matrix();
    m结果[0][0]=m3旋[0][0];m结果[0][1]=m3旋[0][1];m结果[0][2]=m3旋[0][2];m结果[0][3]=m[0][3];
    m结果[1][0]=m3旋[1][0];m结果[1][1]=m3旋[1][1];m结果[1][2]=m3旋[1][2];m结果[1][3]=m[1][3];
    m结果[2][0]=m3旋[2][0];m结果[2][1]=m3旋[2][1];m结果[2][2]=m3旋[2][2];m结果[2][3]=m[2][3];
    m结果[3][0]=m[3][0];m结果[3][1]=m[3][1];m结果[3][2]=m[3][2];m结果[3][3]=m[3][3];#位
    return m结果;

def m3_m_(m3旋,m):
    m[0][0]=m3旋[0][0];m[0][1]=m3旋[0][1];m[0][2]=m3旋[0][2];
    m[1][0]=m3旋[1][0];m[1][1]=m3旋[1][1];m[1][2]=m3旋[1][2];
    m[2][0]=m3旋[2][0];m[2][1]=m3旋[2][1];m[2][2]=m3旋[2][2];

#==============================================================
def m巜f16(f16矩阵):
    m=Matrix();
    for i in range(4):
        m[i][0]=f16矩阵[i*4];m[i][1]=f16矩阵[i*4+1];m[i][2]=f16矩阵[i*4+2];m[i][3]=f16矩阵[i*4+3];
    return m;

def m3巜f33(f33):
    m3=Matrix().to_3x3();
    m3[0][0],m3[1][0],m3[2][0]=f33[0][0],f33[1][0],f33[2][0];#X轴
    m3[0][1],m3[1][1],m3[2][1]=f33[0][1],f33[1][1],f33[2][1];#Y轴
    m3[0][2],m3[1][2],m3[2][2]=f33[0][2],f33[1][2],f33[2][2];#Z轴
    return m3;

def f16巜m(m):
    f16矩阵=[];
    for v4 in m:
        for f in v4:
            f16矩阵.append(f);
    return f16矩阵;

#--------------------------------------------------------------------------
def vLoc_m(v,m):
    m[0][3],m[1][3],m[2][3]=v[0],v[1],v[2] ;

def m3Δ由v一轴f二弧生成m3LIB(v轴,f弧度):
    m3结果=Matrix().to_3x3();
    fXX = v轴.x * v轴.x;
    fYY = v轴.y * v轴.y;
    fZZ = v轴.z * v轴.z;
    fXY = v轴.x * v轴.y;
    fXZ = v轴.x * v轴.z;
    fYZ = v轴.y * v轴.z;
    fSinAngle = sin(f弧度);
    fOneMinusCosAngle = 1 - cos(f弧度);
    m3结果[0][0] = 1 + fOneMinusCosAngle * (fXX - 1);
    m3结果[0][1] = -v轴.z * fSinAngle + fOneMinusCosAngle * fXY;
    m3结果[0][2] = v轴.y * fSinAngle + fOneMinusCosAngle * fXZ;
    m3结果[1][0]= v轴.z * fSinAngle + fOneMinusCosAngle * fXY;
    m3结果[1][1]= 1 + fOneMinusCosAngle * (fYY - 1);
    m3结果[1][2]= -v轴.x * fSinAngle + fOneMinusCosAngle * fYZ;
    m3结果[2][0]= -v轴.y * fSinAngle + fOneMinusCosAngle * fXZ;
    m3结果[2][1]= v轴.x * fSinAngle + fOneMinusCosAngle * fYZ;
    m3结果[2][2] = 1 + fOneMinusCosAngle * (fZZ - 1);
    return m3结果;

def qΔ由v一轴f二弧生成qLIB(v轴,f弧度):
    q=Quaternion();
    f半弧 = f弧度 *0.5;
    fSin半弧 = sin(f半弧);
    q.x = v轴.x * fSin半弧;
    q.y = v轴.y * fSin半弧;
    q.z = v轴.z * fSin半弧;
    q.w = cos(f半弧);
    return q;

#============================================================
def m3巜2v(v乛Xo,v乛Yo,v乛Zo,i0或1):
    m3=Matrix().to_3x3();
    v乛X=Vector();v乛Y=Vector();v乛Z=Vector();
    if(v乛Xo):
        v乛X=v乛Xo.copy();
    if(v乛Yo):
        v乛Y=v乛Yo.copy();
    if(v乛Zo):
        v乛Z=v乛Zo.copy();#print("V",v乛X,v乛Y);
    #------------------------------------------------------------
    if(v乛Xo==None):
        f3Γf3_f3(v乛Y,v乛Z,v乛X);
        if(v乛X.length==0):
            print("!!!!v乛X.length==0",);
            return ;
    elif(v乛Yo==None):
        f3Γf3_f3(v乛Z,v乛X,v乛Y);
        if(v乛Y.length==0):
            print("!!!!v乛Y.length==0",);
            return ;
    elif(v乛Zo==None):
        f3Γf3_f3(v乛X,v乛Y,v乛Z);
        if(v乛Z.length==0):
            print("!!!!v乛Z.length==0",);
            return ; 

    if(i0或1==0):
        f3Γf3_f3(v乛Y,v乛Z,v乛X);#修正X轴
    elif(i0或1==1):
        f3Γf3_f3(v乛Z,v乛X,v乛Y);#修正Y轴
    elif(i0或1==2):
        f3Γf3_f3(v乛X,v乛Y,v乛Z);#修正Z轴
 
    m3[0][0],m3[1][0],m3[2][0]=v乛X[0],v乛X[1],v乛X[2];#X轴
    m3[0][1],m3[1][1],m3[2][1]=v乛Y[0],v乛Y[1],v乛Y[2];#Y轴
    m3[0][2],m3[1][2],m3[2][2]=v乛Z[0],v乛Z[1],v乛Z[2];#Z轴
    m3.normalize();#十常化

    return m3;
    
def m巜2v(v乛Xo,v乛Yo,v乛Zo,v位,i0或1):
    m应=Matrix();
    v乛X=Vector();v乛Y=Vector();v乛Z=Vector();
    if(v乛Xo):
        v乛X=v乛Xo.copy();
    if(v乛Yo):
        v乛Y=v乛Yo.copy();
    if(v乛Zo):
        v乛Z=v乛Zo.copy();#print("V",v乛X,v乛Y);
    #------------------------------------------------------------
    if(v乛Xo==None):
        f3Γf3_f3(v乛Y,v乛Z,v乛X);
        if(v乛X.length==0):
            print("!!!!v乛X.length==0",);
            return ;
    elif(v乛Yo==None):
        f3Γf3_f3(v乛Z,v乛X,v乛Y);
        if(v乛Y.length==0):
            print("!!!!v乛Y.length==0",);
            return ;
    elif(v乛Zo==None):
        f3Γf3_f3(v乛X,v乛Y,v乛Z);
        if(v乛Z.length==0):
            print("!!!!v乛Z.length==0",);
            return ; 

    if(i0或1==0):
        f3Γf3_f3(v乛Y,v乛Z,v乛X);#修正X轴
    elif(i0或1==1):
        f3Γf3_f3(v乛Z,v乛X,v乛Y);#修正Y轴
    elif(i0或1==2):
        f3Γf3_f3(v乛X,v乛Y,v乛Z);#修正Z轴
        
    m应[0][0],m应[1][0],m应[2][0]=v乛X[0],v乛X[1],v乛X[2];#X轴
    m应[0][1],m应[1][1],m应[2][1]=v乛Y[0],v乛Y[1],v乛Y[2];#Y轴
    m应[0][2],m应[1][2],m应[2][2]=v乛Z[0],v乛Z[1],v乛Z[2];#Z轴
    m应.normalize();#十常化
    if(v位 != None):
        m应[0][3]=v位[0];m应[1][3]=v位[1];m应[2][3]=v位[2];
    return m应;
#------------------------------------------------------------
def cf33巜2v(v乛Xo,v乛Yo,v乛Zo,i0或1):#这个是C++的矩阵 跟py是反的
    cf33=((c_float*3)*3)();
    v乛X=Vector();v乛Y=Vector();v乛Z=Vector();
    if(v乛Xo):
        v乛X=v乛Xo.copy();
    if(v乛Yo):
        v乛Y=v乛Yo.copy();
    if(v乛Zo):
        v乛Z=v乛Zo.copy();#print("V",v乛X,v乛Y);
    #------------------------------------------------------------
    if(v乛Xo==None):
        f3Γf3_f3(v乛Y,v乛Z,v乛X);
        if(v乛X.length==0):
            print("!!!!v乛X.length==0",);
            return ;
    elif(v乛Yo==None):
        f3Γf3_f3(v乛Z,v乛X,v乛Y);
        if(v乛Y.length==0):
            print("!!!!v乛Y.length==0",);
            return ;
    elif(v乛Zo==None):
        f3Γf3_f3(v乛X,v乛Y,v乛Z);
        if(v乛Z.length==0):
            print("!!!!v乛Z.length==0",);
            return ; 

    if(i0或1==0):
        f3Γf3_f3(v乛Y,v乛Z,v乛X);#修正X轴
    elif(i0或1==1):
        f3Γf3_f3(v乛Z,v乛X,v乛Y);#修正Y轴
    elif(i0或1==2):
        f3Γf3_f3(v乛X,v乛Y,v乛Z);#修正Z轴

    v乛X.normalize();v乛Y.normalize();v乛Z.normalize();
    cf33[0][0]=v乛X[0];cf33[0][1]=v乛X[1];cf33[0][2]=v乛X[2];#X轴
    cf33[1][0]=v乛Y[0];cf33[1][1]=v乛Y[1];cf33[1][2]=v乛Y[2];#Y轴
    cf33[2][0]=v乛Z[0];cf33[2][1]=v乛Z[1];cf33[2][2]=v乛Z[2];#Z轴

    return cf33;
#============================================================
def vΔΔ矩阵提取轴LIB(m,s轴):
    if(s轴=="X"):
        return  Vector((m[0][0],m[1][0],m[2][0]));#X轴
    elif(s轴=="Y"):
        return  Vector((m[0][1],m[1][1],m[2][1]));#Y轴
    elif(s轴=="Z"):
        return  Vector((m[0][2],m[1][2],m[2][2]));#Z轴
    elif(s轴=="位"):
        return Vector((m[0][3],m[1][3],m[2][3]));

#////////////////////////////////////////////////
def mΔΔ保存相对于总父的子本地矩阵(o总父,o子,o孙):
    if(o子.type=="CURVE"):#子位置 是相对于CURVE 的第一个点位置
        if(o子.data.use_path):
            sp=o子.data.splines[0];
            if(sp.type=="BEZIER"):
                v4第一点位L=sp.bezier_points[0].co;#这个是v4
            else:
                v4第一点位L=sp.points[0].co;#这个是v4

            v4第一点位负L=Vector((-v4第一点位L[0],-v4第一点位L[1],-v4第一点位L[2]));
            v4第一点位负=o子.matrix_world*v4第一点位负L-o子.location;#是相对o子方向 的全局点位所以要  -o子.location

            m孙=o孙.matrix_world;m孙位全局应=m孙.copy();
            m孙位全局应[0][3],m孙位全局应[1][3],m孙位全局应[2][3]=m孙[0][3]+v4第一点位负.x,m孙[1][3]+v4第一点位负.y,m孙[2][3]+v4第一点位负.z;#加上第一点的全局位置
            m孙相对o总父L=(o总父.matrix_world.inverted())*m孙位全局应#*m孙缩放;#这个是相对总父的本地矩阵
            #print("M L==",m孙相对o总父L[0][3],m孙相对o总父L[1][3],m孙相对o总父L[2][3]);

        else:
            m孙相对o总父L=(o总父.matrix_world.inverted())*o孙.matrix_world;
    #--------------------------------------------------------------------------
    else:
        m孙相对o总父L=(o总父.matrix_world.inverted())*o孙.matrix_world;#这个是相对总父的本地矩阵

    return m孙相对o总父L;

def rotate(f3原,f3轴,ㄥ旋角):
    #return (f3原*cos(ㄥ旋角)  +  f3轴.cross(f3原)*sin(ㄥ旋角)  +  f3轴*(1-cos(ㄥ旋角))*(f3原.dot(f3轴)) ;
    f3巜f3Χf(f3原,cos(ㄥ旋角))  +  f巜f3Γf3(f3轴,f3原)*sin(ㄥ旋角)  + f3巜f3Χf( f3巜f3Χf(f3轴,(1-cos(ㄥ旋角))),f巜f3Γf3(f3原,f3轴));


def rotateV(v原,v轴,ㄥ旋角):
    #v__=[None,None,None];
    return  v原*cos(ㄥ旋角)  +  v轴.cross(v原)*sin(ㄥ旋角)  +  v轴*(1-cos(ㄥ旋角))*(v原.dot(v轴)) ;
    

#//////////////////////////////////////////////////
def LΔΔ保留4位小数(Lf):
    if(str(type(Lf)) in["<class 'float'>"]):
        return round(Lf,4);
    elif(str(type(Lf)) in["<class 'int'>","<class 'string'>","<class 'bool'>"]):
        return Lf;

    #----列表浮点---------------------------------------------------------------
    L2=[];Lf=list(Lf);
    for i,f in enumerate(Lf):
        if(f==1):
            f=1.000;
        L2.append(round(f,4));
    return L2;
    
#//////////////////////////////////////////////////
def LΔΔ保留几位小数LIB(Lf,i小数位):
    if(str(type(Lf)) in["<class 'float'>"]):
        return round(Lf,i小数位);
    elif(str(type(Lf)) in["<class 'int'>","<class 'string'>","<class 'bool'>"]):
        return Lf;

    #----浮点列表---------------------------------------------------------------
    L2=[];Lf=list(Lf);#这个会去掉欧拉的"XYZ" 只保留前三个
    for i,f in enumerate(Lf):
        if(f==1.0):
            f=1.000;
        L2.append(round(f,i小数位));
    return L2;

#////几何///////////////////////////////////////
def  iΔ圆心与半径LIB(f2头,f2尾,f2间,f3XYR):
    k1=k2=0;
    x1=(f2头[0]);y1=(f2头[1]);x2=(f2尾[0]);y2=(f2尾[1]);x3=(f2间[0]);y3=(f2间[1]);
    print("x1",x1,"y1",y1,"x2",x2,"y2",y2,"x3",x3,"y3",y3,)
    if((y1==y2) and (y2==y3)):
        print("NO\n");
        return  False ;

    elif((y1!=y2)and(y2!=y3)):
        k1=(x2-x1)/(y2-y1);
        k2=(x3-x2)/(y3-y2);
        print("k1=%f  k2=%f\n",k1,k2);

        if((0<=abs(k1-k2)) and (abs(k1-k2)<0.002)) :

            print("NO 2\n");
            #ΔΔ平均拉直()
            return False  ;

    a=(2*(x2-x1));
    b=(2*(y2-y1));
    #print("a=%d\n",a,"b=%d\n",b);
    c=(x2*x2+y2*y2-x1*x1-y1*y1);
    d=(2*(x3-x2));
    e=(2*(y3-y2));
    f=(x3*x3+y3*y3-x2*x2-y2*y2);

    x=(b*f-e*c)/(b*d-e*a);
    y=(d*c-a*f)/(b*d-e*a);

    #print("圆心x为%d\n", x, "圆心y为%d\n",y);
    r=sqrt((x-x1)*(x-x1)+(y-y1)*(y-y1));
    #print("半径为%d\n", r);
    f3XYR[0]=x;f3XYR[1]=y;f3XYR[2]=r;
    # return  f3XYR;
    return True ;
    
    
    
#///end////end////end////end////end////end////end////end////end////



