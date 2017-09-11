# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.69.x+ Smoke2Cycles-Addon
# --------------------------------------------------------------------------
#
# Author:
# HiPhiSch
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
#

# Credits go to the luxblend25 team. I used their smoke export code as the base 
# and learned a lot. Specifically the file export.volumes.py by Doug Hammond and neo2068
# was really helpful!
# Thank you!!

import bpy
from object_smoke2cycles import interface 
from object_smoke2cycles import create_mat
from traceback import print_exc

bl_info = {
    "name": "Smoke2Cycles",
    "description": "Convert BI smoke/fire simulations into a cycles 2.69.x compatible setup",
    "author": "HiPhiSch",
    "version": (0, 2),
    "blender": (2,69,8),
    "location": "View3D > Tools > Physics > Smoke2Cycles",
    "warning": "BETA, LIBLZO and LIBLZMA must be PRESENT on MacOS32 and Linux",
    "category": "Object",
    "tracker_url": "https://github.com/HiPhiSch/smoke2cycles/issues"
}

def register():       
    create_mat.register()
    interface.register()
    
def unregister():
    interface.unregister()    
    create_mat.unregister()
    
if __name__ == "__main__":  
    print('-' * 40)
    from traceback import print_tb
    try:
        unregister()
    except:
        print("WARNING: unregister failed")
        print_exc()
    register()