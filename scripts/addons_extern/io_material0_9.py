bl_info = {
    "name": "Material IO",
    "author": "Jacob Morris",
    "version": (0, 9),
    "blender": (2, 74, 0),
    "location": "Properties > Materials",
    "description": "Allows The Exporting And Importing Of .bmat Files",
    "category": "Import-Export"
}

import bpy
from bpy.props import StringProperty, EnumProperty, BoolProperty
from datetime import datetime
from bpy.path import basename
from time import tzname
import xml.etree.cElementTree as ET
import ast
import operator
from os import path, makedirs, listdir, walk, remove as remove_file
from shutil import copyfile, rmtree
from xml.dom.minidom import parse as pretty_parse
import zipfile
import zlib


def make_tuple(input):
    out = []
    for i in input:
        out.append(i)
    return tuple(out)


def c_name(name):  # serialize names
    a = name.replace("/", "_")
    b = a.replace(".", "_")
    c = b.replace("\\", "_")
    d = c.replace(" ", "_")
    e = d.replace("&", "_")
    f = e.replace(",", "_")
    return f


def export_node_type(n):
    t = n.type
    is_group = False
    images = []
    # basic info
    out = {"name": c_name(n.name), "bl_idname": n.bl_idname, "label": c_name(n.label), "location": tuple(n.location), "hide": str(n.hide), "height": str(n.height), "width": str(n.width), "mute": str(n.mute), "color": make_tuple(n.color), "use_custom_color": str(n.use_custom_color)}
    if n.parent == None:
        out["parent"] = n.parent
    else:
        out["parent"] = c_name(n.parent.name)
    ns = ""
    i = ""
    o = ""
    # Input
    if t == "TEX_COORD":
        ns = ["from_dupli", n.from_dupli]
    elif t == "ATTRIBUTE":
        ns = ["attribute_name", n.attribute_name]
    elif t in ("FRESNEL", "LAYER_WEIGHT"):
        i = [0, n.inputs[0].default_value]
    elif t == "VALUE":
        o = [0, n.outputs[0].default_value]
    elif t == "RGB":
        o = [0, make_tuple(n.outputs[0].default_value)]
    elif t == "TANGENT":
        ns = ["direction_type", n.direction_type, "axis", n.axis]
    elif t == "WIREFRAME":
        ns = ["use_pixel_size", n.use_pixel_size]
        i = [0, n.inputs[0].default_value]
    elif t == "UVMAP":
        ns = ["uv_map", n.uv_map, "from_dupli", n.from_dupli]
    elif t == "LAMP":
        ns = ["lamp_object", n.lamp_object]
    elif t == "MATERIAL":
        ns = ["use_diffuse", n.use_diffuse, "use_specular", n.use_specular, "invert_normal", n.invert_normal, "material", n.material.name]
        i = [0, make_tuple(n.inputs[0].default_value), 1, make_tuple(n.inputs[1].default_value), 2, n.inputs[2].default_value, 3, make_tuple(n.inputs[3].default_value)]
    # Output
    elif t == "OUTPUT":
        i = [0, make_tuple(n.inputs[0].default_value), 1, n.inputs[1].default_value]
    # Shader
    elif t == "MIX_SHADER":
        i = [0, n.inputs[0].default_value]
    elif t in ("BSDF_DIFFUSE", "BSDF_VELVET", "EMISSION", "VOLUME_ABSORPTION"):
        i = [0, make_tuple(n.inputs[0].default_value), 1, n.inputs[1].default_value]
    elif t == "BSDF_GLOSSY":
        i = [0, make_tuple(n.inputs[0].default_value), 1, n.inputs[1].default_value]
        ns = ["distribution", n.distribution]
    elif t == "BSDF_TRANSPARENT":
        i = [0, make_tuple(n.inputs[0].default_value)]
    elif t in ("BSDF_REFRACTION", "BSDF_GLASS", "BSDF_TOON", "VOLUME_SCATTER"):
        if t in ("BSDF_REFRACTION", "BSDF_GLASS"):
            ns = ["distribution", n.distribution]
        elif t == "BSDF_TOON":
            ns = ["component", n.component]
        i = [0, make_tuple(n.inputs[0].default_value), 1, n.inputs[1].default_value, 2, n.inputs[2].default_value]
    elif t in ("BSDF_TRANSLUCENT", "AMBIENT_OCCLUSION"):
        i = [0, make_tuple(n.inputs[0].default_value)]
    elif t == "BSDF_ANISOTROPIC":
        ns = ["distribution", n.distribution]
        i = [0, make_tuple(n.inputs[0].default_value), 1, n.inputs[1].default_value, 2, n.inputs[2].default_value, 3, n.inputs[3].default_value]
    elif t == "SUBSURFACE_SCATTERING":
        ns = ["falloff", n.falloff]
        i = [0, make_tuple(n.inputs[0].default_value), 1, n.inputs[1].default_value, 2, make_tuple(n.inputs[2].default_value), 3, n.inputs[3].default_value, 4, n.inputs[4].default_value]
    elif t == "BSDF_HAIR":
        ns = ["component", n.component]
        i = [0, make_tuple(n.inputs[0].default_value), 1, n.inputs[1].default_value, 2, n.inputs[2].default_value, 3, n.inputs[3].default_value]
    # Texture
    elif t == "TEX_IMAGE":
        ns = ["image", n.image.name, "color_space", n.color_space, "projection", n.projection, "interpolation", n.interpolation]
        images.append([n.image.name, n.image.filepath])
    elif t == "TEX_ENVIROMENT":
        ns = ["image", n.image.name, "color_space", n.color_space, "projection", n.projection]
        images.append([n.image.name, n.image.filepath])
    elif t == "TEX_SKY":
        ns = ["sky_type", n.sky_type, "sun_direction", tuple(n.sun_direction), "turbitdity", n.turbidity, "ground_albedo", n.ground_albedo]
    elif t == "TEX_NOISE":
        i = [1, n.inputs[1].default_value, 2, n.inputs[2].default_value, 3, n.inputs[3].default_value]
    elif t == "TEX_WAVE":
        ns = ["wave_type", n.wave_type]
        i = [1, n.inputs[1].default_value, 2, n.inputs[2].default_value, 3, n.inputs[3].default_value, 4, n.inputs[4].default_value]
    elif t == "TEX_VORONOI":
        ns = ["coloring", n.coloring]
        i = [1, n.inputs[1].default_value]
    elif t == "TEX_MUSGRAVE":
        ns = ["musgrave_tupe", n.musgrave_type]
        i = [1, n.inputs[1].default_value, 2, n.inputs[2].default_value, 3, n.inputs[3].default_value, 4, n.inputs[4].default_value, 5, n.inputs[5].default_value, 6, n.inputs[6].default_value]
    elif t == "TEX_GRADIENT":
        ns = ["gradient_type", n.gradient_type]
    elif t == "TEX_MAGIC":
        ns = ["turbulence_depth", n.turbulence_depth]
        i = [1, n.inputs[1].default_value, 2, n.inputs[2].default_value]
    elif t == "TEX_CHECKER":
        i = [1, make_tuple(n.inputs[1].default_value), 2, make_tuple(n.inputs[2].default_value), 3, n.inputs[3].default_value]
    elif t == "TEX_BRICK":
        ns = ["offset", n.offset, "squash", n.squash, "offset_frequency", n.offset_frequency, "squash_frequency", n.squash_frequency]
        i = [1, make_tuple(n.inputs[1].default_value), 2, make_tuple(n.inputs[2].default_value), 3, make_tuple(n.inputs[3].default_value), 4, n.inputs[4].default_value, 5, n.inputs[5].default_value, 6, n.inputs[6].default_value, 7, n.inputs[7].default_value, 8, n.inputs[8].default_value]
    # Color
    elif t == "MIX_RGB":
        ns = ["blend_type", n.blend_type, "use_clamp", n.use_clamp]
        i = [0, n.inputs[0].default_value, 1, make_tuple(n.inputs[1].default_value), 2, make_tuple(n.inputs[2].default_value)]
    elif t in ("CURVE_RGB", "CURVE_VEC"):
        i = [0, n.inputs[0].default_value, 1, make_tuple(n.inputs[1].default_value)]
        # get curves
        curves = [make_tuple(n.mapping.black_level), make_tuple(n.mapping.white_level), str(n.mapping.clip_max_x), str(n.mapping.clip_max_y), str(n.mapping.clip_min_x), str(n.mapping.clip_min_y), str(n.mapping.use_clip)]
        for curve in n.mapping.curves:
            points = [curve.extend]
            for point in curve.points:
                points.append([make_tuple(point.location), point.handle_type])
            curves.append(points)
        ns = ["mapping", curves]
    elif t == "INVERT":
        i = [0, n.inputs[0].default_value, 1, make_tuple(n.inputs[1].default_value)]
    elif t == "LIGHT_FALLOFF":
        i = [0, n.inputs[0].default_value, 1, n.inputs[1].default_value]
    elif t == "HUE_SAT":
        i = [0, n.inputs[0].default_value, 1, n.inputs[1].default_value, 2, n.inputs[2].default_value, 3, n.inputs[3].default_value, 4, make_tuple(n.inputs[4].default_value)]
    elif t == "GAMMA":
        i = [0, make_tuple(n.inputs[0].default_value), 1, n.inputs[1].default_value]
    elif t == "BRIGHTCONTRAST":
        i = [0, make_tuple(n.inputs[0].default_value), 1, n.inputs[1].default_value, 2, n.inputs[2].default_value]
    # Vector
    elif t == "MAPPING":
        ns = ["vector_type", n.vector_type, "translation", tuple(n.translation), "rotation", tuple(n.rotation), "scale", tuple(n.scale), "use_min", n.use_min, "use_max", n.use_max, "min", tuple(n.min), "max", tuple(n.max)]
        i = [0, make_tuple(n.inputs[0].default_value)]
    elif t == "BUMP":
        ns = ["invert", n.invert]
        i = [0, n.inputs[0].default_value, 1, n.inputs[1].default_value]
    elif t == "NORMAL_MAP":
        ns = ["space", n.space, "uv_map", n.space]
        i = [0, n.inputs[0].default_value, 1, make_tuple(n.inputs[1].default_value)]
    elif t == "NORMAL":
        i = [0, make_tuple(n.inputs[0].default_value)]
        o = [0, make_tuple(n.outputs[0].default_value)]
    elif t == "VECT_TRANSFORM":
        ns = ["vector_type", n.vector_type, "convert_from", n.convert_from, "convert_to", n.convert_to]
        i = [0, make_tuple(n.inputs[0].default_value)]
    # Converter
    elif t == "SQUEEZE":
        i = [0, n.inputs[0].default_value, 1, n.inputs[1].default_value, 2, n.inputs[2].default_value]
    elif t == "MATH":
        ns = ["operation", n.operation, "use_clamp", n.use_clamp]
        i = [0, n.inputs[0].default_value, 1, n.inputs[1].default_value]
    elif t == "VALTORGB":
        els = []
        for i in n.color_ramp.elements:
            cur_el = [i.position, make_tuple(i.color)]
            els.append(cur_el)
        ns = ["color_ramp.color_mode", n.color_ramp.color_mode, "color_ramp.interpolation", n.color_ramp.interpolation, "color_ramp.elements", els]
        i = [0, n.inputs[0].default_value]
    elif t in ("RGBTOBW", "SEPRGB", "SEPHSV"):
        i = [0, make_tuple(n.inputs[0].default_value)]
    elif t == "VECT_MATH":
        ns = ["operation", n.operation]
        i = [0, make_tuple(n.inputs[0].default_value), 1, make_tuple(n.inputs[1].default_value)]
    elif t in ("COMBRGB", "COMBHSV", "COMBXYZ"):
        i = [0, n.inputs[0].default_value, 1, n.inputs[1].default_value, 2, n.inputs[2].default_value]
    elif t == "SEPXYZ":
        i = [0, make_tuple(n.inputs[0].default_value)]
    elif t in ("WAVELENGTH", "BLACKBODY"):
        i = [0, n.inputs[0].default_value]
    # Script
    elif t == "SCRIPT":
        ns = ["mode", n.mode, "script", n.script]
    # Group
    elif t == "GROUP":
        pos = 0
        temp = []
        is_group = True
        for i2 in n.inputs:
            if i2.type in ("RGBA", "VECTOR"):
                temp.append(pos)
                temp.append(make_tuple(i2.default_value))
            elif i2.type != ("SHADER"):
                temp.append(pos)
                temp.append(i2.default_value)
            else:
                temp.append(pos)
                temp.append("SHADER")
            pos += 1
        if temp != []:
            i = temp
        ns = ["node_tree.name", c_name(n.node_tree.name)]
    elif t == "GROUP_INPUT":
        temp = []
        for i2 in n.outputs:
            if i2.type != "CUSTOM":
                temp.append(i2.bl_idname)
                temp.append(c_name(i2.name))
            ns = ["group_input", temp]
    elif t == "GROUP_OUTPUT":
        temp = []
        for i2 in n.inputs:
            if i2.type != "CUSTOM":
                temp.append(i2.bl_idname)
                temp.append(c_name(i2.name))
        ns = ["group_output", temp]

    # Addon Specific
    elif t == "CUSTOM" and n.bl_idname == "GenericNoteNode":
        # Generic Note Node Addon
        if n.text == "" and n.text_file != "":
            text = ""
            t_file = bpy.data.texts.get(n.text_file)
            for line in t_file.lines:
                text += line.body + "\n"
        else:
            text = n.text

        ns = ["text", text]
    # layout
    out["node_specific"] = ns
    out["inputs"] = i
    out["outputs"] = o
    return out, is_group, images


