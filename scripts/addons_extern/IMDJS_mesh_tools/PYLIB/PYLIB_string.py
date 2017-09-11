
import bpy,sys,os,shutil
from bpy.props import *
from string import*
from ast import literal_eval;

from ctypes import*
import platform
if(platform.system()=="Windows"):  
    from ctypes.wintypes import *

#pathPYLIB=os.path.dirname(__file__);#E"\blender\addons\OBJECT_HairMesher 
#namePYLIB= os.path.basename(pathPYLIB);#OBJECT_HairMesher

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
    
from .PYLIB_attribute import dllΔ载入dllLIB,dllΔ卸载dllLIB;

CLIB = os.path.abspath("B:/CLIB64.dll");
CLIB64 = os.path.abspath("E:/blender/BlenderLib/CLIB64.dll" );

#////////////////////////////////////////////////
def PTfnn(fnn):
    print("len==",len(fnn));
    for L in fnn:
        for i in L:
            print("fnn==",i);
    
def Δ打开文件夹LIB(s文件夹path):
    if(LIBG.dllCLIB==None):
        LIBG.dllCLIB=dllΔ载入dllLIB(LIBG,"dllCLIB",CLIB,CLIB64,None);
    print("s文件夹path==",s文件夹path);#√

    s文件夹path=s文件夹path.encode('gb2312');#√ 
    
    LIBG.dllCLIB.OPEN_FLODER(s文件夹path);
    LIBG.dllCLIB=dllΔ卸载dllLIB(LIBG,"dllCLIB");
    
def sΔ从硬盘读取LIB(f3路径文件):
    file=os.path.join(*f3路径文件);
    with open(file, 'r') as 文件:
        s文件 = literal_eval(文件.read());
        文件.close();
    print("L LAYOUT IN==",s文件);
    return s文件;
#————只导入文件名————————————————————————————————————————————
def Δ从硬盘导入LIB(file种类文件,s类型,cp当前种类,ip激活类型ξ,b多个标签):
    wm = bpy.context.window_manager;
    #if(wm.ep多重预置目录类型wm==模式):
    s种类预置名=None;
    s类型预置文件=os.path.basename(file种类文件)#文件名.后缀
    s种类预置名=os.path.splitext(s类型预置文件)[0];#文件名
    #Δ读取文件并写入wmLIB(wm,file种类文件,s类型,cp当前种类,b多个标签);#暂时不写入wm 因这会耗时
    #----如果找到文件 就增加条项-----------------------------------------------------------
    if(b多个标签 and s种类预置名):
        pg=cp当前种类.add();#包括所有材质种类
        pg.name=s种类预置名 ;pg.sp原名=s种类预置名 ;pg.bp脏=False;
        if(s种类预置名[:2]=="M."):
            pg.sp物类型="MESH";
        elif(s种类预置名[:2]=="E."):
            pg.sp物类型="EMPTY";
        elif(s种类预置名[:2]=="L."):
            pg.sp物类型="LAMP";
        elif(s种类预置名[:2]=="A."):
            pg.sp物类型="ARMATURE";
        elif(s种类预置名[:2]=="l."):
            pg.sp物类型="LATTICE";
        elif(s种类预置名[:2]=="m."):
            pg.sp物类型="META";
        elif(s种类预置名[:2]=="F."):
            pg.sp物类型="FONT";
        elif(s种类预置名[:2]=="C."):
            pg.sp物类型="CAMERA";
        elif(s种类预置名[:2]=="S."):
            pg.sp物类型="SPEAKER";
