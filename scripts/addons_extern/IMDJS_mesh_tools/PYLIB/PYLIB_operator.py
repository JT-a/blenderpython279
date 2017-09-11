
import bpy,sys,os

from bpy.props import *
from mathutils import Matrix,Vector,Euler

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

#----物体吸---------------------------------------------------------------
class 卐激活物名给spLIB卐Operator(bpy.types.Operator):
    bl_idname = "op.imdjs_active_name_sp_lib";
    bl_label = "active_name_sp";
    bl_context='object';
    bl_description="pick the active object"
    
    sp物名=StringProperty(name="", description="", default="");
    #--------------------------------------------------------------------------
    def execute(self, context):
        oA=context.active_object;
        if(oA):
            self.sp物名=oA.name;
            print("pick up object: %s"%oA.name);
        else:
            self.report({"ERROR"},"!!! can't find node");#"INFO" "ERROR" "DEBUG" "WARNING"
        return {"FINISHED"};
    
    
        
#==============================================================










#////////////////////////////////////////////////













#////end////end////end////end////end////end////end////end////








