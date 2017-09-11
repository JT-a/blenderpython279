import bpy

# Aplicando Modificador al objeto


class Uvmod(object):

    def __init__(self, ob=None, img=None):
        self.ob = None
        self.img = None

    def uvmod(self, ob, img):
        if "UV_PROJECT" not in ob.modifiers:
            ob.modifiers.new(name='UV_PROJECT', type='UV_PROJECT')
            ob.modifiers['UV_PROJECT'].use_image_override = True
            camara = bpy.data.objects["Proyector"]
            modificador = ob.modifiers["UV_PROJECT"]
            modificador.projector_count = 1
            modificador.projectors[0].object = camara
            ob.modifiers['UV_PROJECT'].image = img  # seteamos la imagen
            ob.modifiers['UV_PROJECT'].uv_layer = 'uvprojection'  # agregando el mapa de uv
