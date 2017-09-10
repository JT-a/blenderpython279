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

# <pep8 compliant>
import bpy
from bpy.types import Header, Menu
import mathutils
import os.path
import os, sys
import subprocess
import fnmatch

class INFO_OT_toggle_bone_selection(bpy.types.Operator):
    bl_idname = 'armature.toggle_bone_selection'
    bl_label = 'Toggle Selection'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    bone = bpy.props.StringProperty(
        name='Bone',
        options={'SKIP_SAVE'}
    )
    select = bpy.props.BoolProperty(
        name='Select',
        default=False,
        options={'SKIP_SAVE'}
    )

    @classmethod
    def register(cls):
        def get_func(self):
            try:
                bone = bpy.context.active_bone
            except:
                return False
            return bone.select

        def set_func(self, value):
            try:
                bone = bpy.context.active_bone
            except:
                return
            op = eval('bpy.ops.' + cls.bl_idname)
            op(bone=bone.name, select=value)

        bpy.types.Armature.active_bone_selection = bpy.props.BoolProperty(
            name='Active Bone Selection',
            get=get_func,
            set=set_func
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Armature.active_bone_selection

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        if ob and ob.type == 'ARMATURE':
            return ob.mode in {'EDIT', 'POSE'}
        return False

    def execute(self, context):
        ob = context.active_object
        arm = ob.data
        if ob.mode == 'POSE':
            if self.bone not in arm.bones:
                return {'CANCELLED'}
            bone = arm.bones[self.bone]
            bone.select ^= True
        else:
            if self.bone not in arm.edit_bones:
                return {'CANCELLED'}
            bone = arm.edit_bones[self.bone]
            if self.properties.is_property_set('select'):
                select = self.select
            else:
                select = not bone.select
            parent = bone.parent
            if select:
                bone.select = bone.select_head = bone.select_tail = True
                if parent and bone.use_connect:
                    parent.select_tail = True
                    if parent.select_head:
                        parent.select = True
                for child in bone.children:
                    if child.use_connect:
                        child.select_head = True
                        if child.select_tail:
                            child.select = True
            else:
                bone.select = False
                bone.select_tail = False
                if parent and bone.use_connect and parent.select:
                    pass
                else:
                    bone.select_head = False
                    if bone.use_connect:
                        parent.select_tail = False
                        for child in parent.children:
                            if child.use_connect:
                                child.select_head = False
                                child.select = False
                for child in bone.children:
                    if child.use_connect:
                        child.select_head = False
                        child.select = False

        ob.update_tag({'OBJECT', 'DATA'})

        return {'FINISHED'}


class INFO_HT_header(Header):
    bl_space_type = 'INFO'

    def draw(self, context):
        layout = self.layout

        window = context.window
        scene = context.scene
        rd = scene.render

        row = layout.row(align=True)
        row.template_header()

        INFO_MT_editor_menus.draw_collapsible(context, layout)

        if window.screen.show_fullscreen:
            layout.operator("screen.back_to_previous", icon='SCREEN_BACK', text="Back to Previous")
            layout.separator()
        else:
            layout.template_ID(context.window, "screen", new="screen.new", unlink="screen.delete")
            row = layout.row(align=True)
            row.template_ID(context.screen, "scene", new="scene.new", unlink="scene.delete")
            scenes = list(bpy.data.scenes)
            sub = row.row(align=True)
            sub.scale_x = 0.7  # 後ろの余白が多いので
            sub.label('{}/{}'.format(scenes.index(scene) + 1, len(scenes)))

        row = layout.row(align=True)
        ob = context.active_object
        is_visible = ob and ob.is_visible(context.scene)
        if ob:
            icon = 'OUTLINER_OB_' + ob.type
            sub = row.row(align=True)
            sub.active = is_visible
            sub.prop(ob, 'select', text='', icon=icon)
        row.template_ID(context.scene.objects, 'active')
        if (ob and ob.type == 'ARMATURE' and
                ob.mode in {'EDIT', 'POSE'}):
            layers = ob.data.layers
            if ob.mode == 'EDIT':
                bone = ob.data.edit_bones.active
                if bone:
                    is_visible_bone = any(a & b for a, b in
                                          zip(layers, bone.layers))
                    sub = row.row(align=True)
                    sub.active = is_visible_bone
#                    sub.prop(ob.data, 'active_bone_selection', text='',
#                             icon='BONE_DATA')
                    # row.label(text='', icon='BONE_DATA')
                    row.prop(bone, 'name', text='')
            elif ob.mode == 'POSE':
                bone = ob.data.bones.active
                if bone:
                    is_visible_bone = any(a & b for a, b in
                                          zip(layers, bone.layers))
                    sub = row.row(align=True)
                    sub.active = is_visible_bone
#                    sub.prop(ob.data, 'active_bone_selection', text='',
#                             icon='BONE_DATA')
                    row.prop(bone, 'name', text='')
        layout.separator()

        layout.template_running_jobs()

        layout.template_reports_banner()

        row = layout.row(align=True)

        if bpy.app.autoexec_fail is True and bpy.app.autoexec_fail_quiet is False:
            row.label("Auto-run disabled", icon='ERROR')
            if bpy.data.is_saved:
                props = row.operator("wm.revert_mainfile", icon='SCREEN_BACK', text="Reload Trusted")
                props.use_scripts = True

            row.operator("script.autoexec_warn_clear", text="Ignore")

            # include last so text doesn't push buttons out of the header
            row.label(bpy.app.autoexec_fail_message)
            return

        row.operator("wm.splash", text="", icon='BLENDER', emboss=False)
        row.label(text=scene.statistics(), translate=False)

        layout.separator()

        if rd.has_multiple_engines:
            layout.prop(rd, "engine", text='')


class INFO_MT_editor_menus(Menu):
    bl_idname = "INFO_MT_editor_menus"
    bl_label = ""

    def draw(self, context):
        self.draw_menus(self.layout, context)

    @staticmethod
    def draw_menus(layout, context):
        scene = context.scene
        rd = scene.render

        layout.menu("INFO_MT_file", text='', icon='FILESEL')

        if rd.use_game_engine:
            layout.menu("INFO_MT_game", text='', icon='GAME')
        else:
            layout.menu("INFO_MT_render", text='', icon='RENDER_STILL')

        layout.menu("INFO_MT_window", text='', icon='SPLITSCREEN')
        layout.menu("INFO_MT_help", text='', icon='QUESTION')

### File Extras
class RestartBlender(bpy.types.Operator):
	bl_idname = "wm.restart_blender"
	bl_label = "Reboot"
	bl_description = "Blender Restart"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		py = os.path.join(os.path.dirname(__file__), "console_toggle.py")
		filepath = bpy.data.filepath
		if (filepath != ""):
			subprocess.Popen([sys.argv[0], filepath, '-P', py])
		else:
			subprocess.Popen([sys.argv[0],'-P', py])
		bpy.ops.wm.quit_blender()
		return {'FINISHED'}

class RecoverLatestAutoSave(bpy.types.Operator):
	bl_idname = "wm.recover_latest_auto_save"
	bl_label = "Load last AutoSave"
	bl_description = "Load last AutoSave"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		tempPath = context.user_preferences.filepaths.temporary_directory
		lastFile = None
		for fileName in fnmatch.filter(os.listdir(tempPath), "*.blend"):
			path = os.path.join(tempPath, fileName)
			if (lastFile):
				mtime = os.stat(path).st_mtime
				if (lastTime < mtime and fileName != "quit.blend"):
					lastFile = path
					lastTime = mtime
			else:
				lastFile = path
				lastTime = os.stat(path).st_mtime
		bpy.ops.wm.recover_auto_save(filepath=lastFile)
		self.report(type={"INFO"}, message="Load last AutoSave file")
		return {'FINISHED'}

class SaveMainfileUnmassage(bpy.types.Operator):
	bl_idname = "wm.save_mainfile_unmassage"
	bl_label = "Save Without Prompt"
	bl_description = "Save the changes without displaying the confirmation message"
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		if (bpy.data.filepath != ""):
			bpy.ops.wm.save_mainfile()
			self.report(type={"INFO"}, message=bpy.path.basename(bpy.data.filepath)+" Has been saved")
		else:
			self.report(type={"ERROR"}, message="Save File First")
		return {'FINISHED'}

class INFO_MT_file_settings(Menu):
    bl_idname = "INFO_MT_file_settings"
    bl_label = "Settings"

    def draw(self, context):
        layout = self.layout
        layout.operator("screen.userpref_show", text="User Preferences...", icon='PREFERENCES')
 
        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_homefile", icon='SAVE_PREFS')
        layout.operator('wm.save_userpref', icon='SAVE_COPY')
        layout.operator("wm.read_factory_settings", icon='LOAD_FACTORY')

        if any(bpy.utils.app_template_paths()):
            app_template = context.user_preferences.app_template
            if app_template:
                layout.operator(
                    "wm.read_factory_settings",
                    text="Load Factory Template Settings",
                    icon='LOAD_FACTORY',
                ).app_template = app_template
            del app_template

        layout.menu("USERPREF_MT_app_templates", icon='FILE_BLEND')

class INFO_MT_file(Menu):
    bl_label = "File"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.read_homefile", text="New", icon='NEW')
        layout.operator("wm.open_mainfile", text="Open...", icon='FILE_FOLDER')
        layout.menu("INFO_MT_file_open_recent", icon='OPEN_RECENT')
        layout.operator("wm.revert_mainfile", icon='FILE_REFRESH')
        layout.operator("wm.recover_last_session", icon='RECOVER_LAST')
        layout.operator("wm.recover_auto_save", text="Recover Auto Save...", icon='RECOVER_AUTO')
        layout.operator(RecoverLatestAutoSave.bl_idname, icon="RECOVER_AUTO")
        layout.separator()

        layout.operator_context = 'EXEC_AREA' if context.blend_data.is_saved else 'INVOKE_AREA'
        layout.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
        layout.operator(SaveMainfileUnmassage.bl_idname, icon="FILE_TICK")

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save As...", icon='SAVE_AS')
        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save Copy...", icon='SAVE_COPY').copy = True

        layout.separator()

        layout.menu("INFO_MT_file_settings", icon='OPEN_RECENT')

        layout.separator()

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.link", text="Link", icon='LINK_BLEND')
        layout.operator("wm.append", text="Append", icon='APPEND_BLEND')
        layout.menu("INFO_MT_file_external_data", icon='EXTERNAL_DATA')
        layout.menu("INFO_MT_file_previews")

        layout.separator()

        layout.menu("INFO_MT_file_import", icon='IMPORT')
        layout.menu("INFO_MT_file_export", icon='EXPORT')

        layout.separator()

        layout.operator(RestartBlender.bl_idname, icon="COLOR_GREEN")
        layout.separator()

        layout.operator_context = 'EXEC_AREA'
        if bpy.data.is_dirty and context.user_preferences.view.use_quit_dialog:
            layout.operator_context = 'INVOKE_SCREEN'  # quit dialog
        layout.operator("wm.quit_blender", text="Quit", icon='QUIT')


class INFO_MT_file_import(Menu):
    bl_idname = "INFO_MT_file_import"
    bl_label = "Import"

    def draw(self, context):
        if bpy.app.build_options.collada:
            self.layout.operator("wm.collada_import", text="Collada (Default) (.dae)")
        if bpy.app.build_options.alembic:
            self.layout.operator("wm.alembic_import", text="Alembic (.abc)")


class INFO_MT_file_export(Menu):
    bl_idname = "INFO_MT_file_export"
    bl_label = "Export"

    def draw(self, context):
        if bpy.app.build_options.collada:
            self.layout.operator("wm.collada_export", text="Collada (Default) (.dae)")
        if bpy.app.build_options.alembic:
            self.layout.operator("wm.alembic_export", text="Alembic (.abc)")


class INFO_MT_file_external_data(Menu):
    bl_label = "External Data"

    def draw(self, context):
        layout = self.layout

        icon = 'CHECKBOX_HLT' if bpy.data.use_autopack else 'CHECKBOX_DEHLT'
        layout.operator("file.autopack_toggle", icon=icon)

        layout.separator()

        pack_all = layout.row()
        pack_all.operator("file.pack_all")
        pack_all.active = not bpy.data.use_autopack

        unpack_all = layout.row()
        unpack_all.operator("file.unpack_all")
        unpack_all.active = not bpy.data.use_autopack

        layout.separator()

        layout.operator("file.make_paths_relative")
        layout.operator("file.make_paths_absolute")
        layout.operator("file.report_missing_files")
        layout.operator("file.find_missing_files")


class INFO_MT_file_previews(Menu):
    bl_label = "Data Previews"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.previews_ensure")
        layout.operator("wm.previews_batch_generate")

        layout.separator()

        layout.operator("wm.previews_clear")
        layout.operator("wm.previews_batch_clear")


class INFO_MT_game(Menu):
    bl_label = "Game"

    def draw(self, context):
        layout = self.layout

        gs = context.scene.game_settings

        layout.operator("view3d.game_start")

        layout.separator()

        layout.prop(gs, "show_debug_properties")
        layout.prop(gs, "show_framerate_profile")
        layout.prop(gs, "show_physics_visualization")
        layout.prop(gs, "use_deprecation_warnings")
        layout.prop(gs, "use_animation_record")
        layout.separator()
        layout.prop(gs, "use_auto_start")


class INFO_MT_render(Menu):
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout

        layout.operator("render.render", text="Render Image", icon='RENDER_STILL').use_viewport = True
        props = layout.operator("render.render", text="Render Animation", icon='RENDER_ANIMATION')
        props.animation = True
        props.use_viewport = True

        layout.separator()

        layout.operator("render.opengl", text="OpenGL Render Image")
        layout.operator("render.opengl", text="OpenGL Render Animation").animation = True
        layout.menu("INFO_MT_opengl_render")

        layout.separator()

        layout.operator("render.view_show")
        layout.operator("render.play_rendered_anim", icon='PLAY')


class INFO_MT_opengl_render(Menu):
    bl_label = "OpenGL Render Options"

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        layout.prop(rd, "use_antialiasing")
        layout.prop(rd, "use_full_sample")

        layout.prop_menu_enum(rd, "antialiasing_samples")
        layout.prop_menu_enum(rd, "alpha_mode")


class INFO_MT_window(Menu):
    bl_label = "Window"

    def draw(self, context):
        import sys

        layout = self.layout

        layout.operator("wm.window_duplicate")
        layout.operator("wm.window_fullscreen_toggle", icon='FULLSCREEN_ENTER')

        layout.separator()

        layout.operator("screen.screenshot")
        layout.operator("screen.screencast")

        if sys.platform[:3] == "win":
            layout.separator()
            layout.operator("wm.console_toggle", icon='CONSOLE')

        if context.scene.render.use_multiview:
            layout.separator()
            layout.operator("wm.set_stereo_3d", icon='CAMERA_STEREO')


class INFO_MT_help(Menu):
    bl_label = "Help"

    def draw(self, context):
        layout = self.layout

        layout.operator(
                "wm.url_open", text="Manual", icon='HELP',
                ).url = "https://docs.blender.org/manual/en/dev/"
        layout.operator(
                "wm.url_open", text="Release Log", icon='URL',
                ).url = "http://wiki.blender.org/index.php/Dev:Ref/Release_Notes/%d.%d" % bpy.app.version[:2]
        layout.separator()

        layout.operator(
                "wm.url_open", text="Blender Website", icon='URL',
                ).url = "https://www.blender.org"
        layout.operator(
                "wm.url_open", text="Blender Store", icon='URL',
                ).url = "https://store.blender.org"
        layout.operator(
                "wm.url_open", text="Developer Community", icon='URL',
                ).url = "https://www.blender.org/get-involved/"
        layout.operator(
                "wm.url_open", text="User Community", icon='URL',
                ).url = "https://www.blender.org/support/user-community"
        layout.separator()
        layout.operator(
                "wm.url_open", text="Report a Bug", icon='URL',
                ).url = "https://developer.blender.org/maniphest/task/edit/form/1"
        layout.separator()


        layout.operator("wm.operator_cheat_sheet", icon='TEXT')
        layout.operator("wm.sysinfo", icon='TEXT')
        layout.separator()

        layout.operator("wm.splash", icon='BLENDER')


classes = (
    INFO_HT_header,
    INFO_MT_editor_menus,
    INFO_MT_file,
    INFO_MT_file_import,
    INFO_MT_file_export,
    INFO_MT_file_external_data,
    INFO_MT_file_previews,
    INFO_MT_game,
    INFO_MT_render,
    INFO_MT_opengl_render,
    INFO_MT_window,
    INFO_MT_help,
    RestartBlender,
    RecoverLatestAutoSave,
    SaveMainfileUnmassage,
    INFO_MT_file_settings,
)

if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
