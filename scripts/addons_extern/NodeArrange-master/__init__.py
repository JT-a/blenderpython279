#Lisence is FFA, Free For All
#you can do everything with the code, sell, loan, rent, publish it, not publish it, change your license 

bl_info = {
    "name": "Node Arrange",
    "author": "TynkaTopi (JuhaW)",
    "version": (0, 1, 0),
    "blender": (2, 78, 0),
    "location": "Node Editor > Properties > Trees",
    "description": "Node Tree Arrangement Tools",
    "tracker_url": "https://github.com/JuhaW/NodeArrange/issues",
    "category": "Node"}

import sys
import bpy

CYCLES = True
VRAY = not CYCLES


class values():
    average_y = 0
    x_last = 0
    margin_x = 100
    mat_name = ""
    margin_y = 20


class NodePanel(bpy.types.Panel):
    bl_label = "Nodes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Trees"

    def draw(self, context):

        layout = self.layout
        row = layout.row()
        col = layout.column
        # split = layout.split(percentage=.6)
        row.operator('node.button')

        row = layout.row()
        row.prop(bpy.context.scene, 'nodemargin_x', text="Margin x")
        row = layout.row()
        row.prop(bpy.context.scene, 'nodemargin_y', text="Margin y")
        row = layout.row()
        row.prop(context.scene, 'node_center', text="Center nodes")
        row = layout.row()
        row.operator('node.button_center')
        row = layout.row()
        row.operator('node.button_odd')
        row = layout.row()


class NodeButton(bpy.types.Operator):

    'Rearrange whole of current node tree'
    bl_idname = 'node.button'
    bl_label = 'Arrange nodes'

    # not sure this is doing what you expect.
    # blender.org/api/blender_python_api_current/bpy.types.Operator.html#invoke
    def invoke(self, context, value):
        nodemargin(self, context)
        return {'FINISHED'}


class NodeButtonOdd(bpy.types.Operator):

    'Select nodes that have no output or don\'t link to Output node'
    bl_idname = 'node.button_odd'
    bl_label = 'Select odd nodes'

    def execute(self, context):
        nodes_iterate(context.space_data.edit_tree.nodes, False)
        return {'FINISHED'}


class NodeButtonCenter(bpy.types.Operator):

    'Move node tree to the origin'
    bl_idname = 'node.button_center'
    bl_label = 'Center nodes (0,0)'

    def execute(self, context):
        nodes_center(context.space_data.edit_tree.nodes)
        return {'FINISHED'}


def nodemargin(self, context):

    ntree = context.space_data.edit_tree.nodes
    values.margin_x = context.scene.nodemargin_x
    values.margin_y = context.scene.nodemargin_y

    nodes_iterate(ntree)

    # arrange nodes + this center nodes together
    if context.scene.node_center:
        nodes_center(ntree)


def outputnode_search(ntree):  # return node/None

    for node in ntree:
        # print ("node:",node)
        if VRAY:
            if node.bl_idname == 'VRayNodeOutputMaterial' and node.inputs[0].is_linked:
                return node
        else:
            if node.type in ['OUTPUT', 'GROUP_OUTPUT', 'COMPOSITE'] and node.inputs[0].is_linked:
                return node

    print("No output node found")
    return None


