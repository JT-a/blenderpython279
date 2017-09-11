import bpy

from ..utils import structures as st
from ..utils import vawm


def BLI_rctf_isect(src1, src2, dest=None):
    xmin = max(src1[0], src2[0])
    xmax = min(src1[1], src2[1])
    ymin = max(src1[2], src2[2])
    ymax = min(src1[3], src2[3])
    if xmax >= xmin and ymax >= ymin:
        if dest:
            dest[:] = [xmin, xmax, ymin, ymax]
        return True
    else:
        if dest:
            dest[:] = [0, 0, 0, 0]
        return False


def BLI_rctf_isect_pt(rect, x, y):
    return rect[0] <= x <= rect[1] and rect[2] <= y <= rect[3]


def visible_node(space_node, rect):
    """editors/space_node/node_edit.c:819 visible_node()
    :param space_node:
    :param rect:
    :rtype bool:
    """
    node = None
    for node in space_node.edit_tree[::-1]:
        n = st.bNode.cast(node)
        totrect = [n.totr.xmin, n.totr.xmax, n.totr.ymin, n.totr.ymax]
        if BLI_rctf_isect(totrect, rect, None):
            break
    return node


def node_find_indicated_socket(space_node, cursor, in_out=()):
    """editors/space_node/node_edit.c:1061 node_find_indicated_socket()

    :param space_node:
    :param cursor: (Event.mouse_x, Event.mouse_y)
    :param in_out: 'in', 'out'
    :return:
    """

    in_out = tuple(in_out)
    NODE_SOCKSIZE = vawm.widget_unit() * 0.25
    x, y = cursor
    for node in space_node.edit_tree.nodes:
        f = NODE_SOCKSIZE + 4
        rect = [x - f, x + f, y - f, y + f]
        if not node.hide:
            if in_out == ('in',):
                rect[1] += NODE_SOCKSIZE
                rect[0] -= NODE_SOCKSIZE * 4
            elif in_out == ('out',):
                rect[1] += NODE_SOCKSIZE * 4
                rect[0] -= NODE_SOCKSIZE
        sockets = []
        if 'in' in in_out:
            sockets.extend(node.inputs)
        if 'out' in in_out:
            sockets.extend(node.outputs)
        for socket in sockets:
            if not socket.hide:
                sock = st.bNodeSocket.cast(socket)
                if BLI_rctf_isect_pt(rect, sock.locx, sock.locy):
                    if node == visible_node(space_node, rect):
                        return node, socket
    return None, None


###############################################################################
# 以降、ゴミ
###############################################################################
from collections import defaultdict
import bpy
import nodeitems_utils
from ..utils import vaprops


###############################################################################
# Tree
###############################################################################
class CustomNodeTree(bpy.types.NodeTree):
    bl_idname = 'CustomTree'
    bl_label = 'Custom Node Tree'
    bl_icon = 'NODETREE'


###############################################################################
# Socket
###############################################################################
class CustomSocket(bpy.types.NodeSocket):
    bl_idname = 'CustomSocket'
    bl_label = 'Custom Socket'

    parent_type = vaprops.bl_prop_to_py_prop(
        bpy.types.Object.bl_rna.properties['parent_type'])
    parent_vertices = vaprops.bl_prop_to_py_prop(
        bpy.types.Object.bl_rna.properties['parent_vertices'])
    use_connect = vaprops.bl_prop_to_py_prop(
        bpy.types.EditBone.bl_rna.properties['use_connect'])

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        object_type = ''
        if self.is_linked:
            layout.prop(self, 'parent_type', text='')
        else:
            layout.label(text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 1.0, 0.0, 1.0)


class CustomEmptySocket(bpy.types.NodeSocket):
    bl_idname = 'CustomEmptySocket'
    bl_label = 'Custom Empty Socket'

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        layout.label(text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 1.0, 0.0, 1.0)


###############################################################################
# Node
###############################################################################
class _CustomNode:
    @classmethod
    def poll(cls, node_tree):
        return node_tree.bl_idname == CustomNodeTree.bl_idname