def link_info(link):
    out = [c_name(link.from_node.name)]
    fr = link.from_socket.path_from_id()
    fr = fr.split(".")
    if len(fr) == 3:
        fr = fr[2]
    else:
        fr = fr[1]
    n1 = fr.index("[")
    n2 = fr.index("]")
    ind = int(fr[n1 + 1:n2])
    out.append(ind)
    out.append(c_name(link.to_node.name))
    fr = link.to_socket.path_from_id()
    fr = fr.split(".")
    if len(fr) == 3:
        fr = fr[2]
    else:
        fr = fr[1]
    n1 = fr.index("[")
    n2 = fr.index("]")
    ind = int(fr[n1 + 1:n2])
    out.append(ind)
    return out


def export_material(self, context):
    mat_list = []
    et = context.scene.export_materials_type
    folder_path = ""
    folder_name = ""
    # determine what all is being exported
    if et == "1" and context.material != None:
        mat_list.append(context.material.name)
    elif et == "2":
        for i in context.object.data.materials:
            mat_list.append(i.name)
    elif et == "3":
        for i in bpy.data.materials:
            mat_list.append(i.name)
    # export materials
    for mat_name in mat_list:
        mat = bpy.data.materials[mat_name]
        epath = context.scene.save_path_export
        if mat != None:
            if epath != "":
                # try open file
                error = True
                if "//" in epath:
                    epath = bpy.path.abspath(epath)
                if path.exists(epath):
                    error = False
                # error = True
                if error == False:
                    root = ET.Element("material")
                    names = {}
                    data = []
                    m_nodes = mat.node_tree.nodes
                    m_n = []  # main nodes
                    m_l = []  # main links
                    images = []
                    for n_main in m_nodes:  # nodes
                        out, is_group, im = export_node_type(n_main)
                        m_n.append(out)
                        images.append(im)
                        if is_group == True:  # group level 1
                            g_n = []
                            g_l = []
                            for n_group in n_main.node_tree.nodes:  # nodes
                                g_out, is_group1, im1 = export_node_type(n_group)
                                g_n.append(g_out)
                                images.append(im1)

                                if is_group1 == True:  # group level 2
                                    g_n2 = []
                                    g_l2 = []
                                    for n_group2 in n_group.node_tree.nodes:  # nodes
                                        g_out2, is_group2, im2 = export_node_type(n_group2)
                                        g_n2.append(g_out2)
                                        images.append(im2)

                                        if is_group2 == True:  # group level 3
                                            g_n3 = []
                                            g_l3 = []
                                            for n_group3 in n_group2.node_tree.nodes:  # nodes
                                                g_out3, is_group3, im3 = export_node_type(n_group3)
                                                g_n3.append(g_out3)
                                                images.append(im3)

                                                if is_group3 == True:  # group level 4
                                                    g_n4 = []
                                                    g_l4 = []
                                                    for n_group4 in n_group3.node_tree.nodes:  # nodes
                                                        g_out4, is_group4, im4 = export_node_type(n_group4)
                                                        g_n4.append(g_out4)
                                                        images.append(im4)

                                                    for l_group4 in n_group3.node_tree.links:  # links
                                                        out5 = link_info(l_group4)
                                                        g_l4.append(out5)
                                                    data.append([g_n4, g_l4])
                                                    names[c_name(n_group3.node_tree.name)] = len(data) - 1

                                            for l_group3 in n_group2.node_tree.links:  # links
                                                out4 = link_info(l_group3)
                                                g_l3.append(out4)
                                            data.append([g_n3, g_l3])
                                            names[c_name(n_group2.node_tree.name)] = len(data) - 1

                                    for l_group2 in n_group.node_tree.links:  # links
                                        out3 = link_info(l_group2)
                                        g_l2.append(out3)
                                    data.append([g_n2, g_l2])
                                    names[c_name(n_group.node_tree.name)] = len(data) - 1

                            for l_group in n_main.node_tree.links:  # links
                                out2 = link_info(l_group)
                                g_l.append(out2)
                            data.append([g_n, g_l])
                            names[c_name(n_main.node_tree.name)] = len(data) - 1

                    for l_main in mat.node_tree.links:  # links
                        out = link_info(l_main)
                        m_l.append(out)
                    data.append([m_n, m_l])
                    names["main"] = len(data) - 1

                    # write data
                    # material attribs
                    t = datetime.now()
                    date_string = "{}/{}/{} at {}:{}:{} in {}".format(t.month, t.day, t.year, t.hour, t.minute, t.second, tzname[0])
                    root.attrib = {"Render_Engine": context.scene.render.engine, "Material_Name": c_name(mat.name), "Date_Created": date_string, "Number_Of_Nodes": ""}
                    n = 0
                    num_nodes = 0
                    for group in names:
                        sub_e = ET.SubElement(root, group.replace("/", "_"))
                        d = data[names[group]]
                        sub_e_nodes = ET.SubElement(sub_e, group.replace("/", "_") + "_nodes")
                        for i in d[0]:  # nodes
                            ET.SubElement(sub_e_nodes, "node" + str(n), {"name": i["name"], "bl_idname": i["bl_idname"], "label": i["label"], "color": i["color"], "parent": str(i["parent"]), "location": i["location"],
                                                                         "height": i["height"], "width": i["width"], "mute": i["mute"], "hide": i["hide"], "inputs": i["inputs"], "outputs": i["outputs"], "node_specific": i["node_specific"], "use_custom_color": i["use_custom_color"]})
                            num_nodes += 1
                        sub_e_links = ET.SubElement(sub_e, group.replace("/", "_") + "_links")
                        for i in d[1]:  # links
                            ET.SubElement(sub_e_links, "link" + str(n), {"link_info": i})
                            n += 1
                    root.attrib["Number_Of_Nodes"] = str(num_nodes)
                    # get order of groups
                    pre_order = sorted(names.items(), key=operator.itemgetter(1))
                    order = [i[0].replace("/", "_") for i in pre_order]
                    root.attrib["Group_Order"] = str(order)
                    # images
                    img_out = []
                    save_path = epath + c_name(mat.name) + ".bmat"
                    # create folder if needed
                    if (et == "2" and len(context.object.data.materials) >= 2) or (et == "3" and len(bpy.data.materials) >= 2):
                        if not path.exists(epath + c_name(mat.name)) and folder_path == "":
                            try:
                                makedirs(epath + c_name(mat.name))
                                folder_path = epath + c_name(mat.name)
                                folder_name = c_name(mat.name)
                            except PermissionError:
                                pass
                        elif folder_path == "":
                            folder_path = epath + c_name(mat.name)
                    # set save path based on folder path
                    if folder_path != "":
                        save_path = folder_path + "\\" + c_name(mat.name) + ".bmat"
                    # image file paths
                    if context.scene.image_save_type == "1":  # absolute filepaths
                        root.attrib["Path_Type"] = "Absolute"
                        for i in images:
                            for i2 in i:
                                img_out.append([i2[0], bpy.path.abspath(i2[1])])
                    else:  # relative filepaths
                        error = False
                        for i in images:
                            if i != []:
                                error = True
                        if error == True:
                            save_path = epath + c_name(mat.name) + "\\" + c_name(mat.name) + ".bmat"
                            image_path = epath + c_name(mat.name)
                            if not path.exists(epath + c_name(mat.name)) and folder_path == "":
                                try:
                                    makedirs(epath + c_name(mat.name))
                                    folder_path = epath + c_name(mat.name)
                                    folder_name = c_name(mat.name)
                                except PermissionError:
                                    error = False
                            elif folder_path != "":
                                save_path = folder_path + "\\" + c_name(mat.name) + ".bmat"
                                image_path = folder_path
                            # make sure folder_path is correct
                            if path.exists(epath + c_name(mat.name)) and folder_path == "":
                                folder_path = epath + c_name(mat.name)
                        root.attrib["Path_Type"] = "Relative"
                        if error == True:
                            for i in images:
                                for i2 in i:
                                    i3 = bpy.path.abspath(i2[1])
                                    i2_l = i3.split("\\")
                                    img_out.append([i2[0], "//" + i2_l[len(i2_l) - 1]])
                                    if path.exists(image_path):
                                        copyfile(i3, image_path + "\\" + i2_l[len(i2_l) - 1])

                    root.attrib["Images"] = str(img_out)
                    tree = ET.ElementTree(root)
                    error2 = True
                    try:
                        tree.write(save_path)
                        error2 = False
                    except (PermissionError, FileNotFoundError):
                        self.report({"ERROR"}, "Permission Denied At That Location")
                    # if no error make text pretty
                    if error2 == False:
                        pretty_file = pretty_parse(save_path)
                        pretty_text = pretty_file.toprettyxml()
                        file = open(save_path, "w+")
                        file.write(pretty_text)
                        file.close()
                # if error
                elif error == True:
                    self.report({"ERROR"}, "Export Path Is Invalid")
    # zip folder
    if folder_path != "" and context.scene.compress_folder == True:
        if path.exists(epath + "\\" + folder_name + ".zip"):  # if file is already there, delete
            remove_file(epath + "\\" + folder_name + ".zip")
        zf = zipfile.ZipFile(epath + "\\" + folder_name + ".zip", "w", zipfile.ZIP_DEFLATED)
        for dirname, subdirs, files in walk(folder_path):
            for filename in files:
                zf.write(dirname + "\\" + filename, arcname=filename)
        zf.close()
        # delete non-compressed folder
        rmtree(folder_path)


