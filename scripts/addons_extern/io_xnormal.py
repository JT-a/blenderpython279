# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "xNormal applink",
    "author": "Joel Daniels",
    "version": (0, 7),
    "blender": (2, 67, 1),
    "location": "Properties > Scene",
    "description": "Export to and from xNormal 3.18.1",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}


import bpy
from bpy.props import *
from subprocess import Popen
import os
from extensions_framework import util as efutil


def realpath(path):
    return os.path.realpath(efutil.filesystem_path(path))

sep = os.path.sep
#-------------------------------------------------------------------------------------


class PROPERTIES_OT_Export(bpy.types.Operator):
    bl_idname = "xnormal.export"
    bl_label = "Export to xNormal"
    bl_description = "Export selected objects to xNormal."
    bl_options = {'UNDO'}

    def execute(self, context):
        scene = context.scene
        obj = bpy.context.object

        # Find the output directory from xN_output
        export_path = realpath(scene.xN_output)
        if not os.path.exists(export_path):
            os.mkdir(export_path)

        img_export_path = os.path.join(export_path, "images")
        if not os.path.exists(img_export_path):
            os.mkdir(img_export_path)

        # Clean up the directory first, if file overwriting is not enabled.
        if scene.xN_file_overwrite == True:
            for item in os.listdir(export_path):
                if item[-4:] == '.ply':
                    os.remove(export_path + '\\' + item)

        # xNormal executable path.
        xN_exe = os.path.join(realpath(scene.xN_exec_path), 'xNormal.exe')

        # Get a file name for the .xml file, using last part of 'output file' string.
        xml_filePath = os.path.join(realpath(scene.xN_output), scene.xN_proj_name) + '.xml' if scene.xN_proj_name else os.path.join(realpath(scene.xN_output), 'default.xml')
        # Open the file.
        the_xml_file = open(xml_filePath, 'w+')

        # Functions to write the contents of the .xml file.
        def writeXML(file):
            nonlocal img_export_path

            file.write(r"""<?xml version="1.0" encoding="UTF-8"?>
<Settings xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Version="3.18.1">""")
            file.write('\n')

            # Add the full path to the object names.
