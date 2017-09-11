import re

import bpy

from . import operators as ops


translate_iface = bpy.app.translations.pgettext_iface


def indented_layout(layout):
    sp = layout.split(0.025)
    sp.column()
    return sp.column()


def draw_separator(layout):
    row = layout.row()
    row.active = False
    row.label("…" * 100)


def draw_property(layout, obj, attr, text=None, unset=False,
                  paste=False, context_attr="", active=None):
    p = obj.bl_rna.properties[attr]
    if p.type in {'BOOLEAN', 'FLOAT', 'INT'} and not p.is_array:
        split = False
    else:
        split = True
    # is_property_set() is always True if property has get function
    is_property_set = attr in obj

    row = layout.row()
    if active is not None:
        row.active = active
    else:
        if unset and not is_property_set:
            row.active = False
    if split and text != "":
        sp = row.split(1 / 3)  # 基本的にこの比率
        row1 = sp.row()
        text_ = p.name if text is None else text
        row1.label(translate_iface(text_) + ":")
        row2 = sp.row()
        row2_sub = row2.row(align=True)
        row2_sub.prop(obj, attr, text="")
    else:
        row2 = row.row()
        row2_sub = row2.row(align=True)
        kwargs = {} if text is None else {"text": text}
        row2_sub.prop(obj, attr, **kwargs)
    if paste:
        op = row2_sub.operator(ops.WM_OT_pie_menu_text_paste.bl_idname,
                               text="", icon='PASTEDOWN')
        op.data_path = context_attr + "." + attr
    if unset and is_property_set:
        row2_sub = row2.row()
        row2_sub.alignment = 'RIGHT'
        op = row2_sub.operator(ops.WM_OT_pie_menu_property_unset.bl_idname,
                               text="", icon='X', emboss=False)
        op.data = context_attr
        op.property = attr


def verify_operator_string(text):
    return re.match("\w+\.\w+$", text) is not None


def draw_item(item, context, layout, menu, index):
    if item.show_expanded:
        main_layout = layout.box().column()
    else:
        main_layout = layout.column()
    main_layout.context_pointer_set("pie_menu_item", item)

    row = main_layout.row()
    icon = 'TRIA_DOWN' if item.show_expanded else 'TRIA_RIGHT'
    sub = row.row()
    sub.alignment = 'LEFT'
    sub.prop(item, "show_expanded", text="", icon=icon, emboss=False)
    sub.prop(item, "active", text="")

    sp = row.split(0.25)
    if not item.active:
        sp.active = False
    sub1 = sp.row()
    sp_sub = sp.split(0.6)
    sub2 = sp_sub.row()
    sub3 = sp_sub.row()

    sub1.prop(item, "type", text="")
    if item.type != 'SPACER':
        draw_property(sub2, item, "label", "", unset=True,
                      context_attr="pie_menu_item", active=True)
        sub3.prop(item, "icon")

    sub = row.row(align=True)
    sub.alignment = 'RIGHT'
    sub1 = sub.row(align=True)
    op = sub1.operator(ops.WM_OT_pie_menu_item_move.bl_idname, text="",
                       icon='TRIA_UP')
    op.direction = -1
    sub2 = sub.row(align=True)
    op = sub2.operator(ops.WM_OT_pie_menu_item_move.bl_idname, text="",
                       icon='TRIA_DOWN')
    op.direction = 1

    sub = row.row()
    sub.alignment = 'RIGHT'
    sub.operator(ops.WM_OT_pie_menu_item_remove.bl_idname, text="",
                 icon='X')

    if not item.show_expanded:
        return

    column = main_layout.column()

    if item.type == 'SPACER':
        return
    elif item.type == 'MENU':
        column.prop(item, "menu")
    elif item.type == 'OPERATOR':
        _ = item.ensure_argument
        row = column.row()
        is_valid = verify_operator_string(item.operator)
        if item.operator != "":
            if not is_valid:
                row.alert = True
        row.prop(item, "operator")
        if is_valid and item.operator_arguments:
            box = column.box()
            flow = box.column_flow(2)
            for arg in item.operator_arguments:
                arg.draw_ui(context, flow)
    else:
        draw_property(column, item, "execute_string", "Execute",
                      paste=True, context_attr="pie_menu_item")
        draw_property(column, item, "poll_string", "Poll", unset=True,
                      paste=True, context_attr="pie_menu_item",
                      active=True)

        draw_property(column, item, "description", unset=True, paste=True,
                      context_attr="pie_menu_item", active=True)
        column.prop(item, "menu")
        column.prop(item, "undo_push")
        column.prop(item, "shortcut")
        # draw_property(column, self, "translate", unset=True,
        #               context_attr="pie_menu_item")
        column.prop(item, "translate")


