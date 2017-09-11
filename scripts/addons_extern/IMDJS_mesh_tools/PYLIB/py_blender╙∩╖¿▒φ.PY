blender 2.7.3
20150917
blue----
/C11'Flag keyword' STYLE_KEYWORD Colors = 16711935 Colors Back = 0 Colors Auto Back = 1 Font Style = 0
!


----条件判断--------------------------------------------------------------
True
False
Null
None

del
if():
elif():
else:
try:
except:
exec finally from global import lambda object
pass;
print();
raise

with yield and as in is not or
__except __far __fastcall __finally __fortran __huge __inline __int16 __saveregs __segment __segname __self __asm __based __cdecl __declspec __int32 __int64 __int8 __interrupt __leave __loadds __near __pascal __stdcall __try __uuidof


__multiple_inheritance
__single_inheritance
__virtual_inheritance

catch explicit export  mutable  operator   Ellipsis  NotImplemented
__import__
abs();
@classmethod
@staticmethod

literal_eval();
execfile();

format
frozenset
reload();
repr
reversed();
round  slice sorted   super

xrange();
arange
zip

----Attributes-----------------------------------------------------------
__doc__ __email__ __members__ __methods__ __name__ __slots__ __asm __author__ __bases__ __class__ __dict__
----Exceptions---------------------------------------------------------------
ArithmeticError AssertionError AttributeError BaseException DeprecationWarning EOFError EnvironmentError Exception FloatingPointError FutureWarning GeneratorExit IOError ImportError ImportWarning IndentationError IndexError KeyError KeyboardInterrupt LookupError MemoryError NameError NotImplementedError OSError OverflowError OverflowWarning PendingDeprecationWarning ReferenceError RuntimeError RuntimeWarning StandardError StopIteration SyntaxError SyntaxWarning SystemError SystemExit TabError TypeError UnboundLocalError UnicodeDecodeError UnicodeEncodeError UnicodeError UnicodeTranslateError UnicodeWarning UserWarning ValueError Warning WindowsError ZeroDivisionError

--python 内置模块-----------------------------------------------------
array audiodev cmp cmpcache cookie ctypes wintypes deque dircmp dospath gl glob grep imp macpath macurl2path math nt ntpath nturl2path os packmail posixpath pre random re reconvert regex regex_syntax regsub rotor shutil soundex sre statcache strop sunaudio sys timing tzparse ucnhash util webbrowser whatsound whrandom xmllib zipfile time traceback threading multiprocessing signal importlib subprocess logging numpy
#Queue
itertools chain islice accumulate 
struct 

(C);imdjs


<RedLine>-------------------------------------------
def  
--python module----
argv(x); exc_info(x); exit(x); hexversion(x); version(x); maxint(x); maxunicode(x); modules(x); platform(x); stdout(x); stdin(x); stderr(x); exc_clear(x); exec_prefix(x); byteorder(x); copyright(x); api_version(x); version_info(x); displayhook(x); getdefaultencoding(x); getfilesystemencoding(x); setdefaultencoding(x); builtin_module_names(x); executable(x); getwindowsversion(x); stdin(x); readline(x);

map tuple list delattr getattr hasattr setattr len locals globals set range  compile dict dir enumerate eval execfile  delattr  from_iterable sum 

--math 或 cmath---
ceil(x); # 对x向上取整 比如x=1.2 返回2
floor(x); # 对x向下取整 比如x=1.2 返回1
pow(x,y); # 指数运算 得到x的y次方
log(x); # 对数 默认基底为e。可以使用base参数 来改变对数的基地。比如log
sqrt(x); # 平方根
sin(x);
cos(x);
tan(x);
asin(x);
acos(x); #返回角cos值的弧度
atan(x);
degrees(x); #x是弧度，返回角度
radians(x); #x是角度，返回弧度
sinh(x);
cosh(x);
tanh(x);
asinh(x);
acosh(x);
atanh(x);
erf(x);
gamma(x);
pi
search();
atan2();
exp();
fabs();
fmod();
hypot();
log10();

----os--------
listdir(path);#列出目录下的文件
fsencode(filepath);
getcwd();#获取当前工作目录
chdir(newdir);#改变工作目录
makedirs(r"c:\python\test");#创建多级目录
mkdir("test");#创建单个目录
removedirs(r"c:\python"); #删除所给路径最后一个目录下所有空目录。
rmdir("test");#删除单个目录
stat(file);#获取文件属性
chmod(file);#修改文件权限与时间戳
system("dir");#执行操作系统命令
exec(), execvp();#启动新进程
spawnv();#在后台执行程序
exit(), _exit();#终止当前进程


--os.path------------
getatime(); getctime(); getmtime(); path(); dirname(); join(seq); split([sep,[maxsplit]]); splitdrive(); exists(); splitdrive(); splitext(); getsize(); basename(); commonprefix(); isabs isfile isdir(); normcase(); normpath(); getsize(); islink ismount samefile(); 


------------
to_dict();
sep();

==内置方法===========
Decimal __abs__ __add__ __and__ __call__ __cmp__ __coerce__ __contains__ __del__ __delattr__ __delitem巜 __delslice__ __div巜 __divmod__ __eq__ __float__ __floordiv巜 __ge__ __getattribute__ __getitem巜 __getnewargs__ __getslice__ __gt__ __hash__ __hex__ __iadd__ __iand__ __idiv巜 __ilshift__ __imod__ __imul__ __index__ __init__ __int__ __invert__ __ior__ __ipow__ __irshift__ __isub__ __iter__ __ixor__ __le__ __len__ __long__ __lshift__ __lt__ __mod__ __mul__ __ne__ __neg__ __nonzero__ __oct__ __or__ __pos__ __pow__ __radd__ __rand__ __rdiv巜 __rdivmod__ __reduce__ __reduce_ex__ __repr__ __reserved__ __rfloordiv巜 __rlshift__ __rmod__ __rmul__ __ror__ __rpow__ __rrshift__ __rshift__ __rsub__ __rtruediv巜 __rxor__ __setattr__ __setitem巜 __setslice__ __str__ __sub__ __xor__


add(); append(); capitalize(); center(); clear(); close(); conjugate(); copy(); count(substr,[start,[end]]); decode(); difference(); discard(); encode(); endswith(); expandtabs([tabsize]); extend(); fileno(); find(substr,[start,[end]]); flush(); fromkeys(); get(); getcontext(); has_key(); index(substr,[start,[end]]); insert(); intersection(); intersection_update();  isalnum isalpha isatty isdigit islower isspace issubset issuperset istitle isupper  items() iteritems(); itervalues(); sample(); shuffle(); choice(); randrange randint uniform();


--random
keys()
ljust();
lower();
lstrip([chars]);#s
--next
pop();
popitem();
read();
readline();
readlines();
remove();
replace(oldstr,newstr,[count]);#s
reverse();
rfind(substr,[start,[end]]);#s
rindex(substr,[start,[end]]);#s
rjust();
rsplit([sep,[maxsplit]]));
rstrip([chars]);#s
seek();
setdefault('',);
sort();
splitlines([keepends]);
startswith();
strip([chars]);#s
swapcase();
symmetric_difference();
symmetric_difference_update();
tell();
title();
translate(table[,deletechars]);
truncate();
union();
update();
upper();
write();
writelines();
zfill();

LoadLibrary();


--ctypes--------------------------------------------------------------
ARRAY ArgumentError Array BigEndianStructure CDLL(); CFUNCTYPE DEFAULT_MODE DllCanUnloadNow DllGetClassObject FormatError GetLastError HRESULT LibraryLoader LittleEndianStructure OleDLL POINTER PYFUNCTYPE PyDLL RTLD_GLOBAL RTLD_LOCAL SetPointerType Structure Union union WINFUNCTYPE WinDLL(); WinError _CFuncPtr _FUNCFLAG_CDECL _FUNCFLAG_PYTHONAPI _FUNCFLAG_STDCALL _FUNCFLAG_USE_ERRNO _FUNCFLAG_USE_LASTERROR _Pointer _SimpleCData __builtins__ __cached__ __doc__ __file__ __initializing__ __loader__ __name__ __package__ __path__ __version__ _c_functype_cache _calcsize _cast _cast_addr _check_HRESULT _check_size _ctypes_version _dlopen _endian _memmove_addr _memset_addr _os _pointer_type_cache _reset_cache _string_at _string_at_addr _sys _win_functype_cache _wstring_at _wstring_at_addr addressof alignment byref  argtypes restype contents from_param 

c_bool c_buffer  c_byte  c_char  c_char_p  c_double  c_float  c_int  c_int16  c_int32  c_int64  c_int8   c_long   c_longdouble   c_longlong  c_short  c_size_t  c_ssize_t  c_ubyte  c_uint  c_uint16  c_uint32  c_uint64  c_uint8   c_ulong  c_ulonglong  c_ushort  c_void_p  c_voidp  c_wchar  c_wchar_p  
------------
cast cdll create_string_buffer create_unicode_buffer get_errno get_last_error memmove memset oledll pointer py_object pydll pythonapi resize set_errno set_last_error sizeof string_at wstring_at

windll.kernel32.FreeLibrary.(._handle);
walk();
---array---------
array('f',[0.0]*(len(me.loops)*3));

----time--------
ctime
sleep
----threading--------
setDaemon start Thread run getName setName isDaemon isAlive RLock acquire release wait notify Condition


----multiprocessing-----------
Process () Pool () Lock () JoinableQueue () Queue () log_to_stderr () get_logger () current_process () cpu_count () Pipe ()


----Queue-----------
Queue ()
----numpy-----------
ndim shape  size dtype itemsize data   reshape  ndarray  all, alltrue, any, apply along axis, argmax, argmin, argsort, average, bincount, ceil, clip, conj, conjugate, corrcoef, cov, cross, cumprod, cumsum, diff, dot, floor, inner, inv, lexsort, max, maximum, mean, median, min, minimum, nonzero, outer, prod, re, round, sometrue, sort, std, sum, trace, transpose, var, vdot, vectorize, where 
----其它函数---------------------------------------------------------------------
import_module

--bepuik成员---------------
ikbone_addr interpolation_control_addr tweak_control_addr ikjoint_addr auto_ballsocket_addr auto_stiff_child_joint_addr full_pin soft_pin  scene_addr iksolver_addr bepuik_softness bepuik_error_correction bepuik_enabled bepuik_absolute_control bepuik_use_auto_ballsocket   print
--pybepu Function----
pybepu_ikbone_new pybepu_ikbone_new_from_pchan pybepu_ikbone_new_from_bone pybepu_ikbone_set_pin pybepu_ikbone_is_pinned pybepu_ikballsocketjoint_new pybepu_dragcontrol_set_goal pybepu_dragcontrol_translate_goal pybepu_dragcontrol_set_offset pybepu_dragcontrol_new pybepu_ikbone_get_world_head_float16 pybepu_ikbone_get_world_tail_float16 pybepu_statecontrol_set_goal pybepu_statecontrol_rotate_goal pybepu_statecontrol_set_goal_pchan pybepu_statecontrol_new_from_pchan pybepu_statecontrol_new_from_bone pybepu_statecontrol_new pybepu_statecontrol_set_softness_linear_angular pybepu_statecontrol_set_errorcorrection pybepu_statecontrol_set_goal_loc pybepu_statecontrol_translate_goal_loc pybepu_statecontrol_get_goal_float16 pybepu_ikjoint_get_enabled pybepu_ikjoint_set_enabled pybepu_iksolver_new pybepu_ikangularjoint_new pybepu_ikdistancejoint_new pybepu_ikrevolutejoint_new pybepu_ikdistancelimit_new pybepu_iklinearaxislimit_new pybepu_ikpointonlinejoint_new pybepu_ikpointonplanejoint_new pybepu_ikswinglimit_new pybepu_ikswivelhingejoint_new pybepu_iktwistjoint_new pybepu_iktwistlimit_new pybepu_iktwistjoint_set_measurement_axes pybepu_iktwistlimit_set_measurement_axes pybepu_ikbone_free pybepu_control_free pybepu_ikconstraint_free pybepu_iksolver_free pybepu_ikconstraint_set_softness_error_correction pybepu_pchan_get_bone_head pybepu_bone_get_axis pybepu_bone_get_headtotail_loc pybepu_pose_match_ikbones pybepu_pose_mats_match_ikbones pybepu_ikbones_match_pose pybepu_interpolation_controls_match_pose pybepu_pchan_safe_set_enabled_autostiffchildjoint pybepu_pose_enable_autostiffchildjoints pybepu_pose_disable_autostiffchildjoints pybepu_pose_update_autostiffchildjoints_goalrelative pybepu_ob_solve_frame_change pybepu_ob_solve_tweak pybepu_all_selected_bones_on_visible_layers_are_bepuik_type_bone pybepu_bepuikmanager_reinit pybepu_pose_has_pchan   pybepu_temp_pchans_clear pybepu_temp_pchans_set pybepu_temp_pchans_reinit pybepu_pose_match_temp_pchans pybepu_check_bone bepu_pose_collect_constraint_strings bepu_pchan_collect_constraint_strings pybepu_is_refresh_needed pybepu_temp_ebones_clear pybepu_tweakop_update_stiffness
/C7' Flag' STYLE_KEYWORD Colors = 16711935 Colors Back = 0 Colors Auto Back = 1 Font Style = 0
--GL
GL_BLEND  GL_LINES
/C8'data type——yellow' STYLE_KEYWORD Colors = 65535 Colors Back = 0 Colors Auto Back = 1 Font Style = 0
\
[
]
.



/C12'bl modules  GreenBack' STYLE_KEYWORD Colors = 65280 Colors Back = 4210752 Colors Auto Back = 0 Font Style = 0
bpy
addon  print
----stand alone module-------------
bge mathutils geometry Vector  Matrix  Color  Euler  Quaternion noise bpy_extras anim_utils image_utils io_utils keyconfig_utils mesh_utils object_utils view3d_utils bgl blf gpu aud bmesh
/C13'Class  green' STYLE_KEYWORD Colors = 65280 Colors Back = 0 Colors Auto Back = 1 Font Style = 0
&

>
^
~
;
--bmesh Action ActionActuator ActionConstraint ActionFCurves ActionGroup ActionGroups ActionPoseMarkers Actuator ActuatorSensor AddSequence Addon AddonPreferences Addons AdjustmentSequence AlphaOverSequence AlphaUnderSequence AlwaysSensor AndController AnimData AnimDataDrivers AnimViz AnimVizMotionPaths AnimVizOnionSkinning AnyType Area AreaLamp AreaSpaces Armature ArmatureActuator ArmatureBones ArmatureEditBones ArmatureModifier ArmatureSensor ArrayModifier Available BMDeformVert BMEdge BMEdgeSeq BMEditSelIter BMEditSelSeq BMElemSeq BMFace BMFaceSeq BMLayerAccessEdge BMLayerAccessFace BMLayerAccessLoop BMLayerAccessVert BMLayerCollection BMLayerItem BMLoop BMLoopSeq BMLoopUV BMVert BMVertSeq BackgroundImage BackgroundImages BevelModifier BezierSplinePoint BlendData BlendDataActions BlendDataArmatures BlendDataBrushes BlendDataCameras BlendDataCurves BlendDataFonts BlendDataGreasePencils BlendDataGroups BlendDataImages BlendDataLamps BlendDataLattices BlendDataLibraries BlendDataMasks BlendDataMaterials BlendDataMeshes BlendDataMetaBalls BlendDataMovieClips BlendDataNodeTrees BlendDataObjects BlendDataParticles BlendDataScenes BlendDataScreens BlendDataSounds BlendDataSpeakers BlendDataTexts BlendDataTextures BlendDataWindowManagers BlendDataWorlds BlendTexture BlenderRNA BoidRule BoidRuleAverageSpeed BoidRuleAvoid BoidRuleAvoidCollision BoidRuleFight BoidRuleFollowLeader BoidRuleGoal BoidSettings BoidState Bone BoneGroup BoneGroups BoolProperty BoolVectorProperty BooleanModifier BrightContrastModifier Brush BrushTextureSlot BuildModifier CLIP_UL_tracking_objects Camera CameraActuator CameraSolverConstraint CastModifier ChannelDriverVariables ChildOfConstraint ChildParticle ClampToConstraint ClothCollisionSettings ClothModifier ClothSettings CloudsTexture CollectionProperty CollisionModifier CollisionSensor CollisionSettings ColorBalanceModifier ColorManagedDisplaySettings ColorManagedInputColorspaceSettings ColorManagedSequencerColorspaceSettings ColorManagedViewSettings ColorMapping ColorRamp ColorRampElement ColorRampElements ColorSequence CompositorNode CompositorNodeAlphaOver CompositorNodeBilateralblur CompositorNodeBlur CompositorNodeBokehBlur CompositorNodeBokehImage CompositorNodeBoxMask CompositorNodeBrightContrast CompositorNodeChannelMatte CompositorNodeChromaMatte CompositorNodeColorBalance CompositorNodeColorCorrection CompositorNodeColorMatte CompositorNodeColorSpill CompositorNodeCombHSVA CompositorNodeCombRGBA CompositorNodeCombYCCA CompositorNodeCombYUVA CompositorNodeComposite CompositorNodeCrop CompositorNodeCurveRGB CompositorNodeCurveVec CompositorNodeDBlur CompositorNodeDefocus CompositorNodeDespeckle CompositorNodeDiffMatte CompositorNodeDilateErode CompositorNodeDisplace CompositorNodeDistanceMatte CompositorNodeDoubleEdgeMask CompositorNodeEllipseMask CompositorNodeFilter CompositorNodeFlip CompositorNodeGamma CompositorNodeGlare CompositorNodeHueCorrect CompositorNodeHueSat CompositorNodeIDMask CompositorNodeImage CompositorNodeInpaint CompositorNodeInvert CompositorNodeKeying CompositorNodeKeyingScreen CompositorNodeLensdist CompositorNodeLevels CompositorNodeLumaMatte CompositorNodeMapRange CompositorNodeMapUV CompositorNodeMapValue CompositorNodeMask CompositorNodeMath CompositorNodeMixRGB CompositorNodeMovieClip CompositorNodeMovieDistortion CompositorNodeNormal CompositorNodeNormalize CompositorNodeOutputFile CompositorNodePixelate CompositorNodePremulKey CompositorNodeRGB CompositorNodeRGBToBW CompositorNodeRLayers CompositorNodeRotate CompositorNodeScale CompositorNodeSepHSVA CompositorNodeSepRGBA CompositorNodeSepYCCA CompositorNodeSepYUVA CompositorNodeSetAlpha CompositorNodeSplitViewer CompositorNodeStabilize CompositorNodeSwitch CompositorNodeTexture CompositorNodeTime CompositorNodeTonemap CompositorNodeTrackPos CompositorNodeTransform CompositorNodeTranslate CompositorNodeTree CompositorNodeValToRGB CompositorNodeValue CompositorNodeVecBlur CompositorNodeViewer CompositorNodeZcombine CompositorNodes ConsoleLine Constraint ConstraintActuator ConstraintTarget Context ControlFluidSettings Controller CopyLocationConstraint CopyRotationConstraint CopyScaleConstraint CopyTransformsConstraint CrossSequence Curve CurveMap CurveMapPoint CurveMapPoints CurveMapping CurveModifier CurveSplines CurvesModifier DampedTrackConstraint DecimateModifier DelaySensor DisplaceModifier DistortedNoiseTexture DomainFluidSettings DopeSheet Driver DriverTarget DriverVariable DupliObject DynamicPaintBrushSettings DynamicPaintCanvasSettings DynamicPaintModifier DynamicPaintSurface DynamicPaintSurfaces EdgeSplitModifier EditBone EditObjectActuator EffectSequence EffectorWeights EnumProperty EnumPropertyItem EnvironmentMap EnvironmentMapTexture Event ExplodeModifier ExpressionController FCurve FCurveKeyframePoints FCurveModifiers FCurveSample FFmpegSettings FModifier FModifierCycles FModifierEnvelope FModifierEnvelopeControlPoint FModifierEnvelopeControlPoints FModifierFunctionGenerator FModifierGenerator FModifierLimits FModifierNoise FModifierPython FModifierStepped FieldSettings FileSelectParams Filter2DActuator FloatProperties FloatProperty FloatVectorProperty FloorConstraint FluidFluidSettings FluidMeshVertex FluidSettings FluidSimulationModifier FollowPathConstraint FollowTrackConstraint Function GPencilFrame GPencilFrames GPencilLayer GPencilStroke GPencilStrokePoint GPencilStrokePoints GPencilStrokes GameActuator GameBooleanProperty GameFloatProperty GameIntProperty GameObjectSettings GameProperty GameSoftBodySettings GameStringProperty GameTimerProperty GammaCrossSequence GlowSequence GreasePencil GreasePencilLayers Group GroupInputs GroupObjects GroupOutputs Header HemiLamp Histogram HookModifier HueCorrectModifier ID IDMaterials IKParam IMAGE_UV_sculpt IMAGE_UV_sculpt_curve Image ImageFormatSettings ImagePaint ImageSequence ImageTexture ImageUser InflowFluidSettings IntProperties IntProperty IntVectorProperty Itasc JoystickSensor Key KeyConfig KeyConfigurations KeyMap KeyMapItem KeyMapItems KeyMaps KeyboardSensor Keyframe KeyingSet KeyingSetInfo KeyingSetPath KeyingSetPaths KeyingSets KeyingSetsAll KinematicConstraint Lamp LampSkySettings LampTextureSlot LampTextureSlots LaplacianSmoothModifier Lattice LatticeModifier LatticePoint Library LimitDistanceConstraint LimitLocationConstraint LimitRotationConstraint LimitScaleConstraint LocRotScale Location LockedTrackConstraint LoopColors MASK_UL_layers MATERIAL_UL_matslots MESH_UL_shape_keys MESH_UL_uvmaps_vcols MESH_UL_vgroups Macro MagicTexture MaintainVolumeConstraint MarbleTexture Mask MaskLayer MaskLayers MaskModifier MaskParent MaskSequence MaskSpline MaskSplinePoint MaskSplinePointUW MaskSplines Material MaterialGameSettings MaterialHalo MaterialPhysics MaterialRaytraceMirror MaterialRaytraceTransparency MaterialSlot MaterialStrand MaterialSubsurfaceScattering MaterialTextureSlot MaterialTextureSlots MaterialVolume Menu Mesh MeshCacheModifier MeshColor MeshColorLayer MeshDeformModifier MeshEdge MeshEdges MeshFloatProperty MeshFloatPropertyLayer MeshIntProperty MeshIntPropertyLayer MeshLoop MeshLoopColor MeshLoopColorLayer MeshLoops MeshPolygon MeshPolygons MeshSkinVertex MeshSkinVertexLayer MeshSticky MeshStringProperty MeshStringPropertyLayer MeshTessFace MeshTessFaces MeshTextureFace MeshTextureFaceLayer MeshTexturePoly MeshTexturePolyLayer MeshUVLoop MeshUVLoopLayer MeshVertex MeshVertices MessageActuator MessageSensor MetaBall MetaBallElements MetaElement MetaSequence MirrorModifier Modifier MotionPath MotionPathVert MouseSensor MovieClip MovieClipProxy MovieClipScopes MovieClipSequence MovieClipUser MovieReconstructedCamera MovieSequence MovieTracking MovieTrackingCamera MovieTrackingDopesheet MovieTrackingMarker MovieTrackingMarkers MovieTrackingObject MovieTrackingObjectTracks MovieTrackingObjects MovieTrackingReconstruction MovieTrackingSettings MovieTrackingStabilization MovieTrackingTrack MovieTrackingTracks MulticamSequence MultiplySequence MultiresModifier MusgraveTexture NandController NearSensor NlaStrip NlaStrips NlaTrack NlaTracks Node NodeForLoop NodeFrame NodeGroup NodeLink NodeLinks NodeOutputFileSlotFile NodeOutputFileSlotLayer NodeReroute NodeSocket NodeSocketBoolean NodeSocketFloatAngle NodeSocketFloatDistance NodeSocketFloatFactor NodeSocketFloatNone NodeSocketFloatPercentage NodeSocketFloatTime NodeSocketFloatUnsigned NodeSocketIntNone NodeSocketIntUnsigned NodeSocketRGBA NodeSocketShader NodeSocketStringFilepath NodeSocketStringNone NodeSocketVectorAcceleration NodeSocketVectorDirection NodeSocketVectorEuler NodeSocketVectorNone NodeSocketVectorTranslation NodeSocketVectorVelocity NodeSocketVectorXYZ NodeTree NodeWhileLoop NoiseTexture NorController Object ObjectActuator ObjectBase ObjectConstraints ObjectModifiers ObjectSolverConstraint ObstacleFluidSettings OceanModifier OceanTexData OceanTexture Operator OperatorFileListElement OperatorMacro OperatorMousePath OperatorProperties OperatorStrokeElement OrController OutflowFluidSettings OverDropSequence PHYSICS_UL_dynapaint_surfaces PackedFile Paint Panel ParentActuator Particle ParticleBrush ParticleDupliWeight ParticleEdit ParticleFluidSettings ParticleHairKey ParticleInstanceModifier ParticleKey ParticleSettings ParticleSettingsTextureSlot ParticleSettingsTextureSlots ParticleSystem ParticleSystemModifier ParticleSystems ParticleTarget PivotConstraint PointCache PointCaches PointDensity PointDensityTexture PointLamp PointerProperty Pose PoseBone PoseBoneConstraints Property PropertyActuator PropertyGroup PropertyGroupItem PropertySensor PythonConstraint PythonController Quaternion RENDER_UL_renderlayers RadarSensor RandomActuator RandomSensor RaySensor Region RegionView3D RemeshModifier RenderEngine RenderLayer RenderLayers RenderPass RenderResult RenderSettings RigidBodyConstraint RigidBodyJointConstraint RigidBodyObject RigidBodyWorld Rotation SCENE_UL_keying_set_paths SPHFluidSettings Scaling Scene SceneActuator SceneBases SceneGameData SceneGameRecastData SceneObjects SceneRenderLayer SceneSequence Scopes Screen ScrewModifier Sculpt SculptCapabilities SelectedUvElement Sensor Sequence SequenceColorBalance SequenceColorBalanceData SequenceCrop SequenceEditor SequenceElement SequenceElements SequenceModifier SequenceModifiers SequenceProxy SequenceTransform Sequences ShaderNode ShaderNodeAddShader ShaderNodeAmbientOcclusion ShaderNodeAttribute ShaderNodeBackground ShaderNodeBrightContrast ShaderNodeBsdfAnisotropic ShaderNodeBsdfDiffuse ShaderNodeBsdfGlass ShaderNodeBsdfGlossy ShaderNodeBsdfRefraction ShaderNodeBsdfTranslucent ShaderNodeBsdfTransparent ShaderNodeBsdfVelvet ShaderNodeBump ShaderNodeCameraData ShaderNodeCombineRGB ShaderNodeEmission ShaderNodeExtendedMaterial ShaderNodeFresnel ShaderNodeGamma ShaderNodeGeometry ShaderNodeHairInfo ShaderNodeHoldout ShaderNodeHueSaturation ShaderNodeInvert ShaderNodeLayerWeight ShaderNodeLightFalloff ShaderNodeLightPath ShaderNodeMapping ShaderNodeMaterial ShaderNodeMath ShaderNodeMixRGB ShaderNodeMixShader ShaderNodeNewGeometry ShaderNodeNormal ShaderNodeNormalMap ShaderNodeObjectInfo ShaderNodeOutput ShaderNodeOutputLamp ShaderNodeOutputMaterial ShaderNodeOutputWorld ShaderNodeParticleInfo ShaderNodeRGB ShaderNodeRGBCurve ShaderNodeRGBToBW ShaderNodeScript ShaderNodeSeparateRGB ShaderNodeSqueeze ShaderNodeTangent ShaderNodeTexBrick ShaderNodeTexChecker ShaderNodeTexCoord ShaderNodeTexEnvironment ShaderNodeTexGradient ShaderNodeTexImage ShaderNodeTexMagic ShaderNodeTexMusgrave ShaderNodeTexNoise ShaderNodeTexSky ShaderNodeTexVoronoi ShaderNodeTexWave ShaderNodeTexture ShaderNodeTree ShaderNodeValToRGB ShaderNodeValue ShaderNodeVectorCurve ShaderNodeVectorMath ShaderNodeVolumeIsotropic ShaderNodeVolumeTransparent ShaderNodes ShapeActionActuator ShapeKey ShapeKeyBezierPoint ShapeKeyCurvePoint ShapeKeyPoint ShrinkwrapConstraint ShrinkwrapModifier SimpleDeformModifier SkinModifier SmokeCollSettings SmokeDomainSettings SmokeFlowSettings SmokeModifier SmoothModifier SoftBodyModifier SoftBodySettings SolidifyModifier Sound SoundActuator SoundSequence Space SpaceClipEditor SpaceConsole SpaceDopeSheetEditor SpaceFileBrowser SpaceGraphEditor SpaceImageEditor SpaceInfo SpaceLogicEditor SpaceNLA SpaceNodeEditor SpaceOutliner SpaceProperties SpaceSequenceEditor SpaceTextEditor SpaceTimeline SpaceUVEditor SpaceUserPreferences SpaceView3D Speaker SpecialNode SpeedControlSequence Spline SplineBezierPoints SplineIKConstraint SplinePoint SplinePoints SpotLamp StateActuator SteeringActuator StretchToConstraint StringProperties StringProperty Struct StucciTexture SubsurfModifier SubtractSequence SunLamp SurfaceCurve SurfaceModifier TEXTURE_UL_texslots TessfaceUVTextures TexMapping Text TextBox TextCharacterFormat TextCurve TextLine TextMarker Texture TextureNode TextureNodeBricks TextureNodeChecker TextureNodeCompose TextureNodeCoordinates TextureNodeCurveRGB TextureNodeCurveTime TextureNodeDecompose TextureNodeDistance TextureNodeHueSaturation TextureNodeImage TextureNodeInvert TextureNodeMath TextureNodeMixRGB TextureNodeOutput TextureNodeRGBToBW TextureNodeRotate TextureNodeScale TextureNodeTexture TextureNodeTranslate TextureNodeTree TextureNodeValToNor TextureNodeValToRGB TextureNodeViewer TextureNodes TextureSlot Theme ThemeBoneColorSet ThemeClipEditor ThemeConsole ThemeDopeSheet ThemeFileBrowser ThemeFontStyle ThemeGradientColors ThemeGraphEditor ThemeImageEditor ThemeInfo ThemeLogicEditor ThemeNLAEditor ThemeNodeEditor ThemeOutliner ThemePanelColors ThemeProperties ThemeSequenceEditor ThemeSpaceGeneric ThemeSpaceGradient ThemeSpaceListGeneric ThemeStyle ThemeTextEditor ThemeTimeline ThemeUserInterface ThemeUserPreferences ThemeView3D ThemeWidgetColors ThemeWidgetStateColors TimelineMarker TimelineMarkers Timer ToolSettings TouchSensor TrackToConstraint TransformConstraint TransformOrientation TransformSequence UILayout UIList UVLoopLayers UVProjectModifier UVProjector UVTextures UnifiedPaintSettings UnitSettings UnknownType UserPreferences UserPreferencesEdit UserPreferencesFilePaths UserPreferencesInput UserPreferencesSystem UserPreferencesView UserSolidLight UvSculpt VectorFont VertexColors VertexGroup VertexGroupElement VertexGroups VertexPaint VertexWeightEditModifier VertexWeightMixModifier VertexWeightProximityModifier View2D VisibilityActuator VoronoiTexture VoxelData VoxelDataTexture WarpModifier WaveModifier WholeCharacter Window WindowManager WipeSequence WoodTexture World WorldLighting WorldMistSettings WorldStarsSettings WorldTextureSlot WorldTextureSlots XnorController XorController

