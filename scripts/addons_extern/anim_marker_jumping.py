# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Marker Jumping",
    "author": "Greg Zaal",
    "version": (1, 0),
    "blender": (2, 67, 1),
    "location": "Any timeline/animation editor/clip editor > ','/'.'",
    "description": "Simply allows you to go to the next/previous marker",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animation"}

import bpy

marker_areas = ['TIMELINE', 'GRAPH_EDITOR', 'DOPESHEET_EDITOR', 'NLA_EDITOR', 'SEQUENCE_EDITOR']


class MarkerPrev(bpy.types.Operator):
    "Go to the previous Marker"
    bl_idname = 'marker.prev'
    bl_label = 'Previous Marker'

    @classmethod
    def poll(cls, context):
        return context.area.type in marker_areas and context.scene.timeline_markers

    def execute(self, context):
        print("PREVIOUS!")
        markers = context.scene.timeline_markers
        current_frame = context.scene.frame_current
        possible_markers = []
        for m in markers:
            m.select = False
            if m.frame < current_frame:
                possible_markers.append(m.frame)
        if possible_markers:
            to_snap = min(possible_markers, key=lambda x: abs(x - current_frame))
            for m in markers:
                if m.frame == to_snap:
                    m.select = True
            context.scene.frame_current = to_snap
        return {'FINISHED'}


class MarkerNext(bpy.types.Operator):
    "Go to the next Marker"
    bl_idname = 'marker.next'
    bl_label = 'Next Marker'

    @classmethod
    def poll(cls, context):
        return context.area.type in marker_areas and context.scene.timeline_markers

    def execute(self, context):
        print("NEXT!")
        markers = context.scene.timeline_markers
        current_frame = context.scene.frame_current
        possible_markers = []
        for m in markers:
            m.select = False
            if m.frame > current_frame:
                possible_markers.append(m.frame)
        if possible_markers:
            to_snap = min(possible_markers, key=lambda x: abs(x - current_frame))
            for m in markers:
                if m.frame == to_snap:
                    m.select = True
            context.scene.frame_current = to_snap
        return {'FINISHED'}


def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("marker.next")
    layout.operator("marker.prev")

classes = [MarkerPrev, MarkerNext]
addon_keymaps = []


def register():
    # add operator
    for c in classes:
        bpy.utils.register_class(c)

    # add keymap entry
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name="Animation")
    kmi = km.keymap_items.new("marker.prev", 'COMMA', 'PRESS')
    kmi = km.keymap_items.new("marker.next", 'PERIOD', 'PRESS')
    addon_keymaps.append(km)
    bpy.types.TIME_MT_marker.append(menu_func)
    bpy.types.SEQUENCER_MT_marker.append(menu_func)
    bpy.types.NLA_MT_marker.append(menu_func)
    bpy.types.DOPESHEET_MT_marker.append(menu_func)
    bpy.types.GRAPH_MT_marker.append(menu_func)


def unregister():
    # remove operator
    for c in classes:
        bpy.utils.unregister_class(c)

    # remove keymap entry
    for km in addon_keymaps:
        bpy.context.window_manager.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()
    bpy.types.TIME_MT_marker.remove(menu_func)
    bpy.types.SEQUENCER_MT_marker.remove(menu_func)
    bpy.types.NLA_MT_marker.remove(menu_func)
    bpy.types.DOPESHEET_MT_marker.remove(menu_func)
    bpy.types.GRAPH_MT_marker.remove(menu_func)

if __name__ == "__main__":
    register()