#            if scene.xN_export_type == 'obj':
#                type = '.obj'
#            else:
            type = '.ply'
            lowpoly = export_path + '\\' + scene.xN_lowpoly + type
            hipoly = export_path + '\\' + scene.xN_hipoly + type
            cage_obj = ""
            if scene.xN_lowpoly_use_cage:
                if scene.xN_cage_external and scene.xN_cage_file != "":
                    cage_obj = realpath(scene.xN_cage_file)
                elif scene.xN_cage_external and scene.xN_cage_file == "":
                    # Dealbreaker, ladies!
                    self.report({'INFO'}, "Lowpoly cage option is enabled, but no cage file exists.")
                    return {'CANCELLED'}

                elif not scene.xN_cage_external and scene.xN_cage_obj is not None:
                    cage_obj = (export_path + '\\' + scene.xN_cage_obj + type)
                elif scene.xN_cage_external == False and scene.xN_cage_obj is None:
                    # Another dealbreaker, ladies!
                    self.report({'INFO'}, "Lowpoly cage option is enabled, but no cage object is selected.")
                    return {'CANCELLED'}

            # Add the image format to the file name.
            image_output = os.path.join(realpath(img_export_path), scene.xN_proj_name) + scene.xN_img_format if scene.xN_proj_name else os.path.join(realpath(img_export_path), 'default') + scene.xN_img_format

            bools = [scene.xN_render_AO, scene.xN_render_Normal, scene.xN_render_Height, scene.xN_render_Base, scene.xN_discard_BF, scene.xN_closest_hit, scene.xN_AO_limit_ray, scene.xN_normal_tangent_space, scene.xN_AO_jitter, scene.xN_AO_ignore_bf, scene.xN_AO_allow_full, scene.xN_render_Bent, scene.xN_bent_limit_ray, scene.xN_bent_jitter, scene.xN_bent_tanspace, scene.xN_render_PRT, scene.xN_prt_limit_ray, scene.xN_prt_col_normalize, scene.xN_render_convexity, scene.xN_render_thickness, scene.xN_render_proximity, scene.xN_prox_limit_ray, scene.xN_render_cavity, scene.xN_cavity_jitter, scene.xN_render_wireframe_rayfails, scene.xN_wire_render_wire, scene.xN_wire_render_rf, scene.xN_render_direction, scene.xN_direction_tanspace, scene.xN_render_radiosity, scene.xN_radiosity_occl, scene.xN_radiosity_limit_ray, scene.xN_radiosity_pure_occl, scene.xN_render_vcolors, scene.xN_render_curvature, scene.xN_curvature_jitter, scene.xN_curvature_smoothing, scene.xN_render_derivative, scene.xN_hipoly_visible, scene.xN_hipoly_ignore_vcolor, scene.xN_lowpoly_visible, scene.xN_lowpoly_use_cage, scene.xN_lowpoly_batch, scene.xN_lowpoly_normals_override, scene.xN_lowpoly_match_uvs]

            for i in range(len(bools)):
                if bools[i] == True:
                    bools[i] = 'true'
                else:
                    bools[i] = 'false'

            UOffset = 'true' if scene.xN_lowpoly_U_offset else 'false'
            VOffset = 'true' if scene.xN_lowpoly_V_offset else 'false'

            # Write the mesh data to the .xml file.
            file.write(r"""  <HighPolyModel DefaultMeshScale="1.000000">
    <Mesh Visible="{0}" Scale="{1}" IgnorePerVertexColor="{2}" AverageNormals="{3}" BaseTexIsTSNM="false" File="{4}"/>
  </HighPolyModel>
  <LowPolyModel DefaultMeshScale="1.000000">
    <Mesh Visible="{5}" File="{6}" AverageNormals="{7}" MaxRayDistanceFront="{8}" MaxRayDistanceBack="{9}" UseCage="{10}" NormapMapType="Tangent-space" UsePerVertexColors="true" UseFresnel="false" FresnelRefractiveIndex="1.330000" ReflectHDRMult="1.000000" VectorDisplacementTS="false" VDMSwizzleX="X+" VDMSwizzleY="Y+" VDMSwizzleZ="Z+" BatchProtect="{11}" CastShadows="true" ReceiveShadows="true" BackfaceCull="true" NMSwizzleX="X+" NMSwizzleY="Y+" NMSwizzleZ="Z+" CageFile="{17}" HighpolyNormalsOverrideTangentSpace="{12}" TransparencyMode="None" AlphaTestValue="127" Matte="false" Scale="{13}" MatchUVs="{14}" UOffset="{15}" VOffset="{16}"/>
  </LowPolyModel>""".format(bools[40], scene.xN_hipoly_mesh_scale, bools[39], scene.xN_hipoly_normalsmoothing, hipoly, bools[40], lowpoly, scene.xN_lowpoly_normalsmoothing, scene.xN_lowpoly_max_front_ray, scene.xN_lowpoly_max_rear_ray, bools[41], bools[42], bools[43], scene.xN_lowpoly_mesh_scale, bools[44], UOffset, VOffset, cage_obj))
            file.write('\n')

            height_min = 'true' if scene.xN_height_manual_min else 'false'
            height_max = 'true' if scene.xN_height_manual_max else 'false'
            direction_min = 'true' if scene.xN_direction_manual_min else 'false'
            direction_max = 'true' if scene.xN_direction_manual_max else 'false'

            # Write the map generation details.
            file.write(r"""  <GenerateMaps GenNormals="{0}" Width="{1}" Height="{2}" EdgePadding="{3}" BucketSize="{4}" TangentSpace="{5}" ClosestIfFails="{6}" DiscardRayBackFacesHits="{7}" File="{8}" SwizzleX="{9}" SwizzleY="{10}" SwizzleZ="{11}" AA="{12}" BakeHighpolyBaseTex="{13}" BakeHighpolyBaseTextureDrawObjectIDIfNoTexture="false" GenHeights="{14}" HeightTonemap="{15}" HeightTonemapMin="{16}" HeightTonemapMax="{17}" GenAO="{18}" AORaysPerSample="{19}" AODistribution="{20}" AOConeAngle="{21}" AOBias="{22}" AOAllowPureOccluded="{23}" AOLimitRayDistance="{24}" AOAttenConstant="{25}" AOAttenLinear="{26}" AOAttenCuadratic="{27}" AOJitter="{28}" AOIgnoreBackfaceHits="{29}" GenBent="{30}" BentRaysPerSample="{31}" BentConeAngle="{32}" BentBias="{33}" BentTangentSpace="{34}" BentLimitRayDistance="{35}" BentJitter="{36}" BentDistribution="{37}" BentSwizzleX="{38}" BentSwizzleY="{39}" BentSwizzleZ="{40}" GenPRT="{41}" PRTRaysPerSample="{42}" PRTConeAngle="{43}" PRTBias="{44}" PRTLimitRayDistance="{45}" PRTJitter="true" PRTNormalize="{46}" PRTThreshold="{47}" GenProximity="{48}" ProximityRaysPerSample="{49}" ProximityConeAngle="{50}" ProximityLimitRayDistance="{51}" GenConvexity="{52}" ConvexityScale="{53}" GenThickness="{54}" GenCavity="{55}" CavityRaysPerSample="{56}" CavityJitter="{57}" CavitySearchRadius="{58}" CavityContrast="{59}" CavitySteps="{60}" GenWireRays="{61}" RenderRayFails="{62}" RenderWireframe="{63}" GenDirections="{64}" DirectionsTS="{65}" DirectionsSwizzleX="{66}" DirectionsSwizzleY="{67}" DirectionsSwizzleZ="{68}" DirectionsTonemap="{69}" DirectionsTonemapMin="{70}" DirectionsTonemapMax="{71}" GenRadiosityNormals="{72}" RadiosityNormalsRaysPerSample="{73}" RadiosityNormalsDistribution="{74}" RadiosityNormalsConeAngle="{75}" RadiosityNormalsBias="{76}" RadiosityNormalsLimitRayDistance="{76}" RadiosityNormalsAttenConstant="{78}" RadiosityNormalsAttenLinear="{79}" RadiosityNormalsAttenCuadratic="{80}" RadiosityNormalsJitter="true" RadiosityNormalsContrast="{81}" RadiosityNormalsEncodeAO="{82}" RadiosityNormalsCoordSys="{83}" RadiosityNormalsAllowPureOcclusion="{84}" BakeHighpolyVCols="{85}" GenCurv="{86}" CurvRaysPerSample="{87}" CurvBias="{88}" CurvConeAngle="{89}" CurvJitter="{90}" CurvSearchDistance="{91}" CurvTonemap="{92}" CurvDistribution="{93}" CurvAlgorithm="{94}" CurvSmoothing="{95}" GenDerivNM="{96}">""".format(bools[1], scene.xN_dimensions_X, scene.xN_dimensions_Y, scene.xN_edge_padding, scene.xN_bucket_size, bools[7], bools[5], bools[4], (image_output), scene.xN_normal_swizzle1, scene.xN_normal_swizzle2, scene.xN_normal_swizzle3, scene.xN_AA_setting, bools[3], bools[2], scene.xN_height_normalization, height_min, height_max, bools[0], scene.xN_AO_rays, scene.xN_AO_distribution, scene.xN_AO_spread_angle, scene.xN_AO_bias, bools[10], bools[6], scene.xN_AO_atten1, scene.xN_AO_atten2, scene.xN_AO_atten3, bools[8], bools[9], bools[11], scene.xN_bent_rays, scene.xN_bent_spread, scene.xN_bent_bias, bools[14], bools[12], bools[13], scene.xN_bent_distribution, scene.xN_bent_swizzle1, scene.xN_bent_swizzle2, scene.xN_bent_swizzle3, bools[15], scene.xN_prt_rays, scene.xN_prt_spread, scene.xN_prt_bias, bools[16], bools[17], scene.xN_prt_threshold, bools[20], scene.xN_prox_rays, scene.xN_prox_spread, bools[21], bools[18], scene.xN_convexity_scale, bools[19], bools[22], scene.xN_cavity_rays, bools[23], scene.xN_cavity_radius, scene.xN_cavity_contrast, scene.xN_cavity_steps, bools[24], bools[26], bools[25], bools[27], bools[28], scene.xN_direction_swizzle1, scene.xN_direction_swizzle2, scene.xN_direction_swizzle3, scene.xN_direction_normalization, direction_min, direction_max, bools[29], scene.xN_radiosity_rays, scene.xN_radiosity_distribution, scene.xN_radiosity_spread, scene.xN_radiosity_bias, bools[31], scene.xN_radiosity_atten1, scene.xN_radiosity_atten2, scene.xN_radiosity_atten3, scene.xN_radiosity_contrast, bools[30], scene.xN_radiosity_coord, bools[32], bools[33], bools[34], scene.xN_curvature_rays, scene.xN_curvature_bias, scene.xN_curvature_spread, bools[35], scene.xN_curvature_search, scene.xN_curvature_tonemap, scene.xN_curvature_distribution, scene.xN_curvature_algorithm, bools[36], bools[37]))
            file.write('\n')

            file.write(r"""    <NMBackgroundColor R="{0}" G="{1}" B="{2}"/>
    <BakeHighpolyBaseTextureNoTexCol R="255" G="0" B="0"/>
    <BakeHighpolyBaseTextureBackgroundColor R="0" G="0" B="0"/>
    <HMBackgroundColor R="{3}" G="{4}" B="{5}"/>
    <AOOccludedColor R="{6}" G="{7}" B="{8}"/>
    <AOUnoccludedColor R="{9}" G="{10}" B="{11}"/>
    <AOBackgroundColor R="{12}" G="{13}" B="{14}"/>
    <BentBackgroundColor R="{15}" G="{16}" B="{17}"/>
    <PRTBackgroundColor R="{18}" G="{19}" B="{20}"/>
    <ProximityBackgroundColor R="{21}" G="{22}" B="{23}"/>
    <ConvexityBackgroundColor R="{24}" G="{25}" B="{26}"/>
    <CavityBackgroundColor R="{27}" G="{28}" B="{29}"/>
    <RenderWireframeCol R="{30}" G="{31}" B="{32}"/>
    <RenderCWCol R="{33}" G="{34}" B="{35}"/>
    <RenderSeamCol R="{36}" G="{37}" B="{38}"/>
    <RenderRayFailsCol R="{39}" G="{40}" B="{41}"/>
    <RenderWireframeBackgroundColor R="{42}" G="{43}" B="{44}"/>
    <VDMBackgroundColor R="0" G="0" B="0"/>
    <RadNMBackgroundColor R="{45}" G="{46}" B="{47}"/>
    <BakeHighpolyVColsBackgroundCol R="{54}" G="{55}" B="{56}"/>
    <CurvBackgroundColor R="{48}" G="{49}" B="{50}"/>
    <DerivNMBackgroundColor R="{51}" G="{52}" B="{53}"/>
  </GenerateMaps>
  <Detail Scale="0.500000" Method="4Samples"/>""".format(int(scene.xN_normal_bgcolor[0] * 255),
                                                         int(scene.xN_normal_bgcolor[1] * 255),
                                                         int(scene.xN_normal_bgcolor[2] * 255),
                                                         int(scene.xN_height_bgcolor[0] * 255),
                                                         int(scene.xN_height_bgcolor[1] * 255),
                                                         int(scene.xN_height_bgcolor[2] * 255),
                                                         int(scene.xN_AO_occluded_col[0] * 255),
                                                         int(scene.xN_AO_occluded_col[1] * 255),
                                                         int(scene.xN_AO_occluded_col[2] * 255),
                                                         int(scene.xN_AO_unoccluded_col[0] * 255),
                                                         int(scene.xN_AO_unoccluded_col[1] * 255),
                                                         int(scene.xN_AO_unoccluded_col[2] * 255),
                                                         int(scene.xN_AO_bgcolor[0] * 255),
                                                         int(scene.xN_AO_bgcolor[1] * 255),
                                                         int(scene.xN_AO_bgcolor[2] * 255),
                                                         int(scene.xN_bent_bgcolor[0] * 255),
                                                         int(scene.xN_bent_bgcolor[1] * 255),
                                                         int(scene.xN_bent_bgcolor[2] * 255),
                                                         int(scene.xN_prt_bgcolor[0] * 255),
                                                         int(scene.xN_prt_bgcolor[1] * 255),
                                                         int(scene.xN_prt_bgcolor[2] * 255),
                                                         int(scene.xN_prox_bgcolor[0] * 255),
                                                         int(scene.xN_prox_bgcolor[1] * 255),
                                                         int(scene.xN_prox_bgcolor[2] * 255),
                                                         int(scene.xN_convexity_bgcolor[0] * 255),
                                                         int(scene.xN_convexity_bgcolor[1] * 255),
                                                         int(scene.xN_convexity_bgcolor[2] * 255),
                                                         int(scene.xN_cavity_bgcolor[0] * 255),
                                                         int(scene.xN_cavity_bgcolor[1] * 255),
                                                         int(scene.xN_cavity_bgcolor[2] * 255),
                                                         int(scene.xN_wire_color[0] * 255),
                                                         int(scene.xN_wire_color[1] * 255),
                                                         int(scene.xN_wire_color[2] * 255),
                                                         int(scene.xN_wire_CW[0] * 255),
                                                         int(scene.xN_wire_CW[1] * 255),
                                                         int(scene.xN_wire_CW[2] * 255),
                                                         int(scene.xN_wire_seam[0] * 255),
                                                         int(scene.xN_wire_seam[1] * 255),
                                                         int(scene.xN_wire_seam[2] * 255),
                                                         int(scene.xN_wire_rf_color[0] * 255),
                                                         int(scene.xN_wire_rf_color[1] * 255),
                                                         int(scene.xN_wire_rf_color[2] * 255),
                                                         int(scene.xN_wire_bgcolor[0] * 255),
                                                         int(scene.xN_wire_bgcolor[1] * 255),
                                                         int(scene.xN_wire_bgcolor[2] * 255),
                                                         int(scene.xN_radiosity_bgcolor[0] * 255),
                                                         int(scene.xN_radiosity_bgcolor[1] * 255),
                                                         int(scene.xN_radiosity_bgcolor[2] * 255),
                                                         int(scene.xN_curvature_bgcolor[0] * 255),
                                                         int(scene.xN_curvature_bgcolor[1] * 255),
                                                         int(scene.xN_curvature_bgcolor[2] * 255),
                                                         int(scene.xN_derivative_bgcolor[0] * 255),
                                                         int(scene.xN_derivative_bgcolor[1] * 255),
                                                         int(scene.xN_derivative_bgcolor[2] * 255),
                                                         int(scene.xN_vcolors_bgcolor[0] * 255),
                                                         int(scene.xN_vcolors_bgcolor[1] * 255),
                                                         int(scene.xN_vcolors_bgcolor[2] * 255)))
            file.write('\n')
            file.write(r"""  <Viewer3D ShowGrid="true" ShowWireframe="false" ShowTangents="false" ShowNormals="false" ShowBlockers="false" MaxTessellationLevel="0" LightIntensity="0.400000" LightIndirectIntensity="0.000000" Exposure="0.180000" HDRThreshold="0.900000" UseGlow="true" GlowIntensity="1.000000" SSAOEnabled="false" SSAOBright="1.100000" SSAOContrast="1.000000" SSAOAtten="1.000000" SSAORadius="0.250000" SSAOBlurRadius="2.000000" ParallaxStrength="0.000000" ShowHighpolys="true" ShowAO="false" CageOpacity="0.700000" DiffuseGIIntensity="0.810000" CastShadows="true" ShadowBias="1.000000" ShadowArea="0.500000" AxisScl="0.040000" CameraOrbitDistance="0.250000" CameraOrbitAutoCenter="true" ShowStarfield="false">
    <LightAmbientColor R="33" G="33" B="33"/>
    <LightDiffuseColor R="249" G="255" B="255"/>
    <LightSpecularColor R="255" G="255" B="255"/>
    <LightSecondaryColor R="0" G="0" B="0"/>
    <LightTertiaryColor R="0" G="0" B="0"/>
    <BackgroundColor R="0" G="0" B="0"/>
    <GridColor R="180" G="180" B="220"/>
    <CageColor R="76" G="76" B="76"/>
    <CameraRotation e11="0.692134" e12="-0.004270" e13="0.721756" e21="0.189344" e22="0.966035" e23="-0.175859" e31="-0.696490" e32="0.258379" e33="0.669434"/>
    <CameraPosition x="-178.460007" y="131.259995" z="219.479996"/>
    <LightPosition x="-34.639999" y="340.609985" z="104.209999"/>
  </Viewer3D>
</Settings>""")

        writeXML(the_xml_file)
        the_xml_file.close()

        # Export the .obj files. Store the names of the objects in the scene in a list...
        if scene.xN_lowpoly_use_cage and scene.xN_cage_external == False and scene.xN_cage_obj is not None:
            objs_to_export = [bpy.data.objects[scene.xN_hipoly], bpy.data.objects[scene.xN_lowpoly], bpy.data.objects[scene.xN_cage_obj]]
        else:
            objs_to_export = [bpy.data.objects[scene.xN_hipoly], bpy.data.objects[scene.xN_lowpoly]]

        #############################################
        # Figure this out later. Leave disabled for now.

