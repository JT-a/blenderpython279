import bpy


class Update(object):

    def __init__(self, ob=None):
        self.ob = None

    def update(self, ob):
        try:
            ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].texture.image = ob.modifiers['UV_PROJECT'].image
        except:
            pass
