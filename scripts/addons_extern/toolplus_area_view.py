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
    "name": "TP Area",
    "description": "menu to jump to next editor or mode, and for customizing area, split and join",
    "location": "CTRL+BACKSLAH",
    "author": "Cedric_Lepiller & DoubleZ & Lapineige & MKB",
    "version": (0, 1, 0),
    "blender": (2, 78, 0),
    "warning": "",
    "wiki_url": "",
    "category": "ToolPlus"
    }


import bpy, os
from bpy import *
from bpy.props import *
from bpy.types import Operator, AddonPreferences

import rna_keymap_ui

# main menu
class TP_Display_View_Extend_Menu(bpy.types.Menu):
    bl_label = "T+ Area :)"
    bl_idname = "tp_display.view_extend_menu"
     
    def draw(self, context):
        layout = self.layout        
        
        view = context.space_data
        obj = context.active_object
        toolsettings = context.tool_settings        
            
        layout.menu("tp_display.view_custom_menu", text = "Editors", icon = "PLUG")

        if bpy.context.area.type == 'VIEW_3D': 
            
            layout.separator()
  
            layout.prop(context.space_data, "viewport_shade", text="") 
            layout.operator_menu_enum("OBJECT_OT_mode_set", "mode", icon = "EDIT")
             
                
        if context.scene.CustomizeTools:
            
            layout.separator() 
                
            layout.operator("screen.area_split", text="Split Vertical", icon= 'TRIA_RIGHT').direction="VERTICAL"

            layout.operator("screen.area_split", text="Split Horizontal", icon= 'TRIA_DOWN').direction="HORIZONTAL"
        
            layout.separator() 

            layout.operator_context="INVOKE_DEFAULT"
            layout.operator("tp_display.join_area", icon='AUTOMERGE_ON', text="Join Area")        


        if context.scene.QuadTools:
                                
            if context.space_data.region_3d:
                
                layout.separator() 
                
                layout.operator("screen.region_quadview", text = "Quad View", icon = "SPLITSCREEN")
                
                if context.space_data.region_quadviews:
                  
                    region = context.space_data.region_quadviews[2]                        
                    layout.prop(region, "lock_rotation", text = "Lock Rotation")        
                    
                    if region.lock_rotation:
                        layout.prop(region, "show_sync_view", text = "Sync View")
                    
                    if region.show_sync_view:
                        layout.prop(region, "use_box_clip", text = "Box Clip")

        
        if context.scene.ScreenTools:
            
            layout.separator() 
            
            layout.operator("screen.screen_full_area", text = "Full Area", icon = "GO_LEFT")
            layout.operator("wm.window_fullscreen_toggle", text = "Full Screen", icon = "GO_LEFT")
   
            layout.separator()
            layout.operator_context = 'INVOKE_REGION_WIN'                         
            layout.operator("screen.area_dupli", text = "Duplicate Window", icon = "SCREEN_BACK")  

        if context.scene.ShelfTools:
            
            layout.separator()         

            layout.operator("view3d.properties", icon='MENU_PANEL')
            layout.operator("view3d.toolshelf", icon='MENU_PANEL')



