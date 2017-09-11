
import bpy,sys,os,imp,random

from bpy.props import *
from mathutils import Matrix,Vector,Euler
from ctypes import*
from bpy_extras import object_utils
import bmesh
from math import*

#path目录 = os.path.dirname(__file__); #本py文件所在目录 #E"\blender\addons\PYLIB
#s此文件夹=os.path.basename(path目录);  #PYLIB

#Lpath=path目录.split("\\");s上级文件夹=Lpath[-2];

#path上级目录=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

#if(path上级目录 not in sys.path):sys.path.append(path上级目录);
    
#sys.path.append("..") #加入上级目录路径
#sys.path.append(".") #加入本级目录路径 
#print (os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) );
#print("path上级目录==",path上级目录);
#print("sys.path==",sys.path);
#print("sys.modules==",sys.modules.keys());
from .PYLIB_main import 目录PYLIB上级
if("PYLIB.global_var" in sys.modules):
    print("find PYLIB.global_var",);
    LIBG = sys.modules["PYLIB.global_var"];
else:
    if("PYLIB"in sys.modules):
        import  PYLIB.global_var as LIBG;
    else:    
        print("==",目录PYLIB上级+".PYLIB.global_var");
        exec("import "+目录PYLIB上级+".PYLIB.global_var as LIBG");#√

from .PYLIB_math import Lcf3巜Lf3,Lf3巜Lcf3,f3十f3_

#////////////////////////////////////////////////

def ΔΔ清除gl2dLIB():
    LIBG.Dn开始f2画LIB.clear();
    
def ΔΔ清除glLIB():
    """
    LIBG.Lv位X轴LIB.clear();LIBG.Lv位顶LIB.clear();LvX位LIB.clear();
    LIBG.Lv物转位绿顶LIB.clear();LIBG.Lv位叉积LIB.clear();LIBG.LvX位绿LIB.clear();
    
    Lv位矩阵xLIB.clear();Lv位矩阵yLIB.clear();Lv位矩阵zLIB.clear();
    Lv位Q矩阵xLIB.clear();Lv位Q矩阵yLIB.clear();Lv位Q矩阵zLIB.clear();
    """
    #----矩阵----------------------------------------------------------------
    LIBG.L物序L4v位矩阵画LIB.clear();
    #--------------------------------------------------------------------------
    LIBG.Lv位实物画LIB.clear();LIBG.Lv位实物顶LIB.clear();LIBG.L条序Lv线段序画LIB.clear();LIBG.Lv位实物XLIB.clear();
    LIBG.Lcf3位画LIB=[];LIBG.Lcf3位蓝画LIB=[];
    #----法线------------------------------------------------------------------
    LIBG.Lv法线位画LIB.clear();LIBG.Lv法线顶位画LIB.clear();LIBG.L条序LΩωv线段画LIB.clear();
    #----字------------------------------------------------------------------
    LIBG.Lv三角面位画LIB.clear();   
    
    print("CLEAR~~~Lv LIBG",);
    
def Δ转画矩阵LIB(L4cf3):
    LIBG.L物序L4v位矩阵画LIB.append([]);
    LIBG.L物序L4v位矩阵画LIB[0]=[[]]*4;

    LIBG.L物序L4v位矩阵画LIB[0][0]=[L4cf3[3][0],L4cf3[3][1],L4cf3[3][2]];#位
    LIBG.L物序L4v位矩阵画LIB[0][1]=[L4cf3[0][0],L4cf3[0][1],L4cf3[0][2]];#X轴
    LIBG.L物序L4v位矩阵画LIB[0][2]=[L4cf3[1][0],L4cf3[1][1],L4cf3[1][2]];#Y轴
    LIBG.L物序L4v位矩阵画LIB[0][3]=[L4cf3[2][0],L4cf3[2][1],L4cf3[2][2]];#Z轴
    
    f3十f3_(LIBG.L物序L4v位矩阵画LIB[0][0],LIBG.L物序L4v位矩阵画LIB[0][1]);
    f3十f3_(LIBG.L物序L4v位矩阵画LIB[0][0],LIBG.L物序L4v位矩阵画LIB[0][2]);
    f3十f3_(LIBG.L物序L4v位矩阵画LIB[0][0],LIBG.L物序L4v位矩阵画LIB[0][3]);
    print("LIBG.L物序L4v位矩阵画LIB[0]",LIBG.L物序L4v位矩阵画LIB[0]);

