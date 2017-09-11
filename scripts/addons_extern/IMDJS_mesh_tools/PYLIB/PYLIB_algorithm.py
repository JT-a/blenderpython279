import bpy,sys,os,imp,random

from bpy.props import *
from mathutils import Matrix,Vector,Euler,Quaternion
from ctypes import*
from math import*

#////////////////////////////////////////////////
piΞ2=pi/2;
piΧ2=pi*2;

#try:
from .PYLIB_draw import*
#except:pass;
try:
    from .PYLIB_math import*
except:pass;

#=============================================================
def  iΔΔ找最近一个元素LIB(f3找,Lf3,f阈值):
    f最短=100000.0;iξ最短=-1;
    for i,f3 in enumerate(Lf3):
        if(abs(f3[0]-f3找[0])>f阈值):continue; 
        elif(abs(f3[1]-f3找[1])>f阈值):continue; 
        elif(abs(f3[2]-f3找[2])>f阈值):continue;
        f距离最短=length(f3,f3找);
        if(f距离最短>f阈值):continue;
        
        if(f距离最短<f最短):
            f最短=f距离最短;iξ最短=i;
    
    return iξ最短;
#==============================================================

#Y━━━━━━━━━━☐☐☐☐☐☐☐☐☐☐
#↑☐☐☐┃┃┃┄━/fvp3第一点位☐☐☐☐☐☐☐☐☐
#┃☐☐☐┃┃/☐/☐☐☐☐☐☐☐☐☐☐☐☐☐
#┃☐☐☐┃┆┃/☐☐☐☐☐☐☐☐☐☐☐☐☐☐
#┃☐☐☐┃┃/☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
#┃☐☐☐┃/┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
#┃☐☐☐/┃┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
#┃☐☐/┃│┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
#┃☐/☐/┃┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
#┃/━─┃┃┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
#(0,0)━━━━━━━━→X☐☐
#    ━┃━┃━┃━┃━┃奇段☐☐☐☐☐☐☐☐☐☐☐☐
#    ━ ┃  ━ ┃ ━  ┃ ━ ┃偶段☐☐☐☐☐☐☐☐☐☐☐☐☐
def f3ΔΔf3生成指数曲线LIB(f3前后key差值,i本节点已过时间,i本节时间,b是奇数,i指数):
    i位数=len(f3前后key差值);
    if(f3前后key差值==[0.0,0.0,0.0]):
        #print("zero",f3前后key差值);
        return [0.0,0.0,0.0];
    elif(f3前后key差值==[0.0,0.0,0.0,0.0]):
        #print("zero",f3前后key差值);
        return [0.0,0.0,0.0,0.0];

    #--------------------------------------------------------------------------
    f平均一段增量X=f3前后key差值[0]/i本节时间;
    f平均一段增量Y=f3前后key差值[1]/i本节时间;
    f平均一段增量Z=f3前后key差值[2]/i本节时间;

    f半节X=f3前后key差值[0]/2;f半节Y=f3前后key差值[1]/2;f半节Z=f3前后key差值[2]/2;
    if(i位数==4):
        LfW偏移反=[];
        f平均一段增量W=f3前后key差值[3]/i本节时间;
        f半节W=f3前后key差值[3]/2;
    #====前半节======================================================
    i前半时间=i本节时间//2;#时间是段数 #5//2==2;
    if(b是奇数):
        i后半时间=i前半时间+1;#如果段是奇,就把中间段当后半
    else:
        i后半时间=i前半时间;
    
    i本节点已过时间2=i本节点已过时间;
    #for i in range(i前半时间):#5 或 4
    if(i本节点已过时间2<i前半时间):
        if(f半节X==0):
            f偏移X=0;
        else:
            f段Ξ半节NowX=f平均一段增量X*i本节点已过时间2/f半节X;#一开始不是0,如果是中间为0
            f偏移X=f半节X*pow(f段Ξ半节NowX,i指数);

        if(f半节Y==0):
            f偏移Y=0;
        else:
            f段Ξ半节NowY=f平均一段增量Y*i本节点已过时间2/f半节Y;
            f偏移Y=f半节Y*pow(f段Ξ半节NowY,i指数);

        if(f半节Z==0):
            f偏移Z=0;
        else:
            f段Ξ半节NowZ=f平均一段增量Z*i本节点已过时间2/f半节Z;
            f偏移Z=f半节Z*pow(f段Ξ半节NowZ,i指数);


        if(i位数==4):
            if(f半节W==0):
                f偏移W=0;
            else:
                f段Ξ半节NowW=f平均一段增量W*i本节点已过时间2/f半节W;
                f偏移W=f半节W*pow(f段Ξ半节NowW,i指数);


    #----后半节----------------------------------------------------------------
    else:
        i本节点已过时间2=i后半时间-(i本节点已过时间2-i前半时间);#虚拟时间 反过来
        if(f半节X==0):
            f偏移X=0;
        else:
            f段Ξ半节NowX=f平均一段增量X*i本节点已过时间2/f半节X;#一开始不是0,如果是中间为0
            f偏移X=f半节X*pow(f段Ξ半节NowX,i指数);

        if(f半节Y==0):
            f偏移Y=0;
        else:
            f段Ξ半节NowY=f平均一段增量Y*i本节点已过时间2/f半节Y;
            f偏移Y=f半节Y*pow(f段Ξ半节NowY,i指数);

        if(f半节Z==0):
            f偏移Z=0;
        else:
            f段Ξ半节NowZ=f平均一段增量Z*i本节点已过时间2/f半节Z;
            f偏移Z=f半节Z*pow(f段Ξ半节NowZ,i指数);


        if(i位数==4):
            if(f半节W==0):
                f偏移W=0;
            else:
                f段Ξ半节NowW=f平均一段增量W*i本节点已过时间2/f半节W;
                f偏移W=f半节W*pow(f段Ξ半节NowW,i指数);


        f偏移X=f3前后key差值[0]-f偏移X;f偏移Y=f3前后key差值[1]-f偏移Y;f偏移Z=f3前后key差值[2]-f偏移Z;
        if(i位数==4):
            f偏移W=f3前后key差值[3]-f偏移W;

    #print("i==",i位数);
    if(i位数==4):
        return f偏移X,f偏移Y, f偏移Z,f偏移W;
    return f偏移X,f偏移Y, f偏移Z;
    pass