#--------------------------------------------------------------------------
def Δ读取文件并写入wmLIB(wm,file种类文件,s类型,cp当前种类,b多个标签):
    try:
        with open(file种类文件, 'r') as 文件: #读文本文件#例如:E:\blender\addons\object_presets\OBECTS\INDUSTRY\0\闪电.txt
            if(b多个标签):
                s类型预置文件=os.path.basename(file种类文件)#文件名.后缀
                s种类预置名=os.path.splitext(s类型预置文件)[0];#文件名
                #print("import sMAT==",s种类预置名);
                wm['MULTISETTING_WM'][s类型][s种类预置名]= literal_eval(文件.read());
            else:
                wm['MULTISETTING_WM'][s类型] = literal_eval(文件.read());
                #print("写入类型==",s类型);
                #text必须是字典

    except :
        #shutil.copy(file种类文件,  file种类文件+".open error last time");
        print("error import",);
        #os.remove( file种类文件);
        return ;

#==============================================================
def Δ字典写入硬盘LIB(Ds字典,file保存):#file保存=="B:\\错误.txt"
    if(str(type(Ds字典))!="<class 'dict'>"):
        Ds字典=Ds字典.to_dict();
    s字典 = str(Ds字典);
    #----写入字典----------------------------------------------------------
    file = open(file保存, "w");#, encoding="utf8", newline="\n"
    #print("FILE SAVE==",file保存);
    
    Δfw写入器 = file.write;
    Δfw写入器('#Blender v%s %r Copyright by imdjs\n' % (bpy.app.version_string, os.path.basename(bpy.data.filepath)));#第一行
    Δfw写入器(s字典+"\n");#第二行
    
    file.close();

#——————————————————————————————————————————————————————
def DΔ读取一个文件为字典LIB(pg类型,path当前种类,s后辍):
    s父目录=path当前种类;
    sFolder =pg类型.sp原名;
    s类型预置文件=sFolder+s后辍;#文件名.后缀
    file种类文件=os.path.join(s父目录,s类型预置文件);#例如:E:\blender\addons\object_presets\OBECTS\INDUSTRY\0\闪电.txt

    #----打开文件---------------------------------------------------------------
    文件=open(file种类文件, 'r');#'r'  'rb'
    Ls行=文件.readlines();
    #----读取通常属性------------------------------------------------------------
    D字典={};
    for s行 in Ls行:# .readlines():
        if(s行.startswith('{')):#这个可以检测多个字符
            D字典=eval(s行);#只读取 {  开头的行#print("read D通常属性==",D通常属性);
            break;
    文件.close();
    return D字典;


#==============================================================
def iΔ删除重复文件LIB(self, context,pathLIB,sp重复字符):
    i=0;
    for s父目录,Ls所有文件夹名,Ls所有文件名 in os.walk(pathLIB,onerror=None ):
        for sFolder in Ls所有文件名:
            Ls文件名后辍=os.path.splitext(sFolder);#("hello", ".py")
            if(Ls文件名后辍[0].endswith("(1)") ):
                file文件名=os.path.join(s父目录,sFolder);
                os.remove( file文件名);
                i+=1;
    return i;

    
def Δ从硬盘删除LIB(path当前种类,sp激活预置名,b是删除全部,b是文件夹):
    for s父目录,Ls所有文件夹名,Ls所有文件名 in os.walk(path当前种类,onerror=None):#删除 多余的材质
        if(b是文件夹):
            for s文件夹 in Ls所有文件夹名:
                if(not b是删除全部):
                    if(s文件夹==sp激活预置名):#如果硬盘材质名==激活名
                        pathLIB=os.path.join(s父目录,s文件夹);
                        if(os.path.isdir(pathLIB)):
                            shutil.rmtree(pathLIB);
                            break ;

                
        else:
            for sFolder in Ls所有文件名:
                s种类预置名=os.path.splitext(sFolder)[0];#文件名 ,过滤后辍
                if(not b是删除全部):
                    if(s种类预置名==sp激活预置名):#如果硬盘材质名==激活名
                        os.remove( os.path.join(s父目录,sFolder));
                        break ;
                else:
                    os.remove( os.path.join(s父目录,sFolder));
                    
            break ;
        
