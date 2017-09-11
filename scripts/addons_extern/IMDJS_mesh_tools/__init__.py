
#20170219
import bpy,sys
bl_info = {
    "name": "IMDJS_mesh_tools",
    "author": "imdjs",
    "version": (2017,"0219"),
    "blender": (2, 7, 8),
    "api": 278,
    "location": "View3D > Toolbar and View3D > specials menu (W key)",
    "description": "tools for mesh modification",
    "warning": "",
    "category": "Mesh"}


    
    
#////////////////////////////////////////////////
""""""
if("PYLIB"in sys.modules):
    from PYLIB.PYLIB_main import *
else:    
    from .PYLIB.PYLIB_main import*
    
if("IMDJS_mesh_tools.PYLIB.global_var" in sys.modules):
    print("find IMDJS_mesh_tools.PYLIB.global_var",);
    LIBG = sys.modules["IMDJS_mesh_tools.PYLIB.global_var"];
else:
    try:
        import IMDJS_mesh_tools.PYLIB.global_var as LIBG;
    except:
        import PYLIB.global_var as LIBG; 

from .mesh_tools import *
#////////////////////////////////////////////////
path目录mesh_tools = os.path.dirname(__file__); #本py文件所在目录
文件夹此mesh_tools=os.path.basename(path目录mesh_tools);

dllpathMESHB="B:/mesh_tools64.dll"        
#dllpathMESHB=os.path.abspath("%s/mesh_tools32.dll" % path目录mesh_tools);
dllpathMESH=os.path.abspath("%s/mesh_tools64.dll" % path目录mesh_tools);
        