#        # Then export them one at a time.
#        if scene.xN_export_type == 'obj':
#            for object in objs_to_export:
#                for area in context.screen.areas:
#                    if area.type == 'VIEW_3D':
#                        for region in area.regions:
#                            if region.type == 'WINDOW':
#                                override = {
#                                    'window': context.window,
#                                    'area': area,
#                                    'region': region,
#                                    'scene': scene,
#                                    'blend_data': context.blend_data,
#                                    'selected_bases': [ob_base for ob_base in scene.object_bases if ob_base.object.name == object.name]}
#
#                obj_export_name = export_path + '\\' + object.name + '.obj'
#                bpy.ops.export_scene.obj(override, filepath=obj_export_name,  use_mesh_modifiers=True, use_edges=False, use_normals=True, use_uvs = True, use_materials=True, path_mode='ABSOLUTE')

        #############################################


#        elif scene.xN_export_type == 'ply':
        for object in objs_to_export:
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            override = {
                                'window': context.window,
                                'area': area,
                                'region': region,
                                'scene': scene,
                                'blend_data': context.blend_data,
                                'selected_bases': [ob_base for ob_base in scene.object_bases if ob_base.object.name == object.name],
                                'active_object': object}

            obj_export_name = export_path + '\\' + object.name + '.ply'
            # If we're allowing file overwrite:
            if scene.xN_file_overwrite == True:
                bpy.ops.export_mesh.ply(override, filepath=obj_export_name, use_mesh_modifiers=True, use_normals=True, use_uv_coords=True, use_colors=True)

            # If we're not allowing file overwrite, but the mesh doesn't exist yet:
            elif scene.xN_file_overwrite == False and object.name + '.ply' not in os.listdir(export_path):
                bpy.ops.export_mesh.ply(override, filepath=obj_export_name, use_mesh_modifiers=True, use_normals=True, use_uv_coords=True, use_colors=True)

            # If we're not allowing file overwrite, and the mesh already exists:
            else:
                pass

        # Arguments for opening xNormal with subprocess.Popen
        args = (xN_exe, xml_filePath)
        # Open xNormal, passing the created .xml file to the command.
        try:
            Popen(args, bufsize=-1, cwd=export_path, shell=False)
        except PermissionError:
            print("Darn. Couldn't open xNormal. Check permissions and/or xNormal path.")
            pass

        return {'FINISHED'}


