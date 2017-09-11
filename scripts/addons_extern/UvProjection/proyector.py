import bpy


class Proyector(object):

    def __init__(self, ob=None):
        self.ob = None

    def proyectorcillo(self, ob):
        # if 'Proyector' in bpy.context.scene.objects:
        if 'Proyector' in bpy.data.objects:
            # al parecer al borrar con x y con supr no elimina los objetos de bpy.data.objects, les hace un unlink
            # por eso, si existe le digo que le haga link para que vuelva a aparecer el proyector:
            try:
                bpy.context.scene.objects.link(bpy.data.objects['Proyector'])
            except:
                pass
        else:
            # creamos el proyector:
            bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, -9, 0), rotation=(1.5708, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            ob = bpy.context.active_object  # obteniendo objeto activo
            ob.name = "Proyector"  # el nombre del objeto camara
            ob.data.name = "Proyector"  # el nombre de la camara real o subobjeto del objeto camara

            #current_camera = bpy.context.scene.camera
            #bpy.context.scene.camera = ob

            bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            emp = bpy.context.active_object  # obteniendo objeto activo
            emp.name = "Locator"

            #bpy.context.scene.camera = current_camera

            bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
            myproyector = bpy.data.objects[str(ob.name)]
            myproyector.select = True  # lo selecciono
            bpy.context.scene.objects.active = ob  # lo hago objeto activo
            bpy.ops.object.constraint_add(type='CHILD_OF')
            bpy.context.object.constraints['Child Of'].target = bpy.data.objects["Locator"]

            # emparentado:
            #myobject = bpy.data.objects[str(ob.name)]
            #myobject.select = True
            #myobject = bpy.data.objects[str(emp.name)]
            #myobject.select = True
            # bpy.ops.object.parent_set(type='OBJECT')

            bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
            myplocator = bpy.data.objects[str(emp.name)]
            myplocator.select = True
            bpy.context.scene.objects.active = myplocator  # lo hago objeto activo

        if 'Locator' not in bpy.data.objects:
            bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            emp = bpy.context.active_object  # obteniendo objeto activo
            emp.name = "Locator"

            #bpy.ops.object.select_name(name='Proyector', extend=True)
            myobject = bpy.data.objects['Proyector']
            myobject.select = True
            #bpy.ops.object.select_name(name=emp.name, extend=True)
            myobject = bpy.data.objects[str(emp.name)]
            myobject.select = True

            bpy.ops.object.parent_set(type='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')  # deseleccionamos todo
            #bpy.ops.object.select_name(name=emp.name, extend=False)
            myobject = bpy.data.objects[str(emp.name)]
            myobject.select = True

        xloc = bpy.data.objects['Locator']
        xloc.show_x_ray = True
