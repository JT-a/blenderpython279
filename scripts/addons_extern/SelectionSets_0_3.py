bl_info = {
    "name": "Seletion Sets",
    "author": "Johnny Matthews",
    "version": (0, 3),
    "blender": (2, 71, 0),
    "location": "View3D > Tool Self > Tools",
    "description": "Quick Selection Sets",
    "warning": "",
    "wiki_url": "http://johnnygizmo.blogspot.com/p/selection-sets-add-on-for-blender.html",
    "category": "3D View"}


import bpy
import re

#import os
#clear = lambda: os.system('clear')
#clear()
#print("-------")

def Checkname(self,context):
    
    tempname = self.name
    pattern = re.compile("(.+)\(\d*\)$")
    test = pattern.search(tempname)
    if test != None:    
        tempname = test.group(1).rstrip()
    
    bad = True
    num = 0
    while bad:
        bad = False
        for s in bpy.context.scene.selection_sets:      
            if s == self:
                continue
            if num == 0 and self.name == s.name:
                num = 1
                bad = True
            elif self.name + ' (' +str(num)+')' == s.name:
                num = num + 1
                bad = True
    if num > 0:
        self.name = self.name + ' (' +str(num)+')' 


def GetSetFromName(name):
    i = -1
    for n in bpy.context.scene.selection_sets:
        i = i + 1
        if name == n.name:
            return i