#-------------------------------------------------------------------------------------


class PROPERTIES_OT_Import(bpy.types.Operator):
    bl_idname = "xnormal.import"
    bl_label = "Import maps from xNormal"
    bl_description = "Import generated maps from xNormal."
    bl_options = {'UNDO'}

    def execute(self, context):
        scene = context.scene
        engine = scene.render.engine
        lowpoly = scene.xN_lowpoly
        material_name = scene.xN_proj_name if scene.xN_proj_name else 'default'
        object = scene.objects[lowpoly]

        import_path = os.path.join(realpath(scene.xN_output), 'images')

        import_imgs = []
        for item in os.listdir(import_path):
            if item[-4:] == scene.xN_img_format:
                import_imgs.append(item)

        # A quick function for adding the import path to the img file.
        def add_path(img, path):
            return path + '\\' + img

        import_imgs = [add_path(img, import_path) for img in import_imgs]

        ############
        # A function for taking material name and adding textures to that material
        def tex_to_material(mat_name, img, type):
            tex_name = mat_name + '_' + type
            if tex_name not in bpy.data.textures:
                use_texture = bpy.data.textures.new(tex_name, 'IMAGE')
            else:
                use_texture = bpy.data.textures[tex_name]
            material_tex = bpy.data.materials[mat_name].texture_slots.add()  # Add new texture slot
            material_tex.texture = use_texture  # Set it to the texture
            bpy.data.textures[tex_name].image = bpy.data.images[img]
            material_tex.texture_coords = 'UV'
            material_tex.uv_layer = bpy.data.meshes[lowpoly].uv_textures[0].name
            if type == 'normal':
                material_tex.use_map_normal = True
                material_tex.use_map_color_diffuse = False
                bpy.data.textures[tex_name].use_normal_map = True
                if context.scene.xN_normal_tangent_space == True:
                    material_tex.normal_map_space = 'TANGENT'
                else:
                    material_tex.normal_map_space = 'OBJECT'
            elif type == 'ao' or 'cavity':
                material_tex.use_map_color_diffuse = True
                material_tex.diffuse_color_factor = 0.5
                material_tex.blend_type = 'MULTIPLY'
            elif type == 'vcols':
                material_tex.use_map_color_diffuse = True

        # Add texture to lowpoly object
        # if engine == 'BLENDER_RENDER':
        if material_name not in bpy.data.objects[lowpoly].data.materials:
            use_material = bpy.data.materials.new(material_name)
            bpy.data.objects[lowpoly].data.materials.append(use_material)
        else:
            use_material = bpy.data.materials[material_name]

        # Get a list of all the textures currently on this material, if any. We don't want to duplicate textures every time maps are imported
        tex_list = []
        for texture in use_material.texture_slots:
            if texture:
                tex_list.append(texture.name)

        for img in import_imgs:
            print("Opening", img)
            image_name = img.split('\\')[-1]
            if img not in bpy.data.images:
                bpy.ops.image.open(filepath=img)
            else:
                bpy.data.images[image].reload()

            if 'normals' in img:
                if use_material.name + '_normal' not in tex_list:
                    tex_to_material(use_material.name, image_name, 'normal')
            elif 'occlusion' in img:
                if use_material.name + '_ao' not in tex_list:
                    tex_to_material(use_material.name, image_name, 'ao')
            elif 'cavity' in img:
                if use_material.name + '_cavity' not in tex_list:
                    tex_to_material(use_material.name, image_name, 'cavity')
            elif 'vcols' in img:
                if use_material.name + '_vcols' not in tex_list:
                    tex_to_material(use_material.name, image_name, 'vcols')
            else:
                pass

        return {'FINISHED'}

#-------------------------------------------------------------------------------------


class PROPERTIES_OT_Launch_xNormal(bpy.types.Operator):
    bl_idname = "xnormal.launch"
    bl_label = "Launch xNormal Standalone"
    bl_description = "Launch the xNormal standalone application."

    def execute(self, context):
        scene = context.scene

        export_path = realpath(scene.xN_output)

        xN_exe = os.path.join(realpath(scene.xN_exec_path), 'xNormal.exe')
        Popen(xN_exe, bufsize=-1, cwd=export_path, shell=False)

        return {'FINISHED'}

#-------------------------------------------------------------------------------------
# A class for drawing the UI panels


class PROPERTIES_PT_xN_MeshesPanel(bpy.types.Panel):
    bl_idname = "xNormal_Panel"
    bl_label = "xNormal Meshes"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, 'xN_hipoly')
        if scene.xN_hipoly:
            box = layout.box()
            row = box.row()
            row.prop(scene, 'xN_hipoly_visible')
            row.prop(scene, 'xN_hipoly_ignore_vcolor', text='Ignore per-vertex colors')
            row = box.row()
            row.prop(scene, 'xN_hipoly_mesh_scale')
            row.prop(scene, 'xN_hipoly_normalsmoothing')
            layout.separator()

        layout.prop(scene, 'xN_lowpoly')
        if scene.xN_lowpoly:
            box = layout.box()
            row = box.row()
            row.prop(scene, 'xN_lowpoly_visible')
            row.prop(scene, 'xN_lowpoly_batch')
            row = box.row()
            row.prop(scene, 'xN_lowpoly_match_uvs')
            row.prop(scene, 'xN_lowpoly_normals_override', text='High poly normals override')
            row = box.row()
            row.prop(scene, 'xN_lowpoly_use_cage')
            if scene.xN_lowpoly_use_cage:
                row.prop(scene, 'xN_cage_external', text="Use external cage file")
                if scene.xN_cage_external:
                    box.prop(scene, 'xN_cage_file', text="Cage file")
                else:
                    box.prop(scene, 'xN_cage_obj')

            row = box.row()
            row.prop(scene, 'xN_lowpoly_max_front_ray')
            row.prop(scene, 'xN_lowpoly_max_rear_ray')
            row = box.row()
            row.prop(scene, 'xN_lowpoly_mesh_scale')
            row.prop(scene, 'xN_lowpoly_normalsmoothing')
            row = box.row()
            row.prop(scene, 'xN_lowpoly_U_offset')
            row.prop(scene, 'xN_lowpoly_V_offset')
            layout.separator()