def import_material(self, context):
    temp_epath = context.scene.save_path_import
    if temp_epath != "" and path.exists(bpy.path.abspath(temp_epath)) == True and temp_epath.endswith(".bmat"):
        # if multiple files then import them all
        import_list = []
        if context.scene.import_materials_type == "2":
            temp_path = bpy.path.abspath(temp_epath).split("\\")
            print(temp_path)
            del temp_path[len(temp_path) - 1]
            temp_end = temp_path[len(temp_path) - 1]
            del temp_path[len(temp_path) - 1]
            folder_path = ""
            for i in temp_path:
                folder_path += i + "\\"
            folder_path += temp_end
            files = listdir(folder_path)
            for i in files:
                if i.endswith(".bmat"):
                    import_list.append(folder_path + "\\" + i)
        else:
            if "//" in temp_epath:
                temp_epath = bpy.path.abspath(temp_epath)
            import_list.append(temp_epath)

        # for each .bmat file import and create material
        for file_name in import_list:
            epath = file_name
            tree = ET.parse(epath)
            root = tree.getroot()
            mat = bpy.data.materials.new(root.attrib["Material_Name"])
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            # get rid of current nodes
            for i in nodes:
                nodes.remove(i)

            # import images
            images = ast.literal_eval(root.attrib["Images"])
            errors = 0
            for i in images:
                if i[0] not in bpy.data.images:
                    if root.attrib["Path_Type"] == "Relative":
                        path_list = context.scene.save_path_import.split("\\")
                        del path_list[len(path_list) - 1]
                        path_str = ""
                        for part in path_list:
                            path_str += part + "\\"
                        try:
                            bpy.data.images.load(path_str + i[0])
                        except RuntimeError:
                            errors += 1
                    else:
                        try:
                            bpy.data.images.load(i[1])
                        except RuntimeError:
                            errors += 1
            if errors != 0:
                self.report({"ERROR"}, str(errors) + " Picture(s) Couldn't Be Loaded")

            # add new nodes
            order = ast.literal_eval(root.attrib["Group_Order"])
            for group_order in order:
                group = root.findall(group_order)[0]
                counter = 0
                # set up which node tree to use
                if group.tag == "main":
                    nt = nodes
                else:
                    nt = bpy.data.node_groups.new(group.tag, "ShaderNodeTree")
                for type in group:
                    if counter == 0:  # nodes
                        parents = []
                        for node in type:
                            node_created = True
                            # check if node is custom and if it is make sure addon is installed
                            if node.attrib["bl_idname"] == "GenericNoteNode" and "generic_note" not in bpy.context.user_preferences.addons.keys():
                                node_created = False
                                self.report({"WARNING"}, "Generic Note Node Addon Not Installed")

                            if node_created == True:
                                # parse name
                                # create node in group or just create it
                                if group.tag != "main":
                                    temp = nt.nodes.new(node.attrib["bl_idname"])
                                else:
                                    temp = nt.new(node.attrib["bl_idname"])

                                # adjust basic node attributes
                                temp.location = s_to_t(node.attrib["location"])
                                temp.name = node.attrib["name"]
                                temp.label = node.attrib["label"]
                                temp.mute = ast.literal_eval(node.attrib["mute"])
                                temp.height = float(node.attrib["height"])
                                temp.width = float(node.attrib["width"])

                                # see if custom color is in file, should be if newer version
                                try:
                                    if node.attrib["use_custom_color"] == "True":
                                        temp.use_custom_color = True
                                    temp.color = s_to_t(node.attrib["color"])
                                except:
                                    print("This File Is Older And Doesn't Contain Custom Color")

                                # parent
                                if node.attrib["parent"] != "None":
                                    parents.append([node.attrib["name"], node.attrib["parent"], s_to_t(node.attrib["location"])])

                                # hide if needed
                                if node.attrib["hide"] == "True":
                                    temp.hide = True

                                # node specific is first so that groups are set up first
                                nos = node.attrib["node_specific"]
                                if nos != "":
                                    nod = ast.literal_eval(nos)
                                    for i in range(0, len(nod), 2):
                                        att = nod[i]
                                        val = nod[i + 1]
                                        set_attributes(temp, val, att)
                                        if att in ("group_input", "group_output"):
                                            for sub in range(0, len(val), 2):
                                                sub_val = [val[sub], val[sub + 1]]
                                                if att == "group_input":
                                                    nt.inputs.new(sub_val[0], sub_val[1])
                                                else:
                                                    nt.outputs.new(sub_val[0], sub_val[1])
                                # inputs
                                ins = node.attrib["inputs"]
                                if ins != "":
                                    inp = ast.literal_eval(ins)
                                    for i in range(0, len(inp), 2):
                                        if inp[i + 1] != "SHADER":
                                            temp.inputs[inp[i]].default_value = inp[i + 1]
                                # outputs
                                ous = node.attrib["outputs"]
                                if ous != "":
                                    out = ast.literal_eval(ous)
                                    for i in range(0, len(out), 2):
                                        temp.outputs[out[i]].default_value = out[i + 1]
                        # set parents
                        for parent in parents:
                            if group.tag != "main":
                                nt.nodes[parent[0]].parent = nt.nodes[parent[1]]
                                nt.nodes[parent[0]].location = parent[2]
                            else:
                                nt[parent[0]].parent = nt[parent[1]]
                                nt[parent[0]].location = parent[2]

                    # create links
                    elif counter == 1:
                        for link in type:
                            ld = ast.literal_eval(link.attrib["link_info"])
                            if group.tag == "main":
                                o = nt[ld[0]].outputs[ld[1]]
                                i = nt[ld[2]].inputs[ld[3]]
                                mat.node_tree.links.new(o, i)
                            else:
                                o = nt.nodes[ld[0]].outputs[ld[1]]
                                i = nt.nodes[ld[2]].inputs[ld[3]]
                                nt.links.new(o, i)

                    counter += 1

            # get rid of extra groups
            for i in bpy.data.node_groups:
                if i.users == 0:
                    bpy.data.node_groups.remove(i)

            # add material to object
            if context.object != None and context.scene.add_material_auto == True:
                context.object.data.materials.append(mat)
    else:
        if epath == "" or path.exists(bpy.path.abspath(epath)) == False:
            self.report({"ERROR"}, "File Could Not Be Imported")
        else:
            self.report({"ERROR"}, "This File Is Not A .bmat File")


