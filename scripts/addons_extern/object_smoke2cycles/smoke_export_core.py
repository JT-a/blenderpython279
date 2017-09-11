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
import os
import ctypes as ct
import gc
import struct
import mathutils as mu

# exception classes
class EUnsuportedPlatform(Exception):
    pass
class ELoadCompressionLibraryFailed(Exception):
    pass
class ENoDomain(Exception):
    pass
class ENotBaked(Exception):
    pass
    

# utility function:
def is_smoke_domain(obj):
    """Determine if an object is a smoke domain object"""
    if obj is None:
        return False
    
    for m in obj.modifiers:
        if m.name == 'Smoke':
            if m.smoke_type == 'DOMAIN':
                return True
    
    return False

# classes:
class LZx_Reader(object):
    """Reads binary data from lzx_stream"""
    
    dlls = dict()

    search_paths = {
        "LZO": {
            "mac" : [ [], "liblzo2.dylib" ],
            "win" : [ ["lzo.dll"], "lzo.dll" ],
            "linux" : [ ["/usr/lib/liblzo2.so", "/usr/lib/liblzo2.so.2"], "liblzo2.so" ] },
        "LZMA": {
            "mac" : [ [], "iblzmadec.dylib" ],
            "win" : [ ["lzma.dll"], "lzma.dll" ],
            "linux" : [ ["/usr/lib/liblzma.so", "/usr/lib/liblzma.so.2"], "liblzma.so" ] }
        }
    
    @classmethod
    def platform(cls):
        """gets the correct os dependent path for the dynamic libraries"""
        platform = bpy.app.build_platform.decode('utf-8')
        pl_split = platform.split(':')
        os_type = pl_split[0].lower()
        if os_type == "windows":
            os_type = "win" 
        elif os_type == "linux":
            os_type = "linux"
        elif os_type == "darwin":
            os_type = "mac"
        else:
            raise EUnsupportedPlatform("Platform type: %s not supported!" % os_type)
        
        arch = "x86"
        if len(pl_split) > 1:
            if pl_split[1].lower() == "64bit":
                arch = "x64"
        
        return os_type, arch
    
    @classmethod
    def search_path_iter(cls, lib):
        """iterate over all possible search paths"""
        os_type, arch = cls.platform()

        if not lib in cls.search_paths:
            return
        
        for direct_path in cls.search_paths[lib][os_type][0]:
            yield direct_path
                
        sub_path = os.path.join("addons", "object_smoke2cycles", "libs", "%s_%s" % (os_type, arch), cls.search_paths[lib][os_type][1])
        
        yield bpy.utils.user_resource('SCRIPTS', sub_path)
        
        path2 =list( os.path.split(bpy.app.binary_path)[:-1] )
        path2 += ["%d.%02d" % (bpy.app.version[0], bpy.app.version[1])] + ["scripts"]
        path2 = os.path.join(*path2)
        yield os.path.join(path2, sub_path)
        
        return
    
    @classmethod 
    def get_lzx(cls,lib):
        """initializes the LZO/LZMA library"""        
        if not lib in {"LZO", "LZMA"}:
            raise Exception["invalid library type"]

        if not lib in cls.dlls:
            cls.dlls[lib] = None
            
            print ("initializing %s" % lib)
            
            for dll_path in cls.search_path_iter(lib):
                print ("...trying: %s" % dll_path)
                try:
                    dll = ct.cdll.LoadLibrary(dll_path)
                    cls.dlls[lib] = dll
                    break
                except:
                    pass
                
            if not cls.dlls[lib] is None:
                print("%s initialized successfully!" % lib)
            else:
                print("%s could not be initialized!" % lib)
    
        return cls.dlls[lib]  
    
    @classmethod 
    def decompress_floats(cls, compressed, no_floats, lib, optional=None):
        """decompresses a number of floats with the given algorithm"""
        dll = cls.get_lzx(lib)
        
        if dll is None:
            raise ELoadCompressionLibraryFailed("Could not load %s library!" % lib)

        # create buffer
        out_buffer = (ct.c_float * no_floats)()
        out_bytes = ct.c_uint()
    
        # call library
        if lib == "LZO":
            dll.lzo1x_decompress(compressed, ct.c_uint(len(compressed)), ct.byref(out_buffer), ct.byref(out_bytes), None)
        elif lib == "LZMA":
            dll.LzmaUncompress(ct.byref(out_buffer), ct.byref(out_bytes), \
            compressed, ct.byref(ct.c_uint(len(compressed))), \
            optional, ct.c_uint(len(optional)))
            
        # create python list
        res = list(out_buffer)
        del out_buffer # make sure memory is cleaned up here
        gc.collect() # force garbage collection here (avoid out of mem)
        return res

