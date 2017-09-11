bl_info = {
    "name": "UserPrefsBaseline",
    "description": "Save and load named sets of preferences.",
    "author": "dustractor@gmail.com",
    "version": (1, 3),
    "blender": (2, 65, 0),
    "location": "UserPreferences View > This Location",
    "warning": "",
    "wiki_url": "",
    "category": "System"}

import bpy
import json
import os
import sys
import subprocess
import datetime

from . import baseline_lib_funcs


class BPREFS_OT_baseline_calibrate(bpy.types.Operator):
    bl_idname = "baseline.create_baseline_file"
    bl_label = "Create Baseline File"
    bl_description = "Represents prefs at default state. Calculate this data per each updated version of blender."
    bl_options = {"INTERNAL"}

    def execute(self, context):
        run_script = os.path.join(os.path.dirname(__file__), "as_run.py")
        p = subprocess.Popen([bpy.app.binary_path, "-b", "--factory-startup", "-P", run_script], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        a, b = p.communicate()
        a = a.decode()
        ok = a.count("SENTINEL_TOKEN")
        if not ok:
            self.report({"ERROR"}, "An error occured. See console.")
            print(b.decode())
            return {"CANCELLED"}
        context.area.tag_redraw()
        return {"FINISHED"}


class BPREFS_OT_preview_config(bpy.types.Operator):
    bl_idname = "baseline.preview_configuration"
    bl_label = "preview_configuration"
    bl_options = {"INTERNAL"}
    configuration = bpy.props.StringProperty(default="")
    display = bpy.props.StringProperty(default="")

    def draw(self, context):
        layout = self.layout
        for ln in json.loads(self.display):
            label = ln.lstrip().rstrip()
            if len(label) > 1:
                layout.label(label, icon="FILE_TICK")

    def invoke(self, context, event):
        if not self.configuration:
            return {"CANCELLED"}

        cfile = os.path.join(baseline_lib_funcs.baseline_data_storage, self.configuration)
        if not os.path.isfile(cfile):
            return {"CANCELLED"}
        self.display = json.dumps(list(filter(lambda ln: ln.lstrip().startswith("#"), open(cfile, 'r').readlines())))
        context.window_manager.invoke_props_dialog(self, width=800, height=1000)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        print("self.configuration:", self.configuration)

        return {"FINISHED"}


class BPREFS_OT_baseline_set(bpy.types.Operator):
    bl_idname = "baseline.create_configuration_file"
    bl_label = "Output Current Configuration"
    bl_description = "Write changed preferences to file."
    bl_options = {"INTERNAL"}
    name = bpy.props.StringProperty(default="mybaseline")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        Z = baseline_lib_funcs.propdict(context.user_preferences)
        A = json.loads(open(baseline_lib_funcs.baseline_file, "r").read())
        commands = ""
        comments = ""
        commentline = "# %s changed from %s to %s.\n".__mod__
        commandline = "    bpy.context.user_preferences.%s = %s\n".__mod__
        A_addons = set(A['addons'])
        Z_addons = set(Z['addons'])
        addons = Z_addons - A_addons
        del A['addons']
        del Z['addons']
        fname = os.path.join(baseline_lib_funcs.baseline_data_storage, self.name + ".py")
        kcf = os.path.join(baseline_lib_funcs.baseline_keys_storage, self.name + "_keys.py")
        bpy.ops.wm.keyconfig_export(filepath=kcf)

        for k in A:
            before, after = A[k], Z[k]
            if before != after:
                comments += commentline((k, before, after))
                commands += commandline((k, after))
        comments += "\n"
        flines = "\n".join([
            '# File created on %s and labeled %s.' % (datetime.datetime.now().ctime(), self.name),
            'import bpy',
            'import os',
            comments,
            'def register():',
            commands,
            '    addons = %s' % repr(addons),
            "\n".join(['    #[Addon %s enabled.]' % adnm for adnm in addons]),
            '    try:',
            '        list(map(lambda _:bpy.ops.wm.addon_enable(module=_),filter(lambda _:_ not in bpy.context.user_preferences.addons,addons)))',
            '    except:',
            '        pass',
            '    kcf = "%s"' % kcf,
            '    and_sigh_the_keys = bpy.context.user_preferences.addons["%s"].preferences.and_the_keys' % __package__,
            '    if os.path.isfile(kcf) and and_sigh_the_keys:',
            '        bpy.ops.wm.keyconfig_import(filepath=kcf,keep_original=False)'
        ])
        with open(fname, 'w') as outputfile:
            outputfile.write(flines)
        if sys.platform == "darwin":
            os.system("open --reveal '%s'" % fname)
        context.area.tag_redraw()
        return {"FINISHED"}


class BPREFS_OT_baseline_load(bpy.types.Operator):
    bl_idname = "baseline.load_configuration"
    bl_label = "Load Configuration File"
    bl_options = {"INTERNAL"}
    configuration = bpy.props.StringProperty(default="")

    def execute(self, context):
        cfile = os.path.join(baseline_lib_funcs.baseline_data_storage, self.configuration)
        if not os.path.isfile(cfile):
            return {"CANCELLED"}
        cname = self.configuration.rpartition(".")[0]
        syspath = sys.path.copy()
        sys.path.append(baseline_lib_funcs.baseline_data_storage)
        modl = __import__(cname)
        modl.register()
        sys.path = syspath
        return {"FINISHED"}


class UserPrefsBaselineAddon(bpy.types.AddonPreferences):
    bl_idname = __package__
    prop = bpy.props.StringProperty(default="prop")
    and_the_keys = bpy.props.BoolProperty(default=False)  # and it will stay that way...

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        if not os.path.isfile(baseline_lib_funcs.baseline_file):
            box.label("A %s baseline file has not been created yet." % (str(bpy.app.version)))
            box.operator("baseline.create_baseline_file")
        else:
            box.label("Baseline file for %s located at:" % str(bpy.app.version))
            box.label(baseline_lib_funcs.baseline_file)
            box.operator("baseline.create_baseline_file", text="Recalibrate baseline")
        layout.separator()
        box = layout.box()
        for cf in os.listdir(baseline_lib_funcs.baseline_data_storage):
            if not cf.endswith(".py"):
                continue
            row = box.row()
            row.label(cf)
            row.operator('baseline.preview_configuration').configuration = cf
            row.operator('baseline.load_configuration', text="Load %s" % cf.rpartition(".")[0]).configuration = cf
        layout.operator("baseline.create_configuration_file")
        layout.separator()
        layout.prop(self, 'and_the_keys')
        layout.label("Check this if you also want to load the associated hotkeys.")


class BPREFS_MT_menu(bpy.types.Menu):
    bl_idname = "BPREFS_MT_menu"
    bl_label = "Baseline:Configs"

    def draw(self, context):
        layout = self.layout
        layout.label("Load:", icon="PLUGIN")
        for cf in filter(lambda _: _.endswith(".py"), os.listdir(baseline_lib_funcs.baseline_data_storage)):
            layout.operator('baseline.load_configuration', text="Load %s" % cf.rpartition(".")[0]).configuration = cf
        layout.separator()
        layout.label("Preview:", icon="QUESTION")
        for cf in filter(lambda _: _.endswith(".py"), os.listdir(baseline_lib_funcs.baseline_data_storage)):
            layout.operator('baseline.preview_configuration', text="Preview %s" % cf.rpartition(".")[0]).configuration = cf


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file.append(lambda *_: _[0].layout.menu('BPREFS_MT_menu'))


def unregister():
    bpy.utils.unregister_module(__name__)