def Δ转画物位LIB(Lcf3):
    for f3 in Lcf3:
        LIBG.Lv位实物画LIB.append([*f3]);#Vector(
    print("LIBG.Lv位实物画LIB",LIBG.Lv位实物画LIB);
#////画线///////////////////////////////////////
import bgl,blf;
vX=Vector((2.2,0.0,0.0));vY=Vector((0.0,0.2,0.0));vZ=Vector((0.0,0.0,5.0));
v零=Vector((0.0,0.0,0.0));v2零=Vector((0.0,0.0));

Lv2屏位=[v2零,v2零];

def Δ画线3dLIB(self,context):#L2v位
    #font_id = 0
    #if(self.v物位==Vector()):return ;
    bgl.glEnable(bgl.GL_BLEND);
    """"""
    bgl.glBegin(bgl.GL_LINES);#●●ΧGL_LINES  GL_POINT  GL_LINE_STIPPLE
    bgl.glColor3f(*LIBG.t3白LIB); 
    #bgl.glPointSize(20);

    #print("DRAW　Lv位实物画LIB==",LIBG.Lv位实物画LIB);
    #----实物---------------------------------------------------------------
    for i,v物位 in enumerate(LIBG.Lv位实物画LIB):
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v物位);
        #Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv位实物顶LIB[i]);
        Lv2屏位[1][0]=Lv2屏位[0][0]#.copy();
        Lv2屏位[1][1] =Lv2屏位[0][1]+10.0;#画线高
        #if(i==0):print("",v物位,LIBG.Lv位顶LIB[i]);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点

        #bgl.glVertex2f(*Lv2屏位[0]);

        #Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv位实物XLIB[i]);
        #if(i==0):print("",v物位,LIBG.Lv位顶LIB[i]);
        #for v2屏位 in Lv2屏位:
            #bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点    
    #----Lcf3位画LIB---------------------------------------------------------------
    bgl.glColor3f(*LIBG.t3粉紫LIB); 
    for i,cf3物位 in enumerate(LIBG.Lcf3位画LIB):
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,Vector(cf3物位));
        #Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv位实物顶LIB[i]);
        Lv2屏位[1][0]=Lv2屏位[0][0]#.copy();
        Lv2屏位[1][1] =Lv2屏位[0][1]+50.0;#画线高
        #if(i==0):print("",v物位,LIBG.Lv位顶LIB[i]);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点
            
    bgl.glColor3f(*LIBG.t3蓝LIB); 
    for i,cf3物位 in enumerate(LIBG.Lcf3位蓝画LIB):
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,Vector(cf3物位));
        #Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv位实物顶LIB[i]);
        Lv2屏位[1][0]=Lv2屏位[0][0]#.copy();
        Lv2屏位[1][1] =Lv2屏位[0][1]+50.0;#画线高
        #if(i==0):print("",v物位,LIBG.Lv位顶LIB[i]);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点    
    """
    #----采样物---------------------------------------------------------------
    bgl.glColor4f(*LIBG.t4青LIB);
    for i,v物位 in enumerate(LIBG.L条序Lv线段序画LIB):
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v物位);
        #Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,self.v物位+vZ);
        #Lv2屏位[1]=Lv2屏位[0].copy();Lv2屏位[1][1] =Lv2屏位[0][1]+10.0;#画线高
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv法线顶位画LIB[i]);

        #if(i==0):print("",v物位,LIBG.Lv位顶LIB[i]);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点
        
    
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv法线顶位画LIB[i]);    
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LvX位LIB[i]);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点
    #--------------------------------------------------------------------------
    bgl.glColor4f(*LIBG.t4深绿LIB);
    for i,v物位 in enumerate(LIBG.L条序Lv线段序画LIB):
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v物位);
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv物转位绿顶LIB[i]);

        #if(i==0):print("",v物位,LIBG.Lv位顶LIB[i]);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点        
        
        #----X----------------------------------------------------------------
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv物转位绿顶LIB[i]);    
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.LvX位绿LIB[i]);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点        
    #----黄色-----------------------------------------------------------------
    bgl.glColor4f(*LIBG.t4黄LIB);
    for i,v物位 in enumerate(LIBG.L条序Lv线段序画LIB):        
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv物转位绿顶LIB[i]);    
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv位X轴LIB[i]);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点  
    #----叉积-----------------------------------------------------------------
    bgl.glColor3f(*LIBG.t3紫LIB);
    for i,v物位 in enumerate(LIBG.L条序Lv线段序画LIB):        
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv物转位绿顶LIB[i]);    
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv位叉积LIB[i]);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点       

    """
    
    
    """"""   
    #----蓝曲线----------------------------------------------------------------
    bgl.glColor4f(0.0, 1.0, 1.0,1.0);#蓝色
    #bgl.glBegin(bgl.GL_LINES);
    #i凵=len(LIBG.Lv位实物画LIB);#print("i凵",i凵);
    
    for Lv物位蓝 in LIBG.L条序Lv线段序画LIB:
        v2位pre=None;
        for v物位 in Lv物位蓝:
            Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v物位);
            if(v2位pre):
                bgl.glVertex2f(v2位pre[0],v2位pre[1]);#画一个点
                bgl.glVertex2f(Lv2屏位[0][0],Lv2屏位[0][1]);#画另一个点,连成一个线段
            
            v2位pre=Lv2屏位[0] ;
            #gl.glVertex2f(Lv2屏位[0][0],Lv2屏位[0][1]);
            
    #----画一段段线--------------------------------------------------------
    for L2cf3物位蓝 in LIBG.LL2cf3线段序画LIB:
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,Vector(L2cf3物位蓝[0]));
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,Vector(L2cf3物位蓝[1]));
        bgl.glVertex2f(Lv2屏位[0][0],Lv2屏位[0][1]);#画一个点
        bgl.glVertex2f(Lv2屏位[1][0],Lv2屏位[1][1]);#画另一个点,连成一个线段

            #gl.glVertex2f(Lv2屏位[0][0],Lv2屏位[0][1]);        
    #----法线-----------------------------------------------------------------
    bgl.glColor3f(0.0, 1.0, 1.0);#青色
    for i,v物位 in enumerate(LIBG.Lv法线位画LIB):
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v物位);
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv法线顶位画LIB[i]);
        #Lv2屏位[1]=Lv2屏位[0].copy();Lv2屏位[1][1] =Lv2屏位[0][1]+30.0;for v2屏位 in Lv2屏位:bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画线高
        
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点
            
    bgl.glEnable(bgl.GL_POINT_SMOOTH);
    bgl.glPointSize(6);
    #bgl.glBegin(bgl.GL_POINTS );
    #bgl.glBegin(bgl.GL_TRIANGLES);
    
    #----线段----------------------------------------------------------------
    #bgl.glColor3f(*LIBG.t3绿LIB);#绿色
    #bgl.glColor4f(0.0, 1.0, 1.0,1.0);#青色
    #bgl.glRecti(15, 10 , 10 + 60, 10  - 60);
    iI=0.0;iJ=0.5;iK=0.5;
    for Lv线段 in LIBG.L条序LΩωv线段画LIB:    
        v2位pre=None;
        #bgl.glBegin(bgl.GL_POLYGON);
        for i,v线段 in enumerate(Lv线段):
            if(i==0):
                Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v线段);
                fY原来=Lv2屏位[0] [1];
                Lv2屏位[0] [1]+=30;#线高
                bgl.glVertex2f(Lv2屏位[0][0],Lv2屏位[0][1]);
                bgl.glVertex2f(Lv2屏位[0][0],fY原来);#画一节
            else:
                Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v线段);
                #if(v2位pre):
                #bgl.glBegin(bgl.GL_QUADS);
                #bgl.glBegin(bgl.GL_POINTS );
                bgl.glVertex2f(Lv2屏位[0][0],Lv2屏位[0][1]);
                bgl.glVertex2f(Lv2屏位[1][0],Lv2屏位[1][1]);#画一节
        
            #v2位pre=Lv2屏位[0] ;
        bgl.glColor4f(iK, iJ, iI,1.0);
        if(iI>=1.0):iI=0.1;
        if(iJ>=1.0):iJ=0.1;
        if(iK>=1.0):iK=0.1;
        else:
            iI+=0.05; iJ+=0.1; iK+=0.1;
            
    #----画矩阵--------------------------------------------------------------
    iI=0.2;iJ=0.5;iK=0.6;
    v2位=None;
    for i物序, L4v位矩阵 in enumerate(LIBG.L物序L4v位矩阵画LIB):        
        #bgl.glColor3f(*LIBG.Lt3红绿蓝LIB[i物序]); 
        for i,v位 in  enumerate(L4v位矩阵):
            if(i==0):
                v2位= view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v位);
            else:
                bgl.glColor3f(*LIBG.Lt3红绿蓝LIB[i-1]);
                Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v位);    
                #bgl.glColor3f(*LIBG.t3红LIB);
                bgl.glVertex2f(v2位[0], v2位[1]);#画一个点
                bgl.glVertex2f(Lv2屏位[0][0],Lv2屏位[0][1]);#画另一个点,连成一个线段
                #blf.size(0, 13, 72);txt_width, txt_height = blf.dimensions(0, str(25));blf.position(0,0.0,0.0, 0);blf.draw(0, str(25));
        
        """
        bgl.glColor4f( iI,iJ,iK,1.0);
        if(iI>=1.0):iI=0.1;
        if(iJ>=1.0):iJ=0.1;
        if(iK>=1.0):iK=0.1;
        else:
            iI+=0.4; iJ+=0.3; iK+=0.2;
        """
    #----画Q矩阵--------------------------------------------------------------
    """
    for i,v物位 in enumerate(Lv位Q矩阵xLIB):        
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v零);    
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v物位);   
        bgl.glColor3f(*LIBG.t3深红LIB);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点
        #blf.size(0, 13, 72);txt_width, txt_height = blf.dimensions(0, str(25));blf.position(0,0.0,0.0, 0);blf.draw(0, str(25));

        
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v零);    
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,Lv位Q矩阵yLIB[i]);   
        bgl.glColor3f(*LIBG.t3深绿LIB);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点 
            
        Lv2屏位[0] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,v零);    
        Lv2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,Lv位Q矩阵zLIB[i]);   
        bgl.glColor3f(*LIBG.t3深蓝LIB);
        for v2屏位 in Lv2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点     
    """
    #--------------------------------------------------------------------------
    bgl.glDisable(bgl.GL_BLEND);
    bgl.glEnd();
    #print("draw",Lv2屏位);

