
import os

try:
    from PYLIB.PYLIB_main import *
except:    

    from .PYLIB.PYLIB_main import*

#----------------------------------------------------------------------------
class 卐转MESH到CURVE卐Operator(bpy.types.Operator):
    """Enable/disable fake user for ep_ssss"""
    bl_idname = "turn.mesh_curve"
    bl_label = "转MESH到CURVE "
    bl_options = {"REGISTER", "UNDO"}
    ip分辨率=IntProperty(name="分辨率",description="曲线分辨率",default= 3,min=0, max=12,);
    bp结尾=BoolProperty(name="结尾",description="结尾",default= True ,);
    @classmethod
    def poll(cls, context):#决定是否激活
        return (context.active_object.type in ["MESH","CURVE"]);

    def draw(self, context):
        if(context.active_object.type=="MESH"):
            row = self.layout.row();
            row.prop(self, "ip分辨率");
            row.prop(self, "bp结尾");

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        oA=context.active_object;
        if(oA.type=="MESH"):
            bpy.ops.object.convert(target="CURVE", keep_original=False);
            c2=context.active_object.data;
            #print(oA.name);
            c2.resolution_u=self.ip分辨率;
            Lsp=c2.splines;
            print(Lsp)
            for sp in Lsp:
                #sp.type="BEZIER"
                sp.type="NURBS"
                sp.resolution_u=self.ip分辨率;
                sp.use_endpoint_u=self.bp结尾;
                #for bz in sp.bezier_points:
                    #bz.handle_left_type="AUTO";
        elif(oA.type=="CURVE"):
            bpy.ops.object.convert(target="MESH", keep_original=False);
        return {"FINISHED"}
#-------------------------------------------------------------------------------
def ΔUPDATE选择(self, context):
    if(self.bp不变 and self.bp法线):
        self.bp法线=False;
    #elif(self.bp法线):
        #self.bp不变=False;


 #//////////////////////////////////////////////////