class CustomNode(bpy.types.Node, _CustomNode):
    bl_idname = 'CustomNode'
    bl_label = 'Custom Node'
    bl_icon = 'QUESTION'

    # ('CUSTOM', 'UNDEFINED', 'FRAME', 'GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT', 'REROUTE')
    # bl_static_type = 'CUSTOM'

    # bl_width_default = 100

    object_type = vaprops.bl_prop_to_py_prop(
        bpy.types.Object.bl_rna.properties['type'])

    def init(self, context):
        self.inputs.new(CustomSocket.bl_idname, 'Parent')

        self.outputs.new(CustomSocket.bl_idname, 'Socket A')
        self.outputs.new(CustomSocket.bl_idname, 'Socket B')

    # # Copy function to initialize a copied node from an existing one.
    # def copy(self, node):
    #     print("Copying from node ", node)
    #
    # # Free function to clean up on removal.
    # def free(self):
    #     print("Removing node ", self, ", Goodbye!")
    #
    # # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        # layout.label("Node settings")
        layout.prop(self, 'object_type')

    # # Detail buttons in the sidebar.
    # # If this function is not defined, the draw_buttons function is used instead
    # def draw_buttons_ext(self, context, layout):
    #     layout.prop(self, "myFloatProperty")
    #     # myStringProperty button will only be visible in the sidebar
    #     layout.prop(self, "myStringProperty")
    #
    # # Optional: custom label
    # # Explicit user label overrides this, but here we can define a label dynamically
    # def draw_label(self):
    #     return "I am a custom node"

    def update(self):
        # print(self.name, 'update')
        # for socket in self.inputs:
        #     print(socket, socket.enabled)
        pass

    def insert_link(self, link):
        # print(self.name, link)
        pass


###############################################################################
# Group Node
###############################################################################
class CustomGroupNode(bpy.types.Node, _CustomNode):
    bl_idname = 'CustomGroupNode'
    bl_label = 'Custom Group Node'
    bl_icon = 'QUESTION'

    bl_static_type = 'GROUP'
    # type = 'GROUP'

    def update_func(self, context):
        # TODO: 同期
        pass

    group_name = bpy.props.StringProperty(
        name='Group',
        description='Node tree name',
        update=update_func
    )

    def init(self, context):
        self.outputs.new(CustomEmptySocket.bl_idname, 'Input')
        self.outputs.new(CustomEmptySocket.bl_idname, 'Input')
        self.outputs.new(CustomEmptySocket.bl_idname, 'Input')
        self.outputs.new('NodeSocketFloatAngle', 'Input')

    def draw_buttons(self, context, layout):
        layout.prop_search(self, 'group_name', bpy.data, 'node_groups')
        for socket in self.outputs:
            print(socket.name, socket.identifier, socket.bl_idname)
            print(dir(socket))


class CustomGroupNodeInput(bpy.types.Node, _CustomNode):
    bl_idname = 'CustomGroupNodeInput'
    bl_label = 'Custom Group Input'
    bl_icon = 'QUESTION'

    bl_static_type = 'GROUP_INPUT'

    def init(self, context):
        self.outputs.new(CustomEmptySocket.bl_idname, 'Input')

    def insert_link(self, link):
        socket = link.from_socket
        if self.outputs and self.outputs[-1] == socket:
            self.outputs.new(CustomEmptySocket.bl_idname, 'Input')
        # TODO: 同期


class CustomGroupNodeOutput(bpy.types.Node, _CustomNode):
    bl_idname = 'CustomGroupNodeOutput'
    bl_label = 'Custom Group Output'
    bl_icon = 'QUESTION'

    bl_static_type = 'GROUP_OUTPUT'

    def init(self, context):
        self.inputs.new(CustomEmptySocket.bl_idname, 'Output')

    def insert_link(self, link):
        socket = link.to_socket
        if self.inputs and self.inputs[-1] == socket:
            self.inputs.new(CustomEmptySocket.bl_idname, 'Output')
        # TODO: 同期