#==============================================================
def ΔΔ画字(self, context):
    # polling
    #print("DRAW---text");
    #if (context.mode != "EDIT_MESH"):return;
    
    # get screen information
    region = context.region
    屏幕X半 = region.width / 2
    屏幕Y半 = region.height / 2
    width = region.width
    height = region.height

    # get matrices
    view_mat = context.space_data.region_3d.perspective_matrix
    m物Π = context.active_object.matrix_world
    m果Π = view_mat * m物Π

    text_height = 13
    blf.size(0, text_height, 72)
    #--------------------------------------------------------------------------
    def Δ画字(index, v中间):

        vec = m果Π * v中间 ;# order is important
        # dehomogenise
        #vec =Vector((vec[0] / vec[3], vec[1] / vec[3], vec[2] / vec[3]));#
        vec =Vector((vec[0] / vec[2], vec[1] / vec[2]));#, vec[2] / vec[3]

        x = int(屏幕X半 + vec[0] *屏幕X半);
        y = int(屏幕Y半 + vec[1] *屏幕Y半);

        index = str(index);

        txt_width, txt_height = blf.dimensions(0, index);
        ''' draw text '''
        blf.position(0, x-(txt_width/2), y-(txt_height/2), 0);
        blf.draw(0, index);
        
    scene = context.scene;
    #me = context.active_object.data;
    #bm = bmesh.from_edit_mesh(me);
    #print("len Lv三角面位画LIB==",len(LIBG.Lv三角面位画LIB));
    bgl.glColor3f(*LIBG.t3粉紫LIB);
    for i, v三角面位  in enumerate(LIBG.Lv三角面位画LIB):
        Δ画字(i,v三角面位);#.to_4d()
                