class 卐对齐选线卐Operator(bpy.types.Operator):
    bl_idname = "bp.align_to_selected_line"
    bl_label = "对齐选线"
    bl_options = {"REGISTER", "UNDO"}

    bp选点自动对齐=BoolProperty(name="选点自动对齐",description="选点自动对齐",default=False)
    bp拉直=BoolProperty(name="拉直",description="拉直",default=False)
    bp自动对齐=BoolProperty(name="自动对齐",description="自动对齐",default=False)
    bp对齐到最后选点=BoolProperty(name="对齐到最后选点",description="对齐到最后选点",default=True)
    bpX=BoolProperty(name="对齐X",description="对齐X",default=False)
    bpY=BoolProperty(name="对齐Y",description="对齐Y",default=False)
    bpZ=BoolProperty(name="对齐Z",description="对齐Z",default=False)
    bm=None;
    
    @classmethod
    def poll(cls, context):#决定是否激活
        oS=context.object
        if (oS!=None and (oS.type=="MESH" or oS.type=="CURVE")and (context.mode=="EDIT_MESH" or context.mode=="EDIT_CURVE" ) ):
            return True;
        return False;

    def draw(self, context):#第貮步
        layout = self.layout;
        #layout.prop(self, "bp不变");
        layout.prop(self, "bp选点自动对齐");
        uil行=layout.row(align=True);
        uil行.prop(self, "bp拉直");
        uil行.prop(self, "bp自动对齐");
        layout.prop(self, "bp对齐到最后选点");
        uil行=layout.row(align=True);
        #if(not self.bp自动对齐):
        uil行.prop(self, "bpX");uil行.prop(self, "bpY");uil行.prop(self, "bpZ");

    def invoke(self, context, event):#召唤 第壹步
        return context.window_manager.invoke_props_dialog(self);

    #                     ┃
    #                     ┃
    #       ○━━●━━○━━>
    #                     ┃
    #                     ┃

    def execute(self, context): #第三步
        oA=bpy.context.active_object;id=oA.data;
        if(self.bm==None):
            self.bm = bmesh.from_edit_mesh(id);
        if(self.bm.select_history):
            bmve最后选=self.bm.select_history.active;
        else:
            bmve最后选=None;
        Lbme选 = [] ;
        #--------------------------------------------------------------------------
        print("bmesh",len(self.bm.edges));
        for bme in self.bm.edges: #This meshes bme sequence (read-only).Type : BMEdgeSeq
            if (bme.select):
                Lbme选.append(bme);

        bme随机边=Lbme选[0];bmv左=bme随机边.verts[0];bmv右=bme随机边.other_vert(bmv左);
        print("LR==",bmv左,bmv右);
        L序v选点位=[];L序v选点位.append(bmv左.co);L序v选点位.append(bmv右.co);#[[bmv,v左],[bmv,v右]]
        #L序bmv选点=[];
        #L序点ξ=[];L序点ξ.append(bmv左.index);L序点ξ.append(bmv右.index);

        i边数2=i边数=len(Lbme选)+1;
        """
        for bme连选 in bmv左.link_edges:
            if(bme连选.select and bme连选 !=bme随机边 ):
                print("L==",bme连选);

        for bme连选 in bmv右.link_edges:
            if(bme连选.select and bme连选 !=bme随机边 ):
                print("R==",bme连选);
        """
        #----往左添加co---------------------------------------------------------------
        bme随机边右=bme随机边;#随机边会变化 所以要分左右
        bme随机边左=bme随机边;
        
        while(i边数>0):
            for bme连选 in bmv左.link_edges: #Edges connected to this vertex (read-only).
                                                                        #Type : BMElemSeq of BMVert
                if (bme连选.select and bme连选 !=bme随机边左): # 另一条选边
                    bmv下一点 = bme连选.other_vert(bmv左);print("L==",bmv左.index);
                    #bmv随机点的下一个点 <----o----o==o
                    #                                          bmv下一点   bmv左
                    L序v选点位.insert(0,bmv下一点.co);#L序点ξ.insert(0,bmv下一点.index);
                    #L序bmv选点.insert(0,bmv下一点);
                    bmv左=bmv下一点;bme随机边左=bme连选;
                    break;
            i边数-=1;
        #----往右添加co---------------------------------------------------------------;
        while(i边数2>0):
            for bme连选 in bmv右.link_edges: #Edges connected to this vertex (read-only).
                                                                        #Type : BMElemSeq of BMVert
                if (bme连选.select and bme连选 !=bme随机边右): # 另一条选边
                    bmv下一点 = bme连选.other_vert(bmv右); print("R==",bmv右.index);
                    #bmv随机点的下一个点  o==o----o---->
                    #                                                bmv右  bmv下一点
                    L序v选点位.append(bmv下一点.co);#L序点ξ.append(bmv下一点.index);
                    #L序bmv选点.append(bmv下一点);
                    bmv右=bmv下一点;bme随机边右=bme连选;
                    break;
            i边数2-=1;
        #----求最近选的v位---------------------------------------------------------------
        
        
        if(self.bp对齐到最后选点 and bmve最后选!=None):
            if(hasattr(bmve最后选,"verts")):#线中点
                v最后选=(bmve最后选.verts[0].co+bmve最后选.verts[1].co)/2;
            else:
                v最后选=bmve最后选.co;
        else:
            v总和=Vector();
            for v选点位_  in L序v选点位:
                v总和+=v选点位_;

            v最后选=v总和/len(L序v选点位);

        #--------------------------------------------------------------------------
        v头乛尾=L序v选点位[-1]-L序v选点位[0];
        f头尾长=v头乛尾.length;


        if(not self.bp选点自动对齐):
            #----拉直------------------------------------------------------------------
            if(self.bp拉直):
                v乛头=L序v选点位[0];v乛尾=L序v选点位[-1];
                i点数=len(L序v选点位);i=0 ;
                for  v选点位_ in (L序v选点位):
                    if(i==0 or i==(i点数-1)):print("I==",i);i+=1;continue;#头尾不选
                    v乛头__此=v选点位_-v乛头;
                    f夹角=v乛头__此.angle(v头乛尾);print("ANGLE==",degrees(f夹角));
                    f邻边长=v乛头__此.length*cos(f夹角);print("LEN==",f邻边长);
                    v此点位=v头乛尾*(f邻边长/f头尾长)+v乛头;
                    #print("V==",v此点位,v选点位_);
                    v选点位_.x=v此点位.x;v选点位_.y=v此点位.y;v选点位_.z=v此点位.z;#必须这样赋值才成功
                    i+=1;
            #----对齐-----------------------------------------------------------------
            else:
                if(self.bp自动对齐):
                    x=abs(v头乛尾.x); y=abs(v头乛尾.y); z=abs(v头乛尾.z);
                    if(x>y and x>z):
                        for v选点位_  in L序v选点位:
                            v选点位_.y=v最后选.y;v选点位_.z=v最后选.z;

                    elif(y>x and y>z):
                        for v选点位_  in L序v选点位:
                            v选点位_.x=v最后选.x;v选点位_.z=v最后选.z;

                    elif(z>x and z>y):
                        for v选点位_  in L序v选点位:
                            v选点位_.y=v最后选.y;v选点位_.x=v最后选.x;

                else:
                    for v选点位_  in L序v选点位:
                        if(self.bpX):
                            v选点位_.x=v最后选.x;
                        if(self.bpY):
                            v选点位_.y=v最后选.y;
                        if(self.bpZ):
                            v选点位_.z=v最后选.z;

            #----选点自动对齐---------------------------------------------------------------
            #☐☐━━━━━━━━━━━━━━☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
            #☐☐┃☐☐☐●☐☐☐☐☐☐☐☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
            #☐☐┃☐☐┆☐\☐☐☐☐☐☐☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
            #☐☐┃☐☐│☐☐\☐☐☐☐☐●┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
            #☐☐┃☐┆☐☐☐☐\☐☐┄─☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
            #☐☐┃☐│☐☐☐☐☐●─☐☐☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
            #☐☐┃●☐☐☐☐☐☐☐☐☐☐☐┃☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
            #☐☐━━━━━━━━━━━━━━☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐

        else:
            Lbmv选=[bmv  for bmv in self.bm.verts  if (bmv.select)];
            v总和=Vector();
            v头乛尾=Lbmv选[-1].co-Lbmv选[0].co;
            if(not self.bp对齐到最后选点):
                for bmv  in Lbmv选:
                    v总和+=bmv.co;
                v最后选=v总和/len(Lbmv选);

            if(self.bp自动对齐):
                #----计算边界--------------------------------------------------------------
                x小=y小=z小=100000; x大=y大=z大=-100000;
                for bmv  in Lbmv选:
                    v点位=bmv.co;
                    if(v点位.x<x小):x小=v点位.x;
                    if(v点位.x>x大):x大=v点位.x;
                    if(v点位.y<y小):y小=v点位.y;
                    if(v点位.y>y大):y大=v点位.y;
                    if(v点位.z<x小):z小=v点位.z;
                    if(v点位.z>z大):z大=v点位.z;

                x=abs(x大-x小); y=abs(y大-y小); z=abs(z大-z小);
                print("xyz==",x,y,z);
                if(x<y and x<z):#X轴最短
                    for bmv  in Lbmv选:
                        bmv.co.x=v最后选.x;

                elif(y<x and y<z):#Y轴最短
                    for bmv  in Lbmv选:
                        bmv.co.y=v最后选.y;

                elif(z<x and z<y):#Z轴最短
                    for bmv  in Lbmv选:
                        bmv.co.z=v最后选.z;

            else:
                for bmv  in Lbmv选:
                    if(self.bpX):
                        bmv.co.x=v最后选.x;
                    if(self.bpY):
                        bmv.co.y=v最后选.y;
                    if(self.bpZ):
                        bmv.co.z=v最后选.z;



        #--------------------------------------------------------------------------
        id.update(calc_edges=False, calc_tessface=False);
        #self.bm.free();#●●这个如果提前删除,如果继续编辑点会出错
        # ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐
        # ☐━━━━━━━━━━━━ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        # ☐┃ ☐☐    ○━→● ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐
        # ☐┃ ☐☐/┇┄ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        # ☐┃ ☐/┄─ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐
        # ☐┃/─ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐
        # ☐●━━━━━━━━━━━ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        # ☐头 ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        #bpy.ops.object.editmode_toggle();
        #bpy.ops.object.editmode_toggle();
        #for v in L序bmv选点:print("bmv==",L序bmv选点,len(L序bmv选点));
        return {"FINISHED"};