class SelectionSetItem(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Name")
    value = bpy.props.StringProperty(name="Value")

class SelectionSet(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Name",update=Checkname)
    active_list = bpy.props.IntProperty()
    set = bpy.props.CollectionProperty(type=SelectionSetItem)
    

class SelectionSetClearAll(bpy.types.Operator):
    bl_idname = "selset.clear_all"
    bl_label = "Clear All Selection Sets"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        bpy.context.scene.selection_sets.clear()
        return {'FINISHED'}   






class SelectionSetNoRender(bpy.types.Operator):
    bl_idname = "selset.no_render"
    bl_label = "Change set to not Render"
    bl_options = {'INTERNAL'}
    target = bpy.props.StringProperty("")
    
    def execute(self, context):
        bpy.context.scene.selection_sets_active = GetSetFromName(self.target)
        for item in bpy.context.scene.selection_sets[self.target].set:
            if item.name in bpy.data.objects:
                bpy.data.objects[item.name].hide_render = True;
        return {'FINISHED'}   

class SelectionSetRender(bpy.types.Operator):
    bl_idname = "selset.render"
    bl_label = "Change set to Render"
    bl_options = {'INTERNAL'}
    target = bpy.props.StringProperty("")
    def execute(self, context):
        bpy.context.scene.selection_sets_active = GetSetFromName(self.target)
        for item in bpy.context.scene.selection_sets[self.target].set:
            if item.name in bpy.data.objects:
                bpy.data.objects[item.name].hide_render = False;
        return {'FINISHED'}  



class SelectionSetNoVisible(bpy.types.Operator):
    bl_idname = "selset.no_visible"
    bl_label = "Change set to not visible"
    bl_options = {'INTERNAL'}
    target = bpy.props.StringProperty("")
    def execute(self, context):
        bpy.context.scene.selection_sets_active = GetSetFromName(self.target)
        for item in bpy.context.scene.selection_sets[self.target].set:
            if item.name in bpy.data.objects:
                bpy.data.objects[item.name].hide = True;
        return {'FINISHED'}   

class SelectionSetVisible(bpy.types.Operator):
    bl_idname = "selset.visible"
    bl_label = "Change set to visible"
    bl_options = {'INTERNAL'}
    target = bpy.props.StringProperty("")
    def execute(self, context):
        bpy.context.scene.selection_sets_active = GetSetFromName(self.target)
        for item in bpy.context.scene.selection_sets[self.target].set:
            if item.name in bpy.data.objects:
                bpy.data.objects[item.name].hide = False;
        return {'FINISHED'}    





class SelectionSetSelectList(bpy.types.Operator):
    bl_idname = "selset.select_list"
    bl_label = "Select Selection Set Items"
    bl_options = {'INTERNAL'}
    target = bpy.props.StringProperty("")
    def execute(self, context):
        
        bpy.ops.object.select_all(action='TOGGLE')

        bpy.context.scene.selection_sets_active = GetSetFromName(self.target)
        
        for n in bpy.context.scene.selection_sets[self.target].set:
            bpy.ops.object.select_pattern(pattern=n.name, case_sensitive=False, extend=True)
        return {'FINISHED'}   


class SelectionSetAddSet(bpy.types.Operator):
    
    bl_label = "Add Selection Set"
    bl_idname = "selset.add_set"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        
        temp = bpy.context.scene.selection_sets.add()
        bpy.context.scene.selection_sets_active = len(bpy.context.scene.selection_sets)-1
        temp.name = 'New Set'
        
        #bpy.context.scene.selection_sets_active = len(bpy.context.scene.selection_sets)-1
        
        contains = []
        for n in bpy.context.scene.selection_sets[bpy.context.scene.selection_sets_active].set:
            contains.insert(len(contains),n.name)
        for e in bpy.context.selected_objects:
            if e.name not in contains:
                temp = bpy.context.scene.selection_sets[bpy.context.scene.selection_sets_active].set.add()
                temp.name = e.name
        return {'FINISHED'}    

class SelectionSetRemSet(bpy.types.Operator):
    bl_idname = "selset.rem_set"
    bl_label = "Remove Selection Set"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        bpy.context.scene.selection_sets.remove(bpy.context.scene.selection_sets_active)
        return {'FINISHED'}      

class SelectionSetAddItem(bpy.types.Operator):
    bl_idname = "selset.add_item"
    bl_label = "Add Selected Items to Set"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        contains = []
        for n in bpy.context.scene.selection_sets[bpy.context.scene.selection_sets_active].set:
            contains.insert(len(contains),n.name)
        for e in bpy.context.selected_objects:
            if e.name not in contains:
                temp = bpy.context.scene.selection_sets[bpy.context.scene.selection_sets_active].set.add()
                temp.name = e.name
                
                
        return {'FINISHED'}    

class SelectionSetRemItem(bpy.types.Operator):
    bl_idname = "selset.rem_item"
    bl_label = "Remove Selected Items from Set"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        sets = bpy.context.scene.selection_sets
        aset = bpy.context.scene.selection_sets_active
        sets[aset].set.remove(sets[aset].active_list)
        return {'FINISHED'}   


class SelectionSetsSetList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            #layout.prop(item,name)
            #layout.label(item.name if item else "", icon_value=icon)
         
            layout.prop(item,"name",emboss=False,text="",icon='GROUP')
            
            temp = layout.operator(SelectionSetSelectList.bl_idname, icon='BORDER_RECT', text="", emboss=False)       
            temp.target = item.name
            temp = layout.operator(SelectionSetNoRender.bl_idname, icon='RESTRICT_RENDER_ON', text="", emboss=False)  
            temp.target = item.name
            temp = layout.operator(SelectionSetRender.bl_idname, icon='RESTRICT_RENDER_OFF', text="", emboss=False)  
            temp.target = item.name
            temp = layout.operator(SelectionSetNoVisible.bl_idname, icon='RESTRICT_VIEW_ON', text="", emboss=False)  
            temp.target = item.name
            temp = layout.operator(SelectionSetVisible.bl_idname, icon='RESTRICT_VIEW_OFF', text="", emboss=False)  
            temp.target = item.name

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon_value=icon)

"""


class SelectionSetsItemsList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            #layout.prop(item,name)
            layout.label(item.name if item else "", icon_value=icon)
            layout.operator(SelectionSetRemItem.bl_idname,text='',icon='X')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon_value=icon)
"""

class SelectionSets(bpy.types.Panel):
    """A Custom Panel"""
    bl_label = "Selection Sets"
    bl_space_type = "VIEW_3D"
    bl_region_type= "TOOLS"
    bl_category = "Layers"
    
   
    
    def draw(self, context): 
        sets = bpy.context.scene.selection_sets
        layout = self.layout
        
        #row = layout.row()
        #row.operator(SelectionSetClearAll.bl_idname)
        row = layout.row()
        #row.operator(SelectionSetAddSet.bl_idname)
        #row = layout.row()
        #row.label(str(len(bpy.context.scene.selection_sets))+" Sets")
        #row.label(str(len(bpy.context.scene.selection_sets[bpy.context.scene.selection_sets_active].set))+" Items")
        
        row = layout.row()
        row.label("Sets")
        row = layout.row()
        row.template_list("SelectionSetsSetList", "sets", bpy.context.scene,"selection_sets",bpy.context.scene,"selection_sets_active")

        col = row.column(align=True)
        col.operator(SelectionSetAddSet.bl_idname, icon='ZOOMIN', text="")
        col.operator(SelectionSetRemSet.bl_idname, icon='ZOOMOUT', text="")
    
      
        
        
        #if len(sets) > 0:
        row = layout.row()
        row.label("Items")
        row = layout.row()
        #bpy.context.scene.selection_sets_item = None
        
        index = bpy.context.scene.selection_sets_active
        if index > len(sets)-1:
            index = len(sets)-1
        
        if index >= 0:
            row.template_list("UI_UL_list","items",sets[index],"set",bpy.context.scene,"selection_sets_item")

        col = row.column(align=True)    
        col.operator(SelectionSetAddItem.bl_idname, icon='ZOOMIN', text="")
        col.operator(SelectionSetRemItem.bl_idname, icon='ZOOMOUT', text="")
        
def ActiveSetUpdate(self, context):
    i =  -1
    for item in bpy.context.scene.selection_sets[bpy.context.scene.selection_sets_active].set:
        i = i + 1
        if item.name not in bpy.data.objects:
            bpy.context.scene.selection_sets[bpy.context.scene.selection_sets_active].set.remove(i)
    return None        
        
        
def register():
    bpy.utils.register_class(SelectionSetItem)
    bpy.utils.register_class(SelectionSet)
    bpy.utils.register_class(SelectionSetAddSet)
    bpy.utils.register_class(SelectionSetRemSet)
    bpy.utils.register_class(SelectionSetAddItem)
    bpy.utils.register_class(SelectionSetRemItem)
    bpy.utils.register_class(SelectionSetClearAll)
    #bpy.utils.register_class(SelectionSetsItemsList)
    bpy.utils.register_class(SelectionSetsSetList)
    bpy.utils.register_class(SelectionSetSelectList)    
    bpy.utils.register_class(SelectionSetNoVisible)
    bpy.utils.register_class(SelectionSetVisible)  

    bpy.utils.register_class(SelectionSetNoRender)
    bpy.utils.register_class(SelectionSetRender)  
    
    bpy.utils.register_class(SelectionSets)
    
    bpy.types.Scene.selection_sets = bpy.props.CollectionProperty(type=SelectionSet) 
    bpy.types.Scene.selection_sets_active = bpy.props.IntProperty(update=ActiveSetUpdate) 
    bpy.types.Scene.selection_sets_item = bpy.props.IntProperty() 
        
def unregister():
    bpy.utils.unregister_class(SelectionSetClearAll)
    bpy.utils.unregister_class(SelectionSets)
    bpy.utils.unregister_class(SelectionSetAddSet)
    bpy.utils.unregister_class(SelectionSetRemSet)
    bpy.utils.unregister_class(SelectionSetAddItem)
    bpy.utils.unregister_class(SelectionSetRemItem)    
    bpy.utils.unregister_class(SelectionSet)
    bpy.utils.unregister_class(SelectionSetNoVisible)
    bpy.utils.unregister_class(SelectionSetVisible)
    bpy.utils.unregister_class(SelectionSetNoRender)
    bpy.utils.unregister_class(SelectionSetRender)  
    bpy.utils.unregister_class(SelectionSetsSetList)
    bpy.utils.unregister_class(SelectionSetSelectList)  
    bpy.utils.unregister_class(SelectionSetItem)

if __name__ == "__main__":
    register()


