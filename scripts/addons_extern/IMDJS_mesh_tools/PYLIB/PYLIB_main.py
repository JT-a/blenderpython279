

import bpy,sys,os,imp,random

from bpy.props import *
from mathutils import Matrix,Vector,Euler
from ctypes import*
from bpy_extras import object_utils
import bmesh
from math import*

#==============================================================
path目录PYLIB上级 =os.path.abspath(os.path.join(os.path.dirname(__file__),".."));#上级目录 
目录PYLIB上级=os.path.basename(path目录PYLIB上级);
path目录MUT = os.path.dirname(__file__); #本py文件所在目录
文件夹此=os.path.basename(path目录MUT);  #IMDJS_NodeTree

try:
    from .PYLIB_math import*
except:pass;
try:
    from .PYLIB_mesh import*
except:
    print("!!!!! ERROR import PYLIB_mesh",);

try:
    from .PYLIB_object import*
except:
    print("!!!!! ERROR import PYLIB_object",);
try:
    from .PYLIB_attribute import*
except:
    print("!!!!! ERROR import PYLIB_attribute",);
from .PYLIB_attribute import dllΔ载入dllLIB,dllΔ卸载dllLIB,Δ载入模块LIB,Δ删除模块LIB;

try:
    from .PYLIB_algorithm import*
except:
    print("!!!!! ERROR import PYLIB_algorithm",);
try:
    from .PYLIB_string import*
except:
    print("!!!!! ERROR import PYLIB_string",);
try:
    from .PYLIB_find import*
except:
    print("!!!!! ERROR import PYLIB_algorithm",);
#try:
from .PYLIB_print import*
#except:pass;
#try:
from .PYLIB_draw import*

from .PYLIB_operator import*
"""
except:
    print("can't not import PYLIB_draw ",);
    pass;    
"""



#////////////////////////////////////////////////
global iG;iG=0;#global Ds名o物G;Ds名o物G={};

def ΔΔaddTEST1( i,j):
    global iG;
    iG+=20;
    print("iG++==",iG);
    from object_presets.my_class import addClass;#不能一开始就导入 这会导致循环导入
    addClass( i,j);
    return (i+j)*5;

def ΔΔaddTEST( i,j):
    print("addTEST==",i+j);
    return (i+j)*5;



class 卐卸载DLLlib卐Operator(bpy.types.Operator):
    bl_idname = "dele.dll_lib";
    bl_label = "卸载dll";
    bl_options = {"REGISTER", "UNDO"};

    @classmethod
    def poll(cls, context):
        return True; #(obj and obj.type == "MESH")
    def execute(self, context):
        if(LIBG.dll):
            windll.kernel32.FreeLibrary.argtypes = [HMODULE];
            windll.kernel32.FreeLibrary(LIBG.dll._handle);#释放dll
            LIBG.dll=None;
        print("delete DLL ~//////////////////////////////////////////",);
        return {"FINISHED"};


class 卐载入DLLlib卐Operator(bpy.types.Operator):
    bl_idname = "load.dll_lib";
    bl_label = "载入dll";
    bl_options = {"REGISTER", "UNDO"};

    @classmethod
    def poll(cls, context):
        return True; #(obj and obj.type == "MESH")
    def execute(self, context):
        #D=卐DLL类型();
        try:
            LIBG.dll = CDLL(dllpath32);
        except:
            LIBG.dll = CDLL(dllpath64);
        return {"FINISHED"};


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





