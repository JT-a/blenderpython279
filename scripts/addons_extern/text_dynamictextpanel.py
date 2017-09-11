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

'''
    Add-on : Dynamic Text
        Par : Double Z.

    Description :
        Cet add-on permet le changement du contenu d'un objet Text 3D en fonction du temps.
        Par la suite, des éléments tel que le baking (pour permettre le linkage sur d'autres projets), les transitions et l'import de fichiers *.srt ont été rajoutés.

    Remerciements :
        Dono pour l'idée des transitions
        Boby pour l'idée du baking du texte.
        e5dy/edddy pour m'avoir averti sur les potentiels bugs du a l'utilisation des bpy.ops au sein d'un script ainsi qu'a l'explication d'un début de solution très utile pour contourner cela.
        Le forum du Blenderclan pour être un bon forum Francophone sur Blender.
'''

bl_info = {
    'name': "Dynamic Text",
    'author': "DoubleZ",
    'version': (0, 7, 0),
    'blender': (2, 7, 0),
    'api': 60991,
    'location': "",
    'warning': "Now beta ?",
    'description': "",
    'wiki_url': "",
    'category': "Text Editor"}

import bpy
from bpy_extras.io_utils import ImportHelper

# Fonction appelé pour mettre à jour l'affichage du text 3D
# en fonction des paramètres de l'utilisateur


def updateTexts(self):
    current = bpy.context.scene.frame_current

    for obj in bpy.data.objects:
        if obj.type == "FONT" and obj.dynamicSettings.update_blocs:
            inTimeline = False
            for ind, bloc in enumerate(sorted(obj.dynamicBlocs, key=lambda db: db.frameStart)):
                nextPos = sorted(obj.dynamicBlocs, key=lambda db: db.frameStart)[ind + 1].frameStart if ind < len(obj.dynamicBlocs) - 1 else bpy.context.scene.frame_end + 1000
                if current >= bloc.frameStart and current < nextPos:
                    inTimeline = True
                    obj.dynamicSettings.lastBlocUsed = ind
                    finale = bloc.body
                    for ind, custom in enumerate(obj.dynamicCustom):
                        if custom.typeBloc == "FLOAT":
                            nbrStr = str(round(custom.number, custom.afterPoint)) if custom.afterPoint else str(int(custom.number))
                            finale = finale.replace("%" + str(ind), nbrStr)
                        if custom.typeBloc == "TIMER":
                            showTime = custom.number
                            if showTime < 0:
                                showTime *= -1
                                final = "-"
                            else:
                                final = ""

                            day = int(showTime / 216000)
                            hour = int(showTime / 3600) % 24
                            min = int(showTime / 60) % 60
                            sec = int(showTime) % 60

                            if custom.typeTimer == "SS":
                                final += str(sec).zfill(2)
                            if custom.typeTimer == "MM_SS":
                                final += str(min).zfill(2) + ":" + str(sec).zfill(2)
                            if custom.typeTimer == "HH_MM_SS":
                                final += str(hour).zfill(2) + ":" + str(min).zfill(2) + ":" + str(sec).zfill(2)
                            if custom.typeTimer == "DDD_HH_MM_SS":
                                final += str(day).zfill(3) + ":" + str(hour).zfill(2) + ":" + str(min).zfill(2) + ":" + str(sec).zfill(2)

                            virg = abs(custom.number - int(custom.number))
                            if custom.typeMs == "_M":
                                final += "." + str(int(virg * 10))
                            if custom.typeMs == "_MM":
                                final += "." + str(int(virg * 100)).zfill(2)
                            if custom.typeMs == "_MMM":
                                final += "." + str(int(virg * 1000)).zfill(3)
                            if custom.typeMs == "_MMMM":
                                final += "." + str(int(virg * 10000)).zfill(4)
                            finale = finale.replace("%" + str(ind), final)
                    obj.data.body = finale
                    break

            if not inTimeline and len(obj.dynamicBlocs):
                obj.data.body = ""

            if len(obj.material_slots):
                if obj.material_slots[0].material:
                    if obj.material_slots[0].material.use_transparency:
                        alphaIn = (current - obj.dynamicBlocs[obj.dynamicSettings.lastBlocUsed].frameStart + 1) / float(obj.dynamicSettings.fadeStart)
                        alphaOut = (nextPos - current) / float(obj.dynamicSettings.fadeEnd)
                        obj.material_slots[0].material.alpha = alphaIn if alphaIn < alphaOut else alphaOut

    bpy.context.scene.update()