def Δ从硬盘删除一个LIB(s父目录,file):
    file= os.path.join(s父目录,file);
    if(os.path.isfile(file)):
        os.remove(file);#B:\\文件名\\bb.txt
    
    
#==============================================================
def Ls_sΔ读取文本LIB(file文件,b读行):
    #os.chdir('B:\\')       #改变当前工作路径
    if (not os.path.exists(file文件)): # 看一下这个文件是否存在
        return ;
        #exit(-1) ; #，不存在就退出程序
    #print("FILE READ",file文件);
    Ls行=[];S="";
    with open(file文件, 'r' , encoding = "utf_8") as file:#打开你要写的文件a+(不在会添加)与 r+ (必须存在)会增加写入 w与w+会清空原来的
        if(b读行):
            Ls行 =file.readlines() #这个如果读了 下面的read就读不出●●#打开文件，读入每一行#, encoding = "utf_8"
            #print("Ls==",Ls行);#Ls== ['love\n', '\n', '\n', '瀹冧滑\n', '鎴戜滑  瀹冧滑  him  鎴戜滑\n',...]
        else:
            S=file.read();#print("S==",S.encode('raw_unicode_escape').decode('utf-8'));
        #print("S==",S);

    return Ls行,S;




#==============================================================
def  Δ转unicodeLIB(fileRead,file写):
    Ls行,S=Ls_sΔ读取文本LIB(fileRead,False);
    #print("S2==",S);
    #--------------------------------------------------------------------------
    path写=os.path.split(file写)[0];##插件目录/unicode
    if (not os.path.exists(path写)): # 看一下这个文件是否存在
        #print("NOT EXISTS",fileWrite);
        os.makedirs(path写);#创建多级目录
        #return ;
        #exit(-1) ;#退出程序
    with open(file写,'w+', encoding = "utf_8") as file:#encoding = "utf-8" 可以读取中文字符的 utf-8格式py# utf_8_sig为带BOM
        S=S.encode('raw_unicode_escape').decode('utf_8');
        S=S.replace("\\u","UU").replace("UUfeff","");
        file.write(S);

#==============================================================
def  ΔΔ中文转enLIB(fileRead,file写):
    Ls行,S=Ls_sΔ读取文本LIB(fileRead,True);
    #print("S2==",S);
    #--------------------------------------------------------------------------
    path写=os.path.split(file写)[0];##插件目录/unicode
    if (not os.path.exists(path写)): # 看一下这个文件是否存在
        #print("NOT EXISTS",fileWrite);
        os.makedirs(path写);#创建多级目录
        #return ;
        #exit(-1) ;#退出程序
    with open(file写,'w+', encoding = "utf_8") as file:#encoding = "utf-8" 可以读取中文字符的 utf-8格式py# utf_8_sig为带BOM
        Ls写入行="";
        for s行 in Ls行:
            #print("s==",s行);

            for cn,en in Dcn翻译en.items():
                s行=s行.replace(cn,en);# replace是替换只有当有这个词才成功，write是写入
            #file.write(s行) ;
            Ls写入行+=s行;
        file.write(Ls写入行)   # replace是替换只有当有这个词才成功，write是写入
       
        

#==============================================================
def  Δ替换字符LIB(file文件,D替换字符对):#D替换字符对={'love':'hate','yes':'no','它们':'they'};

    Ls行,S=Ls_sΔ读取文本LIB(file文件=file文件,b读行=True);
    #--------------------------------------------------------------------------
    with open(file文件,'w', encoding = "utf_8_sig") as file:#encoding = "utf-8" 可以读取中文字符的 utf-8格式py# utf_8_sig为带BOM
        Ls写入行="";
        for s行 in Ls行:
            print("s==",s行);
            for s in s行.split():#["我们","它们","him","我们"]
                if(s in D替换字符对):
                    print("FIND",s行,s行.split);
                    s行=s行.replace(s,D替换字符对[s]);# replace是替换只有当有这个词才成功，write是写入
            Ls写入行+=s行;
        file.write(Ls写入行)   # replace是替换只有当有这个词才成功，write是写入