#////////////////////////////////////////////
class 卐选择相似_相似uvCURVE卐Operator(bpy.types.Operator):
    bl_idname = "op.select_similar_uv"
    bl_label = "选择相似_相似uv "
    bl_options = {"REGISTER", "UNDO"}

    fp选择阈值=FloatProperty(name='',description='',default=0.001,min=0.0,max=1.0,soft_min=0.0,soft_max=1.0,step=3,precision=2,subtype='NONE',unit='NONE',update=None,get=None,set=None);

    #--------------------------------------------------------------------------
    @classmethod
    def poll(cls, context):#决定是否激活
        return (context.active_object.type in ["MESH"]);

    def draw(self, context):
        if(context.active_object.type=="MESH"):
            row = self.layout.row();
            row.prop(self, "fp选择阈值");

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        oA=context.active_object;
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type="VERT", action="ENABLE");
        id=oA.data;Lmv=id.vertices;Lme=id.vertices;
        if (not  id.uv_layers.active):
            self.report({"ERROR"},"没有uv!!");#"INFO" "ERROR" "DEBUG"
            return {"FINISHED"};

        #----找到选择的uv------------------------------------------------------------

        if(bpy.context.object.mode!="OBJECT"):
            bpy.ops.object.mode_set(mode="OBJECT");
        Cmuvl = id.uv_layers.active.data ;Lmuvl顶点选=[];# 这个只能在物体模式下才能记录数据
        print("Cmuvl",Cmuvl);
        for ξ面,mp全部 in enumerate(id.polygons):
            i面点数=len(mp全部.loop_indices);
            for i步3 in range(i面点数):
                ξ点 = mp全部.vertices[i步3];
                i环=mp全部.loop_indices[i步3];
                if(id.vertices[ξ点].select):
                    Lmuvl顶点选.append(Cmuvl[i环]);

        #----选择uv相近顶点-------------------------------------------------------------
        for ξ面,mp全部 in enumerate(id.polygons):
            i面点数=len(mp全部.loop_indices);
            for i步3 in range(i面点数):
                ξ点 = mp全部.vertices[i步3];
                i环=mp全部.loop_indices[i步3];
                for muvl in Lmuvl顶点选:
                    if(abs(muvl.uv.x)<abs(Cmuvl[i环].uv.x)+self.fp选择阈值 and abs(Cmuvl[i环].uv.x)-self.fp选择阈值<abs(muvl.uv.x) and abs(muvl.uv.y)<abs(Cmuvl[i环].uv.y)+self.fp选择阈值 and abs(Cmuvl[i环].uv.y)-self.fp选择阈值<abs(muvl.uv.y)):
                        if(Lmv[ξ点].select==False and Lmv[ξ点].hide==False):
                            Lmv[ξ点].select=True;
                        break;

        #--------------------------------------------------------------------------
        bpy.ops.object.editmode_toggle();
        return {"FINISHED"};