#//////////////////////////////////////////////////
零=0;
def ΔΔTextureImage保存(mat或lamp,s类型,Ds条目f值):
    b是修改器材质=False;
    if(hasattr(mat或lamp,"texture")):#是修改器材质只有一个
        print("IS MODIFIER",);
        b是修改器材质=True;
        Lmts=[mat或lamp];
    else:
        Lmts=mat或lamp.texture_slots ;#MaterialTextureSlot  贴图槽
        #print("Lmts==",Lmts);
    Ds条目f值["BI_TEXTURE"]={};
    for i贴图槽位置, mts in enumerate (Lmts):
        if(mts!=None and mts.texture!=None):
            #print("MTS==",mts);
            D={};D["TEXTURE"]={};
            if(not b是修改器材质):
                D["use"]=mts.use;
            D["TEXTURE"]["TEXTURE_NAME"]=mts.texture.name;
            D["TEXTURE"]["type"]=mts.texture.type;
            D["TEXTURE"]["use_preview_alpha"]=mts.texture.use_preview_alpha;
            D["TEXTURE"]["use_color_ramp"]=mts.texture.use_color_ramp;
            if(mts.texture.use_color_ramp):
                D["COLORRAMP"]={};
                ΔΔColorRamp保存(D["COLORRAMP"][str(i贴图槽位置)],mts.texture.color_ramp);

            D["TEXTURE"]["factor_red"]=mts.texture.factor_red;
            D["TEXTURE"]["factor_green"]=mts.texture.factor_green;
            D["TEXTURE"]["factor_blue"]=mts.texture.factor_blue;
            D["TEXTURE"]["intensity"]=mts.texture.intensity;
            D["TEXTURE"]["contrast"]=mts.texture.contrast;
            D["TEXTURE"]["saturation"]=mts.texture.saturation;
            D["TEXTURE"]["use_clamp"]=mts.texture.use_clamp;
            #----贴图----------------------------------------------------------------
            if(mts.texture.type=="IMAGE" ):
                D["IMAGE"]={};D["IMAGEIMAGE"]={};
                if(mts.texture.image!=None):
                    D["IMAGEIMAGE"]["IMAGE_NAME"]=mts.texture.image.name;
                    D["IMAGEIMAGE"]["source"]=mts.texture.image.source;
                    D["IMAGEIMAGE"]["filepath"]=mts.texture.image.filepath;
                    D["IMAGEIMAGE"]["use_view_as_render"]=mts.texture.image.use_view_as_render;
                    D["IMAGEIMAGE"]["image_use_alpha"]=mts.texture.image.use_alpha;
                    D["IMAGEIMAGE"]["alpha_mode"]=mts.texture.image.alpha_mode;
                    D["IMAGEIMAGE"]["use_fields"]=mts.texture.image.use_fields;
                    D["IMAGEIMAGE"]["field_order"]=mts.texture.image.field_order;
                #---图像采样----------------------------------------------------------------
                try:#有些贴图类型没有这些属性
                    D["IMAGE"]["use_alpha"]=mts.texture.use_alpha;
                    D["IMAGE"]["use_calculate_alpha"]=mts.texture.use_calculate_alpha;
                    D["IMAGE"]["invert_alpha"]=mts.texture.invert_alpha;
                    D["IMAGE"]["use_flip_axis"]=mts.texture.use_flip_axis;
                    D["IMAGE"]["use_normal_map"]=mts.texture.use_normal_map;
                    D["IMAGE"]["normal_map_space"]=mts.normal_map_space;
                    D["IMAGE"]["use_derivative_map"]=mts.texture.use_derivative_map;
                    D["IMAGE"]["use_mipmap"]=mts.texture.use_mipmap;
                    D["IMAGE"]["use_mipmap_gauss"]=mts.texture.use_mipmap_gauss;
                    D["IMAGE"]["use_interpolation"]=mts.texture.use_interpolation;
                    D["IMAGE"]["filter_type"]=mts.texture.filter_type;
                    D["IMAGE"]["filter_eccentricity"]=mts.texture.filter_eccentricity;
                    D["IMAGE"]["filter_size"]=mts.texture.filter_size;
                    D["IMAGE"]["use_filter_size_min"]=mts.texture.use_filter_size_min;
                    #----图像映射---------------------------------------------------------------
                    D["IMAGE"]["extension"]=mts.texture.extension;
                    D["IMAGE"]["repeat_x"]=mts.texture.repeat_x;D["IMAGE"]["repeat_y"]=mts.texture.repeat_y;
                    D["IMAGE"]["use_mirror_x"]=mts.texture.use_mirror_x;D["IMAGE"]["use_mirror_y"]=mts.texture.use_mirror_y;
                    D["IMAGE"]["crop_min_x"]=mts.texture.crop_min_x;D["IMAGE"]["crop_min_y"]=mts.texture.crop_min_y;
                    D["IMAGE"]["crop_max_x"]=mts.texture.crop_max_x;D["IMAGE"]["crop_max_y"]=mts.texture.crop_max_y;                
                except:pass;    
               

            #----马形分氏-----------------------------------------------------------------
            if(mts.texture.type=="MUSGRAVE"):
                D["MUSGRAVE"]={};
                D["MUSGRAVE"]["musgrave_type"]=mts.texture.musgrave_type;
                D["MUSGRAVE"]["lacunarity"]=mts.texture.lacunarity;
                D["MUSGRAVE"]["dimension_max"]=mts.texture.dimension_max;
                D["MUSGRAVE"]["octaves"]=mts.texture.octaves;
                D["MUSGRAVE"]["offset"]=mts.texture.offset;
                D["MUSGRAVE"]["noise_intensity"]=mts.texture.noise_intensity;
                D["MUSGRAVE"]["gain"]=mts.texture.gain;
                D["MUSGRAVE"]["noise_basis"]=mts.texture.noise_basis;
                D["MUSGRAVE"]["noise_scale"]=mts.texture.noise_scale;
                D["MUSGRAVE"]["nabla"]=mts.texture.nabla;
            #----树木-----------------------------------------------------------------
            if(mts.texture.type=="WOOD"):
                D["WOOD"]={};
                D["WOOD"]["nabla"]=mts.texture.nabla;
                D["WOOD"]["noise_basis"]=mts.texture.noise_basis;
                D["WOOD"]["noise_basis_2"]=mts.texture.noise_basis_2;
                D["WOOD"]["noise_scale"]=mts.texture.noise_scale;
                D["WOOD"]["noise_type"]=mts.texture.noise_type;
                D["WOOD"]["turbulence"]=mts.texture.turbulence;
                D["WOOD"]["wood_type"]=mts.texture.wood_type;
                #D["WOOD"]["users_material"]=mts.texture.users_material;#唯读
                #D["WOOD"]["users_object_modifier"]=mts.texture.users_object_modifier;#唯读
            #----STUCCI-----------------------------------------------------------------
            if(mts.texture.type=="STUCCI"):
                D["STUCCI"]={};
                D["STUCCI"]["noise_basis"]=mts.texture.noise_basis;
                D["STUCCI"]["noise_scale"]=mts.texture.noise_scale;
                D["STUCCI"]["noise_type"]=mts.texture.noise_type;
                D["STUCCI"]["stucci_type"]=mts.texture.stucci_type;
                D["STUCCI"]["turbulence"]=mts.texture.turbulence;
                #D["STUCCI"]["users_material"]=mts.texture.users_material;
                #D["STUCCI"]["users_object_modifier"]=mts.texture.users_object_modifier;
            #----NOISE-----------------------------------------------------------------
            #if(mts.texture.type=="NOISE"):
                #D["STUCCI"]["users_material"]=mts.texture.users_material;
                #D["STUCCI"]["users_object_modifier"]=mts.texture.users_object_modifier;
            #----VOXEL_DATA-----------------------------------------------------------------
            if(mts.texture.type=="VOXEL_DATA"):
                D["VOXEL_DATA"]={};
                if(mts.texture.image!=None):
                    D["VOXEL_DATA"]["IMAGE_NAME"]=mts.texture.image.name;
                    D["VOXEL_DATA"]["source"]=mts.texture.image.source;
                    D["VOXEL_DATA"]["filepath"]=mts.texture.image.filepath;
                    D["VOXEL_DATA"]["use_view_as_render"]=mts.texture.image.use_view_as_render;
                    D["VOXEL_DATA"]["image_use_alpha"]=mts.texture.image.use_alpha;
                    D["VOXEL_DATA"]["alpha_mode"]=mts.texture.image.alpha_mode;
                    D["VOXEL_DATA"]["use_fields"]=mts.texture.image.use_fields;
                    D["VOXEL_DATA"]["field_order"]=mts.texture.image.field_order;

                if(mts.texture.image_user!=None):
                    D["VOXEL_DATA"]["fields_per_frame"]=mts.texture.image_user.fields_per_frame;
                    D["VOXEL_DATA"]["frame_current"]=mts.texture.image_user.frame_current;
                    D["VOXEL_DATA"]["frame_duration"]=mts.texture.image_user.frame_duration;
                    D["VOXEL_DATA"]["frame_offset"]=mts.texture.image_user.frame_offset;
                    D["VOXEL_DATA"]["frame_start"]=mts.texture.image_user.frame_start;
                    D["VOXEL_DATA"]["multilayer_layer"]=mts.texture.image_user.multilayer_layer;
                    D["VOXEL_DATA"]["multilayer_pass"]=mts.texture.image_user.multilayer_pass;
                    D["VOXEL_DATA"]["use_auto_refresh"]=mts.texture.image_user.use_auto_refresh;
                    D["VOXEL_DATA"]["use_cyclic"]=mts.texture.image_user.use_cyclic;
                if(mts.texture.voxel_data!=None):
                    D["VOXEL_DATA"]["DOMAIN_OBJECT_NAME"]=mts.texture.voxel_data.domain_object.name;
                    D["VOXEL_DATA"]["extension"]=mts.texture.voxel_data.extension;
                    D["VOXEL_DATA"]["file_format"]=mts.texture.voxel_data.file_format;
                    D["VOXEL_DATA"]["filepath"]=mts.texture.voxel_data.filepath;
                    D["VOXEL_DATA"]["intensity"]=mts.texture.voxel_data.intensity;
                    D["VOXEL_DATA"]["interpolation"]=mts.texture.voxel_data.interpolation;
                    D["VOXEL_DATA"]["resolution"]=mts.texture.voxel_data.resolution;
                    D["VOXEL_DATA"]["smoke_data_type"]=mts.texture.voxel_data.smoke_data_type;
                    D["VOXEL_DATA"]["still_frame"]=mts.texture.voxel_data.still_frame;
                    D["VOXEL_DATA"]["use_still_frame"]=mts.texture.voxel_data.use_still_frame;

                    #D["VOXEL_DATA"]["users_material"]=mts.texture.users_material;
                    #D["VOXEL_DATA"]["users_material"]=mts.texture.users_object_modifier;
            #----MAGIC-----------------------------------------------------------------
            if(mts.texture.type=="MAGIC"):
                D["MAGIC"]={};
                D["MAGIC"]["noise_depth"]=mts.texture.noise_depth;
                D["MAGIC"]["turbulence"]=mts.texture.turbulence;
                #D["MAGIC"]["users_material"]=mts.texture.users_material;
                #D["MAGIC"]["users_object_modifier"]=mts.texture.users_object_modifier;
            #----OCEAN-----------------------------------------------------------------
            if(mts.texture.type=="OCEAN"):
                D["OCEAN"]={};
                if(mts.texture.ocean!=None):
                    D["OCEAN"]["OCEAN_OBJECT_NAME"]=mts.texture.ocean.ocean_object.name;
                    D["OCEAN"]["output"]=mts.texture.ocean.output;

                #D["OCEAN"]["noise_depth"]=mts.texture.users_material;
                #D["OCEAN"]["noise_depth"]=mts.texture.users_object_modifier;
            #----POINT_DENSITY-----------------------------------------------------------
            if(mts.texture.type=="POINT_DENSITY"):
                D["POINT_DENSITY"]={};
                if(mts.texture.point_density!=None):
                    D["POINT_DENSITY"]["COLORRAMP"]={};
                    ΔΔColorRamp保存(D["POINT_DENSITY"]["COLORRAMP"]["0"],mts.texture.point_density.color_ramp);

                    D["POINT_DENSITY"]["color_source"]=mts.texture.point_density.color_source;
                    D["POINT_DENSITY"]["falloff"]=mts.texture.point_density.falloff;
                    D["POINT_DENSITY"]["use_falloff_curve"]=mts.texture.point_density.use_falloff_curve;
                    if(D["POINT_DENSITY"]["use_falloff_curve"]==True):
                        D["POINT_DENSITY"]["MAPPING"]={};
                        ΔΔmapping保存(D["POINT_DENSITY"]["MAPPING"]["0"],mts.texture.point_density.falloff_curve);

                    D["POINT_DENSITY"]["falloff_soft"]=mts.texture.point_density.falloff_soft;
                    D["POINT_DENSITY"]["falloff_speed_scale"]=mts.texture.point_density.falloff_speed_scale;
                    D["POINT_DENSITY"]["noise_basis"]=mts.texture.point_density.noise_basis;
                    D["POINT_DENSITY"]["OBJECT_NAME"]=mts.texture.point_density.object.name;
                    D["POINT_DENSITY"]["particle_cache_space"]=mts.texture.point_density.particle_cache_space;
                    D["POINT_DENSITY"]["PARTICLE_SYSTEM_NAME"]=mts.texture.point_density.particle_system.name;
                    D["POINT_DENSITY"]["point_source"]=mts.texture.point_density.point_source;
                    D["POINT_DENSITY"]["radius"]=mts.texture.point_density.radius;
                    D["POINT_DENSITY"]["speed_scale"]=mts.texture.point_density.speed_scale;
                    D["POINT_DENSITY"]["turbulence_depth"]=mts.texture.point_density.turbulence_depth;
                    D["POINT_DENSITY"]["turbulence_influence"]=mts.texture.point_density.turbulence_influence;
                    D["POINT_DENSITY"]["turbulence_scale"]=mts.texture.point_density.turbulence_scale;
                    D["POINT_DENSITY"]["turbulence_strength"]=mts.texture.point_density.turbulence_strength;
                    D["POINT_DENSITY"]["use_falloff_curve"]=mts.texture.point_density.use_falloff_curve;
                    D["POINT_DENSITY"]["use_turbulence"]=mts.texture.point_density.use_turbulence;
                    D["POINT_DENSITY"]["vertex_cache_space"]=mts.texture.point_density.vertex_cache_space;

            #----MARBLE-----------------------------------------------------------------
            if(mts.texture.type=="MARBLE"):
                D["MARBLE"]={};
                D["MARBLE"]["marble_type"]=mts.texture.marble_type;
                D["MARBLE"]["nabla"]=mts.texture.nabla;
                D["MARBLE"]["noise_basis"]=mts.texture.noise_basis;
                D["MARBLE"]["noise_basis_2"]=mts.texture.noise_basis_2;
                D["MARBLE"]["noise_depth"]=mts.texture.noise_depth;
                D["MARBLE"]["noise_scale"]=mts.texture.noise_scale;
                D["MARBLE"]["noise_type"]=mts.texture.noise_type;
                D["MARBLE"]["turbulence"]=mts.texture.turbulence;
                #D["MARBLE"]["users_material"]=mts.texture.users_material;
                #D["MARBLE"]["users_object_modifier"]=mts.texture.users_object_modifier;
            #----CLOUDS-----------------------------------------------------------------
            if(mts.texture.type=="CLOUDS"):
                D["CLOUDS"]={};
                D["CLOUDS"]["cloud_type"]=mts.texture.cloud_type;
                D["CLOUDS"]["nabla"]=mts.texture.nabla;
                D["CLOUDS"]["noise_basis"]=mts.texture.noise_basis;
                D["CLOUDS"]["noise_depth"]=mts.texture.noise_depth;
                D["CLOUDS"]["noise_scale"]=mts.texture.noise_scale;
                D["CLOUDS"]["noise_type"]=mts.texture.noise_type;
                #D["CLOUDS"]["users_material"]=mts.texture.users_material;
                #D["CLOUDS"]["users_object_modifier"]=mts.texture.users_object_modifier;
            #----VORONOI-----------------------------------------------------------------
            if(mts.texture.type=="VORONOI"):
                D["VORONOI"]={};
                D["VORONOI"]["color_mode"]=mts.texture.color_mode;
                D["VORONOI"]["distance_metric"]=mts.texture.distance_metric;
                D["VORONOI"]["minkovsky_exponent"]=mts.texture.minkovsky_exponent;
                D["VORONOI"]["nabla"]=mts.texture.nabla;
                D["VORONOI"]["noise_intensity"]=mts.texture.noise_intensity;
                D["VORONOI"]["noise_scale"]=mts.texture.noise_scale;
                D["VORONOI"]["weight_1"]=mts.texture.weight_1;
                D["VORONOI"]["weight_2"]=mts.texture.weight_2;
                D["VORONOI"]["weight_3"]=mts.texture.weight_3;
                D["VORONOI"]["weight_4"]=mts.texture.weight_4;
                #D["VORONOI"]["users_material"]=mts.texture.users_material;
                #D["VORONOI"]["users_object_modifier"]=mts.texture.users_object_modifier;
            #----BLEND-----------------------------------------------------------------
            """"""
            if(mts.texture.type=="BLEND"):
                D["BLEND"]={};
                D["BLEND"]["progression"]=mts.texture.progression;
                D["BLEND"]["use_flip_axis"]=mts.texture.use_flip_axis;
                #D["BLEND"]["users_material"]=mts.texture.users_material; #唯读
                #D["BLEND"]["users_object_modifier"]=mts.texture.users_object_modifier; #唯读

            #----ENVIRONMENT_MAP-----------------------------------------------------------------
            if(mts.texture.type=="ENVIRONMENT_MAP"):
                D["ENVIRONMENT_MAP"]={};
                if(mts.texture.environment_map!=None):
                    D["ENVIRONMENT_MAP"]["clip_end"]=mts.texture.environment_map.clip_end;
                    D["ENVIRONMENT_MAP"]["clip_start"]=mts.texture.environment_map.clip_start;
                    D["ENVIRONMENT_MAP"]["depth"]=mts.texture.environment_map.depth;
                    D["ENVIRONMENT_MAP"]["is_valid"]=mts.texture.environment_map.is_valid;
                    D["ENVIRONMENT_MAP"]["layers_ignore"]=mts.texture.environment_map.layers_ignore;
                    D["ENVIRONMENT_MAP"]["mapping"]=mts.texture.environment_map.mapping;
                    D["ENVIRONMENT_MAP"]["resolution"]=mts.texture.environment_map.resolution;
                    D["ENVIRONMENT_MAP"]["source"]=mts.texture.environment_map.source;
                    D["ENVIRONMENT_MAP"]["VIEWPOINT_OBJECT_NAME"]=mts.texture.environment_map.viewpoint_object.name;
                    D["ENVIRONMENT_MAP"]["zoom"]=mts.texture.environment_map.zoom;

                D["ENVIRONMENT_MAP"]["filter_eccentricity"]=mts.texture.filter_eccentricity;
                D["ENVIRONMENT_MAP"]["filter_probes"]=mts.texture.filter_probes;
                D["ENVIRONMENT_MAP"]["filter_size"]=mts.texture.filter_size;
                D["ENVIRONMENT_MAP"]["filter_type"]=mts.texture.filter_type;
                if(mts.texture.image!=None):
                    D["ENVIRONMENT_MAP"]["IMAGE_NAME"]=mts.texture.image.name;
                    D["ENVIRONMENT_MAP"]["source"]=mts.texture.image.source;
                    D["ENVIRONMENT_MAP"]["filepath"]=mts.texture.image.filepath;
                    D["ENVIRONMENT_MAP"]["use_view_as_render"]=mts.texture.image.use_view_as_render;
                    D["ENVIRONMENT_MAP"]["image_use_alpha"]=mts.texture.image.use_alpha;
                    D["ENVIRONMENT_MAP"]["alpha_mode"]=mts.texture.image.alpha_mode;
                    D["ENVIRONMENT_MAP"]["use_fields"]=mts.texture.image.use_fields;
                    D["ENVIRONMENT_MAP"]["field_order"]=mts.texture.image.field_order;
                if(mts.texture.image_user!=None):
                    D["ENVIRONMENT_MAP"]["fields_per_frame"]=mts.texture.image_user.fields_per_frame;
                    D["ENVIRONMENT_MAP"]["frame_current"]=mts.texture.image_user.frame_current;
                    D["ENVIRONMENT_MAP"]["frame_duration"]=mts.texture.image_user.frame_duration;
                    D["ENVIRONMENT_MAP"]["frame_offset"]=mts.texture.image_user.frame_offset;
                    D["ENVIRONMENT_MAP"]["frame_start"]=mts.texture.image_user.frame_start;
                    D["ENVIRONMENT_MAP"]["multilayer_layer"]=mts.texture.image_user.multilayer_layer;
                    D["ENVIRONMENT_MAP"]["multilayer_pass"]=mts.texture.image_user.multilayer_pass;
                    D["ENVIRONMENT_MAP"]["use_auto_refresh"]=mts.texture.image_user.use_auto_refresh;
                    D["ENVIRONMENT_MAP"]["use_cyclic"]=mts.texture.image_user.use_cyclic;

                D["ENVIRONMENT_MAP"]["use_filter_size_min"]=mts.texture.use_filter_size_min;
                D["ENVIRONMENT_MAP"]["use_mipmap"]=mts.texture.use_mipmap;
                D["ENVIRONMENT_MAP"]["use_mipmap_gauss"]=mts.texture.use_mipmap_gauss;
                #D["ENVIRONMENT_MAP"]["users_material"]=mts.texture.users_material;
                #D["ENVIRONMENT_MAP"]["users_object_modifier"]=mts.texture.users_object_modifier;

            #----DISTORTED_NOISE-----------------------------------------------------------------
            if(mts.texture.type=="DISTORTED_NOISE"):
                D["DISTORTED_NOISE"]={};
                D["DISTORTED_NOISE"]["distortion"]=mts.texture.distortion;
                D["DISTORTED_NOISE"]["nabla"]=mts.texture.nabla;
                D["DISTORTED_NOISE"]["noise_basis"]=mts.texture.noise_basis;
                D["DISTORTED_NOISE"]["noise_distortion"]=mts.texture.noise_distortion;
                D["DISTORTED_NOISE"]["noise_scale"]=mts.texture.noise_scale;
                #D["DISTORTED_NOISE"]["users_material"]=mts.texture.users_material;
                #D["DISTORTED_NOISE"]["users_object_modifier"]=mts.texture.users_object_modifier;

            #----映射-保存-----------------------------------------------------------------
            if(not b是修改器材质):
                D["texture_coords"]=mts.texture_coords;
                if(mts.texture_coords in["UV","ORCO"]):
                    D["use_from_dupli"]=mts.use_from_dupli;
                    D["uv_layer"]=mts.uv_layer;

                elif(mts.texture_coords=="OBJECT"):
                    #if(mts.object==oA):
                        #D["object"]="SELF";
                    if(mts.object):
                        D["object"]=mts.object.name;
                    D["use_from_original"]=mts.use_from_original;

                if(s类型=="MaterialTextureSlot"):
                    D["mapping"]=mts.mapping;
                    D["mapping_x"]=mts.mapping_x;D["mapping_y"]=mts.mapping_y;D["mapping_z"]=mts.mapping_z;

                    D["use_map_diffuse"]=mts.use_map_diffuse;D["diffuse_factor"]=mts.diffuse_factor; D["use_map_color_diffuse"]=mts.use_map_color_diffuse;
                    D["use_map_alpha"]=mts.use_map_alpha;D["alpha_factor"]=mts.alpha_factor;D["use_map_translucency"]=mts.use_map_translucency;D["translucency_factor"]=mts.translucency_factor;
                    D["ambient_factor"]=mts.ambient_factor;D["use_map_ambient"]=mts.use_map_ambient;D["use_map_emit"]=mts.use_map_emit;D["emit_factor"]=mts.emit_factor;
                    D["mirror_factor"]=mts.mirror_factor;D["use_map_mirror"]=mts.use_map_mirror;D["use_map_raymir"]=mts.use_map_raymir;D["raymir_factor"]=mts.raymir_factor;
                    D["use_map_specular"]=mts.use_map_specular;D["specular_factor"]=mts.specular_factor;D["use_map_color_spec"]=mts.use_map_color_spec;D["specular_color_factor"]=mts.specular_color_factor;D["use_map_hardness"]=mts.use_map_hardness;D["hardness_factor"]=mts.hardness_factor;
                    D["use_map_normal"]=mts.use_map_normal;D["normal_factor"]=mts.normal_factor;D["use_map_warp"]=mts.use_map_warp;D["warp_factor"]=mts.warp_factor; D["use_map_displacement"]=mts.use_map_displacement; D["displacement_factor"]=mts.displacement_factor ;

                D["offset"]=mts.offset;D["scale"]=mts.scale;
                #----影响-----------------------------------------------------------------

                D["diffuse_color_factor"]=mts.diffuse_color_factor;
                D["blend_type"]=mts.blend_type;
                D["invert"]=mts.invert;
                D["use_rgb_to_intensity"]=mts.use_rgb_to_intensity;
                D["use_stencil"]=mts.use_stencil;
                D["color"]=mts.color;
                D["default_value"]=mts.default_value;
                D["bump_method"]=mts.bump_method;
                D["bump_objectspace"]=mts.bump_objectspace;

            #--------------------------------------------------------------------------
            Ds条目f值["BI_TEXTURE"][str(i贴图槽位置)]=D;#{"BI_TEXTURE":{"0":{},"1":{}},"3":{},...}

