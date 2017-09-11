
import bpy,sys,os,imp,random

from bpy.props import *
from mathutils import Matrix,Vector,Euler
from ctypes import*
from bpy_extras import object_utils
import bmesh
from math import*

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
    
    
#——————————————————————————————————————————————————————
def Δ删除meshLIB(mesh):
    if(mesh!=None):
        mesh.user_clear();bpy.data.meshes.remove(mesh);     
#////////////////////////////////////////////////
piΞ2=pi/2;
piΧ2=pi*2;
    #                     
    #        0     0     1       1        2      2       3      3      4
    #       ●----●━━━●-----●----->
    #                  bmv左   bmv右     bmv下一点
    #                     
global i几条连选边G;
def Δ连选(Lbme所有选,Lbme目前共选,LL序v选点位,LLbmv选,LLbme连选,bme随机边):
    global i几条连选边G;
    bmv左=bme随机边.verts[0];bmv右=bme随机边.other_vert(bmv左);#    o━━━o
    LL序v选点位[i几条连选边G].append(bmv左.co);LL序v选点位[i几条连选边G].append(bmv右.co);#[v左,v右,v右右,]
    LLbmv选[i几条连选边G].append(bmv左);LLbmv选[i几条连选边G].append(bmv右);
    LLbme连选[i几条连选边G].append(bme随机边);Lbme目前共选.append(bme随机边);
    #----往左添加co---------------------------------------------------------------
    bme随机边右=bme随机边;#随机边会变化 所以要分左右,开始是同一条
    bme随机边左=bme随机边;
    i选边数=len(Lbme所有选)+1;i选边数2=len(Lbme所有选)+1;
    while(i选边数>0):
        for bme连选 in bmv左.link_edges: #Edges connected to this vertex (read-only).#  ━━━o━━━
                                                                    #Type : BMElemSeq of BMVert                                 #            bmv左
            if (bme连选.select and bme连选 !=bme随机边左): # 另一条选边
                bmv下一点 = bme连选.other_vert(bmv左);print("L ADD==",bmv左.index,bmv下一点);
                #bmv随机点的下一个点 <----o━━━o━━━o
                #                                          bmv下一点    bmv左
                LL序v选点位[i几条连选边G].insert(0,bmv下一点.co);#插到前面
                LLbmv选[i几条连选边G].insert(0,bmv下一点);
                LLbme连选[i几条连选边G].insert(0,bme连选);Lbme目前共选.append(bme连选);
                bmv左=bmv下一点;bme随机边左=bme连选;
                break;
        i选边数-=1;
    #----往右添加co---------------------------------------------------------------;
    while(i选边数2>0):
        for bme连选 in bmv右.link_edges: #Edges connected to this vertex (read-only).
                                                                    #Type : BMElemSeq of BMVert
            if (bme连选.select and bme连选 !=bme随机边右): # 另一条选边
                bmv下一点 = bme连选.other_vert(bmv右); print("R ADD==",bmv右.index);
                #bmv随机点的下一个点  o━━━o━━━o---->
                #                                                    bmv右     bmv下一点
                LL序v选点位[i几条连选边G].append(bmv下一点.co);
                LLbmv选[i几条连选边G].append(bmv下一点);
                LLbme连选[i几条连选边G].append(bme连选);Lbme目前共选.append(bme连选);
                bmv右=bmv下一点;bme随机边右=bme连选;
                break;
        i选边数2-=1;
    #----查找另外的边选--------------------------------------------------------------
    #print("Lbme ALL==",Lbme所有选);print("Lbme NOW==",Lbme目前共选);
    
    for bme随机边 in Lbme所有选: 
        if(bme随机边 not in Lbme目前共选):
            i几条连选边G+=1;
            LL序v选点位.append([]);LLbmv选.append([]);LLbme连选.append([]);
            Δ连选(Lbme所有选,Lbme目前共选,LL序v选点位,LLbmv选,LLbme连选,bme随机边);#1
            print("FIND DIFF",bme随机边.index);
            break;
    
#--------------------------------------------------------------------------
def LLvLLbmvLLbme_iΔΔ找连续选点(bm):
    global i几条连选边G;
    #----找到连续选点--------------------------------------------------------------
    Lbme所有选 = [] ;#Lbme所有边 = [] ;
    print("bmesh",len(bm.edges));
    for bme in bm.edges: #This meshes bme sequence (read-only).Type : BMEdgeSeq
        #Lbme所有边.append(bme);
        if (bme.select):
            Lbme所有选.append(bme);
    if(len(Lbme所有选)<1):
        print("NO EDGE SELECT",);
        return None,None,None;
    
    
    #print("LR==",bmv左,bmv右);                                                                                                                     #bmv左     bmv右
    LL序v选点位=[];
    LLbmv选=[];
    Lbme目前共选=[];
    LLbme连选=[];i几条连选边G=0;
    bme随机边=Lbme所有选[0];
    LL序v选点位.append([]);LLbmv选.append([]);LLbme连选.append([]);
    Δ连选(Lbme所有选,Lbme目前共选,LL序v选点位,LLbmv选,LLbme连选,bme随机边);#0
        
    print("LLbmv==",LLbmv选,i几条连选边G);#√
    return LL序v选点位,LLbmv选,LLbme连选,i几条连选边G;

