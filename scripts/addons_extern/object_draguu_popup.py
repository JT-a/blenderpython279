bl_info = {
    "name": "Popup Menu",
    "description": "",
    "author": "Draguu",
    "version": (0, 0, 1),
    "blender": (2, 76, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object"}


import bpy
from bpy.types import Menu, Panel, UIList, Operator
from rna_prop_ui import PropertyPanel
from bpy.props import PointerProperty, StringProperty, BoolProperty, \
    EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, \
    CollectionProperty, BoolVectorProperty


bpy.types.WindowManager.render_simple = BoolProperty(
    name="IPR settings",
    description="Show Simples Render Settings",
    default=False)

bpy.types.WindowManager.cam_simple = BoolProperty(
    name="IPR settings",
    description="Show Simples Camera Settings",
    default=False)

bpy.types.WindowManager.lights_simple = BoolProperty(
    name="IPR settings",
    description="Show Simples Camera Settings",
    default=False)
bpy.types.WindowManager.shading_render = BoolProperty(
    name="rendershading",
    description="show shading settings",
    default=False)
bpy.types.WindowManager.performance_render = BoolProperty(
    name="renderperformance",
    description="show performance settings",
    default=False)
bpy.types.WindowManager.post_render = BoolProperty(
    name="renderpost",
    description="show post settings",
    default=False)
bpy.types.WindowManager.meta_render = BoolProperty(
    name="rendermeta",
    description="show metadata settings",
    default=False)
bpy.types.WindowManager.out_render = BoolProperty(
    name="renderout",
    description="show output settings",
    default=False)
bpy.types.WindowManager.bake_render = BoolProperty(
    name="renderbake",
    description="show bake settings",
    default=False)
bpy.types.WindowManager.layer_layer = BoolProperty(
    name="layerlayer",
    description="show layer settings",
    default=False)
bpy.types.WindowManager.passes_layer = BoolProperty(
    name="passes_layer",
    description="show passes settings",
    default=False)


bpy.types.WindowManager.render_popup = bpy.props.EnumProperty(
    items=(('Onglet_1', "Render", "Render"),
           ('Onglet_2', "layers", "Resolution"),
           ('Onglet_3', "Scene", "Resolution"),
           ('Onglet_4', "World", "Light Paths"),
           ('Onglet_5', "object", "Resolution"),
           ('Onglet_6', "CManag..", "Color Management")),
    default='Onglet_1')


class draguu_Popup(Operator):
    bl_idname = "view3d.draguu_popup"
    bl_label = "Popup Menus"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi
        return context.window_manager.invoke_props_dialog(self, width=dpi_value * 6, height=-550)

    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        WM = bpy.context.window_manager
        row = layout.row(align=True)
        scene = context.scene
        cscene = scene.cycles
        rd = scene.render
        system = context.user_preferences.system
        ob = bpy.context.object
        obj = context.object
        COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_GAME'}

        # Render
        if ob.type == 'MESH':

            row.prop(WM, "render_popup", text=" ", expand=True)
            if WM.render_popup == 'Onglet_1':

                layout = self.layout

                rd = context.scene.render

                row = layout.row(align=True)
                row.operator("render.render", text="Render", icon='RENDER_STILL')
                row.operator("render.render", text="Animation", icon='RENDER_ANIMATION').animation = True

                split = layout.split(percentage=0.33)

                split.label(text="Display:")
                row = split.row(align=True)
                row.prop(rd, "display_mode", text="")
                row.prop(rd, "use_lock_interface", icon_only=True)

                # CPU/GPU Compute
                # row.prop(system, "compute_device", text="")

                # Reso

                split = layout.split()

                col = split.column()
                sub = col.column(align=True)
                sub.label(text="Resolution:")
                sub.prop(rd, "resolution_x", text="X")
                sub.prop(rd, "resolution_y", text="Y")
                sub.prop(rd, "resolution_percentage", text="")

                sub.label(text="Aspect Ratio:")
                sub.prop(rd, "pixel_aspect_x", text="X")
                sub.prop(rd, "pixel_aspect_y", text="Y")

                row = col.row()
                row.prop(rd, "use_border", text="Border")
                sub = row.row()
                sub.active = rd.use_border
                sub.prop(rd, "use_crop_to_border", text="Crop")

                col = split.column()
                sub = col.column(align=True)
                sub.label(text="Frame Range:")
                sub.prop(scene, "frame_start")
                sub.prop(scene, "frame_end")
                sub.prop(scene, "frame_step")

                sub.label(text="Frame Rate:")

                # self.draw_framerate(sub, rd)
                # sub.menu("RENDER_MT_framerate_presets", text=fps_label_text)
                subrow = sub.row(align=True)
                subrow.label(text="Time Remapping:")
                subrow = sub.row(align=True)
                subrow.prop(rd, "frame_map_old", text="Old")
                subrow.prop(rd, "frame_map_new", text="New")
                self.layout.label(text="________________________________________________________________________________________")

                self.layout.prop(rd, "use_antialiasing", text="Anti-Aliasing")

                if layout.active == rd.use_antialiasing:

                    split = layout.split()

                    col = split.column()
                    col.row().prop(rd, "antialiasing_samples", expand=True)
                    sub = col.row()
                    sub.enabled = not rd.use_border
                    sub.prop(rd, "use_full_sample")

                    col = split.column()
                    col.prop(rd, "pixel_filter_type", text="")
                    col.prop(rd, "filter_size", text="Size")


# shading
                self.layout.label(text="________________________________________________________________________________________")
                layout.prop(WM, "shading_render", text="Shading Menu")
                if layout.active == WM.shading_render:
                    self.layout.label(text="Shading:")

                    split = layout.split()
                    col = split.column()

                    col.prop(rd, "use_textures", text="Textures")
                    col.prop(rd, "use_shadows", text="Shadows")
                    col.prop(rd, "use_sss", text="Subsurface Scattering")
                    col.prop(rd, "use_envmaps", text="Environment Map")

                    col = split.column()
                    col.prop(rd, "use_raytrace", text="Ray Tracing")
                    col.prop(rd, "alpha_mode", text="Alpha")
 # performance
                self.layout.label(text="________________________________________________________________________________________")

                layout.prop(WM, "performance_render", text="Performance Menu")
                if layout.active == WM.performance_render:

                    split = layout.split()

                    col = split.column(align=True)
                    col.label(text="Threads:")
                    col.row(align=True).prop(rd, "threads_mode", expand=True)
                    sub = col.column(align=True)
                    sub.enabled = rd.threads_mode == 'FIXED'
                    sub.prop(rd, "threads")

                    col.label(text="Tile Size:")
                    col.prop(rd, "tile_x", text="X")
                    col.prop(rd, "tile_y", text="Y")

                    col.separator()
                    col.prop(rd, "preview_start_resolution")

                    col = split.column()
                    col.label(text="Memory:")
                    sub = col.column()
                    sub.enabled = not (rd.use_border or rd.use_full_sample)
                    sub.prop(rd, "use_save_buffers")
                    sub = col.column()
                    sub.active = rd.use_compositing
                    sub.prop(rd, "use_free_image_textures")
                    sub.prop(rd, "use_free_unused_nodes")
                    sub = col.column()
                    sub.active = rd.use_raytrace
                    sub.label(text="Acceleration structure:")
                    sub.prop(rd, "raytrace_method", text="")
                    if rd.raytrace_method == 'OCTREE':
                        sub.prop(rd, "octree_resolution", text="Resolution")
                    else:
                        sub.prop(rd, "use_instances", text="Instances")
                    sub.prop(rd, "use_local_coords", text="Local Coordinates")

# postprocessing
                self.layout.label(text="________________________________________________________________________________________")

                layout.prop(WM, "post_render", text="Post-Processing")
                if layout.active == WM.post_render:
                    split = layout.split()

                    col = split.column()
                    col.prop(rd, "use_compositing")
                    col.prop(rd, "use_sequencer")

                    split.prop(rd, "dither_intensity", text="Dither", slider=True)

                    layout.separator()

                    split = layout.split()

                    col = split.column()
                    col.prop(rd, "use_fields", text="Fields")
                    sub = col.column()
                    sub.active = rd.use_fields
                    sub.row().prop(rd, "field_order", expand=True)
                    sub.prop(rd, "use_fields_still", text="Still")

                    col = split.column()
                    col.prop(rd, "use_edge_enhance")
                    sub = col.column()
                    sub.active = rd.use_edge_enhance
                    sub.prop(rd, "edge_threshold", text="Threshold", slider=True)
                    sub.prop(rd, "edge_color", text="")
# output
                self.layout.label(text="________________________________________________________________________________________")

                layout.prop(WM, "out_render", text="Output")
                if layout.active == WM.out_render:

                    image_settings = rd.image_settings
                    file_format = image_settings.file_format
                    layout.prop(rd, "filepath", text="")
                    split = layout.split()

                    col = split.column()
                    col.active = not rd.is_movie_format
                    col.prop(rd, "use_overwrite")
                    col.prop(rd, "use_placeholder")

                    col = split.column()
                    col.prop(rd, "use_file_extension")
                    col.prop(rd, "use_render_cache")

                    layout.template_image_settings(image_settings, color_management=False)
                    if rd.use_multiview:
                        layout.template_image_views(image_settings)

                    if file_format == 'QUICKTIME':
                        quicktime = rd.quicktime

                        split = layout.split()
                        col = split.column()
                        col.prop(quicktime, "codec_type", text="Video Codec")
                        col.prop(quicktime, "codec_spatial_quality", text="Quality")

                        # Audio
                        col.prop(quicktime, "audiocodec_type", text="Audio Codec")
                        if quicktime.audiocodec_type != 'No audio':
                            split = layout.split()
                            if quicktime.audiocodec_type == 'LPCM':
                                split.prop(quicktime, "audio_bitdepth", text="")

                            split.prop(quicktime, "audio_samplerate", text="")

                            split = layout.split()
                            col = split.column()
                            if quicktime.audiocodec_type == 'AAC':
                                col.prop(quicktime, "audio_bitrate")

                            subsplit = split.split()
                            col = subsplit.column()

                            if quicktime.audiocodec_type == 'AAC':
                                col.prop(quicktime, "audio_codec_isvbr")

                            col = subsplit.column()
                            col.prop(quicktime, "audio_resampling_hq")
# bake
                self.layout.label(text="________________________________________________________________________________________")

                layout.prop(WM, "bake_render", text="Bake")
                if layout.active == WM.bake_render:
                    rd = context.scene.render

                    layout.operator("object.bake_image", icon='RENDER_STILL')

                    layout.prop(rd, "bake_type")

                    multires_bake = False
                    if rd.bake_type in ['NORMALS', 'DISPLACEMENT', 'DERIVATIVE', 'AO']:
                        layout.prop(rd, "use_bake_multires")
                        multires_bake = rd.use_bake_multires

                    if not multires_bake:
                        if rd.bake_type == 'NORMALS':
                            layout.prop(rd, "bake_normal_space")
                        elif rd.bake_type in {'DISPLACEMENT', 'AO'}:
                            layout.prop(rd, "use_bake_normalize")

                        # col.prop(rd, "bake_aa_mode")
                        # col.prop(rd, "use_bake_antialiasing")

                        layout.separator()

                        split = layout.split()

                        col = split.column()
                        col.prop(rd, "use_bake_to_vertex_color")
                        sub = col.column()
                        sub.active = not rd.use_bake_to_vertex_color
                        sub.prop(rd, "use_bake_clear")
                        sub.prop(rd, "bake_margin")
                        sub.prop(rd, "bake_quad_split", text="Split")

                        col = split.column()
                        col.prop(rd, "use_bake_selected_to_active")
                        sub = col.column()
                        sub.active = rd.use_bake_selected_to_active
                        sub.prop(rd, "bake_distance")
                        sub.prop(rd, "bake_bias")
                    else:
                        split = layout.split()

                        col = split.column()
                        col.prop(rd, "use_bake_clear")
                        col.prop(rd, "bake_margin")

                        if rd.bake_type == 'DISPLACEMENT':
                            col = split.column()
                            col.prop(rd, "use_bake_lores_mesh")

                        if rd.bake_type == 'AO':
                            col = split.column()
                            col.prop(rd, "bake_bias")
                            col.prop(rd, "bake_samples")

                    if rd.bake_type == 'DERIVATIVE':
                        row = layout.row()
                        row.prop(rd, "use_bake_user_scale", text="")

                        sub = row.column()
                        sub.active = rd.use_bake_user_scale
                        sub.prop(rd, "bake_user_scale", text="User Scale")


# layerbutton
            elif WM.render_popup == 'Onglet_2':
                split = layout.split()
                col = split.column()
                sub = col.column(align=True)
                sub.label("Transparency:")
                sub.prop(cscene, "transparent_max_bounces", text="Max")
                sub.prop(cscene, "transparent_min_bounces", text="Min")
                sub.prop(cscene, "use_transparent_shadows", text="Shadows")

# layers
                self.layout.label(text="________________________________________________________________________________________")

                layout.prop(WM, "layer_layer", text="Layer")
                if layout.active == WM.layer_layer:

                    rd = scene.render
                    rl = rd.layers.active

                    split = layout.split()

                    col = split.column()
                    col.prop(scene, "layers", text="Scene")
                    col.label(text="")
                    col.prop(rl, "light_override", text="Lights")
                    col.prop(rl, "material_override", text="Material")

                    col = split.column()
                    col.prop(rl, "layers", text="Layer")
                    col.prop(rl, "layers_zmask", text="Mask Layer")

                    layout.separator()
                    layout.label(text="Include:")

                    split = layout.split()

                    col = split.column()
                    col.prop(rl, "use_zmask")
                    row = col.row()
                    row.prop(rl, "invert_zmask", text="Negate")
                    row.active = rl.use_zmask
                    col.prop(rl, "use_all_z")

                    col = split.column()
                    col.prop(rl, "use_solid")
                    col.prop(rl, "use_halo")
                    col.prop(rl, "use_ztransp")

                    col = split.column()
                    col.prop(rl, "use_sky")
                    col.prop(rl, "use_edge_enhance")
                    col.prop(rl, "use_strand")
                    if bpy.app.build_options.freestyle:
                        row = col.row()
                        row.prop(rl, "use_freestyle")
                        row.active = rd.use_freestyle
# layers
                self.layout.label(text="________________________________________________________________________________________")

                layout.prop(WM, "passes_layer", text="Passes")
                if layout.active == WM.passes_layer:
                    rd = scene.render
                    rl = rd.layers.active

                    split = layout.split()

                    col = split.column()
                    col.prop(rl, "use_pass_combined")
                    col.prop(rl, "use_pass_z")
                    col.prop(rl, "use_pass_vector")
                    col.prop(rl, "use_pass_normal")
                    col.prop(rl, "use_pass_uv")
                    col.prop(rl, "use_pass_mist")
                    col.prop(rl, "use_pass_object_index")
                    col.prop(rl, "use_pass_material_index")
                    col.prop(rl, "use_pass_color")

                    col = split.column()
                    col.prop(rl, "use_pass_diffuse")
                    self.draw_pass_type_buttons(col, rl, "specular")
                    self.draw_pass_type_buttons(col, rl, "shadow")
                    self.draw_pass_type_buttons(col, rl, "emit")
                    self.draw_pass_type_buttons(col, rl, "ambient_occlusion")
                    self.draw_pass_type_buttons(col, rl, "environment")
                    self.draw_pass_type_buttons(col, rl, "indirect")
                    self.draw_pass_type_buttons(col, rl, "reflection")
                    self.draw_pass_type_buttons(col, rl, "refraction")


addon_keymaps = []


def register():
    bpy.utils.register_module(__name__)

    global addon_keymaps
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(draguu_Popup.bl_idname, 'LEFTMOUSE', 'DOUBLE_CLICK', shift=False)

    addon_keymaps.append(km)


def unregister():
    bpy.utils.unregister_module(__name__)

    global addon_keymaps
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
