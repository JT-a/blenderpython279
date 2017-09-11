bl_info = {
    "name": "Doshape Mesh tools",
    "author": "yhoyo (Diego Quevedo)",
    "version": (2, 0, 1),
    "blender": (2, 7, 8),
    "category": "Mesh",
    "location": "View3D > EditMode > ToolShelf",
    "wiki_url": "",
    "tracker_url": ""
}


if "bpy" in locals():
    import imp
    imp.reload(angle_bisector)
    imp.reload(CoDEmanX_pivote)
    imp.reload(edge_length_equalizer)
    imp.reload(equal_angles)
    imp.reload(ganchosybisagras)
    imp.reload(HideShow)
    imp.reload(join_bisector)
    imp.reload(join_explote)
    imp.reload(lines_origami_freestyle)
    imp.reload(modificadoresyemptys)
    imp.reload(mover)
    imp.reload(NirenYang_mesh_edges_length_angle_yi)
    imp.reload(origami_symbols)
    imp.reload(OrigamiPanel)
    imp.reload(perpendicular_bisector)
    imp.reload(perpendicular_circum_center)
    imp.reload(perpendicular_orthocenter)
    imp.reload(render_save_all)
    imp.reload(save_length_vertx_groups)
    imp.reload(separaryunircaras)
    imp.reload(triangle_bisector)
    imp.reload(unfold)
    imp.reload(view3d_idx_view2)


else:
    from. import angle_bisector
    from. import             CoDEmanX_pivote
    from. import             edge_length_equalizer
    from. import             equal_angles
    from. import             ganchosybisagras
    from. import             HideShow
    from. import             join_bisector
    from. import             join_explote
    from. import             lines_origami_freestyle 
    from. import             modificadoresyemptys
    from. import            mover
    from. import             NirenYang_mesh_edges_length_angle_yi
    from. import             origami_symbols
    from. import             OrigamiPanel
    from. import             perpendicular_bisector  
    from. import             perpendicular_circum_center 
    from. import             perpendicular_orthocenter
    from. import             render_save_all 
    from. import             save_length_vertx_groups
    from. import             separaryunircaras
    from. import             triangle_bisector
    from. import             unfold
    from. import             view3d_idx_view2

import bpy



def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()