class NODE_OT_group_make_custom(bpy.types.Operator):
    bl_idname = 'node.group_make_custom'
    bl_label = 'Make Group'

    @classmethod
    def poll(cls, context):
        area = context.area
        if area and area.type == 'NODE_EDITOR':
            space = area.spaces.active
            if (space.node_tree and
                    space.node_tree.bl_idname == CustomNodeTree.bl_idname):
                return True
        return False

    def execute(self, context):
        space = context.area.spaces.active
        node_tree = space.node_tree
        if not node_tree:
            return {'CANCELLED'}
        if node_tree.bl_idname != CustomNodeTree.bl_idname:
            return {'CANCELLED'}

        # 選択ノードが無ければキャンセル
        selected_nodes = [node for node in node_tree.nodes if node.select]
        deselected_nodes = [node for node in node_tree.nodes
                            if not node.select]
        if not selected_nodes:
            return {'CANCELLED'}

        # 選択ノードが有効なタイプかテスト
        for node in selected_nodes:
            if node.bl_idname in {CustomGroupNodeInput, CustomGroupNodeOutput}:
                return {'CANCELLED'}

        # 未選択ノードのインプット・アウトプット両方に選択ノードが
        # 接続されているならキャンセル
        flags = defaultdict(int)
        for link in node_tree.links:
            if link.from_node.select:
                flags[link.to_node] |= 1
            if link.to_node.select:
                flags[link.from_node] |= 2
        for node in node_tree.nodes:
            if not node.select and flags[node] == 3:
                return {'CANCELLED'}

        # 新規tree
        group_tree = bpy.data.node_groups.new(name='Group',
                                              type=CustomNodeTree.bl_idname)
        input_node = group_tree.nodes.new(type=CustomGroupNodeInput.bl_idname)
        output_node = group_tree.nodes.new(
            type=CustomGroupNodeOutput.bl_idname)

        # 現在のtreeにGroupNodeを追加
        group_node = node_tree.nodes.new(type=CustomGroupNode.bl_idname)

        # Yの上方向からの順に並び替える
        selected_nodes.sort(key=lambda n: n.location[1], reverse=True)
        deselected_nodes.sort(key=lambda n: n.location[1], reverse=True)

        # ノードの作成
        node_dict = {}
        for node in selected_nodes:
            new_node = group_tree.nodes.new(type=node.blidname)
            node_dict[node] = new_node
            node_dict[new_node] = node
            # ソケットの作り直し
            new_node.inputs.clear()
            for socket in node.inputs:
                new_node.inputs.new(type=socket.bl_idname, name=socket.name,
                                    identifier=socket.identifier)
            new_node.inputs.clear()
            for socket in node.outputs:
                new_node.outputs.new(type=socket.bl_idname, name=socket.name,
                                     identifier=socket.identifier)
            # 属性の複製
            for attr in dir(node):
                try:
                    if node.is_property_set(attr):
                        setattr(new_node, attr, getattr(node, attr))
                except:
                    pass

        # 選択済み同士のリンク
        input_links = []
        output_links = []
        for link in node_tree.links:
            n1 = link.from_node
            n2 = link.to_node
            s1 = link.from_socket
            s2 = link.to_socket
            g1 = node_dict[n1]
            g2 = node_dict[n2]
            if n1.select and n2.select:
                i1 = list(n1.outputs).index(s1)
                i2 = list(n2.inputs).index(s2)
                group_tree.links.new(g1.outputs[i1], g2.inputs[i2])
            elif n1.select:
                output_links.append(link)
            elif n2.select:
                input_links.append(link)

        # ソート
        def input_links_sort_func(link):
            node = link.from_node
            socket = link.from_socket
            return -node.location[1], list(node.outputs).index(socket)

        def output_links_sort_func(link):
            node = link.to_node
            socket = link.to_socket
            return -node.location[1], list(node.inputs).index(socket)

        input_links.sort(key=input_links_sort_func)
        output_links.sort(key=output_links_sort_func)

        # input側のリンク
        sockets = []
        for link in input_links:
            sockets.append(link.to_socket)
        sockets = sorted(sockets, key=sockets.index)
        for socket in sockets:
            input_node.outputs.new(type=CustomEmptySocket.bl_idname,
                                   name=socket.name)
            group_node.inputs.new(type=socket.bl_idname, name=socket.name)
        for link in input_links:
            i = sockets.index(link.to_socket)
            node_tree.links.new(link.from_socket, group_node.inputs[i])
            j = list(link.to_node.inputs).index(link.to_socket)
            group_tree.links.new(
                input_node.outputs[i], node_dict[link.to_node].inputs[j])

        # output側のリンク
        sockets = []
        for link in output_links:
            sockets.append(link.from_socket)
        sockets = sorted(sockets, key=sockets.index)
        for socket in sockets:
            output_node.inputs.new(type=CustomEmptySocket.bl_idname,
                                   name=socket.name)
            group_node.outputs.new(type=socket.bl_idname, name=socket.name)
        for link in output_links:
            i = sockets.index(link.from_socket)
            node_tree.links.new(group_node.outputs[i], link.to_socket)
            j = list(link.from_node.outputs).index(link.from_socket)
            group_tree.links.new(
                node_dict[link.from_node].outputs[j], output_node.inputs[i])

        # リンクの削除
        for link in input_links:
            node_tree.links.remove(link)
        for link in output_links:
            node_tree.links.remove(link)

        # ノードの削除
        for node in selected_nodes:
            node_tree.nodes.remove(node)

        # group_nameを設定
        group_node.group_name = group_tree.name

        return {'FINISHED'}


