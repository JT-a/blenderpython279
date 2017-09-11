import bpy


class Vistas(object):

    def __init__(self, nada=None):
        self.nada = None

    def vision(self):
        # Poniendo todos los viewports comunes en modo textured en la 263:
        # bpy.context.blend_data.screens[0].areas[4].spaces[0].viewport_shade = 'TEXTURED' # vista animation a textured
        # bpy.context.blend_data.screens[2].areas[4].spaces[0].viewport_shade = 'TEXTURED' # vista default a textured
        # bpy.context.blend_data.screens[4].areas[2].spaces[0].viewport_shade = 'TEXTURED' # vista scripting a textured

        # en la 264a:
        # 0 0 npi
        # 1 4 animation
        # 2 3 compositing
        # 3 4 default
        # 4 4 game logic

        # types:
        # enum in [‘EMPTY’, ‘VIEW_3D’, ‘GRAPH_EDITOR’, ‘OUTLINER’, ‘PROPERTIES’, ‘FILE_BROWSER’,
        # ‘IMAGE_EDITOR’, ‘INFO’, ‘SEQUENCE_EDITOR’, ‘TEXT_EDITOR’, ‘AUDIO_WINDOW’, ‘DOPESHEET_EDITOR’,
        # ‘NLA_EDITOR’, ‘SCRIPTS_WINDOW’, ‘TIMELINE’, ‘NODE_EDITOR’, ‘LOGIC_EDITOR’, ‘CONSOLE’,
        # ‘USER_PREFERENCES’], default ‘EMPTY’
        # for a in bpy.context.screen.areas:
        #    if a.type == 'VIEW_3D' or :
        #        bpy.types.SpaceView3D(a.spaces[0]).viewport_shade = 'TEXTURED'

        # screen names:
        # 3D View Full
        # Animation
        # Compositing
        # Default
        # Game Logic
        # Motion Tracking
        # Scripting
        # UV Editing
        # Video Editing
        # poner todas las vistas con view 3d en modo textured:
        nscreens = ['3D View Full', 'Animation', 'Compositing', 'Default', 'Game Logic',
                    'Motion Tracking', 'Scripting', 'UV Editing', 'Video Editing']
        for s in bpy.data.screens:
            if s.name in nscreens:
                for a in s.areas:
                    if a.type == 'VIEW_3D':
                        bpy.types.SpaceView3D(a.spaces[0]).viewport_shade = 'TEXTURED'

        #bpy.data.screens['Default'].areas[4].spaces[0].viewport_shade = 'TEXTURED'
        #bpy.data.screens['Scripting'].areas[2].spaces[0].viewport_shade = 'TEXTURED'
        #bpy.data.screens['Animation'].areas[4].spaces[0].viewport_shade = 'TEXTURED'

        # bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        bpy.data.scenes['Scene'].game_settings.material_mode = 'GLSL'
        # ponemos todas las imagenes en premultiply:
        for i in bpy.data.images[:]:
            bpy.data.images[i.name].alpha_mode = 'PREMUL'
            #bpy.data.images[i.name].use_premultiply = True