#////////////////////////////////////////////////
from bpy_extras import view3d_utils
global areaG;areaG=None;
class 卐画画lib卐Operator(bpy.types.Operator):
    bl_idname = "op.draw_line_lib"
    bl_label = "draw_line_lib"
    bl_description = "draw_line_lib"

    #cp群组物体= CollectionProperty(type=卐群组物体卐PropertyGroup);

    _handle = None;_handle字= None;

    vZ=Vector((0.0,0.0,0.0));
    #======================================================
    """
    @classmethod
    def poll(cls, context):
        return context.mode=="OBJECT";
    """
    def modal(self, context, event):
        global  areaG;
        #if (context.area):context.area.tag_redraw();
        
        #----刷新界面--------------------------------------------------------
        """"""
        if(not areaG):
            screen=bpy.context.screen;
            for area in screen.areas:
                if(area.type=="VIEW_3D"):
                    areaG=area;
                    area.tag_redraw();
        else:
            areaG.tag_redraw();#为了不用每次都找 area
        
        #----停止--------------------------------------------------------------
        """"""
        #print("LIBG.Li显示3dLIB[0]==",LIBG.Li显示3dLIB[0]);
        if(LIBG.Li显示3dLIB[0]==-1):
            LIBG.Li显示3dLIB[0]=0;
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW');
            #bpy.types.SpaceView3D.draw_handler_remove(self._handle字, 'WINDOW');
            #print("REMOVE modal==",self._handle);
            ΔΔ清除glLIB();areaG=None;#●●防止这个areaG之前记录为其它窗口
            print("remove handle 1 ~~~~",len(LIBG.Lv位实物画LIB));
            #return {"CANCELLED"};
            return {"FINISHED"};
        
        return {"PASS_THROUGH"};
        
    #==============================================================
    def invoke(self, context, event):
        #return {"FINISHED"};
        if(LIBG.Li显示3dLIB[0]< 1):
            LIBG.Li显示3dLIB[0]=1;
            print("BP invoke==",LIBG.Li显示3dLIB[0],len(LIBG.Lv位实物画LIB),len(LIBG.L条序LΩωv线段画LIB) );
            #----增加手柄----------------------------------------------------------------
            self._handle = bpy.types.SpaceView3D.draw_handler_add(Δ画线3dLIB,(self, context), 'WINDOW', 'POST_PIXEL');
            #self._handle字 = bpy.types.SpaceView3D.draw_handler_add(ΔΔ画字,(self, context), 'WINDOW', 'POST_PIXEL');
            context.window_manager.modal_handler_add(self);#●●这个必须要增加,不然不能连续画#(self==Operator) to call  Return type: boolean
            print("add handle+++",);
        else:
            LIBG.Li显示3dLIB[0]=-1;

        #return {"CANCELLED"};
        return {"RUNNING_MODAL"};

     
