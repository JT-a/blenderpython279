import bpy


def crear_slot():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.uv_texture_add()  # agregando slot de mapa uv (por defecto de nombre UVMap)
    bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, correct_aspect=True, use_subsurf_data=False, margin=0.001)
    #bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, correct_aspect=True,use_subsurf_data=False, uv_subsurf_level=6)
    bpy.ops.object.mode_set(mode='OBJECT')
    try:
        bpy.context.object.data.uv_textures['UVMap'].name = "uvprojection"  # renombrado
        bpy.data.meshes[bpy.context.active_object.data.name].uv_textures["uvprojection"].active_render = True
    except:
        pass

# mapas uv


def uwap_cn_nombre():

    slots_uvs = bpy.context.object.data.uv_textures
    numero_slots = len(slots_uvs)

    slots_detectados = []  # <-- los backups y uvprojections
    slots_neutros = []  # <-- el resto

    if numero_slots == 0:
        crear_slot()
    else:

        for i in range(numero_slots):
            if slots_uvs[i].name.find('bkup_') == 0 or slots_uvs[i].name == 'uvprojection':
                slots_detectados.append(slots_uvs[i])
            else:
                slots_neutros.append(slots_uvs[i])

        # limpiando lista de repetidos:
        def rmRepetidos(listado):
            listado = list(set(listado))  # elimina duplicados
            return listado

        # limpiando lista de repetidos:
        slots_neutros = rmRepetidos(slots_neutros)

        lslots_detectados = len(slots_detectados)  # <-- los backups y uvprojections
        lslots_neutros = len(slots_neutros)  # <-- el resto

        if lslots_detectados == numero_slots:
            if slots_uvs[i].name.find('uvprojection') < 0:
                crear_slot()

        # creando backups:
        for i in range(len(slots_neutros)):
            if slots_uvs[i].name not in slots_detectados:
                if slots_uvs[i].name.find('bkup_') < 0:
                    if slots_uvs[i].name != 'uvprojection':
                        slots_uvs[i].name = "bkup_" + slots_uvs[i].name


class Unwrap(object):

    def __init__(self, ob=None):
        self.ob = None

    def unwraping(self, ob):
        if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
            bpy.context.scene.objects.active = bpy.data.objects[str(ob.name)]  # seteando objeto activo
            myobject = bpy.data.objects[str(ob.name)]
            myobject.select = True

            uwap_cn_nombre()

            myobject.select = False
            bpy.context.active_object.name = ''  # deseteando active object
            bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
