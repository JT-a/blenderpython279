

import bpy,sys,os,imp,random

#////print//////////////////////////////////////////
def ΔPTv巛巛(s,v):
    print("print v--------",s);
    print("%f   %f   %f"%(v[0],v[1],v[2]));

def ΔPTmLIB(s,m):
    print("print m-----------",s);
    print("X  %f   %f  %f  "%(m[0][0],m[1][0],m[2][0],m[3][0]));
    print("Y  %f   %f  %f  "%(m[0][1],m[1][1],m[2][1],m[3][1]));
    print("Z  %f   %f  %f  "%(m[0][2],m[1][2],m[2][2],m[3][2]));    
    print("LOC  %f   %f  %f  "%(m[0][3],m[1][3],m[2][3],m[3][3]));     
    
    
    
def PTvectorLIB(s,L):
    print("----PY %s------------"%(s));
    for i in L:
        print("== ",i);
    
def PTVv巛巛(s,L):
    print("----PY %s------------"%(s));
    for f3 in L:
        print("== ",f3[0],f3[1],f3[2]);
    
    