#====画贝兹曲线=================================================
#====计算多项式的系数C(i点数,k)   ==========================================
def  dΔΔ绘多项式系数(i点数,k):
    d=1;
    for i in range(1,i点数):
        d*=i;
    for i in range(1,k+1):
        d/=i;
    for i in range(1,i点数-k):
        d/=i;
    return d;

    
#====bezier根据控制点，曲线上的m个点  =====================================
def ΔΔ画bezier曲线LIB(i画点数,Lv网点位序):
    #====计算Bezier曲线上点的坐标   
    def Δ绘曲线点(t,Lv网点位序):
        x=0;y=0;   z=0;
        i网点数G=len(Lv网点位序);
        for i in range(i网点数G):
            Ber=dΔΔ绘多项式系数(i网点数G,i)*pow(t,i)*pow(1-t,i网点数G-1-i);
            x+=Lv网点位序[i].x*Ber;y+=Lv网点位序[i].y*Ber;z+=Lv网点位序[i].z*Ber;

        #putpixel((int)x,(int)y,GREEN);
        LIBG.L条序Lv线段序画LIB.append(Vector ((x,y,z)));

    for i in range(i画点数+1):
        f当前ξΞ画点数=i/i画点数;
        Δ绘曲线点(f当前ξΞ画点数,Lv网点位序);


#==============================================================
def ΔΔ画B样条曲线LIB(self,Lv):
    ξ点序=len(Lv)-1;
    p1=Vector((0,0,0));p2=Vector((0,0,0));
    #Lx=[3.20,1.00,1.00,3.20,6.00,6.00,3.20,1.00];
    #Ly=[2.40,4.00,1.00,2.40,5.0,4.30,2.40,4.00];
    #LIBG.Lv位实物画LIB=[Vector(x,y,0.0)  for  x in Lx];
    
    
    p1.x=Lv[0].x;
    p1.y=Lv[0].y;#将点描到窗口下侧
    LIBG.Lv位实物画LIB.append(p1*self.fp尺寸);
    for i in range(1,ξ点序+1):
        p2.x=Lv[i].x;
        p2.y=Lv[i].y;
        #cvLine( img,p1,p2,color);//画直线
        LIBG.Lv位实物画LIB.append(p2*self.fp尺寸);
        p1=p2;


    for k in range(ξ点序-1):
        X=(Lv[k].x+Lv[k+1].x)/2;
        Y=(Lv[k].y+Lv[k+1].y)/2;
        p1.x=X;
        p1.y=Y;
        LIBG.L条序Lv线段序画LIB.append(p1*self.fp尺寸);
        U=0.0;
        for j in range(1,self.ip画点数+1):
            U=U+1.0/self.ip画点数;
            X=U*U/2*(Lv[k].x-2*Lv[k+1].x+Lv[k+2].x)  +  U*(Lv[k+1].x-Lv[k].x)  +  (Lv[k].x+Lv[k+1].x)/2;
            Y=U*U/2*(Lv[k].y-2*Lv[k+1].y+Lv[k+2].y)  +  U*(Lv[k+1].y-Lv[k].y)  +  (Lv[k].y+Lv[k+1].y)/2;
            p2.x=X;
            p2.y=Y;
            #cvLine( img,p1,p2,color);//画曲线
            LIBG.L条序Lv线段序画LIB.append(p2*self.fp尺寸);
            p1=p2;

def Δ插值f2LIB(f2一,f2二,f比例):
    pass
    
    
def min(f3):
    f最小=10000000;
    for i in range(3):
        f=f3[i];
        if(f<f最小):#>>>>
            f最小=f;
    return f最小;
    
def max(f3):
    f最大=-10000000;
    for i in range(3):
        f=f3[i];
        if(f>f最大):#< < < 
            f最大=f;
    return f最大;
    
def clamp_min(this):
    if(f最小>this):
        this=f最小;
def clamp_max(this):
    if(this>f最大):
        this=f最大;
#==============================================================
#----毛缩放-----------------------------------------------------------------
#☐☐☐☐☐☐        
#☐↑\☐☐
#☐┃☐┃
#☐┃┃☐☐
#☐┃│↗☐☐
#☐┃/☐☐
#☐┃☐☐
#☐毛根点☐☐☐
                
def LvΔΔ缩放向量序LIB(Lv,v旋转点,f缩放倍数):
    Lv向量scale=[];
    for i,v in enumerate(Lv):
        Lv向量scale.append(v旋转点+(v-v旋转点)*f缩放倍数);
    return Lv向量scale;
    

        
        
        

