# BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
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
# END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Particle Link",
    "author": "Luca Scheller",
    "version": (1, 0),
    "blender": (2, 7, 3),
    "location": "Particle System Tab",
    "description": "Generate Curves Between Particles",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Particle"}

import bpy
from bpy.app.handlers import persistent
from random import randrange


def is_even(num):
    if (num % 2 == 0):
        return True
    else:
        return False


def get_KeyedParticle_Location(Particle):
    frame_current = bpy.context.scene.frame_current
    frame_start = bpy.context.scene.frame_start
    if len(Particle.particle_keys) == 0:
        return (0, 0, 0)
    # Get Blend Keys
    from_blend_index = -1
    for y in range(len(Particle.particle_keys)):
        PK = Particle.particle_keys[y]
        if (PK.time - 1) <= frame_current:
            from_blend_index = y
        else:
            break
    to_blend_index = from_blend_index + 1
    # Calc Location (Different if first target hasn't been reached yet.)
    if from_blend_index == -1:
        PK_location = Particle.particle_keys[0].location
    elif from_blend_index == (len(Particle.particle_keys) - 1):
        PK_location = Particle.particle_keys[(len(Particle.particle_keys) - 1)].location
    else:
        PK_F = Particle.particle_keys[from_blend_index]
        PK_T = Particle.particle_keys[to_blend_index]
        location_blend_ratio = (frame_current - (PK_F.time - 1)) / ((PK_T.time - 1) - (PK_F.time - 1))
        PK_location = ((PK_T.location - PK_F.location) * location_blend_ratio) + PK_F.location

    return PK_location


def UPDATE_ALL(self, context):
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)
    bpy.context.scene.update()


def PL_Addon_First_ExecutionFunction(scene):  # Add-on UserPref Activation

    # Safety Restrictions Override via Scene Update Handler --> Hack / Not a clean solution
    bpy.app.handlers.scene_update_post.remove(PL_Addon_First_ExecutionFunction)

    for x in bpy.data.curves:
        if x.PL_Number != -1:
            for y in bpy.data.objects:
                if y.data != None:
                    if y.data.name == x.name:
                        Object_Curve = y
                        Object_ParticleEmitter = y.constraints[0].target
                        for z in Object_ParticleEmitter.particle_systems:
                            if z.settings.PL_SettingsCollection.ID != "None":
                                temp_ID = eval(z.settings.PL_SettingsCollection.ID)
                                if x.PL_Number in temp_ID:
                                    ParticleSystem = z
                                    ParticleSystem_Settings = z.settings
                                    break
                        ID_Path = Object_ParticleEmitter.particle_systems.active.settings.PL_SettingsCollection
                        temp_ID = eval(ID_Path.ID)
                        break

            # Frame Handler Creation
            FrameHandlerFunction = PL_FrameHandlerBuilder(Object_ParticleEmitter, ParticleSystem, ParticleSystem_Settings, Object_Curve, x, x.PL_Number)
            bpy.app.handlers.frame_change_post.append(FrameHandlerFunction)

    # Update
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)
    bpy.context.scene.update()

    print("Particle Link | Add-on Activated")


@persistent
def PL_Addon_ExecutionFunction(scene):  # Add-on Scene Load -> All Globals/Frame Handlers are cleared on scene load automatically

    for x in bpy.data.curves:
        if x.PL_Number != -1:
            for y in bpy.data.objects:
                if y.data != None:
                    if y.data.name == x.name:
                        Object_Curve = y
                        Object_ParticleEmitter = y.constraints[0].target
                        for z in Object_ParticleEmitter.particle_systems:
                            if z.settings.PL_SettingsCollection.ID != "None":
                                temp_ID = eval(z.settings.PL_SettingsCollection.ID)
                                if x.PL_Number in temp_ID:
                                    ParticleSystem = z
                                    ParticleSystem_Settings = z.settings
                                    break
                        ID_Path = Object_ParticleEmitter.particle_systems.active.settings.PL_SettingsCollection
                        temp_ID = eval(ID_Path.ID)
                        break

            # Frame Handler Creation
            FrameHandlerFunction = PL_FrameHandlerBuilder(Object_ParticleEmitter, ParticleSystem, ParticleSystem_Settings, Object_Curve, x, x.PL_Number)
            bpy.app.handlers.frame_change_post.append(FrameHandlerFunction)

    # Update
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)
    bpy.context.scene.update()

    print("Particle Link | Add-on Activated")