#//////////////////////////////////////////////////
def ΔΔTextureImage应用(Ds条目f值,mat或lamp):
    b是修改器材质=False;
    if(hasattr(mat或lamp,"texture")):#是修改器材质只有一个
        b是修改器材质=True;
        Lmts=[mat或lamp];
    else:
        Lmts=mat或lamp.texture_slots ;#MaterialTextureSlot  贴图槽

    if("BI_TEXTURE" in Ds条目f值.keys()):
        #----先清除所有贴图-----------------------------------------------------------
        for mts in Lmts:
            if(mts):
                mts.texture=None;

        #print("BI_TEXTURE==",Ds条目f值["BI_TEXTURE"]);
        for  s贴图槽位置,D in Ds条目f值["BI_TEXTURE"].items():#{"BI_TEXTURE":{"0":{},"1":{}},"3":{},...} #只选代有保存的
            print("HAVE MTS ",s贴图槽位置);
            mts=Lmts[int(s贴图槽位置)];
            if(D!=None):
                b存在这个纹理=False;
                if(not mts):
                    #print("CREATE MTS ",s贴图槽位置);
                    mts=Lmts.create(int(s贴图槽位置));
                for t2 in bpy.data.textures:
                    if (t2.name==D["TEXTURE"]["TEXTURE_NAME"]):#存在这个纹理
                        mts.texture=t2;
                        b存在这个纹理=True;break;
                #print("EXISIT TEXTURE",t2.name);
                #----新建材质-----------------------------------------------------------
                if(b存在这个纹理==False):
                    t2 = bpy.data.textures.new(D["TEXTURE"]["TEXTURE_NAME"],"IMAGE");#Texture=t2
                    mts.texture=t2;
                    #----保存材质自身属性---------------------------------------------------------
                    mts.texture["TEXTURE"]={};
                    mts.texture["TEXTURE"]["TEXTURE_NAME"]=D["TEXTURE"]["TEXTURE_NAME"];mts.texture["TEXTURE"]["TEXTURE_TYPE"]="IMAGE";

                if(not b是修改器材质):
                    mts.use=D["use"];
                mts.texture.type=D["TEXTURE"]["type"];#这个必须先应用。
                #mts.texture.name=D["TEXTURE"]["TEXTURE_NAME"];
                #Δ字典赋予物体LIB(D["TEXTURE"],mts.texture,[]);
                if(D["TEXTURE"]["use_color_ramp"]):
                    ΔΔColorRamp应用(D["COLORRAMP"][s贴图槽位置],mts.texture.color_ramp);
                #----应用材质属性----------------------------------------------------------
                Δ字典赋予物体LIB(D["TEXTURE"],mts.texture,[]);
                #----贴图-应用---------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="IMAGE"):
                    b找到贴图=False;
                    if("IMAGE_NAME" in D["IMAGEIMAGE"].keys()):
                        for image in bpy.data.images:
                            if("IMAGE" in image.keys()):
                                #print("IMAGE KEYS==",image["IMAGE"].keys());
                                if("IMAGE_NAME" in image["IMAGE"].keys()):
                                    if (image["IMAGE"]["IMAGE_NAME"]==D["IMAGEIMAGE"]["IMAGE_NAME"]):#存在这个贴图
                                        mts.texture.image=image;
                                        b找到贴图=True;mts.texture.image.update();
                                        break;
                        if(b找到贴图==False):
                            #image = bpy.data.images.new(D["IMAGEIMAGE"]["IMAGE_NAME"],10, 10, alpha=False, float_buffer=False);
                            s贴图名=os.path.basename(D["IMAGEIMAGE"]["filepath"]);
                            if(s贴图名!=""):
                                #----先找本地路径-----------------------------------------------------------
                                try:
                                    mts.texture.image=bpy.data.images.load("//"+s贴图名);#先找本地路径
                                    if(mts.texture.image!=None):
                                        mts.texture.image["IMAGE"]={};
                                        mts.texture.image["IMAGE"]["IMAGE_NAME"]=L值[i位置][0][0];n节点.texture["IMAGE"]["IMAGE_TYPE"]=L值[i位置][0][1];
                                        mts.texture.image.update();
      
                                #----有可能图片路径不存在------------------------------------------------------
                                except:
                                    try:
                                        mts.texture.image = bpy.data.images.load(D["IMAGEIMAGE"]["filepath"]);
                                        if(mts.texture.image!=None):
                                            mts.texture.image["IMAGE"]={};
                                            mts.texture.image["IMAGE"]["IMAGE_NAME"]=L值[i位置][0][0];mts.texture.texture["IMAGE"]["IMAGE_TYPE"]=L值[i位置][0][1];
                                            mts.texture.image.update();
                                    except:
                                        print("CAN'T LOAD IMAGE!!",);

                                #----当相对与绝对路径都找不到image--------------------------------------------------
                                if(mts.texture.image==None):
                                    mts.texture.image=bpy.data.images.new(name=s贴图名, width=1, height=1, alpha=False, float_buffer=False, stereo3d=False);
                                    print("NEW IMAGE",s贴图名);
                        
                        #mts.texture.image.name=D["image_namefile:///E:/blender/blender_python_reference/bpy.types.Image.html?highlight=filepath#bpy.types.Image.filepath"];
                        ΔΔ字典赋予左物体(mts.texture.image,D["IMAGEIMAGE"]);


                        #---图像采样-应用---------------------------------------------------------------
                        ΔΔ字典赋予左物体(mts.texture,D["IMAGE"]);

                #----马形分氏-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="MUSGRAVE"):
                    ΔΔ字典赋予左物体(mts.texture,D["MUSGRAVE"]);

                #----树木-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="WOOD"):
                    ΔΔ字典赋予左物体(mts.texture,D["WOOD"]);

                #----STUCCI-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="STUCCI"):
                    ΔΔ字典赋予左物体(mts.texture,D["STUCCI"]);

                #----NOISE-应用----------------------------------------------------------------
                #if(D["TEXTURE"]["type"]=="NOISE"):
                    #mts.texture.users_material=D["users_material"];
                    #mts.texture.users_object_modifier=D["users_object_modifier"];
                #----VOXEL_DATA-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="VOXEL_DATA"):
                    print("texture_type==",D["TEXTURE"]["type"]);
                    if("IMAGE_NAME" in D["VOXEL_DATA"].keys()):
                        b找到贴图=False;
                        for i2 in bpy.data.images:
                            if (i2.name==D["VOXEL_DATA"]["IMAGE_NAME"]):#存在这个贴图
                                mts.texture.image=i2;
                                b找到贴图=True;break;
                        if(b找到贴图==False):
                            i2 = bpy.data.images.new(D["VOXEL_DATA"]["IMAGE_NAME"],10, 10, alpha=False, float_buffer=False);#image=i2
                            try:
                                i2 = bpy.data.images.load(D["VOXEL_DATA"]["filepath"]);
                                mts.texture.image=i2;mts.texture.image.update();
                            except:
                                print("CAN T LOAD IMAGE!!",);

                        for s键,值  in D["VOXEL_DATA"].items():
                            try:
                                setattr(mts.texture.image,s键,值);
                            except:
                                pass;

                    if("DOMAIN_OBJECT_NAME" in D["VOXEL_DATA"].keys()):
                        if(D["VOXEL_DATA"]["DOMAIN_OBJECT_NAME"] in bpy.data.objects.keys()):
                            mts.texture.voxel_data.domain_object=bpy.data.objects[D["VOXEL_DATA"]["DOMAIN_OBJECT_NAME"]];

                        ΔΔ字典赋予左物体(mts.texture.voxel_data,D["VOXEL_DATA"]);

                        #mts.texture.users_material=D["users_material"];
                        #mts.texture.users_object_modifier=D["users_material"];
                #----MAGIC-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="MAGIC"):
                    mts.texture.noise_depth=D["MAGIC"]["noise_depth"];
                    mts.texture.turbulence=D["MAGIC"]["turbulence"];
                    #mts.texture.users_material=D["MAGIC"]["users_material"];
                    #mts.texture.users_object_modifier=D["MAGIC"]["users_object_modifier"];
                #----OCEAN-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="OCEAN"):
                    if("OCEAN_OBJECT_NAME" in D["OCEAN"].keys()):
                        mts.texture.ocean.ocean_object=bpy.data.objects[D["OCEAN"]["OCEAN_OBJECT_NAME"]];
                        mts.texture.ocean.output=D["OCEAN"]["output"];

                    #mts.texture.users_material=D["OCEAN"]["users_material"];
                    #mts.texture.users_object_modifier=D["OCEAN"]["users_object_modifier"];
                #----POINT_DENSITY-应用----------------------------------------------------------
                if(D["TEXTURE"]["type"]=="POINT_DENSITY"):
                    if("COLORRAMP" in D["POINT_DENSITY"].keys()):
                        ΔΔColorRamp应用(D["POINT_DENSITY"]["COLORRAMP"]["0"],mts.texture.point_density.color_ramp);

                        if(D["POINT_DENSITY"]["use_falloff_curve"]==True and "MAPPING" in D["POINT_DENSITY"].keys()):
                            ΔΔmapping应用(D["POINT_DENSITY"]["MAPPING"],mts.texture.point_density.falloff_curve,"0");
                        ΔΔ字典赋予左物体(mts.texture.point_density,D["POINT_DENSITY"]);


                        if(D["POINT_DENSITY"]["OBJECT_NAME"] in bpy.data.objects.keys()):
                            mts.texture.point_density.object=bpy.data.objects[D["POINT_DENSITY"]["OBJECT_NAME"]];

                        if(D["POINT_DENSITY"]["PARTICLE_SYSTEM_NAME"] in bpy.data.particles.keys()):
                            mts.texture.point_density.particle_system=bpy.data.particles[D["POINT_DENSITY"]["PARTICLE_SYSTEM_NAME"]];

                #----MARBLE-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="MARBLE"):
                    ΔΔ字典赋予左物体(mts.texture,D["MARBLE"]);

                #----CLOUDS-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="CLOUDS"):
                    ΔΔ字典赋予左物体(mts.texture,D["CLOUDS"]);

                #----VORONOI-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="VORONOI"):
                    ΔΔ字典赋予左物体(mts.texture,D["VORONOI"]);

                #----BLEND-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="BLEND"):
                    mts.texture.progression=D["BLEND"]["progression"];
                    mts.texture.use_flip_axis=D["BLEND"]["use_flip_axis"];
                    #mts.texture.users_material=D["BLEND"]["users_material"];
                    #mts.texture.users_object_modifier=D["BLEND"]["users_object_modifier"];

                #----ENVIRONMENT_MAP  应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="ENVIRONMENT_MAP"):
                    for s键,值  in D["ENVIRONMENT_MAP"].items():
                        try:
                            setattr(mts.texture.environment_map,s键,值);
                        except:
                            pass;
                        try:
                            setattr(mts.texture,s键,值);
                        except:
                            pass;
                        try:
                            setattr(mts.texture.image,s键,值);
                        except:
                            pass;


                    if(D["ENVIRONMENT_MAP"]["VIEWPOINT_OBJECT_NAME"]in bpy.data.objects.keys()):
                        mts.texture.environment_map.viewpoint_object=bpy.data.objects[D["ENVIRONMENT_MAP"]["VIEWPOINT_OBJECT_NAME"]];


                    if("IMAGE_NAME" in D["ENVIRONMENT_MAP"].keys()):
                        if(D["ENVIRONMENT_MAP"]["IMAGE_NAME"] in bpy.data.images.keys()):
                            mts.texture.image=bpy.data.images[D["IMAGE_NAME"]];


                #----DISTORTED_NOISE-应用----------------------------------------------------------------
                if(D["TEXTURE"]["type"]=="DISTORTED_NOISE"):
                    mts.texture.distortion=D["DISTORTED_NOISE"]["distortion"];
                    mts.texture.nabla=D["DISTORTED_NOISE"]["nabla"];
                    mts.texture.noise_basis=D["DISTORTED_NOISE"]["noise_basis"];
                    mts.texture.noise_distortion=D["DISTORTED_NOISE"]["noise_distortion"];
                    mts.texture.noise_scale=D["DISTORTED_NOISE"]["noise_scale"];
                    #mts.texture.users_material=D["DISTORTED_NOISE"]["users_material"];
                    #mts.texture.users_object_modifier=D["DISTORTED_NOISE"]["users_object_modifier"];

                #//////////////////////////////////////////////////
                #----映射-应用--------------------------------------------------------------
                Δ字典强制赋予物体LIB(D,mts);

                if("texture_coords" in D.keys()):
                    #mts.texture_coords=D["texture_coords"];
                    if(D["texture_coords"]=="OBJECT"):
                        if("object" in D.keys()):
                            if(D["object"]=="SELF"):
                                mts.object=oA;
                            else:
                                try:
                                    mts.object=bpy.data.objects[D["object"]];
                                except:
                                    pass;


