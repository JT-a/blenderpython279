#
# The MIT License (MIT)
#
# Copyright (c) 2014 ishidourou
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# (参考日本語訳：http://sourceforge.jp/projects/opensource/wiki/licenses%2FMIT_licenseより）
#
# Copyright (c) 2014 ishidourou
#
# 以下に定める条件に従い、本ソフトウェアおよび関連文書のファイル（以下「ソフトウェア」）
# の複製を取得するすべての人に対し、ソフトウェアを無制限に扱うことを無償で許可します。
# これには、ソフトウェアの複製を使用、複写、変更、結合、掲載、頒布、サブライセンス、
# および/または販売する権利、およびソフトウェアを提供する相手に同じことを許可する権利も
# 無制限に含まれます。
#
# 上記の著作権表示および本許諾表示を、ソフトウェアのすべての複製または重要な部分に記載
# するものとします。
#
# ソフトウェアは「現状のまま」で、明示であるか暗黙であるかを問わず、何らの保証もなく
# 提供されます。ここでいう保証とは、商品性、特定の目的への適合性、および権利非侵害に
# ついての保証も含みますが、それに限定されるものではありません。 作者または著作権者は、
# 契約行為、不法行為、またはそれ以外であろうと、ソフトウェアに起因または関連し、あるいは
# ソフトウェアの使用またはその他の扱いによって生じる一切の請求、損害、その他の義務に
# ついて何らの責任も負わないものとします。
#
#####################################
# Pocket Mesh Maker
#	   v.1.5
#  (c)ishidourou 2014
####################################

#!BPY

import bpy
import subprocess
import codecs
import os
import platform
import re
from bpy.props import *

