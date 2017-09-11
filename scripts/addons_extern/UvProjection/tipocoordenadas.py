import bpy


class Tipocoordenadas(object):

    def __init__(self, ob=None):
        self.ob = None

    def uvgenerated(self, ob):

        # seteando el tipo de coordenadas "UV" en lugar de "Generated"
        ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].texture_coords = 'UV'
        uv_layer_modifier = ob.modifiers['UV_PROJECT'].uv_layer
        uv_layer_textures = ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].uv_layer

        uv_layer_modifier = "uvprojection"  # seteando su valor a UVTex (Nomenglatura antigua)

        if uv_layer_modifier == '':
            uv_layer_modifier = "uvprojection"  # seteando su valor a UVMap

        if uv_layer_textures == '':
            uv_layer_textures = uv_layer_modifier

        # seteando que use tb como alpha:
        ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].use_map_alpha = True
