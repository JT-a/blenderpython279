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
#
# ----
# NOT: "hk_" ile baslayan islevler program icinde tanimlanmis islevlerdir.
# ----
#
# Programmed by: Hikmet Koyuncu @07-2013
# #####
"""
bl_info = {
    "name": "Group Editor",
    "author": "Hikmet Koyuncu",
    "version": (0, 3),
    "blender": (2, 6, 6),
    "location": "Properties > Group Editor",
    "description": "Group editor.",
    "category": "Object",
    'wiki_url': '',
    'tracker_url': ''}
"""
import bpy


class GroupList(bpy.types.PropertyGroup):
    pass

bpy.utils.register_class(GroupList)



class GroupObjectList(bpy.types.PropertyGroup):
    pass


bpy.utils.register_class(GroupObjectList)

def clearGroupList():
    list = bpy.context.scene.hk_group_list
    for grp in list.items():
        list.remove(0)
        
        
def clearGroupObjectList():
    list = bpy.context.scene.hk_group_object_list
    for obj in list.items():
        list.remove(0)
        
        

def loadGroupList():

    if "hk_group_list" in dir(bpy.context.scene):
        list = bpy.context.scene.hk_group_list
        index = bpy.context.scene.hk_group_list_index

        clearGroupList()
        
        if len(bpy.data.groups) == 0: return
        
        for grp in bpy.data.groups:
            if grp != None and grp.users > 0:
                grp_member = list.add()
                grp_member.name  = grp.name
                grp_member.value = grp.name
                
        count = len(list)
        if count > 0 and index == count:
            bpy.context.scene.hk_group_list_index = index - 1
            
            

def loadGroupObjectList():

    if "hk_group_object_list" in dir(bpy.context.scene):
        list = bpy.context.scene.hk_group_object_list
        listGrp = bpy.context.scene.hk_group_list
        index = bpy.context.scene.hk_group_object_list_index
        indexGrp = bpy.context.scene.hk_group_list_index

        clearGroupObjectList()
        
        grp = bpy.data.groups[listGrp[indexGrp].name]
        if grp.objects == 0: return
        
        for obj in grp.objects:
            if obj != None:
                obj_member = list.add()
                obj_member.name  = obj.name
                obj_member.value = obj.name

        count = len(list)
        if count > 0 and index == count:
            bpy.context.scene.hk_group_object_list_index = index - 1
                      
            
def unlinkGroup(isRemove):
    list = bpy.context.scene.hk_group_list

    if len(list) == 0:
        return {"FINISHED"}
        
    index = bpy.context.scene.hk_group_list_index
    grp = bpy.data.groups[list[index].name]

    bpy.context.user_preferences.edit.use_global_undo = False
    

    if len(grp.objects) > 0:
        for o in grp.objects:               
            grp.objects.unlink(o)
    
    
    if isRemove == True:
        grp.user_clear()
    
    loadGroupObjectList()
    
    bpy.context.user_preferences.edit.use_global_undo = True
    
    loadGroupList()
            
            
#======================================================================
        
        
class HK_RefreshGroupList(bpy.types.Operator):
    bl_label = "Refresh Group List"
    bl_description = "Refresh Group list."
    bl_idname = "scene.hk_refresh_group_list"
    
    def execute(self, context):
        loadGroupList()
        return {"FINISHED"}
    
    
class HK_RefreshObjectList(bpy.types.Operator):
    bl_label = "Refresh Group Object List"
    bl_description = "Refresh Group Object list."
    bl_idname = "scene.hk_refresh_group_object_list"
    
    def execute(self, context):
        loadGroupObjectList()
        return {"FINISHED"}
    

class HK_GetSelectedNameList(bpy.types.Operator):
    bl_label = "Get Selected Group Name from List"
    bl_description = "Get selected group contents (Look 'Object List')."
    bl_idname = "scene.hk_get_group_contents_list"
    
    def execute(self, context):
        list = bpy.context.scene.hk_group_list
        
        if len(list) == 0:
            return {"FINISHED"}
        
        index = bpy.context.scene.hk_group_list_index
        grp = bpy.data.groups[list[index].name]
        
        bpy.context.scene.hk_group_name_txt = grp.name
        
        loadGroupObjectList()
        
        return {"FINISHED"}


class HK_RenameGroup(bpy.types.Operator):
    bl_label = "Rename Group"
    bl_description = "Rename Group."
    bl_idname = "scene.hk_rename_group_list"
    
    def execute(self, context):
        list = bpy.context.scene.hk_group_list
        
        if len(list) == 0:
            return {"FINISHED"}
        
        index = bpy.context.scene.hk_group_list_index
        grp = bpy.data.groups[list[index].name]
        
        grp.name = bpy.context.scene.hk_group_name_txt # Group rename

        list[index].name = grp.name
        
        return {"FINISHED"}
    

class HK_CreateNewGroup(bpy.types.Operator):
    bl_label = "Create New Group"
    bl_description = "Create new group."
    bl_idname = "scene.hk_create_new_group_list"
    
    def execute(self, context):       
        bpy.data.groups.new(name="Group")
        
        loadGroupList() 
        
        return {"FINISHED"}
    