# editor menu
class TP_Display_View_Custom_Menu(bpy.types.Menu):
    bl_label = ""
    bl_idname = "tp_display.view_custom_menu"
     
    def draw(self, context):
        layout = self.layout
        
        col=layout.column()
                
        if context.scene.Menu3DView:
            col.operator("tp_display.view_menu", text="VIEW 3D", icon= 'VIEW3D').variable="VIEW_3D"
        
        if context.scene.MenuNodeEditor:
            col.operator("tp_display.view_menu", text="Node Editor", icon= 'NODETREE').variable="NODE_EDITOR"
        
        if context.scene.MenuImageEditor:
            col.operator("tp_display.view_menu", text="Image Editor", icon= 'IMAGE_COL').variable="IMAGE_EDITOR"
        
        if context.scene.MenuOutliner:
            col.operator("tp_display.view_menu", text="Outliner", icon= 'OOPS').variable="OUTLINER"
            
        if context.scene.MenuProperties:
            col.operator("tp_display.view_menu", text="Properties", icon= 'BUTS').variable="PROPERTIES"
            
        if context.scene.MenuTextEditor:
            col.operator("tp_display.view_menu", text="Text Editor", icon= 'FILE_TEXT').variable="TEXT_EDITOR"
        
        if context.scene.MenuGraphEditor:
            col.operator("tp_display.view_menu", text="Graph Editor", icon= 'IPO').variable="GRAPH_EDITOR"
            
        if context.scene.MenuDopeSheet:     
            col.operator("tp_display.view_menu", text="Dope Sheet", icon= 'ACTION').variable="DOPESHEET_EDITOR"
        
        if context.scene.MenuTimeline:
            col.operator("tp_display.view_menu", text="Timeline", icon= 'TIME').variable="TIMELINE"
        
        if context.scene.MenuNlaEditor:
            col.operator("tp_display.view_menu", text="NLA Editor", icon= 'NLA').variable="NLA_EDITOR"
            
        if context.scene.MenuLogicEditor:
            col.operator("tp_display.view_menu", text="Logic Editor", icon= 'LOGIC').variable="LOGIC_EDITOR"
        
        if context.scene.MenuSequenceEditor:
            col.operator("tp_display.view_menu", text="Sequence Editor", icon= 'SEQUENCE').variable="SEQUENCE_EDITOR"
     
        if context.scene.MenuMovieClip:
            col.operator("tp_display.view_menu", text="Movie Clip Editor", icon= 'RENDER_ANIMATION').variable="CLIP_EDITOR"
   
        if context.scene.MenuPythonConsole:
            col.operator("tp_display.view_menu", text="Python Console", icon= 'CONSOLE').variable="CONSOLE" 
        
        if context.scene.MenuInfo:
            col.operator("tp_display.view_menu", text="Info", icon= 'INFO').variable="INFO"
            
        if context.scene.MenuFileBrowser:
            col.operator("tp_display.view_menu", text="File Browser", icon= 'FILESEL').variable="FILE_BROWSER" 
   
        if context.scene.MenuUserPreferences:
            col.operator("tp_display.view_menu", text="User Preferences", icon= 'PREFERENCES').variable="USER_PREFERENCES"  



# properties 
class TP_Display_Preferences_Addon(AddonPreferences):
    bl_idname = __name__
    
    bpy.types.Scene.CustomizeTools = BoolProperty(default = True)
    bpy.types.Scene.ScreenTools = BoolProperty(default = True)
    bpy.types.Scene.QuadTools = BoolProperty(default = True)
    bpy.types.Scene.ShelfTools = BoolProperty(default = True)

    bpy.types.Scene.Menu3DView = BoolProperty(default = True)
    bpy.types.Scene.MenuNodeEditor = BoolProperty(default = True)
    bpy.types.Scene.MenuImageEditor = BoolProperty(default = True)
    bpy.types.Scene.MenuOutliner = BoolProperty(default = True)
    bpy.types.Scene.MenuProperties = BoolProperty(default = True)
    bpy.types.Scene.MenuTextEditor = BoolProperty(default = True)
    bpy.types.Scene.MenuGraphEditor = BoolProperty(default = True)
    bpy.types.Scene.MenuDopeSheet = BoolProperty(default = True)
    bpy.types.Scene.MenuTimeline = BoolProperty(default = True)
    bpy.types.Scene.MenuNlaEditor = BoolProperty(default = False)
    bpy.types.Scene.MenuLogicEditor = BoolProperty(default = False)
    bpy.types.Scene.MenuSequenceEditor = BoolProperty(default = False)
    bpy.types.Scene.MenuMovieClip = BoolProperty(default = False)
    bpy.types.Scene.MenuPythonConsole = BoolProperty(default = False)
    bpy.types.Scene.MenuInfo = BoolProperty(default = False)
    bpy.types.Scene.MenuFileBrowser = BoolProperty(default = False)
    bpy.types.Scene.MenuUserPreferences = BoolProperty(default = True)

    def draw (self, context):
        layout=self.layout.column_flow(1) 

        box = layout.box().column(1) 
         
        row = box.row(1)  
        row.label("Show Customize Tools:")

        row = box.row(1)        

        if context.scene.CustomizeTools:   
            row.prop(context.scene,"CustomizeTools", text = "Customize Tools", icon="RESTRICT_VIEW_OFF" )
        else:
         row.prop(context.scene,"CustomizeTools", text = "Customize Tools", icon="RESTRICT_VIEW_ON" )

        if context.scene.QuadTools:   
            row.prop(context.scene,"QuadTools", text = "Quad View", icon="RESTRICT_VIEW_OFF" )
        else:
            row.prop(context.scene,"QuadTools", text = "Quad View", icon="RESTRICT_VIEW_ON" )

        if context.scene.ScreenTools:   
            row.prop(context.scene,"ScreenTools", text = "Full Screen", icon="RESTRICT_VIEW_OFF" )
        else:
            row.prop(context.scene,"ScreenTools", text = "Full Screen", icon="RESTRICT_VIEW_ON" )

        if context.scene.ShelfTools:   
            row.prop(context.scene,"ShelfTools", text = "View Shelfs", icon="RESTRICT_VIEW_OFF" )
        else:
            row.prop(context.scene,"ShelfTools", text = "View Shelfs", icon="RESTRICT_VIEW_ON" )
        

        box.separator() 
        
        box = layout.box().column(1) 

        row = box.row(1)  
        row.label("Show Editor in Menu:")
        
        row = box.column_flow(3)        
        row.prop(context.scene,"Menu3DView", text = "3D View", icon= 'VIEW3D')
        row.prop(context.scene,"MenuNodeEditor", text = "Node Editor", icon= 'NODETREE')
        row.prop(context.scene,"MenuImageEditor", text = "Image Editor", icon= 'IMAGE_COL')
        row.prop(context.scene,"MenuOutliner", text = "Outliner", icon= 'OOPS')
        row.prop(context.scene,"MenuProperties", text = "Properties", icon= 'BUTS')
        row.prop(context.scene,"MenuTextEditor", text = "Text Editor", icon= 'FILE_TEXT')
        row.prop(context.scene,"MenuGraphEditor", text = "Graph Editor", icon= 'IPO')
        row.prop(context.scene,"MenuDopeSheet", text = "Dope Sheet", icon= 'ACTION')
        row.prop(context.scene,"MenuTimeline", text = "Timeline", icon= 'TIME')
        row.prop(context.scene,"MenuNlaEditor", text = "Nla Editor", icon= 'NLA')
        row.prop(context.scene,"MenuLogicEditor", text = "Logic Editor", icon= 'LOGIC')
        row.prop(context.scene,"MenuSequenceEditor", text = "Sequence Editor", icon= 'SEQUENCE')
        row.prop(context.scene,"MenuMovieClip", text = "Movie Clip", icon= 'RENDER_ANIMATION')
        row.prop(context.scene,"MenuPythonConsole", text = "Python Console", icon= 'CONSOLE')
        row.prop(context.scene,"MenuInfo", text = "Info", icon= 'INFO')
        row.prop(context.scene,"MenuFileBrowser", text = "File Browser", icon= 'FILESEL')
        row.prop(context.scene,"MenuUserPreferences", text = "User Preferences", icon= 'PREFERENCES')

        box.separator() 
        
        box = layout.box()
                
        col = box.column()
        kc = bpy.context.window_manager.keyconfigs.addon
        for km, kmi in addon_keymaps:
            km = km.active()
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)