#//////////////////////////////////////////////////
def ΔΔColorRamp保存(ramp,L):
    #L=[];#{"s贴图位置":[]}
    L.append([]);#增加后的位置    {"s贴图位置":[[],],}
    #L["DD节点"][s贴图位置]["L节点属性"][i位置].append([]);
    for i,cre in enumerate( ramp.elements):
        L[0].append([]);#{"s贴图位置":[[[],],],}
        L[0][i].append([cre.color]);   #{"s贴图位置":[[[[color],],],],}
        L[0][i].append([cre.position]); #{"s贴图位置":[[[[color],[position]],[[color],[position]],...],]}
    L.append([ramp.interpolation]);   #{"s贴图位置":[[[[color],[position]],[[color],[position]],...],[interpolation]]}

def ΔΔmapping保存(mapping,Ds条目f值):
    L=[];
    L.append([mapping.black_level]);#[black_level,clip_max_x]
    L.append([mapping.clip_max_x]);
    L.append([mapping.clip_max_y]);
    L.append([mapping.clip_min_x]);
    L.append([mapping.clip_min_y]);

    L.append([]);#第6个#[[black_level],[clip_max_x],[]  ]
    for i, c in enumerate( mapping.curves):
        #print("D==",L[5]);
        L[5].append([]);#[[black_level],[clip_max_x],[[],[]]  ]
        #L[5][i].append([c.extend]);
        for j,cmp in enumerate (c.points):
            L[5][i].append([]);#[[black_level],[clip_max_x],[[[],[]],[[],[]] ]    ]
            L[5][i][j].append([cmp.handle_type]);#[[black_level],[clip_max_x],[[[[handle_type],[location]],[[handle_type],[location]]],[[],[]] ]    ]
            L[5][i][j].append([cmp.location]);
            L[5][i][j].append([cmp.select]);
    L.append([mapping.use_clip]);
    L.append([mapping.white_level]); #第8个位置
    Ds条目f值=L;
