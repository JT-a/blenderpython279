#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  The Original Code is Copyright (C) 2012 Dan Wheeler   ###
#  All rights reserved.
#
#  The Original Code is: all of this file.
#

'''
Created on Jan 17, 2012

@author: Quizkid
'''

# if __name__ == '__main__':
#    pass

import bpy
from bpy.utils import register_module, unregister_module
import datetime
import logging

#--- ### Header
bl_info = {
    "name": "UVDistribute",
    "author": "Quizkid",
    "version": (0, 4, 0),
    "blender": (2, 6, 3),
    "api": 46461,
    "location": "UVEditor>UVs>Weld/Align>UVDistribute",
    "category": "UV",
    "description": "Evenly distributes UVs to along Horizontal and Vertical",
    "warning": "Beta",
    "wiki_url": "",
    "tracker_url": ""
}

#--- ### Operator


class UVDistribute(bpy.types.Operator):
    '''Evenly distributes selected UV coordinates along Horizontal and Vertical.'''
    bl_idname = "mesh.uvdistribute"
    bl_label = "UVDistribute"
    bl_description = "Distributes UV coordinates Vertically and Horizontally."

    #--- Blender interface methods
    @classmethod
    def poll(cls, context):
        # print("context.mode %s" % context.mode)
        # Specials are not available in Object Mode
        return (context.mode == 'EDIT_MESH')

    def invoke(self, context, event):
        # input validation: are there any edges selected?
        selected = context.selected_objects
        if len(selected) > 0:
            return {self.execute(context)}
        else:
            self.report(type={'ERROR'}, message="No objects selected")
            return {'CANCELLED'}

    def execute(self, context):
        uvDistribute(self, context.active_object)
        return ('FINISHED')


def menu_draw(self, context):
    self.layout.operator_context = 'INVOKE_REGION_WIN'
    self.layout.operator(UVDistribute.bl_idname, "UVDistribute")


