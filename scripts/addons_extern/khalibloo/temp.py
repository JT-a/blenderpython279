import bpy
for obj in bpy.data.objects:
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.name = "khalibloo"