bl_info = {
    "name": "Pocket Mesh Maker",
    "author": "ishidourou",
    "version": (1, 5),
    "blender": (2, 65, 0),
    "location": "View3D > Toolbar and View3D",
    "description": "PocketMeshMaker",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": 'Mesh'}


class mes():
    title = ('Pocket Mesh Maker', 'ポケットメッシュを作成')
    btn01 = ('Generate Pocket Mesh Add-On', 'ポケットメッシュアドオンを生成')
    addontitle = ('Pocket Mesh', 'ポケットメッシュ')
    addonpath = ('Add-on File path', 'アドオンの保存先:')
    adfile = ('Add-on File name:', 'アドオンのファイル名:')
    adauthor = ('Add-on Author name:', 'アドオンの作者名:')
    adtitle = ('Add-on Title:', 'アドオンのタイトル:')
    apply = ('Apply in advance', '事前に変換を適用')
    finmes = ('was added.', 'が追加されました')
    notmesh = ('Please select mesh object.', 'メッシュオブジェクトを選択してください')
    misstype = ('Please inpyt only Alphanumeric. ', 'ファイル名は半角英数字を入力してください')
    missdir = ('Destination folder does not exist.', '保存先のフォルダがありません')


def lang():
    system = bpy.context.user_preferences.system
    if system.use_international_fonts:
        if system.language == 'ja_JP':
            return 1
    return 0

pmmk_wmessage = 'Please Select Edges.'


class PmmDialog(bpy.types.Operator):
    bl_idname = "pmm.dialog"
    bl_label = 'message'
    bl_options = {'REGISTER'}

    my_message = 'message'

    def execute(self, context):
        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        global pmmk_wmessage
        self.layout.label(pmmk_wmessage)


def error(message):
    global pmmk_wmessage
    pmmk_wmessage = message
    bpy.ops.pmm.dialog('INVOKE_DEFAULT')


class PMMakerPanel(bpy.types.Panel):
    bl_context = "objectmode"
    bl_category = "Create"
    bl_label = mes.title[lang()]
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        self.layout.operator("pm.maker")


def make_script(addontitle, addonclass, addonid, addonfile, authername, apply):

    slist = bpy.context.selected_objects
    ct = 0
    for i in slist:
        if i.type == 'MESH':
            ct = 1
            sob = i
            break
    if ct == 0:
        error(mes.notmesh[lang()])
        return False

    if apply:
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, texture=False, animation=False)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    datstr = ''
    names = ''

    f = codecs.open(addonfile, "w", "utf-8")
    a_part = u"####################################\n# " + addontitle + "\n#\t   v.1.5\n#  (c)" + authername + "\n####################################\n\n#!BPY\nimport bpy\nimport math\nfrom bpy.props import *\n\nbl_info = {\n\t\"name\": \"" + addontitle + "\",\n\t\"author\": \"" + authername + "\",\n\t\"version\": (1, 5),\n\t\"blender\": (2, 65, 0),\n\t\"location\": \"View3D > Toolbar and View3D\",\n\t\"description\": \"" + addonclass + "\",\n\t\"warning\": \"\",\n\t\"wiki_url\": \"\",\n\t\"tracker_url\": \"\",\n\t\"category\": 'POCKET_MESH'}\n\n\n\nclass mes():\n\ttitle = ('" + addontitle + "','" + addontitle + "')\n\tbtn01 = ('Put Mesh','メッシュを配置')\n\tmeshlist = ('Mesh List:','メッシュリスト:')\n\tscale = ('Scale:','拡大率:')\n\trx = ('X Rotation:','X軸回転:')\n\try = ('Y Rotation:','Y軸回転:')\n\trz = ('Z Rotation:','Z軸回転:')\n\tapply = ('Apply Transform','変換を適用する')\n\tput_all = ('Put All','全てを配置')\n\ndef lang():\n\tsystem = bpy.context.user_preferences.system\n\tif system.use_international_fonts:\n\t\tif system.language == 'ja_JP':\n\t\t\treturn 1\n\treturn 0\n\t\n#\tMenu in tools region\nclass " + addonclass + "Panel(bpy.types.Panel):\n\tbl_context = \"objectmode\"\n\tbl_category = \"Create\"\n\tbl_label = mes.title[lang()]\n\tbl_space_type = \"VIEW_3D\"\n\tbl_region_type = \"TOOLS\"\n \n\tdef draw(self, context):\n\t\tself.layout.operator(\"" + addonid + "\")\n\nclass Mymesh:\n\tdef __init__(self, name, loc, data, mode):\n\t\tself.name = name\n\t\tself.loc = loc\n\t\tself.pos = data[0]\n\t\tself.edg = data[1]\n\t\tself.fcs = data[2]\n\t\tself.mode = mode\n\n\tdef set_mode(self,value):\n\t\tself.mode = value\n\tdef set_name(self,sname):\n\t\tself.name = sname\n\n\ndef draw_mymesh(obj, scale, rx, ry, rz, apply):\n\n\tbpy.ops.object.select_all(action='DESELECT')\n\tme = bpy.data.meshes.new(obj.name)\n\tob = bpy.data.objects.new(obj.name, me)\n\n\tob.location = bpy.context.scene.cursor_location\n\tbpy.context.scene.objects.link(ob)\n\tif obj.mode == 'EDGE' or obj.fcs == []:\n\t\tme.from_pydata(obj.pos,obj.edg,[])\n\telse:\n\t\tme.from_pydata(obj.pos,[],obj.fcs)\n\tme.update()\n\n\tbpy.context.scene.objects.active = ob\n\tob.select = True\n\tbpy.ops.object.editmode_toggle()\n\tbpy.ops.mesh.select_all(action='SELECT')\n\tbpy.ops.object.editmode_toggle()\n\n\tbpy.ops.transform.resize(value=(scale, scale, scale))\n\n\trx = rx*math.pi/180\n\try = ry*math.pi/180\n\trz = rz*math.pi/180\n\tbpy.ops.transform.rotate(value=rx, axis=(1, 0, 0), constraint_axis=(True, False, False))\n\tbpy.ops.transform.rotate(value=ry, axis=(0, 0, 1), constraint_axis=(False, True, False))\n\tbpy.ops.transform.rotate(value=rz, axis=(0, 0, 1), constraint_axis=(False, False, True))\n\n\tif apply:\n\t\tbpy.ops.object.transform_apply(location=False, rotation=True, scale=True)\n\n\n#---- main ------\nclass " + addonclass + "(bpy.types.Operator):\n\tbl_idname = \"" + addonid + "\"\n\tbl_label = mes.btn01[lang()]\n\tbl_options = {'REGISTER','UNDO'}\n\n\tmlist = []\n#=>\n"
    f.write(a_part)

    for i in slist:
        bpy.context.scene.objects.active = i
        i.select = True

        loc = "(%f, %f, %f)" % (i.location.x - sob.location.x, i.location.y - sob.location.y, i.location.z - sob.location.z)
        if i.type == 'MESH':
            if len(i.data.vertices) and len(i.data.edges):
                fclist = []

                oname = i.name
                names += oname + ' '
                mesh = i.data

                f.write('\tdata=[[')

                for vertex in mesh.vertices:
                    f.write("(%f,%f,%f)," % (vertex.co.x, vertex.co.y, vertex.co.z))
                f.seek(-1, 1)
                f.write("],[")

                for face in mesh.edges:
                    f.write("(")
                    for index in face.vertices:
                        f.write("%d," % index)
                    f.seek(-1, 1)
                    f.write("),")
                f.seek(-1, 1)
                f.write("],[")

                if len(mesh.polygons):
                    for face in mesh.polygons:
                        f.write("(")
                        for index in face.vertices:
                            f.write("%d," % index)
                        f.seek(-1, 1)
                        f.write("),")
                    f.seek(-1, 1)
                f.write("]]\n")
                b_part = u"\tmm = Mymesh('" + oname + "', " + loc + ", data, 'FACE')\n\tmlist.append(mm)\n\n"
                f.write(b_part)

    c_part = u"#<=\n\tln = len(mlist)\n\titm = [[None for col in range(3)] for row in range(ln)]\n\tct = 0\n\tfor i in mlist:\n\t\titm[ct] = (str(ct), i.name, str(ct))\n\t\tct += 1\n\t\n\tmy_enum = EnumProperty(name=mes.meshlist[lang()],items = itm, default = itm[0][0])\n\tmy_scale = bpy.props.FloatProperty(name=mes.scale[lang()],min=0,max=1000,default=1)\n\tmy_rx = bpy.props.FloatProperty(name=mes.rx[lang()],min=-360,max=360,default=0)\n\tmy_ry = bpy.props.FloatProperty(name=mes.ry[lang()],min=-360,max=360,default=0)\n\tmy_rz = bpy.props.FloatProperty(name=mes.rz[lang()],min=-360,max=360,default=0)\n\tmy_apply = BoolProperty(name=mes.apply[lang()],default=False)\n\tmy_all = BoolProperty(name=mes.put_all[lang()],default=False)\n\n\tdef execute(self, context):\n\t\tenumv = self.my_enum\n\t\tscalev = self.my_scale\n\t\trx = self.my_rx\n\t\try = self.my_ry\n\t\trz = self.my_rz\n\t\tapply = self.my_apply\n\t\tall = self.my_all\n\t\tobjlist = []\n\n\t\tif all:\n\t\t\tfor i in self.mlist:\n\t\t\t\tdraw_mymesh(i, scalev, rx, ry, rz, apply)\n\t\t\t\tbpy.ops.transform.translate(value=i.loc)\n\t\t\t\tobjlist.append(bpy.context.object)\n\n\n\t\t\tfor i in objlist:\n\t\t\t\ti.select = True\n\n\t\telse:\n\t\t\tdraw_mymesh(self.mlist[int(enumv)], scalev, rx, ry, rz, apply)\n\n\t\treturn{'FINISHED'}\n\n\tdef invoke(self, context, event):\n\t\twm = context.window_manager\n\t\treturn wm.invoke_props_dialog(self)\n\n#\tRegistration\ndef register():\n\tbpy.utils.register_class(" + addonclass + "Panel)\n\tbpy.utils.register_class(" + addonclass + ")\n\ndef unregister():\n\tbpy.utils.unregister_class(" + addonclass + "Panel)\n\tbpy.utils.unregister_class(" + addonclass + ")\n\nif __name__ == \"__main__\":\n\tregister()\n"
    f.write(c_part)
    f.close()

    error(names + mes.finmes[lang()])
    return 1

