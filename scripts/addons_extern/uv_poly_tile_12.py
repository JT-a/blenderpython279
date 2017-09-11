# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#  Code by Koilz @ http://wiki.blender.org/ 2015
#
# ##### END GPL LICENSE BLOCK #####


# ----------------------------------------------------------------
# Addon

bl_info = {
    "name": "Poly Tile 1.2",
    "author": "koilz",
    "version": (1, 2),
    "blender": (2, 72, 0),
    "location": "3D View > Mesh Edit Mode > Tools > PT",
    "description": "Unwrap selected polygons to tile based coordinates.",
    "warning": "",
    "wiki_url": "",
    "category": "UV"}

# ----------------------------------------------------------------


# ----------------------------------------------------------------
# Header

import bpy

UVR = [('R0', '0', '0'),
       ('R90', '90', '90'),
       ('R180', '180', '180'),
       ('R270', '270', '270')]


class UPT_props(bpy.types.PropertyGroup):

    # static settings

    TXW = bpy.props.IntProperty(name="Texture Width", description="Texture Width", default=128)
    TXH = bpy.props.IntProperty(name="Texture Height", description="Texture Height", default=128)

    TXX = bpy.props.IntProperty(name="Texture X", description="Texture X, origin for tiles", default=0)
    TXY = bpy.props.IntProperty(name="Texture Y", description="Texture Y, origin for tiles", default=0)

    TLW = bpy.props.IntProperty(name="Tile Width", description="Tile Width", default=32)
    TLH = bpy.props.IntProperty(name="Tile Height", description="Tile Height", default=32)

    TLB = bpy.props.IntProperty(name="Tile Border Size", description="Tile border size in pixels, based on texture resolution", default=0)

    # dynamic settings

    TLXO = bpy.props.IntProperty(name="Tile X", description="Tile X offset", default=0)
    TLYO = bpy.props.IntProperty(name="Tile Y", description="Tile Y offset", default=0)

    TLXM = bpy.props.BoolProperty(name="X Mirror", description="X Mirror the UV mapping", default=False)
    TLYM = bpy.props.BoolProperty(name="Y Mirror", description="Y Mirror the UV mapping", default=False)

    TLRT = bpy.props.EnumProperty(items=UVR, name="Rotate", description="Rotate the UV Mapping", default='R0')

# ----------------------------------------------------------------


# ----------------------------------------------------------------
# Operator

class OT_PT(bpy.types.Operator):
    """Unwrap selected polygons to tile based coordinates."""
    bl_idname = "scene.poly_tile"
    bl_label = "Poly Tile"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    # static settings

    TXW = bpy.props.IntProperty(name="Texture Width", description="Texture Width", default=128)
    TXH = bpy.props.IntProperty(name="Texture Height", description="Texture Height", default=128)

    TXX = bpy.props.IntProperty(name="Texture X", description="Texture X, origin for tiles", default=0)
    TXY = bpy.props.IntProperty(name="Texture Y", description="Texture Y, origin for tiles", default=0)

    TLW = bpy.props.IntProperty(name="Tile Width", description="Tile Width", default=32)
    TLH = bpy.props.IntProperty(name="Tile Height", description="Tile Height", default=32)

    TLB = bpy.props.IntProperty(name="Tile Border Size", description="Tile border size in pixels, based on texture resolution", default=0)

    # dynamic settings

    TLXO = bpy.props.IntProperty(name="Tile X", description="Tile X offset", default=0)
    TLYO = bpy.props.IntProperty(name="Tile Y", description="Tile Y offset", default=0)

    TLXM = bpy.props.BoolProperty(name="X Mirror", description="X Mirror the UV mapping", default=False)
    TLYM = bpy.props.BoolProperty(name="Y Mirror", description="Y Mirror the UV mapping", default=False)

    TLRT = bpy.props.EnumProperty(items=UVR, name="Rotate", description="Rotate the UV Mapping", default='R0')

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        pmode = context.active_object.mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Add UVMap if none

        if bpy.context.active_object.data.uv_textures.active_index == -1:
            bpy.ops.mesh.uv_texture_add()

        # Texture size

        tx_w = self.TXW
        tx_h = self.TXH

        # UV pixel

        uvp_w = 1.0 / self.TXW
        uvp_h = 1.0 / self.TXH

        # Tile start

        tile_x = uvp_w * self.TXX
        tile_y = uvp_w * self.TXY

        # Tile size

        tile_w = uvp_w * self.TLW
        tile_h = uvp_h * self.TLH

        # Tile border

        tile_border_w = uvp_w * self.TLB
        tile_border_h = uvp_h * self.TLB

        # UV map

        uvt = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]

        # UV map based on offset

        tx0 = tile_w * (self.TLXO)
        tx1 = tile_w * (self.TLXO + 1)
        tx2 = tile_w * (self.TLXO + 1)
        tx3 = tile_w * (self.TLXO)

        ty0 = tile_h * (self.TLYO)
        ty1 = tile_h * (self.TLYO)
        ty2 = tile_h * (self.TLYO + 1)
        ty3 = tile_h * (self.TLYO + 1)

        # Add border

        uva = [[tx0 + (tile_border_w), ty0 + (tile_border_h)],
               [tx1 - (tile_border_w), ty1 + (tile_border_h)],
               [tx2 - (tile_border_w), ty2 - (tile_border_h)],
               [tx3 + (tile_border_w), ty3 - (tile_border_h)]]

        # Mirror

        if self.TLXM == False:
            uvt[0][0] = uva[0][0]
            uvt[1][0] = uva[1][0]
            uvt[2][0] = uva[2][0]
            uvt[3][0] = uva[3][0]
        else:
            uvt[0][0] = uva[1][0]
            uvt[1][0] = uva[0][0]
            uvt[2][0] = uva[3][0]
            uvt[3][0] = uva[2][0]

        if self.TLYM == False:
            uvt[0][1] = uva[0][1]
            uvt[1][1] = uva[1][1]
            uvt[2][1] = uva[2][1]
            uvt[3][1] = uva[3][1]
        else:
            uvt[0][1] = uva[2][1]
            uvt[1][1] = uva[3][1]
            uvt[2][1] = uva[0][1]
            uvt[3][1] = uva[1][1]

        # Rotate to selected

        layer_id = 0

        for p in context.active_object.data.polygons:
            if p.select:
                layer = context.active_object.data.uv_layers.active

                if self.TLRT == 'R0':
                    layer.data[layer_id].uv = uvt[0]
                    layer.data[layer_id + 1].uv = uvt[1]
                    layer.data[layer_id + 2].uv = uvt[2]
                    layer.data[layer_id + 3].uv = uvt[3]

                if self.TLRT == 'R90':
                    layer.data[layer_id].uv = uvt[1]
                    layer.data[layer_id + 1].uv = uvt[2]
                    layer.data[layer_id + 2].uv = uvt[3]
                    layer.data[layer_id + 3].uv = uvt[0]

                if self.TLRT == 'R180':
                    layer.data[layer_id].uv = uvt[2]
                    layer.data[layer_id + 1].uv = uvt[3]
                    layer.data[layer_id + 2].uv = uvt[0]
                    layer.data[layer_id + 3].uv = uvt[1]

                if self.TLRT == 'R270':
                    layer.data[layer_id].uv = uvt[3]
                    layer.data[layer_id + 1].uv = uvt[0]
                    layer.data[layer_id + 2].uv = uvt[1]
                    layer.data[layer_id + 3].uv = uvt[2]

            layer_id += p.loop_total

        bpy.ops.object.mode_set(mode=pmode)

        return {'FINISHED'}