class 卐圆化选点卐Operator(bpy.types.Operator):
    bl_idname = 'mesh.round_selected_points'
    bl_label = "round_selected_points"
    bl_description = "round the selected points"
    bl_options = {'REGISTER', 'UNDO'}
    
    bp是反选序=BoolProperty(name='reverse',description='',default=False,subtype='NONE',update=None,get=None,set=None);
    bp是传播=BoolProperty(name='transmission',description='',default=False,subtype='NONE',update=None,get=None,set=None);
    bp是渐变圆=BoolProperty(name='--',description='渐变圆',default=False,subtype='NONE',update=None,get=None,set=None);    
    fp圆心偏移=FloatProperty(name='radian',description='adjust the radian ',default=0.0,min=-100.0,max=100.0,step=3,precision=2,subtype='NONE',unit='NONE',update=None,get=None,set=None);
    ep限制类型 = EnumProperty( name="clamp", description="clamp to X Y Z",items=  [("NONE","none","---","NONE",0),("X","x","---","NONE",1),("Y", "y","---.","NONE",2) ,("Z", "z","---.","NONE",3)  ,("AUTO", "auto","---.","NONE",4)  ],default="NONE");
                                                                                               
    @classmethod
    def poll(cls, context):
        oA = context.active_object
        return (oA and oA.type == 'MESH' and context.mode == 'EDIT_MESH');
        
    def draw(self, context):
        uil界 = self.layout;
        uil行2=uil界.row(align=True);
        uil行2.prop_enum(self,  "ep限制类型", value="NONE", text_ctxt="", translate=True, icon="NONE");
        uil行2.prop_enum(self,  "ep限制类型", value="X", text_ctxt="", translate=True, icon="NONE");
        uil行2.prop_enum(self,  "ep限制类型", value="Y", text_ctxt="", translate=True, icon="NONE");
        uil行2.prop_enum(self,  "ep限制类型", value="Z", text_ctxt="", translate=True, icon="NONE");        
        uil行2.prop_enum(self,  "ep限制类型", value="AUTO",  text_ctxt="", translate=True, icon="NONE");  
        
        uil行=uil界.row(align=False);
        uil行.prop(data=self,property='bp是传播',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=False,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0);
        uil行.prop(data=self,property='bp是反选序',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=False,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0);
        uil行.prop(data=self,property='bp是渐变圆',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=False,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0);        
        uil行=uil界.row(align=False);        
        uil行.prop(data=self,property='fp圆心偏移',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=False,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0);  
    
    def invoke(self, context, event):
        self.fp圆心偏移=0.0;self.bp是反选序=False;
        self.bp是传播=False;self.ep限制类型="AUTO";
        return self.execute(context);
        
    def execute(self, context):    
        LIBG.dllMESH=dllΔ载入dllLIB(LIBG,"dllMESH",dllpathMESHB,dllpathMESH,None);#●●必须要这样才不出错       
        if(LIBG.dllMESH==None):
            self.report({"ERROR"},"没有  LIBG.dllMESH");#"INFO" "ERROR" "DEBUG" "WARNING"
            return {"FINISHED"};
        
        bpy.ops.object.editmode_toggle();
        print("LIBG.dllMESH",LIBG.dllMESH);
        oA=context.active_object;
        key=oA.data.shape_keys;
        if( key ):
            if(oA.active_shape_key.value!=1):
                oA.active_shape_key.value=1;

            if(oA.data.shape_keys and len(oA.data.shape_keys.key_blocks)>1):
                Csk=oA.data.shape_keys.key_blocks;
                sk基=oA.data.shape_keys.reference_key;Cskp基=sk基.data;
                if(oA.data.shape_keys .use_relative==False):
                    oA.data.shape_keys .use_relative=True;
                if(oA.show_only_shape_key==True):
                    oA.show_only_shape_key=False;

        
        cvpO=c_void_p(oA.as_pointer());f3圆心Π_=(c_float*3)();f44画_=((c_float*4)*4)();Lf3输出弧_=((c_float*3)*25)();
        LIBG.dllMESH.ΔΔ旋转3d向量多块(c_void_p(context.as_pointer()),cvpO,self.bp是传播,self.bp是反选序,self.bp是渐变圆,self.ep限制类型.encode('gb2312'),c_float(self.fp圆心偏移));#Lf3输出弧_
        #LIBG.Lv位实物画LIB.append([*f3圆心Π_]);print("HART",LIBG.Lv位实物画LIB);
        """
        Δ转画物位LIB(Lf3输出弧_);
        Δ转画矩阵LIB(f44画_);
        """
        #bpy.ops.op.draw_line_lib("INVOKE_DEFAULT");       
        if(LIBG.Li显示3dLIB[0]==-1):self.report({"WARNING"},"除移手柄==%d"%LIBG.Li显示3dLIB[0]);
        
        #LIBG.dllMESH=dllΔ卸载dllLIB(LIBG,"dllMESH");#●●必须要这样才不出错
        bpy.ops.object.editmode_toggle();
        return {'FINISHED'};        

#//////////////////////////////////////////
class 卐桥焊接卐Operator(bpy.types.Operator):
    bl_idname = "op.mesh_tools_bridge_weld";
    bl_label = "bridge_weld";
    bl_options = {"REGISTER", "UNDO"};
    
    bp是焊接=BoolProperty(name='weld',description='is welding or not',default=True,subtype='NONE',update=None,get=None,set=None);
    bp是按序焊接=BoolProperty(name='order',description='is welding in order',default=True,subtype='NONE',update=None,get=None,set=None);
    bp是反序=BoolProperty(name='reverse',description='reverse two of order',default=False,subtype='NONE',update=None,get=None,set=None);
    bp是反方向=BoolProperty(name='opposite',description='reverse the second one of order',default=False,subtype='NONE',update=None,get=None,set=None);    
    ip左中右=IntProperty(name='LMR',description='weld points in left or middle or right',default=1,min=0,max=2,step=1,subtype='NONE',update=None,get=None,set=None);

    
    @classmethod
    def poll(cls, context):
        oA=context.active_object;
        if(oA):
            return oA.mode=="EDIT";
        return False;
    def draw(self, context):
        uil界 = self.layout;
        uil行=uil界.row(align=False);
        uil行.prop(data=self,property='bp是焊接',text='weld',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=True,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0);
        uil行.prop(data=self,property='bp是按序焊接',text='order',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=True,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0);        
        uil行.prop(data=self,property='bp是反序',text='reverse',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=True,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0);        
        uil行.prop(data=self,property='bp是反方向',text='opposite',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=True,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0);        
        
        uil行=uil界.row(align=True);
        uil行.prop(data=self,property='ip左中右',text='LMR',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=False,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0);
        
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self,400,5);
        return {"FINISHED"};

    def execute(self, context):
        LIBG.dllMESH=dllΔ载入dllLIB(LIBG,"dllMESH",dllpathMESHB,dllpathMESH,None);
        oA=context.active_object;
        cvpO=c_void_p(oA.as_pointer());
        bpy.ops.object.editmode_toggle();
        #if(bpy.context.active_object.mode!="OBJECT"):bpy.ops.object.mode_set(mode="OBJECT");
        LIBG.dllMESH.Δ桥焊接(cvpO,self.bp是按序焊接,self.bp是反序,self.bp是反方向,self.ip左中右);
        
        bpy.ops.object.editmode_toggle();
        if(self.bp是焊接):
            bpy.ops.mesh.remove_doubles(threshold=0.001, use_unselected=False);
        #LIBG.dllMESH=dllΔ卸载dllLIB(LIBG,"dllMESH");
        return {"FINISHED"};
        