#--------------------------------------------------------------------------
def ΔΔColorRamp应用(L,ramp):
    #{"s贴图位置":[[[[color],[position]],[[color],[position]],...],[interpolation]]}
    #----先清除元素,但保留第一个-----------------------------------------------------
    i长=len(ramp.elements);
    for i ,cre in enumerate(ramp.elements):
        if(len(ramp.elements)>1):
            ramp.elements.remove(ramp.elements[-1]);#ColorRampElement

    #--------------------------------------------------------------------------
    for i in range( len(L[0])):#[[[color],[position]],[[color],[position]],...]
        if(i>0):#第一个不新建
            cre=ramp.elements.new(L[0][i][1][零]);
        else:
            cre=ramp.elements[i];

        cre.color=L[0][i][0][零];
        cre.position=L[0][i][1][零];

    ramp.interpolation=L[1][零];

def ΔΔmapping应用(Ds条目f值,mapping):
    L=Ds条目f值;
    #for i主 in range(len(L)):
    mapping.initialize();#初始化曲边
    mapping.black_level=L[0][零];
    mapping.clip_max_x=L[1][零];
    mapping.clip_max_y=L[2][零];
    mapping.clip_min_x=L[3][零];
    mapping.clip_min_y=L[4][零];
    """"""
    for i主,c in enumerate( mapping.curves):
        for j in range(len(L[5][i主])):
            cmp=c.points.new(0,0);
            cmp.handle_type=L[5][i主][j][0][零];
            cmp.location=L[5][i主][j][1][零];
            cmp.select=L[5][i主][j][2][零];
    mapping.use_clip=L[6][零];
    mapping.white_level=L[7][零];
    mapping.update();