bpy.utils.register_class(卐画画lib卐Operator) ;

#////2d//////////////////////////////////////////
Lf2屏位=[v2零,v2零];
def Δ画线2dLIB(self,context):#L2v位
    #font_id = 0
    #if(self.v物位==Vector()):return ;
    #bgl.glEnable(bgl.GL_BLEND);
    """"""
    bgl.glBegin(bgl.GL_LINES);#●●ΧGL_LINES  GL_POINT  GL_LINE_STIPPLE
    bgl.glColor3f(*LIBG.t3粉紫LIB); 
    bgl.glPointSize(20);

    for n,f2画LIB in LIBG.Dn开始f2画LIB.items():
        Lf2屏位[0] =f2画LIB;
        #Lf2屏位[1] = view3d_utils.location_3d_to_region_2d(context.region, context.space_data.region_3d,LIBG.Lv位实物顶LIB[i]);
        Lf2屏位[1][0]=Lf2屏位[0][0]#.copy();
        Lf2屏位[1][1] =Lf2屏位[0][1]+40.0;#画线高
        #if(i==0):print("",f2位,LIBG.Lv位顶LIB[i]);
        for v2屏位 in Lf2屏位:
            bgl.glVertex2f(v2屏位[0], v2屏位[1]);#画一个点
            
    #bgl.glDisable(bgl.GL_BLEND);
    #bgl.glPointSize(5);
    bgl.glEnd();
    