def s_to_t(s):
    tu = s.split(", ")
    tu[0] = tu[0].replace("(", "")
    tu[len(tu) - 1] = tu[len(tu) - 1].replace(")", "")
    out = []
    for i in tu:
        out.append(float(i))
    return out


def set_attributes(temp, val, att):
    # determine node attribute
    if att == "from_dupli":
        temp.from_dupli = val
    elif att == "attribute_name":
        temp.attribute_name = val
    elif att == "direction_type":
        temp.direction_type = val
    elif att == "axis":
        temp.axis = val
    elif att == "use_pixel_size":
        temp.use_pixel_size = val
    elif att == "uv_map":
        temp.uv_map = val
    elif att == "distribution":
        temp.distribution = val
    elif att == "component":
        temp.component = val
    elif att == "falloff":
        temp.falloff = val
    elif att == "image":
        try:
            temp.image = bpy.data.images[val]
        except KeyError:
            pass
    elif att == "color_space":
        temp.color_space = val
    elif att == "projection":
        temp.projection = val
    elif att == "interpolation":
        temp.interpolation = val
    elif att == "sky_type":
        temp.sky_type = val
    elif att == "sun_direction":
        temp.sun_direction = val
    elif att == "turbitdity":
        temp.turbitdity = val
    elif att == "ground_albedo":
        temp.ground_albedo = val
    elif att == "wave_type":
        temp.wave_type = val
    elif att == "coloring":
        temp.coloring = val
    elif att == "musgrave_type":
        temp.musgrave_type = val
    elif att == "gradient_type":
        temp.gradient_type = val
    elif att == "turbulence_depth":
        temp.turbulence_depth = val
    elif att == "offset":
        temp.offset = val
    elif att == "squash":
        temp.squash = val
    elif att == "offset_frequency":
        temp.offset_frequency = val
    elif att == "squash_frequency":
        temp.squash_frequency = val
    elif att == "blend_type":
        temp.blend_type = val
    elif att == "use_clamp":
        temp.use_clamp = val
    elif att == "vector_type":
        temp.vector_type = val
    elif att == "translation":
        temp.translation = val
    elif att == "rotation":
        temp.rotation = val
    elif att == "scale":
        temp.scale = val
    elif att == "use_min":
        temp.use_min = val
    elif att == "use_max":
        temp.use_max = val
    elif att == "min":
        temp.min = val
    elif att == "max":
        temp.max = val
    elif att == "invert":
        temp.invert = val
    elif att == "space":
        temp.space = val
    elif att == "color_ramp.color_mode":
        temp.color_ramp.color_mode = val
    elif att == "color_ramp.interpolation":
        temp.color_ramp.interpolation = val
    elif att == "color_ramp.elements":
        e = temp.color_ramp.elements
        if len(val) >= 2:
            e[0].position = val[0][0]
            e[0].color = val[0][1]
            e[1].position = val[1][0]
            e[1].color = val[1][1]
            del val[0:2]
        for el in val:
            e_temp = e.new(el[0])
            e_temp.color = el[1]
    elif att == "operation":
        temp.operation = val
    elif att == "mode":
        temp.mode = val
    elif att == "script":
        temp.script = val
    elif att == "node_tree.name":
        temp.node_tree = bpy.data.node_groups[val]
    elif att == "use_diffuse":
        temp.use_diffuse = val
    elif att == "use_specular":
        temp.use_specular = val
    elif att == "invert_normal":
        temp.invert_normal = val
    elif att == "material":
        try:
            temp.material = bpy.data.materials[val]
        except KeyError:
            pass
    elif att == "lamp_object":
        temp.lamp_object = val
    elif att == "mapping":
        # set curves
        temp.mapping.black_level = val[0]
        temp.mapping.white_level = val[1]
        temp.mapping.clip_max_x = float(val[2])
        temp.mapping.clip_max_y = float(val[3])
        temp.mapping.clip_min_x = float(val[4])
        temp.mapping.clip_min_y = float(val[5])
        if val[6] == "True":
            temp.mapping.use_clip = True
        else:
            temp.mapping.use_clip = False
        for i in range(7):
            del val[0]
        # go through each curve
        counter = 0
        for i in val:
            # i == [[location, handle_type], [location, handle_type]] so forth for however many points on curve
            # set first two points
            curves = temp.mapping.curves
            curves[counter].extend = i[0]
            del i[0]
            curves[counter].points[0].location = i[0][0]
            curves[counter].points[0].handle_type = i[0][1]
            curves[counter].points[1].location = i[1][0]
            curves[counter].points[1].handle_type = i[1][1]
            del i[0]
            del i[0]
            for i2 in i:
                temp_point = temp.mapping.curves[counter].points.new(i2[0][0], i2[0][1])
                temp_point.handle_type = i2[1]
            counter += 1
    elif att == "text":
        temp.text = val