#==============================================================
def dir_sΔ得当前选物目录与文件名LIB(oA,sData名):
    fileBlend=bpy.data.filepath;#B:\\文件名123.blend
    dir目录=os.path.dirname(fileBlend);#B:\\
    if(sData名=="" or sData名!=oA.data.name):
        sData名=oA.data.name;
        """
        for s in sID:
            #if (not s.isdigit() ):
            if(s!="."):
                sData名+=s;
            else:
                break;
        """
    return dir目录,sData名;

#==============================================================
def  sΔ提取当前文件夹目录LIB():
    sID=bpy.context.active_object.data.name;
    fileBlend=bpy.data.filepath;#B:\\文件名123.blend
    dir目录=os.path.dirname(fileBlend);#B:\\
    #pathBlend=os.path.splitext(fileBlend)[0];#B:\\文件名123
    fBlend=os.path.basename(fileBlend);#文件名123.blend
    sBlend=os.path.splitext(fBlend)[0];#文件名123
    s文件夹名="";
    for s in sBlend:
        #if (not s.isdigit() ):
        if(s!="."):
            s文件夹名+=s;
        else:
            break;
    path文件目录_=os.path.join(dir目录,s文件夹名,sID);#B:\\文件名\\
    return path文件目录_;#找到这个lib文件夹

#==============================================================
def sΔ名字增量LIB(s名,Ls名):#把相同的s名_  编上序号
    i = 0
    while (s名 in Ls名):
        i += 1
        if (s名[-3:].isdigit() and s名[-4] == "."): #sk.isdigit() 所有字符都是数字 并且  之后是.
            s名 = "{}{:03d}".format(s名[:len(s名)-3], i)#03d  表示小数点后保留三位整数 打印name.00i
        else:
            s名 += ".001"
    return s名;
    
#////////////////////////////////////////////////
import webbrowser
class 卐关于我卐Operator(bpy.types.Operator):
    bl_idname = 'op.about_me'
    bl_label = ''
    bl_description = 'about me'
    bp查看更新=BoolProperty(name="check updated version",description = 'check updated version',default=False)
    Ls介绍=[
                      "this addon is for editing  mesh uvs  first you mush select one uv line or a circle,",
                      "and than press the button with different function to relax or arange the uv,",
                      "1:circle button is for making the seleted line become a circle shape ,",                      
                      "2:smooth button is for smoothing the uv line  like you do with smooth brush ",
                      "but preserving  the shape of uv line .and the  smooth*3 will smooth the uv but",
                      "not preserving  the shape of uv line .",
                      "3:straighten and align button does as the build-in function but will rearrange the uv points .",
                      "copy and paste button just will copy selected uvs and paste to another uv layer .",
                      "---------------------------------------------------------",

                      "---------------------------------------------------imdjs",                      
                      ];
    
    url链接="http://blog.sina.com.cn/s/blog_4f03100c01010wqb.html";
    
    #--------------------------------------------------------------------------
    @classmethod 
    def poll(self,context):
        return True ;
    
    def draw(self, context):
        """"""
        for s in self.Ls介绍:
            self.layout.label(text=s, text_ctxt="", translate=True, icon='NONE', icon_value=0);
        self.layout.prop(self, "bp查看更新");   
        
    def invoke(self, context, event):#运行的第壹步
        return context.window_manager.invoke_props_dialog(self,600,50);

    def execute(self, context):
        if(self.bp查看更新):
            webbrowser.open(self.url链接, new=0, autoraise=True);
        return {'FINISHED'};  
        
bpy.utils.register_class(卐关于我卐Operator);