#//////////////////////////////////////////
class 卐卸载DLL卐Operator(bpy.types.Operator):
    bl_idname = "op.dll_mesh_tools";
    bl_label = "卸载dll";
    #bl_options = {"REGISTER", "UNDO"};

    @classmethod
    def poll(cls, context):
        return True; #(obj and obj.type == "MESH")
    def execute(self, context):
        if(LIBG.dllMESH):
            windll.kernel32.FreeLibrary.argtypes = [HMODULE];#定义参数的类型
            windll.kernel32.FreeLibrary(LIBG.dllMESH._handle);#释放dll
            LIBG.dllMESH=None;
            print("DEL~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~",);
        return {"FINISHED"};  
#////////////////////////////////////////////////
class 卐MESH_TOOLS卐Menu(bpy.types.Menu):
    bl_label = "mesh_tools"

    def draw(self, context):
        uil界 = self.layout;
        uil界.operator(卐圆化选点卐Operator.bl_idname, text="round",icon="SPHERECURVE");
        uil界.operator(卐桥焊接卐Operator.bl_idname, text="bridge weld",icon="FULLSCREEN_EXIT");
        uil界.operator(卐对齐选线卐Operator.bl_idname,text="align select",icon="COLLAPSEMENU");
        uil界.operator(卐矩形化选点卐Operator.bl_idname,text="Rectangular",icon="BORDER_RECT");
        uil界.operator(卐轴到所选卐Operator.bl_idname,text="axis to select", icon="MANIPUL");
        uil界.operator(卐转MESH到CURVE卐Operator.bl_idname,text="M2C", icon="OUTLINER_OB_CURVE");
        uil界.separator();
        uil界.operator(卐选择相似_相似uvCURVE卐Operator.bl_idname,text="选择相似_相似uv",icon="RESTRICT_SELECT_OFF");
        uil界.separator();
        uil界.operator(卐MESH点ξ生成组卐Operator.bl_idname,text="点ξ生成组",icon="GROUP_VERTEX");
        #uil界.operator(卐卸载DLL卐Operator.bl_idname, text="",icon="CANCEL");

def Δmenu_mesh_tools(self, context):
    self.layout.menu("卐MESH_TOOLS卐Menu",translate=True,icon="EDITMODE_HLT")




def register():
    bpy.utils.register_module(__name__);
    bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(Δmenu_mesh_tools);

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(Δmenu_mesh_tools);
    bpy.ops.op.dll_mesh_tools("INVOKE_DEFAULT");
    Δ删除模块LIB(Ls模块名=[文件夹此mesh_tools]+Ls模块LIB);
    bpy.utils.unregister_module(__name__);
    print("unregister~~~",);

if __name__ == "__main__":
    register()
    
    
    
    
    
    
    
    