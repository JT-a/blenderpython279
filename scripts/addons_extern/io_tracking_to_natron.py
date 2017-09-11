"""
Export Blender's tracking data for use in Natron.

Natron's native animation import/export writes keyframe data in the form
of columns, ie column 1 has all X location of first marker, 2 has Y location.
This script exports all markers on the active clip.

Licensed under Apache 2.0 license
https://www.apache.org/licenses/LICENSE-2.0

You are free to use this software free of charge for personal and commercial
purposes. Credit is not required, but appreciated.

Jeffrey "Italic_" Hoover
http://italic-anim.blogspot.com
"""

bl_info = {
    "name": "Tracker to Natron",
    "author": "Italic_",
    "version": (1, 2),
    "blender": (2, 76, 0),
    "location": "Clip Editor -> Tools",
    "description": "Export tracking data to Natron format",
    "category": "Import-Export"
}

import bpy
import os
from pathlib import Path


class NatronTrackExport(bpy.types.Operator):
    """Export all tracks on active clip to ascii file for Natron to read."""

    bl_idname = "track.export_to_natron"
    bl_label = "Export Track Data"
    bl_description = (
        "Export all tracks on active clip to ascii file for Natron to read"
    )
    bl_options = {'REGISTER'}

    def execute(self, context):
        activeClipName = [area.spaces[0].clip.name
                          for area in bpy.context.screen.areas
                          if area.type == 'CLIP_EDITOR' and
                          area.spaces[0].clip is not None]
        activeClip = bpy.data.movieclips[activeClipName[0]]
        activeClipDim = activeClip.size[:]

        blendDir = bpy.path.abspath("//")

        if blendDir == "":
            self.report({'ERROR'}, "Blend file is not saved")
            return {'CANCELLED'}

        markerLen = 0

        for i, ob in enumerate(activeClip.tracking.objects):
            track_dir = str(Path(blendDir) / "track_data" / ob.name)
            os.makedirs(track_dir, exist_ok=True)
            exportFile = os.path.join(track_dir, "%s.naa"
                                      % str(activeClipName).split("'")[1])
            openFile = open(exportFile, 'w+')

            markerLen = min(len(pt.markers) for j, pt in enumerate(ob.tracks)) - 1
            markerLists = [list() for _ in range(markerLen - 1)]

            print("\nTracking Object: %s" % ob.name)

            for j, pt in enumerate(ob.tracks):
                print("\tTrack: %i" % j)
                # print("\t\tMarkers: 1 - %i" % (range(enumerate(pt.markers))))

                for k, marker in enumerate(pt.markers):
                    if 0 < k < markerLen:
                        print("\t\tMarker: %i" % k)

                        natCoordX = "%.10f" % round(marker.co[0] * activeClipDim[0], 10)
                        natCoordY = "%.10f" % round(marker.co[1] * activeClipDim[1], 10)

                        markerLists[k - 1].append(natCoordX)
                        markerLists[k - 1].append(natCoordY)

            openFile.writelines("_".join(lines) + "\n"
                                for lines in markerLists)
            openFile.close()

        self.report({'INFO'}, "Export complete: %i frames" % (markerLen - 1))
        return {'FINISHED'}


class NatronTrackExportPanel(bpy.types.Panel):
    bl_label = "Natron"
    bl_space_type = "CLIP_EDITOR"
    bl_region_type = "TOOLS"
    bl_category = "Track"

    def draw(self, context):
        layout = self.layout
        layout.operator('track.export_to_natron')


def register():
    bpy.utils.register_class(NatronTrackExport)
    bpy.utils.register_class(NatronTrackExportPanel)


def unregister():
    bpy.utils.unregister_class(NatronTrackExportPanel)
    bpy.utils.unregister_class(NatronTrackExport)


if __name__ == "__main__":
    register()
