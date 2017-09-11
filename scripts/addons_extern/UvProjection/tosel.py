import bpy


class Tosel(object):

    def __init__(self, ob=None, img=None):
        self.ob = None
        self.img = None

    def aplicar(self, ob, img):

        # si hay objeto seleccionado entonces:
        if ob:

            try:

                #img = imagen()
                # img viene por parametros

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

                        # seteamos la imagen al modificador
                        sobject.modifiers['UV_PROJECT'].image = img  # seteamos la imagen
                        # le seteamos las coordenadas de tipo de mapeo:
                        tc.uvgenerated(sobject)
                        # actualizamos las relaciones:

            except:
                pass