def callUt(self, context):  # utilisée de manière ponctuelle
    updateTexts(self)

# Fonction convertissant du timecode d'un fichier srt en frame correspondante


def getFrame(time, state):
    temps = time.split(" ")
    fps = bpy.context.scene.render.fps

    if state == "debut":
        pos = 0
    elif state == "fin":
        pos = 2
    else:
        pos = 0

    hour = int(temps[pos].split(":")[0])
    minute = int(temps[pos].split(":")[1])
    seconde = int(temps[pos].split(":")[2].split(",")[0])
    frame = int(temps[pos].split(":")[2].split(",")[1])

    return hour * 3600 * fps + minute * 60 * fps + seconde * fps + int(frame / (1000 / fps))

# Paramètres données pour le text 3D pour une périodé donné


class DynamicTextBlocs(bpy.types.PropertyGroup):
    # Tous
    bloc_items = [
        ("TEXT", "Text", "", 1),
        ("NUMBER", "Number", "", 2),
        ("TIMER", "Timer", "", 3)]
    frameStart = bpy.props.IntProperty(default=1, min=1, update=callUt)
    frameEnd = bpy.props.IntProperty(default=1, min=1, update=callUt)
    body = bpy.props.StringProperty(default="", update=callUt)

# Paramètres appliqué a l'ensemble des blocs


class DynamicTextSettings(bpy.types.PropertyGroup):
    fadeStart = bpy.props.IntProperty(default=1, min=1)
    fadeEnd = bpy.props.IntProperty(default=1, min=1)
    lastBlocUsed = bpy.props.IntProperty(default=-1)
    update_blocs = bpy.props.BoolProperty(default=False, update=callUt)


class DynamicTextCustomisableValue(bpy.types.PropertyGroup):
    bloc_items = [
        ("FLOAT", "Float", "", 1),
        ("TIMER", "Timer", "", 2)]
    typeBloc = bpy.props.EnumProperty(items=bloc_items, update=callUt)

    # Type Float
    number = bpy.props.FloatProperty(default=0, update=callUt)
    afterPoint = bpy.props.IntProperty(default=1, min=0, max=10, update=callUt)

    # Type Timer (share the "number" value)
    timer_items = [
        ("SS", "ss", "", 1),
        ("MM_SS", "mm:ss", "", 2),
        ("HH_MM_SS", "hh:mm:ss", "", 3),
        ("DDD_HH_MM_SS", "ddd:hh:mm:ss", "", 4)]
    ms_items = [
        ("NONE", "None", "", 1),
        ("_M", ".m", "", 2),
        ("_MM", ".mm", "", 3),
        ("_MMM", ".mmm", "", 4),
        ("_MMMM", ".mmmm", "", 5)]
    typeTimer = bpy.props.EnumProperty(items=timer_items, default="HH_MM_SS", update=callUt)
    typeMs = bpy.props.EnumProperty(items=ms_items, update=callUt)

bpy.utils.register_class(DynamicTextBlocs)
bpy.utils.register_class(DynamicTextSettings)
bpy.utils.register_class(DynamicTextCustomisableValue)
bpy.types.Object.dynamicBlocs = bpy.props.CollectionProperty(type=DynamicTextBlocs)
bpy.types.Object.dynamicSettings = bpy.props.PointerProperty(type=DynamicTextSettings)
bpy.types.Object.dynamicCustom = bpy.props.CollectionProperty(type=DynamicTextCustomisableValue)

# Panel contenant les propriétés modifiables