class PROPERTIES_PT_xN_MapsPanel(bpy.types.Panel):
    bl_label = "xNormal Maps"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, 'xN_render_AO', text='Ambient occlusion map')
        if scene.xN_render_AO:
            box = layout.box()
            row = box.row()
            row.prop(scene, 'xN_AO_allow_full')
            row.prop(scene, 'xN_AO_jitter')
            row = box.row()
            row.prop(scene, 'xN_AO_limit_ray')
            row.prop(scene, 'xN_AO_ignore_bf')
            box.prop(scene, 'xN_AO_rays')
            box.prop(scene, 'xN_AO_bias')
            box.prop(scene, 'xN_AO_spread_angle')
            box.label("Attenuation:")
            row = box.row()
            row.prop(scene, 'xN_AO_atten1', text='Constant')
            row.prop(scene, 'xN_AO_atten2', text='Linear')
            row.prop(scene, 'xN_AO_atten3', text='Quadratic')
            box.prop(scene, 'xN_AO_distribution')
            row = box.row()
            row.prop(scene, 'xN_AO_occluded_col', text='Occluded')
            row.prop(scene, 'xN_AO_unoccluded_col', text='Unoccluded')
            layout.separator()

        layout.prop(scene, 'xN_render_Normal', text='Normal map')
        if scene.xN_render_Normal:
            box = layout.box()
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_normal_tangent_space')
            col.separator()
            col.separator()
            col.prop(scene, 'xN_normal_bgcolor')
            col = split.column()
            col.label('Swizzle:')
            col.prop(scene, 'xN_normal_swizzle1')
            col.prop(scene, 'xN_normal_swizzle2')
            col.prop(scene, 'xN_normal_swizzle3')
            layout.separator()

        layout.prop(scene, 'xN_render_Height', text='Height map')
        if scene.xN_render_Height:
            box = layout.box()
            box.prop(scene, 'xN_height_normalization')
            if scene.xN_height_normalization == 'Manual':
                row = box.row()
                row.prop(scene, 'xN_height_manual_min')
                row.prop(scene, 'xN_height_manual_max')
            box.prop(scene, 'xN_height_bgcolor')
            layout.separator()

        layout.prop(scene, 'xN_render_cavity', text='Cavity map')
        if scene.xN_render_cavity:
            box = layout.box()
            box.prop(scene, 'xN_cavity_jitter', text='Cavity map jitter')
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_cavity_rays')
            col.prop(scene, 'xN_cavity_steps')
            col = split.column()
            col.prop(scene, 'xN_cavity_radius')
            col.prop(scene, 'xN_cavity_contrast')
            box.prop(scene, 'xN_cavity_bgcolor')

        layout.prop(scene, 'xN_render_convexity', text='Convexity map')
        if scene.xN_render_convexity:
            box = layout.box()
            box.prop(scene, 'xN_convexity_scale')
            box.prop(scene, 'xN_convexity_bgcolor')

        layout.prop(scene, 'xN_render_Bent', text='Bent normal map')
        if scene.xN_render_Bent:
            box = layout.box()
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_bent_jitter')
            col.prop(scene, 'xN_bent_limit_ray')
            col = split.column()
            col.prop(scene, 'xN_bent_tanspace')
            box.prop(scene, 'xN_bent_rays')
            box.prop(scene, 'xN_bent_bias')
            box.prop(scene, 'xN_bent_spread')
            box.prop(scene, 'xN_bent_distribution', text='Distribution')
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_bent_bgcolor')
            col = split.column()
            col.label('Swizzle:')
            col.prop(scene, 'xN_bent_swizzle1')
            col.prop(scene, 'xN_bent_swizzle2')
            col.prop(scene, 'xN_bent_swizzle3')
            layout.separator()

        layout.prop(scene, 'xN_render_curvature', text='Curvature map')
        if scene.xN_render_curvature:
            box = layout.box()
            row = box.row()
            row.prop(scene, 'xN_curvature_jitter')
            row.prop(scene, 'xN_curvature_smoothing')
            box.prop(scene, 'xN_curvature_rays')
            box.prop(scene, 'xN_curvature_bias')
            box.prop(scene, 'xN_curvature_spread')
            box.prop(scene, 'xN_curvature_search')
            box.prop(scene, 'xN_curvature_algorithm')
            box.prop(scene, 'xN_curvature_tonemap')
            box.prop(scene, 'xN_curvature_distribution')
            box.prop(scene, 'xN_curvature_bgcolor')
            layout.separator()

        layout.prop(scene, 'xN_render_direction', text='Direction map')
        if scene.xN_render_direction:
            box = layout.box()
            box.prop(scene, 'xN_direction_tanspace')
            box.prop(scene, 'xN_direction_normalization')
            if scene.xN_direction_normalization == 'Manual':
                row = box.row()
                row.prop(scene, 'xN_direction_manual_min')
                row.prop(scene, 'xN_direction_manual_max')
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_direction_bgcolor')
            col = split.column()
            col.label('Swizzle:')
            col.prop(scene, 'xN_direction_swizzle1')
            col.prop(scene, 'xN_direction_swizzle2')
            col.prop(scene, 'xN_direction_swizzle3')
            layout.separator()

        layout.prop(scene, 'xN_render_proximity', text='Proximity map')
        if scene.xN_render_proximity:
            box = layout.box()
            box.prop(scene, 'xN_prox_limit_ray')
            box.prop(scene, 'xN_prox_rays')
            box.prop(scene, 'xN_prox_spread')
            box.prop(scene, 'xN_prox_bgcolor')
            layout.separator()

        layout.prop(scene, 'xN_render_derivative', 'Derivative map')
        if scene.xN_render_derivative:
            box = layout.box()
            box.prop(scene, 'xN_derivative_bgcolor')
            layout.separator()

        layout.prop(scene, 'xN_render_radiosity', 'Radiosity map')
        if scene.xN_render_radiosity:
            box = layout.box()
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_radiosity_occl')
            col.prop(scene, 'xN_radiosity_pure_occl')
            col = split.column()
            col.prop(scene, 'xN_radiosity_limit_ray')
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_radiosity_rays')
            col.prop(scene, 'xN_radiosity_bias')
            col = split.column()
            col.prop(scene, 'xN_radiosity_spread')
            col.prop(scene, 'xN_radiosity_contrast')
            row = box.row()
            row.prop(scene, 'xN_radiosity_coord', text='Coordinates')
            row.prop(scene, 'xN_radiosity_distribution')
            row = box.row()
            row.prop(scene, 'xN_radiosity_atten1', text='Constant')
            row.prop(scene, 'xN_radiosity_atten2', text='Linear')
            row.prop(scene, 'xN_radiosity_atten3', text='Quadratic')
            box.prop(scene, 'xN_radiosity_bgcolor')
            layout.separator()

        layout.prop(scene, 'xN_render_PRT', 'PRT-p / PRT-n map')
        if scene.xN_render_PRT:
            box = layout.box()
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_prt_limit_ray')
            col = split.column()
            col.prop(scene, 'xN_prt_col_normalize')
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_prt_rays')
            col.prop(scene, 'xN_prt_bias')
            col = split.column()
            col.prop(scene, 'xN_prt_spread')
            col.prop(scene, 'xN_prt_threshold')
            box.prop(scene, 'xN_prt_bgcolor')
            layout.separator()

        layout.prop(scene, 'xN_render_thickness', 'Thickness map')

        layout.prop(scene, 'xN_render_vcolors', "Bake hipoly's vertex colors")
        if scene.xN_render_vcolors:
            box = layout.box()
            box.prop(scene, 'xN_vcolors_bgcolor')
            layout.separator()

        layout.prop(scene, 'xN_render_wireframe_rayfails', 'Render wireframe and rayfails')
        if scene.xN_render_wireframe_rayfails:
            box = layout.box()
            split = box.split()
            col = split.column()
            col.prop(scene, 'xN_wire_render_rf')
            col = split.column()
            col.prop(scene, 'xN_wire_render_wire')
            row = box.row()
            row.prop(scene, 'xN_wire_CW')
            row.prop(scene, 'xN_wire_color', text='Wire color')
            row = box.row()
            row.prop(scene, 'xN_wire_rf_color', text='Rayfail color')
            row.prop(scene, 'xN_wire_seam', 'Seam color')
            box.prop(scene, 'xN_wire_bgcolor')

#----------------------------------------------------


