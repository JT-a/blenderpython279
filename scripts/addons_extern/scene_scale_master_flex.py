#   Scale Master Flex

#   How to use this script:
#     1 - To use this script in your own files, just copy and paste this text into the text editor window
#     2 - Select your objects
#     3 - If desired change overall dimensions by using the "unit scale" value in the scene properties
#     4 - Hover over this script and press alt+p to run it

#   Tutorial on how the script works:
#     - https://youtu.be/X_dJYAMCGYw

#   What this script does:
#     -Resizes selected objects based on the "unit scale" value in the scene properties in order to correct their dimensions.
#     -Applies scale to selected objects
#     -Applies scale to linked duplicates while keeping them linked
#     -Applies scale to lattice deformed objects without messing them up
#     -Adjusts modifier values when applying scale so they don't visually change

#   by Chris Plush | cgmasters.net

import bpy

bl_info = {'name': 'Scale Master Flex',
           'category': 'Object'}

var2 = bpy.context.scene.unit_settings.scale_length
objects = bpy.context.selected_objects
bpy.context.scene.objects.active = objects[0]
linkedoblist = []
linkedmeshlist = []
latticelist = []
latticedata = []
latticechildren = []

#Runs through modifiers to change values based on object scaling and scene scaling
def modifierfun(var):
    if mod.name == 'Bevel':
        mod.width *= var
    elif mod.name == 'Solidify':
        mod.thickness *= var
    elif mod.name == 'Array':
        mod.constant_offset_displace[0] *= var
        mod.constant_offset_displace[1] *= var
        mod.constant_offset_displace[2] *= var
        mod.merge_threshold *= var
    elif mod.name == 'Boolean':
        mod.double_threshold *= var
    elif mod.name == 'Mirror':
        mod.merge_threshold *= var
    elif mod.name == 'Screw':
        mod.screw_offset *= var
    elif mod.name == 'Wireframe':
        mod.thickness *= var
    elif mod.name == 'Cast':
        mod.radius *= var
    elif mod.name == 'Hook':
        mod.falloff_radius *= var
    elif mod.name == 'Shrinkwrap':
        mod.offset *= var
    elif mod.name == 'Warp':
        mod.falloff_radius *= var
    elif mod.name == 'Wave':
        mod.start_position_x *= var
        mod.start_position_y *= var
        mod.falloff_radius *= var
        mod.height *= var
        mod.width *= var
        mod.narrowness *= var

#Append lattices to a list. Append their children to another list.
for ob in objects:
    if ob.type == 'LATTICE' and ob.children:
        latticelist.append(ob)
        latticedata.append(ob.data)
        latticechildren.append(ob.children[0])
    if ob.type not in ['EMPTY', 'SPEAKER'] and ob.data.users > 1 and ob.type!= 'LATTICE':
        linkedoblist.append(ob)
        linkedmeshlist.append(ob.data)

#First pass. Change modifier values to compensate for any object scaling. Make any linked lattice children single users.
for ob in objects:
    var1 = min(ob.scale, key=lambda x:abs(1-x))
    if latticechildren.count(ob) > 0:
        bpy.ops.object.make_single_user(object=True, obdata=True)
    if ob.modifiers:
        for mod in ob.modifiers:
            modifierfun(var1)

#Clear parenting of lattice children but keep lattice modifier active
for ob in latticechildren:
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

#Resize all selected objects based on the scene's unit scale
bpy.ops.transform.resize(value = (1.0*var2,1.0*var2,1.0*var2))

#Deselect objects we don't want to apply scaling to
for ob in objects:
    if ob.type in ['CAMERA','LAMP', 'EMPTY', 'SPEAKER', 'LATTICE']:
        ob.select = False

#Make objects single users and apply scale
bpy.ops.object.make_single_user(object=True, obdata=True)
bpy.ops.object.transform_apply(scale=True)

#Relink duplicate meshes
for ob in linkedoblist:
    ob.data = linkedmeshlist[linkedoblist.index(ob)]

#Second modifier pass. Change modifier values to be proportional to scene's unit scale.
for ob in objects:
    if ob.modifiers:
        for mod in ob.modifiers:
            modifierfun(var2)

#Re-parent children to lattices
for child in latticechildren:
    bpy.ops.object.select_all(action='DESELECT')
    latticeparent = latticelist[latticechildren.index(child)]
    child.select = True
    latticeparent.select = True
    bpy.context.scene.objects.active = latticeparent
    bpy.ops.object.parent_set(type='LATTICE')

#Re-link duplicate lattices
for ob in latticelist:
    ob.data = latticedata[latticelist.index(ob)]

#Reset the scene's unit scale back to 1
bpy.context.scene.unit_settings.scale_length = 1

#Reselect original selection
for ob in objects:
    ob.select = True