#////////////////////////////////////////////////
class 卐弹出询问窗口卐Operator(bpy.types.Operator):
    bl_idname = "op.ask_for_sure";
    bl_label = "弹出询问窗口";
    bl_options = {"REGISTER", "UNDO"};
    sp=StringProperty(name="注意", description="", default="你确定？");
    pathLIB=StringProperty(name="文件路径", description="E:/blender/addons/", default="E:/blender/addons/");
    #==============================================================
    @classmethod
    def poll(cls, context):
        return True; #(obj and obj.type == "MESH")

    #==============================================================
    def draw(self, context):    
        self.layout.prop(self, "sp");
        
    def invoke(self, context, event):   return context.window_manager.invoke_props_dialog(self,400,50);#召唤


#////////////////////////////////////////////////
class 卐改名卐OperatorLIB(bpy.types.Operator):
    bl_idname = "op.rename_module_lib";
    bl_label = "改名模块";
    
    pathLIB=StringProperty(name="文件路径", description="E:/blender/addons/", default="E:/blender/addons/");
    
    def draw(self, context):    
        self.layout.prop(self, "pathLIB");
    def invoke(self, context, event):   return context.window_manager.invoke_props_dialog(self,400,50);#召唤
    #==============================================================
    def execute(self, context):
        #_卐改名模块=卐改名模块卐Operator(bpy.types.Operator);
        self.pathLIB+="/__pycache__";
        #==============================================================
        for s父目录,Ls所有文件夹名,Ls所有文件名 in os.walk(self.pathLIB,onerror=None ):
            for sFolder in Ls所有文件名:
                if(sFolder[-15:]==".cpython-35.pyc"):
                    file原名=os.path.join(s父目录,sFolder);
                    sFolder=sFolder[:-15]+".pyc";
                    file改名=os.path.join(s父目录,sFolder);
                    try:
                        os.rename(file原名,file改名);
                    except:
                        print("EORROR path save&origine==",file改名,file原名);

        return {"FINISHED"};

bpy.utils.register_class(卐改名卐OperatorLIB);

#////////////////////////////////////////////////
class 卐unicode化lib卐Operator(bpy.types.Operator):
    bl_idname = "op.unicode_py_lib";
    bl_label = "unicode化";
    pathLIB=StringProperty(name="文件路径", description="E:/blender/addons/", default="E:/blender/addons/");

    
    def draw(self, context):    
        self.layout.prop(self, "pathLIB");
    def invoke(self, context, event):   return context.window_manager.invoke_props_dialog(self,400,50);#召唤
    #==============================================================
    def execute(self, context):

        #pathLIB = os.path.dirname(__file__) ;
        ΔΔunicode化(self, context,self.pathLIB);
        self.report({"ERROR"},"unicode");#"INFO" "ERROR" "DEBUG" "WARNING"
        return {"FINISHED"};


def ΔΔunicode化(self, context,pathLIB):
    Ls本目录所有文件名=os.listdir(pathLIB);
    #print("Ls==",Ls本目录所有文件名);return ;
    for sFolder in Ls本目录所有文件名:
        #print("===",sFolder);
        if(sFolder[-3:]==".py"):
            fileRead=os.path.join(pathLIB,sFolder);
            fileWrite=os.path.join(pathLIB+"/unicode/",sFolder);
            #print("READ==",fileRead,fileWrite);
            #Δ转unicodeLIB(fileRead,fileWrite);
            ΔΔ中文转enLIB(fileRead,fileWrite);
            
            
            
bpy.utils.register_class(卐unicode化lib卐Operator);

