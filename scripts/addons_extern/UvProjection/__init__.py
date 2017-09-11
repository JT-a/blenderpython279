# License:
''' Copyright (c) 2012 Jorge Hernandez - Melendez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
bl_info = {
    "name": "Automatic UVProjection",
    "description": "Quickly and easy create projects of Camera Mapping",
    "author": "Jorge Hernandez - Melenedez",
    "version": (2, 0),
    "blender": (2, 71, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "UV"}

if "bpy" in locals():
    import imp
    imp.reload(vistas)
    imp.reload(unwrap)
    imp.reload(uvmod)
    imp.reload(material)
    imp.reload(proyector)
    imp.reload(tipocoordenadas)
    imp.reload(update)
else:
    from . import vistas
    from . import unwrap
    from . import uvmod
    from . import material
    from . import proyector
    from . import tipocoordenadas
    from . import update

import bpy
from bpy.props import *


u = unwrap.Unwrap()
v = vistas.Vistas()
um = uvmod.Uvmod()
m = material.Material()
p = proyector.Proyector()
tc = tipocoordenadas.Tipocoordenadas()
up = update.Update()


def mySceneProperties():
    # para el listado de objetos esto es necesario:
    # son como propiedades para el item de interfaz:
    bpy.types.Object.Proyector = bpy.props.StringProperty()
    bpy.types.Scene.IBPath = bpy.props.StringProperty(name="", attr="custompath", description="Base Image Path", maxlen=1024, default="")

    # smoothable #########################################################################################:
    bpy.types.Scene.Levelv = bpy.props.IntProperty(name="Level View", default=1, min=0, max=6)
    bpy.types.Scene.Levelr = bpy.props.IntProperty(name="Level Render", default=1, min=0, max=6)
    bpy.types.Scene.ODisplay = bpy.props.BoolProperty(name="Optimal Display", description="Active optimal display", default=True)
    bpy.types.Scene.Soften = bpy.props.BoolProperty(name="Soften normals", description="Active smooth shade (per selection objects manageables)", default=False)
    bpy.types.Scene.Typealg = bpy.props.BoolProperty(name="Simple", description="Subdivision Algorithm Simple", default=True)
    bpy.types.Scene.shadelessmode = bpy.props.BoolProperty(name="Shadeless Mode", description="Active Shadeless (for selected objects or all)", default=True)
    bpy.types.Scene.MatSpecular = bpy.props.FloatProperty(name="Specular", description="Specular value (for selected objects or all)", default=0)
    # fin smoothable ######################################################################################

mySceneProperties()

# intento de hacer un boton de reload addon (pero no tiene mucho sentido crear este boton)
# def restart_addon():
#    bpy.ops.wm.addon_disable(module='UVProjection')
#    bpy.ops.wm.addon_enable(module='UVProjection')

# Menu in toolprops region


class Botones_UVProjection(bpy.types.Panel):
    bl_label = "Automatic UVProjection"
    bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOL_PROPS"
    bl_region_type = "TOOLS"
    bl_category = "UVP"

    def draw(self, context):
        layout = self.layout
        #layout.label("hola mundo")
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
        scn = context.scene

        # el comodin contiene la imagen actual del loader.
        if not 'comodin' in bpy.data.textures:
            comodin = bpy.data.textures.new(type='IMAGE', name='comodin')

        # intento de hacer un boton de reload addon (pero no tiene mucho sentido crear este boton)
        #col.operator("restarta.restarta", text='Reload Addon')

        # col.operator("object.custom_path")
        # col.prop(context.scene,"IBPath")

        col.label("Load Images:")

        # Al crear una nueva escena con ctrl + n el addon no se recargaba y el comodin no se volvia a crear, de esta manera si no esta se crea:
        try:
            # primero intento de manera normal:
            comodin = bpy.data.textures[0]
            col.template_image(comodin, "image", comodin.image_user)

        except:
            # si da error seguramente es una escena nueva por lo tanto lo creo otra vez:
            if bpy.data.textures[0].name != 'comodin':
                comodin = bpy.data.textures.new(type='IMAGE', name='comodin')

            comodin = bpy.data.textures[0]
            col.template_image(comodin, "image", comodin.image_user)

        ''' # Esto lo dejo para futuras versiones  :)
        # listado de objetos en desplegable: en concreto del objeto activo:
        #col.prop(context.scene.objects, "active", text="Proyector? :")
        
        # listado de objetos en la escena:
        # el string Proyector llama una parte creada arriba
        # donde el string cameras puede ir meshes dependiendo de lo que quisieramos :)
        col.prop_search(context.object, "Proyector", bpy.data, "cameras")
        # para obtener el valor de el item actual de el listado de objetos de la escena:
        # lo podemos sacar de: bpy.context.object.Proyector

        # para cambiar el nombre real de la camara:
        # bpy.data.cameras['Camera.001'].name = "jojo"
        # bpy.context.scene.camera.data.name = "grr"
        '''
        col.label("Apply Projections:")
        subrow0 = col.row(align=True)
        #col.operator("ol.ol", text='(Only) load image to blender')
        subrow0.operator("toselected.toselected", text='To Selected')
        subrow0.operator("mod.mod", text='To ALL')
        #col.operator("unwrapeado.unwrapeado", text='(Only) Auto UnWrap for all')
        col.operator("uprel.uprel", text='Material //-// Render  -  Update')

        col.label("Handlers:")

        # para el modo de coordenadas ########################################:
        #col.label("Handlers Orientations:")
        view = context.space_data
        orientation = view.current_orientation

        row = layout.row(align=True)
        col.prop(view, "transform_orientation", text="")
        #col.operator("transform.create_orientation", text="", icon='ZOOMIN')
        if orientation:
            row = layout.row(align=True)
            col.prop(orientation, "name", text="")
            col.operator("transform.delete_orientation", text="", icon="X")
        # fin modo coordenadas ################################################

        col.label("Objects:")
        # lock unlock:
        subrow1 = col.row(align=True)
        subrow1.operator("lock.lock", text='Lock')
        subrow1.operator("unlock.unlock", text='Unlock')
        # select camera:
        subrow7 = col.row(align=True)
        subrow7.operator("selctcam.selctcam", text='Select projector')
        subrow7.operator("selctloc.selctloc", text='Select locator ')

        # smoothable #############################################################:
        col.label("Smooth Settings:")
        subrow2 = col.row(align=True)
        subrow2.operator("smoothable.smoothable", text='Manageable')
        subrow2.operator("dessmoothable.dessmoothable", text='Unmanageable')

        subrow3 = col.row(align=True)
        subrow3.operator("allsmooth.allsmooth", text='Subsurf')
        subrow3.operator("delsmooth.delsmooth", text='Del Subsurfs')

        col.operator("upsetigs.upsetings", text='Update')
        subrow4 = col.row(align=True)
        subrow4.prop(scn, 'Levelv', toggle=True)
        subrow4.prop(scn, 'Levelr', toggle=True)

        subrow5 = col.row(align=True)
        subrow5.prop(scn, 'Typealg', toggle=True)
        subrow5.prop(scn, 'ODisplay')

        col.operator("stosmooth.stosmooth", text='Subsurfs to Manageable')
        col.operator("selsmoothables.selsmoothables", text='Select All Manageables')
        col.operator("clearsm.clearsm", text='Remove all mngbl & subsrf')

        col.label("Settings Display:")
        col.prop(scn, 'Soften')
        col.prop(scn, 'shadelessmode')

        col.prop(scn, 'MatSpecular')

        # wire:
        subrow6 = col.row(align=True)
        subrow6.operator("setwire.setwire", text='Wire On')
        subrow6.operator("unsetwire.unsetwire", text='Wire Off')

        # fin smoothable ##########################################################

        col.label("Camera/Locator settings:")

        col.operator("updaterot.updaterot", text='Locator  -  Update Orientations')
        col.operator("updaterotcam.updaterotcam", text='Projector  -  Update Orientations')

        col.operator("influencek.influencek", text='locator  -  Connect')
        col.operator("noinfluencek.noinfluencek", text='locator  -  Disconnect')

        #subrow = col.row(align=True)
        #subrow.operator("influence.influence", text='With influence')
        #subrow.operator("noinfluence.noinfluence", text='Without influence')
        #subrow2 = col.row(align=True)
        #subrow2.operator("setinverse.setinverse", text='Set inverse')
        #subrow2.operator("clearinverse.clearinverse", text='Clear inverse')


def imagen():
    #img = bpy.data.images.load(filepath=bpy.context.scene.IBPath)
    img = bpy.data.textures[0].image
    #img.use_premultiply = True
    return img


def getsettings():
    scn = bpy.context.scene
    todo = [int(scn.Levelv), int(scn.Levelr), scn.ODisplay, scn.Soften]
    return todo


def myshade(todo, ob):
    if "smoothable" in ob:
        if todo == True:
            bpy.ops.object.shade_smooth()
        else:
            bpy.ops.object.shade_flat()


def smoothable():
    if bpy.context.selected_objects:
        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                bpy.ops.object.select_all(action='DESELECT')
                scn = bpy.context.scene
                scn.objects.active = ob
                ob.select = True
                bpy.types.Object.smoothable = bpy.props.IntProperty()
                ob.smoothable = 1
                #bpy.context.object["smoothable"] = 1
                todo = getsettings()
                myshade(todo[3], ob)
                bpy.ops.object.select_all(action='DESELECT')
    else:
        scn = bpy.context.scene
        for ob in bpy.data.scenes[scn.name].objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                bpy.ops.object.select_all(action='DESELECT')
                scn = bpy.context.scene
                scn.objects.active = ob
                ob.select = True
                bpy.types.Object.smoothable = bpy.props.IntProperty()
                ob.smoothable = 1
                #bpy.context.object["smoothable"] = 1
                todo = getsettings()
                myshade(todo[3], ob)
                bpy.ops.object.select_all(action='DESELECT')


def dessmoothable():
    if bpy.context.selected_objects:
        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                bpy.ops.object.select_all(action='DESELECT')
                scn = bpy.context.scene
                scn.objects.active = ob
                ob.select = True
                bpy.types.Object.smoothable = bpy.props.IntProperty()
                ob.smoothable = 0
                bpy.ops.wm.properties_remove(data_path="object", property="smoothable")
                bpy.ops.object.select_all(action='DESELECT')
    else:
        scn = bpy.context.scene
        for ob in bpy.data.scenes[scn.name].objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                bpy.ops.object.select_all(action='DESELECT')
                scn = bpy.context.scene
                scn.objects.active = ob
                ob.select = True
                bpy.types.Object.smoothable = bpy.props.IntProperty()
                ob.smoothable = 0
                bpy.ops.wm.properties_remove(data_path="object", property="smoothable")
                bpy.ops.object.select_all(action='DESELECT')


def delmismooth():
    if bpy.context.selected_objects:
        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                bpy.ops.object.select_all(action='DESELECT')
                scn = bpy.context.scene
                scn.objects.active = ob
                ob.select = True
                # if ob.get("smoothable") == 1: # vale tanto get, como .propiedad
                todo = getsettings()

                modificadores = []
                for mod in ob.modifiers:
                    modificadores.append(mod)

                if "smoothable" in ob and ob.smoothable == 1:
                    indice = 0
                    existe = False
                    while (not existe and indice < len(modificadores)):
                        if ob.modifiers[indice].type == 'SUBSURF':
                            existe = True
                            donde = indice
                        else:
                            existe = False
                        indice += 1

                    if existe:
                        nombre = ob.modifiers[donde].name
                        bpy.ops.object.modifier_remove(modifier=nombre)
                        # myshade(todo[3],ob)
                        bpy.ops.object.shade_flat()
                bpy.ops.object.select_all(action='DESELECT')
    else:
        scn = bpy.context.scene
        for ob in bpy.data.scenes[scn.name].objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                bpy.ops.object.select_all(action='DESELECT')
                scn = bpy.context.scene
                scn.objects.active = ob
                ob.select = True
                # if ob.get("smoothable") == 1: # vale tanto get, como .propiedad
                todo = getsettings()

                modificadores = []
                for mod in ob.modifiers:
                    modificadores.append(mod)

                if "smoothable" in ob and ob.smoothable == 1:
                    indice = 0
                    existe = False
                    while (not existe and indice < len(modificadores)):
                        if ob.modifiers[indice].type == 'SUBSURF':
                            existe = True
                            donde = indice
                        else:
                            existe = False
                        indice += 1

                    if existe:
                        nombre = ob.modifiers[donde].name
                        bpy.ops.object.modifier_remove(modifier=nombre)
                        # myshade(todo[3],ob)
                        bpy.ops.object.shade_flat()
                bpy.ops.object.select_all(action='DESELECT')


def mismooth():
    scn = bpy.context.scene
    todo = getsettings()
    if bpy.context.selected_objects:
        for ob in bpy.context.selected_objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                bpy.ops.object.select_all(action='DESELECT')
                scn.objects.active = ob
                ob.select = True

                modificadores = []
                for mod in ob.modifiers:
                    modificadores.append(mod)

                if "smoothable" in ob and ob.smoothable == 1:
                    indice = 0
                    existe = False
                    while (not existe and indice < len(modificadores)):
                        if ob.modifiers[indice].type == 'SUBSURF':
                            existe = True
                            donde = indice
                        else:
                            existe = False
                        indice += 1

                    if not existe:
                        bpy.ops.object.modifier_add(type='SUBSURF')
                        myshade(todo[3], ob)
                        ob.modifiers['Subsurf'].levels = todo[0]
                        ob.modifiers['Subsurf'].render_levels = todo[1]
                        ob.modifiers['Subsurf'].show_only_control_edges = todo[2]
                        if scn.Typealg:
                            ob.modifiers['Subsurf'].subdivision_type = 'SIMPLE'
                        else:
                            ob.modifiers['Subsurf'].subdivision_type = 'CATMULL_CLARK'

                        nombre = 'Subsurf'
                        for i in range(len(modificadores)):
                            bpy.ops.object.modifier_move_up(modifier=nombre)

                    else:
                        myshade(todo[3], ob)
                        ob.modifiers[donde].levels = todo[0]
                        ob.modifiers[donde].render_levels = todo[1]
                        ob.modifiers[donde].show_only_control_edges = todo[2]
                        if scn.Typealg:
                            ob.modifiers[donde].subdivision_type = 'SIMPLE'
                        else:
                            ob.modifiers[donde].subdivision_type = 'CATMULL_CLARK'

                        nombre = 'Subsurf'
                        for i in range(len(modificadores)):
                            bpy.ops.object.modifier_move_up(modifier=nombre)

                bpy.ops.object.select_all(action='DESELECT')
    else:
        scn = bpy.context.scene
        for ob in bpy.data.scenes[scn.name].objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                bpy.ops.object.select_all(action='DESELECT')
                scn.objects.active = ob
                ob.select = True

                modificadores = []
                for mod in ob.modifiers:
                    modificadores.append(mod)

                if "smoothable" in ob and ob.smoothable == 1:
                    indice = 0
                    existe = False
                    while (not existe and indice < len(modificadores)):
                        if ob.modifiers[indice].type == 'SUBSURF':
                            existe = True
                            donde = indice
                        else:
                            existe = False
                        indice += 1

                    if not existe:
                        bpy.ops.object.modifier_add(type='SUBSURF')
                        myshade(todo[3], ob)
                        ob.modifiers['Subsurf'].levels = todo[0]
                        ob.modifiers['Subsurf'].render_levels = todo[1]
                        ob.modifiers['Subsurf'].show_only_control_edges = todo[2]
                        if scn.Typealg:
                            ob.modifiers['Subsurf'].subdivision_type = 'SIMPLE'
                        else:
                            ob.modifiers['Subsurf'].subdivision_type = 'CATMULL_CLARK'

                        nombre = 'Subsurf'
                        for i in range(len(modificadores)):
                            bpy.ops.object.modifier_move_up(modifier=nombre)

                    else:
                        myshade(todo[3], ob)
                        ob.modifiers[donde].levels = todo[0]
                        ob.modifiers[donde].render_levels = todo[1]
                        ob.modifiers[donde].show_only_control_edges = todo[2]
                        if scn.Typealg:
                            ob.modifiers[donde].subdivision_type = 'SIMPLE'
                        else:
                            ob.modifiers[donde].subdivision_type = 'CATMULL_CLARK'

                        nombre = 'Subsurf'
                        for i in range(len(modificadores)):
                            bpy.ops.object.modifier_move_up(modifier=nombre)

                bpy.ops.object.select_all(action='DESELECT')


def updatesmooth():
    scn = bpy.context.scene
    todo = getsettings()

    if bpy.context.selected_objects:
        for ob in bpy.context.selected_objects:
            try:
                bpy.context.selected_objects[0].material_slots[0].material.specular_intensity = scn.MatSpecular
            except:
                pass
            try:
                if scn.shadelessmode:
                    bpy.context.selected_objects[0].material_slots[0].material.use_shadeless = True
                else:
                    bpy.context.selected_objects[0].material_slots[0].material.use_shadeless = False
            except:
                pass

            modificadores = []
            for mod in ob.modifiers:
                modificadores.append(mod)

            if "smoothable" in ob:  # and ob.smoothable == 1:
                indice = 0
                existe = False
                while (not existe and indice < len(modificadores)):
                    if ob.modifiers[indice].type == 'SUBSURF':
                        existe = True
                        donde = indice
                    else:
                        existe = False
                    indice += 1

                if existe:
                    myshade(todo[3], ob)
                    ob.modifiers[donde].levels = todo[0]
                    ob.modifiers[donde].render_levels = todo[1]
                    ob.modifiers[donde].show_only_control_edges = todo[2]
                    if scn.Typealg:
                        ob.modifiers[donde].subdivision_type = 'SIMPLE'
                    else:
                        ob.modifiers[donde].subdivision_type = 'CATMULL_CLARK'

                    nombre = ob.modifiers[donde].name
                    for i in range(len(modificadores)):
                        bpy.ops.object.modifier_move_up(modifier=nombre)

    else:
        scn = bpy.context.scene
        for ob in bpy.data.scenes[scn.name].objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                bpy.ops.object.select_all(action='DESELECT')
                scn.objects.active = ob
                ob.select = True
                try:
                    ob.material_slots[0].material.specular_intensity = scn.MatSpecular
                except:
                    pass
                try:
                    if scn.shadelessmode:
                        ob.material_slots[0].material.use_shadeless = True
                    else:
                        ob.material_slots[0].material.use_shadeless = False
                except:
                    pass

                modificadores = []
                for mod in ob.modifiers:
                    modificadores.append(mod)

                if "smoothable" in ob:  # and ob.smoothable == 1:
                    indice = 0
                    existe = False
                    while (not existe and indice < len(modificadores)):
                        if ob.modifiers[indice].type == 'SUBSURF':
                            existe = True
                            donde = indice
                        else:
                            existe = False
                        indice += 1

                    if existe:
                        myshade(todo[3], ob)
                        ob.modifiers[donde].levels = todo[0]
                        ob.modifiers[donde].render_levels = todo[1]
                        ob.modifiers[donde].show_only_control_edges = todo[2]
                        if scn.Typealg:
                            ob.modifiers[donde].subdivision_type = 'SIMPLE'
                        else:
                            ob.modifiers[donde].subdivision_type = 'CATMULL_CLARK'

                        nombre = ob.modifiers[donde].name
                        for i in range(len(modificadores)):
                            bpy.ops.object.modifier_move_up(modifier=nombre)

            bpy.ops.object.select_all(action='DESELECT')


def importar():
    scn = bpy.context.scene
    todo = getsettings()
    for ob in bpy.data.scenes[scn.name].objects:
        if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
            bpy.ops.object.select_all(action='DESELECT')
            scn.objects.active = ob
            ob.select = True

            modificadores = []
            for mod in ob.modifiers:
                modificadores.append(mod)

            indice = 0
            existe = False
            while (not existe and indice < len(modificadores)):
                if ob.modifiers[indice].type == 'SUBSURF':
                    existe = True
                    donde = indice
                else:
                    existe = False
                indice += 1

            if existe:
                bpy.types.Object.smoothable = bpy.props.IntProperty()
                ob.smoothable = 1

                myshade(todo[3], ob)
                ob.modifiers[donde].levels = todo[0]
                ob.modifiers[donde].render_levels = todo[1]
                ob.modifiers[donde].show_only_control_edges = todo[2]
                if scn.Typealg:
                    ob.modifiers[donde].subdivision_type = 'SIMPLE'
                else:
                    ob.modifiers[donde].subdivision_type = 'CATMULL_CLARK'

                nombre = ob.modifiers[donde].name
                for i in range(len(modificadores)):
                    bpy.ops.object.modifier_move_up(modifier=nombre)

            bpy.ops.object.select_all(action='DESELECT')


def clearsm():
    scn = bpy.context.scene
    for ob in bpy.data.scenes[scn.name].objects:
        if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
            bpy.ops.object.select_all(action='DESELECT')
            scn.objects.active = ob
            ob.select = True
            todo = getsettings()

            modificadores = []
            for mod in ob.modifiers:
                modificadores.append(mod)

            if "smoothable" in ob and ob.smoothable == 1:
                indice = 0
                existe = False
                while (not existe and indice < len(modificadores)):
                    if ob.modifiers[indice].type == 'SUBSURF':
                        existe = True
                        donde = indice
                    else:
                        existe = False
                    indice += 1

                if existe:
                    nombre = ob.modifiers[donde].name
                    bpy.ops.object.modifier_remove(modifier=nombre)

                ob.smoothable = 0
                bpy.ops.object.shade_flat()
                bpy.ops.wm.properties_remove(data_path="object", property="smoothable")
            bpy.ops.object.select_all(action='DESELECT')


class myclearsm(bpy.types.Operator):
    bl_idname = "clearsm.clearsm"
    bl_label = "Remove all smooths/ables"
    bl_description = "Delete all manageable system and subsurfs"

    def execute(self, context):
        clearsm()
        return{'FINISHED'}


class selsmoothables(bpy.types.Operator):
    bl_idname = "selsmoothables.selsmoothables"
    bl_label = "Select All Manageable"
    bl_description = "Select All Objects in manageable system manager"

    def execute(self, context):
        scn = bpy.context.scene
        bpy.ops.object.select_all(action='DESELECT')
        for ob in bpy.data.scenes[scn.name].objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                if 'smoothable' in ob:
                    myobject = bpy.data.objects[str(ob.name)]
                    myobject.select = True
                    scn.objects.active = myobject
        return{'FINISHED'}


class importables(bpy.types.Operator):
    bl_idname = "stosmooth.stosmooth"
    bl_label = "Smooths to Smoothable"
    bl_description = "Import all subsurfs to my manageable system"

    def execute(self, context):
        importar()
        return{'FINISHED'}


class smoothables(bpy.types.Operator):
    bl_idname = "smoothable.smoothable"
    bl_label = "Smoothable"
    bl_description = "Add objects to my manageable system manager (to selected objects or all)"

    def execute(self, context):
        smoothable()
        return{'FINISHED'}


class dessmoothables(bpy.types.Operator):
    bl_idname = "dessmoothable.dessmoothable"
    bl_label = "DesSmoothable"
    bl_description = "Only Remove objects from my manageable system manager, not subsurfs (to selected objects or all)"

    def execute(self, context):
        dessmoothable()
        return{'FINISHED'}


class delsmooth(bpy.types.Operator):
    bl_idname = "delsmooth.delsmooth"
    bl_label = "Del Smooths"
    bl_description = "Remove subsurfs but not out of my manageable system (for selected object or all)"

    def execute(self, context):
        delmismooth()
        return{'FINISHED'}


class smooth(bpy.types.Operator):
    bl_idname = "allsmooth.allsmooth"
    bl_label = "Smooth"
    bl_description = "add Subsurf to manageables objects (for selected objects or all)"

    def execute(self, context):
        mismooth()
        return{'FINISHED'}


class upsettings(bpy.types.Operator):
    bl_idname = "upsetigs.upsetings"
    bl_label = "Update"
    bl_description = "Update all settings for all subsurfs objects (in selected objects or all)"

    def execute(self, context):
        updatesmooth()
        return{'FINISHED'}


class SelectCam(bpy.types.Operator):
    bl_idname = "selctcam.selctcam"
    bl_label = "projector-(camera)  -  Select"
    bl_description = "Easy select Projector-Camera"

    def execute(self, context):
        if "Proyector" in bpy.data.objects:
            try:
                bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
                myprojector = bpy.data.objects["Proyector"]
                myprojector.select = True
                bpy.context.scene.objects.active = myprojector  # lo hago objeto activo
            except:
                pass
        return{'FINISHED'}


class SelectCam(bpy.types.Operator):
    bl_idname = "selctloc.selctloc"
    bl_label = "locator - Select"
    bl_description = "Easy select locator"

    def execute(self, context):
        if "Locator" in bpy.data.objects:
            try:
                bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
                myprojector = bpy.data.objects["Locator"]
                myprojector.select = True
                bpy.context.scene.objects.active = myprojector  # lo hago objeto activo
            except:
                pass
        return{'FINISHED'}


class LockOb(bpy.types.Operator):
    bl_idname = "lock.lock"
    bl_label = "Lock"
    bl_description = "Lock objects (in selected objects or all)"

    def execute(self, context):

        if bpy.context.selected_objects:
            for o in bpy.context.selected_objects:
                for x in range(len(o.lock_location)):
                    o.lock_location[x] = True
                    o.lock_rotation[x] = True
                    o.lock_scale[x] = True
        else:
            for o in bpy.data.objects:
                for x in range(len(o.lock_location)):
                    o.lock_location[x] = True
                    o.lock_rotation[x] = True
                    o.lock_scale[x] = True

        return{'FINISHED'}


class UnLockOb(bpy.types.Operator):
    bl_idname = "unlock.unlock"
    bl_label = "Lock"
    bl_description = "UnLock objects (in selected objects or all)"

    def execute(self, context):

        if bpy.context.selected_objects:
            for o in bpy.context.selected_objects:
                for x in range(len(o.lock_location)):
                    o.lock_location[x] = False
                    o.lock_rotation[x] = False
                    o.lock_scale[x] = False
        else:
            for o in bpy.data.objects:
                for x in range(len(o.lock_location)):
                    o.lock_location[x] = False
                    o.lock_rotation[x] = False
                    o.lock_scale[x] = False

        return{'FINISHED'}


class WireOn(bpy.types.Operator):
    bl_idname = "setwire.setwire"
    bl_label = "Set wireframe mode On"
    bl_description = "Set wireframe mode On (in selected objects or all)"

    def execute(self, context):
        if bpy.context.selected_objects:
            for o in bpy.context.selected_objects:
                o.show_wire = True
        else:
            for o in bpy.data.objects:
                o.show_wire = True
        return{'FINISHED'}


class WireOff(bpy.types.Operator):
    bl_idname = "unsetwire.unsetwire"
    bl_label = "UnSet wireframe mode Off"
    bl_description = "Set wireframe mode Off (in selected objects or all)"

    def execute(self, context):
        if bpy.context.selected_objects:
            for o in bpy.context.selected_objects:
                o.show_wire = False
        else:
            for o in bpy.data.objects:
                o.show_wire = False
        return{'FINISHED'}


class UpdateRott(bpy.types.Operator):
    bl_idname = "updaterot.updaterot"
    bl_label = "Locator  -  Update Orientations"
    bl_description = "Update orientation Locator respect Projector"

    def execute(self, context):
        if "Locator" in bpy.data.objects:
            if bpy.data.objects['Proyector'].constraints['Child Of'].influence == 0:
                bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
                myplocator = bpy.data.objects["Locator"]
                myplocator.select = True
                bpy.context.scene.objects.active = myplocator  # lo hago objeto activo

                myplocator.constraints.new('TRACK_TO')
                myplocator.constraints["Track To"].target = bpy.data.objects["Proyector"]
                myplocator.constraints["Track To"].up_axis = 'UP_Y'
                myplocator.constraints["Track To"].track_axis = 'TRACK_Z'

                bpy.ops.nla.bake(frame_start=1, frame_end=1, step=1, only_selected=True, clear_constraints=True, bake_types={'OBJECT'})
                bpy.ops.anim.keyframe_clear_v3d()

                # chapuza para q luego el conector vuelva a funcionar juassss
                myplocator.constraints.new('TRACK_TO')
                myplocator.constraints["Track To"].target = bpy.data.objects["Proyector"]
                myplocator.constraints["Track To"].up_axis = 'UP_Y'
                myplocator.constraints["Track To"].track_axis = 'TRACK_Z'
                cons = myplocator.constraints['Track To']
                myplocator.constraints["Track To"].target = None
                myplocator.constraints.remove(cons)

        return{'FINISHED'}


class UpdateRottCam(bpy.types.Operator):
    bl_idname = "updaterotcam.updaterotcam"
    bl_label = "Locator  -  Update Orientations"
    bl_description = "Update orientation Projector respect Locator (use with care!!)"

    def execute(self, context):
        if "Proyector" in bpy.data.objects:
            if 'Track To' not in bpy.data.objects['Proyector'].constraints and bpy.data.objects['Proyector'].constraints['Child Of'].influence == 0:
                bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
                myproyector = bpy.data.objects["Proyector"]
                myproyector.select = True
                bpy.context.scene.objects.active = myproyector  # lo hago objeto activo

                bpy.data.objects['Proyector'].constraints.new('TRACK_TO')
                bpy.data.objects['Proyector'].constraints["Track To"].target = bpy.data.objects["Locator"]
                bpy.data.objects['Proyector'].constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
                bpy.data.objects['Proyector'].constraints["Track To"].up_axis = 'UP_Y'

                bpy.ops.nla.bake(frame_start=1, frame_end=1, step=1, only_selected=True, clear_constraints=True, bake_types={'OBJECT'})
                bpy.ops.anim.keyframe_clear_v3d()

                bpy.data.objects['Proyector'].constraints.new('CHILD_OF')
                bpy.data.objects['Proyector'].constraints['Child Of'].influence = 0
                bpy.context.object.constraints['Child Of'].target = bpy.data.objects["Locator"]

        return{'FINISHED'}


class Influence(bpy.types.Operator):
    bl_idname = "influence.influence"
    bl_label = "With influence"
    bl_description = "The projector will influence for locator"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True  # la selecciono
        bpy.context.scene.objects.active = camara
        try:
            bpy.context.object.constraints['Child Of'].influence = 1
            bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
        except:
            pass
        return{'FINISHED'}


class NoInfluence(bpy.types.Operator):
    bl_idname = "noinfluence.noinfluence"
    bl_label = "Without influence"
    bl_description = "The projector will not influence for locator"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True  # la selecciono
        bpy.context.scene.objects.active = camara
        try:
            bpy.context.object.constraints['Child Of'].influence = 0
            bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
        except:
            pass
        return{'FINISHED'}


class InfluenceK(bpy.types.Operator):
    bl_idname = "influencek.influencek"
    bl_label = "With influence Keep position"
    bl_description = "The projector will influence the locator and projector(camera) maintain the current position"

    def execute(self, context):
        if "Locator" in bpy.data.objects:
            bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
            camara = bpy.data.objects['Proyector']
            camara.select = True  # la selecciono
            bpy.context.scene.objects.active = camara
            try:
                coordenada = bpy.data.objects['Proyector'].matrix_world.translation
                coordenadas = [coordenada.x, coordenada.y, coordenada.z]
                bpy.context.object.constraints['Child Of'].influence = 1
                bpy.data.objects['Proyector'].matrix_world.translation = coordenadas

                #original_type = bpy.context.area.type
                #bpy.context.area.type = "PROPERTIES"
                #bpy.context.space_data.context = 'CONSTRAINT'

                # clear inverse
                # bpy.context.object.constraints['Child Of'].inverse_matrix = Matrix() # 4x4 Unit/identity matrix
                # set inverse
                bpy.context.object.constraints['Child Of'].inverse_matrix = bpy.context.object.constraints['Child Of'].target.matrix_world.inverted()  # is matrix_world really correct?
                # bpy.ops.constraint.childof_set_inverse(constraint="Child Of", owner='OBJECT') # <-- no se por que este no va.

                #bpy.context.area.type = original_type

                # influencia = bpy.context.object.constraints['Child Of'].influence #<- truco para q refreske
                # bpy.context.object.constraints['Child Of'].influence = influencia+1 #<- truco para q refreske
                # bpy.context.object.constraints['Child Of'].influence = influencia #<- truco para q refreske

                bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
                locator = bpy.data.objects["Locator"]
                locator.select = True  # la selecciono
                bpy.context.scene.objects.active = locator
            except:
                pass
        return{'FINISHED'}


class NoInfluencek(bpy.types.Operator):
    bl_idname = "noinfluencek.noinfluencek"
    bl_label = "Without influence Keep position"
    bl_description = "The projector will not influence the locator and projector(camera) maintain the current position"

    def execute(self, context):
        if "Locator" in bpy.data.objects:
            bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
            camara = bpy.data.objects["Proyector"]
            camara.select = True  # la selecciono
            bpy.context.scene.objects.active = camara
            locator = bpy.data.objects["Locator"]
            try:
                coordenada = bpy.data.objects['Proyector'].matrix_world.translation
                coordenadas = [coordenada.x, coordenada.y, coordenada.z]
                bpy.context.object.constraints['Child Of'].influence = 0
                bpy.data.objects['Proyector'].matrix_world.translation = coordenadas
                # bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
                locator.select = True  # la selecciono
                bpy.context.scene.objects.active = locator

                bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
                locator = bpy.data.objects["Locator"]
                locator.select = True  # la selecciono
                bpy.context.scene.objects.active = locator
            except:
                pass
        return{'FINISHED'}


class Inverse(bpy.types.Operator):
    bl_idname = "setinverse.setinverse"
    bl_label = "Set inverse"
    bl_description = "Inverse influence from locator"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True  # la selecciono
        bpy.context.scene.objects.active = camara
        try:
            bpy.ops.constraint.childof_set_inverse(constraint='Child Of', owner='OBJECT')
            influencia = bpy.context.object.constraints['Child Of'].influence  # <- truco para q refreske
            bpy.context.object.constraints['Child Of'].influence = influencia + 1  # <- truco para q refreske
            bpy.context.object.constraints['Child Of'].influence = influencia  # <- truco para q refreske
            # bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        except:
            pass
        return{'FINISHED'}


class ClearInverse(bpy.types.Operator):
    bl_idname = "clearinverse.clearinverse"
    bl_label = "Clear inverse"
    bl_description = "Dont Inverse influence from locator"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True  # la selecciono
        bpy.context.scene.objects.active = camara
        try:
            bpy.ops.constraint.childof_clear_inverse(constraint='Child Of', owner='OBJECT')
            influencia = bpy.context.object.constraints['Child Of'].influence  # <- truco para q refreske
            bpy.context.object.constraints['Child Of'].influence = influencia + 1  # <- truco para q refreske
            bpy.context.object.constraints['Child Of'].influence = influencia  # <- truco para q refreske
            # bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        except:
            pass
        return{'FINISHED'}


class AccionToselected(bpy.types.Operator):
    bl_idname = "toselected.toselected"
    bl_label = "To Selected"
    bl_description = "Apply projections to selected objects"

    def execute(self, context):
        # capturo el objeto en cuestion:
        ob = bpy.context.selected_objects
        # acciones:
        p.proyectorcillo(ob)

        if ob:
            img = imagen()
            v.vision()
            # si son muchos por eso me lo recorro:
            for i in range(len(ob)):
                if ob[i].type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                    sobject = ob[i]
                    # selecciono el objeto correspondiente a esa pasada:
                    sobject.select = True

                    # hago las acciones:
                    u.unwraping(sobject)
                    # uvmod requiere de la imagen se la paso por argumentos:
                    um.uvmod(sobject, img)
                    m.trymat(sobject, img)

                    # le seteamos las coordenadas de tipo de mapeo:
                    tc.uvgenerated(sobject)  # este setea en las coordenadas de textura que use uv
                    # actualizamos las relaciones:
                    up.update(ob)

        return{'FINISHED'}


class Accion_ToALL(bpy.types.Operator):
    bl_idname = "mod.mod"
    bl_label = "Apply/Update Modifier"
    bl_description = "Apply projections to all objects"

    def execute(self, context):

        img = imagen()
        v.vision()
        for ob in bpy.data.objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                p.proyectorcillo(ob)

                # hago las acciones:
                u.unwraping(ob)
                # uvmod requiere de la imagen se la paso por argumentos:
                um.uvmod(ob, img)
                m.trymat(ob, img)

                # le seteamos las coordenadas de tipo de mapeo:
                tc.uvgenerated(ob)
                # actualizamos las relaciones:
                up.update(ob)

        return{'FINISHED'}


class RELATIONS(bpy.types.Operator):
    bl_idname = "uprel.uprel"
    bl_label = "Update Relationship Material Modifier - Material Renderable"
    bl_description = "Only Update Relationship Material Modifier - Material Renderable"

    def execute(self, context):
        ob = bpy.context.active_object
        for ob in bpy.data.objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                try:
                    ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].texture.image = ob.modifiers['UV_PROJECT'].image
                except:
                    pass
        v.vision()
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