class SmokeExporter(object):
    """Exports smoke/fire data from pcache file"""

    @staticmethod
    def get_smoke_domain(domain_obj):
        """return the domain settings"""
        if domain_obj is None:
            return None
        
        for m in domain_obj.modifiers:
            if m.name == 'Smoke':
                if m.smoke_type == 'DOMAIN':
                    return m.domain_settings
        return None    
    
    
    def __init__(self, domain_obj, frame):
        # input
        frm_old = bpy.context.scene.frame_current
        try:
            bpy.context.scene.frame_set(frame)
            
            bpy.context.scene
            domain = self.get_smoke_domain(domain_obj)
            if domain is None:
                raise ENoDomain("Not a valid smoke domain object!")                    
            
            self.__smokecache = domain.point_cache
            self.__is_high_res = domain.use_high_resolution
            self.__high_res_amp = domain.amplify + 1
            self.__domain_dim = domain_obj.dimensions[:]
            self.__bb_v0 = mu.Vector(domain_obj.bound_box[0])
            self.__bb_v6 = mu.Vector(domain_obj.bound_box[6])  
            self.__wm = domain_obj.matrix_world.copy()      
            self.__frame = frame
            self.__maxres = domain.resolution_max
            self.__domain = domain
            self.__domain_obj_name = domain_obj.name
        
            # smoke file    
            self.__pcache = None
            
            self.__cell_count = 0
            self.__cell_count_high = 0
        
            # output
            self.__smoke = None
            self.__fire = None
            self.cache_opt = None
            
            self.__pcache_extracted = False           
        finally:
            bpy.context.scene.frame_set(frm_old)
            
    @property
    def smoke(self):
        """get the smoke density voxel information"""
        # do the magic
        if not self.__pcache_extracted:
            self.__extract_pcache()
        return self.__smoke

    @property
    def fire(self):
        """get the fire voxel information"""
        # do the magic
        if not self.__pcache_extracted:
            self.__extract_pcache()
        return self.__fire
        
    @property
    def adaptive_bbox_wm(self):
        """return the matrix_world of the adaptive domain"""
        v1 = self.__bb_v0
        v2 = self.__bb_v6
        
        # location
        wm = mu.Matrix.Translation(0.5 * (v1 + v2))
        # scale
        scl = 0.5 * (v2 - v1)
        for i in range(3):
            wm[i][i] = abs(scl[i])
        # transform in object coordinates
        return self.__wm * wm
     
    @property
    def adaptive_bbox_inv_scale(self):
        """return the inverse scale of the adaptive domain box"""
        scl = 0.5 * (self.__bb_v6 - self.__bb_v0)
        for i in range(3):
            scl[i] = 0.0 if scl[i] == 0.0 else 1.0 / scl[i]   
        return scl
        
    @property    
    def resolution(self):
        """get x, y, z voxel resolution for smoke / fire"""
        if not self.__pcache_extracted:
            self.__extract_pcache(header_only=True)
        
        # no data    
        if self.__cell_count == 1:
            return [1, 1, 1]
            
        if not self.cache_opt is None:
            res = [self.cache_opt["res_x"], \
                self.cache_opt["res_y"], self.cache_opt["res_z"]]
            if self.__is_high_res:
                res = [r *  self.__high_res_amp for r in res]
            return res
        else:
            max_dim = max(self.__domain_dim)    
            return [int(round(self.__maxres *self.__domain_dim[i]/max_dim)) for i in range(3)]
        
    @property
    def smoke_domain(self):
        """return the smoke domain"""
        return self.__domain
    
    
    @property
    def flame_temp_span(self):
        """return the flame minimum and maximum temperature"""
        return self.__domain.flame_ignition * 1000.0, self.__domain.flame_max_temp * 1000.0
        
    def __pcache_read_compression_header(self):
        """read the header for a value block"""
        result = dict()
        
        result["compression"] = struct.unpack("B", self.__pcache.read(1))[0]
        if result["compression"] > 2:
            raise Exception("Unknown compression type %d used" % result["compression"])
        
        if result["compression"] > 0:
            result["comp_size"] = struct.unpack("I", self.__pcache.read(4))[0]
        
        result["compression"] = (None, "LZO", "LZMA")[result["compression"]]
                              
        return result

    def __pcache_skip_part(self, use_high_res=False):
        """skip over one entry"""
        if use_high_res:
            cell_count = self.__cell_count_high
        else:
            cell_count = self.__cell_count
        # read compression header
        comp_header = self.__pcache_read_compression_header()

        if comp_header["compression"] is None:
            # skip uncompressed data
            self.__pcache.seek(cell_count * ct.sizeof(ct.c_float), 1)
        else:
            # skip compressed datax
            self.__pcache.seek(comp_header["comp_size"], 1)
            # skip lzma properties if required
            if comp_header["compression"] == "LZMA":
                prop_size = struct.unpack("I", self.__pcache.read(4))[0]
                self.__pcache.seek(prop_size, 1)
    
    def __pcache_read_part(self, use_high_res=False):
        """read one entry"""
        # smoke/fire -> switch to high res if required
        if use_high_res:
            cell_count = self.__cell_count_high
        else:
            cell_count = self.__cell_count
        # read compression header
        comp_header = self.__pcache_read_compression_header()
        
        if comp_header["compression"] is None:
            # read uncompressed data
            return struct.unpack("%df" % self.__cell_count, \
                self.__pcache.read( cell_count * ct.sizeof(ct.c_float) ) )
        
        # read compressed data
        compressed = self.__pcache.read(comp_header["comp_size"])

        # read lzma properties if required
        optional = None
        if comp_header["compression"] == "LZMA":
            prop_size = struct.unpack("I", self.__pcache.read(4))[0]
            optional = self.__pcache.read(prop_size)
        
        # unpack compressed data
        return LZx_Reader.decompress_floats(\
            compressed, cell_count, comp_header["compression"], optional)
        
    
    def __extract_pcache(self, header_only=False): 
        """Extract data from binary pcache file"""
        SM_ACTIVE_HEAT = (1<<0) 
        SM_ACTIVE_FIRE = (1<<1)
        SM_ACTIVE_COLORS = (1<<2)
        SM_ACTIVE_COLOR_SET	= (1<<3)               
        
        smokecache = self.__smokecache
        
        # check for bake
        if not smokecache.is_baked:
            raise ENotBaked("Export error: bake first!")
            
        # determine binary file name
        cachefilepath = os.path.join(
            os.path.splitext(os.path.dirname(bpy.data.filepath))[0],
                "blendcache_" + os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        )
        prefix = smokecache.name if (smokecache.name != "") else "".join(["%02X" % ci for ci in self.__domain_obj_name.encode("utf-8")])
        cachefilename = prefix+"_%06d_%02d.bphys" % (self.__frame,smokecache.index)
        fullpath = os.path.join( cachefilepath, cachefilename )

        # open file
        self.__pcache = open(fullpath, "rb")
        pcache = self.__pcache
        try:
            # read magic
            read_buffer = pcache.read(8)
            if read_buffer  != b"BPHYSICS":
                raise Exception("Wrong header magic!")
                
            ptcache_type, cell_count = struct.unpack("3I", pcache.read(12))[:2]
            self.__cell_count = cell_count
            if not (ptcache_type & 0xFFFF) in (3,4):
                raise Exception("Wrong file type")
              
            # version 1.x ?  
            cache_v1 = struct.unpack("4s", pcache.read(4))[0].decode('ASCII')[:2] == "1."
            if not cache_v1:
                pcache.seek(-4, 1)

            # 1.x header:
            self.cache_opt = dict()            
            if cache_v1:
                cache_opt = dict()
                cache_opt["cache_fields"], cache_opt["active_fields"], \
                    cache_opt["res_x"], cache_opt["res_y"], cache_opt["res_z"], \
                    cache_opt["res_dx"] = struct.unpack("5If", pcache.read(6*4))                
                self.__cell_count = cache_opt["res_x"] * \
                    cache_opt["res_y"] * cache_opt["res_z"]
                self.cache_opt = cache_opt            
                            
            # smoke high res?    
            self.__cell_count_high = self.__cell_count
            if self.__is_high_res:
                self.__cell_count_high *= self.__high_res_amp * \
                    self.__high_res_amp * self.__high_res_amp    
            
            # old format and not high res        
            if (not cache_v1) and (ptcache_type & 4 != 0):
                self.__is_hight_res = False            
                
            # no data
            if self.__cell_count <= 1:
                self.__is_high_res = False
            
            if not header_only:        
                # shadow
                self.__pcache_skip_part()
                # density
                if not self.__is_high_res:
                    self.__smoke = self.__pcache_read_part()
                else:
                    self.__pcache_skip_part()
                # density old
                if not cache_v1:
                    self.__pcache_skip_part()
                
                if (not cache_v1) or (cache_opt["cache_fields"] & SM_ACTIVE_HEAT > 0):
                    # heat
                    self.__pcache_skip_part()
                    # heat old
                    self.__pcache_skip_part()
                if cache_v1:
                    if cache_opt["cache_fields"] & SM_ACTIVE_FIRE > 0:
                        # fire                
                        if not self.__is_high_res:
                            self.__fire = self.__pcache_read_part()
                        else:
                            self.__pcache_skip_part()
                            
                        for i in range(2): # fuel and react:
                            self.__pcache_skip_part()                
                                        
                    if cache_opt["cache_fields"] & SM_ACTIVE_COLORS > 0:
                        # r, g, b
                        for i in range(3):
                            self.__pcache_skip_part
                        

                # high resolution:
                if self.__is_high_res:
                    # should be always here but does not matter if not high res:
                    # -------------
                    for i in range(3): # vx, vy, vz
                        self.__pcache_skip_part()
                    if not cache_v1:
                        for i in range(3):
                            self.__pcache_skip_part() # vx, vy, vz (old values)                    
                    # obstacle
                    self.__pcache_skip_part()                    
                    # dx, dt
                    skip_bytes = 2*ct.sizeof(ct.c_float)
                    if cache_v1: #p0, p1, dp0, shift, obj_shift_f, obmat, base_res, res min, res max, active color
                        skip_bytes += (3 + 3 + 3 + 3 + 16 + 3) * ct.sizeof(ct.c_float) # p0, p1, dp0, obj_shift_f, obmat, active_color
                        skip_bytes += (3 + 3 + 3 + 3) * ct.sizeof(ct.c_uint) # shift, base_res, res min, res max
                    pcache.seek(skip_bytes, 1) # skip
                    # --------------------------------
                    
                    
                    # smoke (high res)
                    self.__smoke = self.__pcache_read_part(use_high_res=True)
                    # fire (high res)                    
                    if (cache_v1) and (cache_opt["cache_fields"] & SM_ACTIVE_FIRE > 0):
                        self.__fire = self.__pcache_read_part(use_high_res=True)
        finally:
            self.__pcache.close() 

        if not header_only:    
            self.__pcache_extracted = True   
            # no fire information available?
            if (not cache_v1) or (cache_opt["cache_fields"] & SM_ACTIVE_FIRE == 0):
                self.__fire = [0.0] * len(self.__smoke)
                          
# test functions                            
if __name__ == "__main__":
    print ("-" * 40)    
    #print(LZx_Reader.platform())        
    #print(list(LZx_Reader.search_path_iter("LZO")))
    #print(list(LZx_Reader.search_path_iter("LZMA")))    
    #print(LZx_Reader.get_lzx("LZO"))
    #print(LZx_Reader.get_lzx("LZMA"))
    
    #smoke_exporter = SmokeExporter(bpy.context.object.modifiers[0].domain_settings.point_cache,
    #    True, 2, bpy.context.scene.frame_current        
    #)
    smoke_exporter = SmokeExporter(bpy.context.object,
        bpy.context.scene.frame_current)
    print(len(smoke_exporter.fire)**0.33333333)
    # print(smoke_exporter.resolution)
    # print(smoke_exporter.fire)
    print(smoke_exporter.cache_opt)