# Operators


def PL_FrameHandlerBuilder(Object_ParticleEmitter, ParticleSystem, ParticleSystem_Settings, Object_Curve, Curve_Curve, ID):
    def PL_FrameHandler(scene):

        try:
            ParticleSystem.settings.PL_SettingsCollection
            Object_Curve.data.splines
        except:
            # Reset UI
            try:
                temp_ID = eval(ParticleSystem_Settings.PL_SettingsCollection.ID)
                temp_ID.remove(Curve_Curve.PL_Number)
                if len(temp_ID) == 0:
                    ParticleSystem_Settings.PL_SettingsCollection.ID = "None"
                else:
                    ParticleSystem_Settings.PL_SettingsCollection.ID = str(temp_ID)
            except:
                pass
            # Remove Frame Handlers
            for x in bpy.app.handlers.frame_change_post:
                if int(x.__name__[3:]) == Curve_Curve.PL_Number:
                    bpy.app.handlers.frame_change_post.remove(x)
            # Remove Curve Object
            try:
                for x in bpy.data.scenes:
                    x.objects.unlink(Object_Curve)
                bpy.data.objects.remove(Object_Curve)
            except:
                pass
            # Remove Curve
            Curve_Curve.user_clear()
            bpy.data.curves.remove(Curve_Curve)
            return

        # Create Vars
        scene = bpy.context.scene
        ParticleSystem_Type = ParticleSystem_Settings.type
        ParticleSystem_PhysicsType = ParticleSystem_Settings.physics_type
        Curve_Type = ParticleSystem_Settings.PL_SettingsCollection.Curve_Type
        Curve_Connection_Type = ParticleSystem_Settings.PL_SettingsCollection.Curve_Connection_Type
        Curve_Seed = eval(ParticleSystem_Settings.PL_SettingsCollection.Curve_Seed)[1]
        Curve_Seed_MRC_Recalc = eval(ParticleSystem_Settings.PL_SettingsCollection.Curve_Seed)[0]
        Count = ParticleSystem_Settings.count
        Max_Random_Connections = ParticleSystem_Settings.PL_SettingsCollection.Curve_Max_Random_Connections
        Middle_Point_Use = ParticleSystem_Settings.PL_SettingsCollection.Middle_Point_Use
        Middle_Point_Size = ParticleSystem_Settings.PL_SettingsCollection.Middle_Point_Size
        if Middle_Point_Use:
            Point_Count = 2
        else:
            Point_Count = 1

        if ParticleSystem_Type == "EMITTER":

            if Curve_Type == "BEZIER":
                # Remove Curves
                for x in Object_Curve.data.splines:
                    Object_Curve.data.splines.remove(x)

                # Generate Curve Points
                LoopRange = ParticleSystem_Settings.count
                Point_Counter = 0
                Create_Curve = True
                for x in range(LoopRange - 1):
                    Particle = ParticleSystem.particles[x]
                    Particle_Next = ParticleSystem.particles[x + 1]
                    if Particle.alive_state == "ALIVE" and Particle_Next.alive_state == "ALIVE":
                        if ParticleSystem_PhysicsType == "KEYED":
                            PK_location = get_KeyedParticle_Location(Particle)
                            PK_Next_location = get_KeyedParticle_Location(Particle_Next)
                        else:
                            PK_location = Particle.location
                            PK_Next_location = Particle_Next.location
                        if Create_Curve == True:
                            Curve = Object_Curve.data.splines.new(Curve_Type)
                            Curve.bezier_points[0].co[:3] = PK_location - Object_ParticleEmitter.location
                            Create_Curve = False
                        Curve.bezier_points.add(Point_Count)
                        Point_Counter += Point_Count
                        if Middle_Point_Use == True:
                            Curve.bezier_points[Point_Counter - 1].co[:3] = ((PK_location + PK_Next_location) / 2) - Object_ParticleEmitter.location
                            Curve.bezier_points[Point_Counter - 1].radius = Middle_Point_Size
                        Curve.bezier_points[Point_Counter].co[:3] = PK_Next_location - Object_ParticleEmitter.location

                # Recalc Handles
                if Create_Curve == False:
                    for x in Curve.bezier_points:
                        x.handle_left_type = "AUTO"
                        x.handle_right_type = "AUTO"

            if Curve_Type == "POLY":
                if Curve_Connection_Type == "ORDERED":
                    # Remove Curves
                    for x in Object_Curve.data.splines:
                        Object_Curve.data.splines.remove(x)

                    # Generate Curve Points
                    LoopRange = ParticleSystem_Settings.count
                    for x in range(LoopRange - 1):
                        Particle = ParticleSystem.particles[x]
                        Particle_Next = ParticleSystem.particles[x + 1]
                        if Particle.alive_state == "ALIVE" and Particle_Next.alive_state == "ALIVE":
                            if ParticleSystem_PhysicsType == "KEYED":
                                PK_location = get_KeyedParticle_Location(Particle)
                                PK_Next_location = get_KeyedParticle_Location(Particle_Next)
                            else:
                                PK_location = Particle.location
                                PK_Next_location = Particle_Next.location
                            Curve = Object_Curve.data.splines.new(Curve_Type)
                            Curve.points[0].co[:3] = PK_location - Object_ParticleEmitter.location
                            Point_Counter = 0
                            Curve.points.add(Point_Count)
                            Point_Counter += Point_Count
                            if Middle_Point_Use == True:
                                Curve.points[Point_Counter - 1].co[:3] = ((PK_location + PK_Next_location) / 2) - Object_ParticleEmitter.location
                                Curve.points[Point_Counter - 1].radius = Middle_Point_Size
                            Curve.points[Point_Counter].co[:3] = PK_Next_location - Object_ParticleEmitter.location
                elif Curve_Connection_Type == "RANDOM":
                    # Recalc Seed if necessary
                    if Curve_Seed == None or len(Curve_Seed) != Count or Curve_Seed_MRC_Recalc != Max_Random_Connections:
                        PL_Seed(Count, Max_Random_Connections, ParticleSystem_Settings.PL_SettingsCollection)
                        Curve_Seed = eval(ParticleSystem_Settings.PL_SettingsCollection.Curve_Seed)[1]

                    # Remove Curves
                    for x in Object_Curve.data.splines:
                        Object_Curve.data.splines.remove(x)

                    # Generate Curve Points
                    LoopRange = ParticleSystem_Settings.count
                    for x in range(LoopRange - 1):
                        Particle = ParticleSystem.particles[x]
                        if Particle.alive_state == "ALIVE":
                            PK_location = Particle.location
                            Curve_Seed_Alive = []
                            for y in Curve_Seed[x]:
                                if ParticleSystem.particles[y].alive_state == "ALIVE":
                                    Curve_Seed_Alive.append(y)
                            for y in Curve_Seed_Alive:
                                if ParticleSystem_PhysicsType == "KEYED":
                                    PK_location = get_KeyedParticle_Location(Particle)
                                    PK_Next_location = get_KeyedParticle_Location(ParticleSystem.particles[y])
                                else:
                                    PK_Next_location = ParticleSystem.particles[y].location
                                Curve = Object_Curve.data.splines.new(Curve_Type)
                                Curve.points[0].co[:3] = PK_location - Object_ParticleEmitter.location
                                Point_Counter = 0
                                Curve.points.add(Point_Count)
                                Point_Counter += Point_Count
                                if Middle_Point_Use == True:
                                    Curve.points[Point_Counter - 1].co[:3] = ((PK_location + PK_Next_location) / 2) - Object_ParticleEmitter.location
                                    Curve.points[Point_Counter - 1].radius = Middle_Point_Size
                                Curve.points[Point_Counter].co[:3] = PK_Next_location - Object_ParticleEmitter.location

        else:
            # Remove Curves
            for x in Object_Curve.data.splines:
                Object_Curve.data.splines.remove(x)

    PL_FrameHandler.__name__ = "PL_" + str(ID)
    return PL_FrameHandler