#==============================================================
#☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
#☐☐☐☐☐☐☐☐☐☐☐bme连2☐☐☐☐☐☐☐☐☐☐
#☐☐○☐☐☐○☐☐☐○☐☐☐○bmv下一个☐☐
#☐☐┃☐☐☐┃☐☐☐┃☐☐☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐
#☐☐┃☐╋☐┃☐╋☐┃☐╋☐┃bme连☐☐☐☐☐☐☐☐☐☐☐☐☐
#☐☐┃☐☐☐┃☐☐☐┃☐☐☐┃☐☐☐☐☐☐☐☐☐☐☐
#☐☐●━━━●━━━●━━━●bmv连选☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
#                                                    bme此边
def LiLbmvLbmeΔΔ找连续选点传播单行(Lbmv连选前一行,Lbmv连选,Lbme连选):#假设只选了边缘
    #Lbme连选Copy=Lbme连选.copy();
    Lbmv下一行=[];Lbme下一行=[];
    Lξ点传播=[];
    i选点数单行=len(Lbme连选);
    for  ξ点,bmv连选 in enumerate(Lbmv连选): 
        if(ξ点!=i选点数单行):#不是最后 一个序
            bme此边=Lbme连选[ξ点];
        else:#最后一个序  共用前一个序的边
            bme此边=Lbme连选[ξ点-1];
        #----找到一个点-------------------------------------------------------------
        b找到=False;
        """
        for bme连 in bmv连选.link_edges: 
            print(bmv连选.index,"LINKS E==",bme连.index);
        print("-------------------",);
        """
        for bme连 in bmv连选.link_edges: 
            if (bme连!=bme此边):
                for bmf连面 in bme连.link_faces:
                    if(bmf连面 in bme此边.link_faces):#两边共面,找到
                        bmv下一个=bme连.other_vert(bmv连选);
                        if(bmv下一个 not in Lbmv连选前一行):
                            Lξ点传播.append(bmv下一个.index);
                            Lbmv下一行.append(bmv下一个);
                            if(ξ点!=i选点数单行):#不是最后 一个序    
                                for bme连2 in bmv下一个.link_edges: 
                                    if(bme连2 !=bme连):
                                        if(bme连2 in bmf连面.edges):#找到连边2
                                            Lbme下一行.append(bme连2);
                                            break;
                            
                            b找到=True;
                            break;
                        
            if(b找到):
                break;
    #print("LiTRANS=",Lξ点传播);
    return Lξ点传播,Lbmv下一行,Lbme下一行;
  
#////////////////////////////////////////////////
def Δ得点权LIB(oA,vgDens,vg,L点序f权__):
    id=oA.data;Cmv=id.vertices;L点序f权__=[-1]*len(Cmv);
    for ξ点,mv in enumerate(Cmv):
        Cvge点=mv.groups;
        try:L点序f权__[ξ点]=vg.weight(ξ点);#看这点有没有权,如果不成功就是-1
            #if(ξ点==1):print("dens",vgDens,vgDens.weight(ξ点));
        except:pass;
        
        

def iΔ得三角面数LIB(o):
    id=oA.data;Cmv=id.vertices;mA=oA.matrix_world;i艹三角面数=0;
    for ξ面,mp全部 in enumerate(id.polygons):
        i面点数=len(mp全部.loop_indices);
        #----三角面---------------------------------------------------------------
        if(i面点数==3):
            i艹三角面数+=1;
        #====四边面====================================================
        elif(i面点数==4):
            i艹三角面数+=2;
        elif(i面点数>4):
            i艹三角面数+=(i面点数-3);
    
    return i艹三角面数;
    
    
"""
  
#////测试//////////////////////////////////////
try:
    oA=bpy.context.active_object;id=oA.data;
    bm = bmesh.from_edit_mesh(id);

    #----找到连续选 点--------------------------------------------------------------
    LL序v选点位,LLbmv连选,LLbme连选,i几条连选边G=LLvLLbmvLLbme_iΔΔ找连续选点(bm);#这个v选点位是引用
    LLbmv连选First=LLbmv连选.copy();

    for i in range(i几条连选边G+1):
        Lbmv连选=LLbmv连选[i];Lbme连选=LLbme连选[i];
        
        Lξ点传播,Lbmv下一行,Lbme下一行=LiLbmvLbmeΔΔ找连续选点传播单行([],Lbmv连选,Lbme连选);#第一行
        i点数行=len(Lbme连选);
        LL=[[] for i in range(len(Lξ点传播))];#[[],[],...]
        
        #I=4;
        while(len(Lξ点传播)>0):
            print("L while==",Lξ点传播);
            for i,ξ点 in enumerate(Lξ点传播):
                LL[i].append(ξ点);#[[0],[1],...]
            Lbmv连选Pre=Lbmv下一行;
            Lξ点传播,Lbmv下一行,Lbme下一行=LiLbmvLbmeΔΔ找连续选点传播单行(Lbmv连选,Lbmv下一行,Lbme下一行);
            #print("L==",Lξ点传播);
            Lbmv连选=Lbmv连选Pre;
            
            #for i,iξ in enumerate(Lξ点传播):print("THIS I==",iξ,Lbmv下一行[i].index);
            #I-=1;
        print("FIRST LINE==",LLbmv连选First);
        print("LL==",LL,i几条连选边G);
            
    print("-------------------------------------------------------------------------",);

except:pass;    
"""
#////////////////////////////////////////////////













#////end////end////end////end////end////end////end////end////