###############################################################################
# Category
###############################################################################
# Node Categories
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
class MyNodeCategory(nodeitems_utils.NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == CustomNodeTree.bl_idname

# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory('OBJECTNODES', 'Object Nodes', items=[
        # our basic node
        nodeitems_utils.NodeItem(CustomNode.bl_idname),
        nodeitems_utils.NodeItem(CustomGroupNode.bl_idname),
    ]),
    MyNodeCategory('BONENODES', 'Bone Nodes', items=[
        # the node item can have additional settings,
        # which are applied to new nodes
        # NB: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()
        nodeitems_utils.NodeItem(
            CustomNode.bl_idname,
            label='Node A',
            # settings={
            #     'myStringProperty': repr('Lorem ipsum dolor sit amet'),
            #     'myFloatProperty': repr(1.0),
            # }
        ),
        nodeitems_utils.NodeItem(
            CustomNode.bl_idname,
            label='Node B',
            # settings={
            #     'myStringProperty': repr('consectetur adipisicing elit'),
            #     'myFloatProperty': repr(2.0),
            # }
        ),
    ]),
]


###############################################################################
# Operator
###############################################################################
class NODE_OT_hierarchy(bpy.types.Operator):
    bl_idname = 'node.hierarchy'
    bl_label = 'Init Hierarchy'

    @classmethod
    def poll(cls, context):
        area = context.area
        if area and area.type == 'NODE_EDITOR':
            space = area.spaces.active
            if (space.node_tree and
                    space.node_tree.bl_idname == CustomNodeTree.bl_idname):
                return True
        return False

    def execute(self, context):
        space = context.area.spaces.active
        node_tree = space.node_tree
        if not node_tree:
            return {'CANCELLED'}
        if node_tree.bl_idname != CustomNodeTree.bl_idname:
            return {'CANCELLED'}

        node_tree.nodes.clear()

        x = y = 0
        margin = 10
        width = 100
        for ob in context.scene.objects:
            node = node_tree.nodes.new(CustomNode.bl_idname)
            node.hide = True
            node.name = node.label = ob.name
            node.width = node.width_hidden = width
            node.location = x, y
            y -= vawm.widget_unit() + margin
        # node_tree.interface_update(context)
        # x = y = 0
        # margin = 5
        # for node in node_tree.nodes:
        #     node.location = x, y
        #     y -= node.height + margin
        # print(node.height)

        n1, n2, n3 = node_tree.nodes
        node_tree.links.new(n1.inputs[0], n2.outputs[0], False)
        node_tree.links.new(n1.inputs[0], n3.outputs[0], False)

        # node_tree.interface_update(context)
        # for node in node_tree.nodes:
        #     n = st.bNode.cast(node)
        #     totrect = [n.totr.xmin, n.totr.xmax, n.totr.ymin, n.totr.ymax]
        #     print(totrect)

        return {'FINISHED'}


"""
group_make
group_edit
group_ungroup
group_separate
group_insert

node_group.c: 603:
    node_group_make_insert_selected()
"""

classes = [
    CustomSocket,
    CustomEmptySocket,

    CustomNode,

    CustomGroupNode,
    CustomGroupNodeInput,
    CustomGroupNodeOutput,

    CustomNodeTree,

    NODE_OT_hierarchy,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    for cls in classes[::-1]:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