#//———game———————————————————————————————————————————————
BL_ActionActuator BL_ArmatureActuator BL_ArmatureBone BL_ArmatureChannel BL_ArmatureConstraint BL_ArmatureObject BL_Shader BL_ShapeActionActuator CListValue CPropValue CValue KX_ArmatureSensor KX_BLENDER_GLSL_MATERIAL KX_BLENDER_MULTITEX_MATERIAL KX_BlenderMaterial KX_Camera KX_CameraActuator KX_CharacterWrapper KX_ConstraintActuator KX_ConstraintWrapper KX_FontObject KX_GameActuator KX_GameObject KX_IpoActuator KX_LibLoadStatus KX_LightObject KX_MeshProxy KX_MouseFocusSensor KX_NavMeshObject KX_NearSensor KX_NetworkMessageActuator KX_NetworkMessageSensor KX_ObjectActuator KX_ParentActuator KX_PolyProxy KX_PolygonMaterial KX_RadarSensor KX_RaySensor KX_SCA_AddObjectActuator KX_SCA_DynamicActuator KX_SCA_EndObjectActuator KX_SCA_ReplaceMeshActuator KX_Scene KX_SceneActuator KX_SoundActuator KX_StateActuator KX_SteeringActuator KX_TEXFACE_MATERIAL KX_TouchSensor KX_TrackToActuator KX_VehicleWrapper KX_VertexProxy KX_VisibilityActuator  PyObjectPlus SCA_2DFilterActuator SCA_ANDController SCA_ActuatorSensor SCA_AlwaysSensor SCA_DelaySensor SCA_IActuator SCA_IController SCA_ILogicBrick SCA_IObject SCA_ISensor SCA_JoystickSensor SCA_KeyboardSensor SCA_MouseSensor SCA_NANDController SCA_NORController SCA_ORController SCA_PropertyActuator SCA_PropertySensor SCA_PythonController SCA_PythonJoystick SCA_PythonKeyboard SCA_PythonMouse SCA_RandomActuator SCA_RandomSensor SCA_XNORController SCA_XORController


ExportHelper
ImportHelper



/C14'ctypes   LightBlue' STYLE_KEYWORD Colors = 16776960 Colors Back = 0 Colors Auto Back = 1 Font Style = 0
%
+
-
);
@
=
ARRAY ArgumentError Array BigEndianStructure CDLL CFUNCTYPE DEFAULT_MODE DllCanUnloadNow DllGetClassObject FormatError GetLastError HRESULT LibraryLoader  LittleEndianStructure OleDLL POINTER PYFUNCTYPE  PyDLL RTLD_GLOBAL  RTLD_LOCAL SetPointerType Structure Union WINFUNCTYPE  WinDLL  WinError _CFuncPtr _FUNCFLAG_CDECL  _FUNCFLAG_PYTHONAPI  _FUNCFLAG_STDCALL _FUNCFLAG_USE_ERRNO  _FUNCFLAG_USE_LASTERROR  _Pointer _SimpleCData  __builtins__  __cached__ __doc__  __file__ __initializing__  __loader__ __name__ __package__  __path__ __version__ _c_functype_cache  _calcsize  _cast  _cast_addr  _check_HRESULT _check_size  _ctypes_version  _dlopen  _endian  _memmove_addr _memset_addr  _os  _pointer_type_cache  _reset_cache  _string_at _string_at_addr  _sys  _win_functype_cache  _wstring_at  _wstring_at_addr addressof  alignment byref 
--Oringe---
AUD_DEVICE_JACK AUD_DEVICE_NULL AUD_DEVICE_OPENAL AUD_DEVICE_SDL AUD_DISTANCE_MODEL_EXPONENT AUD_DISTANCE_MODEL_EXPONENT_CLAMPED AUD_DISTANCE_MODEL_INVALID AUD_DISTANCE_MODEL_INVERSE AUD_DISTANCE_MODEL_INVERSE_CLAMPED AUD_DISTANCE_MODEL_LINEAR AUD_DISTANCE_MODEL_LINEAR_CLAMPED AUD_FORMAT_FLOAT32 AUD_FORMAT_FLOAT64 AUD_FORMAT_INVALID AUD_FORMAT_S16 AUD_FORMAT_S24 AUD_FORMAT_S32 AUD_FORMAT_U8 AUD_STATUS_INVALID AUD_STATUS_PAUSED AUD_STATUS_PLAYING BL_DST_ALPHA BL_DST_COLOR BL_ONE BL_ONE_MINUS_DST_ALPHA BL_ONE_MINUS_DST_COLOR BL_ONE_MINUS_SRC_ALPHA BL_ONE_MINUS_SRC_COLOR BL_SRC_ALPHA BL_SRC_ALPHA_SATURATE BL_SRC_COLOR BL_ZERO CAM_POS CD_MCOL CD_MTFACE CD_ORCO CD_TANGENT CLIPPING CONSTANT_TIMER CONSTRAINT_IK_COPYPOSE CONSTRAINT_IK_DISTANCE CONSTRAINT_IK_FLAG_POS CONSTRAINT_IK_FLAG_ROT CONSTRAINT_IK_FLAG_STRETCH CONSTRAINT_IK_FLAG_TIP CONSTRAINT_IK_MODE_INSIDE CONSTRAINT_IK_MODE_ONSURFACE CONSTRAINT_IK_MODE_OUTSIDE CONSTRAINT_TYPE_CLAMPTO CONSTRAINT_TYPE_DISTLIMIT CONSTRAINT_TYPE_KINEMATIC CONSTRAINT_TYPE_LOCKTRACK CONSTRAINT_TYPE_LOCLIKE CONSTRAINT_TYPE_MINMAX CONSTRAINT_TYPE_ROTLIKE CONSTRAINT_TYPE_SIZELIKE CONSTRAINT_TYPE_STRETCHTO CONSTRAINT_TYPE_TRACKTO CONSTRAINT_TYPE_TRANSFORM Fill GPU_DATA_16F GPU_DATA_1F GPU_DATA_1I GPU_DATA_2F GPU_DATA_3F GPU_DATA_4F GPU_DATA_4UB GPU_DATA_9F GPU_DYNAMIC_LAMP_DYNCO GPU_DYNAMIC_LAMP_DYNCOL GPU_DYNAMIC_LAMP_DYNENERGY GPU_DYNAMIC_LAMP_DYNIMAT GPU_DYNAMIC_LAMP_DYNPERSMAT GPU_DYNAMIC_LAMP_DYNVEC GPU_DYNAMIC_OBJECT_COLOR GPU_DYNAMIC_OBJECT_IMAT GPU_DYNAMIC_OBJECT_MAT GPU_DYNAMIC_OBJECT_VIEWIMAT GPU_DYNAMIC_OBJECT_VIEWMAT GPU_DYNAMIC_SAMPLER_2DBUFFER GPU_DYNAMIC_SAMPLER_2DIMAGE GPU_DYNAMIC_SAMPLER_2DSHADOW INSIDE INTERSECT Identity(size=); KERNING_DEFAULT KX_ACTIONACT_FLIPPER KX_ACTIONACT_LOOPEND KX_ACTIONACT_LOOPSTOP KX_ACTIONACT_PINGPONG KX_ACTIONACT_PLAY KX_ACTIONACT_PROPERTY KX_ACTION_MODE_LOOP KX_ACTION_MODE_PING_PONG KX_ACTION_MODE_PLAY KX_ACT_ARMATURE_DISABLE KX_ACT_ARMATURE_ENABLE KX_ACT_ARMATURE_RUN KX_ACT_ARMATURE_SETINFLUENCE KX_ACT_ARMATURE_SETTARGET KX_ACT_ARMATURE_SETWEIGHT KX_ARMSENSOR_LIN_ERROR_ABOVE KX_ARMSENSOR_LIN_ERROR_BELOW KX_ARMSENSOR_ROT_ERROR_ABOVE KX_ARMSENSOR_ROT_ERROR_BELOW KX_ARMSENSOR_STATE_CHANGED KX_CONSTRAINTACT_DIRNX KX_CONSTRAINTACT_DIRNY KX_CONSTRAINTACT_DIRNZ KX_CONSTRAINTACT_DIRPX KX_CONSTRAINTACT_DIRPY KX_CONSTRAINTACT_DIRPZ KX_CONSTRAINTACT_DISTANCE KX_CONSTRAINTACT_DOROTFH KX_CONSTRAINTACT_FHNX KX_CONSTRAINTACT_FHNY KX_CONSTRAINTACT_FHNZ KX_CONSTRAINTACT_FHPX KX_CONSTRAINTACT_FHPY KX_CONSTRAINTACT_FHPZ KX_CONSTRAINTACT_LOCAL KX_CONSTRAINTACT_LOCX KX_CONSTRAINTACT_LOCY KX_CONSTRAINTACT_LOCZ KX_CONSTRAINTACT_MATERIAL KX_CONSTRAINTACT_NORMAL KX_CONSTRAINTACT_ORIX KX_CONSTRAINTACT_ORIY KX_CONSTRAINTACT_ORIZ KX_CONSTRAINTACT_PERMANENT KX_CONSTRAINTACT_ROTX KX_CONSTRAINTACT_ROTY KX_CONSTRAINTACT_ROTZ KX_DYN_DISABLE_DYNAMICS KX_DYN_DISABLE_RIGID_BODY KX_DYN_ENABLE_RIGID_BODY KX_DYN_RESTORE_DYNAMICS KX_DYN_SET_MASS KX_FALSE KX_GAME_LOAD KX_GAME_LOADCFG KX_GAME_QUIT KX_GAME_RESTART KX_GAME_SAVECFG KX_GAME_START KX_INPUT_ACTIVE KX_INPUT_JUST_ACTIVATED KX_INPUT_JUST_RELEASED KX_INPUT_NONE KX_MOUSE_BUT_LEFT KX_MOUSE_BUT_MIDDLE KX_MOUSE_BUT_RIGHT KX_PARENT_REMOVE KX_PARENT_SET KX_PROPSENSOR_CHANGED KX_PROPSENSOR_EQUAL KX_PROPSENSOR_EXPRESSION KX_PROPSENSOR_INTERVAL KX_PROPSENSOR_NOTEQUAL KX_RADAR_AXIS_NEG_X KX_RADAR_AXIS_NEG_Y KX_RADAR_AXIS_NEG_Z KX_RADAR_AXIS_POS_X KX_RADAR_AXIS_POS_Y KX_RADAR_AXIS_POS_Z KX_RANDOMACT_BOOL_BERNOUILLI KX_RANDOMACT_BOOL_CONST KX_RANDOMACT_BOOL_UNIFORM KX_RANDOMACT_FLOAT_CONST KX_RANDOMACT_FLOAT_NEGATIVE_EXPONENTIAL KX_RANDOMACT_FLOAT_NORMAL KX_RANDOMACT_FLOAT_UNIFORM KX_RANDOMACT_INT_CONST KX_RANDOMACT_INT_POISSON KX_RANDOMACT_INT_UNIFORM KX_RAY_AXIS_NEG_X KX_RAY_AXIS_NEG_Y KX_RAY_AXIS_NEG_Z KX_RAY_AXIS_POS_X KX_RAY_AXIS_POS_Y KX_RAY_AXIS_POS_Z KX_SCENE_ADD_BACK_SCENE KX_SCENE_ADD_FRONT_SCENE KX_SCENE_REMOVE_SCENE KX_SCENE_RESTART KX_SCENE_RESUME KX_SCENE_SET_CAMERA KX_SCENE_SET_SCENE KX_SCENE_SUSPEND KX_SENSOR_ACTIVE KX_SENSOR_INACTIVE KX_SENSOR_JUST_ACTIVATED KX_SENSOR_JUST_DEACTIVATED KX_SOUNDACT_LOOPBIDIRECTIONAL KX_SOUNDACT_LOOPBIDIRECTIONAL_STOP KX_SOUNDACT_LOOPEND KX_SOUNDACT_LOOPSTOP KX_SOUNDACT_PLAYEND KX_SOUNDACT_PLAYSTOP KX_STATE1 KX_STATE10 KX_STATE11 KX_STATE12 KX_STATE13 KX_STATE14 KX_STATE15 KX_STATE16 KX_STATE17 KX_STATE18 KX_STATE19 KX_STATE2 KX_STATE20 KX_STATE21 KX_STATE22 KX_STATE23 KX_STATE24 KX_STATE25 KX_STATE26 KX_STATE27 KX_STATE28 KX_STATE29 KX_STATE3 KX_STATE30 KX_STATE4 KX_STATE5 KX_STATE6 KX_STATE7 KX_STATE8 KX_STATE9 KX_STATE_OP_CLR KX_STATE_OP_CPY KX_STATE_OP_NEG KX_STATE_OP_SET KX_STEERING_FLEE KX_STEERING_PATHFOLLOWING KX_STEERING_SEEK KX_TRUE LibFree(name=); LibList(); LibLoad(blend=,type=,data=,load_actions=False,verbose=False,load_scripts=True,async=False); LibNew(name=,type=,data=); Linspace MODELMATRIX MODELMATRIX_INVERSE MODELMATRIX_INVERSETRANSPOSE MODELMATRIX_TRANSPOSE MODELVIEWMATRIX MODELVIEWMATRIX_INVERSE MODELVIEWMATRIX_INVERSETRANSPOSE MODELVIEWMATRIX_TRANSPOSE NORMAL NextFrame(); OUTSIDE OrthoProjection(axis,size); PrintGLInfo(); PrintMemInfo(); RAS_2DFILTER_BLUR RAS_2DFILTER_CUSTOMFILTER RAS_2DFILTER_DILATION RAS_2DFILTER_DISABLED RAS_2DFILTER_ENABLED RAS_2DFILTER_EROSION RAS_2DFILTER_GRAYSCALE RAS_2DFILTER_INVERT RAS_2DFILTER_LAPLACIAN RAS_2DFILTER_MOTIONBLUR RAS_2DFILTER_NOFILTER RAS_2DFILTER_PREWITT RAS_2DFILTER_SEPIA RAS_2DFILTER_SHARPEN RAS_2DFILTER_SOBEL RM_POLYS RM_TRIS RM_WALLS ROTATION ROT_MODE_QUAT ROT_MODE_XYZ ROT_MODE_XZY ROT_MODE_YXZ ROT_MODE_YZX ROT_MODE_ZXY ROT_MODE_ZYX Range Repeat SHADOW SHD_TANGENT SPOT SUN Scale(factor=,size=,axis=); Shear(plane=,size=,factor=); Translation(vector=); UV VIEWMATRIX VIEWMATRIX_INVERSE VIEWMATRIX_INVERSETRANSPOSE VIEWMATRIX_TRANSPOSE XYZ a aa_samples absorption acceleration accuracy act_spline action action_blend_type action_extrapolation action_frame_end action_frame_start action_influence actions activate(actuator=); active activeButtons active_action active_action_unset active_base active_boid_rule active_boid_rule_index active_boid_state active_boid_state_index active_bone active_camera active_channels_group active_clip active_clone active_dupliweight active_dupliweight_index active_events active_file active_file_text active_frame active_index active_input active_input_index active_keyconfig active_layer active_layer_index active_marker active_material active_material_index active_node active_node_material active_object active_object_index active_operator active_output active_particle_target active_particle_target_index active_pose_bone active_render active_section active_shape_key active_shape_key_index active_strip active_textbox active_texture active_texture_index active_track_index activity_culling activity_culling_box_radius activity_culling_radius actuator actuators adapt_margin adapt_threshold adapt_to_speed adaptation adaptive_angle adaptive_pixel adaptive_subframes add addDebugProperty(name=,debug=True); addObject addProp addScene(name=,overlay=1); addWheel additional_res addon_filter addon_search addon_support addons adjugate(); adjugated(); aero aerodynamics_type agent_height agent_radius aggression air_acc_max air_ave_max air_damping air_personal_space air_speed_max air_speed_min alert align alignAxisToVect(vect=,axis=2,factor=1.0); align_orientation(other=); align_roll(vector); alignment alive_state all alliance alpha alpha_blend alpha_factor alpha_influence alpha_mode alt ambient ambient_color ambient_factor amplify amplitude angV angle angle(other=,fallback=None); angle_limit angle_max angle_min angle_offset angle_signed(other=,fallback=None); angle_x angle_y angularVelocity angular_velocity angular_velocity_factor angular_velocity_mode animation_data animation_data_clear(); animation_data_create(); animation_offset_end animation_offset_start animation_player animation_player_preset animation_visualization anisotropic_filter antialiasing_samples ao_blend_type ao_factor ao_samples append(node_tree=,node=None); applyBraking applyEngineForce applyForce(force=,local=False); applyImpulse(point=,impulse=,local=False); applyMovement(movement=,local=False); applyRotation(rotation=,local=False); applyTorque(torque=,local=False); apply_effector_to_children apply_guide_to_children apply_to_children apply_to_hair_growing apply_to_location apply_to_rotation area area_dupli areas arm_head arm_mat arm_tail armatures array_index array_length as_keywords as_string(self); ascii aspect_correction aspect_x aspect_y asymmetry atmosphere_distance_factor atmosphere_extinction atmosphere_inscattering atmosphere_turbidity attenuation attrDict attraction_radius attraction_strength attribute_name audio_channels audio_device audio_distance_model audio_doppler_factor audio_doppler_speed audio_mixing_buffer audio_mixrate audio_sample_format audio_sample_rate audio_strip audio_volume author auto_keying_mode auto_save_time auto_smooth_angle auto_smooth_factor auto_snap auto_texspace autodesk_3ds auxiliary_target average_error average_separation axis axisSingle axisValues axis_direction axis_number axis_threshold axis_u axis_v axis_x axis_y axis_z b back backdrop_channels backdrop_x backdrop_y backdrop_zoom background_images background_set backscattered_light bake(scene=,object=,pass_type=,pixel_array=,num_pixels=,depth=,result=); bake_aa_mode bake_bias bake_distance bake_foam_fade bake_location bake_margin bake_normal_space bake_quad_split bake_type ball_damp ball_size ball_stiff bank base_path basename bbone_in bbone_out bbone_segments bbone_x bbone_z begin_result(x=,y=,w=,h=,layer=''); behavior bend bending_stiffness bending_stiffness_max beta bevel_depth bevel_factor_end bevel_factor_mapping_end bevel_factor_mapping_start bevel_factor_start bevel_object bevel_resolution bevel_weight bezier_points bias billboard_align billboard_animation billboard_normal_uv billboard_object billboard_offset billboard_offset_split billboard_size billboard_split_uv billboard_tilt billboard_tilt_random billboard_time_index_uv billboard_uv_split billboard_velocity_head billboard_velocity_tail bind_display_space_shader(scene=); bindcode birth_time getProfileInfo();
bl_context='object'#['render','data','material','render_layer','world','texture','particle','scene','objectmode','mesh_edit','bone','texturepaint','particlemode','physics','curve_edit','surface_edit','text_edit','armature_edit','mball_edit','lattice_edit','posemode','imagepaint','weightpaint']
bl_description
bl_height_default
bl_height_max
bl_height_min
bl_icon
bl_idname
bl_label
bl_options={'REGISTER','UNDO','BLOCKING','MACRO','GRAB_POINTER','PRESET','INTERNAL'};#Operator
bl_options={'DEFAULT_CLOSED','HIDE_HEADER'};#Panel
bl_region_type='WINDOW'#'HEADER','CHANNELS','TEMPORARY','UI','TOOLS','TOOL_PROPS','PREVIEW']
bl_socket_idname
bl_space_type='PROPERTIES'#['EMPTY','VIEW_3D','TIMELINE','GRAPH_EDITOR','DOPESHEET_EDITOR','NLA_EDITOR','IMAGE_EDITOR','SEQUENCE_EDITOR','CLIP_EDITOR','TEXT_EDITOR','NODE_EDITOR','LOGIC_EDITOR','OUTLINER','USER_PREFERENCES','INFO','FILE_BROWSER','CONSOLE']
bl_static_type bl_use_postprocess bl_use_preview bl_use_shading_nodes bl_width_default bl_width_max bl_width_min black_level blend blendIn blendTime blend_alpha blend_color blend_data blend_distance blend_factor blend_in blend_out blend_type blending blue blur_glossy blur_max blur_post blur_pre blur_radius bodies body body_format body_message body_property body_type boids bokeh bone bone_color_sets bone_from bone_groups bone_pose bone_pose_active bone_solid bone_target bone_to bones boost_factor border_max_x border_max_y border_min_x border_min_y bound_box box(); boxInsideFrustum branch_smoothing branch_threshold bright brightness brownian_factor brush_group brush_influence_scale brush_radius_scale brush_settings brushes buffersize build_100 build_25 build_50 build_75 build_free_run build_free_run_rec_date build_record_run build_undistorted_100 build_undistorted_25 build_undistorted_50 build_undistorted_75 bulge bump_method bump_objectspace bundle bundle_solid buoyancy burning_rate button button_number button_text button_text_hi button_title bvh cache_cloth cache_dynamicpaint cache_format cache_particles cache_resolution cache_smoke cache_softbody calc_angle calc_area(); calc_center_bounds(); calc_center_median(); calc_center_median_weighted(); calc_edge_angle(); calc_face_angle(); calc_face_angle_signed(); calc_length(); calc_matrix_camera(x=1,y=1,scale_x=1.0,scale_y=1.0); calc_normal calc_normals(); calc_normals_split(split_angle=3.14159); calc_perimeter(); calc_shell_factor(); calc_smooth_groups(use_bitflags=False); calc_tangent(uvmap=''); calc_tangent(loop=); calc_tessface(); calc_vert_angle(); calc_volume(signed=False); callback_add(cb=,args=,draw_mode=); callback_remove camera_fit_coords(scene=,coordinates=); camera_override camera_path camera_to_world cameras cancel canvas_settings canvas_surfaces cast_type catadioptric caustics_reflective caustics_refractive cell_height cell_size center_x center_y chain_count chance channel channel_group channel_id channel_matrix channels channels_region channels_selected channels_visibility_set channels_visibility_toggle character_index character_index_end character_index_start charge check checker_distance child_length child_length_threshold child_nbr child_particles child_parting_factor child_parting_max child_parting_min child_radius child_roundness child_seed child_size child_size_random child_type children childrenRecursive children_recursive children_recursive_basename choke choppiness chunk_size cineon_black cineon_gamma cineon_white clamp clean_action clean_error clean_frames clear(); climb_max clip clip_black clip_editor clip_end clip_max_x clip_max_y clip_min_x clip_min_y clip_start clip_user clip_white clipboard clone_alpha clone_cursor_set clone_image clone_offset closest_point_on_mesh(point=,max_dist=1.84467e+19); cloud_type clump_factor clump_shape cluster_iterations co co_deform co_hair(object=,particle_no=0,step=0); co_hair_space co_object(object=,modifier=,particle=); coefficients col coll_settings collide collider_friction collision collision_bounds_type collision_extents collision_group collision_margin collision_quality collision_settings collision_type color color1 color2 color3 color4 color_balance color_depth color_dry_threshold color_factor color_hue color_layer color_mapping color_maximum color_mode color_modulation color_multiply color_picker_type color_ramp color_random color_range color_saturation color_set color_source color_space color_spread_speed color_value coloring colors colorspace_settings column(align=False); column_flow(columns=0,align=False); compare(item=); component compound compressibility compression compression_threshold coneOrigin coneTarget cone_angle_inner cone_angle_outer cone_inner_angle_3d cone_outer_angle_3d cone_outer_gain_3d cone_volume_outer conjugated connected constant_offset_displace constraint constraints context_pointer_set(name=,data=); contrast control_points controllers convert convert_from convert_space(pose_bone=None,matrix=(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0),from_space='WORLD',to_space='WORLD'); convert_to converter_node convex_hull convex_sweep_test(object=,start=,end=); copy from(other=); from_face_interp(face=); from_face_interp(face=,vert=True); from_vert_interp(vert_pair=,fac=); correction correction_method correlation_min count courant_target crease crease_pinch_factor crease_weight create(index=); create_long_hair_children crop crop_max_x crop_max_y crop_min_x crop_min_y cross(other=); ctrl cull_face current_character current_line current_orientation cursor cursor_color_add cursor_color_subtract cursor_location cursor_modal_restore(); cursor_modal_set(cursor=); cursor_position_y cursor_set(cursor=); cursor_warp(x=,y=); curve curve_guide curve_mapping curves custom_shape custom_shape_transform cycles cycles_after cycles_before cycles_curves dLoc dRot damp damp_factor damping damping_epsilon damping_factor damping_max damping_random damping_rotation damping_time darkness data_path dbvt_culling deactivate(actuator=); deactivation_angular_threshold deactivation_linear_threshold deactivation_time debug_bvh_type debug_use_spatial_splits decimate_type decompose(); default_array default_correlation_min default_flag default_frames_limit default_key_count default_margin default_max default_min default_motion_model default_pattern_match default_pattern_size default_search_size default_value default_weight default_weight_a default_weight_b define deform deform_axis deform_method deform_mode delSource delay delete_bookmark delete_frame(frame=); delete_orientation delete_tracks delta_location delta_rotation_euler delta_rotation_quaternion delta_scale density density_factor density_scale depth depth_clamp depth_max depth_object depth_threshold derivate_coefficient description despill_balance despill_factor detect_data(); determinant(); device die_time diffuse diffuse_bounces diffuse_color diffuse_color_factor diffuse_factor diffuse_fresnel diffuse_fresnel_factor diffuse_intensity diffuse_ramp diffuse_ramp_blend diffuse_ramp_factor diffuse_ramp_input diffuse_samples diffuse_shader diffuse_toon_size diffuse_toon_smooth dilate_distance dimension_max dimensions direction direction_axis direction_axis_pos direction_type directory disableMist(); disableMotionBlur(); disableRigidBody(); disabled_marker displace_factor displace_type displacement_factor display_aspect display_channel display_mode display_settings display_type dissolve dissolve_speed distance distance_3d_max distance_3d_reference distance_max distance_maximum distance_metric distance_min distance_model distance_reference distance_repel distortion distortion_type distribution dither_intensity dm_info(type=); doCustomProps doLoc doRot3d doRot4d doScale doc_edit dof_distance dof_object domain_object domain_resolution domain_settings dome_angle dome_buffer_resolution dome_mode dome_tessellation dome_text dome_tilt dopesheet dopesheet_channel dopesheet_editor dopesheet_subchannel doppler_factor dot(other=); double_array double_threshold dpi drag drag_factor drag_threshold draw(context); drawLine(fromVec=,toVec=,color=); drawObstacleSimulation draw_action draw_bounds_type draw_buttons(context,layout=); draw_buttons_ext(context,layout=); draw_channels draw_color(context,node=); draw_depth draw_filter(context,layout=); draw_handler_add(); draw_handler_remove(); draw_header(context); draw_item(context,layout=,data=,item=,icon=,active_data=,active_propname=,index=); draw_label(); draw_method draw_mode draw_overexposed draw_percentage draw_preset(context); draw_size draw_step draw_stretch_type draw_type drawingmode drip_acceleration drip_velocity driver drivers dry_spe dt_frac dupli_faces_scale dupli_frames_end dupli_frames_off dupli_frames_on dupli_frames_start dupli_group dupli_list dupli_list_clear(); dupli_list_create(scene=,settings='VIEWPORT'); dupli_object dupli_offset dupli_type dupli_weights duration dynamic_friction dynamic_operation dynamic_paint

edge edge_collapse_loop edge_color edge_crease_inner edge_crease_outer edge_crease_rim edge_draw_type edge_facesel edge_index edge_kernel_radius edge_kernel_tolerance edge_keys edge_max_error edge_max_len edge_mode edge_path_live_unwrap edge_path_mode edge_seam edge_select edge_sharp edge_threshold edge_weight_method edges edit edit_bone edit_bones edit_format edit_image edit_mask edit_movieclip edit_object edit_quality edit_text edit_tree editable_bones editmesh_active effect_fader effect_hair effect_strip effect_ui effector_amount effector_group effector_weights elasticity element_index elements emission emission_color emission_color_factor emission_factor emit emit_factor emit_from emitter_distance empty empty_draw_size empty_draw_type empty_image_offset enableMotionBlur(factor=); enableRigidBody(); enableVisibility(visible=); enableVisualization enabled end endGame(); endObject(); end_cap end_result(result=,cancel=False,do_merge_results=False); end_time energy enforce engine enum_item_description(data=,property=,identifier=); enum_item_icon(data=,property=,identifier); enum_item_name(data=,property=,identifier=); enum_items envelope_distance envelope_weight environment_color environment_energy environment_map error error_location error_rotation error_set(message); error_threshold etch_adaptive_limit etch_convert_mode etch_length_limit etch_number etch_roll_mode etch_side etch_subdivision_number etch_template eval_factor eval_frame eval_time evaluate(position=); evaluate_envelope(point=); evaluation_type event_timer_add(time_step=,window=None); event_timer_remove(timer=); event_type exclude_ambient_occlusion exclude_emit exclude_environment exclude_indirect exclude_reflection exclude_refraction exclude_shadow exclude_specular execute(context=,event=); executePriority exit_key expandPath(path=); export_layout expose exposure expression extension extra_edge_len extra_face_angle extra_face_area extrapolation extrude eyedropper

f_stop face_count face_dot face_index face_orientation face_select face_select_inverse facedot_size faces facing facing_axis factor factor_blue factor_green factor_radius factor_random factor_red factor_repulsion factor_rest_length factor_stiff_viscosity factor_x factor_y factor_z factory fade fade_frames fade_to fadein fadeout fall_speed falloff falloff_curve falloff_power falloff_radius falloff_soft falloff_speed_scale falloff_strength falloff_type family far fbx fcurve_unselected_alpha fcurves fear_factor feather_distance feather_falloff feature_set feedback ffmpeg fh_damping fh_distance fh_force fh_height field field_factor field_order fields_per_frame fileName file_browser(); file_extension file_format file_paste file_slots(); filename filepath filepath_from_user(image_user=None); filepath_raw filepaths fileselect_add(operator=); fill_mode film_exposure film_transparent filter_eccentricity filter_fcurve_name filter_glob filter_group filter_items(context,data=,property=); filter_pass filter_probes filter_size filter_text filter_type filter_width find(key); find(name=,space_type='EMPTY',region_type='WINDOW'); findPath find_armature(); find_frame(frame=,exact=True); find_modal(name=); find_text fit_length fit_type fixed_type flame_ignition flame_max_temp flame_smoke flame_smoke_color flame_vorticity flaps flare_boost flare_seed flare_size flare_subflare_count flare_subflare_size flee_distance flip_axis float_array float_max float_mean float_min float_value floor_location flow flow_settings fluid_group fluid_mesh_vertices fluid_radius foam_coverage foam_layer_name focal_length focal_length_pixels follow_curve font_bold font_bold_italic font_directory font_italic font_kerning_style font_size fonts force forceLimitX forceLimitY forceLimitZ force_field_1 force_field_2 force_max_x force_max_y force_max_z force_min_x force_min_y force_min_z foreach_get(attr=,seq=); foreach_set(attr=,seq=); form_factor forward_axis fps fps_base frame frameEnd frameMessageCount framePropName frameStart frame_after frame_before frame_blend_in frame_color frame_current frame_duration frame_end frame_final_duration frame_final_end frame_final_start frame_map_new frame_map_old frame_method frame_node frame_number frame_offset_end frame_offset_start frame_path(frame=-2147483648); frame_preview_end frame_preview_start frame_property frame_range frame_relative frame_scale frame_server_port frame_set(frame=,subframe); frame_start frame_step frame_still_end frame_still_start frame_subframe frame_substeps frame_type frames frames_limit frames_skipped free(); free_axis free_normals_split(); free_tangents(); frequency fresnel fresnel_factor friction friction_coefficients friction_factor friction_random from_existing(src_driver=None); from_id(id=); from_max_x from_max_y from_max_z from_mesh(mesh=, face_normals=True, use_shape_key=False, shape_key_index=0); from_min_x from_min_y from_min_z from_node from_object(object=,scene=,deform=True,render=False,cage=False,face_normals=True); from_pydata(vertices=,edges,faces=); from_socket(node=,socket=); from_string(string=); front frustum_culling function_type functions fuzzy