#////////////////////////////////////////////
class 卐矩形化选点卐Operator(bpy.types.Operator):
    bl_idname = "bp.rect_selected"
    bl_label = "矩形化选点"
    bl_options = {"REGISTER", "UNDO"}

    fp垂直偏差= FloatProperty(name="垂直偏差", description="垂直偏差",default=0.001,min=0.0, max=0.1, step=5, precision=3,) # soft_min=0.0001, soft_max=0.01,
    """
    bp拉直= BoolProperty(name="拉直", description="拉直",default=False)
    bp自动对齐= BoolProperty(name="自动对齐", description="自动对齐",default=False)
    bp对齐到最后选点= BoolProperty(name="对齐到最后选点", description="对齐到最后选点",default=True)
    bpX= BoolProperty(name="对齐X", description="对齐X",default=False)
    bpY= BoolProperty(name="对齐Y",description="对齐Y",default=False )
    bpZ= BoolProperty(name="对齐Z",description="对齐Z",default=False )
    """
    @classmethod
    def poll(cls, context):#决定是否激活
        oS=context.object
        if (oS!=None and (oS.type=="MESH" or oS.type=="CURVE")and (context.mode=="EDIT_MESH" or context.mode=="EDIT_CURVE" ) ):
            return True;
        return False;

    def draw(self, context):#第貮步
        layout = self.layout;
        #layout.prop(self, "bp不变");
        layout.prop(self, "fp垂直偏差", emboss=True,slider=True);
        """
        uil行=layout.row(align=True);
        uil行.prop(self, "bp拉直");
        uil行.prop(self, "bp自动对齐");
        layout.prop(self, "bp对齐到最后选点");
        uil行=layout.row(align=True);
        #if(not self.bp自动对齐):
        uil行.prop(self, "bpX");uil行.prop(self, "bpY");uil行.prop(self, "bpZ");
        """
    #def invoke(self, context, event):#召唤 第壹步
        #return context.window_manager.invoke_props_dialog(self);

        #☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
        #☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
        #☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐
        #☐☐☐☐☐☐☐☐☐☐┄●━━━━━━━┄●☐☐☐☐☐☐
        #☐☐☐☐☐☐☐☐┄─☐☐☐☐☐☐☐┄─☐┃☐☐☐☐☐☐
        #☐☐☐☐☐☐☐●━━━━━━━━●☐☐☐┃☐☐☐☐☐☐
        #☐☐☐☐☐☐/☐☐☐☐☐☐☐☐/┃☐☐☐┃☐☐☐☐☐☐
        #☐☐☐☐☐/☐☐☐☐☐☐☐☐/☐┃☐☐☐┃☐☐☐☐☐☐
        #☐☐☐☐●━━━━━━━━●☐☐┃☐☐☐┃☐☐☐☐☐☐
        #☐☐☐┆┃┅┈☐☐☐☐┄┗┃☐☐┃☐☐☐┃☐☐☐☐
        #☐☐☐│┃☐☐┅┈┄─☐☐┃☐☐┃☐☐☐┃☐☐☐☐
        #☐☐┆☐┃☐☐┄─┅┈☐☐┃☐☐┃☐☐☐┃☐☐☐☐☐
        #☐☐│☐┃┄─☐☐☐☐┅┈┃☐☐┃☐☐☐┃☐☐☐☐☐
        #☐┆☐☐○━━━━━━━━●☐☐┃☐☐┄●☐☐☐☐☐☐
        #☐●☐☐☐┅┈☐☐☐☐☐☐☐┅┈┃┄─☐☐☐☐☐☐☐☐
        #☐☐☐☐☐☐☐●━━━━━━━━●☐☐☐☐☐☐☐☐☐☐
        #☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐☐


    def execute(self, context): #第三步
        oA=bpy.context.active_object;id=oA.data;
        bm = bmesh.from_edit_mesh(id);select_history=bm.select_history;
        L序十bmv选 = [] ;Lbmv歪=[];Lv乛边=[];bmve最后选=select_history.active;
        #--------------------------------------------------------------------------
        def Δ找连选边(bmv开始点,bmv上一点,bmv此点,i第几个歪,i第几点):
            if(i第几点>6):return ;
            bme下一边=None;
            Lbme选 = [] ;Lbmv选 = [] ;
            for bme连 in bmv此点.link_edges:
                if(bme连.select):
                    #Lbme选.append(bme连);
                    for bmv in bme连.verts:
                        if(bmv!=bmv此点):
                            Lbmv选.append(bmv);
                            if(bmv!=bmv上一点 and bmv!=bmv开始点):
                                bme下一边=bme连;

                                if(bmv上一点):
                                    PRE=bmv上一点.index;
                                else:
                                    PRE=None;
                                #print("start==",bmv开始点.index,"PRE==",PRE,"POINT  this==",bmv.index,);

                            #break;

            v乛0=Lbmv选[1].co-bmv此点.co;v乛1=Lbmv选[0].co-bmv此点.co;
            f夹角=v乛0.angle(v乛1, piΞ2);#print("ANGLE==",f夹角);
            print("ANGLE==",f夹角);

            #----修十垂线---------------------------------------------------------------
            if(f夹角>(piΞ2-self.fp垂直偏差) and (piΞ2+self.fp垂直偏差)>f夹角):#垂直
                v乛垂线修十=vΔΔ修正垂线LIB(v乛0,v乛1);
                if( v乛垂线修十):#如果不垂直
                    v垂线修十位=v乛垂线修十+bmv此点.co;
                    print("FIX==",Lbmv选[0].co,v垂线修十位);
                    Lbmv选[0].co=v垂线修十位;


                L序十bmv选.extend(Lbmv选);
                L序十bmv选.insert(-1,bmv此点);

                i第几个歪=i第几点;
                return ;

            """
            else:
                if(i第几个歪==None or (i第几个歪 ==0) or(i第几个歪 ==1 and i第几点!=3)):
                    L序十bmv选.append(bmv此点);
                else:#第几点 至少>0
                    if(i第几个歪 ==2):
                        L序十bmv选.insert(0,bmv此点);
                    elif(i第几个歪 ==1 and  i第几点==3):
                        L序十bmv选.insert(-1,bmv此点);
            """
            i第几点+=1;

            #--------------------------------------------------------------------------
            if(bme下一边):
                #print("NEXT EDGE==",bme下一边.index);print("--------------------------------------------------------------",);
                for bmv边点 in bme下一边.verts:#最后加入的边
                    if(bmv边点!=bmv此点 and bmv边点!=bmv开始点):
                        #print("BMV edge==",bmv开始点.index,bmv此点.index,bmv边点.index);
                        bmv上一点=bmv此点;
                        bmv此点=bmv边点;
                        #print("BMV start==",bmv开始点);
                        Δ找连选边(bmv开始点,bmv上一点,bmv此点,i第几个歪,i第几点);
                        break;


        #bmv开始点上一点  bme连  bmv边点 ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        # ☐●━━━━━━━→○ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        #      ↑ ☐☐ ☐☐ ☐☐ ☐┃ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        # 连 ┃ ☐☐ ☐☐ ☐☐ ☐┃ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        # 边 ┃ ☐☐ ☐☐ ☐☐ ☐┃ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        # ☐┃ ☐☐ ☐☐ ☐☐ ☐↓ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        # ☐○←━━━━━━━○ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐
        # ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐ ☐☐

        for bmv in bm.verts:
            if (bmv.select):
                i第几个歪=None;i第几点=0;bmv上一点=None;
                Δ找连选边(bmv,bmv上一点,bmv,i第几个歪,i第几点);
                break;

        #--------------------------------------------------------------------------、
        if(len(L序十bmv选)!=3):
            self.report({"WARNING"},"两个以上歪点");#"INFO" "ERROR" "DEBUG"
            return {"FINISHED"};
        #----找出歪点--------------------------------------------------------------
        for bmv in bm.verts:
            if(bmv.select and bmv not in L序十bmv选):
                Lbmv歪.append(bmv);
                break;

        v中间点位=(L序十bmv选[-1].co-L序十bmv选[0].co)/2+L序十bmv选[0].co;
        v歪位应=(v中间点位-L序十bmv选[1].co)*2+L序十bmv选[1].co;
        #f对角线长=(L序十bmv选[-1].co-L序十bmv选[1].co).length;
        #f对角线长=sqrt(pow(f3斜边乛[0],2)+pow(f3斜边乛[1],2)+pow(f3斜边乛[2],2));
        Lbmv歪[0].co=v歪位应;

        id.update();

        return {"FINISHED"}