def PL_Seed(Count, Max_Random_Connections, PL_SettingsCollection):
    # Generate Seed
    Seed = {}
    for x in range(Count):
        Seed[x] = []
        MRC = randrange(1, Max_Random_Connections + 1)
        for y in range(MRC):
            Seed[x].append(randrange(Count))

    MRC_Recalc = Max_Random_Connections
    Output = [MRC_Recalc, Seed]
    # Write Seed
    PL_SettingsCollection.Curve_Seed = str(Output)


class PL_Generate_ParticleLinks(bpy.types.Operator):
    bl_idname = "pl.generate_particlelinks"
    bl_label = "Generate Particle Links"
    bl_options = {"REGISTER"}

    def execute(self, context):

        scene = bpy.context.scene

        # Safe ID
        bpy.data.scenes[0].PL_Count += 1
        ID_Path = bpy.context.active_object.particle_systems.active.settings.PL_SettingsCollection
        temp_ID = eval(ID_Path.ID)
        if temp_ID == None:
            temp_ID = set()
            temp_ID.add(bpy.data.scenes[0].PL_Count)
            ID_Path.ID = str(temp_ID)
        else:
            temp_ID.add(bpy.data.scenes[0].PL_Count)
            ID_Path.ID = str(temp_ID)

        # Curve Object Creation
            # Safe Selection
        Safe_Selection = bpy.context.selected_objects
        Object_ParticleEmitter = bpy.context.active_object

        # Create Curve
        bpy.ops.curve.primitive_bezier_curve_add(radius=1, location=Object_ParticleEmitter.location)
        Object_Curve = scene.objects.active
        Object_Curve.name = "Particle_Linker_" + Object_ParticleEmitter.name
        Object_Curve.data.name = "Particle_Linker_" + Object_ParticleEmitter.name
        Object_Curve.use_extra_recalc_data = True
        Object_Curve.data.PL_Number = bpy.data.scenes[0].PL_Count
        Object_Curve.data.fill_mode = "FULL"
        Object_Curve.data.bevel_depth = 0.25
        Object_Curve.data.use_uv_as_generated = True
        Object_Curve.constraints.new("COPY_LOCATION")
        Object_Curve.constraints[0].target = Object_ParticleEmitter
        Object_Curve.constraints[0].use_offset = True
        Object_Curve.location = (0, 0, 0)
        # Restore Selection
        Object_Curve.select = False
        scene.objects.active = Object_ParticleEmitter
        for x in Safe_Selection:
            x.select = True

        # Frame Handler Creation
        ParticleSystem = Object_ParticleEmitter.particle_systems.active
        ParticleSystem_Settings = ParticleSystem.settings
        FrameHandlerFunction = PL_FrameHandlerBuilder(Object_ParticleEmitter, ParticleSystem, ParticleSystem_Settings, Object_Curve, Object_Curve.data, bpy.data.scenes[0].PL_Count)
        bpy.app.handlers.frame_change_post.append(FrameHandlerFunction)

        # Update
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)
        bpy.context.scene.update()

        return {"FINISHED"}


