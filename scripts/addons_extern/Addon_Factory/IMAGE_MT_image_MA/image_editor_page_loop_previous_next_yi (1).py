bl_info = {
    "name": "image editor page loop",
    "author": "NirenYang[BlenderCN]",
    "version": (0, 1),
    "blender": (2, 75, 3),
    "location": "[image editor] Page Up/Down",
    "description": "image editor page loop",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "image",
}

"""
Image Edtior
图像浏览快捷键插件
Page Up/Down

"""
import bpy
import threading
from time import ctime,sleep

enum_page = [( 'PAGE_UP', 'up', 'previous' ),
            ( 'PAGE_DOWN', 'down', 'next' )]
class IMAGE_OT_page_loop(bpy.types.Operator):
    """
    上/下 一张 图片
    """
    bl_idname = 'image.page_loop'
    bl_label = 'page_loop'

    input_page = bpy.props.EnumProperty(name='page_loop', description='page up/down', items=enum_page)

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return context.area.type == 'IMAGE_EDITOR'
        
    def execute(self, context):
        C = context
        D = bpy.data
        
        if len(D.images) < 1:
            self.report({'INFO'}, 'image need!')
            return {'CANCELLED'}
        
        dImages = D.images.values()
        current_image_index = dImages.index(context.space_data.image)
        
        print("current_image_index",current_image_index)
        
        if self.input_page == 'PAGE_UP':
            current_image_index = current_image_index -1
        else:
            current_image_index = current_image_index +1
        
        print("current_image_index -+ ",current_image_index)
        
        if current_image_index < 0:
            current_image_index = len(dImages)-1
        elif current_image_index == len(dImages):
            current_image_index = 0
        
        print("current_image_index final ",current_image_index)
        
        context.space_data.image = dImages[current_image_index]
        
        return {'FINISHED'}

    
def registerImageLoopHotkey(balabala):
    sleep(5)
    kc = bpy.context.window_manager.keyconfigs.default.keymaps['Image']
    if kc:
        kmi = kc.keymap_items.new('image.page_loop', "PAGE_UP", 'PRESS')
        kmi.properties.input_page = "PAGE_UP"
        kmi = kc.keymap_items.new('image.page_loop', "PAGE_DOWN", 'PRESS')
        kmi.properties.input_page = "PAGE_DOWN"
    # print(ctime)
        
def unregisterImageLoopHotkey():
    kc = bpy.context.window_manager.keyconfigs.default.keymaps['Image']
    if kc:
        if "PAGE_UP" in kc.keymap_items.keys():
            kc.keymap_items.remove( kc.keymap_items["PAGE_UP"])
        if "PAGE_DOWN" in kc.keymap_items.keys():
            kc.keymap_items.remove( kc.keymap_items["PAGE_DOWN"])
    
def register():   
    bpy.utils.register_class(IMAGE_OT_page_loop) 
    
    # print(ctime)
    t1 = threading.Thread(target=registerImageLoopHotkey, args=("",))   # 无法启动注册，只好线程延迟
    # setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。
    # 子线程启动后，父线程也继续执行下去，当父线程执行完最后一条语句print "all over %s" %ctime()后，没有等待子线程，直接就退出了，同时子线程也一同结束。
    t1.setDaemon(True)
    t1.start()
    # t1.join()
    
    #registerImageLoopHotkey()


def unregister():
    unregisterImageLoopHotkey()
    bpy.utils.unregister_class(IMAGE_OT_page_loop)
    




if __name__ == "__main__":
    register()