###############################################################
def nodes_iterate(ntree, arrange=True):

    nodeoutput = outputnode_search(ntree)
    if nodeoutput is None:
        return None
    nodeoutput.label = str(0)
    # print ("nodeoutput:",nodeoutput)

    a = []
    a.append(nodeoutput)
    a.append(0)
    nodelist = []
    nodelist.append(a)

    nodecounter = 0
    level = 0

    while nodecounter < len(nodelist):

        basenode = nodelist[nodecounter][0]
        inputlist = (i for i in basenode.inputs if i.is_linked)
        nodecounter += 1

        for input in inputlist:

            for nlinks in input.links:

                node = nlinks.from_node
                node.label = str(int(basenode.label) + 1)
                level = int(basenode.label)

                b = []
                b.append(node)
                b.append(level + 1)
                nodelist.append(b)

    ########################################
    # delete duplicated nodes at the same level, first wins

    templist = []
    for item in nodelist:
        if item not in templist:
            templist.append(item)
    '''
    for item in a:
        print ("item:", item[1])
    print()
    '''

    # delete duplicated nodes
    newnodes = []
    newlevels = []

    for i, item in enumerate(reversed(templist)):
        # print ("nodelist reversed:", item)
        # node label back to default
        item[0].label = ""
        if item[0] not in newnodes:
            newnodes.append(item[0])
            newlevels.append(item[1])
            # print (i,item[0],item[1])

    nodelist = []
    for i, item in enumerate(newnodes):
        # print ("newnodes:",i,item,newlevels[i])
        a = []
        a.append(item)
        a.append(newlevels[i])
        nodelist.append(a)

    nodelist.reverse()
    newnodes.reverse()
    newlevels.reverse()

    if not arrange:
        nodes_odd(ntree, newnodes)
        return None

    ########################################
    level = 0
    levelmax = max(newlevels) + 1
    values.x_last = 0

    while level < levelmax:

        values.average_y = 0
        nodes = [x for i, x in enumerate(newnodes) if newlevels[i] == level]
        nodes_arrange(nodes, level)
        # print ("level:", level, nodes)
        level = level + 1

    return None


###############################################################
def nodes_odd(ntree, nodelist):

    for i in ntree:
        i.select = False

    a = [x for x in ntree if x not in nodelist]
    # print ("odd nodes:",a)
    for i in a:
        i.select = True


def nodes_arrange(nodelist, level):

    # node x positions

    widthmax = max([x.dimensions.x for x in nodelist])
    xpos = values.x_last - (widthmax + values.margin_x) if level != 0 else 0
    # print ("nodelist, xpos", nodelist,xpos)
    values.x_last = xpos

    # node y positions
    x = 0
    y = 0

    for node in nodelist:

        if node.hide:
            hidey = (node.dimensions.y / 2) - 8
            y = y - hidey
        else:
            hidey = 0

        node.location.y = y
        y = y - values.margin_y - node.dimensions.y + hidey

        node.location.x = xpos

    y = y + values.margin_y

    center = (0 + y) / 2
    values.average_y = center - values.average_y

    for node in nodelist:

        node.location.y -= values.average_y


def nodes_center(ntree):

    bboxminx = []
    bboxmaxx = []
    bboxmaxy = []
    bboxminy = []

    for node in ntree:
        if not node.parent:
            bboxminx.append(node.location.x)
            bboxmaxx.append(node.location.x + node.dimensions.x)
            bboxmaxy.append(node.location.y)
            bboxminy.append(node.location.y - node.dimensions.y)

    # print ("bboxminy:",bboxminy)
    bboxminx = min(bboxminx)
    bboxmaxx = max(bboxmaxx)
    bboxminy = min(bboxminy)
    bboxmaxy = max(bboxmaxy)
    center_x = (bboxminx + bboxmaxx) / 2
    center_y = (bboxminy + bboxmaxy) / 2
    '''
    print ("minx:",bboxminx)
    print ("maxx:",bboxmaxx)
    print ("miny:",bboxminy)
    print ("maxy:",bboxmaxy)

    print ("bboxes:", bboxminx, bboxmaxx, bboxmaxy, bboxminy)
    print ("center x:",center_x)
    print ("center y:",center_y)
    '''

    x = 0
    y = 0

    for node in ntree:

        if not node.parent:
            node.location.x -= center_x
            node.location.y += -center_y


def register():
    bpy.types.Scene.nodemargin_x = bpy.props.IntProperty(default=100, update=nodemargin)
    bpy.types.Scene.nodemargin_y = bpy.props.IntProperty(default=20, update=nodemargin)
    bpy.types.Scene.node_center = bpy.props.BoolProperty(default=True, update=nodemargin)
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.nodemargin_x
    del bpy.types.Scene.nodemargin_y
    del bpy.types.Scene.node_center

if __name__ == "__main__":
    register()