gain gain_3d_max gain_3d_min game game_settings gamma gather_method ge_shadow_buffer_type generate(context,ks=,data=); generate_particles generated_height generated_type generated_width geometry_mode getActionFrame(layer=0); getAngularVelocity(local=False); getAnisotropicfIltering(); getAverageFrameRate(); getAxisVect(vect=); getBlendFileList(path='//'); getButtonActiveList getButtonStatus getCameraToWorld getClipboard getConstraintId getConstraintType getCurrentController(); getCurrentScene(); getDistanceTo(other=); getExitKey(); getEyeSeparation(); getFocalLength(); getFragmentProg getGLSLMaterialSetting(setting=,enable=); setAnisotropicfIltering(level=); setMipmapping(value=); getMipmapping(); getKeyStatus getLinearVelocity(local=False); getLogicTicRate(); getMaterial getMaterialIndex getMaterialMode(mode=); getMaterialName getMaxLogicFrame(); getMaxPhysicsFrame(); getMesh getNormal getNumVertex getNumWheels(); getPhysicsId(); getPhysicsTicRate(); getPolygon getPropertyNames(); getRGBA getRandomFloat(); getReactionForce(); getSceneList(); getScreenPosition getScreenRay getScreenVect getShader getSpectrum(); getStripElem getTextureName getUV getUV2 getVectTo(other=); getVelocity(point=(0,0,0)); getVertex getVertexArrayLength getVertexIndex getVertexProg getWheelOrientationQuaternion getWheelPosition getWheelRotation getWindowHeight(); getWindowWidth(); getWorldToCamera getXYZ get_from_context(context); ghos ghost_frame_end ghost_frame_start ghost_range_max ghost_size ghost_step ghost_type gl_clip_alpha gl_free(); gl_load(frame=0,filter=9985,mag=9729); gl_texture gl_texture_limit gl_touch(frame=0,filter=9985,mag=9729); glare_type globalDict gloss_anisotropic gloss_factor gloss_samples gloss_threshold glossy_bounces glossy_samples glsl_shader goal_default goal_friction goal_max goal_min goal_spring gradient_type gravity gravity_factor grease_pencil grease_pencil_eraser_radius grease_pencil_manhattan_distance grease_pencil_source green grid grid_levels grid_lines grid_random grid_resolution grid_scale grid_subdivisions ground_albedo groupMembers groupObject group_node groups guide_clump_amount guide_clump_shape guide_free guide_kink_amplitude guide_kink_axis guide_kink_frequency guide_kink_shape guide_kink_type guide_minimum