class HK_AddObjectGroup(bpy.types.Operator):
    bl_label = "Add Object Group List"
    bl_description = "Add selected object to group."
    bl_idname = "scene.hk_add_object_group_list"
    
    def execute(self, context):
        list = bpy.context.scene.hk_group_list
        
        if len(list) == 0:
            return {"FINISHED"}
        
        index = bpy.context.scene.hk_group_list_index

        bpy.ops.object.group_link(group=list[index].name)
        bpy.ops.group.objects_add_active(group=list[index].name)
        
        loadGroupObjectList() 
        
        return {"FINISHED"}
    
    
class HK_RemoveObjectGroup(bpy.types.Operator):
    bl_label = "Remove Object Group List"
    bl_description = "Remove selected object from selected group."
    bl_idname = "scene.hk_remove_object_group_list"
    
    def execute(self, context):
        list = bpy.context.scene.hk_group_list
        
        if len(list) == 0:
            return {"FINISHED"}
        
        index = bpy.context.scene.hk_group_list_index
        
        bpy.ops.group.objects_remove(group=list[index].name)
        
        loadGroupObjectList()
        
        return {"FINISHED"}
    
    

class HK_UnlinkObjectListGroup(bpy.types.Operator):
    bl_label = "Unlink Object Group List"
    bl_description = "Unlink selected object from selected group."
    bl_idname = "scene.hk_unlink_object_group_list"
    
    def execute(self, context):
        list = bpy.context.scene.hk_group_object_list
        listGrp = bpy.context.scene.hk_group_list
        
        if len(list) == 0 or len(listGrp) == 0:
            return {"FINISHED"}
        
        index    = bpy.context.scene.hk_group_object_list_index
        indexGrp = bpy.context.scene.hk_group_list_index
        
        
        bpy.ops.object.select_all(action='DESELECT') 
        
        print( bpy.data.objects[list[index].name] )
        print( listGrp[indexGrp].name )
        
        o = bpy.data.objects[list[index].name]
        o.select = True 
        bpy.context.scene.objects.active = o  
        bpy.ops.group.objects_remove(group=listGrp[indexGrp].name)
        
        loadGroupObjectList()
        
        
        return {"FINISHED"}
    


class HK_UnlinkSelGrp(bpy.types.Operator):
    bl_label = "Unlink Selected Group"
    bl_description = "Unlink selected group."
    bl_idname = "scene.hk_unlink_selected_group"
    
    def execute(self, context):
        unlinkGroup(False)
        
        return {"FINISHED"}

    
class HK_RemoveSelGrp(bpy.types.Operator):
    bl_label = "Remove Selected Group"
    bl_description = "Remove selected group."
    bl_idname = "scene.hk_remove_selected_group"
    
    def execute(self, context):
        # Show Message Box
        if len(bpy.context.scene.hk_group_list) > 0:
            bpy.ops.error.hk_msgbox('INVOKE_DEFAULT')
        
        return {"FINISHED"}
    
    

class HK_SelectGroup(bpy.types.Operator):
    bl_label = "Select Group"
    bl_description = "Select group."
    bl_idname = "scene.hk_select_group_list"
    
    def execute(self, context):
        list = bpy.context.scene.hk_group_list
    
        if len(list) == 0:
            return {"FINISHED"}
        
        index = bpy.context.scene.hk_group_list_index
        grp = bpy.data.groups[list[index].name]
        
               
        if len(grp.objects) > 0:
            for o in grp.objects:
                o.select = True  
    
        return {"FINISHED"}
    
    

class HK_DeselectGroup(bpy.types.Operator):
    bl_label = "Deselect Group"
    bl_description = "Deselect group."
    bl_idname = "scene.hk_deselect_group_list"
    
    def execute(self, context):
        list = bpy.context.scene.hk_group_list
    
        if len(list) == 0:
            return {"FINISHED"}
        
        index = bpy.context.scene.hk_group_list_index
        grp = bpy.data.groups[list[index].name]
        
        
        if len(grp.objects) > 0:
            for o in grp.objects:
                o.select = False  
    
        return {"FINISHED"}
    
    

class HK_SelectObjectListGroup(bpy.types.Operator):
    bl_label = "Select Object Group List"
    bl_description = "Select object from object list."
    bl_idname = "scene.hk_select_object_group_list"
    
    def execute(self, context):
        list = bpy.context.scene.hk_group_object_list
        
        if len(list) == 0:
            return {"FINISHED"}
        
        index = bpy.context.scene.hk_group_object_list_index       
        
        bpy.ops.object.select_all(action='DESELECT') 
        
        o = bpy.data.objects[list[index].name]
        o.select = True  
        bpy.context.scene.objects.active = o  
        
        return {"FINISHED"}
  

#======================================================================


iIndexTmp = 0

class SCENE_PT_HK_GroupEditor_ItemList(bpy.types.UIList):
  def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):   
    layout.label(item.name)
       

class HK_MsgBox(bpy.types.Operator):
    bl_idname = "error.hk_msgbox"
    bl_label = "Remove Group"
 
    def execute(self, context):
        unlinkGroup(True)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)
 
    def draw(self, context):
        self.layout.label("Are you sure?", icon="CANCEL")
        
bpy.utils.register_class(HK_MsgBox)





def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
