#*********************************************************************************************
# NAME : shaderNodeObjectIndexer.py
#
# TYPE : Input Shader
#
# DESCRIPTION : compute the number of object sharing the same prefix name of the current object.
#               linked to this material. Work with node_objectindexer.osl
#
# SOCKETS :
# 	Outputs :
# 		Total        	: int 	- total number of objects ( 1 <= Total <= +inf. )
#               RefLoc          : point - TODO
#               InfLoc          : point - TODO
#       Options :
#               Auto Update     : bool  - compute Total (unset it if you prefer to set Total yourself)
#
# AUTHOR
# 	Valery Seys - Paris /\
#
# CHANGELOG
# 11/12/15 12:01    initial release
#
# TODO
#
#********************************************************************************************/
bl_info = {
    "name": "Shader Node Object Indexer (Cycles)",
    "description": "Provide Object Info Index, works with the shader node_objectindexer.osl",
    "author": "Valery Seys",
    "version": (0, 0, 1),
    "blender": (2, 7, 6),
    "location": "Node Editor",
    "category": "Node",
    "warning": "Beta",
    "wiki-url": "",
}

import bpy
import importlib
import nodeitems_builtins
import nodeitems_utils
from bpy.types import NodeTree, Node, NodeSocket
from nodeitems_utils import NodeCategory, NodeItem, NodeItemCustom
from nodeitems_builtins import ShaderNewNodeCategory