class PL_Generate_ParticleLinks_RandomSeed(bpy.types.Operator):
    bl_idname = "pl.generate_particlelinks_randomseed"
    bl_label = "Generate Particle Links Random Seed"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        # Vars
        PL_SettingsCollection = bpy.context.active_object.particle_systems.active.settings.PL_SettingsCollection
        ParticleSystem_Settings = bpy.context.active_object.particle_systems.active.settings
        Count = ParticleSystem_Settings.count
        Max_Random_Connections = PL_SettingsCollection.Curve_Max_Random_Connections

        # Generate / Write Seed
        PL_Seed(Count, Max_Random_Connections, PL_SettingsCollection)

        return {"FINISHED"}

# Operators

# Panels


class PL_Panel(bpy.types.Panel):
    bl_idname = "pl.particlelink_panel"
    bl_label = "Particle Link"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "particle"

    def draw(self, context):

        if bpy.context.active_object.particle_systems.active != None:
            scene = bpy.context.scene
            ParticleSettings = bpy.context.active_object.particle_systems.active.settings
            layout = self.layout
            row = layout.row()
            col = row.column()

            if ParticleSettings.type == "EMITTER":
                if ParticleSettings.PL_SettingsCollection.ID == "None":
                    col.operator("pl.generate_particlelinks", icon='CONSTRAINT', text="Generate Particle Links")
                else:
                    col.operator("pl.generate_particlelinks", icon='CONSTRAINT', text="Generate Particle Links")
                    col.separator()
                    col.label(text="Curve Type")
                    row = col.row()
                    row.prop(ParticleSettings.PL_SettingsCollection, "Curve_Type", expand=True)
                    if ParticleSettings.PL_SettingsCollection.Curve_Type == "POLY":
                        col.separator()
                        col.label(text="Curve Connection Type")
                        row = col.row()
                        row.prop(ParticleSettings.PL_SettingsCollection, "Curve_Connection_Type", expand=True)
                        if ParticleSettings.PL_SettingsCollection.Curve_Connection_Type == "RANDOM":
                            col.operator("pl.generate_particlelinks_randomseed", icon='FILE_REFRESH', text="Refresh Seed")
                            col.prop(ParticleSettings.PL_SettingsCollection, "Curve_Max_Random_Connections")
                    col.separator()
                    row = col.row()
                    row.prop(ParticleSettings.PL_SettingsCollection, "Middle_Point_Use")
                    row = row.row()
                    row.prop(ParticleSettings.PL_SettingsCollection, "Middle_Point_Size")
                    row.enabled = False
                    if ParticleSettings.PL_SettingsCollection.Middle_Point_Use == True:
                        row.enabled = True
            elif ParticleSettings.type == "HAIR":
                col.label(text="Particle linking only works with particles.", icon='ERROR')