global area2G;area2G=None;
class 卐画画2dlib卐Operator(bpy.types.Operator):
    bl_idname = "op.draw_line_2d_lib"
    bl_label = "draw_line_2d_lib"
    bl_description = "draw_line_2d_lib"

    #cp群组物体= CollectionProperty(type=卐群组物体卐PropertyGroup);

    _handle = None;_handle字= None;

    def modal(self, context, event):
        global area2G;
        #if (context.area):context.area.tag_redraw();
        
        #----刷新界面--------------------------------------------------------
        """"""
        if(not area2G):
            screen=bpy.context.screen;
            for area in screen.areas:
                if(area.type=="VIEW_3D"):
                    area2G=area;
                    area.tag_redraw();
        else:
            area2G.tag_redraw();#为了不用每次都找 area
        
        #----停止--------------------------------------------------------------
        """"""
        if(LIBG.Li显示2dLIB[0]==-1):
            if(LIBG._handle2d):
                bpy.types.SpaceNodeEditor.draw_handler_remove(LIBG._handle2d, 'WINDOW');
            LIBG.Li显示2dLIB[0]=0;
            #bpy.types.SpaceNodeEditor.draw_handler_remove(self._handle字, 'WINDOW');
            #print("REMOVE modal==",self._handle);
            ΔΔ清除gl2dLIB();
            #self.report({"ERROR"},"remove draw handle 2d");#"INFO" "ERROR" "DEBUG" "WARNING"
            #return {"CANCELLED"};
            return {"FINISHED"};
        
        return {"PASS_THROUGH"};
        
    #==============================================================
    def invoke(self, context, event):
        if(LIBG.Li显示2dLIB[0]< 1):
            LIBG.Li显示2dLIB[0]=1;
            print("BP invoke==",LIBG.Li显示2dLIB[0],len(LIBG.Dn开始f2画LIB));#return {"FINISHED"};
            #----增加手柄----------------------------------------------------------------
            LIBG._handle2d = bpy.types.SpaceNodeEditor.draw_handler_add(Δ画线2dLIB,(self, context), 'WINDOW', 'POST_PIXEL');
            #self._handle字 = bpy.types.SpaceNodeEditor.draw_handler_add(ΔΔ画字,(self, context), 'WINDOW', 'POST_PIXEL');
            context.window_manager.modal_handler_add(self);#(self==Operator) to call  Return type: boolean
            print("add handle++++",);
            
        else:
            LIBG.Li显示2dLIB[0]=-1;print("BP invoke1==",LIBG.Li显示2dLIB[0]);

        return {"RUNNING_MODAL"};

        
bpy.utils.register_class(卐画画2dlib卐Operator) ;

#////////////////////////////////////////////////
def ΔΔ画画3dLIB(self):
    bpy.ops.op.draw_line_lib("INVOKE_DEFAULT");
    if(LIBG.Li显示3dLIB[0]==-1):self.report({"WARNING"},"除移手柄==%d"%LIBG.Li显示3dLIB[0]);