bpy.types.Scene.import_export_mat = EnumProperty(name="Import/Export", items=(("1", "Import", ""), ("2", "Export", "")))
bpy.types.Scene.save_path_export = StringProperty(name="Export Path", subtype="DIR_PATH")
bpy.types.Scene.save_path_import = StringProperty(name="Import Path", subtype="FILE_PATH")
bpy.types.Scene.image_save_type = EnumProperty(name="Image Path", items=(("1", "Absolute Paths", ""), ("2", "Make Paths Relative", "")))
bpy.types.Scene.add_material_auto = BoolProperty(name="Add Material To Object?", default=True)
bpy.types.Scene.export_materials_type = EnumProperty(name="Export Type", items=(("1", "Selected", ""), ("2", "Current Objects", ""), ("3", "All Materials", "")))
bpy.types.Scene.import_materials_type = EnumProperty(name="Import Type", items=(("1", "Single", ""), ("2", "Multiple", "")))
bpy.types.Scene.compress_folder = BoolProperty(name="Compress Folder?")


class MaterialIOPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_material_io_panel"
    bl_label = "Material IO Panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "material"
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "import_export_mat")
        layout.separator()

        if context.scene.import_export_mat == "2":
            layout.prop(context.scene, "save_path_export")
            layout.prop(context.scene, "image_save_type")
            layout.prop(context.scene, "export_materials_type")
            layout.prop(context.scene, "compress_folder", icon="FILTER")
            layout.separator()
            layout.operator("export.material_io_export", icon="ZOOMOUT")

        else:
            layout.prop(context.scene, "save_path_import")
            layout.prop(context.scene, "import_materials_type")
            layout.prop(context.scene, "add_material_auto", icon="MATERIAL")
            layout.separator()
            layout.operator("import.material_io_import", icon="ZOOMIN")


class MaterialIOExport(bpy.types.Operator):
    bl_idname = "export.material_io_export"
    bl_label = "Export Material"

    def execute(self, context):
        export_material(self, context)
        return {"FINISHED"}


class MaterialIOImport(bpy.types.Operator):
    bl_idname = "import.material_io_import"
    bl_label = "Import Material"

    def execute(self, context):
        import_material(self, context)
        return {"FINISHED"}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
if __name__ == "__main__":
    register()