# Panels

# Addon Before Execution Definitions

Curve_Type_Items = [
    ("BEZIER", "Bezier", ""),
    ("POLY", "Poly", "")
]

Curve_Connection_Type_Items = [
    ("ORDERED", "Ordered", ""),
    ("RANDOM", "Random", "")
]


class PL_Settings(bpy.types.PropertyGroup):
    ID = bpy.props.StringProperty(default="None")
    Curve_Type = bpy.props.EnumProperty(items=Curve_Type_Items, default="POLY", update=UPDATE_ALL)
    Curve_Connection_Type = bpy.props.EnumProperty(items=Curve_Connection_Type_Items, default="ORDERED", update=UPDATE_ALL)
    Curve_Seed = bpy.props.StringProperty(default="[1,None]", update=UPDATE_ALL)
    Curve_Max_Random_Connections = bpy.props.IntProperty(name='Maximum Connections Per Particle', default=3, min=1, description='Maximum Number of Random Connections Per Particle', update=UPDATE_ALL)
    Middle_Point_Use = bpy.props.BoolProperty(name='Use Middle Point', default=False, description='Add Middle Point for Detailed Adjustment', update=UPDATE_ALL)
    Middle_Point_Size = bpy.props.FloatProperty(name='Middle Point Size', default=1, min=0, description='Middle Point Size', update=UPDATE_ALL)

# Addon Before Execution Definitions


def register():

    # Panels, Ops & Vars
    bpy.utils.register_class(PL_Panel)
    bpy.utils.register_class(PL_Generate_ParticleLinks)
    bpy.utils.register_class(PL_Generate_ParticleLinks_RandomSeed)
    bpy.utils.register_class(PL_Settings)
    bpy.types.ParticleSettings.PL_SettingsCollection = bpy.props.PointerProperty(type=PL_Settings)
    bpy.types.Scene.PL_Count = bpy.props.IntProperty(default=0, min=0)
    bpy.types.Curve.PL_Number = bpy.props.IntProperty(default=-1, min=0)

    # App Handlers
    bpy.app.handlers.load_post.append(PL_Addon_ExecutionFunction)
    bpy.app.handlers.scene_update_post.append(PL_Addon_First_ExecutionFunction)  # Post Load Hack


def unregister():

    # Panels, Ops & Vars
    bpy.utils.unregister_class(PL_Panel)
    bpy.utils.unregister_class(PL_Generate_ParticleLinks)
    bpy.utils.unregister_class(PL_Generate_ParticleLinks_RandomSeed)
    bpy.utils.unregister_class(PL_Settings)

    # App Handlers
    bpy.app.handlers.load_post.remove(PL_Addon_ExecutionFunction)

    # PL Frame Handlers
    for x in bpy.app.handlers.frame_change_post:
        if x.__name__[:3] == "PL_":
            bpy.app.handlers.frame_change_post.remove(x)

if __name__ == "__main__":
    register()