class DynamicTextPanel(bpy.types.Panel):
    bl_label = "Dynamic Text Panel"
    bl_idname = "TEXT_PT_DYNAMIC_TEXT"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return True if context.object.type == "FONT" else False

    def draw_header(self, context):
        layout = self.layout
        ds = context.object.dynamicSettings

        layout.prop(ds, "update_blocs", text="")

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=False)
        obj = context.object

        col.operator("dynamictext.bake_blocs", "Bake bloc(s)")

        tog = col.column(align=True)
        tog.operator("dynamictext.add_bloc", "Add to timeline", icon="ZOOMIN")
        tog.operator("dynamictext.add_custom", "Add Custom", icon="ZOOMIN")
        tog.scale_y = 1.3

        col.label("Fade(s) length:")
        row = layout.row(align=True)
        row.prop(obj.dynamicSettings, "fadeStart", text="In")
        row.prop(obj.dynamicSettings, "fadeEnd", text="Out")

        if obj.dynamicSettings.fadeStart > 1 or obj.dynamicSettings.fadeEnd > 1:
            if len(obj.material_slots):
                if not obj.material_slots[0].material:
                    layout.label("Material needed", icon="ERROR")
                else:
                    if not obj.material_slots[0].material.use_transparency:
                        layout.label("Material transparency needed", icon="ERROR")
            else:
                layout.label("Material needed", icon="ERROR")

        box = layout.box()
        for ind, bloc in enumerate(obj.dynamicCustom):
            col = box.column()
            row = col.row()
            row.prop(bloc, "typeBloc", text="%" + str(ind))
            row.prop(bloc, "number", text="")
            row.operator("dynamictext.remove_custom", text="", icon="X", emboss=False).index = ind
            if bloc.typeBloc == "FLOAT":
                col.prop(bloc, "afterPoint", text="After Points")
            if bloc.typeBloc == "TIMER":
                col.prop(bloc, "typeTimer", text="Display")
                col.prop(bloc, "typeMs", text="Precision")

        for ind, bloc in enumerate(sorted(obj.dynamicBlocs, key=lambda db: db.frameStart)):
            box = layout.box()
            col = box.column()
            row = col.row()
            row.prop(bloc, "frameStart", text="Start")
            row.operator("dynamictext.remove_bloc", text="", icon="X", emboss=False).index = ind
            row = col.row(align=True)
            sub = row.row()
            sub.scale_x = 3
            sub.prop(bloc, "body", text="")
            row.operator("dynamictext.set_text", text="set").index = ind

# Ajoute une nouvelle variable customisable


class AddCustom(bpy.types.Operator):
    bl_idname = "dynamictext.add_custom"
    bl_label = "Dynamic text : Add customisable variable"

    @classmethod
    def poll(cls, context):
        return True if bpy.context.object.type == "FONT" else False

    def execute(self, context):
        bpy.context.object.dynamicCustom.add()
        return {"FINISHED"}

# Ajoute une nouvelle variable customisable


class RemoveCustom(bpy.types.Operator):
    bl_idname = "dynamictext.remove_custom"
    bl_label = "Dynamic text : Remove customisable variable"

    index = bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return True if bpy.context.object.type == "FONT" else False

    def execute(self, context):
        bpy.context.object.dynamicCustom.remove(self.index)
        return {"FINISHED"}

# Ajoute un nouveau bloc avec les paramètres par défaut selon la frame en cours et le texte affiché sur le texte 3D


class AddBloc(bpy.types.Operator):
    bl_idname = "dynamictext.add_bloc"
    bl_label = "Dynamic text : Add new text bloc"

    @classmethod
    def poll(cls, context):
        return True if bpy.context.object.type == "FONT" else False

    def execute(self, context):
        bloc = bpy.context.object.dynamicBlocs.add()
        bloc.body = bpy.context.object.data.body
        bloc.frameStart = bpy.context.scene.frame_current
        bloc.frameEnd = bpy.context.scene.frame_current + 100
        return {'FINISHED'}

# Supprime le bloc