Dcn翻译en={
"ΔΔ":"FUNC",
"Δ":"FUN",
"不":"Not",
"两点":"TwoPoints",
"关于":"about",
"删除":"Dele",
"卸载":"unload",
"叉积":"Cross",
"反":"inverse",
"后":"Back",
"头":"head",
"子":"Child",
"级":"Level",
"宽":"With",
"密度":"dense",
"寻找":"Find",
"尾":"Tail",
"已":"Have",
"平行":"Parallel",
"序":"Order",
"开始":"Start",
"数":"Num",
"文件夹":"Floder",
"是":"Isi",
"最短":"Shortest",
"权":"weight",
"根":"Root",
"模块":"Module",
"此":"This",
"毛发宽":"width",
"毛点":"HairNum",
"点":"Point",
"生成":"Generate",
"目录":"Cata",
"乛":"Vector",
"类型":"Type",
"ξ":"Ind",
"线":"Line",
"组":"Group",
"距离":"Distance",
"载入":"load",
"长":"Long",
"骼":"s",

"面":"face",
"节":"Knob",
"采样":"Sam",
"自动":"Auto",
"因子":"Fac",
"指数":"Ind",
"栋":"Col",
"变":"Change",
"了":"Le",
"增加":"Increse",
"随机":"Random",
"毛":"Hair",
"到":"To",
"绑定":"Rig",
"骨":"Bone",
"最":"Most",
"长":"Long",
"位":"Loc",
"界":"Jie",
"行":"Row",
"平均":"Everage",
"中":"Mid",
"清除":"Clear",
"间":"M",
"环":"Loop",
"小":"Small",
"大":"Big",
"物":"Object",
"有":"Have",
"阈":"Threshold",
"值":"Value",
"短":"Short",
"累":"Plus",
"架":"Arm",
"偏移":"Off",
"扭曲":"Twist",
"应":"Should",
"左":"Left",
"右":"Right",
"减":"Sub",
"增":"Add",
"寻找":"Find",
"法":"Nor",
"平滑":"Smooth",
"夹角":"Angle",
"横":"Hori",
"边":"Edge",
"脊梁":"Arc",
"向":"V",
"第":"No_",
"当前":"Current",
"颜色":"Color",
"延":"Extend",
"新":"New",
"脏":"Dirty",
"旧":"Old",
"网格":"Mesh",
"全部":"All",
"每":"Per",
"修改器":"Mod",
"画":"Draw",
"实时":"RealTime",
"总":"Total",
"毛":"Hair",
"发":"H",
"其它":"Other",
"三角":"Tri",
"本":"This",
"此":"This",
"读":"Read",
"写":"Write",
"文件":"file",
"名":"Name",
"夹":"Jie",
"查看":"Check",
"更新":"Update",
"链接":"Link",
"弹出":"Pop",
"询问":"Ask",
"窗口":"Window",
"改":"Change",
"模块":"Module",
"路径":"Path",
"召唤":"Call",
"全":"All",
"卐":"Class",
"一":"One",
"条":"Strip",
"弓":"Arc",
"加":"Plus",
"顶":"Top",
"计":"Cal",
"算":"Culate",
"网":"Net",
"精":"Sim",
"简":"Sim",
"距":"Off",
"旋":"Rot",
"Г":"Cross",
"Ξ":"Div",
"垂":"Vertical",
"直":"Straight",
"上":"Up",
"下":"Down",
"零":"Zero",
"个":"One",
"因":"Due",
"二":"Two",
"三":"Three",
"显":"Show",
"示":"Vis",
"化":"Ize",
"我":"Me",
"更":"Change",
"介":"Intro",
"绍":"Duce",
"假":"Fake",
"虚":"Virtual",
"矩":"Mat",
"步":"Step",
"混":"Mix",
"合":"Mix",
"":"Ask",
"形":"Shape",
"尺":"Size",
"寸":"Size",
"分":"Div",
"配":"Alloc",
"子":"Son",
"孙":"son",
"父":"Farther",
"量":"Vol",
"轴":"Axis",
"转":"Rot",
"真":"True",
"竖":"Vert",
"倍":"Times",
"制":"py",
"复":"Co",
"心":"Hart",
"积":"Product",
"夹":"Clip",
"角":"Angle",
"壹":"One",
"原":"Ori",
"实":"True",
"这":"This",
"比":"Ratio",
"例":"Ex",
"找":"Find",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
"":"",
















}
























#////end////end////end////end////end////end////end////end////


