class PROPERTIES_PT_xN_ExportPanel(bpy.types.Panel):
    bl_label = "xNormal Import / Export"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # layout.prop(scene, 'xN_render_Base')
        row = layout.row()
        row.prop(scene, 'xN_discard_BF')
        row.prop(scene, 'xN_file_overwrite', text='Allow mesh overwrite')
        layout.prop(scene, 'xN_closest_hit')
        layout.prop(scene, 'xN_dimensions_X')
        layout.prop(scene, 'xN_dimensions_Y')
        layout.prop(scene, 'xN_edge_padding', icon='BLENDER', toggle=True)
        layout.prop(scene, 'xN_bucket_size')
        layout.prop(scene, 'xN_AA_setting')
        layout.prop(scene, 'xN_img_format')
#        layout.prop(scene, 'xN_export_type')
        layout.prop(scene, 'xN_output')
        layout.prop(scene, 'xN_exec_path')
        layout.prop(scene, 'xN_proj_name')
        layout.separator()

        row = layout.row()
        row.label(text="Generate maps with xNormal:")
        row.label(text="Import the maps from xNormal:")
        row = layout.row()
        row.operator("xnormal.export", icon="EXPORT")

        row.operator("xnormal.import", text="Import Maps", icon='BLENDER')

        layout.separator()

        row = layout.row(align=True)
        row.scale_y = 2.0
        row.operator("xnormal.launch")

#-------------------------------------------------------------
# Function for getting all the objects in the scene for EnumProps


def get_objects(scene, context):
    objects = []
    for object in bpy.context.scene.objects:
        if object.type == 'MESH':
            objects.append((object.name, object.name, ""))

    return objects
#-------------------------------------------------------------

swizzle_coords = [
    ('X+', 'X+', ''),
    ('X-', 'X-', ''),
    ('Y+', 'Y+', ''),
    ('Y-', 'Y-', ''),
    ('Z+', 'Z+', ''),
    ('Z-', 'Z-', '')]

normalization = [
    ('Interactive', 'Interactive', ''),
    ('Manual', 'Manual', ''),
    ('Raw', 'Raw FP Values', '')]

distribution = [
    ('Uniform', 'Uniform', ''),
    ('Cosine', 'Cosine', ''),
    ('Cosinesq', 'Cosinesq', '')]

algorithm = [
    ('Average', 'Average', ''),
    ('Gaussian', 'Gaussian', '')]

coord_system = [
    ('AliB', 'AliB', ''),
    ('OpenGL', 'OpenGL', ''),
    ('Direct3D', 'Direct3D', '')]

