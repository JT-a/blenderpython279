import bpy

######## materiales ############


def MiMaterial():
    scn = bpy.context.scene
    mat = bpy.data.materials.new("MiMaterial")
    mat.specular_intensity = scn.MatSpecular
    if scn.shadelessmode:
        mat.use_shadeless = True
    else:
        mat.use_shadeless = False
    #mat.use_shadeless = True
    mat.use_transparency = True
    mat.alpha = 0

    return mat


class Material(object):

    def __init__(self, ob=None, img=None):
        self.ob = None
        self.img = None

    def trymat(self, ob, img):
        try:

            # if "MiMaterial" not in ob.data.materials or img != ob.data.materials[0].texture_slots[0].texture.image.name:
            material = MiMaterial()

            # si no existe el material lo creamos:
            # si existe es 0 si no existe es -1
            if ob.data.materials.find('MiMaterial') != 0:

                # si no hay materiales lo creamos:
                if len(ob.data.materials) == 0:
                    bpy.ops.object.material_slot_add()
                    # ob.data.materials.append(material)
                    ob.data.materials[0] = material

            # le aplicamos el material al objeto:
            ob.data.materials[0] = material

            # abreviamos el slot de nombre de textura (agregando slot texture)
            slot = ob.data.materials[ob.data.materials[0].name].texture_slots.add()
            # borramos las texturas en slot 1 osea la segunda si hubiera:
            ob.data.materials[ob.data.materials[0].name].texture_slots.clear(1)

            # si el nombre del slot texture del primer material no tiene nombre:
            if ob.data.materials[ob.data.materials[0].name].texture_slots[0].name == '':
                # creamos la textura:
                tipoimg = bpy.data.textures.new(type='IMAGE', name='Textura')
                # y se la aplicamos:
                slot.texture = tipoimg

            # especificando la imagen de textura:
            ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].texture.image = img
            # seteando que utilice el alpha de la propia imagen:
            ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].use_map_alpha
            ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].uv_layer = 'uvprojection'  # agregando el mapa de uv
            ######## fin materiales ########

            # reaplicando settings al modificador:
            camara = bpy.data.objects["Proyector"]
            modificador = ob.modifiers["UV_PROJECT"]
            modificador.projector_count = 1
            modificador.projectors[0].object = camara
            ob.modifiers['UV_PROJECT'].image = img  # seteamos la imagen
            ob.modifiers['UV_PROJECT'].uv_layer = 'uvprojection'  # agregando el mapa de uv

        except:
            pass