class RemoveBloc(bpy.types.Operator):
    bl_idname = "dynamictext.remove_bloc"
    bl_label = "Dynamic text : Remove bloc"

    index = bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return True if bpy.context.object.type == "FONT" else False

    def execute(self, context):
        context.object.dynamicBlocs.remove(self.index)
        return {'FINISHED'}

# Remplace le texte du bloc en cours par ce qui est affiché sur la vue 3D


class SetText(bpy.types.Operator):
    bl_idname = "dynamictext.set_text"
    bl_label = "Dynamic text : Set Text"

    index = bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return True if bpy.context.object.type == "FONT" else False

    def execute(self, context):
        context.object.dynamicBlocs[self.index].body = context.object.data.body
        return {'FINISHED'}

# Converti le texte dynamique en plusieurs textes non dynamique
# Utile pour linker les élements sur d'autre projet et personnaliser plus en détail le texte


class BakeBlocs(bpy.types.Operator):
    bl_idname = "dynamictext.bake_blocs"
    bl_label = "Dynamic text : Bake blocs"

    @classmethod
    def poll(cls, context):
        return True if context.object.type == "FONT" else False

    def execute(self, context):
        original = context.object
        originalSettings = context.object.dynamicSettings
        originalBlocs = context.object.dynamicBlocs

        for ind, bloc in enumerate(originalBlocs):
            if bloc.body != "":
                nextPos = sorted(originalBlocs, key=lambda db: db.frameStart)[ind + 1].frameStart if ind < len(originalBlocs) - 1 else bpy.context.scene.frame_end + 1000

                textData = bpy.context.object.data.copy()
                objText = bpy.data.objects.new(original.name, textData)
                bpy.context.scene.objects.link(objText)

                objText.data.body = bloc.body

                objText.hide = True
                objText.keyframe_insert(data_path="hide", index=-1, frame=0)
                objText.keyframe_insert(data_path="hide", index=-1, frame=nextPos)
                objText.hide = False
                objText.keyframe_insert(data_path="hide", index=-1, frame=bloc.frameStart)

                objText.hide_render = True
                objText.keyframe_insert(data_path="hide_render", index=-1, frame=0)
                objText.keyframe_insert(data_path="hide_render", index=-1, frame=nextPos)
                objText.hide_render = False
                objText.keyframe_insert(data_path="hide_render", index=-1, frame=bloc.frameStart)

                if len(objText.material_slots):
                    if objText.material_slots[0].material:
                        mat = objText.material_slots[0].material
                        mat.alpha = 0.0
                        mat.keyframe_insert(data_path="alpha", index=-1, frame=bloc.frameStart - 1)
                        mat.keyframe_insert(data_path="alpha", index=-1, frame=nextPos)
                        mat.alpha = 1.0
                        mat.keyframe_insert(data_path="alpha", index=-1, frame=bloc.frameStart - 1 + originalSettings.fadeStart)
                        mat.keyframe_insert(data_path="alpha", index=-1, frame=nextPos - originalSettings.fadeEnd)
        return{'FINISHED'}

# Fonctions utiles pour Blender


def register():
    bpy.utils.register_class(DynamicTextPanel)
    bpy.utils.register_class(AddBloc)
    bpy.utils.register_class(AddCustom)
    bpy.utils.register_class(RemoveBloc)
    bpy.utils.register_class(RemoveCustom)
    bpy.utils.register_class(SetText)
    bpy.utils.register_class(BakeBlocs)

    bpy.app.handlers.frame_change_post.append(updateTexts)
    bpy.app.handlers.render_pre.append(updateTexts)


def unregister():
    bpy.utils.unregister_class(DynamicTextPanel)
    bpy.utils.unregister_class(AddBloc)
    bpy.utils.unregister_class(AddCustom)
    bpy.utils.unregister_class(RemoveBloc)
    bpy.utils.unregister_class(RemoveCustom)
    bpy.utils.unregister_class(SetText)
    bpy.utils.unregister_class(BakeBlocs)

    bpy.app.handlers.frame_change_post.remove(updateTexts)
    bpy.app.handlers.render_pre.remove(updateTexts)


if __name__ == "__main__":
    register()