def uvDistribute(self, sc):
    # put into Object mode
    bpy.ops.object.editmode_toggle()
    mesh = sc.data
    logger = logging.getLogger()
    # uncomment the following line (and comment out the NullerHandler line) to write logging to the file
    # hdlr = logging.FileHandler('/tmp/pythonlog3.log', mode='a')
    hdlr = logging.NullHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    logger.info("-" * 80)
    logger.info("Run begun: %s \n", datetime.datetime.today())

    # Creating a blank dictionary
    d = {}

    uv_layer = mesh.uv_layers.active.data

    logger.info("uv_layer: %r" % uv_layer)
    uvSelectedCount = 0
    uvNotSelectedCount = 0

    for poly in mesh.polygons:
        # print("Polygon index: %d, length: %d" % (poly.index, poly.loop_total))
        # range is used here to show how the polygons reference loops,
        # for convenience 'poly.loop_indices' can be used instead.
        if poly.select:
            for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                # if the uv point is selected:
                if uv_layer[loop_index].select:
                    uvSelectedCount += 1
                    print("    Vertex: %d" % mesh.loops[loop_index].vertex_index)
                    print("    UV: %r" % uv_layer[loop_index].uv)
                    selectVal = ("False", "True")[uv_layer[loop_index].select]
                    print("      select: %r" % selectVal)
                    myVec = tuple(uv_layer[loop_index].uv)
                    # uv_layer[loop_index].uv = myVec
                    # print("        -- New Vector" + myVec)
                    if myVec not in d:
                        # create new UV record
                        d[myVec] = []
                        # add blender indices that had those UV values
                        tcoord = poly.index, loop_index - poly.loop_start
                        d[myVec].append(tcoord)
                else:
                    uvNotSelectedCount += 1

    logger.info("Distinct selected UV point count %f out of %f selected and %f NOT selected\n", len(d), uvSelectedCount, uvNotSelectedCount)

    if len(d) < 3:
        self.report(type={'ERROR'}, message="Minimum of 3 UVs must be selected to distribute.")
        logger.removeHandler(hdlr)
        # put back into edit mode
        bpy.ops.object.editmode_toggle()
        return

    logger.info("  d has: %s" % d)

    # at this point, each record in d looks like this:
    # (2.5, 3.2), [(1, 5), (2, 9), (13, 19)]
    # where there is a UV coordinate tuple as a key, and an
    # array of tuples, representing the poly.index and loop_index locations in the array above
    # where these tuples are found

    # Determine minimums and maximums in X and Y directions

    minx = 0
    maxx = 0
    miny = 0
    maxy = 0

    for k in d.keys():
        if minx == 0 or k[0] < minx:
            minx = k[0]
        if maxx == 0 or k[0] > maxx:
            maxx = k[0]
        if miny == 0 or k[1] < miny:
            miny = k[1]
        if maxy == 0 or k[1] > maxy:
            maxy = k[1]

    logger.info("  minx: %f", minx)
    logger.info("  maxx: %f", maxx)
    logger.info("  miny: %f", miny)
    logger.info("  maxy: %f", maxy)

    deltaX = maxx - minx
    deltaY = maxy - miny

    # set up a dict so that the ordinal position can be quickly looked up
    sortedX = []
    sortedY = []
    for k in d.keys():
        sortedX.append(k[0])
        sortedY.append(k[1])

    sortedX.sort()
    sortedY.sort()

    xOrdDict = {}
    yOrdDict = {}
    i = 0

    for x in sortedX:
        if x not in xOrdDict:
            xOrdDict[x] = i
            i = i + 1
    i = 0
    for y in sortedY:
        if y not in yOrdDict:
            yOrdDict[y] = i
            i = i + 1

    logger.info("  sortedX has: %s" % sortedX)
    logger.info("  sortedY has: %s \n" % sortedY)
    logger.info("  xOrdDict has: %s" % xOrdDict)
    logger.info("  yOrdDict has: %s \n" % yOrdDict)
    logger.info("  deltaX is: %f" % deltaX)
    logger.info("  deltaY is: %f \n" % deltaY)

    uvDistCount = 0
    uvSelectedCount = 0
    uvNotSelectedCount = 0

    if 1 == 1:
        # write back to original UVs
        mesh = sc.data
        uv_layer = mesh.uv_layers.active.data
        for poly in mesh.polygons:
            # print("Polygon index: %d, length: %d" % (poly.index, poly.loop_total))
            # range is used here to show how the polygons reference loops,
            # for convenience 'poly.loop_indices' can be used instead.
            if poly.select:
                for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
                    # if the uv point is selected:
                    if uv_layer[loop_index].select:
                        uvSelectedCount += 1
                        myVec = tuple(uv_layer[loop_index].uv)
                        myU = myVec[0]
                        myV = myVec[1]
                        # default values
                        newX = myU
                        newY = myV
                        # calculate new X coord
                        if len(xOrdDict) > 1:
                            newX = (xOrdDict[myU] / (len(xOrdDict) - 1)) * deltaX + minx
                        if len(yOrdDict) > 1:
                            newY = (yOrdDict[myV] / (len(yOrdDict) - 1)) * deltaY + miny

                        logger.info('moving myU,myV %f,%f to newX,newY %f,%f for poly.index %f  loop_index %f ', myU, myV, newX, newY, poly.index, loop_index - poly.loop_start)

                        if myVec in d:
                            # rewrite new location
                            uv_layer[loop_index].uv = [newX, newY]
                            uvDistCount += 1
                    else:
                        uvNotSelectedCount += 1

        logger.info("UVs distributed %f out of %f selected and %f unselected", uvDistCount, uvSelectedCount, uvNotSelectedCount)

        self.report(type={'INFO'}, message=("UVs distributed (" + str(uvDistCount) + ")"))

    else:
        logger.info('Not updating UV data, updating routine disabled.')

    logger.info("Run completed: %s \n", datetime.datetime.today())

    logger.removeHandler(hdlr)
    # put back into edit mode
    bpy.ops.object.editmode_toggle()


#--- ### Register
def register():
    # run in eval because Eclipse can't see the VIEW3D...
    # eval('bpy.types.VIEW3D_MT_edit_mesh_specials.prepend(menu_draw)')
    eval('bpy.types.IMAGE_MT_uvs_weldalign.prepend(menu_draw)')
    register_module(__name__)


def unregister():
    # run in eval because Eclipse can't see the VIEW3D...
    # eval('bpy.types.VIEW3D_MT_edit_mesh_specials.remove(menu_draw)')
    eval('bpy.types.IMAGE_MT_uvs_weldalign.remove(menu_draw)')
    unregister_module(__name__)
#--- ### Main code
if __name__ == '__main__':
    register()