def draw_menu(menu, context, layout):
    if menu.show_expanded:
        main_layout = layout.box().column()
    else:
        main_layout = layout.column()
    main_layout.context_pointer_set("pie_menu", menu)

    row = main_layout.row()
    icon = 'TRIA_DOWN' if menu.show_expanded else 'TRIA_RIGHT'
    sub = row.row()
    sub.alignment = 'LEFT'
    sub.prop(menu, "show_expanded", text="", icon=icon, emboss=False)
    sub.prop(menu, "active", text="")
    sub = row.row()
    if not menu.active:
        sub.active = False
    sub.prop(menu, "label", text="")
    sub2 = sub.row()
    """:type: bpy.types.UILayout"""
    if not menu.idname:
        sub2.alert = True
    sub2.prop(menu, "name", text="ID Name")
    sub = row.row()
    sub.alignment = 'RIGHT'
    sub.operator(ops.WM_OT_pie_menu_menu_remove.bl_idname, text="",
                 icon='X')

    if not menu.show_expanded:
        return

    column = main_layout.column()

    row = column.row()
    split = row.split()
    sp_column1 = split.column()
    sp_column2 = split.column()

    draw_property(sp_column1, menu, "draw_type",
                  unset=True, context_attr="pie_menu")
    draw_property(sp_column1, menu, "icon_scale")
    draw_property(sp_column1, menu, "icon_expand")
    draw_property(sp_column1, menu, "radius",
                  unset=True, context_attr="pie_menu")

    draw_property(sp_column1, menu, "translate")
    draw_property(sp_column1, menu, "item_order")

    sp_column2.label("Quick Action:")
    draw_property(sp_column2, menu, "quick_action", text="",
                  context_attr="pie_menu")
    sub = sp_column2.row()
    if menu.quick_action != 'FIXED':
        sub.active = False
    draw_property(sub, menu, "quick_action_index", context_attr="pie_menu")

    sp_column2.label("Highlight:")
    draw_property(sp_column2, menu, "highlight", text="",
                  context_attr="pie_menu")
    sub = sp_column2.row()
    if menu.highlight != 'FIXED':
        sub.active = False
    draw_property(sub, menu, "highlight_index", context_attr="pie_menu")

    draw_separator(column)

    draw_property(column, menu, "poll_string", "Poll Function", paste=True,
                  context_attr="pie_menu")
    draw_property(column, menu, "init_string", "Init Function", paste=True,
                  context_attr="pie_menu")

    draw_separator(column)

    for mod in ["", "shift", "ctrl", "alt", "oskey"]:
        if mod == "":
            show_expanded_attr = "show_expanded_items"
        else:
            show_expanded_attr = "show_expanded_" + mod
        show_expanded = getattr(menu, show_expanded_attr)
        if show_expanded:
            column_items = main_layout.box().column()
        else:
            column_items = main_layout.column()
        row = column_items.row()
        icon = 'TRIA_DOWN' if show_expanded else 'TRIA_RIGHT'
        row.prop(menu, show_expanded_attr, text="", icon=icon,
                 emboss=False)

        use_items = True
        if mod == "":
            row.label("Items:")
        else:
            text = ("Cmd" if mod == "oskey" else mod.title()) + " Items:"
            sub = row.row(align=True)
            if not getattr(menu, "use_" + mod):
                sub.active = False
                use_items = False
            sub.prop(menu, "use_" + mod, text="")
            sub.label(text)

        if not show_expanded:
            continue
        column_items_ = indented_layout(column_items)
        if mod == "":
            items = menu.menu_items
        else:
            items = getattr(menu, mod + "_items")
        for i, item in enumerate(items):
            col = column_items_.column()
            if not use_items:
                col.active = False
            draw_item(item, context, col, menu, i)

        row = column_items_.row()
        row.alignment = 'LEFT'
        op = row.operator(ops.WM_OT_pie_menu_item_add.bl_idname,
                          text="Add Item", icon='ZOOMIN')
        op.modifier = mod