hair_keys hair_length hair_step half_life_time halo halo_intensity halo_step handle_align handle_auto handle_auto_clamped handle_free handle_left handle_left_type handle_right handle_right_type handle_sel_align handle_sel_auto handle_sel_auto_clamped handle_sel_free handle_sel_vect handle_vect handle_vertex handle_vertex_select handle_vertex_size hard_max hard_min hardness hardness_factor harmonic harmonic_damping has_accumulate has_auto_smooth has_bundle has_data has_ghost_curves has_height has_ik has_jitter has_multiple_caches has_multiple_engines has_normal_weight has_overlay has_persistence has_pinch_factor has_plane_offset has_random_texture_angle has_reports has_script_error has_sculpt_plane has_secondary_color has_smooth_stroke has_space_attenuation has_spacing has_strength has_texture_angle has_texture_angle_source hat hatSingle hatValues hat_direction hat_number head head_local head_radius head_tail header header_text header_text_hi header_text_set(text=''); headtail health height hexagonal_grid hide hide_recent_locations hide_render hide_select hide_set(hide); highlights_contrast highlights_gain highlights_gamma highlights_lift highlights_saturation highpass highres_sampling hinge histogram history hitNormal hitObject hitObjectList hitPosition hitUV hold1 hold2 horizon_brightness horizon_color horizon_factor hsv i18n_branches_directory icon(data=); icon_alpha icon_file icon_filepath id id_from id_root id_type identifier identity(); idname idp_array ik_dist ik_dof_x ik_dof_y ik_dof_z ik_flag ik_limit_x ik_limit_y ik_limit_z ik_lin_control ik_lin_weight ik_linear_weight ik_max_x ik_max_y ik_max_z ik_min_x ik_min_y ik_min_z ik_mode ik_param ik_rot_control ik_rot_weight ik_rotation_weight ik_solver ik_stiffness_x ik_stiffness_y ik_stiffness_z ik_stretch ik_type ik_weight image image_editor image_fileformat image_output_path image_paint_object image_resolution image_settings image_strip image_tool image_user images impact_factor in_out_node ensure_lookup_table(); index index_update(); indirect_bounces indirect_factor inflow inflow_velocity influence influence_location influence_rotation influence_scale inherit_scale init(context); init_color init_color_type init_layername init_socket(node=,socket=,data_path=); init_texture initial_velocity initialize(); inner inner_anim inner_anim_sel inner_driven inner_driven_sel inner_key inner_key_sel inner_mode inner_sel input_1 input_2 input_count input_mask_id input_mask_strip input_mask_type input_samples input_template(index=); inputs insert(text=''); insert_frame(frame=,co=(0.0,0.0); instantAddObject instantReplaceMesh int_array int_max int_mean int_min int_value integral_coefficient integrator intensity interface interface_update(context); internal_friction interpolation interpolation_type_u interpolation_type_v interpolation_type_w introspect();

----2----------------------------------------------------------------------
invalid inverse_matrix invert(fallback=None); invert_alpha invert_gain invert_gamma invert_grid invert_lift invert_mouse_zoom invert_normal invert_proximity invert_rgb invert_safe(); invert_stencil invert_vertex_group invert_vertex_group_clump invert_vertex_group_density invert_vertex_group_field invert_vertex_group_kink invert_vertex_group_length invert_vertex_group_rotation invert_vertex_group_roughness_1 invert_vertex_group_roughness_2 invert_vertex_group_roughness_end invert_vertex_group_size invert_vertex_group_tangent invert_vertex_group_velocity invert_x invert_y invert_z invert_zmask invert_zoom_wheel inverted(fallback=None); inverted_safe(); invisible invoke(context=,event=); invoke_confirm(operator=,event=); invoke_popup(operator=,width=300,height=20); invoke_props_dialog(operator=,width=300,height=20); invoke_props_popup(operator=,event=); invoke_search_popup ior is3D isCollider isPlayingAction(layer=0);  isValid isVisible is_active is_active_output is_animatable is_animation is_animation_playing is_baked is_baking is_bound is_boundary is_cache_user is_cached is_camera is_deform_modified(scene=,settings=); is_dirty is_duplicator is_editable is_edited is_enum_flag is_exist is_external is_float is_fluid is_global_hair is_hair is_hidden is_in_ik_chain is_in_memory is_library_editable is_linked is_loose is_manifold is_modal is_modified(scene=,settings=); is_movie_format is_negative is_never_none is_nla_tweakmode is_occlusion_query_supported(); is_orthogonal is_orthogonal_axis_vectors is_outdated is_output is_path_absolute is_perspective is_preview is_proxy_local is_readonly is_registered is_registered_node_type(); is_registered_optional is_required is_runtime is_saved is_singleton is_skip_save is_solo is_start is_supports_mask is_temporary is_updated－ is_user_defined is_user_modified is_valid is_visible(scene=); is_wire is_wrapped item iterations iterator(context,ks=); jitter jitter_factor join joint_bindings joint_rotation joystick_index joysticks jump jumpCount jump_speed k1 k2 k3 keep keep_axis key key_blocks key_modifier keyboard keyconfigs keyed_loops keyframe keyframe_a keyframe_b keyframe_new_handle_type keyframe_new_interpolation_type keyframe_points keying_sets keying_sets_all keymap_items keymaps keys_step kink kink_amplitude kink_amplitude_clump kink_axis kink_factor kink_flat kink_frequency kink_shape label(text='',text_ctxt='',translate=True,icon='NONE',icon_value=0); label_size lacunarity lambda_border lambda_factor lamp_object lamps land_acc_max land_ave_max land_jump_speed land_personal_space land_smooth land_speed_max land_stick_force language lastDraw lastsel_point lattices layer layer_slots layer_weight layers layers_exclude layers_from_view(view=); layers_ignore layers_local_view layers_protected layers_used layers_zmask layout layout_type length length_factor length_max length_mode length_random length_squared lennardjones lens lens_unit lerp(other=,factor=); level level_height levels  libraries libraryName life life_factor lifetime lifetime_random lift light_group light_method light_override light_settings lights limit limit_angle_max_x limit_angle_max_y limit_angle_max_z limit_angle_min_x limit_angle_min_y limit_angle_min_z limit_channel limit_max limit_max_x limit_max_y limit_max_z limit_method limit_min limit_min_x limit_min_y limit_min_z limit_mode linV linVelocityMax linVelocityMin lin_attenuation lin_error line_count line_error line_info line_input line_length_head line_length_tail line_numbers_background line_output line_thickness line_thickness_mode line_width linearVelocity linear_attenuation linear_drag linear_stiffness linear_velocity linear_viscosity link(); link_append link_edges link_faces link_loop_next link_loop_prev link_loops links list_text list_text_hi list_title listener_location listener_orientation listener_velocity load(imageBuffer=,width=,height=); plot(imageBuffer=,width=,height=,positionX=,positionY=); getSource(imageMix=); getWeight(imageMix=);  loadGlobalDict(); load_from_file(filename=,x=0,y=0); localAngularVelocity localInertia localLinearVelocity localOrientation localPosition localScale localTransform local_view location location_iterations location_mass_center lock lock_axis lock_billboard lock_boids_to_surface lock_bone lock_bounds lock_camera lock_camera_and_layers lock_cursor lock_frame lock_ik_x lock_ik_y lock_ik_z lock_location lock_location_x lock_location_y lock_location_z lock_object lock_rotation lock_rotation_w lock_rotation_x lock_rotation_y lock_rotation_z lock_rotations_4d lock_scale lock_selection lock_time_cursor lock_weight lock_x lock_y lock_z locked_marker log logic_editor logic_step_max long_key long_key_selected look_ahead loop loop_count loop_indices loop_total loops lowpass magnetic magnitude main_axis makeScreenshot(filename=); make_compatible(other=); manipulator_handle_size manipulator_hotspot manipulator_size map_curve map_from map_mode map_to map_to_x_from map_to_y_from map_to_z_from map_type mapping mapping_x mapping_y mapping_z marble_type margin margin_column mark_all marker_outline markers markers_clear mask_constant mask_draw_type mask_tex_map_object mask_tex_mapping mask_tex_use_channel mask_tex_uv_layer mask_texture mask_tool mask_type mask_vertex_group masks mass master_contrast master_gain master_gamma master_lift master_saturation match material_id material_index material_link material_mode material_name material_offset material_offset_rim material_override material_slot material_slots materials matrix matrix_basis matrix_channel matrix_from_frame(frame=1); matrix_local matrix_original matrix_parent_inverse matrix_world matte_channel max maxJumps max_bounces max_dist max_iterations max_value max_x max_y maximum_width maxrate mcol_on_emitter(modifier=,particle=,particle_no=0,vcol_no=0); median_scale memory_cache_limit memory_estimate menu(menu=,text='',text_ctxt='',translate=True,icon='NONE'); menu_pie(); merge_threshold mesh_light_samples mesh_select_mode meshes meta_ball meta_stack meta_strip meta_strips meta_strips_selected metaballs mid_level midtones_contrast midtones_end midtones_gain midtones_gamma midtones_lift midtones_saturation midtones_start min min_bounces min_dist min_value min_x min_y mini_axis_brightness mini_axis_size minimum_width minkovsky_exponent minrate mirror_color mirror_factor mirror_object mist_settings mix mix_mode mix_set modal(context=,event=); modal_handler_add(operator=); mode mode_after mode_before modelview_matrix modifier_key_1 modifier_key_2 modifiers module motion_blur_factor motion_blur_samples motion_blur_shutter motion_model motion_path mouse mouse_double_click_time mouse_event mouse_prev_x mouse_prev_y mouse_region_x mouse_region_y mouse_x mouse_y move movie_strip movieclip_strip movieclips mpeg_preseek ms_diffusion ms_intensity ms_spread multicam_source multilayer_layer multilayer_pass multiply_speed musgrave_type mutate mute muted nabla name－ name_property narrowness navmesh ndof_fly_helicopter ndof_lock_horizon ndof_orbit_sensitivity ndof_panx_invert_axis ndof_pany_invert_axis ndof_panz_invert_axis ndof_roll_invert_axis ndof_rotate_invert_axis ndof_sensitivity ndof_sensitivity_change ndof_tilt_invert_axis ndof_turntable ndof_zoom_invert ndof_zoom_updown near neg_ticks negate(); nested new new_clip(name=,clip=,channel=,frame_start=); new_effect(name=,type=,channel=,frame_start=,frame_end=0,seq1=None,seq2=None,seq3=None); new_image(name=,filepath=,channel=,frame_start=); new_mask(name=,mask,channel=,frame_start=); new_modal(propvalue=,type=,value=,any=False,shift=False,ctrl=False,alt=False,oskey=False,key_modifier='NONE'); new_movie(name=,filepath=,channel=,frame_start=); new_node_tree(type='',name='NodeTree'); new_scene(name=,scene=,channel=,frame_start=); new_sound(name=,filepath=,channel=,frame_start=); next next_marker ngon_method nla_editor nla_tracks no_caustics node_active node_backdrop node_editor node_groups node_output node_selected node_tree nodes noise noise_basis noise_basis_2 noise_depth noise_distortion noise_intensity noise_scale noise_type noodle_curving normal normal_angle normal_factor normal_map_space normal_size normal_up normal_update(); normal_weight normalize(); normalized(); numAxis numButtons numHats numMaterials numPolygons nurb_sel_uline nurb_sel_vline nurb_uline nurb_vline obj  objectLastCreated object_active object_align object_align_factor object_bases object_distance object_factor object_from object_grouped object_grouped_active object_origin_size object_property object_selected object_to objects objectsInactive obstacle_radius obstacle_simulation occlusion occlusion_culling_resolution ocean ocean_object octaves octree_depth octree_resolution offset offset_factor offset_frequency offset_location offset_mode offset_object offset_rotation offset_x offset_y offset_z onGround onion_skin_frames opacity open_left_mouse_delay open_right_mouse_delay open_sublevel_delay open_toplevel_delay operation operator(operator=,text='',text_ctxt='',translate=True,icon='NONE',emboss=True,icon_value=0); operator_context operator_enum(operator=,property=); operator_menu_enum(operator=,property=,text='',text_ctxt='',translate=True,icon='NONE'); operators option order order_u order_v orient_weight orientation orientations orig_height orig_width ortho_scale oskey other_vert(vert=); outline outline_width output output_exists(object=,index=); output_name_a output_name_b output_template(index=); outputs overlay_frame overlay_type owner owner_space pack(as_png=False); packed_file packetsize paint_alpha paint_color paint_distance paint_ramp paint_settings(context); paint_source paint_wetness panel panel_title para1 para2 parameters params parent parent_bone parent_index(parent_test=); parent_recursive parent_type parent_vertices partial_slip_factor particle_cache_space particle_edit particle_edit_object particle_factor particle_index particle_influence particle_keys particle_settings particle_size particle_system particle_system_editable particle_system_index particle_systems particle_uv particles parts_x parts_y passNumber pass_alpha_threshold pass_index passepartout_alpha passes pathUpdatePeriod path_after path_before path_duration path_end path_length path_menu(searchpaths=,operator=,props_default={},filter_ext=None); path_start paths pattern_bound_box pattern_corners pattern_match pause(); pauseSound pen_flip permeability perspective perspective_matrix phase phase_factor phase_factor_random phase_multiplier phase_offset physics physics_engine physics_gravity physics_step_max physics_step_sub physics_type pid piemenu_begin__internal(title=,icon='NONE',event=None); piemenu_end__internal(menu=None); pin pin_id pin_stiffness pin_uv pingpong pitch pivot_point pivot_type pivot_x pivot_y pivot_z pixel_aspect pixel_aspect_x pixel_aspect_y pixel_filter_type pixels plane_offset plane_track_name plane_trim plasticity play(); playAction(name=,start_frame=,end_frame=,layer=0,priority=0,blendin=0,play_mode=KX_ACTION_MODE_PLAY,layer_weight=0.0,ipo_flags=0,speed=1.0,blend_mode=KX_ACTION_BLEND_BLEND); play_mode ply pointInsideFrustum point_cache point_cache_compress_type point_caches point_count_u point_count_v point_density point_source points points_u points_v points_w pole_angle pole_subtarget poll(context); poll_instance(node_tree=); poly_order polygon_layers_float polygon_layers_int polygon_layers_string polygons pop(index=-1,update_data=False); popup_menu(draw_func,title='',icon='NONE'); pos_ticks pose_bone pose_head pose_library pose_markers pose_matrix pose_position pose_tail position positive post_draw power pre_draw pre_roll precision premul prepend pressure prev_angular_velocity prev_location prev_rotation prev_velocity preview_aa_samples preview_back preview_render_type preview_resolution preview_samples preview_start_resolution preview_stitch_active preview_stitch_edge preview_stitch_face preview_stitch_stitchable preview_stitch_unstitchable preview_stitch_vert previous_marker primitive principal priority progress progress_begin(min=,max=); progress_end(); progression progressive project project_limit projection projection_blend projection_matrix projector_count projectors prompt prop(data=,property=,text='',text_ctxt='',translate=True,icon='NONE',expand=False,slider=False,toggle=False,icon_only=False,event=False,full_event=False,emboss=True,index=-1,icon_value=0); propName prop_enum(data=,property=,value=,text='',text_ctxt='',translate=True,icon='NONE'); prop_menu_enum(data=,property=,text='',text_ctxt='',translate=True,icon='NONE'); prop_search(data=,property=,search_data=,search_property=,text='',text_ctxt='',translate=True,icon='NONE'); prop_unified_color(parent=,context,brush=,prop_name=,text=''); prop_unified_color_picker(parent=,context,brush=,prop_name=,value_slider=True); prop_unified_size(parent=,context,brush=,prop_name=,icon='NONE',text='',slider=False); prop_unified_strength(parent=,context,brush=,prop_name=,icon='NONE',text='',slider=False); prop_unified_weight(parent=,context,brush=,prop_name=,icon='NONE',text='',slider=False); properties property proportional_coefficient proportional_edit proportional_edit_falloff proportional_size props_enum(data=,property=); propvalue protect proximity_falloff proximity_geometry proximity_mode proxy proxy_group proxy_render_size puff_mode pull pupmenu_begin__internal(title,icon='NONE'); pupmenu_end__internal(menu=None); push quad_attenuation quad_method quadratic_attenuation quadratic_drag quality queue_count quit_dialog radial_falloff radial_max radial_min radial_symmetry radius radius_interpolation radius_scale random_position random_seed range rate ratio rayCast(objto=,objfrom=,dist=,prop=,face=,xray=,poly=); rayCastTo(other=,dist=,prop=); rayDirection rayLength raySource rayTarget ray_cast(start=,end=); ray_direction ray_length ray_type raycast raymir_factor raytrace_method raytrace_mirror raytrace_transparency react_event reactor_factor reactor_target_object reactor_target_particle_system rebuild recast_data recent_files reconstruction record_composite rect red reference reference_axis reference_key reference_object reference_value refine_intrinsics reflect reflect_factor reflection reflection_color reflection_color_factor reflection_factor refresh(); region region_3d region_data region_merge_size region_min_size region_to_view(x=,y=); region_type regions register_properties(data_rna_type=); regrow_hair reinstancePhysicsMesh(gameObject=,meshObject=); reiteration_method rel_max_x rel_max_y rel_min_x rel_min_y relative relative_frame relative_key relative_offset_displace removeParent(); remove_threshold render(scene=None); render_display_mode render_levels render_output_directory render_quality render_resolution render_resolution_u render_resolution_v render_slot render_step render_steps render_type rendered_child_count repeat repeat_x repeat_y repel_force replaceMesh(mesh=,useDisplayMesh=True,usePhysicsMesh=False); replace_text report(type=,message=); repulsion resetDistance reset_distance resize_2d resize_3d resize_4d resize_4x4(); resized resolution resolution_max resolution_percentage resolution_u resolution_v resolution_x resolution_y rest_density rest_length rest_shape_key restart restartGame(); restoreDynamics(); restore_item_to_default(item=); restore_to_default(); resume rigidbody_world ring_count roll rolloff_factor_3d root_size root_width rotDamp rot_error rotate(other=); rotate_axis(axis,angle); Rotation(angle=,size=,axis=); rotation rotation_angle rotation_axis_angle rotation_damping rotation_difference(other=); rotation_estimate rotation_euler rotation_factor_random rotation_max rotation_mode rotation_quaternion rotation_range rotation_start rotation_track rough_factor roughness roughness_1 roughness_1_size roughness_2 roughness_2_size roughness_2_threshold roughness_end_shape roughness_endpoint rounding row(align=False); rules ruleset_type sample sample_all_lights_direct sample_clamp_direct sample_clamp_indirect sample_dist sample_histogram sample_max_error sample_method sampled_points samples sampling_pattern saturation save(filepath=,scene=None,layout=(0.0,0.0,1.0,0.0,2.0,0.0,0.0,1.0,1.0,1.0,2.0,1.0); saveGlobalDict(); save_render(filepath=,scene=None); save_version scale(width,height); scale_estimate scale_length scale_max scale_start_x scale_start_y scale_to_length scale_x scale_y scaling scattering scattering_factor scene_strip scenes scope_back scopes screen_balance screen_grab_size screencast_fps screencast_wait_time screens screw_offset script_directory scripts scroll_handle scrollback scrollbar sculpt_capabilities sculpt_levels sculpt_object sculpt_paint_overlay_color sculpt_plane sculpt_tool seam seam_bleed search_max search_min secondary_target seed select select_control_point select_edge select_end select_end_line select_flip_active select_flush(select=); select_flush_mode(); select_head select_history select_inverse select_left_handle select_loose_verts select_mode select_mouse select_right_handle select_same_type select_same_type_next select_same_type_prev select_search select_set(select=); select_shortest_path select_start select_tail select_vertex_path selectable_bases selectable_objects selected_bases selected_bones selected_editable_bases selected_editable_bones selected_editable_objects selected_editable_sequences selected_file selected_highlight selected_marker selected_nodes selected_objects selected_pose_bones selected_sequences selected_text self_collision_quality self_distance_min self_friction self_terminated selfterminated sendMessage(subject=,body='',to=''); sensor_fit sensor_height sensor_width sensors separator(); sequence_editor sequence_editor_clear(); sequence_editor_create(); sequencer_colorspace_settings sequencer_gl_preview sequencer_gl_render sequences sequences_all setActionFrame(frame=,layer=0); setAmbientColor(rgb=); setAngularVelocity(velocity=,local=False); setAttrib setBackgroundColor(rgba=); setBlending setBoolBernouilli setBoolConst setBoolUniform setClipboard setCollisionMargin(margin=); setCustomMaterial setExitKey(key=); setEyeSeparation(eyesep=); setFloatConst setFloatNegativeExponential setFloatNormal setFloatUniform setFocalLength(focallength=); setGLSLMaterialSetting(setting=,enable=); setGravity(gravity=); setIntConst setIntPoisson setIntUniform setLinearVelocity(velocity=,local=False); setLogicTicRate(ticrate=); setMaterialMode(mode=); setMaxLogicFrame(maxlogic=); setMaxPhysicsFrame(maxphysics=); setMistColor(rgb=); setMistEnd(end=); setMistStart(start=); setMousePosition(x=,y=); setNormal setNumberOfPasses setOcclusion(occlusion=,recursive=); setOnTop setParent(parent=,compound=True,ghost=True); setPhysicsTicRate(ticrate=); setRGBA setRollInfluence setSampler setSource(imageMix=); setWeight(imageMix=); getLastError(); imageToArray(image=,mode=); materialID(object=,name=); setLogFile(filename=); EventToString(event=); EventToCharacter(event=,shift=); createConstraint(physicsid=,physicsid2=,constrainttype=,[pivotX,pivotY,pivotZ,[axisX,axisY,axisZ,[flag]]]]); exportBulletFile(filename=); getAppliedImpulse(constraintId=); getVehicleConstraint(constraintId=); getCharacter(gameobj=); removeConstraint(constraintId=); setCcdMode(ccdMode=); setContactBreakingTreshold(breakingTreshold=); setDeactivationAngularTreshold(angularTreshold=); setDeactivationLinearTreshold(linearTreshold=); setDeactivationTime(time=); setDebugMode(mode=);  setSteeringValue setSuspensionCompression setSuspensionDamping setSuspensionStiffness setTextureface setTyreFriction setUV setUV2 setUniform1f setUniform1i setUniform2f setUniform2i setUniform3f setUniform3i setUniform4f setUniform4i setUniformDef setUniformMatrix3 setUniformMatrix4 setUniformfv setUniformiv setViewport setVisible(visible=,recursive=); setWindowSize(width=,height=); setFullScreen(enable=); getFullScreen(); setXYZ set_resolution(scene=None,object=None,resolution='PREVIEW'); settings sewing_force_max shadedown shader shaderText shader_type shadetop shading_system shadow_adaptive_threshold shadow_adjust shadow_buffer_bias shadow_buffer_bleed_bias shadow_buffer_clip_end shadow_buffer_clip_start shadow_buffer_samples shadow_buffer_size shadow_buffer_soft shadow_buffer_type shadow_cast_alpha shadow_color shadow_factor shadow_filter_type shadow_method shadow_offset_x shadow_offset_y shadow_only_type shadow_ray_bias shadow_ray_sample_method shadow_ray_samples_x shadow_ray_samples_y shadow_sample_buffers shadow_soft_size shadowalpha shadowcolor shadows_contrast shadows_gain shadows_gamma shadows_lift shadows_saturation shape shape_key_add(name='Key',from_mix=True); shape_keys shape_threshold sharpness shift shift_x shift_y shininess showMouse(visible=); show_actuators show_actuators_active_object show_actuators_active_states show_actuators_linked_controller show_actuators_selected_objects show_alive show_all_edges show_all_objects_origin show_armatures show_axes show_axis show_axis_x show_axis_y show_axis_z show_backdrop show_backface_culling show_background_image show_background_images show_blue_channel show_bone_custom_shapes show_bounds show_brush show_brush_on_surface show_bundle_names show_bundles show_cache show_camera_path show_cameras show_colored_constraints show_column_layout show_cone show_controllers show_controllers_active_object show_controllers_linked_controller show_controllers_selected_objects show_cursor show_curves show_cyclic_dependencies show_datablock_filters show_dead show_debug show_debug_info show_debug_properties show_debug_state show_default_expanded show_disabled show_double_sided show_edge_bevel_weight show_edge_crease show_edge_seams show_edge_sharp show_edges show_expanded show_expanded_children show_expanded_items show_expanded_summary show_extra_edge_angle show_extra_edge_length show_extra_face_angle show_extra_face_area show_extra_indices showFramerate(enable=); showProfile(enable=); showProperties(enable=); autoDebugList(enable=); clearDebugList(); setVsync(value=); getVsync(); show_faces show_filters show_floor show_frame_indicator show_frame_numbers show_framerate_profile show_frames show_freestyle_edge_marks show_freestyle_face_marks show_fullscreen show_graph_frames show_graph_hidden show_graph_only_selected show_graph_tracks show_green_channel show_grid show_group_colors show_guide show_handles show_header show_health show_hidden show_hidden_files_datablocks show_high_resolution show_highlight show_in_editmode show_keyframe_action_all show_keyframe_highlight show_keyframe_numbers show_lamps show_large_cursors show_lattices show_limits show_line show_line_highlight show_line_numbers show_low_resolution show_manipulator show_margin show_marker_pattern show_marker_search show_mask_smooth show_maskedit show_materials show_menus show_meshes show_metaballs show_mini_axis show_missing_nla show_mist show_modified_edges show_mouse show_name show_names show_nodes show_normal_face show_normal_loop show_normal_vertex show_normalized_coords show_number show_object_info show_obstacle_simulation show_on_cage show_on_foreground show_only_control_edges show_only_ghost_selected show_only_group_objects show_only_matching_fcurves show_only_render show_only_selected show_only_shape_key show_options show_other_objects show_outline_selected show_overlay show_paint show_particles show_passepartout show_physics_visualization show_pivot show_playback_fps show_points show_pose_markers show_preview show_reconstruction show_red_channel show_relationship_lines show_render show_repeat show_report_debug show_report_error show_report_info show_report_operator show_report_warning show_restrict_columns show_safe_margin show_scenes show_seconds show_sensor show_sensors show_sensors_active_object show_sensors_active_states show_sensors_linked_controller show_sensors_selected_objects show_separate_color show_shaded show_shapekeys show_size show_sliders show_smooth_edges show_speakers show_splash show_stable show_state_panel show_statvis show_stretch show_strip_curves show_summary show_sync_view show_syntax_highlight show_texture show_texture_space show_textured_solid show_textures show_thumbnails show_tiny_markers show_title_safe show_tooltips show_tooltips_python show_tracer show_track_path show_transforms show_transparent show_unborn show_uv_local_view show_uvedit show_velocity show_view_name show_viewport show_visualization show_waveform show_weight show_wire show_word_wrap show_worlds show_x_ray shrink shrink_max shrink_min shrink_speed shrinkwrap_type sigma_color sigma_space simplify_ao_sss simplify_child_particles simplify_rate simplify_refsize simplify_shadow_samples simplify_subdivision simplify_transition simplify_viewport simulation_rate simulation_scale sine single_axis_number size size_factor size_min size_random size_source size_x size_y skin_root skin_vertices sky_blend sky_blend_type sky_color_space sky_exposure sky_type slerp(other=,factor=); slider_max slider_min slip_type slope slope_max slow_parent_offset slurph small_caps_scale smoke smoke_data_type smoke_type smokeflow smooth smooth_stroke_factor smooth_view smudge_strength snap_element snap_node_element snap_target snap_type socket_value_update(context); soft_body soft_max soft_min solid_lights solid_radius solver sort_method sound_directory sound_strips sound_strips_selected sounds source space space_character space_data space_line space_list space_type space_word spaces spacing spatial_size speaker speakers specular specular_alpha specular_color specular_color_factor specular_factor specular_hardness specular_intensity specular_ior specular_ramp specular_ramp_blend specular_ramp_factor specular_ramp_input specular_shader specular_slope specular_toon_size specular_toon_smooth specularity speed speed_factor speed_max speed_min speed_of_sound speed_scale sphereInsideFrustum splines split(percentage=0.0,align=False); split_angle spot_blend spot_size spotblend spotsize spread spread_speed spring_damping spring_force spring_frames spring_length square squash squash_frequency srna stabilization stabilize2d stamp_background stamp_font_size stamp_foreground stamp_note_text standard_derivation star_settings star_tip_count startGame(blend=); startSound start_cap start_point start_position_object start_position_x start_position_y start_time state states states_initial states_visible statistics(); status step step_count step_height step_max step_method step_min step_size steps stereo stereo_eye_separation stereo_mode stickiness sticky sticky_add sticky_remove sticky_select_mode stiff_viscosity stiffness still_frame stl stop(); stopAction(layer=0); stopAll stopSound strand streaks stream_index strength strip_elem_from_frame(frame=); strip_time strips strips_selected strobe stroke_method strokes structs structural_stiffness structural_stiffness_max stucci_type subdivision_type subframes subject subjects subsurf_levels subsurface_samples subsurface_scattering subtarget subtype summary sun_brightness sun_direction sun_intensity sun_size support_display_space_shader(scene=); surface_format surface_smooth surface_subdivisions surface_type suspend suspendDynamics(); suspended svg swap(other); sync_mode syntax_builtin syntax_comment syntax_numbers syntax_special syntax_string system system_rotation tab_width tag(value=); tag_redraw(); tag_update(); tail tail_local tail_radius tangent_factor tangent_phase tap taper_object target targetProperty target_count target_space targets temperature template_ID(data=,property=,new='',open='',unlink=''); template_ID_preview(data=,property=,new='',open='',unlink='',rows=0,cols=0); template_any_ID(data=,property=,type_property=,text='',text_ctxt='',translate=True); template_color_picker(data=,property=,value_slider=False,lock=False,lock_luminosity=False,cubic=False); template_color_ramp(data=,property=,expand=False); template_color_wheel template_colormanaged_view_settings(data=,property=); template_colorspace_settings(data=,property=); template_component_menu(data=,property=,name=''); template_constraint(data=); template_curve_mapping(data=,property=,type='NONE',levels=False,brush=False,use_negative_slope=False); template_edit_mode_selection(); template_header template_header_3D(); template_histogram(data=,property=); template_icon_view(data=,property=); template_image(data=,property=,image_user=,compact=False); template_image_layers(image,image_user=); template_image_settings(image_settings=,color_management=False); template_keymap_item_properties(item=); template_layers(data=,property=,used_layers_data=,used_layers_property=,active_layer=); template_list(listtype_name=,list_id='',dataptr=,propname=,active_dataptr=,active_propname=,rows=5,maxrows=5,type='DEFAULT',columns=9); template_marker(data=,property=,clip_user=,track=,compact=False); template_modifier(data=); template_movieclip(data=,property=,clip_user=); template_node_link(ntree=,node=,socket=); template_node_socket(color=(0.0,0.0,0.0,1.0); template_node_view(ntree=,node=,socket=); template_operator_search(); template_palette(data=,property=,color=False); template_path_builder(data=,property=,root,text='',text_ctxt='',translate=True); template_preview(id=,show_buttons=True,parent=None,slot=None,preview_id=''); template_reports_banner(); template_running_jobs(); template_texture_user(); template_track(data=,property=); template_vectorscope template_waveform(data=,property=); temporary_directory tessface_uv_textures tessface_vertex_colors tessfaces test_break(); test_type tex texco_mesh texface_convert texspace_location texspace_size text_boxes text_editor text_hi text_sel texts texture_angle_source_no_random texture_angle_source_random texture_collection_rate texture_context texture_coords texture_coords_object texture_directory texture_factor texture_mapping texture_mesh texture_mode texture_nabla texture_name texture_overlay_alpha texture_sample_bias texture_slot texture_slots texture_time_out texture_type texture_user textures tface theme_area themes thickness thickness_clamp thickness_inner thickness_outer thickness_vertex_group threads threads_mode threshold threshold_neighbor threshold_neighbour tile tile_order tile_x tile_y tiles_x tiles_y tilexrep tileyrep tilt_interpolation timeOffset timeTaken time_delta time_duration time_factor time_mode time_offset time_scale time_step time_tweak timecode timecode_style timeline timeline_markers timestep tip_size tip_width to_2d(); to_3d(); to_3x3(); to_4d(); to_4x4(); to_axis_angle(); to_euler(); 
----3--------------------------------------------------------------------
to_matrix(); to_max_x to_max_y to_max_z to_mesh(mesh=); to_mesh(scene=,apply_modifiers=,settings=,calc_tessface=True,calc_undeformed=False); to_min_x to_min_y to_min_z to_node to_property to_quaternion(); to_scale(); to_socket to_track_quat(track=,up=); to_translation(); to_tuple(precision=-1); toggleProperty tolerance tonemap_type tool_settings torque total_edge_sel total_face_sel total_levels total_vert_sel tracer_particles track_axis track_name track_object tracking tracking_object tracks tracks_draw_size tracks_draw_type trail_count transform(matrix=,filter=None); transform(matrix); transformUV transform_channel transform_orientation transform_space transform_type transition_strip transition_strips transition_strips_selected translate(vec); translate_start_x translate_start_y translation translation_context translation_unit translucency translucency_factor transmission_bounces transmission_color transmission_color_factor transmission_samples transparency_method transparent transparent_max_bounces transparent_min_bounces transpose(); transposed(); tree_type triggered turbidity turbulence turbulence_depth turbulence_influence turbulence_scale turbulence_strength turn_speed turnspeed tweak tweak_duplicate tweak_threshold twist_mode twist_smooth type type_info u u2 ui_styles ui_type unbind_display_space_shader(); underline_height underline_position undistort undo_memory_limit undo_steps unified_paint_settings(parent=,context); unit unit_settings unit_test_compare(mesh=None); units unlink(); unlink_selected unpack(method='USE_LOCAL'); unprojected_radius unspill_blue unspill_green unspill_red up_axis updateTexture update_autoflags(data=); update_data_paths update_from_editmode(); update_memory_stats(memory_used=0.0,memory_peak=0.0); update_method update_period update_progress(progress=); update_result(result=); update_script_node(node=None); update_stats(stats=,info=); update_tag(refresh=set(); use use3D useAllKeys useChildren useContinue useDisplayMesh useHighPriority useIpoAdd useIpoAsForce useIpoLocal useLocalAngV useLocalDLoc useLocalDRot useLocalForce useLocalLinV useLocalTorque useMaterial useNegPulseMode useOcclusion usePhysicsMesh usePosPulseMode usePropBody usePulseCollision usePulseFocus useRecursion useRestart useViewport useXRay use_16bit_textures use_2d_force use_2d_stabilization use_3d_position use_3d_tracking use_absolute use_absolute_alpha use_absolute_path_time use_absorption use_accumulate use_active_clip use_activity_culling use_actor use_adaptive_domain use_adaptive_space use_add use_add_linear_velocity use_additive use_advanced_hair use_airbrush use_all_events use_all_faces use_all_keys use_all_states use_all_z use_alpha use_alpha_preview use_always_true use_ambient_occlusion use_anchor use_angular_limit_x use_angular_limit_y use_angular_limit_z use_animated_influence use_animated_mesh use_animated_time use_animated_time_cyclic use_animation use_animation_record use_anisotropic_friction use_antialias_z use_antialiasing use_apply_on_spline use_as_speed use_atmosphere use_audio use_audio_scrub use_audio_sync use_auto_blend use_auto_clip_end use_auto_clip_start use_auto_ik use_auto_keying use_auto_merge_keyframes use_auto_normalize use_auto_perspective use_auto_refresh use_auto_render use_auto_save_temporary_files use_auto_smooth use_auto_start use_auto_step use_auto_texspace use_auto_update use_auto_velocity use_autoscale use_avoid use_avoid_collision use_backface_culling use_bake_antialiasing use_bake_clear use_bake_lores_mesh use_bake_multires use_bake_normalize use_bake_selected_to_active use_bake_to_vertex_color use_beauty_drawing use_bending_constraints use_bezier_u use_bezier_v use_blender_units use_blue_channel use_bokeh use_bold use_bone_envelopes use_bone_head use_bone_object_action use_bone_sketching use_border use_boundary use_box_clip use_brute use_cache use_calculate_alpha use_camera_clip use_camera_lock_parent use_cast_approximate use_cast_buffer_shadows use_cast_shadows use_cast_shadows_only use_chain_offset use_checker_even use_checker_odd use_children use_cineon_log use_clamp use_clamp_x use_clamp_y use_climb use_clip use_clone_layer use_closetip use_cluster_rigid_to_softbody use_cluster_soft_to_softbody use_collapse_triangulate use_collision use_collision_bounds use_collision_compound use_color_balance use_color_management use_color_ramp use_color_unpremultiply use_compositing use_compound use_connect use_constant_offset use_continue_last_frame use_crease use_crop use_crop_size use_crop_to_border use_cubic use_curve_follow use_curve_radius use_curved use_curves use_custom_color use_custom_icon use_customdata_edge_bevel use_customdata_edge_crease use_customdata_vertex_bevel use_cyclic use_cyclic_offset use_cyclic_u use_cyclic_v use_dead use_debug use_default_blue_channel use_default_brute use_default_fade use_default_green_channel use_default_interpolate use_default_normalization use_default_red_channel use_deform use_deform_bounds use_deform_delay use_deform_only use_deform_preserve_volume use_deinterlace use_deprecation_warnings use_derivative_map use_desktop use_diagnose use_die_on_collision use_diffuse use_diffuse_ramp use_directional_menus use_disk_cache use_display_lists use_dissolve use_dissolve_boundaries use_dissolve_log use_dissolve_smoke use_dissolve_smoke_log use_dither use_drag_immediately use_drip use_drops use_dry_log use_drying use_dupli_faces_scale use_dupli_frames_speed use_dupli_vertices_rotation use_duplicate_action use_duplicate_armature use_duplicate_curve use_duplicate_fcurve use_duplicate_lamp use_duplicate_material use_duplicate_mesh use_duplicate_metaball use_duplicate_particle use_duplicate_surface use_duplicate_text use_duplicate_texture use_dynamic_bind use_dynamic_rotation use_edge_angle use_edge_collision use_edge_cut use_edge_enhance use_edge_sharp use_edge_to_edge use_edges use_edit_all use_emit_random use_emitter_deflect use_emulate_numpad use_endpoint_u use_endpoint_v use_enter_edit_mode use_entire_array use_envelope_multiply use_environment_light use_envmaps use_estimate_matrix use_etch_autoname use_etch_overdraw use_etch_quick use_even_distribution use_even_divisions use_even_offset use_external use_external_shadows use_extra_recalc_data use_extra_recalc_object use_extreme_alpha use_face_collision use_face_texture use_face_texture_alpha use_factor_density use_fade_time use_falloff use_falloff_curve use_fast_edit use_feather use_fh_normal use_fh_paralel_axis use_fields use_fields_still use_file_compression use_file_extension use_fill use_fill_caps use_fill_deform use_filter use_filter_blender use_filter_case_sensitive use_filter_complete use_filter_files use_filter_folder use_filter_font use_filter_image use_filter_movie use_filter_script use_filter_size_min use_filter_sound use_filter_text use_find_all use_find_wrap use_fit use_fixed_location use_flare_mode use_flight use_flip_axis use_flip_normals use_flip_x use_flip_y use_float use_floats use_foam use_force use_force_distance use_frame_drop use_frame_end use_frame_rate use_frame_start use_free_image_textures use_free_unused_nodes use_freestyle use_from_dupli use_from_original use_frontface use_full_oversampling use_full_resolution use_full_sample use_game_engine use_gamma_correction use_generated_flo use_generated_float use_ghost use_global_coords use_global_dupli use_global_pivot use_global_scene use_global_undo use_glsl_color_management use_glsl_extra_textures use_glsl_lights use_glsl_nodes use_glsl_ramps use_glsl_shaders use_glsl_shadows use_goal use_gpu_mipmap use_gravity use_grayscale_preview use_grease_pencil_sessions use_grease_pencil_simplify_stroke use_grease_pencil_smooth_stroke use_green_channel use_group_count use_group_pick_random use_group_restrict use_groupnode_buffer use_guide_path_add use_guide_path_weight use_hair_bspline use_hair_dynamics use_halo use_hidden_preview use_high_resolution use_ik_limit_x use_ik_limit_y use_ik_limit_z use_ik_linear_control use_ik_rotation_control use_image_override use_image_pin use_in_air use_incremental_displace use_indirect_light use_influence use_inherit_rotation use_inherit_scale use_initial_rest_length use_initial_velocity use_insertkey_xyz_to_rgb use_instances use_international_fonts use_interpolation use_inverse_smooth_pressure use_invert_sort use_italic use_jitter use_keep_above_surface use_keyed_timing use_keyframe_insert_auto use_keyframe_insert_available use_keyframe_insert_keyingset use_keyframe_insert_needed use_land use_level use_library_path use_light_cache use_light_group_exclusive use_light_group_local use_limit_x use_limit_y use_limit_z use_line use_lines use_linked_collision use_live_edit use_live_unwrap use_load_ui use_local use_local_angular_velocity use_local_coords use_local_force use_local_linear_velocity use_local_linear_velocity? use_local_location use_local_rotation use_local_torque use_location use_location_x use_location_y use_location_z use_locked_size use_loose use_lossless_output use_manipulator_rotate use_manipulator_scale use_manipulator_translate use_manual_calibration use_map_alpha use_map_ambient use_map_blend use_map_clump use_map_color use_map_color_diffuse use_map_color_emission use_map_color_reflection use_map_color_spec use_map_color_transmission use_map_damp use_map_density use_map_diffuse use_map_displacement use_map_emission use_map_emit use_map_field use_map_gravity use_map_hardness use_map_horizon use_map_kink use_map_length use_map_life use_map_mirror use_map_normal use_map_raymir use_map_reflect use_map_rough use_map_scatter use_map_shadow use_map_size use_map_specular use_map_taper use_map_time use_map_translucency use_map_velocity use_map_warp use_map_zenith_down use_map_zenith_up use_marker_sync use_mask use_match_case use_material use_material_detect use_material_physics_fh use_max use_max_distance use_max_x use_max_y use_max_z use_memory_cache use_merge_vertices use_merge_vertices_cap use_mesh_automerge use_min use_min_distance use_min_x use_min_y use_min_z use_mipmap use_mipmap_gauss use_mipmaps use_mirror_merge use_mirror_topology use_mirror_u use_mirror_v use_mirror_vertex_groups use_mirror_x use_mirror_y use_mist use_modifier_stack use_module use_mono use_motion_blur use_motion_extrapolate use_mouse_continuous use_mouse_depth_cursor use_mouse_depth_navigate use_mouse_emulate_3_button use_mouse_mmb_paste use_mouse_over_open use_multi_modifier use_multipaint use_multiple_springs use_multiply_size_mass use_mute_footage use_negative use_negative_direction use_negative_frames use_negative_volume use_nla use_node_format use_nodes use_normal use_normal_calculate use_normal_falloff use_normal_flip use_normal_map use_normal_x use_normal_y use_normal_z use_normalization use_normalized use_normals use_object_color use_object_coords use_object_offset use_object_screw_offset use_obstacle_create use_occlude use_occlude_geometry use_occlusion use_occlusion_culling use_offset use_offset_pressure use_on_land use_onion_skinning use_only_boost use_only_selected_curves_handles use_only_selected_keyframe_handles use_only_shadow use_only_vertices use_opencl use_original_normal use_outflow use_output_a use_output_b use_outside use_overlay_lock use_overwrite use_own_layer use_paint_erase use_paint_image use_paint_mask use_paint_mask_vertex use_paint_sculpt use_paint_vertex use_paint_weight use_parent_particles use_particle_kill use_particle_radius use_pass_ambient_occlusion use_pass_color use_pass_combined use_pass_diffuse use_pass_diffuse_color use_pass_diffuse_direct use_pass_diffuse_indirect use_pass_emit use_pass_environment use_pass_glossy_color use_pass_glossy_direct use_pass_glossy_indirect use_pass_indirect use_pass_material_index use_pass_mist use_pass_normal use_pass_object_index use_pass_reflection use_pass_refraction use_pass_shadow use_pass_specular use_pass_subsurface_color use_pass_subsurface_direct use_pass_subsurface_indirect use_pass_transmission_color use_pass_transmission_direct use_pass_transmission_indirect use_pass_uv use_pass_vector use_pass_z use_path use_path_follow use_persistent use_pin_cloth use_pin_id use_pivot_point_align use_pixel_size use_placeholder use_plane_trim use_play_3d_editors use_play_animation_editors use_play_clip_editors use_play_image_editors use_play_node_editors use_play_properties_editors use_play_sequence_editors use_play_top_left_3d_editor use_positive_direction use_predict use_premultiply use_preserve_length use_preserve_root use_preserve_shape use_pressure_jitter use_pressure_size use_pressure_spacing use_pressure_strength use_preview use_preview_alpha use_preview_images use_preview_range use_primary_overlay use_priority use_progressive_refine use_project_x use_project_y use_project_z use_projector use_proportional_edit_mask use_proportional_edit_objects use_proximity_project use_proximity_ramp_alpha use_proxy use_proxy_custom_directory use_proxy_custom_file use_puff_volume use_pulse use_pulse_false_level use_pulse_true_level use_quality_normals use_quick_cache use_radial_max use_radial_min use_radiosity use_radius use_radius_as_size use_rake use_random_order use_random_rotation use_ray_shadow_bias use_raytrace use_react_multiple use_react_start_end use_realtime_update use_record_with_nla use_red_channel use_relative use_relative_location use_relative_offset use_relative_parent use_relative_paths use_remove use_remove_disconnected use_render_adaptive use_render_emitter use_render_undistorted use_repeat use_replace use_replace_display_mesh use_replace_physics_mesh use_restore_mesh use_restrict_animation_updates use_restricted_range use_reverse use_reverse_frames use_rim use_ring use_root use_root_coords use_rotate_45 use_rotate_around_active use_rotate_from_normal use_rotation use_rotation_dupli use_rotation_x use_rotation_y use_rotation_z use_rotations use_save_buffers use_save_preview_images use_scale_dupli use_scale_x use_scale_y use_scale_z use_scripts_auto_execute use_seam use_secondary_overlay use_self use_self_collision use_self_effect use_self_intersection_check use_separate use_sequencer use_sequencer_gl_preview use_sequencer_gl_render use_servo_limit_x use_servo_limit_y use_servo_limit_z use_sewing_springs use_shaded use_shadeless use_shadow use_shadow_layer use_shadows use_shape_key_edit_mode use_shape_match use_shrink use_simplify use_simplify_triangulate use_simplify_viewport use_single_layer use_size use_size_deflect use_sky use_sky_blend use_sky_paper use_sky_real use_sleep use_slow_parent use_small_caps use_smooth use_smooth_emitter use_smooth_shade use_smooth_stroke use_smudge use_snap use_snap_align_rotation use_snap_peel_object use_snap_project use_snap_self use_snap_to_pixels use_soft use_solid use_sound_3d use_space use_space_attenuation use_specular use_specular_ramp use_speed_vectors use_spray use_spread use_sss use_stabilize_rotation use_stamp use_stamp_camera use_stamp_date use_stamp_filename use_stamp_frame use_stamp_lens use_stamp_marker use_stamp_note use_stamp_render_time use_stamp_scene use_stamp_sequencer_strip use_stamp_time use_star use_stars use_stencil_layer use_sticky use_stiff_quads use_stiffness_scale use_still_frame use_straight_alpha_output use_strand use_strand_primitive use_stretch use_stretch_u use_stretch_v use_stroke_endpoints use_subsurf_uv use_surface_diffuse use_surface_noobs use_symmetry_feather use_symmetry_x use_symmetry_y use_symmetry_z use_tabs_as_spaces use_tail use_tangent_shading use_tap use_target_z use_targets use_text_antialiasing use_texture use_textured_fonts use_textures use_threaded use_tiles use_time_offset use_time_override use_transform use_transform_limit use_translate_interface use_translate_tooltips use_translation use_transparency use_transparent_shadows use_tripod_solver use_turbulence use_two_pass use_umbra use_underline use_uniform_scale use_unspill use_uv_as_generated use_uv_project use_uv_sculpt use_uv_select_sync use_variable_size use_velocity_alpha use_velocity_color use_velocity_depth use_velocity_length use_vertex_buffer_objects use_vertex_color_light use_vertex_color_paint use_vertex_groups use_vertex_normal use_view_as_render use_viewer_border use_viscoelastic_springs use_visible use_visual_keying use_volume_preserve use_wave_open_border use_weight_color_range use_whole_group use_wrap use_x use_x_ray use_x_symmetry use_y use_y_stretch use_y_symmetry use_z use_z_symmetry use_zbuffer use_zmask use_zoom_to_mouse use_ztransp used_states user_clear－ user_interface user_preferences userjit users_dupli_group users_group users_id users_logic users_material users_object_modifier users_scene uv uv1 uv2 uv4 uv_editor uv_layer uv_layer_clone uv_layer_clone_index uv_layer_stencil uv_layer_stencil_index uv_layers uv_map uv_on_emitter(modifier); uv_on_emitter(modifier=,particle=,particle_no=0,uv_no=0); uv_raw uv_relax_method uv_sculpt uv_sculpt_all_islands uv_sculpt_lock_borders uv_sculpt_tool uv_select_mode uv_texture_clone uv_texture_clone_index uv_texture_stencil uv_texture_stencil_index uv_textures uvedit_aspect(object=); v v1 v2 v4 validate validate_material_indices(); value value_max value_min value_offset value_sliders variables vector vector_type vectorscope_alpha vel_damping velocity velocity_factor velocity_max velocity_min velocity_radius velocity_ramp velocity_strength verify(); vert_select_inverse vertex vertex_cache_space vertex_colors vertex_group vertex_group_a vertex_group_b vertex_group_bending vertex_group_clump vertex_group_field vertex_group_goal vertex_group_kink vertex_group_length vertex_group_mass vertex_group_rotation vertex_group_roughness_1 vertex_group_roughness_2 vertex_group_roughness_end vertex_group_self_collisions vertex_group_shrink vertex_group_size vertex_group_spring vertex_group_structural_stiffness vertex_group_tangent vertex_group_velocity vertex_group_weight vertex_groups vertex_index vertex_normal vertex_paint vertex_paint_object vertex_select vertex_size vertex_tool vertices vertices_raw verts verts_per_poly video_bitrate view view2d_grid_spacing_min view_3d view_axis view_camera_offset view_camera_zoom view_center view_distance view_draw(context=None); view_frame(scene=None); view_location view_matrix view_perspective view_rotate_method view_rotation view_settings view_sliders view_to_region(x=,y=,clip=True); view_type view_update(context=None); view_zoom_axis view_zoom_method viewpoint_object viewport_display_mode viewport_shade virtual_parents viscosity_base viscosity_exponent visibility visible visible_bases visible_bones visible_objects visible_pose_bones volume volume_bounces volume_homogeneous_sampling volume_initialization volume_max volume_max_steps volume_maximum volume_min volume_minimum volume_samples volume_step_size vortex vorticity voxel_data w wander warp warp_factor wave_alignment wave_clamp wave_damping wave_direction wave_factor wave_scale wave_scale_min wave_smoothness wave_speed wave_spring wave_timescale wave_type waveform_alpha waveform_mode wcol_box wcol_list_item wcol_menu wcol_menu_back wcol_menu_item wcol_num wcol_numslider wcol_option wcol_progress wcol_pulldown wcol_radio wcol_regular wcol_scroll wcol_state wcol_text wcol_toggle wcol_tool wcol_tooltip weight(index=); weight_1 weight_2 weight_3 weight_4 weight_color_range weight_from_bones weight_interpolation weight_paint  weight_softbody weld_threshold wheel_scroll_lines white_level widget widget_label width width_fade width_hidden wind wind_velocity window window_draw_method window_manager window_managers window_sliders windows wire wire_select wood_type worldAngularVelocity worldLinearVelocity worldOrientation worldPosition worldScale worldTransform world_to_camera worlds wrap_axis wrap_method write(text=); x x3d x_axis xz_scale_mode y y_axis yield_ratio z z_axis z_direction z_scale zenith_color zenith_down_factor zenith_up_factor zero(); zsort



xX xY xZ M03 yX yY yZ M13 zX zY zZ M23 LX zX zY zZ
------------
def  后来增加的():
lod_levels default loop_start use_freestyle_mark lines shadow_frustum_size show_shadow_box shadow_frustum_size cast_shadow use_multiple_importance_sampling icon_id icon_pixels icon_pixels_float icon_size image_pixels image_pixels_float image_size is_icon_custom is_image_custom previews 


----MY--------
fvp3loc fvp3scale fvp3euler fvp4q
----------共用-----------------------------------------------
--classbpy.types.ID
copy();
is_library_indirect
is_updated
is_updated_data
library
name
tag
use_fake_user
user_clear();
users

--classbpy.types.bpy_struct-----------------------------------
as_pointer();
driver_add(path,index=-1);
driver_remove(path,index=-1);
get(key,default=None);
is_property_hidden(property=);
is_property_set(property=);
items();
keyframe_delete();
keyframe_insert();
keys();
path_from_id(property='');
path_resolve(path,coerce=True);
property_unset(property=);
type_recast();
values();
id_data


----bpy.ops-------------------------------------------------------------
bpy.ops.action.clean(threshold=0.001);
bpy.ops.action.clickselect(extend=False,column=False,channel=False);
bpy.ops.action.delete();
bpy.ops.action.duplicate();
bpy.ops.action.duplicate_move(ACTION_OT_duplicate=None,TRANSFORM_OT_transform=None);
bpy.ops.action.extrapolation_type(type='CONSTANT');
bpy.ops.action.frame_jump();
bpy.ops.action.handle_type(type='FREE');
bpy.ops.action.interpolation_type(type='CONSTANT');
bpy.ops.action.keyframe_insert(type='ALL');
bpy.ops.action.keyframe_type(type='KEYFRAME');
bpy.ops.action.markers_make_local();
bpy.ops.action.paste(offset='START',merge='MIX');
bpy.ops.action.previewrange_set();
bpy.ops.action.sample();
bpy.ops.action.select_all_toggle(invert=False);
bpy.ops.action.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True,axis_range=False);
bpy.ops.action.select_column(mode='KEYS');
bpy.ops.action.select_leftright(mode='CHECK',extend=False);
bpy.ops.action.select_less();
bpy.ops.action.select_linked();
bpy.ops.action.select_more();
bpy.ops.action.snap(type='CFRA');
bpy.ops.action.view_all();
bpy.ops.action.view_selected();
bpy.ops.anim.change_frame(frame=0,snap=False);
bpy.ops.anim.channels_clean_empty();
bpy.ops.anim.channels_click(extend=False,children_only=False);
bpy.ops.anim.channels_collapse(all=True);
bpy.ops.anim.channels_delete();
bpy.ops.anim.channels_editable_toggle(mode='TOGGLE',type='PROTECT');
bpy.ops.anim.channels_expand(all=True);
bpy.ops.anim.channels_fcurves_enable();
bpy.ops.anim.channels_find(query='Query');
bpy.ops.anim.channels_group(name='New Group');
bpy.ops.anim.channels_move(direction='DOWN');
bpy.ops.anim.channels_rename();
bpy.ops.anim.channels_select_all_toggle(invert=False);
bpy.ops.anim.channels_select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.anim.channels_setting_disable(mode='DISABLE',type='PROTECT');
bpy.ops.anim.channels_setting_enable(mode='ENABLE',type='PROTECT');
bpy.ops.anim.channels_setting_toggle(mode='TOGGLE',type='PROTECT');
bpy.ops.anim.channels_ungroup();
bpy.ops.anim.clear_useless_actions(only_unused=True);
bpy.ops.anim.driver_button();
bpy.ops.anim.driver_button_add(all=True);
bpy.ops.anim.driver_button_remove(all=True);
bpy.ops.anim.keyframe_clear_button(all=True);
bpy.ops.anim.keyframe_clear_v3d();
bpy.ops.anim.keyframe_delete_button(all=True);
bpy.ops.anim.keyframe_delete_v3d();
bpy.ops.anim.keyframe_insert(type='DEFAULT',confirm_success=True);
bpy.ops.anim.keyframe_insert_button(all=True);
bpy.ops.anim.keyframe_insert_menu(type='DEFAULT',confirm_success=False,always_prompt=False);
bpy.ops.anim.keying_set_active_set(type='DEFAULT');
bpy.ops.anim.keying_set_add();
bpy.ops.anim.keying_set_export(filepath='',filter_folder=True,filter_text=True,filter_python=True);
bpy.ops.anim.keying_set_path_add();
bpy.ops.anim.keying_set_path_remove();
bpy.ops.anim.keying_set_remove();
bpy.ops.anim.keyingset_button_add(all=True);
bpy.ops.anim.keyingset_button_remove();
bpy.ops.anim.paste_driver_button();
bpy.ops.anim.previewrange_clear();
bpy.ops.anim.previewrange_set(xmin=0,xmax=0,ymin=0,ymax=0);
bpy.ops.anim.update_animated_transform_constraints(use_convert_to_radians=True);
bpy.ops.armature.align();
bpy.ops.armature.armature_layers(layers=T32False);
bpy.ops.armature.autoside_names(type='XAXIS');
bpy.ops.armature.bone_layers(layers=T32False);
bpy.ops.armature.bone_primitive_add(name='Bone');
bpy.ops.armature.calculate_roll(type='X',axis_flip=False,axis_only=False);
bpy.ops.armature.click_extrude();
bpy.ops.armature.delete();
bpy.ops.armature.duplicate();
bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate=None,TRANSFORM_OT_translate=None);
bpy.ops.armature.extrude(forked=False);
bpy.ops.armature.extrude_forked(ARMATURE_OT_extrude=None,TRANSFORM_OT_translate=None);
bpy.ops.armature.extrude_move(ARMATURE_OT_extrude=None,TRANSFORM_OT_translate=None);
bpy.ops.armature.fill();
bpy.ops.armature.flip_names();
bpy.ops.armature.hide(unselected=False);
bpy.ops.armature.layers_show_all(all=True);
bpy.ops.armature.merge(type='WITHIN_CHAIN');
bpy.ops.armature.parent_clear(type='CLEAR');
bpy.ops.armature.parent_set(type='CONNECTED');
bpy.ops.armature.reveal();
bpy.ops.armature.select_all(action='TOGGLE');
bpy.ops.armature.select_hierarchy(direction='PARENT',extend=False);
bpy.ops.armature.select_less();
bpy.ops.armature.select_linked(extend=False);
bpy.ops.armature.select_mirror(only_active=False,extend=False);
bpy.ops.armature.select_more();
bpy.ops.armature.select_similar(type='LENGTH',threshold=0.1);
bpy.ops.armature.separate();
bpy.ops.armature.shortest_path_pick();
bpy.ops.armature.split();
bpy.ops.armature.subdivide(number_cuts=1);
bpy.ops.armature.switch_direction();
bpy.ops.boid.rule_add(type='GOAL');
bpy.ops.boid.rule_del();
bpy.ops.boid.rule_move_down();
bpy.ops.boid.rule_move_up();
bpy.ops.boid.state_add();
bpy.ops.boid.state_del();
bpy.ops.boid.state_move_down();
bpy.ops.boid.state_move_up();
bpy.ops.brush.active_index_set(mode='',index=0);
bpy.ops.brush.add();
bpy.ops.brush.curve_preset(shape='SMOOTH');
bpy.ops.brush.reset();
bpy.ops.brush.scale_size(scalar=1.0);
bpy.ops.brush.stencil_control(mode='TRANSLATION',texmode='PRIMARY');
bpy.ops.brush.stencil_fit_image_aspect(use_repeat=True,use_scale=True,mask=False);
bpy.ops.brush.stencil_reset_transform(mask=False);
bpy.ops.brush.uv_sculpt_tool_set(tool='PINCH');
bpy.ops.buttons.directory_browse(directory='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=False,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.buttons.file_browse(filepath='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=False,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.buttons.toolbox();
bpy.ops.camera.preset_add(remove_active=False,name='',use_focal_length=False);
bpy.ops.clip.add_marker(location=(0.0,0.0);
bpy.ops.clip.add_marker_at_click();
bpy.ops.clip.add_marker_move(CLIP_OT_add_marker=None,TRANSFORM_OT_translate=None);
bpy.ops.clip.add_marker_slide(CLIP_OT_add_marker=None,TRANSFORM_OT_translate=None);
bpy.ops.clip.apply_solution_scale(distance=0.0);
bpy.ops.clip.bundles_to_mesh();
bpy.ops.clip.camera_preset_add(remove_active=False,name='',use_focal_length=True);
bpy.ops.clip.change_frame(frame=0);
bpy.ops.clip.clean_tracks(frames=0,error=0.0,action='SELECT');
bpy.ops.clip.clear_solution();
bpy.ops.clip.clear_track_path(action='REMAINED',clear_active=False);
bpy.ops.clip.constraint_to_fcurve();
bpy.ops.clip.tracks();
bpy.ops.clip.create_plane_track();
bpy.ops.clip.cursor_set(location=(0.0,0.0);
bpy.ops.clip.delete_marker();
bpy.ops.clip.delete_proxy();
bpy.ops.clip.delete_track();
bpy.ops.clip.detect_features(placement='FRAME',margin=16,threshold=0.5,min_distance=120);
bpy.ops.clip.disable_markers(action='DISABLE');
bpy.ops.clip.dopesheet_select_channel(location=(0.0,0.0),extend=False);
bpy.ops.clip.dopesheet_view_all();
bpy.ops.clip.frame_jump(position='PATHSTART');
bpy.ops.clip.graph_center_current_frame();
bpy.ops.clip.graph_delete_curve();
bpy.ops.clip.graph_delete_knot();
bpy.ops.clip.graph_disable_markers(action='DISABLE');
bpy.ops.clip.graph_select(location=(0.0,0.0),extend=False);
bpy.ops.clip.graph_select_all_markers(action='TOGGLE');
bpy.ops.clip.graph_select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.clip.graph_view_all();
bpy.ops.clip.hide_tracks(unselected=False);
bpy.ops.clip.hide_tracks_clear();
bpy.ops.clip.join_tracks();
bpy.ops.clip.keyframe_delete();
bpy.ops.clip.keyframe_insert();
bpy.ops.clip.lock_tracks(action='LOCK');
bpy.ops.clip.mode_set(mode='TRACKING');
bpy.ops.clip.open(directory='',files=None,filter_blender=False,filter_backup=False,filter_image=True,filter_movie=True,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.clip.paste_tracks();
bpy.ops.clip.prefetch();
bpy.ops.clip.properties();
bpy.ops.clip.rebuild_proxy();
bpy.ops.clip.refine_markers(backwards=False);
bpy.ops.clip.reload();
bpy.ops.clip.select(extend=False,location=(0.0,0.0);
bpy.ops.clip.select_all(action='TOGGLE');
bpy.ops.clip.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.clip.select_circle(x=0,y=0,radius=1,gesture_mode=0);
bpy.ops.clip.select_grouped(group='ESTIMATED');
bpy.ops.clip.select_lasso(path=None,deselect=False,extend=True);
bpy.ops.clip.set_axis(axis='X');
bpy.ops.clip.set_center_principal();
bpy.ops.clip.set_origin(use_median=False);
bpy.ops.clip.set_plane(plane='FLOOR');
bpy.ops.clip.set_scale(distance=0.0);
bpy.ops.clip.set_scene_frames();
bpy.ops.clip.set_solution_scale(distance=0.0);
bpy.ops.clip.set_solver_keyframe(keyframe='KEYFRAME_A');
bpy.ops.clip.set_viewport_background();
bpy.ops.clip.setup_tracking_scene();
bpy.ops.clip.slide_marker(offset=(0.0,0.0);
bpy.ops.clip.slide_plane_marker();
bpy.ops.clip.solve_camera();
bpy.ops.clip.stabilize_2d_add();
bpy.ops.clip.stabilize_2d_remove();
bpy.ops.clip.stabilize_2d_select();
bpy.ops.clip.stabilize_2d_set_rotation();
bpy.ops.clip.tools();
bpy.ops.clip.track_color_preset_add(remove_active=False,name='');
bpy.ops.clip.track_color();
bpy.ops.clip.track_markers(backwards=False,sequence=False,clip='');
bpy.ops.clip.track_settings_as_default();
bpy.ops.clip.track_to_empty();
bpy.ops.clip.tracking_object_new();
bpy.ops.clip.tracking_object_remove();
bpy.ops.clip.tracking_settings_preset_add(remove_active=False,name='');
bpy.ops.clip.view_all(fit_view=False);
bpy.ops.clip.view_ndof();
bpy.ops.clip.view_pan(offset=(0.0,0.0);
bpy.ops.clip.view_selected();
bpy.ops.clip.view_zoom(factor=0.0);
bpy.ops.clip.view_zoom_in(location=(0.0,0.0);
bpy.ops.clip.view_zoom_out(location=(0.0,0.0);
bpy.ops.clip.view_zoom_ratio(ratio=0.0);
bpy.ops.cloth.preset_add(remove_active=False,name='');
bpy.ops.console.autocomplete();
bpy.ops.console.banner();
bpy.ops.console.clear(scrollback=True,history=False);
bpy.ops.console.clear_line();
bpy.ops.console.copy();
bpy.ops.console.as_script();
bpy.ops.console.delete(type='NEXT_CHARACTER');
bpy.ops.console.execute(interactive=False);
bpy.ops.console.history_append(text='',current_character=0,remove_duplicates=False);
bpy.ops.console.history_cycle(reverse=False);
bpy.ops.console.indent();
bpy.ops.console.insert(text='');
bpy.ops.console.language(language='');
bpy.ops.console.move(type='LINE_BEGIN');
bpy.ops.console.paste();
bpy.ops.console.scrollback_append(text='',type='OUTPUT');
bpy.ops.console.select_set();
bpy.ops.console.unindent();
bpy.ops.constraint.childof_clear_inverse(constraint='',owner='OBJECT');
bpy.ops.constraint.childof_set_inverse(constraint='',owner='OBJECT');
bpy.ops.constraint.delete();
bpy.ops.constraint.followpath_path_animate(constraint='',owner='OBJECT',frame_start=1,length=100);
bpy.ops.constraint.limitdistance_reset(constraint='',owner='OBJECT');
bpy.ops.constraint.move_down(constraint='',owner='OBJECT'
bpy.ops.constraint.move_up(constraint='',owner='OBJECT');
bpy.ops.constraint.objectsolver_clear_inverse(constraint='',owner='OBJECT');
bpy.ops.constraint.objectsolver_set_inverse(constraint='',owner='OBJECT');
bpy.ops.constraint.stretchto_reset(constraint='',owner='OBJECT');
bpy.ops.curve.cyclic_toggle(direction='CYCLIC_U');
bpy.ops.curve.de_select_first();
bpy.ops.curve.de_select_last();
bpy.ops.curve.delete(type='VERT');
bpy.ops.curve.duplicate();
bpy.ops.curve.duplicate_move(CURVE_OT_duplicate=None,TRANSFORM_OT_translate=None);
bpy.ops.curve.extrude(mode='TRANSLATION');
bpy.ops.curve.extrude_move(CURVE_OT_extrude=None,TRANSFORM_OT_translate=None);
bpy.ops.curve.handle_type_set(type='AUTOMATIC');
bpy.ops.curve.hide(unselected=False);
bpy.ops.curve.make_segment();
bpy.ops.curve.match_texture_space();
bpy.ops.curve.normals_make_consistent(calc_length=False);
bpy.ops.curve.primitive_bezier_circle_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.curve.primitive_bezier_curve_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.curve.primitive_nurbs_circle_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.curve.primitive_nurbs_curve_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.curve.primitive_nurbs_path_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.curve.radius_set(radius=1.0);
bpy.ops.curve.reveal();
bpy.ops.curve.select_all(action='TOGGLE');
bpy.ops.curve.select_less();
bpy.ops.curve.select_linked();
bpy.ops.curve.select_linked_pick(deselect=False);
bpy.ops.curve.select_more();
bpy.ops.curve.select_next();
bpy.ops.curve.select_nth(nth=2);
bpy.ops.curve.select_previous();
bpy.ops.curve.select_random(percent=50.0,action='SELECT');
bpy.ops.curve.select_row();
bpy.ops.curve.separate();
bpy.ops.curve.shade_flat();
bpy.ops.curve.shade_smooth();
bpy.ops.curve.smooth();
bpy.ops.curve.smooth_radius();
bpy.ops.curve.smooth_tilt();
bpy.ops.curve.smooth_weight();
bpy.ops.curve.spin(center=(0.0,0.0,0.0),axis=(0.0,0.0,0.0));
bpy.ops.curve.spline_type_set(type='POLY',use_handles=False);
bpy.ops.curve.spline_weight_set(weight=1.0);
bpy.ops.curve.split();
bpy.ops.curve.subdivide(number_cuts=1);
bpy.ops.curve.switch_direction();
bpy.ops.curve.tilt_clear();
bpy.ops.curve.vertex_add(location=(0.0,0.0,0.0);
bpy.ops.dpaint.bake();
bpy.ops.dpaint.output_toggle(output='A');
bpy.ops.dpaint.surface_slot_add();
bpy.ops.dpaint.surface_slot_remove();
bpy.ops.dpaint.type_toggle(type='CANVAS');
bpy.ops.ed.redo();
bpy.ops.ed.undo();
bpy.ops.ed.undo_history(item=0);
bpy.ops.ed.undo_push(message='Add an undo step *function may be moved*');
bpy.ops.file.autopack_toggle();
bpy.ops.file.bookmark_add();
bpy.ops.file.bookmark_delete(index=-1);
bpy.ops.file.bookmark_toggle();
bpy.ops.file.cancel();
bpy.ops.file.delete();
bpy.ops.file.directory_new(directory='',open=False);
bpy.ops.file.execute(need_active=False);
bpy.ops.file.filenum(increment=1);
bpy.ops.file.find_missing_files(find_all=False,directory='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=False,filemode=9,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.file.hidedot();
bpy.ops.file.highlight();
bpy.ops.file.make_paths_absolute();
bpy.ops.file.make_paths_relative();
bpy.ops.file.next();
bpy.ops.file.pack_all();
bpy.ops.file.pack_libraries();
bpy.ops.file.parent();
bpy.ops.file.previous();
bpy.ops.file.refresh();
bpy.ops.file.rename();
bpy.ops.file.report_missing_files();
bpy.ops.file.reset_recent();
bpy.ops.file.select(extend=False,fill=False,open=True);
bpy.ops.file.select_all_toggle();
bpy.ops.file.select_bookmark(dir='');
bpy.ops.file.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.file.smoothscroll();
bpy.ops.file.unpack_all(method='USE_LOCAL');
bpy.ops.file.unpack_item(method='USE_LOCAL',id_name='',id_type=19785);
bpy.ops.file.unpack_libraries();
bpy.ops.fluid.bake();
bpy.ops.fluid.preset_add(remove_active=False,name='');
bpy.ops.font.case_set(case='LOWER');
bpy.ops.font.case_toggle();
bpy.ops.font.change_character(delta=1);
bpy.ops.font.change_spacing(delta=1);
bpy.ops.font.delete(type='ALL');
bpy.ops.font.insert_lorem();
bpy.ops.font.line_break();
bpy.ops.font.move(type='LINE_BEGIN');
bpy.ops.font.move_select(type='LINE_BEGIN');
bpy.ops.font.open(filepath='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=True,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.font.select_all();
bpy.ops.font.style_set(style='BOLD',clear=False);
bpy.ops.font.style_toggle(style='BOLD');
bpy.ops.font.text_copy();
bpy.ops.font.text_cut();
bpy.ops.font.text_insert(text='',accent=False);
bpy.ops.font.text_paste();
bpy.ops.font.text_paste_from_clipboard(filepath='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=True,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.font.text_paste_from_file(filepath='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=True,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.font.textbox_add();
bpy.ops.font.textbox_remove(index=0);
bpy.ops.font.unlink();
bpy.ops.gpencil.active_frame_delete();
bpy.ops.gpencil.convert(type='PATH',use_normalize_weights=True,radius_multiplier=1.0,use_link_strokes=True,timing_mode='FULL',frame_range=100,start_frame=1,use_realtime=False,end_frame=250,gap_duration=0.0,gap_randomness=0.0,seed=0,use_timing_data=False);
bpy.ops.gpencil.copy();
bpy.ops.gpencil.data_add();
bpy.ops.gpencil.data_unlink();
bpy.ops.gpencil.delete(type='POINTS');
bpy.ops.gpencil.draw(mode='DRAW',stroke=None,wait_for_input=True);
bpy.ops.gpencil.duplicate();
bpy.ops.gpencil.duplicate_move(GPENCIL_OT_duplicate=None,TRANSFORM_OT_translate=None);
bpy.ops.gpencil.layer_add();
bpy.ops.gpencil.layer_duplicate();
bpy.ops.gpencil.layer_move(type='UP');
bpy.ops.gpencil.layer_remove();
bpy.ops.gpencil.paste();
bpy.ops.gpencil.select(extend=False,deselect=False,toggle=False,entire_strokes=False,location=(0,0);
bpy.ops.gpencil.select_all(action='TOGGLE');
bpy.ops.gpencil.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.gpencil.select_circle(x=0,y=0,radius=1,gesture_mode=0);
bpy.ops.gpencil.select_lasso(path=None,deselect=False,extend=True);
bpy.ops.gpencil.select_less();
bpy.ops.gpencil.select_linked();
bpy.ops.gpencil.select_more();
bpy.ops.graph.bake();
bpy.ops.graph.clean(threshold=0.001);
bpy.ops.graph.click_insert(frame=1.0,value=1.0);
bpy.ops.graph.clickselect(extend=False,column=False,curves=False);
bpy.ops.graph.copy();
bpy.ops.graph.cursor_set(frame=0,value=0.0);
bpy.ops.graph.delete();
bpy.ops.graph.duplicate(mode='TRANSLATION');
bpy.ops.graph.duplicate_move(GRAPH_OT_duplicate=None,TRANSFORM_OT_transform=None);
bpy.ops.graph.easing_type(type='AUTO');
bpy.ops.graph.euler_filter();
bpy.ops.graph.extrapolation_type(type='CONSTANT');
bpy.ops.graph.fmodifier_add(type='NULL',only_active=True);
bpy.ops.graph.fmodifier_copy();
bpy.ops.graph.fmodifier_paste();
bpy.ops.graph.frame_jump();
bpy.ops.graph.ghost_curves_clear();
bpy.ops.graph.ghost_curves_create();
bpy.ops.graph.handle_type(type='FREE');
bpy.ops.graph.hide(unselected=False);
bpy.ops.graph.interpolation_type(type='CONSTANT');
bpy.ops.graph.keyframe_insert(type='ALL');
bpy.ops.graph.mirror(type='CFRA');
bpy.ops.graph.paste(offset='START',merge='MIX');
bpy.ops.graph.previewrange_set();
bpy.ops.graph.properties();
bpy.ops.graph.reveal();
bpy.ops.graph.sample();
bpy.ops.graph.select_all_toggle(invert=False);
bpy.ops.graph.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True,axis_range=False,include_handles=False
bpy.ops.graph.select_circle(x=0,y=0,radius=1,gesture_mode=0);
bpy.ops.graph.select_column(mode='KEYS');
bpy.ops.graph.select_lasso(path=None,deselect=False,extend=True);
bpy.ops.graph.select_leftright(mode='CHECK',extend=False);
bpy.ops.graph.select_less();
bpy.ops.graph.select_linked();
bpy.ops.graph.select_more();
bpy.ops.graph.smooth();
bpy.ops.graph.snap(type='CFRA');
bpy.ops.graph.sound_bake(filepath='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=True,filter_python=False,filter_font=False,filter_sound=True,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,display_type='FILE_DEFAULTDISPLAY',low=0.0,high=100000.0,attack=0.005,release=0.2,threshold=0.0,use_accumulate=False,use_additive=False,use_square=False,sthreshold=0.1);
bpy.ops.graph.view_all(include_handles=True);
bpy.ops.graph.view_selected(include_handles=True);
bpy.ops.group.create(name='Group');
bpy.ops.group.objects_add_active(group='');
bpy.ops.group.objects_remove(group='');
bpy.ops.group.objects_remove_active(group='');
bpy.ops.group.objects_remove_all();
bpy.ops.image.change_frame(frame=0);
bpy.ops.image.clear_render_border();
bpy.ops.image.curves_point_set(point='BLACK_POINT');
bpy.ops.image.cycle_render_slot(reverse=False);
bpy.ops.image.external_edit(filepath='');
bpy.ops.image.invert(invert_r=False,invert_g=False,invert_b=False,invert_a=False);
bpy.ops.image.match_movie_length();
bpy.ops.image.new(name='Untitled',width=1024,height=1024,color=(0.0,0.0,0.0,1.0),alpha=True,generated_type='BLANK',float=False,gen_context='NONE');
bpy.ops.image.open(filepath='',directory='',files=None,filter_blender=False,filter_backup=False,filter_image=True,filter_movie=True,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.image.pack(as_png=False);
bpy.ops.image.project_apply();
bpy.ops.image.project_edit();
bpy.ops.image.properties();
bpy.ops.image.read_renderlayers();
bpy.ops.image.reload();
bpy.ops.image.render_border(xmin=0,xmax=0,ymin=0,ymax=0);
bpy.ops.image.replace(filepath='',filter_blender=False,filter_backup=False,filter_image=True,filter_movie=True,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.image.sample();
bpy.ops.image.sample_line(xstart=0,xend=0,ystart=0,yend=0,cursor=1002);
bpy.ops.image.save();
bpy.ops.image.save_as(save_as_render=False,copy=False,filepath='',check_existing=True,filter_blender=False,filter_backup=False,filter_image=True,filter_movie=True,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.image.save_dirty();
bpy.ops.image.save_sequence();
bpy.ops.image.toolshelf();
bpy.ops.image.unpack(method='USE_LOCAL',id='');
bpy.ops.image.view_all(fit_view=False);
bpy.ops.image.view_ndof();
bpy.ops.image.view_pan(offset=(0.0,0.0);
bpy.ops.image.view_selected();
bpy.ops.image.view_zoom(factor=0.0);
bpy.ops.image.view_zoom_in(location=(0.0,0.0);
bpy.ops.image.view_zoom_out(location=(0.0,0.0);
bpy.ops.image.view_zoom_ratio(ratio=0.0);
bpy.ops.info.report_copy();
bpy.ops.info.report_delete();
bpy.ops.info.report_replay();
bpy.ops.info.reports_display_update();
bpy.ops.info.select_all_toggle();
bpy.ops.info.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.info.select_pick(report_index=0);
bpy.ops.lamp.sunsky_preset_add(remove_active=False,name='');
bpy.ops.lattice.flip(axis='U');
bpy.ops.lattice.make_regular();
bpy.ops.lattice.select_all(action='TOGGLE');
bpy.ops.lattice.select_less();
bpy.ops.lattice.select_mirror(axis='X',extend=False);
bpy.ops.lattice.select_more();
bpy.ops.lattice.select_random(percent=50.0,action='SELECT');
bpy.ops.lattice.select_ungrouped(extend=False);
bpy.ops.logic.actuator_add(type='',name='',object='');
bpy.ops.logic.actuator_move(actuator='',object='',direction='UP');
bpy.ops.logic.actuator_remove(actuator='',object='');
bpy.ops.logic.controller_add(type='LOGIC_AND',name='',object='');
bpy.ops.logic.controller_move(controller='',object='',direction='UP');
bpy.ops.logic.controller_remove(controller='',object='');
bpy.ops.logic.links_cut(path=None,cursor=9);
bpy.ops.logic.properties();
bpy.ops.logic.sensor_add(type='',name='',object='');
bpy.ops.logic.sensor_move(sensor='',object='',direction='UP');
bpy.ops.logic.sensor_remove(sensor='',object='');
bpy.ops.logic.view_all();
bpy.ops.marker.add();
bpy.ops.marker.camera_bind();
bpy.ops.marker.delete();
bpy.ops.marker.duplicate(frames=0);
bpy.ops.marker.make_links_scene(scene='');
bpy.ops.marker.move(frames=0);
bpy.ops.marker.rename(name='RenamedMarker');
bpy.ops.marker.select(extend=False,camera=False);
bpy.ops.marker.select_all(action='TOGGLE');
bpy.ops.marker.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.mask.add_feather_vertex(location=(0.0,0.0);
bpy.ops.mask.add_feather_vertex_slide(MASK_OT_add_feather_vertex=None,MASK_OT_slide_point=None);
bpy.ops.mask.add_vertex(location=(0.0,0.0);
bpy.ops.mask.add_vertex_slide(MASK_OT_add_vertex=None,MASK_OT_slide_point=None);
bpy.ops.mask.splines();
bpy.ops.mask.cyclic_toggle();
bpy.ops.mask.delete();
bpy.ops.mask.duplicate();
bpy.ops.mask.duplicate_move(MASK_OT_duplicate=None,TRANSFORM_OT_translate=None);
bpy.ops.mask.feather_weight_clear();
bpy.ops.mask.handle_type_set(type='AUTO');
bpy.ops.mask.hide_view_clear();
bpy.ops.mask.hide_view_set(unselected=False);
bpy.ops.mask.layer_move(direction='UP');
bpy.ops.mask.layer_new(name='');
bpy.ops.mask.layer_remove();
bpy.ops.mask.new(name='');
bpy.ops.mask.normals_make_consistent();
bpy.ops.mask.parent_clear();
bpy.ops.mask.parent_set();
bpy.ops.mask.paste_splines();
bpy.ops.mask.primitive_circle_add(size=100.0,location=(0.0,0.0);
bpy.ops.mask.primitive_square_add(size=100.0,location=(0.0,0.0);
bpy.ops.mask.select(extend=False,deselect=False,toggle=False,location=(0.0,0.0);
bpy.ops.mask.select_all(action='TOGGLE');
bpy.ops.mask.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.mask.select_circle(x=0,y=0,radius=1,gesture_mode=0);
bpy.ops.mask.select_lasso(path=None,deselect=False,extend=True);
bpy.ops.mask.select_less();
bpy.ops.mask.select_linked();
bpy.ops.mask.select_linked_pick(deselect=False);
bpy.ops.mask.select_more();
bpy.ops.mask.shape_key_clear();
bpy.ops.mask.shape_key_feather_reset();
bpy.ops.mask.shape_key_insert();
bpy.ops.mask.shape_key_rekey(location=True,feather=True);
bpy.ops.mask.slide_point(slide_feather=False,is_new_point=False);
bpy.ops.mask.slide_spline_curvature();
bpy.ops.mask.switch_direction();
bpy.ops.material.copy();
bpy.ops.material.new();
bpy.ops.material.paste();
bpy.ops.material.sss_preset_add(remove_active=False,name='');
bpy.ops.mball.delete_metaelems();
bpy.ops.mball.duplicate_metaelems();
bpy.ops.mball.duplicate_move(MBALL_OT_duplicate_metaelems=None,TRANSFORM_OT_translate=None);
bpy.ops.mball.hide_metaelems(unselected=False);
bpy.ops.mball.reveal_metaelems();
bpy.ops.mball.select_all(action='TOGGLE');
bpy.ops.mball.select_random_metaelems(percent=50.0,action='SELECT');
bpy.ops.mball.select_similar(type='TYPE',threshold=0.1);
bpy.ops.mesh.beautify_fill(angle_limit=3.14159);
bpy.ops.mesh.bevel(offset_type='OFFSET',offset=0.0,segments=1,profile=0.5,vertex_only=False,clamp_overlap=False,material=-1);
bpy.ops.mesh.bisect(plane_co=(0.0,0.0,0.0),plane_no=(0.0,0.0,0.0),use_fill=False,clear_inner=False,clear_outer=False,threshold=0.0001,xstart=0,xend=0,ystart=0,yend=0,cursor=1002);
bpy.ops.mesh.blend_from_shape(shape='',blend=1.0,add=True);
bpy.ops.mesh.bridge_edge_loops(type='SINGLE',use_merge=False,merge_factor=0.5,twist_offset=0,number_cuts=0,interpolation='PATH',smoothness=1.0,profile_shape_factor=0.0,profile_shape='SMOOTH');
bpy.ops.mesh.colors_reverse();
bpy.ops.mesh.colors_rotate(use_ccw=False);
bpy.ops.mesh.customdata_clear_mask();
bpy.ops.mesh.customdata_clear_skin();
bpy.ops.mesh.delete(type='VERT');
bpy.ops.mesh.delete_edgeloop(use_face_split=True);
bpy.ops.mesh.delete_loose(use_verts=True,use_edges=True,use_faces=False);
bpy.ops.mesh.dissolve_degenerate(threshold=0.0001);
bpy.ops.mesh.dissolve_edges(use_verts=True,use_face_split=False);
bpy.ops.mesh.dissolve_faces(use_verts=False);
bpy.ops.mesh.dissolve_limited(angle_limit=0.0872665,use_dissolve_boundaries=False,delimit=set();
bpy.ops.mesh.dissolve_mode(use_verts=False,use_face_split=False,use_boundary_tear=False);
bpy.ops.mesh.dissolve_verts(use_face_split=False,use_boundary_tear=False);
bpy.ops.mesh.drop_named_image(name='Image',filepath='Path',relative_path=True);
bpy.ops.mesh.dupli_extrude_cursor(rotate_source=True);
bpy.ops.mesh.duplicate(mode=1);
bpy.ops.mesh.duplicate_move(MESH_OT_duplicate=None,TRANSFORM_OT_translate=None);
bpy.ops.mesh.edge_collapse();
bpy.ops.mesh.edge_face_add();
bpy.ops.mesh.edge_rotate(use_ccw=False);
bpy.ops.mesh.edge_split();
bpy.ops.mesh.edgering_select(extend=False,deselect=False,toggle=False,ring=True);
bpy.ops.mesh.edges_select_sharp(sharpness=0.523599);
bpy.ops.mesh.extrude_edges_indiv(mirror=False);
bpy.ops.mesh.extrude_edges_move(MESH_OT_extrude_edges_indiv=None,TRANSFORM_OT_translate=None);
bpy.ops.mesh.extrude_faces_indiv(mirror=False);
bpy.ops.mesh.extrude_faces_move(MESH_OT_extrude_faces_indiv=None,TRANSFORM_OT_shrink_fatten=None);
bpy.ops.mesh.extrude_region(mirror=False);
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region=None,TRANSFORM_OT_translate=None);
bpy.ops.mesh.extrude_region_shrink_fatten(MESH_OT_extrude_region=None,TRANSFORM_OT_shrink_fatten=None);
bpy.ops.mesh.extrude_repeat(offset=2.0,steps=10);
bpy.ops.mesh.extrude_vertices_move(MESH_OT_extrude_verts_indiv=None,TRANSFORM_OT_translate=None);
bpy.ops.mesh.extrude_verts_indiv(mirror=False);
bpy.ops.mesh.face_split_by_edges();
bpy.ops.mesh.faces_mirror_uv(direction='POSITIVE',precision=3);
bpy.ops.mesh.faces_select_linked_flat(sharpness=0.0174533);
bpy.ops.mesh.faces_shade_flat();
bpy.ops.mesh.faces_shade_smooth();
bpy.ops.mesh.fill(use_beauty=True);
bpy.ops.mesh.fill_grid(span=1,offset=0,use_interp_simple=False);
bpy.ops.mesh.fill_holes(sides=4);
bpy.ops.mesh.flip_normals();
bpy.ops.mesh.hide(unselected=False);
bpy.ops.mesh.inset(use_boundary=True,use_even_offset=True,use_relative_offset=False,use_edge_rail=False,thickness=0.01,depth=0.0,use_outset=False,use_select_inset=False,use_individual=False,use_interpolate=True);
bpy.ops.mesh.intersect(mode='SELECT_UNSELECT',use_separate=True,threshold=1e-06);
bpy.ops.mesh.knife_project(cut_through=False);
bpy.ops.mesh.knife_tool(use_occlude_geometry=True,only_selected=False);
bpy.ops.mesh.loop_multi_select(ring=False);
bpy.ops.mesh.loop_select(extend=False,deselect=False,toggle=False,ring=False);
bpy.ops.mesh.loop_to_region(select_bigger=False);
bpy.ops.mesh.loopcut(number_cuts=1,smoothness=0.0,falloff='ROOT',edge_index=-1,mesh_select_mode_init=(False,False,False);
bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut=None,TRANSFORM_OT_edge_slide=None);
bpy.ops.mesh.mark_seam(clear=False);
bpy.ops.mesh.mark_sharp(clear=False,use_verts=False);
bpy.ops.mesh.merge(type='CENTER',uvs=False);
bpy.ops.mesh.noise(factor=0.1);
bpy.ops.mesh.normals_make_consistent(inside=False);
bpy.ops.mesh.poke(offset=0.0,use_relative_offset=False,center_mode='MEAN_WEIGHTED');
bpy.ops.mesh.primitive_circle_add(vertices=32,radius=1.0,fill_type='NOTHING',view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=1.0,radius2=0.0,depth=2.0,end_fill_type='NGON',view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.mesh.primitive_cube_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=1.0,depth=2.0,end_fill_type='NGON',view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.mesh.primitive_grid_add(x_subdivisions=10,y_subdivisions=10,radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,size=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.mesh.primitive_monkey_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.mesh.primitive_plane_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.mesh.primitive_torus_add(rotation=(0.0,0.0,0.0),location=(0.0,0.0,0.0),view_align=False,major_segments=48,minor_segments=12,mode='MAJOR_MINOR',major_radius=1.0,minor_radius=0.25,abso_major_rad=1.25,abso_minor_rad=0.75);
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,size=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY',ngon_method='BEAUTY');
bpy.ops.mesh.region_to_loop();
bpy.ops.mesh.remove_doubles(threshold=0.0001,use_unselected=False);
bpy.ops.mesh.reveal();
bpy.ops.mesh.rip(mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,release_confirm=False,use_fill=False);
bpy.ops.mesh.rip_edge(mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,release_confirm=False);
bpy.ops.mesh.rip_edge_move(MESH_OT_rip_edge=None,TRANSFORM_OT_translate=None);
bpy.ops.mesh.rip_move(MESH_OT_rip=None,TRANSFORM_OT_translate=None);
bpy.ops.mesh.rip_move_fill(MESH_OT_rip=None,TRANSFORM_OT_translate=None);
bpy.ops.mesh.screw(steps=9,turns=1,center=(0.0,0.0,0.0),axis=(0.0,0.0,0.0);
bpy.ops.mesh.select_all(action='TOGGLE');
bpy.ops.mesh.select_axis(mode='POSITIVE',axis='X_AXIS');
bpy.ops.mesh.select_face_by_sides(number=4,type='EQUAL',extend=True);
bpy.ops.mesh.select_interior_faces();
bpy.ops.mesh.select_less(use_face_step=True);
bpy.ops.mesh.select_linked(limit=False);
bpy.ops.mesh.select_linked_pick(deselect=False,limit=False);
bpy.ops.mesh.select_loose(extend=False);
bpy.ops.mesh.select_mirror(extend=False);
bpy.ops.mesh.select_mode(use_extend=False,use_expand=False,type='VERT',action='TOGGLE');
bpy.ops.mesh.select_more(use_face_step=True);
bpy.ops.mesh.select_next_loop();
bpy.ops.mesh.select_non_manifold(extend=True,use_wire=True,use_boundary=True,use_multi_face=True,use_non_contiguous=True,use_verts=True);
bpy.ops.mesh.select_nth(nth=2,offset=0);
bpy.ops.mesh.select_random(percent=50.0,action='SELECT');
bpy.ops.mesh.select_similar(type='NORMAL',compare='EQUAL',threshold=0.0);
bpy.ops.mesh.select_similar_region();
bpy.ops.mesh.select_ungrouped(extend=False);
bpy.ops.mesh.separate(type='SELECTED');
bpy.ops.mesh.shape_propagate_to_all();
bpy.ops.mesh.shortest_path_pick(extend=False);
bpy.ops.mesh.shortest_path_select(use_length=True);
bpy.ops.mesh.solidify(thickness=0.01);
bpy.ops.mesh.sort_elements(type='VIEW_ZAXIS',elements=set(),reverse=False,seed=0);
bpy.ops.mesh.spin(steps=9,dupli=False,angle=1.5708,center=(0.0,0.0,0.0),axis=(0.0,0.0,0.0);
bpy.ops.mesh.split();
bpy.ops.mesh.subdivide(number_cuts=1,smoothness=0.0,quadtri=False,quadcorner='STRAIGHT_CUT',fractal=0.0,fractal_along_normal=0.0,seed=0);
bpy.ops.mesh.subdivide_edgering(number_cuts=10,interpolation='PATH',smoothness=1.0,profile_shape_factor=0.0,profile_shape='SMOOTH');
bpy.ops.mesh.symmetrize(direction='NEGATIVE_X',threshold=0.0001);
bpy.ops.mesh.symmetry_snap(direction='NEGATIVE_X',threshold=0.05,factor=0.5,use_center=True);
bpy.ops.mesh.tris_convert_to_quads(limit=0.698132,uvs=False,vcols=False,sharp=False,materials=False);
bpy.ops.mesh.unsubdivide(iterations=2);
bpy.ops.mesh.uv_texture_add();
bpy.ops.mesh.uv_texture_remove();
bpy.ops.mesh.uvs_reverse();
bpy.ops.mesh.uvs_rotate(use_ccw=False);
bpy.ops.mesh.vert_connect();
bpy.ops.mesh.vert_connect_nonplanar(angle_limit=0.0872665);
bpy.ops.mesh.vertex_color_add();
bpy.ops.mesh.vertex_color_remove();
bpy.ops.mesh.vertices_smooth(factor=0.5,repeat=1,xaxis=True,yaxis=True,zaxis=True);
bpy.ops.mesh.vertices_smooth_laplacian(repeat=1,lambda_factor=5e-05,lambda_border=5e-05,use_x=True,use_y=True,use_z=True,preserve_volume=True);
bpy.ops.mesh.wireframe(use_boundary=True,use_even_offset=True,use_relative_offset=False,use_replace=True,thickness=0.01,offset=0.01,use_crease=False,crease_weight=0.01);
bpy.ops.nla.action_pushdown(channel_index=-1);
bpy.ops.nla.action_sync_length(active=True);
bpy.ops.nla.actionclip_add(action='');
bpy.ops.nla.apply_scale();
bpy.ops.nla.bake(frame_start=1,frame_end=250,step=1,only_selected=True,visual_keying=False,clear_constraints=False,clear_parents=False,bake_types={'POSE'});
bpy.ops.nla.channels_click(extend=False);
bpy.ops.nla.clear_scale();
bpy.ops.nla.click_select(extend=False);
bpy.ops.nla.delete();
bpy.ops.nla.duplicate(linked=False,mode='TRANSLATION');
bpy.ops.nla.fmodifier_add(type='NULL',only_active=False);
bpy.ops.nla.fmodifier_copy();
bpy.ops.nla.fmodifier_paste();
bpy.ops.nla.make_single_user();
bpy.ops.nla.meta_add();
bpy.ops.nla.meta_remove();
bpy.ops.nla.move_down();
bpy.ops.nla.move_up();
bpy.ops.nla.mute_toggle();
bpy.ops.nla.previewrange_set();
bpy.ops.nla.properties();
bpy.ops.nla.select_all_toggle(invert=False);
bpy.ops.nla.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True,axis_range=False);
bpy.ops.nla.select_leftright(mode='CHECK',extend=False);
bpy.ops.nla.selected_objects_add();
bpy.ops.nla.snap(type='CFRA');
bpy.ops.nla.soundclip_add();
bpy.ops.nla.split();
bpy.ops.nla.swap();
bpy.ops.nla.tracks_add(above_selected=False);
bpy.ops.nla.tracks_delete();
bpy.ops.nla.transition_add();
bpy.ops.nla.tweakmode_enter();
bpy.ops.nla.tweakmode_exit();
bpy.ops.nla.view_all();
bpy.ops.nla.view_selected();
bpy.ops.node.add_and_link_node(type='',use_transform=False,settings=None,link_socket_index=0);
bpy.ops.node.add_file(filepath='',filter_blender=False,filter_backup=False,filter_image=True,filter_movie=True,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY',name='Image');
bpy.ops.node.add_mask(name='Mask');
bpy.ops.node.add_node(type='',use_transform=False,settings=None);
bpy.ops.node.add_reroute(path=None,cursor=6);
bpy.ops.node.add_search(type='',use_transform=False,settings=None,node_item='');
bpy.ops.node.attach();
bpy.ops.node.backimage_fit();
bpy.ops.node.backimage_move();
bpy.ops.node.backimage_sample();
bpy.ops.node.backimage_zoom(factor=1.2);
bpy.ops.node.clear_viewer_border();
bpy.ops.node.clipboard_copy();
bpy.ops.node.clipboard_paste();
bpy.ops.node.collapse_hide_unused_toggle();
bpy.ops.node.delete();
bpy.ops.node.delete_reconnect();
bpy.ops.node.detach();
bpy.ops.node.detach_translate_attach(NODE_OT_detach=None,TRANSFORM_OT_translate=None,NODE_OT_attach=None);
bpy.ops.node.duplicate(keep_inputs=False);
bpy.ops.node.duplicate_move(NODE_OT_duplicate=None,NODE_OT_translate_attach=None);
bpy.ops.node.duplicate_move_keep_inputs(NODE_OT_duplicate=None,NODE_OT_translate_attach=None);
bpy.ops.node.find_node(prev=False);
bpy.ops.node.group_edit(exit=False);
bpy.ops.node.group_insert();
bpy.ops.node.group_make();
bpy.ops.node.group_separate(type='COPY');
bpy.ops.node.group_ungroup();
bpy.ops.node.hide_socket_toggle();
bpy.ops.node.hide_toggle();
bpy.ops.node.join();
bpy.ops.node.link(detach=False);
bpy.ops.node.link_make(replace=False);
bpy.ops.node.link_viewer();
bpy.ops.node.links_cut(path=None,cursor=9);
bpy.ops.node.links_detach();
bpy.ops.node.move_detach_links(NODE_OT_links_detach=None,TRANSFORM_OT_translate=None);
bpy.ops.node.move_detach_links_release(NODE_OT_links_detach=None,NODE_OT_translate_attach=None);
bpy.ops.node.mute_toggle();
bpy.ops.node.new_node_tree(type='',name='NodeTree');
bpy.ops.node.node_color_preset_add(remove_active=False,name='');
bpy.ops.node.node_color();
bpy.ops.node.options_toggle();
bpy.ops.node.output_file_add_socket(file_path='Image');
bpy.ops.node.output_file_move_active_socket(direction='DOWN');
bpy.ops.node.output_file_remove_active_socket();
bpy.ops.node.parent_set();
bpy.ops.node.preview_toggle();
bpy.ops.node.properties();
bpy.ops.node.read_fullsamplelayers();
bpy.ops.node.read_renderlayers();
bpy.ops.node.render_changed();
bpy.ops.node.resize();
bpy.ops.node.select(mouse_x=0,mouse_y=0,extend=False);
bpy.ops.node.select_all(action='TOGGLE');
bpy.ops.node.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True,tweak=False);
bpy.ops.node.select_circle(x=0,y=0,radius=1,gesture_mode=0);
bpy.ops.node.select_grouped(extend=False,type='TYPE');
bpy.ops.node.select_lasso(path=None,deselect=False,extend=True);
bpy.ops.node.select_link_viewer(NODE_OT_select=None,NODE_OT_link_viewer=None);
bpy.ops.node.select_linked_from();
bpy.ops.node.select_linked_to();
bpy.ops.node.select_same_type_step(prev=False);
bpy.ops.node.shader_script_update();
bpy.ops.node.toolbar();
bpy.ops.node.translate_attach(TRANSFORM_OT_translate=None,NODE_OT_attach=None);
bpy.ops.node.tree_path_parent();
bpy.ops.node.tree_socket_add(in_out='IN');
bpy.ops.node.tree_socket_move(direction='UP');
bpy.ops.node.tree_socket_remove();
bpy.ops.node.view_all();
bpy.ops.node.view_selected();
bpy.ops.node.viewer_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.object.add(radius=1.0,type='EMPTY',view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=(False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False
bpy.ops.object.add_named(linked=False,name='');
bpy.ops.object.align(bb_quality=True,align_mode='OPT_2',relative_to='OPT_4',align_axis=set();
bpy.ops.object.anim_transforms_to_deltas();
bpy.ops.object.armature_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.object.bake(type='COMBINED',filepath='',width=512,height=512,margin=16,use_selected_to_active=False,cage_extrusion=0.0,cage_object='',normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z',save_mode='INTERNAL',use_clear=False,use_cage=False,use_split_materials=False,use_automatic_name=False,uv_layer='');
bpy.ops.object.bake_image();
bpy.ops.object.camera_add(view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=(False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False
bpy.ops.object.constraint_add(type='');
bpy.ops.object.constraint_add_with_targets(type='');
bpy.ops.object.constraints_clear();
bpy.ops.object.constraints_copy();
bpy.ops.object.convert(target='MESH',keep_original=False);
bpy.ops.object.delete(use_global=False);
bpy.ops.object.drop_named_image(filepath='',relative_path=True,name='',view_align=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.object.drop_named_material(name='Material');
bpy.ops.object.dupli_offset_from_cursor();
bpy.ops.object.duplicate(linked=False,mode='TRANSLATION');
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate=None,TRANSFORM_OT_translate=None);
bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate=None,TRANSFORM_OT_translate=None);
bpy.ops.object.duplicates_make_real(use_base_parent=False,use_hierarchy=False);
bpy.ops.object.editmode_toggle();
bpy.ops.object.effector_add(type='FORCE',radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.object.empty_add(type='PLAIN_AXES',radius=1.0,view_align=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.object.explode_refresh(modifier='');
bpy.ops.object.forcefield_toggle();
bpy.ops.object.game_physics_copy();
bpy.ops.object.game_property_clear();
bpy.ops.object.game_property_copy(operation='COPY',property='');
bpy.ops.object.game_property_new(type='FLOAT',name='');
bpy.ops.object.game_property_remove(index=0);
bpy.ops.object.group_add();
bpy.ops.object.group_instance_add(name='Group',group='',view_align=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.object.group_link(group='');
bpy.ops.object.group_remove();
bpy.ops.object.group_unlink();
bpy.ops.object.grouped_select();
bpy.ops.object.hide_render_clear();
bpy.ops.object.hide_render_clear_all();
bpy.ops.object.hide_render_set(unselected=False);
bpy.ops.object.hide_view_clear();
bpy.ops.object.hide_view_set(unselected=False);
bpy.ops.object.hook_add_newob();
bpy.ops.object.hook_add_selob(use_bone=False);
bpy.ops.object.hook_assign(modifier='');
bpy.ops.object.hook_recenter(modifier='');
bpy.ops.object.hook_remove(modifier='');
bpy.ops.object.hook_reset(modifier='');
bpy.ops.object.hook_select(modifier='');
bpy.ops.object.isolate_type_render();
bpy.ops.object.join();
bpy.ops.object.join_shapes();
bpy.ops.object.join_uvs();
bpy.ops.object.lamp_add(type='POINT',radius=1.0,view_align=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.object.laplaciandeform_bind(modifier='');
bpy.ops.object.location_clear();
bpy.ops.object.lod_add();
bpy.ops.object.lod_by_name();
bpy.ops.object.lod_clear_all();
bpy.ops.object.lod_generate(count=3,target=0.1,package=False);
bpy.ops.object.lod_remove(index=1);
bpy.ops.object.logic_bricks_copy();
bpy.ops.object.make_dupli_face();
bpy.ops.object.make_links_data(type='OBDATA');
bpy.ops.object.make_links_scene(scene='');
bpy.ops.object.make_local(type='SELECT_OBJECT');
bpy.ops.object.make_single_user(type='SELECTED_OBJECTS',object=False,obdata=False,material=False,texture=False,animation=False);
bpy.ops.object.material_slot_add();
bpy.ops.object.material_slot_assign();
bpy.ops.object.material_slot_copy();
bpy.ops.object.material_slot_deselect();
bpy.ops.object.material_slot_remove();
bpy.ops.object.material_slot_select();
bpy.ops.object.meshdeform_bind(modifier='');
bpy.ops.object.metaball_add(type='BALL',radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.object.mode_set(mode='OBJECT',toggle=False);
bpy.ops.object.modifier_add(type='SUBSURF');
bpy.ops.object.modifier_apply(apply_as='DATA',modifier='');
bpy.ops.object.modifier_convert(modifier='');
bpy.ops.object.modifier_copy(modifier='');
bpy.ops.object.modifier_move_down(modifier='');
bpy.ops.object.modifier_move_up(modifier='');
bpy.ops.object.modifier_remove(modifier='');
bpy.ops.object.move_to_layer(layers=T20False);
bpy.ops.object.multires_base_apply(modifier='');
bpy.ops.object.multires_external_pack();
bpy.ops.object.multires_external_save(filepath='',check_existing=True,filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=True,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY',modifier='');
bpy.ops.object.multires_higher_levels_delete(modifier='');
bpy.ops.object.multires_reshape(modifier='');
bpy.ops.object.multires_subdivide(modifier='');
bpy.ops.object.ocean_bake(modifier='',free=False);
bpy.ops.object.origin_clear();
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN',center='MEDIAN');
bpy.ops.object.parent_clear(type='CLEAR');
bpy.ops.object.parent_no_inverse_set();
bpy.ops.object.parent_set(type='OBJECT',xmirror=False,keep_transform=False);
bpy.ops.object.particle_system_add();
bpy.ops.object.particle_system_remove();
bpy.ops.object.paths_calculate(start_frame=1,end_frame=250);
bpy.ops.object.paths_clear();
bpy.ops.object.paths_update();
bpy.ops.object.posemode_toggle();
bpy.ops.object.proxy_make(object='DEFAULT');
bpy.ops.object.quick_explode(style='EXPLODE',amount=100,frame_duration=50,frame_start=1,frame_end=10,velocity=1.0,fade=True);
bpy.ops.object.quick_fluid(style='BASIC',initial_velocity=(0.0,0.0,0.0),show_flows=False,start_baking=False);
bpy.ops.object.quick_fur(density='MEDIUM',view_percentage=10,length=0.1);
bpy.ops.object.quick_smoke(style='SMOKE',show_flows=False);
bpy.ops.object.randomize_transform(random_seed=0,use_delta=False,use_loc=True,loc=(0.0,0.0,0.0),use_rot=True,rot=(0.0,0.0,0.0),use_scale=True,scale_even=False,scale=(1.0,1.0,1.0);
bpy.ops.object.rotation_clear();
bpy.ops.object.scale_clear();
bpy.ops.object.select_all(action='TOGGLE');
bpy.ops.object.select_by_layer(match='EXACT',extend=False,layers=1);
bpy.ops.object.select_by_type(extend=False,type='MESH');
bpy.ops.object.select_camera(extend=False);
bpy.ops.object.select_grouped(extend=False,type='CHILDREN_RECURSIVE');
bpy.ops.object.select_hierarchy(direction='PARENT',extend=False);
bpy.ops.object.select_linked(extend=False,type='OBDATA');
bpy.ops.object.select_mirror(extend=False);
bpy.ops.object.select_pattern(pattern='*',case_sensitive=False,extend=True);
bpy.ops.object.select_random(percent=50.0,action='SELECT');
bpy.ops.object.select_same_group(group='');
bpy.ops.object.shade_flat();
bpy.ops.object.shade_smooth();
bpy.ops.object.shape_key_add(from_mix=True);
bpy.ops.object.shape_key_clear();
bpy.ops.object.shape_key_mirror(use_topology=False);
bpy.ops.object.shape_key_move(type='TOP');
bpy.ops.object.shape_key_remove(all=False);
bpy.ops.object.shape_key_retime();
bpy.ops.object.shape_key_transfer(mode='OFFSET',use_clamp=False);
bpy.ops.object.skin_armature_create(modifier='');
bpy.ops.object.skin_loose_mark_clear(action='MARK');
bpy.ops.object.skin_radii_equalize();
bpy.ops.object.skin_root_mark();
bpy.ops.object.slow_parent_clear();
bpy.ops.object.slow_parent_set();
bpy.ops.object.speaker_add(view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.object.subdivision_set(level=1,relative=False);
bpy.ops.object.text_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.object.track_clear(type='CLEAR');
bpy.ops.object.track_set(type='DAMPTRACK');
bpy.ops.object.transform_apply(location=False,rotation=False,scale=False);
bpy.ops.object.unlink_data();
bpy.ops.object.vertex_group_add();
bpy.ops.object.vertex_group_assign();
bpy.ops.object.vertex_group_assign_new();
bpy.ops.object.vertex_group_blend(group_select_mode='',factor=1.0);
bpy.ops.object.vertex_group_clean(group_select_mode='',limit=0.0,keep_single=False);
bpy.ops.object.vertex_group_copy();
bpy.ops.object.vertex_group_to_linked();
bpy.ops.object.vertex_group_to_selected();
bpy.ops.object.vertex_group_deselect();
bpy.ops.object.vertex_group_fix(dist=0.0,strength=1.0,accuracy=1.0);
bpy.ops.object.vertex_group_invert(group_select_mode='',auto_assign=True,auto_remove=True);
bpy.ops.object.vertex_group_levels(group_select_mode='',offset=0.0,gain=1.0);
bpy.ops.object.vertex_group_limit_total(group_select_mode='',limit=4);
bpy.ops.object.vertex_group_lock(action='TOGGLE');
bpy.ops.object.vertex_group_mirror(mirror_weights=True,flip_group_names=True,all_groups=False,use_topology=False);
bpy.ops.object.vertex_group_move(direction='UP');
bpy.ops.object.vertex_group_normalize();
bpy.ops.object.vertex_group_normalize_all(group_select_mode='',lock_active=True);
bpy.ops.object.vertex_group_quantize(group_select_mode='',steps=4);
bpy.ops.object.vertex_group_remove(all=False);
bpy.ops.object.vertex_group_remove_from(use_all_groups=False,use_all_verts=False);
bpy.ops.object.vertex_group_select();
bpy.ops.object.vertex_group_set_active(group='');
bpy.ops.object.vertex_group_sort(sort_type='NAME');
bpy.ops.object.vertex_group_transfer_weight(group_select_mode='WT_REPLACE_ALL_VERTEX_GROUPS',method='WT_BY_NEAREST_FACE',replace_mode='WT_REPLACE_ALL_WEIGHTS');
bpy.ops.object.vertex_parent_set();
bpy.ops.object.vertex_random(offset=0.1,uniform=0.0,normal=0.0,seed=0);
bpy.ops.object.vertex_warp(warp_angle=6.28319,offset_angle=0.0,min=-1,max=1.0,viewmat=(0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0),center=(0.0,0.0,0.0);
bpy.ops.object.vertex_weight_copy();
bpy.ops.object.vertex_weight_delete(weight_group=-1);
bpy.ops.object.vertex_weight_normalize_active_vertex();
bpy.ops.object.vertex_weight_paste(weight_group=-1);
bpy.ops.object.vertex_weight_set_active(weight_group=-1);
bpy.ops.object.visual_transform_apply();
bpy.ops.outliner.action_set(action='');
bpy.ops.outliner.animdata_operation(type='CLEAR_ANIMDATA');
bpy.ops.outliner.data_operation(type='SELECT');
bpy.ops.outliner.drivers_add_selected();
bpy.ops.outliner.drivers_delete_selected();
bpy.ops.outliner.expanded_toggle();
bpy.ops.outliner.group_operation(type='UNLINK');
bpy.ops.outliner.id_operation(type='UNLINK');
bpy.ops.outliner.item_activate(extend=True,recursive=False);
bpy.ops.outliner.item_openclose(all=True);
bpy.ops.outliner.item_rename();
bpy.ops.outliner.keyingset_add_selected();
bpy.ops.outliner.keyingset_remove_selected();
bpy.ops.outliner.material_drop(object='Object',material='Material');
bpy.ops.outliner.object_operation(type='SELECT');
bpy.ops.outliner.operation();
bpy.ops.outliner.parent_clear(dragged_obj='Object',type='CLEAR');
bpy.ops.outliner.parent_drop(child='Object',parent='Object',type='OBJECT');
bpy.ops.outliner.renderability_toggle();
bpy.ops.outliner.scene_drop(object='Object',scene='Scene');
bpy.ops.outliner.scroll_page(up=False);
bpy.ops.outliner.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0);
bpy.ops.outliner.selectability_toggle();
bpy.ops.outliner.selected_toggle();
bpy.ops.outliner.show_active();
bpy.ops.outliner.show_hierarchy();
bpy.ops.outliner.show_one_level(open=True);
bpy.ops.outliner.visibility_toggle();
bpy.ops.paint.add_simple_uvs();
bpy.ops.paint.add_texture_paint_slot(type='DIFFUSE_COLOR',name='Untitled',width=1024,height=1024,color=(0.0,0.0,0.0,1.0),alpha=True,generated_type='BLANK',float=False);
bpy.ops.paint.brush_colors_flip();
bpy.ops.paint.brush_select(paint_mode='ACTIVE',sculpt_tool='BLOB',vertex_paint_tool='MIX',weight_paint_tool='MIX',texture_paint_tool='DRAW',toggle=False,create_missing=False);
bpy.ops.paint.delete_texture_paint_slot();
bpy.ops.paint.face_select_all(action='TOGGLE');
bpy.ops.paint.face_select_hide(unselected=False);
bpy.ops.paint.face_select_linked();
bpy.ops.paint.face_select_linked_pick(deselect=False);
bpy.ops.paint.face_select_reveal(unselected=False);
bpy.ops.paint.grab_clone(delta=(0.0,0.0);
bpy.ops.paint.hide_show(action='HIDE',area='INSIDE',xmin=0,xmax=0,ymin=0,ymax=0);
bpy.ops.paint.image_from_view(filepath='');
bpy.ops.paint.image_paint(stroke=None,mode='NORMAL');
bpy.ops.paint.mask_flood_fill(mode='VALUE',value=0.0);
bpy.ops.paint.mask_lasso_gesture(path=None,mode='VALUE',value=1.0);
bpy.ops.paint.project_image(image='');
bpy.ops.paint.sample_color(location=(0,0),palette=False);
bpy.ops.paint.texture_paint_toggle();
bpy.ops.paint.vert_select_all(action='TOGGLE');
bpy.ops.paint.vert_select_ungrouped(extend=False);
bpy.ops.paint.vertex_color_dirt(blur_strength=1.0,blur_iterations=1,clean_angle=3.14159,dirt_angle=0.0,dirt_only=False);
bpy.ops.paint.vertex_color_set();
bpy.ops.paint.vertex_color_smooth();
bpy.ops.paint.vertex_paint(stroke=None,mode='NORMAL');
bpy.ops.paint.vertex_paint_toggle();
bpy.ops.paint.weight_from_bones(type='AUTOMATIC');
bpy.ops.paint.weight_gradient(type='LINEAR',xstart=0,xend=0,ystart=0,yend=0,cursor=1002);
bpy.ops.paint.weight_paint(stroke=None,mode='NORMAL');
bpy.ops.paint.weight_paint_toggle();
bpy.ops.paint.weight_sample();
bpy.ops.paint.weight_sample_group(group='DEFAULT');
bpy.ops.paint.weight_set();
bpy.ops.paintcurve.add_point(location=(0,0);
bpy.ops.paintcurve.add_point_slide(PAINTCURVE_OT_add_point=None,PAINTCURVE_OT_slide=None
bpy.ops.paintcurve.cursor();
bpy.ops.paintcurve.delete_point();
bpy.ops.paintcurve.draw();
bpy.ops.paintcurve.new();
bpy.ops.paintcurve.select(location=(0,0),toggle=False,extend=False);
bpy.ops.paintcurve.slide(align=False,select=True);
bpy.ops.palette.color_add();
bpy.ops.palette.color_delete();
bpy.ops.palette.new();
bpy.ops.particle.brush_edit(stroke=None);
bpy.ops.particle.connect_hair(all=False);
bpy.ops.particle.delete(type='PARTICLE');
bpy.ops.particle.disconnect_hair(all=False);
bpy.ops.particle.dupliob_copy();
bpy.ops.particle.dupliob_move_down();
bpy.ops.particle.dupliob_move_up();
bpy.ops.particle.dupliob_remove();
bpy.ops.particle.edited_clear();
bpy.ops.particle.hide(unselected=False);
bpy.ops.particle.mirror();
bpy.ops.particle.new();
bpy.ops.particle.new_target();
bpy.ops.particle.particle_edit_toggle();
bpy.ops.particle.rekey(keys_number=2);
bpy.ops.particle.remove_doubles(threshold=0.0002);
bpy.ops.particle.reveal();
bpy.ops.particle.select_all(action='TOGGLE');
bpy.ops.particle.select_less();
bpy.ops.particle.select_linked(deselect=False,location=(0,0);
bpy.ops.particle.select_more();
bpy.ops.particle.select_random(percent=50.0,type='HAIR');
bpy.ops.particle.select_roots(action='SELECT');
bpy.ops.particle.select_tips(action='SELECT');
bpy.ops.particle.subdivide();
bpy.ops.particle.target_move_down();
bpy.ops.particle.target_move_up();
bpy.ops.particle.target_remove();
bpy.ops.particle.weight_set(factor=1.0);
bpy.ops.pose.armature_apply();
bpy.ops.pose.autoside_names(axis='XAXIS');
bpy.ops.pose.bone_layers(layers=T32False);
bpy.ops.pose.breakdown(prev_frame=0,next_frame=0,percentage=0.5);
bpy.ops.pose.constraint_add(type='');
bpy.ops.pose.constraint_add_with_targets(type='');
bpy.ops.pose.constraints_clear();
bpy.ops.pose.constraints_copy();
bpy.ops.pose.copy();
bpy.ops.pose.flip_names();
bpy.ops.pose.group_add();
bpy.ops.pose.group_assign(type=0);
bpy.ops.pose.group_deselect();
bpy.ops.pose.group_move(direction='UP');
bpy.ops.pose.group_remove();
bpy.ops.pose.group_select();
bpy.ops.pose.group_sort();
bpy.ops.pose.group_unassign();
bpy.ops.pose.hide(unselected=False);
bpy.ops.pose.ik_add(with_targets=True);
bpy.ops.pose.ik_clear();
bpy.ops.pose.loc_clear();
bpy.ops.pose.paste(flipped=False,selected_mask=False);
bpy.ops.pose.paths_calculate(start_frame=1,end_frame=250,bake_location='TAILS');
bpy.ops.pose.paths_clear();
bpy.ops.pose.paths_update();
bpy.ops.pose.propagate(mode='WHILE_HELD',end_frame=250.0);
bpy.ops.pose.push(prev_frame=0,next_frame=0,percentage=0.5);
bpy.ops.pose.quaternions_flip();
bpy.ops.pose.relax(prev_frame=0,next_frame=0,percentage=0.5);
bpy.ops.pose.reveal();
bpy.ops.pose.rot_clear();
bpy.ops.pose.rotation_mode_set(type='QUATERNION');
bpy.ops.pose.scale_clear();
bpy.ops.pose.select_all(action='TOGGLE');
bpy.ops.pose.select_constraint_target();
bpy.ops.pose.select_grouped(extend=False,type='LAYER');
bpy.ops.pose.select_hierarchy(direction='PARENT',extend=False);
bpy.ops.pose.select_linked(extend=False);
bpy.ops.pose.select_mirror(only_active=False,extend=False);
bpy.ops.pose.select_parent();
bpy.ops.pose.transforms_clear();
bpy.ops.pose.user_transforms_clear(only_selected=True);
bpy.ops.pose.visual_transform_apply();
bpy.ops.poselib.action_sanitize();
bpy.ops.poselib.apply_pose(pose_index=-1);
bpy.ops.poselib.browse_interactive(pose_index=-1);
bpy.ops.poselib.new();
bpy.ops.poselib.pose_add(frame=1,name='Pose');
bpy.ops.poselib.pose_remove(pose='');
bpy.ops.poselib.pose_rename(name='RenamedPose',pose='');
bpy.ops.poselib.unlink();
bpy.ops.ptcache.add();
bpy.ops.ptcache.bake(bake=False);
bpy.ops.ptcache.bake_all(bake=True);
bpy.ops.ptcache.bake_from_cache();
bpy.ops.ptcache.free_bake();
bpy.ops.ptcache.free_bake_all();
bpy.ops.ptcache.remove();
bpy.ops.render.opengl(animation=False,sequencer=False,write_still=False,view_context=True);
bpy.ops.render.play_rendered_anim();
bpy.ops.render.preset_add(remove_active=False,name='');
bpy.ops.render.render(animation=False,write_still=False,use_viewport=False,layer='',scene='');
bpy.ops.render.view_cancel();
bpy.ops.render.view_show();
bpy.ops.rigidbody.bake_to_keyframes(frame_start=1,frame_end=250,step=1);
bpy.ops.rigidbody.connect(con_type='FIXED',pivot_type='CENTER',connection_pattern='SELECTED_TO_ACTIVE');
bpy.ops.rigidbody.constraint_add(type='FIXED');
bpy.ops.rigidbody.constraint_remove();
bpy.ops.rigidbody.mass_calculate(material='DEFAULT',density=1.0);
bpy.ops.rigidbody.object_add(type='ACTIVE');
bpy.ops.rigidbody.object_remove();
bpy.ops.rigidbody.object_settings_copy();
bpy.ops.rigidbody.objects_add(type='ACTIVE');
bpy.ops.rigidbody.objects_remove();
bpy.ops.rigidbody.shape_change(type='MESH');
bpy.ops.rigidbody.world_add();
bpy.ops.rigidbody.world_remove();
bpy.ops.scene.delete();
bpy.ops.scene.new(type='NEW');
bpy.ops.scene.render_layer_add();
bpy.ops.scene.render_layer_remove();
bpy.ops.screen.actionzone(modifier=0);
bpy.ops.screen.animation_cancel(restore_frame=True);
bpy.ops.screen.animation_play(reverse=False,sync=False);
bpy.ops.screen.animation_step();
bpy.ops.screen.area_join(min_x=-100,min_y=-100,max_x=-100,max_y=-100);
bpy.ops.screen.area_move(x=0,y=0,delta=0);
bpy.ops.screen.area_options();
bpy.ops.screen.area_split(direction='HORIZONTAL',factor=0.5,mouse_x=-100,mouse_y=-100);
bpy.ops.screen.area_swap();
bpy.ops.screen.back_to_previous();
bpy.ops.screen.delete();
bpy.ops.screen.frame_jump(end=False);
bpy.ops.screen.frame_offset(delta=0);
bpy.ops.screen.header();
bpy.ops.screen.header_flip();
bpy.ops.screen.header_toggle_menus();
bpy.ops.screen.header_toolbox();
bpy.ops.screen.keyframe_jump(next=True);
bpy.ops.screen.marker_jump(next=True);
bpy.ops.screen.new();
bpy.ops.screen.redo_last();
bpy.ops.screen.region_blend();
bpy.ops.screen.region_flip();
bpy.ops.screen.region_quadview();
bpy.ops.screen.region_scale();
bpy.ops.screen.repeat_history(index=0);
bpy.ops.screen.repeat_last();
bpy.ops.screen.screen_full_area(use_hide_panels=False);
bpy.ops.screen.screen_set(delta=0);
bpy.ops.screen.screencast(filepath='',full=True);
bpy.ops.screen.screenshot(filepath='',check_existing=True,filter_blender=False,filter_backup=False,filter_image=True,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,display_type='FILE_DEFAULTDISPLAY',full=True);
bpy.ops.screen.spacedata_cleanup();
bpy.ops.screen.userpref_show();
bpy.ops.script.autoexec_warn_clear();
bpy.ops.script.execute_preset(filepath='',menu_idname='');
bpy.ops.script.python_file_run(filepath='');
bpy.ops.script.reload();
bpy.ops.sculpt.brush_stroke(stroke=None,mode='NORMAL',ignore_background_click=False);
bpy.ops.sculpt.detail_flood_fill();
bpy.ops.sculpt.dynamic_topology_toggle();
bpy.ops.sculpt.optimize();
bpy.ops.sculpt.sample_detail_size(location=(0,0);
bpy.ops.sculpt.sculptmode_toggle();
bpy.ops.sculpt.set_detail_size();
bpy.ops.sculpt.set_persistent_base();
bpy.ops.sculpt.symmetrize();
bpy.ops.sculpt.uv_sculpt_stroke(mode='NORMAL');
bpy.ops.sequencer.change_effect_input(swap='A_B');
bpy.ops.sequencer.change_effect_type(type='CROSS');
bpy.ops.sequencer.change_path(filepath='',directory='',files=None,filter_blender=False,filter_backup=False,filter_image=True,filter_movie=True,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.sequencer.copy();
bpy.ops.sequencer.crossfade_sounds();
bpy.ops.sequencer.cut(frame=0,type='SOFT',side='BOTH');
bpy.ops.sequencer.cut_multicam(camera=1);
bpy.ops.sequencer.deinterlace_selected_movies();
bpy.ops.sequencer.delete();
bpy.ops.sequencer.duplicate(mode='TRANSLATION');
bpy.ops.sequencer.duplicate_move(SEQUENCER_OT_duplicate=None,TRANSFORM_OT_translate=None);
bpy.ops.sequencer.effect_strip_add(filepath='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=False,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY',frame_start=0,frame_end=0,channel=1,replace_sel=True,overlap=False,type='CROSS',color=(0.0,0.0,0.0);
bpy.ops.sequencer.gap_insert(frames=10);
bpy.ops.sequencer.gap_remove(all=False);
bpy.ops.sequencer.image_strip_add(directory='',files=None,filter_blender=False,filter_backup=False,filter_image=True,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY',frame_start=0,frame_end=0,channel=1,replace_sel=True,overlap=False);
bpy.ops.sequencer.images_separate(length=1);
bpy.ops.sequencer.lock();
bpy.ops.sequencer.mask_strip_add(frame_start=0,channel=1,replace_sel=True,overlap=False,mask='');
bpy.ops.sequencer.meta_make();
bpy.ops.sequencer.meta_separate();
bpy.ops.sequencer.meta_toggle();
bpy.ops.sequencer.movie_strip_add(filepath='',files=None,filter_blender=False,filter_backup=False,filter_image=False,filter_movie=True,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY',frame_start=0,channel=1,replace_sel=True,overlap=False,sound=True);
bpy.ops.sequencer.movieclip_strip_add(frame_start=0,channel=1,replace_sel=True,overlap=False,clip='');
bpy.ops.sequencer.mute(unselected=False);
bpy.ops.sequencer.offset_clear();
bpy.ops.sequencer.paste();
bpy.ops.sequencer.properties();
bpy.ops.sequencer.reassign_inputs();
bpy.ops.sequencer.rebuild_proxy();
bpy.ops.sequencer.refresh_all();
bpy.ops.sequencer.reload(adjust_length=False);
bpy.ops.sequencer.rendersize();
bpy.ops.sequencer.sample();
bpy.ops.sequencer.scene_strip_add(frame_start=0,channel=1,replace_sel=True,overlap=False,scene='');
bpy.ops.sequencer.select(extend=False,linked_handle=False,left_right='NONE',linked_time=False);
bpy.ops.sequencer.select_active_side(side='BOTH');
bpy.ops.sequencer.select_all(action='TOGGLE');
bpy.ops.sequencer.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.sequencer.select_grouped(extend=False,type='TYPE');
bpy.ops.sequencer.select_handles(side='BOTH');
bpy.ops.sequencer.select_less();
bpy.ops.sequencer.select_linked();
bpy.ops.sequencer.select_linked_pick(extend=False);
bpy.ops.sequencer.select_more();
bpy.ops.sequencer.slip(offset=0);
bpy.ops.sequencer.snap(frame=0);
bpy.ops.sequencer.sound_strip_add(filepath='',files=None,filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=True,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY',frame_start=0,channel=1,replace_sel=True,overlap=False,cache=False);
bpy.ops.sequencer.strip_jump(next=True,center=True);
bpy.ops.sequencer.strip_modifier_add(type='COLOR_BALANCE');
bpy.ops.sequencer.strip_modifier_move(name='Name',direction='UP');
bpy.ops.sequencer.strip_modifier_remove(name='Name');
bpy.ops.sequencer.swap(side='RIGHT');
bpy.ops.sequencer.swap_data();
bpy.ops.sequencer.swap_inputs();
bpy.ops.sequencer.unlock();
bpy.ops.sequencer.unmute(unselected=False);
bpy.ops.sequencer.view_all();
bpy.ops.sequencer.view_all_preview();
bpy.ops.sequencer.view_ghost_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0);
bpy.ops.sequencer.view_selected();
bpy.ops.sequencer.view_toggle();
bpy.ops.sequencer.view_zoom_ratio(ratio=1.0);
bpy.ops.sketch.cancel_stroke();
bpy.ops.sketch.convert();
bpy.ops.sketch.delete();
bpy.ops.sketch.draw_preview(snap=False);
bpy.ops.sketch.draw_stroke(snap=False);
bpy.ops.sketch.finish_stroke();
bpy.ops.sketch.gesture(snap=False);
bpy.ops.sketch.select();
bpy.ops.sound.bake_animation();
bpy.ops.sound.mixdown(filepath='',check_existing=True,filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=True,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.sound.open(filepath='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=True,filter_python=False,filter_font=False,filter_sound=True,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY',cache=False,mono=False);
bpy.ops.sound.open_mono(filepath='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=True,filter_python=False,filter_font=False,filter_sound=True,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY',cache=False,mono=True);
bpy.ops.sound.pack();
bpy.ops.sound.unpack(method='USE_LOCAL',id='');
bpy.ops.sound.update_animation_flags();
bpy.ops.surface.primitive_nurbs_surface_circle_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.surface.primitive_nurbs_surface_curve_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.surface.primitive_nurbs_surface_cylinder_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.surface.primitive_nurbs_surface_surface_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.surface.primitive_nurbs_surface_torus_add(radius=1.0,view_align=False,enter_editmode=False,location=(0.0,0.0,0.0),rotation=(0.0,0.0,0.0),layers=T20False);
bpy.ops.text.autocomplete();
bpy.ops.text.comment();
bpy.ops.text.convert_whitespace(type='SPACES');
bpy.ops.text.copy();
bpy.ops.text.cursor_set(x=0,y=0);
bpy.ops.text.cut();
bpy.ops.text.delete(type='NEXT_CHARACTER');
bpy.ops.text.duplicate_line();
bpy.ops.text.find();
bpy.ops.text.find_set_selected();
bpy.ops.text.indent();
bpy.ops.text.insert(text='');
bpy.ops.text.jump(line=1);
bpy.ops.text.line_break();
bpy.ops.text.line_number();
bpy.ops.text.make_internal();
bpy.ops.text.move(type='LINE_BEGIN');
bpy.ops.text.move_lines(direction='DOWN');
bpy.ops.text.move_select(type='LINE_BEGIN');
bpy.ops.text.new();
bpy.ops.text.open(filepath='',filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=True,filter_font=False,filter_sound=False,filter_text=True,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,display_type='FILE_DEFAULTDISPLAY',internal=False);
bpy.ops.text.overwrite_toggle();
bpy.ops.text.paste(selection=False);
bpy.ops.text.properties();
bpy.ops.text.refresh_pyconstraints();
bpy.ops.text.reload();
bpy.ops.text.replace();
bpy.ops.text.replace_set_selected();
bpy.ops.text.resolve_conflict(resolution='IGNORE');
bpy.ops.text.run_script();
bpy.ops.text.save();
bpy.ops.text.save_as(filepath='',check_existing=True,filter_blender=False,filter_backup=False,filter_image=False,filter_movie=False,filter_python=True,filter_font=False,filter_sound=False,filter_text=True,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.text.scroll(lines=1);
bpy.ops.text.scroll_bar(lines=1);
bpy.ops.text.select_all();
bpy.ops.text.select_line();
bpy.ops.text.select_word();
bpy.ops.text.selection_set(select=False);
bpy.ops.text.start_find();
bpy.ops.text.to_3d_object(split_lines=False);
bpy.ops.text.uncomment();
bpy.ops.text.unindent();
bpy.ops.text.unlink();
bpy.ops.texture.envmap_clear();
bpy.ops.texture.envmap_clear_all();
bpy.ops.texture.envmap_save(layout=(0.0,0.0,1.0,0.0,2.0,0.0,0.0,1.0,1.0,1.0,2.0,1.0),filepath='',check_existing=True,filter_blender=False,filter_backup=False,filter_image=True,filter_movie=True,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.texture.new();
bpy.ops.texture.slot_copy();
bpy.ops.texture.slot_move(type='UP');
bpy.ops.texture.slot_paste();
bpy.ops.time.end_frame_set();
bpy.ops.time.start_frame_set();
bpy.ops.time.view_all();
bpy.ops.transform.bend(value=(0.0),mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),gpencil_strokes=False,release_confirm=False);
bpy.ops.transform.create_orientation(name='',use_view=False,use=False,overwrite=False);
bpy.ops.transform.edge_bevelweight(value=0.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),release_confirm=False);
bpy.ops.transform.edge_crease(value=0.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),release_confirm=False);
bpy.ops.transform.edge_slide(value=0.0,mirror=False,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),correct_uv=False,release_confirm=False);
bpy.ops.transform.mirror(constraint_axis=(False,False,False),constraint_orientation='GLOBAL',proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,gpencil_strokes=False,release_confirm=False);
bpy.ops.transform.push_pull(value=0.0,mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),release_confirm=False);
bpy.ops.transform.resize(value=(1.0,1.0,1.0),constraint_axis=(False,False,False),constraint_orientation='GLOBAL',mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),gpencil_strokes=False,texture_space=False,remove_on_cancel=False,release_confirm=False);
bpy.ops.transform.rotate(value=0.0,axis=(0.0,0.0,0.0),constraint_axis=(False,False,False),constraint_orientation='GLOBAL',mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),gpencil_strokes=False,release_confirm=False);
bpy.ops.transform.select_orientation(orientation='GLOBAL');
bpy.ops.transform.seq_slide(value=(0.0,0.0),snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),release_confirm=False);
bpy.ops.transform.shear(value=0.0,mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),gpencil_strokes=False,release_confirm=False);
bpy.ops.transform.shrink_fatten(value=0.0,mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),release_confirm=False);
bpy.ops.transform.skin_resize(value=(1.0,1.0,1.0),constraint_axis=(False,False,False),constraint_orientation='GLOBAL',mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),release_confirm=False);
bpy.ops.transform.tilt(value=0.0,mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),release_confirm=False);
bpy.ops.transform.tosphere(value=0.0,mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),gpencil_strokes=False,release_confirm=False);
bpy.ops.transform.trackball(value=(0.0,0.0),mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),gpencil_strokes=False,release_confirm=False);
bpy.ops.transform.transform(mode='TRANSLATION',value=(0.0,0.0,0.0,0.0),axis=(0.0,0.0,0.0),constraint_axis=(False,False,False),constraint_orientation='GLOBAL',mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),release_confirm=False);
bpy.ops.transform.translate(value=(0.0,0.0,0.0),constraint_axis=(False,False,False),constraint_orientation='GLOBAL',mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1.0,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),gpencil_strokes=False,texture_space=False,remove_on_cancel=False,release_confirm=False);
bpy.ops.transform.vert_slide(value=0.0,mirror=False,snap=False,snap_target='CLOSEST',snap_point=(0.0,0.0,0.0),snap_align=False,snap_normal=(0.0,0.0,0.0),release_confirm=False);
bpy.ops.ui.data_path_button();
bpy.ops.ui.to_selected_button(all=True);
bpy.ops.ui.drop_color(color=(0.0,0.0,0.0),gamma=False);
bpy.ops.ui.editsource();
bpy.ops.ui.edittranslation_init();
bpy.ops.ui.eyedropper_color();
bpy.ops.ui.eyedropper_id();
bpy.ops.ui.reloadtranslation();
bpy.ops.ui.reports_to_textblock();
bpy.ops.ui.reset_default_button(all=True);
bpy.ops.ui.reset_default_theme();
bpy.ops.ui.unset_property_button();
bpy.ops.uv.align(axis='ALIGN_AUTO');
bpy.ops.uv.average_islands_scale();
bpy.ops.uv.circle_select(x=0,y=0,radius=1,gesture_mode=0);
bpy.ops.uv.cube_project(cube_size=1.0,correct_aspect=True,clip_to_bounds=False,scale_to_bounds=False);
bpy.ops.uv.cursor_set(location=(0.0,0.0);
bpy.ops.uv.cylinder_project(direction='VIEW_ON_EQUATOR',align='POLAR_ZX',radius=1.0,correct_aspect=True,clip_to_bounds=False,scale_to_bounds=False);
bpy.ops.uv.follow_active_quads(mode='LENGTH_AVERAGE');
bpy.ops.uv.hide(unselected=False);
bpy.ops.uv.lightmap_pack(PREF_CONTEXT='SEL_FACES',PREF_PACK_IN_ONE=True,PREF_NEW_UVLAYER=False,PREF_APPLY_IMAGE=False,PREF_IMG_PX_SIZE=512,PREF_BOX_DIV=12,PREF_MARGIN_DIV=0.1);
bpy.ops.uv.mark_seam();
bpy.ops.uv.minimize_stretch(fill_holes=True,blend=0.0,iterations=0);
bpy.ops.uv.pack_islands(rotate=True,margin=0.001);
bpy.ops.uv.pin(clear=False);
bpy.ops.uv.project_from_view(orthographic=False,camera_bounds=True,correct_aspect=True,clip_to_bounds=False,scale_to_bounds=False);
bpy.ops.uv.remove_doubles(threshold=0.02,use_unselected=False);
bpy.ops.uv.reset();
bpy.ops.uv.reveal();
bpy.ops.uv.seams_from_islands(mark_seams=True,mark_sharp=False);
bpy.ops.uv.select(extend=False,location=(0.0,0.0);
bpy.ops.uv.select_all(action='TOGGLE');
bpy.ops.uv.select_border(pinned=False,gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.uv.select_lasso(path=None,deselect=False,extend=True);
bpy.ops.uv.select_less();
bpy.ops.uv.select_linked(extend=False);
bpy.ops.uv.select_linked_pick(extend=False,location=(0.0,0.0);
bpy.ops.uv.select_loop(extend=False,location=(0.0,0.0);
bpy.ops.uv.select_more();
bpy.ops.uv.select_pinned();
bpy.ops.uv.select_split();
bpy.ops.uv.smart_project(angle_limit=66.0,island_margin=0.0,user_area_weight=0.0,use_aspect=True);
bpy.ops.uv.snap_cursor(target='PIXELS');
bpy.ops.uv.snap_selected(target='PIXELS');
bpy.ops.uv.sphere_project(direction='VIEW_ON_EQUATOR',align='POLAR_ZX',correct_aspect=True,clip_to_bounds=False,scale_to_bounds=False);
bpy.ops.uv.stitch(use_limit=False,snap_islands=True,limit=0.01,static_island=0,midpoint_snap=False,clear_seams=True,mode='VERTEX',stored_mode='VERTEX',selection=None);
bpy.ops.uv.tile_set(tile=(0,0);
bpy.ops.uv.unwrap(method='ANGLE_BASED',fill_holes=True,correct_aspect=True,use_subsurf_data=False,margin=0.001);
bpy.ops.uv.weld();
bpy.ops.view2d.ndof();
bpy.ops.view2d.pan(deltax=0,deltay=0);
bpy.ops.view2d.reset();
bpy.ops.view2d.scroll_down(deltax=0,deltay=0,page=False);
bpy.ops.view2d.scroll_left(deltax=0,deltay=0);
bpy.ops.view2d.scroll_right(deltax=0,deltay=0);
bpy.ops.view2d.scroll_up(deltax=0,deltay=0,page=False);
bpy.ops.view2d.scroller_activate();
bpy.ops.view2d.smoothview(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0);
bpy.ops.view2d.zoom(deltax=0.0,deltay=0.0);
bpy.ops.view2d.zoom_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0);
bpy.ops.view2d.zoom_in(zoomfacx=0.0,zoomfacy=0.0);
bpy.ops.view2d.zoom_out(zoomfacx=0.0,zoomfacy=0.0);
bpy.ops.view3d.background_image_add(name='Image',filepath='',filter_blender=False,filter_backup=False,filter_image=True,filter_movie=True,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=9,relative_path=True,display_type='FILE_DEFAULTDISPLAY');
bpy.ops.view3d.background_image_remove(index=0);
bpy.ops.view3d.camera_to_view();
bpy.ops.view3d.camera_to_view_selected();
bpy.ops.view3d.clear_render_border();
bpy.ops.view3d.clip_border(xmin=0,xmax=0,ymin=0,ymax=0);
bpy.ops.view3d.copybuffer();
bpy.ops.view3d.cursor3d();
bpy.ops.view3d.dolly(delta=0,mx=0,my=0);
bpy.ops.view3d.edit_mesh_extrude_individual_move();
bpy.ops.view3d.edit_mesh_extrude_move_normal();
bpy.ops.view3d.edit_mesh_extrude_move_shrink_fatten();
bpy.ops.view3d.enable_manipulator(translate=False,rotate=False,scale=False);
bpy.ops.view3d.fly();
bpy.ops.view3d.game_start();
bpy.ops.view3d.layers(nr=1,extend=False,toggle=True);
bpy.ops.view3d.localview();
bpy.ops.view3d.manipulator(constraint_axis=(False,False,False),constraint_orientation='GLOBAL',release_confirm=False);
bpy.ops.view3d.move();
bpy.ops.view3d.navigate();
bpy.ops.view3d.ndof_all();
bpy.ops.view3d.ndof_orbit();
bpy.ops.view3d.ndof_orbit_zoom();
bpy.ops.view3d.ndof_pan();
bpy.ops.view3d.object_as_camera();
bpy.ops.view3d.pastebuffer();
bpy.ops.view3d.properties();
bpy.ops.view3d.render_border(xmin=0,xmax=0,ymin=0,ymax=0,camera_only=False);
bpy.ops.view3d.rotate();
bpy.ops.view3d.ruler();
bpy.ops.view3d.select(extend=False,deselect=False,toggle=False,center=False,enumerate=False,object=False,location=(0,0);
bpy.ops.view3d.select_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0,extend=True);
bpy.ops.view3d.select_circle(x=0,y=0,radius=1,gesture_mode=0);
bpy.ops.view3d.select_lasso(path=None,deselect=False,extend=True);
bpy.ops.view3d.select_menu(name='',toggle=False);
bpy.ops.view3d.select_or_deselect_all(extend=False,toggle=False,deselect=False,center=False,enumerate=False,object=False);
bpy.ops.view3d.smoothview();
bpy.ops.view3d.snap_cursor_to_active();
bpy.ops.view3d.snap_cursor_to_center();
bpy.ops.view3d.snap_cursor_to_grid();
bpy.ops.view3d.snap_cursor_to_selected();
bpy.ops.view3d.snap_selected_to_cursor(use_offset=True);
bpy.ops.view3d.snap_selected_to_grid();
bpy.ops.view3d.toolshelf();
bpy.ops.view3d.view_all(use_all_regions=False,center=False);
bpy.ops.view3d.view_center_camera();
bpy.ops.view3d.view_center_cursor();
bpy.ops.view3d.view_center_lock();
bpy.ops.view3d.view_center_pick();
bpy.ops.view3d.view_lock_clear();
bpy.ops.view3d.view_lock_to_active();
bpy.ops.view3d.view_orbit(type='ORBITLEFT');
bpy.ops.view3d.view_pan(type='PANLEFT');
bpy.ops.view3d.view_persportho();
bpy.ops.view3d.view_roll(angle=0.0,type='ROLLANGLE');
bpy.ops.view3d.view_selected(use_all_regions=False);
bpy.ops.view3d.viewnumpad(type='LEFT',align_active=False);
bpy.ops.view3d.walk();
bpy.ops.view3d.zoom(delta=0,mx=0,my=0);
bpy.ops.view3d.zoom_border(gesture_mode=0,xmin=0,xmax=0,ymin=0,ymax=0);
bpy.ops.view3d.zoom_camera_1_to_1();
bpy.ops.wm.addon_disable(module='');
bpy.ops.wm.addon_enable(module='');
bpy.ops.wm.addon_expand(module='');
bpy.ops.wm.addon_install(overwrite=True,target='DEFAULT',filepath='',filter_folder=True,filter_python=True,filter_glob='*.py;*.zip');
bpy.ops.wm.addon_refresh();
bpy.ops.wm.addon_remove(module='');
bpy.ops.wm.appconfig_activate(filepath='');
bpy.ops.wm.appconfig_default();
bpy.ops.wm.append(filepath='',directory='',filename='',files=None,filter_blender=True,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=1,display_type='FILE_DEFAULTDISPLAY',link=False,autoselect=True,active_layer=True,instance_groups=False);
bpy.ops.wm.blenderplayer_start();
bpy.ops.wm.call_menu(name='');
bpy.ops.wm.call_menu_pie(name='');
bpy.ops.wm.context_collection_boolean_set(data_path_iter='',data_path_item='',type='TOGGLE');
bpy.ops.wm.context_cycle_array(data_path='',reverse=False);
bpy.ops.wm.context_cycle_enum(data_path='',reverse=False);
bpy.ops.wm.context_cycle_int(data_path='',reverse=False);
bpy.ops.wm.context_menu_enum(data_path='');
bpy.ops.wm.context_modal_mouse(data_path_iter='',data_path_item='',header_text='',input_scale=0.01,invert=False,initial_x=0);
bpy.ops.wm.context_pie_enum(data_path='');
bpy.ops.wm.context_scale_float(data_path='',value=1.0);
bpy.ops.wm.context_scale_int(data_path='',value=1.0,always_step=True);
bpy.ops.wm.context_set_boolean(data_path='',value=True);
bpy.ops.wm.context_set_enum(data_path='',value='');
bpy.ops.wm.context_set_float(data_path='',value=0.0,relative=False);
bpy.ops.wm.context_set_id(data_path='',value='');
bpy.ops.wm.context_set_int(data_path='',value=0,relative=False);
bpy.ops.wm.context_set_string(data_path='',value='');
bpy.ops.wm.context_set_value(data_path='',value='');
bpy.ops.wm.context_toggle(data_path='');
bpy.ops.wm.context_toggle_enum(data_path='',value_1='',value_2='');
bpy.ops.wm.prev_settings();
bpy.ops.wm.debug_menu(debug_value=0);
bpy.ops.wm.dependency_relations();
bpy.ops.wm.doc_view(doc_id='');
bpy.ops.wm.doc_view_manual(doc_id='');
bpy.ops.wm.interaction_preset_add(remove_active=False,name='');
bpy.ops.wm.interface_theme_preset_add(remove_active=False,name='');
bpy.ops.wm.keyconfig_activate(filepath='');
bpy.ops.wm.keyconfig_export(filepath='keymap.py',filter_folder=True,filter_text=True,filter_python=True);
bpy.ops.wm.keyconfig_import(filepath='keymap.py',filter_folder=True,filter_text=True,filter_python=True,keep_original=True);
bpy.ops.wm.keyconfig_preset_add(remove_active=False,name='');
bpy.ops.wm.keyconfig_remove();
bpy.ops.wm.keyconfig_test();
bpy.ops.wm.keyitem_add();
bpy.ops.wm.keyitem_remove(item_id=0);
bpy.ops.wm.keyitem_restore(item_id=0);
bpy.ops.wm.keymap_restore(all=False);
bpy.ops.wm.link(filepath='',directory='',filename='',files=None,filter_blender=True,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=1,relative_path=True,display_type='FILE_DEFAULTDISPLAY',link=True,autoselect=True,active_layer=True,instance_groups=True);
bpy.ops.wm.memory_statistics();
bpy.ops.wm.open_mainfile(filepath='',filter_blender=True,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=8,display_type='FILE_DEFAULTDISPLAY',load_ui=True,use_scripts=True);
bpy.ops.wm.operator_cheat_sheet();
bpy.ops.wm.operator_defaults();
bpy.ops.wm.operator_pie_enum(data_path='',prop_string='');
bpy.ops.wm.operator_preset_add(remove_active=False,name='',operator='');
bpy.ops.wm.path_open(filepath='');
bpy.ops.wm.properties_add(data_path='');
bpy.ops.wm.properties_context_change(context='');
bpy.ops.wm.properties_edit(data_path='',property='',value='',min=-10000,max=10000.0,description='');
bpy.ops.wm.properties_remove(data_path='',property='');
bpy.ops.wm.quit_blender();
bpy.ops.wm.radial_control(data_path_primary='',data_path_secondary='',use_secondary='',rotation_path='',color_path='',fill_color_path='',zoom_path='',image_id='',secondary_tex=False);
bpy.ops.wm.read_factory_settings();
bpy.ops.wm.read_history();
bpy.ops.wm.read_homefile(filepath='',load_ui=True);
bpy.ops.wm.recover_auto_save(filepath='',filter_blender=True,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=False,filemode=8,display_type='FILE_LONGDISPLAY');
bpy.ops.wm.recover_last_session();
bpy.ops.wm.redraw_timer(type='DRAW',iterations=10);
bpy.ops.wm.revert_mainfile(use_scripts=True);
bpy.ops.wm.save_as_mainfile(filepath='',check_existing=True,filter_blender=True,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=8,display_type='FILE_DEFAULTDISPLAY',compress=False,relative_remap=True,copy=False,use_mesh_compat=False);
bpy.ops.wm.save_homefile();
bpy.ops.wm.save_mainfile(filepath='',check_existing=True,filter_blender=True,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_btx=False,filter_collada=False,filter_folder=True,filemode=8,display_type='FILE_DEFAULTDISPLAY',compress=False,relative_remap=False);
bpy.ops.wm.save_userpref();
bpy.ops.wm.search_menu();
bpy.ops.wm.splash();
bpy.ops.wm.sysinfo();
bpy.ops.wm.theme_install(overwrite=True,filepath='',filter_folder=True,filter_glob='*.xml');
bpy.ops.wm.url_open(url='');
bpy.ops.wm.userpref_autoexec_path_add();
bpy.ops.wm.userpref_autoexec_path_remove(index=0);
bpy.ops.wm.window_duplicate();
bpy.ops.wm.window_fullscreen_toggle();
bpy.ops.world.new();



----bpy_extras----------------------------------------------------------------------
AddObjectHelper
ExportHelper
ImportHelper
add_object_align_init(context=,operator=));
area_tri(v1=,v2=,v3=);
aspect(fontid=,aspect=));
axis_conversion(from_forward='Y'=,from_up='Z'=,to_forward='Y'=,to_up='Z');
axis_conversion_ensure(operator=,forward_attr=,up_attr=);
bake_action(frame_start=,frame_end=,frame_step=1=,only_selected=False,do_pose=True,do_object=True,do_visual_keying=True,do_constraint_clear=False,do_parents_clear=False,do_clean=False,action=None);
barycentric_transform(point=,tri_a1=,tri_a2=,tri_a3=,tri_b1=,tri_b2=,tri_b3=);
blur(fontid=,radius=);
box_fit_2d(points=));
box_pack_2d(boxes=);
cell(position=);
cell_vector(position);
clipping(fontid=,xmin=,ymin=,xmax=,ymax);
convex_hull_2d(points=);
create_derived_objects(scene=,ob=);
dimensions(fontid=,text=);
disable(fontid=,option=);
distance_point_to_plane(pt=,plane_co=,plane_no);
draw(fontid=,text=);
edge_face_count(mesh=);
edge_face_count_dict(mesh=);
edge_loops_from_edges(mesh=,edges=None);
edge_loops_from_tessfaces(mesh=,tessfaces=None=,seams=());
edge_rotate(edge=,ccw=False);
edge_split(edge=,vert=,fac=);
enable(fontid=,option=);
export_shader(scene=,material=);
face_flip(faces=);
face_join(faces=,remove=True);
face_random_points(num_points=,tessfaces=);
face_split(face=,vert_a=,vert_b=,coords=();=,use_exist=True,example=None);
face_split_edgenet(face=,edgenet=);
face_vert_separate(face=,vert=);
fractal(position=,H=,lacunarity=,octaves=,noise_basis=noise.types.STDPERLIN);
free_derived_objects(ob=);
from_edit_mesh(mesh=);
glAccum glAlphaFunc glAreTexturesResident glBegin glBindTexture glBitmap glBlendFunc glCallList glCallLists glClear glClearAccum glClearColor glClearDepth glClearIndex glClearStencil glClipPlane glColor glColorMask glColorMaterial glCopyPixels glCullFace glDeleteLists glDeleteTextures glDepthFunc glDepthMask glDepthRange glDisable glDrawBuffer glDrawPixels glEdgeFlag glEnable glEnd glEndList glEvalCoord glEvalMesh glEvalPoint glFeedbackBuffer glFinish glFlush glFog glFrontFace glFrustum glGenLists glGenTextures glGet glGetClipPlane glGetError glGetLight glGetMap glGetMaterial glGetPixelMap glGetPolygonStipple glGetString glGetTexEnv glGetTexGen glGetTexImage glGetTexLevelParameter glGetTexParameter glHint glIndex glInitNames glIsEnabled glIsList glIsTexture glLight glLightModel glLineStipple glLineWidth glListBase glLoadIdentity glLoadMatrix glLoadName glLogicOp glMap1 glMap2 glMapGrid glMaterial glMatrixMode glMultMatrix glNewList glNormal3 glOrtho glPassThrough glPixelMap glPixelStore glPixelTransfer glPixelZoom glPointSize glPolygonMode glPolygonOffset glPolygonStipple glPopAttrib glPopClientAttrib glPopMatrix glPopName glPrioritizeTextures glPushAttrib glPushClientAttrib glPushMatrix glPushName glRasterPos glReadBuffer glReadPixels glRect glRenderMode glRotate glScale glScissor glSelectBuffer glShadeModel glStencilFuc glStencilMask glStencilOp glTexCoord glTexEnv glTexGen glTexImage1D glTexImage2D glTexParameter glTranslate glVertex glViewport gluLookAt gluOrtho2D gluPerspective gluPickMatrix gluProject gluUnProject
hetero_terrain(position=,H=,lacunarity=,octaves=,offset=,noise_basis=noise.types.STDPERLIN);
hybrid_multi_fractal(position=,H=,lacunarity=,octaves=,offset=,gain=,noise_basis=noise.types.STDPERLIN);
interpolate_bezier(knot1=,handle1=,handle2=,knot2=,resolution=);
intersect_line_line(v1=,v2=,v3=,v4=);
intersect_line_line_2d(lineA_p1=,lineA_p2=,lineB_p1=,lineB_p2=);
intersect_line_plane(line_a=,line_b=,plane_co=,plane_no=,no_flip=False);
intersect_line_sphere(line_a=,line_b=,sphere_co=,sphere_radius=,clip=True);
intersect_line_sphere_2d(line_a=,line_b=,sphere_co=,sphere_radius=,clip=True);
intersect_plane_plane(plane_a_co=,plane_a_no=,plane_b_co=,plane_b_no=);
intersect_point_line(pt=,line_p1=,line_p2=);
intersect_point_quad_2d(pt=,quad_p1=,quad_p2=,quad_p3=,quad_p4=);
intersect_point_tri(pt=,tri_p1=,tri_p2=,tri_p3=);
intersect_point_tri_2d(pt=,tri_p1=,tri_p2=,tri_p3=);
intersect_ray_tri(v1=,v2=,v3=,ray=,orig=,clip=True);
intersect_sphere_sphere_2d(p_a=,radius_a=,p_b=,radius_b=);
keyconfig_export(wm=,kc=,filepath=);
keyconfig_merge(kc1=,kc2=);
keyconfig_test(kc=);
km_exists_in(km=,export_keymaps=);
load(filename=);
load_image(imagepath=,dirname=''=,place_holder=False,recursive=False,ncase_cmp=True,convert_callback=None=,verbose=False,relpath=None);
location_3d_to_region_2d(region=,rv3d=,coord=);
loop_separate(loop=);
mesh_linked_tessfaces(mesh=);
mesh_linked_uv_islands(mesh=);
multi_fractal(position=,H=,lacunarity=,octaves=,noise_basis=noise.types.STDPERLIN);
ngon_tessellate(from_data=,indices=,fix_loops=True);
noise(position=,noise_basis=noise.types.STDPERLIN);
noise_vector(position=,noise_basis=noise.types.STDPERLIN);
object_add_grid_scale(context=);
object_add_grid_scale_apply_operator(operator=,context=);
object_data_add(context=,obdata=,operator=None=,use_active_layer=True,name=None);
object_image_guess(obj=,bm=None);
path_reference(filepath=,base_src=,base_dst=,mode='AUTO'=,subdir=''=,set=None=,library=None);
path_reference_copy(set=,report=<built-in_function_print=>);
path_reference_mode
points_in_planes(planes=);
position(fontid=,x=,y=,z=);
random_unit_vector(size=3);
region_2d_to_location_3d(region=,rv3d=,coord=,depth_location=);
region_2d_to_origin_3d(region=,rv3d=,coord=);
region_2d_to_vector_3d(region=,rv3d=,coord=);
ridged_multi_fractal(position=,H=,lacunarity=,octaves=,offset=,gain=,noise_basis=noise.types.STDPERLIN);
rotation(fontid=,angle=);
seed_set(seed=);
shadow(fontid=,level=,r=,g=,b=,a=);
shadow_offset(fontid=,x=,y=);
size(fontid=,size=,dpi=);
tessellate_polygon(veclist_list=);
to_list();
turbulence(position=,octaves=,hard=,noise_basis=noise.types.STDPERLIN=,amplitude_scale=0.5=,frequency_scale=2.0);
turbulence_vector(position=,octaves=,hard=,noise_basis=noise.types.STDPERLIN=,amplitude_scale=0.5=,frequency_scale=2.0);
unique_name(key=,name=,name_dict=,name_max=-1=,clean_func=None=,sep='.');
unload(filename=);
unpack_face_list(list_of_tuples=);
unpack_list(list_of_tuples=);
variable_lacunarity(position=,distortion=,noise_type1=noise.types.STDPERLIN=,noise_type2=noise.types.STDPERLIN);
vert_collapse_edge(vert=,edge=);
vert_collapse_faces(vert=,edge=,fac=,join_faces=);
vert_dissolve(vert);
vert_separate(vert=,edges=);
volume_tetrahedron(v1=,v2=,v3=,v4=);
voronoi(position=,distance_metric=noise.distance_metrics.DISTANCE=,exponent=2.5);
world_to_camera_view(scene=,obj=,coord=);



----bpy.app----------------------------------------------------------------------
:
{
}
*

abspath(path,start=None,library=None);
 anim app background binary_path blend_paths boid build_cflags build_cxxflags build_date build_linkflags build_platform build_revision build_system build_time build_type buttons clean_name console context data debug debug_events debug_ffmpeg debug_python debug_value debug_wm display_name display_name_from_filepath dpaint driver_namespace ed ensure_ext events export_anim export_mesh export_scene file font frame_change_post frame_change_pre gpencil graph group handlers import_anim import_curve import_mesh import_scene info is_subdir keyconfig_set load_post load_pre load_scripts logic manual_map marker mask mball module_names modules_from_path nla node ops outliner paint particle path persistent pose poselib preset_find preset_paths props ptcache refresh_script_paths register_class register_manual_map register_module relpath render_cancel render_complete render_post render_pre render_stats resolve_ncase resource_path save_post save_pre scene_update_post scene_update_pre script script_path_pref script_path_user script_paths sculpt sequencer sketch smpte_from_frame smpte_from_seconds sound surface tempdir text time types ui unregister_class unregister_manual_map unregister_module user_resource utils version version_char version_cycle version_string view2d view3d wm world

bpy.context.---------
active_base active_bone active_gpencil_frame active_gpencil_layer active_node active_object active_operator active_pose_bone area armature blend_data bone brush camera cloth collision curve dynamic_paint edit_bone edit_image edit_mask edit_movieclip edit_object edit_text editable_bones editable_gpencil_layers editable_gpencil_strokes fluid gpencil_data gpencil_data_owner image_paint_object lamp lattice line_style material material_slot mesh meta_ball mode object particle_edit_object particle_settings particle_system particle_system_editable pose_bone region region_data scene screen sculpt_object selectable_bases selectable_objects selected_bases selected_editable_bases selected_editable_bones selected_editable_objects selected_editable_sequences selected_nodes selected_objects selected_pose_bones selected_sequences sequences smoke soft_body space_data speaker texture texture_slot texture_user texture_user_property tool_settings user_preferences vertex_paint_object visible_bases visible_bones visible_gpencil_layers visible_objects visible_pose_bones window window_manager world



----Purple-----------------------
print  continue for  return  while  break


def  CLIB函数():
Lf3_oCo oMv_Lf3 oMv_Ψ2f 

----PYLIB-------------------------------------------------
atan3LIB   iΔ圆心与半径LIB  fΔΔ知三点对角弧 fΔΔ两乛夹角弧正 fΔΔ从乛一逆转到乛二弧正 ΔΔ角对边乛LIB fΔΔ加弧正真 f2巜f2十f2  f2十f2_f2 f2巜f2一f2  f2一f2_f2 f3一f3_f3  f3Χf_f3   f3巜f3十f3  f3巜f3Χf f2Χf_f2  f3十f3_f3  f3巜f3一f3  f巜f2乛f2 length length1 f2_f2  f巜f3λf3  f巜f3Γf3 f巜vΓv vLoc_m v巜f3十f3 v巜f3一f3 f3十f3_ f3巜f3十f3Ξ2 f2巜f2十f2Ξ2  iΔΔ找最近一个元素LIB fΔΔ两点对角线长 ΔΔ知弧点给f2四真 bΔΔ检测总弧是否顺时针 f2ΔΔ从乛一逆转弧后的乛  f3ΔΔ角对边乛LIB  fΔΔ两f2夹角弧正LIB  fΔΔ两f3夹角弧LIB fΔΔ两m夹角弧LIB m3ΔΔ两乛生成m3 TΔΔ减LIB  TΔΔ加LIB  TΔΔ乘LIB  TΔΔ除LIB m巜m3_m  m3_m_ f3ΔΔf3生成指数曲线LIB f3ΔΔm得f3位LIB vΔΔm得v位LIB mΔΔm移位LIB ΔΔm移位LIB  f16巜m  m巜f16  m巜2v  m3巜2v cf33巜2v vΔΔ矩阵提取轴LIB  v_f3_ Lcf3巜Lf3  cf3巜f3  cf2巜f2 cf33巜m3 v巜f3 LLcf3巜LLf3 f2巜cf2 f3巜cf3 m3巜f33 Lf3巜Lcf3 f3Γf3_f3 Lv巜Lcf3 p2cf  Ψ3cf p4cf  Ψ2ci Lci巜Li Lcf巜Lf  cmp_f3 Δ隐显物LIB clamp_min clamp_max rotateV 

----global_var--------------------------
G DLL _卐DLL LIB LIBG 
t3黑LIB t3白LIB t3灰LIB t3浅黑LIB t3灰蓝LIB t3灰青LIB t3红LIB t3绿LIB t3青LIB t3蓝LIB t3紫LIB t3粉紫LIB t3深红LIB t3深绿LIB t3深蓝LIB t4青LIB t4黄LIB t4深绿LIB 
ci2LIB ci3LIB ci4LIB cf2LIB cf3LIB cf4LIB cf33LIB cf44LIB 
b停止更新G  dllCLIB dllTEST dllIMDJS dllMESH space节点LIB region节点LIB


----画画--------------------------
Lv法线位画LIB Lv法线顶位画LIB L物序L4v位矩阵画LIB Lv位实物画LIB Lcf3位画LIB Lcf3位蓝画LIB L条序Lv线段序画LIB LL2cf3线段序画LIB L条序LΩωv线段画LIB Lv三角面位画LIB Lv物位蓝LIB  Lv位实物顶LIB Lt3红绿蓝LIB Li显示2dLIB Li显示3dLIB 


==字典==========
ID_PLUGIN
doc
docS
op
command
register
unregister
percentage
icon
bepuik
----导出obj关键字--------
mtllib usemtl vt vn f s o

--blender script Func--------
bl_info CopySelectedObjectConstraints CopySelectedObjectModifiers CopySelectedPoseConstraints INFO_MT_mesh_add OBJECT_PT_keys_status ScreencastKeysStatus ScreencastKeysTimerReset SetupMathView VIEW3D_MT_edit_mesh_edges VIEW3D_MT_AddMenu VIEW3D_MT_AlignMenu VIEW3D_MT_ArmatureName VIEW3D_MT_assign_material VIEW3D_MT_copypopup VIEW3D_MT_CursorMenu VIEW3D_MT_edit_multi VIEW3D_MT_edit_TK VIEW3D_MT_EditArmatureTK VIEW3D_MT_EditCursorMenu VIEW3D_MT_EditCurveCtrlpoints VIEW3D_MT_EditCurveSegments VIEW3D_MT_EditCurveSpecials VIEW3D_MT_editM_Edge VIEW3D_MT_GroupMenu VIEW3D_MT_KeyframeMenu VIEW3D_MT_make_links VIEW3D_MT_master_material VIEW3D_MT_MirrorMenu VIEW3D_MT_ParentMenu VIEW3D_MT_PoseCopy VIEW3D_MT_posecopypopup VIEW3D_MT_PoseNames VIEW3D_MT_select_material VIEW3D_MT_SelectArmatureMenu VIEW3D_MT_SelectCurveMenu VIEW3D_MT_SelectEditMenu VIEW3D_MT_SelectMenu VIEW3D_MT_SelectMetaball VIEW3D_MT_SelectPoseMenu VIEW3D_MT_SelectSurface VIEW3D_MT_Space_Dynamic_Menu VIEW3D_MT_TransformMenu VIEW3D_MT_undoS  VIEW3D_OT_activate_measure_panel VIEW3D_OT_assign_material VIEW3D_OT_clean_material_slots VIEW3D_OT_CursorToEdgeIntersection VIEW3D_OT_display_measurements VIEW3D_OT_material_remove VIEW3D_OT_material_to_texface VIEW3D_OT_pivot_cursor VIEW3D_OT_reenter_editmode VIEW3D_OT_replace_material VIEW3D_OT_revert_pivot VIEW3D_OT_select_material_by_name VIEW3D_OT_texface_to_material  VIEW3D_PT_3dnavigationPanel VIEW3D_PT_math_vis VIEW3D_PT_measure VIEW3D_PT_tools_objectmode VIEW3D_PT_tools_meshedit VIEW3D_PT_tools_curveedit VIEW3D_PT_tools_surfaceedit VIEW3D_PT_tools_armatureedit VIEW3D_PT_tools_mballedit VIEW3D_PT_tools_latticeedit VIEW3D_PT_tools_posemode VIEW3D_PT_transform_orientations VIEW3D_PT_view3d_properties
VIEW3D_PT_view3d_display  #显示方式
VIEW3D_PT_view3d_meshdisplay #网格显示面板


----cython--------------------------
cdef cimport cython parallel prange threadid clock 
libc stdlib auto do  bool char float int long str  static  volatile unsigned extern 
malloc realloc rand srand 
NULL 

--poser---------------------------------
otherActor hip abdomen chest neck head lCollor lShoulder rShoulder lArm rArm lForarm rForarm lHand rHand lThumber1 lThumber2 lThumber3 rThumber1 rThumber2 rThumber3 lIndex1 lIndex2 lIndex3 rIndex1 rIndex2 rIndex3 lRing1 lRing2 lRing3 rRing1 rRing2 rRing3 lPinky1 lPinky2 lPinky3 rPinky1 rPinky2 rPinky3 lEye rEye 
GL_BLEND GL_LINES
\
[
]
.



--OPENGL--------------------------------------------------------------------------
--glColor
glColor3b glColor3d glColor3f glColor3i glColor3s glColor3ub glColor3ui glColor3us glColor4b glColor4d glColor4f glColor4i glColor4s glColor4ub glColor4ui glColor4us glColor3bv glColor3dv glColor3fv glColor3iv glColor3sv glColor3ubv glColor3uiv glColor3usv glColor4bv glColor4dv glColor4fv glColor4iv glColor4sv glColor4ubv glColor4uiv glColor4usv --glVertex glVertex2d glVertex2f glVertex2i glVertex2s glVertex3d glVertex3f glVertex3i glVertex3s glVertex4d glVertex4f glVertex4i glVertex4s glVertex2dv glVertex2fv glVertex2iv glVertex2sv glVertex3dv glVertex3fv glVertex3iv glVertex3sv glVertex4dv glVertex4fv glVertex4iv glVertex4sv
----内置PYLIB--------------------------------------------------------
sΔ名字增量LIB sΔ提取当前文件夹目录LIB Δ替换字符LIB Ls_sΔ读取文本LIB Δ从硬盘删除LIB iΔ删除重复文件LIB DΔ读取一个文件为字典LIB Δ字典写入硬盘LIB Δ读取文件并写入wmLIB Δ从硬盘导入LIB sΔ从硬盘读取LIB Δ打开文件夹LIB PTfnn Δ删除物LIB oΔ新建物LIB oΔ复制物LIB  Δ复制物LIB SWAP 


----临时addons关键字----------------------------------------------------
----cubesurfer--------------------------
mciso 
----临时C函数--------------------------------------------------------
----hairmesher------
Δ毛发点数面数 ΔΔ一毛发构建点面 fΔ创建粒子一毛发 Δ创建渐变材质 ΔΔ毛得最近头皮面ξlast Δ初始化V毛序V检测ξ面lastGG  ΔΔ收集毛发权 ΔΔ删除相近毛 Δ初始化V毛序Vξ面最近头皮序G ΔΔ收集面位法LIB bΔV毛序V检测ξ面lastG是空 bΔV毛序Vξ面最近头皮序G是空 Δ初始化V毛序V检测ξ面lastG 
#------------------------------
 Δ毛点减点 fΔ创建粒子毛发 Δ毛发点数面数 ΔΔ毛发构建点面 Δ初始化V毛序Vξ面最近头皮序GG Δ初始化V毛序V检测ξ面lastGG  ΔΔ得毛发权 Δ选择相近点 Δ选择相近毛 ΔΔ毛得最近头皮面ξlast iΔΔ面ξ忽略 

==blender键位============
LEFTMOUSE MIDDLEMOUSE RIGHTMOUSE WHEELUPMOUSE WHEELDOWNMOUSE MOUSEX MOUSEY
--Keyboard Keys
--Alphabet keys
AKEY BKEY CKEY DKEY EKEY FKEY GKEY HKEY IKEY JKEY KKEY LKEY MKEY NKEY OKEY PKEY QKEY RKEY SKEY TKEY UKEY VKEY WKEY XKEY YKEY ZKEY
--Number keys
ZEROKEY ONEKEY TWOKEY THREEKEY FOURKEY FIVEKEY SIXKEY SEVENKEY EIGHTKEY NINEKEY
--Modifiers Keys
CAPSLOCKKEY LEFTCTRLKEY LEFTALTKEY RIGHTALTKEY RIGHTCTRLKEY RIGHTSHIFTKEY LEFTSHIFTKEY
--Arrow Keys
LEFTARROWKEY
DOWNARROWKEY
RIGHTARROWKEY
UPARROWKEY
--Numberpad Keys
PAD0 PAD1 PAD2 PAD3 PAD4 PAD5 PAD6 PAD7 PAD8 PAD9 PADPERIOD PADSLASHKEY PADASTERKEY PADMINUS PADENTER PADPLUSKEY
--Function Keys
F1KEY F2KEY F3KEY F4KEY F5KEY F6KEY F7KEY F8KEY F9KEY F10KEY F11KEY F12KEY F13KEY F14KEY F15KEY F16KEY F17KEY F18KEY F19KEY
--Other Keys
ACCENTGRAVEKEY BACKSLASHKEY BACKSPACEKEY COMMAKEY DELKEY ENDKEY EQUALKEY ESCKEY HOMEKEY INSERTKEY LEFTBRACKETKEY LINEFEEDKEY MINUSKEY PAGEDOWNKEY PAGEUPKEY PAUSEKEY PERIODKEY QUOTEKEY RIGHTBRACKETKEY RETKEY ENTERKEY SEMICOLONKEY SLASHKEY SPACEKEY TABKEY NONE BUTTON4MOUSE BUTTON5MOUSE ACTIONMOUSE SELECTMOUSE MOUSEMOVE INBETWEEN_MOUSEMOVE TRACKPADPAN TRACKPADZOOM MOUSEROTATE WHEELINMOUSE WHEELOUTMOUSE EVT_TWEAK_L EVT_TWEAK_M EVT_TWEAK_R EVT_TWEAK_A EVT_TWEAK_S   ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE LEFT_CTRL LEFT_ALT LEFT_SHIFT RIGHT_ALT RIGHT_CTRL RIGHT_SHIFT OSKEY GRLESS ESC TAB RET SPACE LINE_FEED BACK_SPACE DEL SEMI_COLON PERIOD COMMA QUOTE ACCENT_GRAVE MINUS SLASH BACK_SLASH EQUAL LEFT_BRACKET RIGHT_BRACKET LEFT_ARROW DOWN_ARROW RIGHT_ARROW UP_ARROW NUMPAD_0 NUMPAD_1 NUMPAD_2 NUMPAD_3 NUMPAD_4 NUMPAD_5 NUMPAD_6 NUMPAD_7 NUMPAD_8 NUMPAD_9 NUMPAD_ASTERIX NUMPAD_ENTER NUMPAD_MINUS NUMPAD_PERIOD NUMPAD_PLUS NUMPAD_SLASH F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12 F13 F14 F15 F16 F17 F18 F19 PAUSE INSERT HOME PAGE_UP PAGE_DOWN END MEDIA_PLAY MEDIA_STOP MEDIA_FIRST MEDIA_LAST WINDOW_DEACTIVATE TIMER TIMER0 TIMER1 TIMER2 TIMER_AUTOSAVE TIMER_JOBS TIMER_REPORT  NDOF_BUTTON_1 NDOF_BUTTON_10 NDOF_BUTTON_2 NDOF_BUTTON_3 NDOF_BUTTON_4 NDOF_BUTTON_5 NDOF_BUTTON_6 NDOF_BUTTON_7 NDOF_BUTTON_8 NDOF_BUTTON_9 NDOF_BUTTON_A NDOF_BUTTON_ALT NDOF_BUTTON_B NDOF_BUTTON_BACK NDOF_BUTTON_BOTTOM NDOF_BUTTON_C NDOF_BUTTON_CTRL NDOF_BUTTON_DOMINANT NDOF_BUTTON_ESC NDOF_BUTTON_FIT NDOF_BUTTON_FRONT NDOF_BUTTON_ISO1 NDOF_BUTTON_ISO2 NDOF_BUTTON_LEFT NDOF_BUTTON_MINUS NDOF_BUTTON_PANZOOM NDOF_BUTTON_PLUS NDOF_BUTTON_RIGHT NDOF_BUTTON_ROLL_CCW NDOF_BUTTON_ROLL_CW NDOF_BUTTON_ROTATE NDOF_BUTTON_SHIFT NDOF_BUTTON_SPIN_CCW NDOF_BUTTON_SPIN_CW NDOF_BUTTON_TILT_CCW NDOF_BUTTON_TILT_CW NDOF_BUTTON_TOP NDOF_DOM NDOF_FLY NDOF_MOTION NDOF_BUTTON_MENU NDOF_TRANS NDOF_TURN

--map_type--
KEYBOARD
TWEAK
MOUSE
NDOF
TEXTINPUT TIMER
--blender object type
MESH CURVE SURFACE META FONT ARMATURE LATTICE EMPTY CAMERA LAMP SPEAKER
----object mode--------
EDIT_MESH EDIT_CURVE EDIT_SURFACE EDIT_TEXT EDIT_ARMATURE EDIT_METABALL EDIT_LATTICE POSE SCULPT PAINT_WEIGHT PAINT_VERTEX PAINT_TEXTURE PARTICLE OBJECT
----spline type--------
POLY BEZIER BSPLINE CARDINAL NURBS  AUTOMATIC VECTOR ALIGNED FREE_ALIGN TOGGLE_FREE_ALIGN FREE VECTOR ALIGNED AUTO
----modify type--------
MESH_CACHE UV_PROJECT UV_WARP VERTEX_WEIGHT_EDIT VERTEX_WEIGHT_MIX VERTEX_WEIGHT_PROXIMITY ARRAY BEVEL BOOLEAN BUILD DECIMATE EDGE_SPLIT MASK MIRROR MULTIRES REMESH SCREW SKIN SOLIDIFY SUBSURF TRIANGULATE WIREFRAME ARMATURE CAST CURVE DISPLACE HOOK LAPLACIANSMOOTH LAPLACIANDEFORM LATTICE MESH_DEFORM SHRINKWRAP SIMPLE_DEFORM SMOOTH WARP WAVE CLOTH COLLISION DYNAMIC_PAINT EXPLODE FLUID_SIMULATION OCEAN PARTICLE_INSTANCE PARTICLE_SYSTEM SMOKE SOFT_BODY SURFACE MESH_CACHE


--blender constraints type--------
CAMERA_SOLVER OBJECT_SOLVER FOLLOW_TRACK COPY_LOCATION COPY_ROTATION COPY_SCALE COPY_TRANSFORMS LIMIT_DISTANCE LIMIT_LOCATION LIMIT_ROTATION LIMIT_SCALE MAINTAIN_VOLUME TRANSFORM CLAMP_TO DAMPED_TRACK IK LOCKED_TRACK SPLINE_IK STRETCH_TO TRACK_TO ACTION CHILD_OF FLOOR FOLLOW_PATH PIVOT RIGID_BODY_JOINT SCRIPT SHRINKWRAP
--operator--
RUNNING_MODAL CANCELLED FINISHED PASS_THROUGH REGISTER UNDO BLOCKING MACRO GRAB_POINTER PRESET INTERNAL  DEBUG INFO OPERATOR PROPERTY WARNING ERROR ERROR_INVALID_INPUT ERROR_INVALID_CONTEXT ERROR_OUT_OF_MEMORY

--blender icon
NONE QUESTION ERROR CANCEL TRIA_RIGHT TRIA_DOWN TRIA_LEFT TRIA_UP ARROW_LEFTRIGHT PLUS DISCLOSURE_TRI_DOWN DISCLOSURE_TRI_RIGHT RADIOBUT_OFF RADIOBUT_ON MENU_PANEL BLENDER DOT  GO_LEFT PLUG UI NODE NODE_SEL FULLSCREEN SPLITSCREEN RIGHTARROW_THIN BORDERMOVE VIEWZOOM ZOOMIN ZOOMOUT PANEL_CLOSE COPY_ID EYEDROPPER LINK_AREA AUTO CHECKBOX_DEHLT CHECKBOX_HLT UNLOCKED LOCKED UNPINNED PINNED SCREEN_BACK RIGHTARROW DOWNARROW_HLT DOTSUP DOTSDOWN LINK INLINK PLUGIN HELP GHOST_ENABLED COLOR LINKED UNLINKED HAND ZOOM_ALL ZOOM_SELECTED ZOOM_PREVIOUS ZOOM_IN ZOOM_OUT RENDER_REGION BORDER_RECT BORDER_LASSO FREEZE STYLUS_PRESSURE GHOST_DISABLED NEW FILE_TICK QUIT URL RECOVER_LAST FULLSCREEN_ENTER FULLSCREEN_EXIT BLANK1 LAMP MATERIAL TEXTURE ANIM WORLD SCENE EDIT GAME RADIO SCRIPT PARTICLES PHYSICS SPEAKER TEXTURE_SHADED VIEW3D IPO OOPS BUTS FILESEL IMAGE_COL INFO SEQUENCE TEXT IMASEL SOUND ACTION NLA SCRIPTWIN TIME NODETREE LOGIC CONSOLE PREFERENCES CLIP ASSET_MANAGER OBJECT_DATAMODE EDITMODE_HLT FACESEL_HLT VPAINT_HLT TPAINT_HLT WPAINT_HLT SCULPTMODE_HLT POSE_HLT PARTICLEMODE LIGHTPAINT SCENE_DATA RENDERLAYERS WORLD_DATA OBJECT_DATA MESH_DATA CURVE_DATA META_DATA LATTICE_DATA LAMP_DATA MATERIAL_DATA TEXTURE_DATA ANIM_DATA CAMERA_DATA PARTICLE_DATA LIBRARY_DATA_DIRECT GROUP ARMATURE_DATA POSE_DATA BONE_DATA CONSTRAINT SHAPEKEY_DATA CONSTRAINT_BONE PACKAGE UGLYPACKAGE BRUSH_DATA IMAGE_DATA FILE FCURVE FONT_DATA RENDER_RESULT SURFACE_DATA EMPTY_DATA SETTINGS RENDER_ANIMATION RENDER_STILL BOIDS STRANDS LIBRARY_DATA_INDIRECT GREASEPENCIL GROUP_BONE GROUP_VERTEX GROUP_VCOL GROUP_UVS RNA RNA_ADD OUTLINER_OB_EMPTY OUTLINER_OB_MESH OUTLINER_OB_CURVE OUTLINER_OB_LATTICE OUTLINER_OB_META OUTLINER_OB_LAMP OUTLINER_OB_CAMERA OUTLINER_OB_ARMATURE OUTLINER_OB_FONT OUTLINER_OB_SURFACE OUTLINER_OB_SPEAKER RESTRICT_VIEW_OFF RESTRICT_VIEW_ON RESTRICT_SELECT_OFF RESTRICT_SELECT_ON RESTRICT_RENDER_OFF RESTRICT_RENDER_ON OUTLINER_DATA_EMPTY OUTLINER_DATA_MESH OUTLINER_DATA_CURVE OUTLINER_DATA_LATTICE OUTLINER_DATA_META OUTLINER_DATA_LAMP OUTLINER_DATA_CAMERA OUTLINER_DATA_ARMATURE OUTLINER_DATA_FONT OUTLINER_DATA_SURFACE OUTLINER_DATA_SPEAKER OUTLINER_DATA_POSE MESH_PLANE MESH_CUBE MESH_CIRCLE MESH_UVSPHERE MESH_ICOSPHERE MESH_GRID MESH_MONKEY MESH_CYLINDER MESH_TORUS MESH_CONE LAMP_POINT LAMP_SUN LAMP_SPOT LAMP_HEMI LAMP_AREA META_EMPTY META_PLANE META_CUBE META_BALL META_ELLIPSOID META_CAPSULE SURFACE_NCURVE SURFACE_NCIRCLE SURFACE_NSURFACE SURFACE_NCYLINDER SURFACE_NSPHERE SURFACE_NTORUS CURVE_BEZCURVE CURVE_BEZCIRCLE CURVE_NCURVE CURVE_NCIRCLE CURVE_PATH COLOR_RED COLOR_GREEN COLOR_BLUE FORCE_FORCE FORCE_WIND FORCE_VORTEX FORCE_MAGNETIC FORCE_HARMONIC FORCE_CHARGE FORCE_LENNARDJONES FORCE_TEXTURE FORCE_CURVE FORCE_BOID FORCE_TURBULENCE FORCE_DRAG FORCE_SMOKEFLOW MODIFIER MOD_WAVE MOD_BUILD MOD_DECIM MOD_MIRROR MOD_SOFT MOD_SUBSURF HOOK MOD_PHYSICS MOD_PARTICLES MOD_BOOLEAN MOD_EDGESPLIT MOD_ARRAY MOD_UVPROJECT MOD_DISPLACE MOD_CURVE MOD_LATTICE CONSTRAINT_DATA MOD_ARMATURE MOD_SHRINKWRAP MOD_CAST MOD_MESHDEFORM MOD_BEVEL MOD_SMOOTH MOD_SIMPLEDEFORM MOD_MASK MOD_CLOTH MOD_EXPLODE MOD_FLUIDSIM MOD_MULTIRES MOD_SMOKE MOD_SOLIDIFY MOD_SCREW MOD_VERTEX_WEIGHT MOD_DYNAMICPAINT MOD_REMESH MOD_OCEAN MOD_WARP MOD_SKIN MOD_TRIANGULATE REC PLAY FF REW PAUSE PREV_KEYFRAME NEXT_KEYFRAME PLAY_AUDIO PLAY_REVERSE PREVIEW_RANGE PMARKER_ACT PMARKER_SEL PMARKER MARKER_HLT MARKER SPACE2 SPACE3 KEYINGSET KEY_DEHLT KEY_HLT MUTE_IPO_OFF MUTE_IPO_ON VISIBLE_IPO_OFF VISIBLE_IPO_ON DRIVER SOLO_OFF SOLO_ON FRAME_PREV FRAME_NEXT VERTEXSEL EDGESEL FACESEL ROTATE CURSOR ROTATECOLLECTION ROTATECENTER ROTACTIVE ALIGN SMOOTHCURVE SPHERECURVE ROOTCURVE SHARPCURVE LINCURVE NOCURVE RNDCURVE PROP_OFF PROP_ON PROP_CON SCULPT_DYNTOPO PARTICLE_POINT PARTICLE_TIP PARTICLE_PATH MAN_TRANS MAN_ROT MAN_SCALE MANIPUL SNAP_OFF SNAP_ON SNAP_NORMAL SNAP_INCREMENT SNAP_VERTEX SNAP_EDGE SNAP_FACE SNAP_VOLUME STICKY_UVS_LOC STICKY_UVS_DISABLE STICKY_UVS_VERT CLIPUV_DEHLT CLIPUV_HLT SNAP_PEEL_OBJECT GRID PASTEDOWN COPYDOWN PASTEFLIPUP PASTEFLIPDOWN SNAP_SURFACE RETOPO UV_VERTEXSEL UV_EDGESEL UV_FACESEL UV_ISLANDSEL UV_SYNC_SELECT BBOX WIRE SOLID SMOOTH POTATO ORTHO LOCKVIEW_OFF LOCKVIEW_ON AXIS_SIDE AXIS_FRONT AXIS_TOP NDOF_DOM NDOF_TURN NDOF_FLY NDOF_TRANS LAYER_USED LAYER_ACTIVE SORTALPHA SORTBYEXT SORTTIME SORTSIZE LONGDISPLAY SHORTDISPLAY GHOST IMGDISPLAY SAVE_AS SAVE_COPY BOOKMARKS FONTPREVIEW FILTER NEWFOLDER OPEN_RECENT FILE_PARENT FILE_REFRESH FILE_FOLDER FILE_BLANK FILE_BLEND FILE_IMAGE FILE_MOVIE FILE_SCRIPT FILE_SOUND FILE_FONT FILE_TEXT RECOVER_AUTO SAVE_PREFS LINK_BLEND APPEND_BLEND IMPORT EXPORT EXTERNAL_DATA LOAD_FACTORY LOOP_BACK LOOP_FORWARDS BACK FORWARD FILE_BACKUP DISK_DRIVE MATPLANE MATSPHERE MATCUBE MONKEY HAIR ALIASED ANTIALIASED MAT_SPHERE_SKY WORDWRAP_OFF WORDWRAP_ON SYNTAX_OFF SYNTAX_ON LINENUMBERS_OFF LINENUMBERS_ON SCRIPTPLUGINS SEQ_SEQUENCER SEQ_PREVIEW SEQ_LUMA_WAVEFORM SEQ_CHROMA_SCOPE SEQ_HISTOGRAM SEQ_SPLITVIEW IMAGE_RGB IMAGE_RGB_ALPHA IMAGE_ALPHA IMAGE_ZDEPTH IMAGEFILE BRUSH_ADD BRUSH_BLOB BRUSH_BLUR BRUSH_CLAY BRUSH_CLAY_STRIPS BRUSH_CLONE BRUSH_CREASE BRUSH_DARKEN BRUSH_FILL BRUSH_FLATTEN BRUSH_GRAB BRUSH_INFLATE BRUSH_LAYER BRUSH_LIGHTEN BRUSH_MASK BRUSH_MIX BRUSH_MULTIPLY BRUSH_NUDGE BRUSH_PINCH BRUSH_SCRAPE BRUSH_SCULPT_DRAW BRUSH_SMEAR BRUSH_SMOOTH BRUSH_SNAKE_HOOK BRUSH_SOFTEN BRUSH_SUBTRACT BRUSH_TEXDRAW BRUSH_THUMB BRUSH_ROTATE BRUSH_VERTEXDRAW VIEW3D_VEC EDIT_VEC EDITMODE_DEHLT EDITMODE_HLT DISCLOSURE_TRI_RIGHT_VEC DISCLOSURE_TRI_DOWN_VEC MOVE_UP_VEC MOVE_DOWN_VEC X_VEC SMALL_TRI_RIGHT_VEC


------------
INVOKE_DEFAULT INVOKE_REGION_WIN INVOKE_REGION_CHANNELS INVOKE_REGION_PREVIEW INVOKE_AREA INVOKE_SCREEN EXEC_DEFAULT EXEC_REGION_WIN EXEC_REGION_CHANNELS EXEC_REGION_PREVIEW EXEC_AREA EXEC_SCREEN 

----C 关键字--------------------------
size_t  void  this 

----C函数--------------------------
malloc  main printf cout cout endl 









////end////end////end////end////end////end////end////end////end