# ----------------------------------------------------------------


# ----------------------------------------------------------------
# Panel

class PT_UPT(bpy.types.Panel):

    bl_label = "Poly Tile"
    bl_idname = "VIEW3D_PT_UPT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Shading / UVs"
    bl_context = "mesh_edit"

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.mode == 'EDIT')

    def draw(self, context):
        layout = self.layout

        # static settings

        col = layout.column(align=True)

        row = col.row(align=True)
        row.prop(context.scene.UPT, 'TXW')
        row.prop(context.scene.UPT, 'TXH')

        row = col.row(align=True)
        row.prop(context.scene.UPT, 'TXX')
        row.prop(context.scene.UPT, 'TXY')

        row = col.row(align=True)
        row.prop(context.scene.UPT, 'TLW')
        row.prop(context.scene.UPT, 'TLH')

        row = col.row(align=True)
        row.prop(context.scene.UPT, 'TLB')

        # dynamic settings

        col = layout.column(align=True)

        row = col.row(align=True)
        row.prop(context.scene.UPT, 'TLXO')
        row.prop(context.scene.UPT, 'TLYO')

        row = col.row(align=True)
        row.prop(context.scene.UPT, 'TLXM', toggle=True)
        row.prop(context.scene.UPT, 'TLYM', toggle=True)

        row = col.row(align=True)
        col = row.column(align=True)
        col.row(align=True).prop(context.scene.UPT, 'TLRT', expand=True)

        # operator

        col = layout.column(align=True)
        xx = col.operator('scene.poly_tile')

        xx.TXW = context.scene.UPT.TXW
        xx.TXH = context.scene.UPT.TXH
        xx.TXX = context.scene.UPT.TXX
        xx.TXY = context.scene.UPT.TXY
        xx.TLW = context.scene.UPT.TLW
        xx.TLH = context.scene.UPT.TLH
        xx.TLB = context.scene.UPT.TLB

        xx.TLXO = context.scene.UPT.TLXO
        xx.TLYO = context.scene.UPT.TLYO
        xx.TLXM = context.scene.UPT.TLXM
        xx.TLYM = context.scene.UPT.TLYM
        xx.TLRT = context.scene.UPT.TLRT

# ----------------------------------------------------------------


# ----------------------------------------------------------------
# Register

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.UPT = bpy.props.PointerProperty(type=UPT_props)


def unregister():
    del bpy.types.Scene.UPT
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

# ----------------------------------------------------------------