tonemapping = [
    ('Monocrome', 'Monochrome', ''),
    ('2Col', 'Two Colors', ''),
    ('3Col', 'Three Colors', '')]


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.xN_hipoly = EnumProperty(items=get_objects, name="Hi-poly object")
    bpy.types.Scene.xN_lowpoly = EnumProperty(items=get_objects, name="Low-poly object")
    bpy.types.Scene.xN_cage_obj = EnumProperty(items=get_objects, name="Cage object")
    bpy.types.Scene.xN_cage_external = BoolProperty(name="Use external file", description="Use external file for cage object", default=False)
    bpy.types.Scene.xN_render_AO = BoolProperty(
        name="Render Ambient Occlusion Map",
        description="xNormal will generate AO map.",
        default=False)

    #----------

    bpy.types.Scene.xN_render_Normal = BoolProperty(
        name="Render Normal Map",
        description="xNormal will generate normal map.",
        default=False)

    #-----------

    bpy.types.Scene.xN_render_Height = BoolProperty(
        name="Render Height Map",
        description="xNormal will generate height map.",
        default=False)

    #-----------

    bpy.types.Scene.xN_render_Base = BoolProperty(
        name="Render Base Texture Map",
        description="xNormal will generate base texture map.",
        default=False)

    #-----------

    bpy.types.Scene.xN_discard_BF = BoolProperty(
        name="Discard backfaces hits",
        description="Baking option",
        default=True)

    #-----------

    bpy.types.Scene.xN_closest_hit = BoolProperty(
        name="Closest hit if ray fails",
        description="Baking option",
        default=True)

    #-----------

    bpy.types.Scene.xN_dimensions_X = EnumProperty(
        items=[("16", "16", ""),
               ("32", "32", ""),
               ("64", "64", ""),
               ("128", "128", ""),
               ("256", "256", ""),
               ("512", "512", ""),
               ("1024", "1024", ""),
               ("2048", "2048", ""),
               ("4096", "4096", "")],
        name="Image Size X",
        description="",
        default="512")

    #-----------

    bpy.types.Scene.xN_dimensions_Y = EnumProperty(
        items=[("16", "16", ""),
               ("32", "32", ""),
               ("64", "64", ""),
               ("128", "128", ""),
               ("256", "256", ""),
               ("512", "512", ""),
               ("1024", "1024", ""),
               ("2048", "2048", ""),
               ("4096", "4096", "")],
        name="Image Size Y",
        description="",
        default="512")

    #-----------

    bpy.types.Scene.xN_edge_padding = IntProperty(
        name="Edge Padding",
        description="Image edge padding",
        default=16,
        min=0,
        max=128,
        step=1)

    #-----------

    bpy.types.Scene.xN_bucket_size = EnumProperty(
        items=[("16", "16", ""),
               ("32", "32", ""),
               ("64", "64", ""),
               ("128", "128", ""),
               ("256", "256", ""),
               ("512", "512", "")],
        name="Bucket size",
        description="")

    #--------------

    bpy.types.Scene.xN_AA_setting = EnumProperty(
        items=[('1', '1x', ''),
               ('2', '2x', ''),
               ('4', '4x', '')],
        name="Antialiasing samples",
        description="")

    #--------------

    bpy.types.Scene.xN_output = StringProperty(
        name="Export path",
        description="File location for exporting .obj and saving maps",
        default='',
        subtype='DIR_PATH')

    #---------------
    bpy.types.Scene.xN_proj_name = StringProperty(
        name="Project name",
        description="Generic name to use for baked images",
        default='')
    #---------------

    bpy.types.Scene.xN_img_format = EnumProperty(
        items=[('.png', 'PNG', ''),
               ('.tga', 'TGA', ''),
               ('.jpg', 'JPG', '')],
        name="Image format",
        description="")

    #----------------

    bpy.types.Scene.xN_exec_path = StringProperty(
        name="Path to xNormal",
        description="Path to the xNormal .exe",
        default='',
        subtype='DIR_PATH')

    #----------------

    bpy.types.Scene.xN_normal_swizzle1 = EnumProperty(items=swizzle_coords, name='', description='', default='X+')

    bpy.types.Scene.xN_normal_swizzle2 = EnumProperty(items=swizzle_coords, name='', description='', default='Y+')

    bpy.types.Scene.xN_normal_swizzle3 = EnumProperty(items=swizzle_coords, name='', description='', default='Z+')

    bpy.types.Scene.xN_normal_tangent_space = BoolProperty(name='Tangent space', description='Generate tangent space normal map. Otherwise, use object space', default=True)

    bpy.types.Scene.xN_normal_bgcolor = FloatVectorProperty(name='Background color', description='Background color of the normal map', default=(0.502, 0.502, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #----------------

    bpy.types.Scene.xN_height_bgcolor = FloatVectorProperty(name='Background color', description='Background color of the height map', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    bpy.types.Scene.xN_height_normalization = EnumProperty(items=normalization, name='Normalization', description='Normalization mode', default='Interactive')

    bpy.types.Scene.xN_height_manual_min = FloatProperty(name='Min', description='', default=0.00000, precision=5)
    bpy.types.Scene.xN_height_manual_max = FloatProperty(name='Max', description='', default=0.00000, precision=5)

    #--------------

    bpy.types.Scene.xN_AO_rays = IntProperty(name='Rays', description='', default=128, min=0)

    bpy.types.Scene.xN_AO_distribution = EnumProperty(items=distribution, name='Distribution', description='Distribution mode', default='Uniform')

    bpy.types.Scene.xN_AO_occluded_col = FloatVectorProperty(name='Occluded color', description='Occluded color', default=(0.0, 0.0, 0.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    bpy.types.Scene.xN_AO_unoccluded_col = FloatVectorProperty(name='Unoccluded color', description='Unoccluded color', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    bpy.types.Scene.xN_AO_bias = FloatProperty(name='Bias', description='', default=0.080000, precision=6)

    bpy.types.Scene.xN_AO_spread_angle = FloatProperty(name='Spread angle', description='', default=162.00)

    bpy.types.Scene.xN_AO_limit_ray = BoolProperty(name='Limit ray distance', description='Limit ray distance', default=False)

    bpy.types.Scene.xN_AO_atten1 = FloatProperty(name='', description='', default=1.00000)
    bpy.types.Scene.xN_AO_atten2 = FloatProperty(name='', description='', default=0.00000)
    bpy.types.Scene.xN_AO_atten3 = FloatProperty(name='', description='', default=0.00000)

    bpy.types.Scene.xN_AO_jitter = BoolProperty(name='Jitter', description='', default=False)

    bpy.types.Scene.xN_AO_ignore_bf = BoolProperty(name='Ignore backface hits', description='', default=False)
    bpy.types.Scene.xN_AO_allow_full = BoolProperty(name='Allow 100% occlusion', description='Allow 100% occlusion', default=True)

    bpy.types.Scene.xN_AO_bgcolor = FloatVectorProperty(name='Background color', description='', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #-------------

    bpy.types.Scene.xN_render_Bent = BoolProperty(name='Bent normal map', description='Render bent normal map', default=False)
    bpy.types.Scene.xN_bent_rays = IntProperty(name='Rays', description='', default=128, min=0)
    bpy.types.Scene.xN_bent_bias = FloatProperty(name='Bias', description='', default=0.080000, precision=6)

    bpy.types.Scene.xN_bent_spread = FloatProperty(name='Spread angle', description='', default=162.00)
    bpy.types.Scene.xN_bent_limit_ray = BoolProperty(name='Limit ray distance', description='', default=False)

    bpy.types.Scene.xN_bent_jitter = BoolProperty(name='Jitter', description='', default=False)
    bpy.types.Scene.xN_bent_swizzle1 = EnumProperty(items=swizzle_coords, name='', description='', default='X+')
    bpy.types.Scene.xN_bent_swizzle2 = EnumProperty(items=swizzle_coords, name='', description='', default='Y+')
    bpy.types.Scene.xN_bent_swizzle3 = EnumProperty(items=swizzle_coords, name='', description='', default='Z+')

    bpy.types.Scene.xN_bent_tanspace = BoolProperty(name='Tangent space', description='Generate tangent space normal map, otherwise use object space', default=False)

    bpy.types.Scene.xN_bent_distribution = EnumProperty(items=distribution, name='Distribution', description='', default='Uniform')
    bpy.types.Scene.xN_bent_bgcolor = FloatVectorProperty(name='Background color', description='Background color', default=(0.502, 0.502, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #-------------

    bpy.types.Scene.xN_render_PRT = BoolProperty(name='PRT-p / PRT-n', description='Render PRT-p / PRT-n', default=False)
    bpy.types.Scene.xN_prt_rays = IntProperty(name='Rays', description='', default=128)
    bpy.types.Scene.xN_prt_bias = FloatProperty(name='Bias', description='', default=0.080000, precision=6)
    bpy.types.Scene.xN_prt_spread = FloatProperty(name='Spread angle', description='', default=179.50)
    bpy.types.Scene.xN_prt_limit_ray = BoolProperty(name='Limit ray distance', description='', default=False)
    bpy.types.Scene.xN_prt_col_normalize = BoolProperty(name='PRT color normalize', description='', default=True)
    bpy.types.Scene.xN_prt_threshold = FloatProperty(name='Threshold', description='', default=0.005000, precision=6)
    bpy.types.Scene.xN_prt_bgcolor = FloatVectorProperty(name='Background color', description='Background color', default=(0.0, 0.0, 0.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #-------------
    bpy.types.Scene.xN_render_convexity = BoolProperty(name='Convexity map', description='Render convexity map', default=False)
    bpy.types.Scene.xN_convexity_scale = FloatProperty(name='Scale', description='', default=1.000, precision=3)
    bpy.types.Scene.xN_convexity_bgcolor = FloatVectorProperty(name='Background color', description='', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #------------

    bpy.types.Scene.xN_render_thickness = BoolProperty(name='Thickness map', description='Render thickness map', default=False)

    #-------------
    bpy.types.Scene.xN_render_proximity = BoolProperty(name='Proximity map', description='Render proximity map', default=False)
    bpy.types.Scene.xN_prox_rays = IntProperty(name='Rays', description='Rays', default=128)
    bpy.types.Scene.xN_prox_spread = FloatProperty(name='Spread angle', description='', default=80.00)
    bpy.types.Scene.xN_prox_limit_ray = BoolProperty(name='Limit ray distance', description='', default=False)
    bpy.types.Scene.xN_prox_bgcolor = FloatVectorProperty(name='Background color', description='', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #-------------
    bpy.types.Scene.xN_render_cavity = BoolProperty(name='Cavity map', description='Render cavity map', default=False)
    bpy.types.Scene.xN_cavity_rays = IntProperty(name='Rays', description='', default=128)
    bpy.types.Scene.xN_cavity_jitter = BoolProperty(name='Jitter', description='', default=False)
    bpy.types.Scene.xN_cavity_radius = FloatProperty(name='Radius', description='', default=0.500000, precision=6)
    bpy.types.Scene.xN_cavity_contrast = FloatProperty(name='Contrast', description='', default=1.250, precision=3)
    bpy.types.Scene.xN_cavity_steps = IntProperty(name='Steps', description='', default=4, min=0)
    bpy.types.Scene.xN_cavity_bgcolor = FloatVectorProperty(name='Background color', description='', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #------------
    bpy.types.Scene.xN_render_wireframe_rayfails = BoolProperty(name='Wireframe and ray fails', description='Render wireframe and ray fails', default=False)
    bpy.types.Scene.xN_wire_render_wire = BoolProperty(name='Render wireframe', description='Render wireframe', default=True)
    bpy.types.Scene.xN_wire_color = FloatVectorProperty(name='Wireframe color', description='', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')
    bpy.types.Scene.xN_wire_CW = FloatVectorProperty(name='CW', description='', default=(0.0, 0.0, 1.0), min=0.0, max=1.0, precision=3, subtype='COLOR')
    bpy.types.Scene.xN_wire_seam = FloatVectorProperty(name='Seam', description='', default=(0.0, 1.0, 0.0), min=0.0, max=1.0, precision=3, subtype='COLOR')
    bpy.types.Scene.xN_wire_render_rf = BoolProperty(name='Render rayfails', description='', default=True)
    # Only show if above is true
    bpy.types.Scene.xN_wire_rf_color = FloatVectorProperty(name='Color', description='', default=(1.0, 0.0, 0.0), min=0.0, max=1.0, precision=3, subtype='COLOR')
    bpy.types.Scene.xN_wire_bgcolor = FloatVectorProperty(name='Background color', description='', default=(0.0, 0.0, 0.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #----------
    bpy.types.Scene.xN_render_direction = BoolProperty(name='Direction map', description='', default=False)
    bpy.types.Scene.xN_direction_swizzle1 = EnumProperty(items=swizzle_coords, name='', description='', default='X+')
    bpy.types.Scene.xN_direction_swizzle2 = EnumProperty(items=swizzle_coords, name='', description='', default='Y+')
    bpy.types.Scene.xN_direction_swizzle3 = EnumProperty(items=swizzle_coords, name='', description='', default='Z+')
    bpy.types.Scene.xN_direction_tanspace = BoolProperty(name='Tangent space', description='Generate tangent space normal map, otherwise use object space', default=True)
    bpy.types.Scene.xN_direction_bgcolor = FloatVectorProperty(name='Background color', description='', default=(0.0, 0.0, 0.0), min=0.0, max=1.0, precision=3, subtype='COLOR')
    bpy.types.Scene.xN_direction_normalization = EnumProperty(items=normalization, name='Normalization', description='Normalization', default='Interactive')
    bpy.types.Scene.xN_direction_manual_min = FloatProperty(name='Min', description='', default=0.00000, precision=5)
    bpy.types.Scene.xN_direction_manual_max = FloatProperty(name='Max', description='', default=0.00000, precision=5)

    #----------
    bpy.types.Scene.xN_render_radiosity = BoolProperty(name='Radiosity map', description='Render radiosity map', default=False)
    bpy.types.Scene.xN_radiosity_rays = IntProperty(name='Rays', description='', default=128, min=0)
    bpy.types.Scene.xN_radiosity_occl = BoolProperty(name='Encode occlusion', description='', default=True)
    bpy.types.Scene.xN_radiosity_distribution = EnumProperty(items=distribution, name='Distribution', description='Distribution', default='Uniform')
    bpy.types.Scene.xN_radiosity_bias = FloatProperty(name='Bias', description='', default=0.080000, precision=6)
    bpy.types.Scene.xN_radiosity_spread = FloatProperty(name='Spread angle', description='', default=162.00)
    bpy.types.Scene.xN_radiosity_limit_ray = BoolProperty(name='Limit ray distance', description='', default=False)
    bpy.types.Scene.xN_radiosity_atten1 = FloatProperty(name='', description='', default=1.00000, precision=5)
    bpy.types.Scene.xN_radiosity_atten2 = FloatProperty(name='', description='', default=0.00000, precision=5)
    bpy.types.Scene.xN_radiosity_atten3 = FloatProperty(name='', description='', default=0.00000, precision=5)
    bpy.types.Scene.xN_radiosity_coord = EnumProperty(items=coord_system, name='Coordinate system', description='Coordinate system', default='AliB')
    bpy.types.Scene.xN_radiosity_contrast = FloatProperty(name='Contrast', description='', default=1.00000, precision=5)
    bpy.types.Scene.xN_radiosity_pure_occl = BoolProperty(name='Allow pure occlusion', description='', default=False)
    bpy.types.Scene.xN_radiosity_bgcolor = FloatVectorProperty(name='Background color', description='Background color', default=(0.0, 0.0, 0.0), min=0.0, max=1.0, subtype='COLOR')

    #----------------------
    bpy.types.Scene.xN_render_vcolors = BoolProperty(name="Bake highpoly's vertex colors", description="Render highpoly's vertex colors as map", default=False)
    bpy.types.Scene.xN_vcolors_bgcolor = FloatVectorProperty(name='Background color', description='', default=(1.0, 1.0, 1.0), min=0.0, max=1.0, subtype='COLOR')

    #-----------------
    bpy.types.Scene.xN_render_curvature = BoolProperty(name='Curvature map', description='Render curvature map', default=False)
    bpy.types.Scene.xN_curvature_rays = IntProperty(name='Rays', description='', default=128)
    bpy.types.Scene.xN_curvature_jitter = BoolProperty(name='Jitter', description='', default=False)
    bpy.types.Scene.xN_curvature_spread = FloatProperty(name='Spread angle', description='', default=162.00)
    bpy.types.Scene.xN_curvature_bias = FloatProperty(name='Bias', description='', default=0.0001000000, precision=10)
    bpy.types.Scene.xN_curvature_algorithm = EnumProperty(items=algorithm, name='Algorithm', description='', default='Average')
    bpy.types.Scene.xN_curvature_distribution = EnumProperty(items=distribution, name='Distribution', description='', default='Cosine')
    bpy.types.Scene.xN_curvature_search = FloatProperty(name='Search distance', description='', default=1.00000000, precision=8)
    bpy.types.Scene.xN_curvature_tonemap = EnumProperty(items=tonemapping, name='Tonemapping', description='Tone mapping method', default='3Col')
    bpy.types.Scene.xN_curvature_smoothing = BoolProperty(name='Smoothing', description='', default=True)
    bpy.types.Scene.xN_curvature_bgcolor = FloatVectorProperty(name='Background color', description='Background color', default=(0.0, 0.0, 0.0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #---------------------
    bpy.types.Scene.xN_render_derivative = BoolProperty(name='Derivative map', description='Render derivative map', default=False)
    bpy.types.Scene.xN_derivative_bgcolor = FloatVectorProperty(name='Background color', description='', default=(0.498, 0.498, 0), min=0.0, max=1.0, precision=3, subtype='COLOR')

    #---------------------
    bpy.types.Scene.xN_hipoly_visible = BoolProperty(name='Visible', description='', default=True)
    bpy.types.Scene.xN_hipoly_mesh_scale = FloatProperty(name='Mesh scale', description='', default=1.000, precision=3)
    bpy.types.Scene.xN_hipoly_ignore_vcolor = BoolProperty(name='Ignore per-vertex color', description='', default=True)
    bpy.types.Scene.xN_hipoly_normalsmoothing = EnumProperty(items=[
        ('AverageNormals', 'Average normals', ''),
        ('UseExportedNormals', 'Use exported normals', ''),
        ('HardenNormals', 'Harden normals', '')],
        name='Smoothing',
        description='',
        default='UseExportedNormals')
    bpy.types.Scene.xN_lowpoly_visible = BoolProperty(name='Visible', description='', default=True)
    bpy.types.Scene.xN_lowpoly_max_front_ray = FloatProperty(name='Maximum frontal ray distance', description='', default=0.5)
    bpy.types.Scene.xN_lowpoly_max_rear_ray = FloatProperty(name='Maximum rear ray distance', description='', default=0.5)
    bpy.types.Scene.xN_lowpoly_use_cage = BoolProperty(name='Use cage', description='', default=False)
    bpy.types.Scene.xN_lowpoly_normalsmoothing = EnumProperty(items=[
        ('AverageNormals', 'Average normals', ''),
        ('UseExportedNormals', 'Use exported normals', ''),
        ('HardenNormals', 'Harden normals', '')],
        name='Smoothing',
        description='',
        default='UseExportedNormals')
    bpy.types.Scene.xN_lowpoly_batch = BoolProperty(name='Batch protection', description='', default=False)
    bpy.types.Scene.xN_lowpoly_normals_override = BoolProperty(name='Hipoly normals override tangent space', description='High poly normals override tangent space', default=True)
    bpy.types.Scene.xN_lowpoly_mesh_scale = FloatProperty(name='Mesh scale', description='', default=1.000, precision=3)
    bpy.types.Scene.xN_lowpoly_match_uvs = BoolProperty(name='Match UVs', description='', default=False)
    bpy.types.Scene.xN_lowpoly_U_offset = FloatProperty(name='U offset', description='', default=0.000, precision=3)
    bpy.types.Scene.xN_lowpoly_V_offset = FloatProperty(name='V offset', description='', default=0.000, precision=3)
    bpy.types.Scene.xN_export_type = EnumProperty(items=[
        ('obj', 'OBJ', 'If using .obj export, both objects MUST be on VISIBLE LAYERS when exporting or you will get errors'),
        ('ply', 'PLY', 'Use if baking highpoly vertex colors')],
        name='Export type',
        description='Mesh type to use for export',
        default='ply')
    bpy.types.Scene.xN_cage_file = StringProperty(subtype='FILE_PATH')
    bpy.types.Scene.xN_file_overwrite = BoolProperty(name="Allow file overwrite", description="If enabled, meshes will always be exported. Otherwise, they will only be exported if they do not currently exist in the output directory", default=True)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