class ObjectIndexer(bpy.types.Node):
    bl_idname = 'ShaderNodeObjectIndexer'
    bl_label = 'Object Info Indexer'       # label seen in the property panel
    bl_icon = 'INFO'

    checkLoc = False

    def onAutoUpdateChange(self, context):   # act as static
        node = self.getNode(context)
        if node is None:
            return
        if node.autoUpdateProperty == True:
            node.computeTotal(context)
            node["autoUpdateProperty"] = True
        else:
            node["autoUpdateProperty"] = False

    def onUserTotalChange(self, context):    # act as static
        node = self.getNode(context)
        if node is None:
            return
        print("==> DEBUG : onUserTotalChange() called, computerChange : %d" % int(node.isaComputerChange))
        if not node.isaComputerChange:
            node.autoUpdateProperty = False
            node.outputs["Total"].default_value = node.userTotalProperty
            node.updateLinks(node)
        else:
            node.isaComputerChange = False
            node.userTotalProperty = node.outputs["Total"].default_value

    autoUpdateProperty = bpy.props.BoolProperty(name="Auto Update", description="Update automatically total", default=False, update=onAutoUpdateChange)
    userTotalProperty = bpy.props.IntProperty(name="Total", description="Total", default=1, min=1, step=1, update=onUserTotalChange)
    isaComputerChange = bpy.props.BoolProperty(name="ComputerChange", default=False)  # avoid recursing (change coming from computation, not user)

    @classmethod
    def poll(cls, ntree):       # TODO
        print("==> DEBUG : poll() called")
        b = False
        # Make your node appear in different node trees by adding their bl_idname type here.
        if ntree.bl_idname == 'ShaderNodeTree':
            b = True
        return b

    def init(self, context):    # context is not set yet and is not usable
        self.outputs.new('NodeSocketInt', "Total")              # our output socket
        self.outputs["Total"].default_value = self.userTotalProperty
        self.outputs.new('NodeSocketVector', "RefLoc")
        self.outputs["RefLoc"].default_value = (0.0, 0.0, 0.0)
        self.outputs.new('NodeSocketVector', "InfLoc")
        self.outputs["InfLoc"].default_value = (0.0, 0.0, 0.0)

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        currentScene = context.scene
        layout.prop(self, "autoUpdateProperty")
        layout.prop(self, "userTotalProperty")
        # prop_search(data, property, search_data, search_property, text="", text_ctxt="", translate=True, icon='NONE')
        # we use 'SNOI_OREF' as string : see self.register()
        layout.label("Spacial Reference:")
        layout.prop_search(currentScene, "SNOI_OREF", currentScene, "objects", text="Reference")
        layout.prop_search(currentScene, "SNOI_OEXT", currentScene, "objects", text="Influence")

    # The label seen on the Node Title Bar
    def draw_label(self):
        return "Object Indexer"

    def update(self):   # Update on editor changes
        print("==> DEBUG : update()")
        currentScene = bpy.context.scene
        # Checking if OREF AND OEXT are set:
        if currentScene.SNOI_OREF is not None and currentScene.SNOI_OREF != '' and currentScene.SNOI_OEXT is not None and currentScene.SNOI_OEXT != '':
            self.outputs["RefLoc"].default_value = currentScene.objects[currentScene.SNOI_OREF].location
            self.outputs["InfLoc"].default_value = currentScene.objects[currentScene.SNOI_OEXT].location
            self.checkLoc = True
            print("==> DEBUG : refLoc,infLoc set.")
        else:
            self.checkLoc = False
            print("==> DEBUG : refLoc,infLoc unset.")

        if self.autoUpdateProperty:
            self.computeTotal(bpy.context)
        # Review linked outputs.
        self.updateLinks(self)

    def updateLinks(self, node):
        print("==> DEBUG : updateLinks() ...")
        try:
            out = node.outputs["Total"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if out.is_linked:
                print("==> DEBUG : node is linked")
                for o in out.links:
                    if o.is_valid:
                        print("==> DEBUG : link %s (type %s)" % (o.to_socket.name, o.to_socket.bl_idname))
                        if o.to_socket.bl_idname == "NodeSocketInt":
                            o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
        can_continue = False
        if node.checkLoc is True:
            print("==> DEBUG : checkLoc True, reviewing Outputs...")
        try:
            outRef = node.outputs["RefLoc"]
            outInf = node.outputs["InfLoc"]
            can_continue = True
        except:
            can_continue = False
        if can_continue:
            if outRef.is_linked and outInf.is_linked:
                print("==> DEBUG : vectors linked, updating valid nodes")
                for o in outRef.links:
                    if o.is_valid:
                        if o.to_socket.bl_idname == "NodeSocketVector":
                            o.to_socket.node.inputs[o.to_socket.name].default_value = outRef.default_value
                for o in outInf.links:
                    if o.is_valid:
                        if o.to_socket.bl_idname == "NodeSocketVector":
                            o.to_socket.node.inputs[o.to_socket.name].default_value = outInf.default_value

    def getNode(self, context):
        materialName = context.object.active_material.name
        if hasattr(context, 'node'):
            return context.node
        else:
            n = bpy.data.materials[materialName].node_tree.nodes.active
            if hasattr(n, 'getNode'):    # yes, it's me
                return n
            else:
                return None     # user disconnect links from other node, we loose the focus: no need to compute anything

    def computeTotal(self, context):
        materialName = context.object.active_material.name
        znode = self.getNode(context)
        if znode is None:
            return
        if not znode.autoUpdateProperty:
            return
        else:
            print("==> DEBUG : computeTotal() for %s" % context.object.name)
        # currently one object : me
        total = 1
        # what about me
        objectNameSplited = context.object.name.split('.')
        if len(objectNameSplited) > 1:
            objectNamePrefix, objectNameSuffix = objectNameSplited
        else:
            objectNamePrefix = objectNameSplited[0]
            objectNameSuffix = None
        # Ok, now find out if clones exists (with same material of course ..)
        for obj, ptr in bpy.data.scenes[bpy.context.scene.name].objects.items():
            if ptr.type == 'MESH' and objectNamePrefix in obj and context.object.name != obj:
                for mat, matPtr in ptr.material_slots.items():
                    if mat == materialName:
                        print("==> DEBUG : found clone : %s" % obj)
                        total = total + 1
        znode.isaComputerChange = True
        znode.outputs["Total"].default_value = total
        znode.userTotalProperty = total


myNewMenuCategory = {
    "SH_NEW_INPUT":
    ShaderNewNodeCategory("SH_NEW_INPUT", "Input", items=[
        NodeItem("ShaderNodeTexCoord"),
        NodeItem("ShaderNodeAttribute"),
        NodeItem("ShaderNodeLightPath"),
        NodeItem("ShaderNodeFresnel"),
        NodeItem("ShaderNodeLayerWeight"),
        NodeItem("ShaderNodeRGB"),
        NodeItem("ShaderNodeValue"),
        NodeItem("ShaderNodeTangent"),
        NodeItem("ShaderNodeNewGeometry"),
        NodeItem("ShaderNodeWireframe"),
        NodeItem("ShaderNodeObjectInfo"),
        NodeItem("ShaderNodeHairInfo"),
        NodeItem("ShaderNodeParticleInfo"),
        NodeItem("ShaderNodeCameraData"),
        NodeItem("ShaderNodeUVMap"),
        NodeItem("ShaderNodeUVAlongStroke", poll=nodeitems_builtins.line_style_shader_nodes_poll),
        NodeItem("NodeGroupInput", poll=nodeitems_builtins.group_input_output_item_poll),
        NodeItem("ShaderNodeObjectIndexer"),
    ]), }


def registerMenu():
    # remove, replace, add back the menu
    nodeitems_builtins.unregister()

    for index, nodeCat in enumerate(nodeitems_builtins.shader_node_categories):
        if nodeCat.identifier == "SH_NEW_INPUT":
            newMenu = myNewMenuCategory[nodeCat.identifier]
            nodeitems_builtins.shader_node_categories[index] = newMenu

    nodeitems_builtins.register()


def unregisterMenu():
    #  if this fails menus aren't loaded. this ensure that they can load
    try:
        nodeitems_builtins.unregister()
    except:
        pass
    #  reload the code dumps all changes
    importlib.reload(nodeitems_builtins)
    nodeitems_builtins.register()


def register():
    # bpy.utils.register_class(updateTotalOperator)
    bpy.utils.register_class(ObjectIndexer)
    bpy.types.Scene.SNOI_OREF = bpy.props.StringProperty()    # Shader Node Object Indexer - Object as Reference of group
    bpy.types.Scene.SNOI_OEXT = bpy.props.StringProperty()    # Shader Node Object Indexer - External Object
    try:
        registerMenu()
    except:
        unregisterMenu()
        raise
    bpy.app.handlers.frame_change_pre.append(pre_frame_change)
    print("==> registered")


def unregister():
    try:
        unregisterMenu()
        bpy.utils.unregister_class(ObjectIndexer)
        print("==> unregistered")
    except RuntimeError:
        raise


def pre_frame_change(scene):
    if scene.render.engine == 'CYCLES':
        # Scan materials to see if I have a custom node within any of the trees.
        for m in bpy.data.materials:
            if m.node_tree != None:
                for n in m.node_tree.nodes:
                    if n.bl_idname == 'CustomNodeType':
                        print(n.bl_idname)
                        # One of our custom nodes, let's update it.
                        # When we set the value that will trigger an update inside the node.
                        # Even if we change it to the same value it was.
                        v = n.some_value
                        n.some_value = v

if __name__ == "__main__":
    print("==> try to unregistering")
    # if hasattr(bpy.utils, "ObjectIndexer"):
    #    print("==> class ObjectIndexer registered")
    try:
        unregister()
    except RuntimeError:
        pass
    print("==> registering")
    register()
