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
    "name": "TP Display File",
    "author": "marvin.k.breuer",
    "version": (0,1),
    "blender": (2, 7, 7),
    "category": "Tool+"
    }


import bpy
from bpy import *


class VIEW3D_TP_Display_File(bpy.types.Menu):
    bl_label = "File [ALT+W]"
    bl_idname = "tp_display.file_menu"  

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.read_homefile", text="New", icon='NEW')
        layout.operator("wm.open_mainfile", text="Open...", icon='FILE_FOLDER')
        layout.menu("INFO_MT_file_open_recent", icon='OPEN_RECENT')
        layout.menu("tp_display.file_recocver", icon='RECOVER_LAST')

        layout.separator()

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.link", text="Link", icon='LINK_BLEND')
        layout.operator("wm.append", text="Append", icon='APPEND_BLEND')
        layout.menu("INFO_MT_file_previews")   
             
        layout.separator()

        layout.menu("INFO_MT_file_import", icon='IMPORT')
        layout.menu("INFO_MT_file_export", icon='EXPORT')

        layout.separator()

        layout.operator("object.make_local", icon='LAYER_USED')
        layout.operator("object.proxy_make", icon='LAYER_USED')

        layout.separator()

        layout.operator_context = 'EXEC_AREA' if context.blend_data.is_saved else 'INVOKE_AREA'
        layout.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')

        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save As...", icon='SAVE_AS')
        layout.operator_context = 'INVOKE_AREA'
        layout.operator("wm.save_as_mainfile", text="Save Copy...", icon='SAVE_COPY').copy = True


        layout.separator()

        layout.operator("screen.userpref_show", text="User Preferences...", icon='PREFERENCES')
        layout.menu("tp_display.file_settings", icon='MODIFIER')
        layout.menu("INFO_MT_file_external_data", icon='EXTERNAL_DATA')

        layout.separator()

        layout.operator_context = 'EXEC_AREA'
        if bpy.data.is_dirty and context.user_preferences.view.use_quit_dialog:
            layout.operator_context = 'INVOKE_SCREEN'  # quit dialog
        layout.operator("wm.quit_blender", text="Quit", icon='QUIT')


class VIEW3D_TP_Display_File_Recover(bpy.types.Menu):
    bl_label = "Revert & Recover"
    bl_idname = "tp_display.file_recocver"  

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator_context = 'INVOKE_AREA'
        
        layout.operator("wm.revert_mainfile", icon='FILE_REFRESH')
        layout.operator("wm.recover_last_session", icon='RECOVER_LAST')
        layout.operator("wm.recover_auto_save", text="Recover Auto Save...", icon='RECOVER_AUTO')        
        

class VIEW3D_TP_Display_File_Settings(bpy.types.Menu):
    bl_label = "Start Up"
    bl_idname = "tp_display.file_settings"  

    def draw(self, context):
        layout = self.layout
        settings = context.tool_settings
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator_context = 'INVOKE_AREA'
        
        layout.operator("wm.save_homefile", icon='SAVE_PREFS')
        layout.operator("wm.read_factory_settings", icon='LOAD_FACTORY')     



def register():

    bpy.utils.register_class(VIEW3D_TP_Display_File_Settings)
    bpy.utils.register_class(VIEW3D_TP_Display_File_Recover)
    bpy.utils.register_class(VIEW3D_TP_Display_File)
        
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name='Window')
        kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS', alt=True)
        kmi.properties.name = "tp_display.file_menu"               


def unregister():
  
    bpy.utils.unregister_class(VIEW3D_TP_Display_File_Settings)
    bpy.utils.unregister_class(VIEW3D_TP_Display_File_Recover)
    bpy.utils.unregister_class(VIEW3D_TP_Display_File)
           
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps['Window']
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "":
                    km.keymap_items.remove(kmi)
                    break                 

if __name__ == "__main__":
    register() 	

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=VIEW3D_TP_Display_File.bl_idname)