#//////////////////////////////////////////////////
class 卐轴到所选卐Operator(bpy.types.Operator):
    bl_idname = "bp.axis_to_selected"
    bl_label = "轴到所选"
    bl_options = {"REGISTER", "UNDO"}
    bp不变= BoolProperty(name="保持方向", description="保持方向",default=False,update=ΔUPDATE选择 )
    bp法线= BoolProperty(name="法线方向",description="法线方向",default=False,update=ΔUPDATE选择 )

    @classmethod
    def poll(cls, context):#决定是否激活
        oS=context.object
        if (oS!=None and (oS.type=="MESH" or oS.type=="CURVE")and (context.mode=="EDIT_MESH" or context.mode=="EDIT_CURVE" ) ):
            return True;
        return False;

    def draw(self, context):#第貮步
        layout = self.layout;
        #layout.prop(self, "bp不变");
        layout.prop(self, "bp法线");

    def invoke(self, context, event):#召唤 第壹步
        return context.window_manager.invoke_props_dialog(self);

    def execute(self, context): #第三步
        oA=context.active_object;
        bpy.ops.object.editmode_toggle();
        if(oA.scale!=Vector((1,1,1))):
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True);


        v物位之前=oA.location.copy();
        #v缩放之前=oA.scale.copy();
        m物之前=oA.matrix_world.copy();
        m3物之前=m物之前.to_3x3() ;#只计方向 不计位置
        Lv物点位全局=[];LskLv物点位全局=[];Lsk=[];

        #----CURVE----------------------------------------------------------------
        LspS=[];
        if(oA.type=="CURVE"):
            spline0=oA.data.splines[0];
            if(spline0.type!='BEZIER'):
                for sp in spline0.points:
                    if(sp.select):
                        LspS.append(sp);
            else:
                for bsp in spline0.bezier_points:
                    if(bsp.select_control_point):
                        LspS.append(bsp);
            #----获所有点位置-------------------------------------------------------------
            key=oA.data.shape_keys;v3=Vector((0.0,0.0,0.0));
            if(not key):
                if(spline0.type!='BEZIER'):
                    for spline in oA.data.splines:
                        for sp in spline.points:#BezierSplinePoint  <bsp
                            v3[0]=sp.co[0];v3[1]=sp.co[1];v3[2]=sp.co[2];
                            Lv物点位全局.append(m物之前*v3);
                    print("Lv==",Lv物点位全局);
                else:
                    for spline in oA.data.splines:
                        for bsp in spline.bezier_points:#BezierSplinePoint  <bsp
                            Lv物点位全局.append(m物之前*bsp.co);

            else:
                Lsk=key.key_blocks
                for i, sk in enumerate(Lsk):
                    LskLv物点位全局.append([]);
                    dt=sk.data;
                    for d in dt:
                        LskLv物点位全局[i].append(m物之前*d.co);

        #----MESH-----------------------------------------------------------------
        elif(oA.type=="MESH"):
            Lv物点=oA.data.vertices;
            key=oA.data.shape_keys;
            if(not key ):
                for mv in oA.data.vertices:
                    Lv物点位全局.append(m物之前*mv.co);
                #print("LV==",LΔΔ保留4位小数(Lv物点位全局[0]),LΔΔ保留4位小数(Lv物点位全局[1]),LΔΔ保留4位小数(Lv物点位全局[2]),LΔΔ保留4位小数(Lv物点位全局[3]));

            else:
                #for mv in oA.data.vertices:Lv物点位全局.append(m物之前*mv.co);#■■

                Lsk=key.key_blocks
                for i, sk in enumerate(Lsk):
                    LskLv物点位全局.append([]);
                    dt=sk.data;
                    for d in dt:
                        LskLv物点位全局[i].append(m物之前*d.co);


                for skLv物点位全局 in LskLv物点位全局:
                    print("LVsk=",LΔΔ保留4位小数(skLv物点位全局[0]),LΔΔ保留4位小数(skLv物点位全局[1]),LΔΔ保留4位小数(skLv物点位全局[2]),LΔΔ保留4位小数(skLv物点位全局[3]));


            Lmp=oA.data.polygons;Lme=oA.data.edges;Lmv=oA.data.vertices;
            LmpS=[];LmeS=[];LmvS=[];
            for mp in Lmp:
                if(mp.select):
                    LmpS.append(mp);
            print("LmpS==",len(LmpS));
            for me in Lme:
                if(me.select):
                    LmeS.append(me);
            for mv in Lmv:
                if(mv.select):
                    LmvS.append(mv);

            if(len(LmpS)>0):
                i面点数=len(LmpS[0].loop_indices);
            v尺寸=oA.dimensions;#print("dimensions==",v尺寸.x*0.2);
            #----选择了两线------------------------------------------------------------
            if(len(LmeS)==2):
                mv点0=Lv物点[LmeS[0].vertices[0]];mv点1=Lv物点[LmeS[0].vertices[1]];mv点2=Lv物点[LmeS[1].vertices[0]];mv点3=Lv物点[LmeS[1].vertices[1]];
                v法线1=m3物之前*(mv点0.normal+mv点1.normal);print("Normal 1==",v法线1);
                v法线2=m3物之前*(mv点2.normal+mv点3.normal);print("Normal 2==",v法线2);
                v共法Z=v法线1+v法线2;
                v点位0=mv点0.co;v点位1=mv点1.co;v点位2=mv点2.co;v点位3=mv点3.co;
                if(v共法Z.length<v尺寸.x*0.3):
                    v共法Z=m3物之前*(v点位0-v点位1);
                    print("Z==",v共法Z);

                v中点0=(v点位0+v点位1)/2;
                v中点1=(v点位2+v点位3)/2;
                v乛X=m3物之前*(v中点1-v中点0); print("vX==",v乛X);
                m应=m巜2v(v乛X,None,v共法Z,None,2);
                v位应=m物之前*((v点位0+v点位1+v点位2+v点位3)/4);m应[0][3],m应[1][3],m应[2][3]=v位应[0],v位应[1],v位应[2] ;#位应


            #----选择了一个面-------------------------------------------------------------
            elif(len(LmpS)==1 and i面点数>3):

                v法线Z=m3物之前*(LmpS[0].normal);print("Normal==",v法线Z);

                v点位0=Lv物点[LmpS[0].vertices[0]].co;v点位1=Lv物点[LmpS[0].vertices[1]].co;
                v点位2=Lv物点[LmpS[0].vertices[2]].co;v点位3=Lv物点[LmpS[0].vertices[3]].co;
                f3中点1=[(v点位0[0]+v点位1[0])/2,(v点位0[1]+v点位1[1])/2,(v点位0[2]+v点位1[2])/2];
                f3中点2=[(v点位2[0]+v点位3[0])/2,(v点位2[1]+v点位3[1])/2,(v点位2[2]+v点位3[2])/2];
                v乛边到边X=m3物之前*Vector(([f3中点2[0]-f3中点1[0],f3中点2[1]-f3中点1[1],f3中点2[2]-f3中点1[2]]));

                m应=m巜2v(v乛边到边X,None,v法线Z,None,2);
                v位应=m物之前*((v点位0+v点位1+v点位2+v点位3)/4);m应[0][3],m应[1][3],m应[2][3]=v位应[0],v位应[1],v位应[2] ;#位应
                #print("v4==",v位应);

            #----选择了两个面----------------------------------------------------------
            elif(len(LmpS)==2 and i面点数>3):
                v法线1=m3物之前*(LmpS[0].normal);print("Normal 1==",v法线1);
                v法线2=m3物之前*(LmpS[1].normal);print("Normal 2==",v法线2);
                v共法Z=v法线1+v法线2;
                print("vZ==",v共法Z,v共法Z.length);
                if(v共法Z.length<v尺寸.x*0.2):
                    v点位0=(Lv物点[LmpS[0].vertices[0]].co);v点位1=(Lv物点[LmpS[0].vertices[1]].co);
                    v点位2=(Lv物点[LmpS[0].vertices[2]].co);v点位3=(Lv物点[LmpS[0].vertices[3]].co);
                    f3中点1=[(v点位0[0]+v点位1[0])/2,(v点位0[1]+v点位1[1])/2,(v点位0[2]+v点位1[2])/2];
                    f3中点2=[(v点位2[0]+v点位3[0])/2,(v点位2[1]+v点位3[1])/2,(v点位2[2]+v点位3[2])/2];
                    v共法Z=m3物之前*Vector(([f3中点2[0]-f3中点1[0],f3中点2[1]-f3中点1[1],f3中点2[2]-f3中点1[2]]));
                    print("vZ Zero==",v共法Z);


                v乛X=m3物之前*(LmpS[0].center)-m3物之前*(LmpS[1].center);

                m应=m巜2v(v乛X,None,v共法Z,None,1);
                v位应=m物之前*((LmpS[0].center+LmpS[1].center)/2);m应[0][3],m应[1][3],m应[2][3]=v位应[0],v位应[1],v位应[2] ;#位应
                print("vLoc==",v位应);
            #--------------------------------------------------------------------------
            else:
                if(self.bp法线):
                    self.report({"ERROR"},"不能选法线");#"INFO" "ERROR" "DEBUG"
                    return {"FINISHED"};
        #====其它选择情况==============================================
        if(not self.bp法线):
            v总和=Vector((0.0,0.0,0.0));
            m应=m物之前;
            if(oA.type=="MESH"):
                for mv in LmvS:
                    v总和+=mv.co;
                v位应=m物之前*((v总和)/len(LmvS));
                print("V SHOULD==",v位应);
            elif(oA.type=="CURVE"):
                for sp in LspS:
                    v总和[0]+=sp.co[0];v总和[1]+=sp.co[1];    v总和[2]+=sp.co[2] ;

                v位应=m物之前*((v总和)/len(LspS));

            m应[0][3],m应[1][3],m应[2][3]=v位应[0],v位应[1],v位应[2] ;#位应



        #----赋值点位---------------------------------------------------------------
        """"""
        oA.matrix_world=m应;
        #oA.scale=v缩放之前;#print("SCALE==",v缩放之前);

        m物应逆= m应.inverted();

        if(oA.type=="MESH"):
            if(not LskLv物点位全局 ):
                for i,mv in enumerate(oA.data.vertices):
                    mv.co=m物应逆*(Lv物点位全局[i]);#print("MESH",);
                #return {"FINISHED"};
            else:
                print("SK",);#return {"FINISHED"};
                for i,sk in enumerate(Lsk):
                    dt=sk.data;
                    for j,d in enumerate(dt):
                        d.co=m物应逆*(LskLv物点位全局[i][j]);

        #--------------------------------------------------------------------------
        elif(oA.type=="CURVE"):
            if(not LskLv物点位全局 ):
                if(spline0.type!="BEZIER"):
                    for i,sp in enumerate(spline0.points):
                        v=m物应逆*(Lv物点位全局[i]);
                        sp.co[0]=v[0];sp.co[1]=v[1];sp.co[2]=v[2];

                else:
                    for i,bsp in enumerate(spline0.bezier_points):
                        bsp.co=m物应逆*(Lv物点位全局[i]);

            else:
                for i,sk in enumerate(Lsk):
                    dt=sk.data;
                    for j,d in enumerate(dt):
                        d.co=m物应逆*(LskLv物点位全局[i][j]);

        #bpy.ops.object.editmode_toggle();
        #print("m应==",m物应逆);
        bpy.ops.object.editmode_toggle();
        return {"FINISHED"};




#///end////end////end////end////end////end////end////end////end////










