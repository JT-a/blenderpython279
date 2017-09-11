bl_info = {
    "name": "Wazou Popup Addon",
    "description": "",
    "author": "Your Name",
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

# Active Camera
#
# bpy.types.Scene.cameratoto = bpy.props.StringProperty(default="")
#
# class ActiveCameraSelection(bpy.types.Operator):
#    bl_idname = "object.activecameraselection"
#    bl_label = "Active Camera Selection"
#
#    def execute(self, context):
#        bpy.data.objects[context.scene.cameratoto].select=True
#        bpy.ops.view3d.object_as_camera()
#
#        return {'FINISHED'}
#
# Select Camera
# class CameraSelection(bpy.types.Operator):
#    bl_idname = "object.cameraselection"
#    bl_label = "Camera Selection"
#
#    def execute(self, context):
#
#        for cam in bpy.data.cameras:
#            bpy.ops.object.select_camera()
#
#        return {'FINISHED'}


bpy.types.WindowManager.render_simple = BoolProperty(
    name="IPR settings",
    description="Show Simples Render Settings",
    default=True)

bpy.types.WindowManager.cam_simple = BoolProperty(
    name="IPR settings",
    description="Show Simples Camera Settings",
    default=True)

bpy.types.WindowManager.lights_simple = BoolProperty(
    name="IPR settings",
    description="Show Simples Camera Settings",
    default=True)


bpy.types.WindowManager.render_popup = bpy.props.EnumProperty(
    items=(('Onglet_1', "Render", "Render"),
           ('Onglet_2', "Sampling", "Resolution"),
           ('Onglet_3', "LPaths", "Light Paths"),
           ('Onglet_4', "CManag..", "Color Management")),
    default='Onglet_1')


class Wazou_Popup(Operator):
    bl_idname = "view3d.wazou_popup"
    bl_label = "Wazou_Popup"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi
        return context.window_manager.invoke_props_dialog(self, width=dpi_value * 4, height=500)

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

        # Render
        if ob.type == 'MESH':

            layout.prop(WM, "render_simple", text="Simple Settings")
            if not WM.render_simple:
                layout = self.layout
                row = layout.row(align=True)
                row.prop(WM, "render_popup", text=" ", expand=True)
                if WM.render_popup == 'Onglet_1':

                    row = layout.row(align=True)
                    row.operator("render.render", text="Render", icon='RENDER_STILL')
                    row.prop(cscene, "feature_set", text="")
                    row = layout.row(align=True)
                    row.prop(cscene, "device", text="")

                    # CPU/GPU Compute
                    row.prop(system, "compute_device", text="")

                    # Reso
                    split = layout.split()
                    col = split.column()
                    sub = col.column(align=True)
                    sub.label(text="Resolution:")
                    sub.prop(rd, "resolution_x", text="X")
                    sub.prop(rd, "resolution_y", text="Y")
                    sub.prop(rd, "resolution_percentage", text="")

                    # Tiles
                    col = split.column(align=True)
                    sub = col.column(align=True)
                    sub.label(text="Tiles:")

                    sub.prop(rd, "tile_x", text="X")
                    sub.prop(rd, "tile_y", text="Y")
                    sub.prop(cscene, "use_progressive_refine", text="Progressive")

                    row = layout.row()
                    row.prop(cscene, "film_transparent")
                    row.prop(rd, "use_border", text="Border")

                # Sampling
                elif WM.render_popup == 'Onglet_2':
                    split = layout.split()

                    col = split.column()
                    sub = col.column(align=True)
                    sub.label("Settings:")
                    sub.prop(cscene, "seed")
                    sub.prop(cscene, "sample_clamp_direct")
                    sub.prop(cscene, "sample_clamp_indirect")

                    col = split.column()
                    sub = col.column(align=True)
                    sub.label(text="Samples:")
                    sub.prop(cscene, "samples", text="Render")
                    sub.prop(cscene, "preview_samples", text="Preview")

                    row = layout.row()
                    row.label("Volume Heterogeneous:")
                    row = layout.row(align=True)
                    row.prop(cscene, "volume_step_size")
                    row.prop(cscene, "volume_max_steps")

                # Light_Pasths
                elif WM.render_popup == 'Onglet_3':
                    split = layout.split()
                    col = split.column()
                    sub = col.column(align=True)
                    sub.label("Transparency:")
                    sub.prop(cscene, "transparent_max_bounces", text="Max")
                    sub.prop(cscene, "transparent_min_bounces", text="Min")
                    sub.prop(cscene, "use_transparent_shadows", text="Shadows")

                    col.separator()

                    col.prop(cscene, "caustics_reflective", text="Refle Caustics")
                    col.prop(cscene, "caustics_refractive", text="Refra Caustics")
                    col.prop(cscene, "blur_glossy")

                    col = split.column()

                    sub = col.column(align=True)
                    sub.label(text="Bounces:")
                    sub.prop(cscene, "max_bounces", text="Max")
                    sub.prop(cscene, "min_bounces", text="Min")

                    sub = col.column(align=True)
                    sub.prop(cscene, "diffuse_bounces", text="Diffuse")
                    sub.prop(cscene, "glossy_bounces", text="Glossy")
                    sub.prop(cscene, "transmission_bounces", text="Transmission")
                    sub.prop(cscene, "volume_bounces", text="Volume")

                # Color Management
                elif WM.render_popup == 'Onglet_4':

                    col = layout.column()
                    col.label(text="Display:")
                    col.prop(scene.display_settings, "display_device")

                    col = layout.column()
                    col.separator()
                    col.label(text="Render:")
                    col.template_colormanaged_view_settings(scene, "view_settings")

                    col = layout.column()
                    col.separator()
                    col.label(text="Sequencer:")
                    col.prop(scene.sequencer_colorspace_settings, "name")

            else:
                # Reso
                layout.operator("render.render", text="Render", icon='RENDER_STILL')
                split = layout.split()
                col = split.column()
                sub = col.column(align=True)
                sub.label(text="Resolution:")
                sub.prop(rd, "resolution_x", text="X")
                sub.prop(rd, "resolution_y", text="Y")
                sub.prop(rd, "resolution_percentage", text="")

                col = split.column()
                sub = col.column(align=True)
                sub.label(text="Samples:")
                sub.prop(cscene, "samples", text="Render")
                sub.prop(cscene, "preview_samples", text="Preview")
                sub.prop(cscene, "use_progressive_refine", text="Progressive")

        elif ob.type == 'CAMERA':
            layout.prop(WM, "cam_simple", text="Simple Settings")
            if not WM.cam_simple:
                row = layout.row(align=True)
                row.prop(ob, "name", text="", icon='OUTLINER_DATA_CAMERA')

    #            row = layout.row(align=True)
                row.operator("view3d.viewnumpad", text="", icon='VISIBLE_IPO_ON').type = 'CAMERA'
    #            if context.space_data.lock_camera == False:
    #                row.operator("wm.context_toggle", text="", icon='UNLOCKED').data_path = "space_data.lock_camera"
    #            elif context.space_data.lock_camera == True:
    #                row.operator("wm.context_toggle", text="", icon='LOCKED').data_path = "space_data.lock_camera"

                row.operator("view3d.camera_to_view", text="", icon='MAN_TRANS')

                row.operator("view3d.object_as_camera", text="", icon='CURSOR')

                row.operator("object.delete", text="", icon='PANEL_CLOSE')

                row = layout.row()
                row.prop(context.object.data, "lens", text="Focal Length")
                row = layout.row()
                row.label("Clipping :")
                row = layout.row(align=True)
                row.prop(context.object.data, "clip_start", text="Start")
                row.prop(context.object.data, "clip_end", text="End")

                row = layout.row()
                row.label("Composition Guides :")
                row = layout.row()
                row.prop(context.object.data, "show_guide", text="Composition guides")

                row = layout.row()
                row.label("Depth Of Field :")

                row = layout.row()
                row.prop(context.object.data, "dof_object", text="")
                row.prop(context.object.data.cycles, "aperture_type", text="")

                row = layout.row()
                row.prop(context.object.data, "dof_distance", text="Distance")

                if context.object.data.cycles.aperture_type == 'RADIUS':
                    row.prop(context.object.data.cycles, "aperture_size", text="size")

                elif context.object.data.cycles.aperture_type == 'FSTOP':
                    row.prop(context.object.data.cycles, "aperture_fstop", text="size")
            else:

                layout.prop(context.object.data, "lens", text="Focal Length")
                row = layout.row()
                row.prop(context.object.data, "dof_object", text="")
                row.prop(context.object.data.cycles, "aperture_size", text="size")
                row = layout.row()
                row.prop(context.object.data, "show_guide", text="Composition guides")

        # Render
        if ob.type == 'LAMP':

            layout.prop(WM, "lights_simple", text="Simple Settings")
            if not WM.lights_simple:
                row = layout.row(align=True)
                if obj.data.type == 'AREA':
                    row.prop(ob, "name", text="", icon='LAMP_AREA')

                if obj.data.type == 'HEMI':
                    row.prop(ob, "name", text="", icon='LAMP_HEMI')

                if obj.data.type == 'SPOT':
                    row.prop(ob, "name", text="", icon='LAMP_SPOT')

                if obj.data.type == 'SUN':
                    row.prop(ob, "name", text="", icon='LAMP_SUN')

                if obj.data.type == 'POINT':
                    row.prop(ob, "name", text="", icon='LAMP_POINT')

                # Visibility, selection, Render, Delete
                row.prop(obj.data, "type", text="")
                row.prop(obj, "hide", icon='VISIBLE_IPO_ON', text="")
                row.prop(obj, "hide_select", icon='RESTRICT_SELECT_OFF', text="")
                row.prop(obj, "hide_render", icon='RESTRICT_RENDER_OFF', text="")
                row.operator("object.delete", text="", icon='PANEL_CLOSE')

                # Light Type
                row = layout.row()
                if obj.data.type in {'POINT', 'SUN'}:
                    row = layout.row()
                    row.prop(obj.data, "shadow_soft_size", text="Size")
                    row = layout.row(align=True)
                    row.prop(obj.data.cycles, "cast_shadow", text="Shadow")
                    row.prop(obj.data.cycles, "use_multiple_importance_sampling", text="MIS")

                if obj.data.type == 'AREA':
                    row = layout.row(align=True)
                    if obj.data.shape == 'SQUARE':
                        split = layout.split()
                        col = split.column(align=True)
                        sub = col.column(align=True)
                        sub.prop(obj.data, "shape", text="")
                        sub.prop(ob.data, "size")

                        sub = col.column(align=True)

                        sub.prop(obj.data.cycles, "cast_shadow", text="Shadow")
                        sub.prop(obj.data.cycles, "use_multiple_importance_sampling", text="MIS")

                    elif obj.data.shape == 'RECTANGLE':

                        row = layout.row(align=True)
                        row.prop(obj.data, "shape", text="")
                        row.prop(obj.data, "size", text="X")
                        row.prop(obj.data, "size_y", text="Y")
                    row = layout.row()
                    row.prop(obj.data.cycles, "use_multiple_importance_sampling", text="MIS")
                    row.prop(obj.data.cycles, "cast_shadow", text="Shadow")

                if obj.data.type == 'HEMI':
                    row = layout.row(align=True)
                    row.prop(obj.data.cycles, "use_multiple_importance_sampling", text="MIS")
                    row.prop(obj.data.cycles, "cast_shadow", text="Shadow")
                    layout.label(text="Not supported, interpreted as sun lamp")

                if obj.data.type == 'SPOT':
                    row = layout.row()
                    row.prop(obj.data, "shadow_soft_size", text="Size")

                    row = layout.row(align=True)
                    row.prop(obj.data.cycles, "use_multiple_importance_sampling", text="MIS")
                    row.prop(obj.data.cycles, "cast_shadow", text="Shadow")

                    row = layout.row()
                    row.label("Spot Shape :")
                    row.prop(obj.data, "spot_size", text="Size")
                    row.prop(obj.object.data, "spot_blend", text="Blend", slider=True)
                    row.prop(obj.data, "show_cone")

                layout = self.layout
                cobj = context.active_object
                node_emission = cobj.data.node_tree.nodes["Emission"]

                layout.label("Light")
                row = layout.row(align=True)
                row.label("Color:")
                row.prop(node_emission.inputs[0], 'default_value', text='')
                row = layout.row(align=True)
                row.label("Strength:")
                row.prop(node_emission.inputs[1], 'default_value', text='')

            else:
                layout = self.layout
                cobj = context.active_object
                node_emission = cobj.data.node_tree.nodes["Emission"]

                layout.label("Light")
                row = layout.row(align=True)
                row.label("Color:")
                row.prop(node_emission.inputs[0], 'default_value', text='')
                row = layout.row(align=True)
                row.label("Strength:")
                row.prop(node_emission.inputs[1], 'default_value', text='')


addon_keymaps = []


def register():
    bpy.utils.register_module(__name__)

    global addon_keymaps
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(Wazou_Popup.bl_idname, 'LEFTMOUSE', 'DOUBLE_CLICK', shift=True)

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