#---- main ------


class PMMaker(bpy.types.Operator):

    bl_idname = "pm.maker"
    bl_label = mes.btn01[lang()]
    bl_options = {'REGISTER', 'UNDO'}

    pmname = 'pocketmesh'

    my_adpath = bpy.props.StringProperty(name=mes.addonpath[lang()], default='')
    my_file = bpy.props.StringProperty(name=mes.adfile[lang()], default=pmname)
    my_aname = bpy.props.StringProperty(name=mes.adauthor[lang()], default='BlenderUser')
    my_title = bpy.props.StringProperty(name=mes.adtitle[lang()], default=mes.addontitle[lang()])
    my_apply = BoolProperty(name=mes.apply[lang()], default=False)

    def execute(self, context):

        title = self.my_title
        adpath = self.my_adpath
        fname = self.my_file
        author = self.my_aname
        apply = self.my_apply

        regexp = re.compile(r'^[0-9A-Za-z]+$')

        if regexp.search(fname) == None:
            error(mes.misstype[lang()])
            return{'FINISHED'}

        my_class = 'PMSH' + fname
        my_id = 'pm.sh' + fname
        my_id = my_id.lower()
        fname += '.py'

        if adpath == '':
            adpath = os.path.join(bpy.utils.user_resource('SCRIPTS'), "addons")
        else:
            if os.path.isdir(adpath) == False:
                error(mes.missdir[lang()])
                return{'FINISHED'}

        addon_filename = os.path.join(adpath, fname)
        make_script('PM: ' + title, my_class, my_id, addon_filename, author, apply)

        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

#	Registration


def register():
    bpy.utils.register_class(PMMakerPanel)
    bpy.utils.register_class(PMMaker)
    bpy.utils.register_class(PmmDialog)


def unregister():
    bpy.utils.unregister_class(PMMakerPanel)
    bpy.utils.unregister_class(PMMaker)
    bpy.utils.unregister_class(PmmDialog)

if __name__ == "__main__":
    register()