# operator to show editor in the menu
class TP_Display_View_Menu(bpy.types.Operator):    
    bl_idname = "tp_display.view_menu"
    bl_label = "View_Menu"
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.area.type=self.variable
        return {'FINISHED'}  


# join operator  
class TP_Display_Join_Area(bpy.types.Operator):
    """Join 2 area, press and clic on the second area to join"""
    bl_idname = "tp_display.join_area"
    bl_label = "Join Area"

    min_x = IntProperty()
    min_y = IntProperty()

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':
            self.max_x = event.mouse_x
            self.max_y = event.mouse_y
            bpy.ops.screen.area_join(min_x=self.min_x, min_y=self.min_y, max_x=self.max_x, max_y=self.max_y)
            bpy.ops.screen.screen_full_area()
            bpy.ops.screen.screen_full_area()
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.min_x = event.mouse_x
        self.min_y = event.mouse_y
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}



addon_keymaps = []

def register():

    bpy.utils.register_class(TP_Display_View_Custom_Menu)  
    bpy.utils.register_class(TP_Display_View_Extend_Menu)
    bpy.utils.register_class(TP_Display_Preferences_Addon)
    bpy.utils.register_class(TP_Display_View_Menu)
    bpy.utils.register_class(TP_Display_Join_Area)

    #kEYMAP#
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name='Window')

    #Move
    kmi = km.keymap_items.new('wm.call_menu', 'BACK_SLASH', 'PRESS', shift=True)
    kmi.properties.name = "tp_display.view_extend_menu"        

    kmi.active = True
    addon_keymaps.append((km, kmi))    


def unregister():

    bpy.utils.unregister_class(TP_Display_View_Custom_Menu) 
    bpy.utils.unregister_class(TP_Display_View_Extend_Menu)
    bpy.utils.unregister_class(TP_Display_Preferences_Addon)
    bpy.utils.unregister_class(TP_Display_View_Menu)
    bpy.utils.unregister_class(TP_Display_Join_Area)

    #kEYMAP#
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        
    addon_keymaps.clear()  

if __name__ == "__main__":
    register()        

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=TP_Display_View_Extend_Menu.bl_idname)