#==============================================================
def ΔΔ画B样条曲线过控制点LIB(L条序Lv网点,L条序Lv输出点):

    for Lv网点 in L条序Lv网点:    
        for i in range(len(Lv网点)):
            LIBG.Lv位实物画LIB.append(Lv网点[i]);
            
    LIBG.L条序Lv线段序画LIB=L条序Lv输出点;
    """        
    for Lv输出点 in L条序Lv输出点:
        Lv=[];
        for i in range(len(Lv输出点)):
            Lv.append(Lv输出点[i]);
            
        LIBG.L条序Lv线段序画LIB.append(Lv);#条序[[v,v],[v,v],...]
    """
    print("draw INER---------------------",LIBG.b显示3dLIB[0],len(LIBG.Lv位实物画LIB));
    #bpy.ops.op.draw_line_lib("INVOKE_DEFAULT");
    
#///////////////////////////////////////////////
def ΔΔ刷新界面LIB(area,region):
    screen=bpy.context.screen;
    if(area):
        for a in screen.areas:
            if(a.type==area):#EMPTY", "VIEW_3D", "TIMELINE", "GRAPH_EDITOR", "DOPESHEET_EDITOR", "NLA_EDITOR", "IMAGE_EDITOR", "SEQUENCE_EDITOR", "CLIP_EDITOR", "TEXT_EDITOR", "NODE_EDITOR", "LOGIC_EDITOR", "PROPERTIES", "OUTLINER", "USER_PREFERENCES", "INFO", "FILE_BROWSER", "CONSOLE"
                #a.tag_redraw();#■■这个能刷新所有 region画面
                if(region):
                    for r in a.regions:#WINDOW", "HEADER", "CHANNELS", "TEMPORARY", "UI", "TOOLS", "TOOL_PROPS", "PREVIEW
                        if(r.type==region):
                            r.tag_redraw();
                            break;
                    break;
            #for s in a.spaces:
                #if(s.type=="PROPERTIES"):
                    #print(s)
                    #s.context=s模式;#["SCENE", "RENDER", "RENDER_LAYER", "WORLD", "OBJECT", "CONSTRAINT", "MODIFIER", "DATA", "BONE", "BONE_CONSTRAINT", "MATERIAL", "TEXTURE", "PARTICLES", "PHYSICS"]
    print("refresh~~",area,region);
    
#//////////////////////////////////////////////////
def ΔΔ切换到菜单LIB(s模式):
    """
    global s上次模式G;
    if(s上次模式G==s模式):
        print("IS LAST TIME",);return ;
    """
    screen=bpy.context.screen;
    for a in screen.areas:
        if(a.type=="PROPERTIES"):
            for s in a.spaces:
                if(s.type=="PROPERTIES"):
                    try:
                        s.context=s模式;
                    except:pass;

                    #s上次模式G=s模式;
                    break;
                    #["SCENE", "RENDER", "RENDER_LAYER", "WORLD", "OBJECT", "CONSTRAINT", "MODIFIER", "DATA", "BONE", "BONE_CONSTRAINT", "MATERIAL", "TEXTURE", "PARTICLES", "PHYSICS"]
            break;


def ΔΔ切换到指定spaceLIB(area类型,space类型,s模式):
    screen=bpy.context.screen;
    for a in screen.areas:
        if(a.type==area类型):#"EMPTY", "VIEW_3D", "TIMELINE", "GRAPH_EDITOR", "DOPESHEET_EDITOR", "NLA_EDITOR", "IMAGE_EDITOR", "SEQUENCE_EDITOR", "CLIP_EDITOR", "TEXT_EDITOR", "NODE_EDITOR", "LOGIC_EDITOR", "PROPERTIES", "OUTLINER", "USER_PREFERENCES", "INFO", "FILE_BROWSER", "CONSOLE"
         #print(a.type)
            for s in a.spaces:
                if(s.type==space类型):#
                    #print(s)
                    s.context=s模式;
                    break;#["SCENE", "RENDER", "RENDER_LAYER", "WORLD", "OBJECT", "CONSTRAINT", "MODIFIER", "DATA", "BONE", "BONE_CONSTRAINT", "MATERIAL", "TEXTURE", "PARTICLES", "PHYSICS"]
            break;





#////end////end////end////end////end////end////end////end////