#//////////////////////////////////////////////////
def  ΔΔcurve保存(Ds条目f值,cm):
    Ds条目f值.append([cm.black_level]);
    Ds条目f值.append([cm.clip_max_x]);
    Ds条目f值.append([cm.clip_max_y]);
    Ds条目f值.append([cm.clip_min_x]);
    Ds条目f值.append([cm.clip_min_y]);

    Ds条目f值.append([]);#第6个
    for i, c in enumerate(cm.curves):
        Ds条目f值[5].append([]);
        #Ds条目f值[5][i].append([c.extend]);
        for j,cmp in enumerate (c.points):
            Ds条目f值[5][i].append([]);
            Ds条目f值[5][i][j].append([cmp.handle_type]);
            Ds条目f值[5][i][j].append([cmp.location]);
            Ds条目f值[5][i][j].append([cmp.select]);
    Ds条目f值.append([cm.use_clip]);
    Ds条目f值.append([cm.white_level]);
#--------------------------------------------------------------------------
def  ΔΔcurve应用(Ds条目f值,cm):
    零=0;
    L值=Ds条目f值;
    #for i主 in range(len(L值)):
    cm.black_level=L值[0][零];
    cm.clip_max_x=L值[1][零];
    cm.clip_max_y=L值[2][零];
    cm.clip_min_x=L值[3][零];
    cm.clip_min_y=L值[4][零];
    for i主,c in enumerate(cm.curves):
        for j in range(len(L值[5][i主])):
            cmp=c.points.new(0,0);
            cmp.handle_type=L值[5][i主][j][0][零];
            cmp.location=L值[5][i主][j][1][零];
            cmp.select=L值[5][i主][j][2][零];
    cm.use_clip=L值[6][零];
    cm.white_level=L值[7][零];
    cm.update();


#//////////////////////////////////////////////////

#//////////////////////////////////////////////////
def ΔΔ节点颜色():
    oA=bpy.context.object;
    matA=oA.active_material;
    DLn=matA.node_tree.nodes;
    def         赋值(DLn):
        for s主, n节点 in DLn.items():
            if(n节点.bl_idname=="ShaderNodeAddShader"):
                n节点.color=(0.0, 0.0, 1.0);#蓝色
                n节点.use_custom_color=True;
            elif(n节点.bl_idname=="ShaderNodeBrightContrast"):
                n节点.use_custom_color=True;
                n节点.color=(1.0, 1.0, 0.5);#浅黄色

            elif(n节点.bl_idname=="ShaderNodeBsdfDiffuse"):
                n节点.use_custom_color=True;
                n节点.color=(0.0, 0.0, 0.0);#黑色
            elif(n节点.bl_idname=="ShaderNodeBsdfGlossy"):
                n节点.use_custom_color=True;
                n节点.color=(1.0, 1.0, 0.0);#黄色
            elif(n节点.bl_idname=="ShaderNodeBsdfAnisotropic"):
                n节点.use_custom_color=True;
                n节点.color=(0.6, 1.0, 0.6);#色
            elif(n节点.bl_idname=="ShaderNodeBsdfTransparent"):
                n节点.use_custom_color=True;
                n节点.color=(1.0, 0.8, 1.0);#红白色
            elif(n节点.bl_idname=="ShaderNodeBsdfTranslucent"):
                n节点.use_custom_color=True;
                n节点.color=(1.0, 0.8, 0.8);#红白色

            elif(n节点.bl_idname=="ShaderNodeBsdfVelvet"):
                n节点.use_custom_color=True;
                n节点.color=(0.5, 0.5, 0.5);#灰色
            elif(n节点.bl_idname=="ShaderNodeEmission"):
                n节点.use_custom_color=True;
                n节点.color=(0.8, 1.0, 1.0);#白色
            elif(n节点.bl_idname=="ShaderNodeGamma"):
                n节点.use_custom_color=True;
                n节点.color=(1.0, 1.0, 0.5);#浅黄色

            elif(n节点.bl_idname=="ShaderNodeHueSaturation"):
                n节点.use_custom_color=True;
                n节点.color=(1.0, 0.0, 0.0);#红色
            elif(n节点.bl_idname=="ShaderNodeMath"):
                n节点.use_custom_color=True;
                n节点.color=(0.0, 1.0, 1.0);#色
            elif(n节点.bl_idname=="ShaderNodeMixRGB"):
                n节点.use_custom_color=True;
                n节点.color=(0.0, 0.5, 0.0);#深绿色
            elif(n节点.bl_idname=="ShaderNodeMixShader"):
                n节点.use_custom_color=True;
                n节点.color=(0.0, 1.0, 0.0);#绿色
            elif(n节点.bl_idname=="ShaderNodeRGBCurve"):
                n节点.use_custom_color=True;
                n节点.color=(1.0, 0.0, 0.0);#红色
            elif(n节点.bl_idname=="ShaderNodeValToRGB"):
                n节点.use_custom_color=True;
                n节点.color=(1.0, 0.0, 0.0);#红色
            elif(n节点.bl_idname=="ShaderNodeTexImage"):
                n节点.use_custom_color=True;
                n节点.color=(0.15, 0.15, 0.15);#浅黑色

            elif(n节点.bl_idname=="ShaderNodeGroup"):
                n节点.use_custom_color=True;
                n节点.color=(1.0, 0.0, 1.0);#紫色
                DLn次=n节点.node_tree.nodes;
                赋值(DLn次);
    #----------------------------------------------------------------------------
    赋值(DLn);





#----------------------------------------------------------------------------------
global bG;bG=False;
def ΔΔ载入截图(context,cp当前种类,ip激活ξ,s激活预置名,path当前种类):
    global bG;
    if (bpy.data.textures.find("物体预置截图") == -1):#在bl找不到这个材质
        bpy.data.textures.new("物体预置截图", "IMAGE");

    if (bpy.data.images.find(s激活预置名+".jpg") == -1):#在bl找不到这个截图
        file截图=os.path.join(path当前种类,s激活预置名+".jpg");
        if(os.path.exists(file截图)):
            bpy.ops.image.open(filepath=file截图);

    #r=context.region;
    #r.view2d.view_to_region(x=0.1, y=0.1, clip=True)
    #print("R==",r.height,r.width,r.type,context.area.type);
    #context.region.tag_redraw();
    #print("SP type==",context.space_data.type);
    #bpy.ops.view2d.reset()
    #bpy.ops.view2d.smoothview(gesture_mode=0, xmin=0, xmax=0, ymin=0, ymax=0)
    """"""
    if(bG==False):
        bpy.ops.view2d.zoom(deltax=3, deltay=0.0);
        bG=True;
    else:
        bpy.ops.view2d.zoom(deltax=-3, deltay=0.0);
        bG=False ;
    #bpy.ops.view2d.scroller_activate()
    #bpy.ops.view2d.zoom(deltax=-3, deltay=0.0);
    #bpy.ops.view2d.zoom_in(zoomfacx=0.1, zoomfacy=0.0)
    #bpy.ops.view2d.zoom_border(gesture_mode=0, xmin=0.1, xmax=0.5, ymin=0, ymax=0)

    ΔΔ刷新界面LIB(area="VIEW_3D",region="TOOL_PROPS");
    #context.region.tag_redraw();#这个能刷新画面
    """
    context.area.tag_redraw();
    for space in context.area.spaces:
        print("SP type==",space.type);
    """
    #bpy.data.images[s激活预置名+".jpg"].update()#(frame=0, filter=9985, mag=9729);


#//////////////////////////////////////////////////
def bΔΔ检测bl版本LIB(self,i1,i2):
    vs=bpy.app.version;
    print(vs);
    #print(vs[0],vs[1]);
    if(vs[0]>i1 or vs[1]>i2):
        print("INVAILD  VERSION");
        if(self):
            self.report({"ERROR"},"VERSION exceed the time limit  this addon limits the version before %d.%d"%(i1,i2));#"INFO" "ERROR" "DEBUG" "WARNING"
        return  False;

    return True;


#//////////////////////////////////////////////////
def ΔPTm物体LIB(o):
    m=o.matrix_world;
    for i in range(3):
        print("o.m==",LΔΔ保留4位小数(m[i][0]),LΔΔ保留4位小数(m[i][1]),LΔΔ保留4位小数(m[i][2]));

def ΔPTm3巛巛(m):
    for i in range(3):
        print("m==",LΔΔ保留4位小数(m[i][0]),LΔΔ保留4位小数(m[i][1]),LΔΔ保留4位小数(m[i][2]));

#//////////////////////////////////////////////////
def ΔPTmatrxLIB(m应):#这里打印的与界面内驱动的不一样 ，但驱动用这里的正确
    print("matrx:------------------------------",);
    print("X==",m应[0][0],m应[0][1],m应[0][2]);
    print("Y==",m应[1][0],m应[1][1],m应[1][2]);
    print("Z==",m应[2][0],m应[2][1],m应[2][2]);

def ΔΔM打印matrxLIB(m应):#这里打印的与界面内驱动的相同，但驱动不能用这里的
                                                    #这个打印与bpc->bone->bone_mat相同
    print("matrxM:------------------------------",);
    print("X==",m应[0][0],m应[1][0],m应[2][0]);
    print("Y==",m应[0][1],m应[1][1],m应[2][1]);
    print("Z==",m应[0][2],m应[1][2],m应[2][2]);


#////注册按键//////////////////////////////////////////
#Ls类别界面=["3D View","Object Mode","Mesh","Curve","Armature","Pose","Vertex Paint","Weight Paint","Object Non-modal","Sculpt","Timeline","Outliner"];
def kmiΔ新建LIB(km,idname="",type="", value="",any=False,shift=False,ctrl=False,alt=False,oskey=False,head=False):
    """
    kmi = km.keymap_items.get(idname, None);#看看有没有这个键存在
    if(kmi):
        if (kmi.type==type and kmi.any==any  and kmi.shift ==shift  and kmi.ctrl ==ctrl and kmi.alt==alt ):
            #kmi.idname = idname;
            if(kmi.active==False):
                kmi.active=True;
            #print("BP",kmi.properties,kmi.name);
            #print("FIND KMI",kmi.idname);
            return kmi;

    else:
        print("NEW KEY",);
        kmi=km.keymap_items.new(idname=idname, type=type, value=value,any=any ,shift=shift ,ctrl=ctrl,alt=alt,oskey=oskey,head=head );#没有 就新建
        if(kmi.active==False ):kmi.active=True ;
    """

    kmi=km.keymap_items.new(idname=idname, type=type, value=value,any=any ,shift=shift ,ctrl=ctrl,alt=alt,oskey=oskey,head=head );#没有 就新建
    return kmi;

#——————————————————————————————————————————————————————
def ΔΔ不勾选按键LIB(LLsKC类别,LDs类别id与按键,b注册还是反注册):
    Lkc=[None,None,None];
    Lkc[0]= bpy.context.window_manager.keyconfigs.addon;
    Lkc[1]= bpy.context.window_manager.keyconfigs.user;
    Lkc[2]= bpy.context.window_manager.keyconfigs.default;
    for kc in Lkc:
        if(kc):
            for LsKC in LLsKC类别:
                if(LsKC[0] in kc.keymaps.keys()):#"3D View" "Object Mode"
                    km = kc.keymaps[LsKC[0]];
                    Ckmi全部=km.keymap_items;#全部键位
                    Lkeys=Ckmi全部.keys();
                    #print("Lkeys==",Lkeys);
                    for kmi全部 in Ckmi全部:
                        #--------------------------------------------------------------------------
                        for i项 in LsKC[3]:#[0,1,2,3,4,5,6,7,8,9,10,11,12]
                            Ds类别id与按键 = LDs类别id与按键[i项];
                            #if(kmi全部.idname=="object.duplicate_move_linked" and  Ds类别id与按键["idname"] in Lkeys):print("LINKED==",kmi全部.idname);

                            if(Ds类别id与按键["idname"] in Lkeys):
                                kmi=Ckmi全部[Ds类别id与按键["idname"]];
                                #if(kmi.idname=="bp.duplica_root"):print("KMI==",kmi.idname);
                                #if(kmi全部.idname=="object.duplicate_move_linked"):print("LINKED 2==",kmi全部.idname);
                                if(Ds类别id与按键["idname"]!=kmi全部.idname ):
                                    if (kmi全部.type ==Ds类别id与按键["type"] and kmi全部.any==Ds类别id与按键["any"]and kmi全部.shift==Ds类别id与按键["shift"]   and kmi全部.ctrl==Ds类别id与按键["ctrl"]  and kmi全部.alt== Ds类别id与按键["alt"] ):
                                        print("FIND",kmi全部.idname,Ds类别id与按键["type"] ,Ds类别id与按键["any"] ,Ds类别id与按键["shift"]  ,Ds类别id与按键["ctrl"] ,Ds类别id与按键["alt"] );
                                    #print("kmi.idname==",kmi.idname,kmi.type ,kmi.any, kmi.shift, kmi.ctrl,kmi.alt );
                                if (    kmi全部.idname != Ds类别id与按键["idname"] and (kmi全部.type ==Ds类别id与按键["type"] and kmi全部.any==Ds类别id与按键["any"]and kmi全部.shift==Ds类别id与按键["shift"]   and kmi全部.ctrl==Ds类别id与按键["ctrl"]  and kmi全部.alt== Ds类别id与按键["alt"])   ):
                                    print("kmi.idname==",kmi.idname,kmi.type ,kmi.any, kmi.shift, kmi.ctrl,kmi.alt );
                                    if(kmi全部.active==True and b注册还是反注册==True):
                                        kmi全部.active=False;print("False______",kmi全部.idname);
                                    elif(kmi全部.active==False and b注册还是反注册==False):
                                        kmi全部.active=True;print("True______",kmi全部.idname);
                            """
                            for  kmi全部 in  km.keymap_items:
                                for Ds类别id与按键 in LDs类别id与按键:
                                    if (kmi全部.idname != Ds类别id与按键["idname"] and (kmi全部.type ==Ds类别id与按键["type"] and kmi全部.any==Ds类别id与按键["any"]and kmi全部.shift==Ds类别id与按键["shift"]   and kmi全部.ctrl==Ds类别id与按键["ctrl"]  and kmi全部.alt== Ds类别id与按键["alt"] )):
                                        if(kmi全部.active==True and b注册还是反注册==True):
                                            kmi全部.active=False;#print("False",);
                                        elif(kmi全部.active==False and b注册还是反注册==False):
                                            kmi全部.active=True;#print("True",);
                                        #print("FIND SAME KEY",);
                            """

#——————————————————————————————————————————————————————
def ΔΔ注册按键LIB(LLsKC类别,LDs类别id与按键):
    Lkc=[None,None,None];
    Lkc[0]= bpy.context.window_manager.keyconfigs.addon;
    #Lkc[1]= bpy.context.window_manager.keyconfigs.user;
    #Lkc[2]= bpy.context.window_manager.keyconfigs.default;
    for kc in Lkc:
        if(kc):
            for LsKC in LLsKC类别:
                #print("LSKC==",LsKC);
                if(LsKC[0] in kc.keymaps.keys()):
                    km=kc.keymaps[LsKC[0]];
                else:
                    #km=kc.keymaps.find(name="3D View", space_type="VIEW_3D", region_type="WINDOW");
                    km = kc.keymaps.new(name=LsKC[0],space_type=LsKC[1], region_type=LsKC[2], modal=False);
                #--------------------------------------------------------------------------
                for i项 in LsKC[3]:#[0,1,2,3,4,5,6,7,8,9,10,11,12]
                    Ds类别id与按键 = LDs类别id与按键[i项];
                    kmi=kmiΔ新建LIB(km,idname=Ds类别id与按键["idname"],type=Ds类别id与按键["type"], value=Ds类别id与按键["value"],any=Ds类别id与按键["any"],
                                                shift=Ds类别id与按键["shift"],ctrl=Ds类别id与按键["ctrl"],alt=Ds类别id与按键["alt"],head=Ds类别id与按键["head"]);
                    print("NEW KMI",kmi,LsKC[0]);
                    if("properties" in Ds类别id与按键.keys()):#有属性
                        for 键,值 in Ds类别id与按键["properties"].items():
                            #print("PROPERTIES",kmi.idname,键,值);
                            #try:
                            setattr(kmi.properties,键,值);
                                #kmi.properties.name = "MY_Q_menu";#这个键绑定的类名
                            #except:pass;
    #--------------------------------------------------------------------------
    ΔΔ不勾选按键LIB(LLsKC类别,LDs类别id与按键,True);

#——————————————————————————————————————————————————————
def ΔΔ注销按键LIB(LLsKC类别,LDs类别id与按键):
    Lkc=[None,None,None];
    Lkc[0]= bpy.context.window_manager.keyconfigs.addon;
    #Lkc[1]= bpy.context.window_manager.keyconfigs.user;
    #Lkc[2]= bpy.context.window_manager.keyconfigs.default;
    #print("reg--------",);
    for kc in Lkc:
        if(kc):
            #print("KEY",kc.keymaps);
            for LsKC in LLsKC类别:#LsKC==("3D View","VIEW_3D","WINDOW",[0,1,2,3,4,5,6,7,8,9,10,11,12])
                if(LsKC[0] in kc.keymaps.keys()):
                    km = kc.keymaps[LsKC[0]];#"3D View"
                    #print("FIND KM",km);
                    Ckmi全部=km.keymap_items;
                    #print("Ckmi全部==",Ckmi全部[0]);
                    for i项 in LsKC[3]:#[0,1,2,3,4,5,6,7,8,9,10,11,12] #有的==[]
                        Ds类别id与按键 = LDs类别id与按键[i项];#{"idname":"wm.call_menu","type":"Q","value":"PRESS",  "any":False,  "shift":False,"ctrl":False, "alt":False, "oskey":False,"head":False,"properties":{"name":"MY_Q_menu"}}
                        #if(Ds类别id与按键["idname"] in Ckmi全部):
                        if(Ds类别id与按键["idname"] in Ckmi全部.keys()):
                            kmi=Ckmi全部[Ds类别id与按键["idname"]];
                            #print("KMI==",kmi.idname);
                        else:continue;
                        #kmi=getattr(OBJ,sKey,sErrorPrint);
                        #try:
                        #if (kmi.idname ==Ds类别id与按键["idname"]):
                        if("name" in Ds类别id与按键["properties"].keys()):
                            if (kmi.properties.name ==Ds类别id与按键["properties"]["name"]):
                                #print("REMOVE KMI",kmi.idname );
                                km.keymap_items.remove(kmi);#break;#如果删除了kmi 就跳出

                        #----检查键位是否吻合-------------------------------------------------------
                        else:
                            if(Ds类别id与按键["type"]==kmi.type and Ds类别id与按键["value"]==kmi.value and Ds类别id与按键["any"]==kmi.any and \
                                Ds类别id与按键["shift"]==kmi.shift and Ds类别id与按键["ctrl"]==kmi.ctrl and Ds类别id与按键["alt"]==kmi.alt and Ds类别id与按键["oskey"]==kmi.oskey):
                                #print("REMOVE KMI",kmi.idname );
                                km.keymap_items.remove(kmi);#break;

                            """
                            try:
                                kc.keymaps.remove(km);
                            except:pass;
                            """
    #--------------------------------------------------------------------------
    ΔΔ不勾选按键LIB(LLsKC类别,LDs类别id与按键,False);



#///end////end////end////end////end////end////end////end////end////



