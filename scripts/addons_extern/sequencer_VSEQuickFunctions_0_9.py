# VSE Quick Functions
#
# This script is designed to make Blender's VSE easier to use by implementing features
# often found in other video editors, or features that I find useful as a video editor.
# Features that this script includes:
#
# QuickContinuous -
#   Setting can be found in the sequence editor 'View' menu.
#   When Quickcontinuous is enabled, it will constantly run and detect sequence
#       editing events, and adjust sequences as needed.
#   Many of the other features require this to be enabled to work: Parenting,
#       Ripple, Fade auto-adjustments and Proxy settings.
#
# QuickFades -
#   Can be found in the sequence editor properties panel, or by pressing the
#        'f' key over the sequencer.
#   Fade Length - The target length for fade editing or creating.
#   Set Fadein/Set Fadeout - Allows easy adding, detecting and changing of
#       fade in/out.  The script will check the curve for any fades already
#       applied to the sequence (either manually or by the script), and edit them
#       if found.  Can apply the same fade to multiple sequences at once.
#   Transition Type - Selects the type of transition for adding.
#   Crossfade Prev/Next Sequence - Allows easy adding of transitions between sequences.
#       Will simply find an overlapping sequence from the active sequence and add
#       a transition.
#   Smart Cross to Prev/Next - Adjust the length of the active sequence and the
#       next sequence to create a transition of the target fade length.  Will also
#       attempt to avoid extending the sequences past their end points if possible.
#   When QuickContinuous is running, fade in and outs will be automatically fixed
#       when a sequence start or end frame is adjusted.
#
# QuickSnaps -
#   Can be found in the sequence editor 'Strip' menu, or by pressing the
#       's' key over the sequencer.
#   Allows quickly snapping sequences to each other or moving the cursor to sequences.
#   Cursor To Nearest Second - Will round the cursor position to the nearest
#       second, based on framerate.
#   Cursor To Beginning/End Of Sequence - Will move the cursor to the beginning or
#       end of the active sequence.
#   Selected To Cursor - The same as the 'shift-s' shortcut in the VSE.
#   Sequence Beginning/End To Cursor - Moves all selected sequences so their
#       beginning/end is at the cursor.
#   Sequence To Previous/Next Sequence - Detects the previous or next sequence in the
#       timeline from the active sequence.  Moves the active sequence so it's beginning
#       or end matches the previous sequence's end or beginning.
#
# QuickZooms -
#   Can be found in the sequence editor 'View' menu, or by pressing the
#       'z' key over the sequencer.
#   Zoom All - Zooms the sequencer out to show all sequences.
#   Zoom Selected - Zooms the sequencer to show the currently selected sequence(s).
#   Zoom Cursor - Zooms the sequencer to an amount of frames around the cursor.
#   Size - How many frames should be shown by using Zoom Cursor.
#       Changing this value will automatically activate Zoom Cursor.
#   Zoom ______ - Several preset zoom values for convenience.
#
# QuickParents -
#   Can be found in the sequence editor properties panel under "Edit Strip", or by
#       pressing the 'Ctrl-p' key over the sequencer.
#   This implements a parenting system for sequences, allowing easy
#       selecting of multiple related sequences.  Note that any relationships will
#       be broken if a sequence is renamed!
#   Children or Parents of selected sequence will be shown at the top of
#       the Panel, or bottom of the Menu.
#   Select Children or Parent - Selects any related sequences to the current sequence.
#       Also can be accomplished with the shortcut 'Shift-p'.
#   Clear Children or Parent - Removes relationships from selected sequence.
#   Set Active As Parent - If multiple sequences are selected, this will set
#       selected sequences as children of the active (last selected) sequence.
#   Auto-Select Sequence Children - Works with QuickContinuous by automatically
#       selecting any child sequences when a sequence is selected.  Note that this
#       may slow down the framerate of the sequencer a bit.
#   Cut/Move Sequence Children - Works with  QuickContinuous by finding any children
#       of a moved or cut sequence and performing the same operation on them.
#       If the sequence is cut, any children under the cursor will be cut as well,
#       and the script will duplicate parent/child relationships to the
#       cut sequences.  If the parent sequence is resized and a child sequences have
#       the same endpoints, they will be resized as well.
#   Auto-Parent New Audio To Video - Works with QuickContinuous to automatically parent
#       an audio sequence to the video of an imported movie clip that includes both.
#   All parenting features require QuickContinuous to be enabled.
#
# QuickList -
#   Can be found in the sequence editor properties panel.
#   Displays a list of loaded sequences and allows you to change various settings.
#   Display Mode - Changes the way the sequences are displayed in the panel:
#       Standard - The largest mode, displays all information on 2 or more lines.
#       Standard Compact - Like Standard, but does not display child sequences,
#           and meta strip sub-sequences.
#       One Line - Displays most information on one line.
#       One Line Compact - Like One Line, but does not display child sequences,
#           and meta strip sub-sequences.
#   Select All - Like pressing the 'a' key in the sequencer, this will toggle
#       the selection of all sequences.
#   Sort by - Reorders the list based on timeline position, title, or length.
#   Eye Icon - Mutes/unmutes sequence.
#   Padlock Icon - Locks/unlocks sequence.
#   Sequence Type Button - Allows selecting and deselecting sequence.
#   Sequence Title - Allows editing of sequence name.
#   Len/Pos - Move or resize the sequence.
#   Proxy settings - Enable/disable proxy and sizes.
#   In non-compact modes, the child sequences will be displayed here, as well as
#       any sub-sequences in a meta strip.
#   If a sequence is an effect, and it is applied to another sequence,
#       it will be indented and placed below it's parent.
#
# QuickProxy -
#   Can be found in the sequence editor properties panel, under 'Proxy/Timecode'
#   Can automatically enable proxy settings, and automatically generate proxies
#       on imported sequences.
#   Enable Proxy On Import - The below settings will be applied to imported/added
#       sequences that can utilize them.
#   Auto-Build Proxy On Import - Proxies will start being generated as soon as
#       a file is imported.
#   Percentage Values - Enable proxies for these resolutions.
#   Quality - Video quality setting for enabled proxies.
#   Note that QuickProxy requires QuickContinuous to be enabled to function.
#
# QuickMarkers -
#   Can be found in the sequence editor properties panel, also Alt-M in the sequencer.
#   Add markers to the timeline using name presets.
#   New Preset - Enter a marker title into the text field, and click the + button.
#   Place A Marker - Click on a marker button once a preset has been added.
#   Remove A Preset - Click the X button next to a preset to remove it.
#   Deselect New Markers - With this enabled, newly created markers will be
#       unselected to prevent accidental moving.
#
# QuickRipple -
#   Can be found in the sequence editor view menu, 'Ripple Editing Mode'.
#   When enabled, this will automatically move all clips following the active clip
#       when the active clip is deleted, or the ending point is changed.
#       Currently, adjusting the start point has no effect due to the way the
#       grab operator works.
#   QuickRipple features require QuickContinuous to be enabled to function.
#
#
#
# Known Bugs:
#   Proxy building progress bar is not shown for some reason...
#   Copy/paste a parent/child pair does not update parent relationships
#   When moving the edge of a parent clip that is a different length than a child clip, setting the edge to the child clips edge will 'grab' that child clip's edge as well...
#   When moving a parent clip, if a child gets 'pushed' to another channel, it wont return to the original channel. Ideally, it should remember where it is in relation to its parent and try to return to that
#
# Todo:
#   Option to correct the active strip when cutting (if you cut with mouse on the right, active strip remains on left even tho right is selected)
#   Improve QuickRipple - if possible make start frame editing work. If possible, implement sequence moving (strips auto-adjusted when strip is 'popped' out of the sequence, or dropped in)
#   Possible: Context-aware popup, depending on what is selected or what was just done, options change
#   Possible: QuickCuts - trim left/right of strip at edit line, ripple trim left/right,
#   Possible: UnCut/Merge feature: if two strips have the same source, and are next to each other and have the same offset, delete one and extend the other to fill that space
#   Reimplement cursor following if it is possible to determine zoom level of the sequencer area
#       This could allow for overlay details or functions as well such as fades, displaying the current zoom window size in minutes/seconds,
#       Also this could allow for remembering previous zoom, and returning to it
#
# Changelog:
#   0.86
#       Fixed transparency in title scenes
#       Fixed no sequences in a scene throwing an error
#       Added auto-parenting of movie sequences with sound
#       Cleaned up quicklist, meta strips now list sub-sequences, effects are indented under the parent sequence
#   0.87
#       Continuous functions should work inside meta strips now
#       Fixed a couple small bugs
#   0.88
#       Added drop shadows to titler
#       Added color picker and material duplicate button to titler
#       Hopefully fixed continuous functions from throwing errors when no strips are loaded
#       Improved adding/changing fades, added a clear fades button
#   0.89
#       Fixed zoom to cursor not working inside meta strips
#       Fixed zoom to cursor not working in Blender 2.74
#       Fixed child sequences being moved twice if they were manually moved along with the parent
#       Recoded continuous function - parenting is more reliable, all cut sequences are detected and parented properly, fades are now moved when a sequence is resized
#       Removed continuous snapping, snapping is now built-in in blender as of 2.73
#       Added quick zoom presets
#       Added settings to hide different Quick panels
#       Added QuickParenting option to auto-select child sequences, also child sequences' endpoints will be moved when a parent is resized if they match up.
#       Added font loading button to QuickTitler
#       Added templates to QuickTitler
#       Added display modes for QuickList
#       Cleaned and commented code
#   0.89.1
#       Removed an extra check in the modal function that wasn't doing anything but slowing down the script
#   0.9
#       Split QuickTitling off into its own addon
#       Cleaned up variables
#       Improved child sequence auto-select: handle selections are now duplicated as well
#       Parenting is now stored in a sequence variable of .parent
#       Rewrote continuous modal operator to hopefully fix incorrect detections of add/cut/resize/move
#       Now uses addon preferences to enable or disable features (list, fades and parenting)
#       Edit panel displays fade in/out
#       Parenting panel is simplified and merged into the edit panel
#       Improved crossfade adding
#       Added Quickproxy to automatically enable proxes on imported sequences
#       Added Quickmarkers to add markers to the timeline with a preset name
#       Rewrote the continuous function AGAIN, to now be a handler - this means movement/resizing of child clips is now in real-time, and fades are continuously updated.  Also, switching scenes shouldnt have any adverse affect on the script.
#       New variables added to sequence strips to help track changes: .last_frame_final_start, .last_frame_start, .last_frame_final_duration, .last_select, and .new
#       Child sequences can now be automatically deleted when deleting a parent
#       Renaming a clip should now fix the relationships
#       QuickRipple implemented to enable timeline ripple-style editing
#       Improved performance by only checking sequences in current editing scope (not checking sequences inside meta strips if not in that meta strip)


import bpy
import math
import os
from bpy.app.handlers import persistent


bl_info = {
    "name": "VSE Quick Functions",
    "description": "Improves functionality of the sequencer by adding new menus for snapping, adding fades, zooming, sequence parenting, ripple editing, and playback speed.",
    "author": "Hudson Barkley (Snu)",
    "version": (0, 9, 0),
    "blender": (2, 77, 0),
    "location": "Sequencer Panels; Sequencer Menus; Sequencer S, F, Z, Ctrl-P, Shift-P, Alt-M Shortcuts",
    "wiki_url": "none yet",
    "category": "Sequencer"
}


# Functions used by various features

# Proxy Panel Addon function
def proxy_panel(self, context):
    prefs = context.user_preferences.addons[__name__].preferences
    scene = context.scene
    vseqf = scene.vseqf
    layout = self.layout
    if prefs.proxy:
        row = layout.row()
        row.separator()
        row = layout.row()
        row.prop(vseqf, 'enableproxy')
        row = layout.row()
        row.prop(vseqf, 'buildproxy')

        row = layout.row(align=True)
        row.prop(vseqf, "proxy25", toggle=True)
        row.prop(vseqf, "proxy50", toggle=True)
        row.prop(vseqf, "proxy75", toggle=True)
        row.prop(vseqf, "proxy100", toggle=True)

        row = layout.row()
        row.prop(vseqf, "proxyquality")


# Sequencer Edit Panel Addon function
def edit_panel(self, context):
    prefs = context.user_preferences.addons[__name__].preferences

    scene = context.scene
    vseqf = scene.vseqf
    layout = self.layout
    if prefs.fades:
        active_sequence = scene.sequence_editor.active_strip
        fadein = fades(sequence=active_sequence, fade_length=0, type='in', mode='detect')
        fadeout = fades(sequence=active_sequence, fade_length=0, type='out', mode='detect')

        row = layout.row()
        if fadein > 0:
            row.label("Fadein: " + str(round(fadein)) + " Frames")
        else:
            row.label("No Fadein Detected")
        if fadeout > 0:
            row.label("Fadeout: " + str(round(fadeout)) + " Frames")
        else:
            row.label("No Fadeout Detected")

    if prefs.parenting:
        sequence = scene.sequence_editor.active_strip
        selected = bpy.context.selected_sequences
        children = find_children(sequence)
        parent = find_parent(sequence)

        box = layout.box()
        # List relationships for active sequence
        row = box.row()
        if parent:
            row = box.row()
            split = row.split(percentage=.8, align=True)
            split.label("Parent: " + parent.name)
            split.operator('vseqf.quickparents', text='', icon="BORDER_RECT").action = 'selectparent'
            split.operator('vseqf.quickparents', text='', icon="X").action = 'clearparent'
        if (len(children) > 0):
            row = box.row()
            split = row.split(percentage=.8, align=True)
            subsplit = split.split(percentage=.1)
            subsplit.prop(scene.vseqf, 'expandedchildren', icon="TRIA_DOWN" if scene.vseqf.expandedchildren else "TRIA_RIGHT", icon_only=True, emboss=False)
            subsplit.label("Children: " + children[0].name)
            split.operator('vseqf.quickparents', text='', icon="BORDER_RECT").action = 'selectchildren'
            split.operator('vseqf.quickparents', text='', icon="X").action = 'clearchildren'
            if scene.vseqf.expandedchildren:
                index = 1
                while index < len(children):
                    row = box.row()
                    split = row.split(percentage=.1)
                    split.label()
                    split.label(children[index].name)
                    index = index + 1

        row = box.row()
        split = row.split()
        if (len(selected) <= 1):
            split.enabled = False
        split.operator('vseqf.quickparents', text='Set Active As Parent').action = 'add'
        split = row.split()
        split.prop(vseqf, 'selectchildren')
        row = box.row()
        row.prop(vseqf, 'children')
        row.prop(vseqf, 'deletechildren')
        row = box.row()
        row.prop(vseqf, 'autoparent')


# Draws the menu for settings
def draw_quicksettings_menu(self, context):
    layout = self.layout
    layout.prop(context.scene.vseqf, 'ripple')
    layout.prop(context.scene.vseqf, 'continuousenable')
    # layout.menu('vseqf.settings_menu', text="Quick Settings")

# Find sequences after a frame


def sequences_after_frame(sequences, frame, add_locked=True, add_parented=True, add_effect=True):
    update_sequences = []
    for seq in sequences:
        if seq.frame_final_start >= frame:
            # sequence starts after frame
            if (not seq.lock) or add_locked:
                # always adding locked, or sequence is not locked
                if add_parented or (not find_parent(seq)):
                    # always adding parents, or parent not found
                    if add_effect or (not hasattr(seq, 'input_1')):
                        update_sequences.append(seq)
    return update_sequences


# Returns an array of sequences sorted by distance from a sequence
def find_close_sequence(sequences, selected_sequence, direction, mode='overlap'):
    #'sequences' is a list of sequences to search through
    #'selected_sequence' is the active sequence
    #'direction' needs to be 'next' or 'previous'
    #'mode'
    #   if mode is overlap, will only return overlapping sequences
    #   if mode is channel, will only return sequences in sequence's channel
    #   if mode is set to other, all sequences are considered

    overlap_nexts = []
    overlap_previous = []
    nexts = []
    previous = []

    # iterate through sequences to find all sequences to one side of the selected sequence
    for current_sequence in sequences:
        # don't bother with sound type sequences
        if (current_sequence.type != 'SOUND'):
            if current_sequence.frame_final_start >= selected_sequence.frame_final_end:
                # current sequence is after selected sequence
                # dont append if channel mode and sequences are not on same channel
                if (mode == 'channel') & (selected_sequence.channel != current_sequence.channel):
                    pass
                else:
                    nexts.append(current_sequence)
            elif current_sequence.frame_final_end <= selected_sequence.frame_final_start:
                # current sequence is before selected sequence
                # dont append if channel mode and sequences are not on same channel
                if (mode == 'channel') & (selected_sequence.channel != current_sequence.channel):
                    pass
                else:
                    previous.append(current_sequence)

            elif (current_sequence.frame_final_start > selected_sequence.frame_final_start) & (current_sequence.frame_final_start < selected_sequence.frame_final_end) & (current_sequence.frame_final_end > selected_sequence.frame_final_end):
                # current sequence startpoint is overlapping selected sequence
                overlap_nexts.append(current_sequence)
            elif (current_sequence.frame_final_end > selected_sequence.frame_final_start) & (current_sequence.frame_final_end < selected_sequence.frame_final_end) & (current_sequence.frame_final_start < selected_sequence.frame_final_start):
                # current sequence endpoint is overlapping selected sequence
                overlap_previous.append(current_sequence)

    nexts_all = nexts + overlap_nexts
    previous_all = previous + overlap_previous
    if direction == 'next':
        if mode == 'overlap':
            if len(overlap_nexts) > 0:
                return min(overlap_nexts, key=lambda overlap: abs(overlap.channel - selected_sequence.channel))
            else:
                # overlap mode, but no overlaps
                return False
        else:
            if len(nexts_all) > 0:
                return min(nexts_all, key=lambda next: (next.frame_final_start - selected_sequence.frame_final_end))
            else:
                # no next sequences
                return False
    else:
        if mode == 'overlap':
            if len(overlap_previous) > 0:
                return min(overlap_previous, key=lambda overlap: abs(overlap.channel - selected_sequence.channel))
            else:
                return False
        else:
            if len(previous_all) > 0:
                return min(previous_all, key=lambda prev: (selected_sequence.frame_final_start - prev.frame_final_end))
            else:
                return False

# Converts a frame number to a standard timecode in the format HH:MM:SS:FF


def timecode_from_frames(frame, framespersecond, levels=0, subsecondtype='miliseconds'):
    # the 'levels' variable limits the larger timecode elements
    #   a levels = 3 will return MM:SS:FF
    #   a levels = 0 will auto format the returned value to cut off any zero divisors
    #   a levels = 4 will return the entire timecode every time
    # the 'subsecondtime' variable determines the fraction denominator for the FF section,
    #   the default of 'miliseconds' will return the last value as a division of 100 (0-99)
    #   setting it to 'frames' will return the last value as a division of the frames per second

    # ensure the levels value is sane
    if (levels > 4):
        levels = 4

    # set the sub second divisor type
    if (subsecondtype == 'frames'):
        subseconddivisor = framespersecond
    else:
        subseconddivisor = 100

    # check for negative values
    if frame < 0:
        negative = True
        frame = abs(frame)
    else:
        negative = False

    # calculate divisions, starting at largest and taking the remainder of each to calculate the next smaller
    totalhours = math.modf(float(frame) / framespersecond / 60.0 / 60.0)
    totalminutes = math.modf(totalhours[0] * 60)
    remainingseconds = math.modf(totalminutes[0] * 60)
    hours = int(totalhours[1])
    minutes = int(totalminutes[1])
    seconds = int(remainingseconds[1])
    subseconds = int(round(remainingseconds[0] * subseconddivisor))

    # format and return the time value
    time = str(hours).zfill(2) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2) + ':' + str(subseconds).zfill(2)[-2:]
    if levels == 0:
        # cut off any larger divisors that are zero
        while (time[0:3] == '00:'):
            time = time[3:len(time)]
        if negative:
            time = '-' + time
        return time
    else:
        time = time.split(':', 4 - levels)[-1]
        if negative:
            time = '-' + time
        return time


# Functions related to continuous update

def update_sequence(sequence):
    sequence.last_frame_final_start = sequence.frame_final_start
    sequence.last_frame_start = sequence.frame_start
    sequence.last_frame_final_duration = sequence.frame_final_duration
    sequence.last_select = sequence.select
    sequence.last_channel = sequence.channel
    sequence.last_name = sequence.name
    sequence.new = False

# New continuous function


@persistent
def vseqf_continuous(scene):
    vseqf = scene.vseqf
    if vseqf.continuousenable:
        if vseqf.skip_index < scene.vseqf_skip_interval:
            vseqf.skip_index += 1
        elif vseqf.skip_index >= scene.vseqf_skip_interval:
            vseqf.skip_index = 0
            prefs = bpy.context.user_preferences.addons[__name__].preferences
            if scene.sequence_editor:
                if len(scene.sequence_editor.meta_stack) > 0:
                    # inside a meta strip
                    sequencer = scene.sequence_editor.meta_stack[-1]
                else:
                    # not inside a meta strip
                    sequencer = scene.sequence_editor
                if hasattr(sequencer, 'sequences'):
                    sequences = sequencer.sequences
                else:
                    sequences = []

                if vseqf.lastsequencer != str(sequencer):
                    # sequencer was changed (went in/out of a meta strip) only update variables on this loop
                    frame_current = scene.frame_current
                    scene.total_sequences = len(sequences)
                    vseqf.lastsequences.clear()

                    for sequence in sequences:
                        sequenceinfo = vseqf.lastsequences.add()
                        sequenceinfo.name = sequence.name
                        sequenceinfo.frame_final_start = sequence.frame_final_start
                        sequenceinfo.frame_final_end = sequence.frame_final_end

                    vseqf.lastsequencer = str(sequencer)

                else:
                    new_sequences = []
                    cut_sequences = []
                    cut_to_sequences = []
                    moved_sequences = []
                    resized_sequences = []
                    selected_sequences = []
                    removed_sequences = []
                    renamed_sequences = []
                    copied_sequences = []

                    frame_current = scene.frame_current

                    last_total_sequences = scene.total_sequences
                    total_sequences = len(sequences)
                    if total_sequences > last_total_sequences:
                        added_sequences = True
                        deleted_sequences = False
                    elif total_sequences == last_total_sequences:
                        added_sequences = False
                        deleted_sequences = False
                    else:
                        added_sequences = False
                        deleted_sequences = True
                    scene.total_sequences = total_sequences
                    if deleted_sequences:
                        for lastsequence in vseqf.lastsequences:
                            if lastsequence.name not in sequences:
                                removed_sequences.append([lastsequence.name, lastsequence.frame_final_start, lastsequence.frame_final_end, lastsequence.parent, lastsequence.do_not_ripple])

                    vseqf.lastsequences.clear()

                    # need to detect: added, resized, moved, cut
                    for sequence in sequences:
                        sequenceinfo = vseqf.lastsequences.add()
                        sequenceinfo.name = sequence.name
                        sequenceinfo.frame_final_start = sequence.frame_final_start
                        sequenceinfo.frame_final_end = sequence.frame_final_end
                        if sequence.parent == 'do_not_ripple':
                            sequenceinfo.do_not_ripple = True
                        if sequence.new:
                            # this sequence has just been added
                            new_sequences.append(sequence)
                            update_sequence(sequence)
                        if sequence.select:
                            selected_sequences.append(sequence)
                        if (sequence.frame_start != sequence.last_frame_start) or (sequence.channel != sequence.last_channel):
                            # this sequence was just moved
                            difference = sequence.frame_start - sequence.last_frame_start
                            channel_difference = sequence.channel - sequence.last_channel
                            moved_sequences.append([sequence, difference, channel_difference])
                        if sequence.frame_final_duration != sequence.last_frame_final_duration:
                            # this sequence was just resized or cut
                            if added_sequences:
                                # there are more sequences, this must have been cut
                                if sequence.frame_final_start != sequence.last_frame_final_start:
                                    # this is a cut to sequence
                                    cut_to_sequences.append([sequence, sequence.last_frame_final_start, sequence.last_frame_final_duration])
                                else:
                                    # this is a cut from sequence
                                    cut_sequences.append([sequence, sequence.last_frame_final_start, sequence.last_frame_final_duration])
                            else:
                                # same number of sequences, this must have been resized
                                resized_sequences.append([sequence, sequence.last_frame_final_start, sequence.last_frame_final_duration])
                        elif (sequence.last_name != sequence.name) and sequence.last_name:
                            # this sequence was renamed or copied, but not cut
                            if sequence.last_name in sequences:
                                # last name still exists, must have been copied
                                copied_sequences.append([sequence, sequence.last_name])
                            else:
                                renamed_sequences.append([sequence, sequence.last_name])

                        update_sequence(sequence)

                    # Deal with copied sequences
                    for sequenceinfo in copied_sequences:
                        sequence, last_name = sequenceinfo
                        # todo: if both child and parent are copied/pasted, update parenting variable to reflect this

                    # Deal with renamed sequences
                    for sequenceinfo in renamed_sequences:
                        sequence, last_name = sequenceinfo
                        children = find_children(last_name, name=True)
                        for child in children:
                            child.parent = sequence.name

                    # Deal with moved sequences
                    if scene.vseqf.ripple:
                        for sequenceinfo in moved_sequences:
                            sequence, difference, channel_difference = sequenceinfo
                            # todo: ripple moving clips

                    if prefs.parenting and scene.vseqf.children and not scene.vseqf.selectchildren:
                        for sequenceinfo in moved_sequences:
                            # move any child sequences along with the parent, if they are not selected as well
                            sequence, difference, channel_difference = sequenceinfo
                            if sequence.name in sequencer.sequences:
                                children = find_children(sequence)
                                for child in children:
                                    if not child.select:
                                        child.frame_start = child.frame_start + difference
                                        # child.channel = child.channel + channel_difference

                    # Deal with resized sequences
                    if prefs.parenting or prefs.fades or scene.vseqf.ripple:
                        for sequenceinfo in resized_sequences:
                            sequence, last_frame_final_start, last_frame_final_duration = sequenceinfo
                            start_frame = last_frame_final_start
                            end_frame = start_frame + last_frame_final_duration
                            if scene.vseqf.ripple:
                                if sequence == scene.sequence_editor.active_strip:
                                    # if ripple mode, move sequences after the resized one up or down the timeline
                                    sequences_to_check = sequencer.sequences

                                    update_sequences = sequences_after_frame(sequences_to_check, end_frame, add_locked=False, add_parented=False, add_effect=False)
                                    if last_frame_final_start != sequence.frame_final_start:
                                        # left handle was changed
                                        # would need to move this sequence as well as all sequences after, but the way the grab operator works makes this impossible to set properly
                                        pass
                                    else:
                                        # right handle was changed, move all sequences after to match
                                        duration = sequence.frame_final_end - end_frame
                                        for seq in update_sequences:
                                            seq.frame_start = seq.frame_start + duration
                            if prefs.fades:
                                # Fix fades in sequence if they exist
                                fade_in = fades(sequence, fade_length=0, type='in', mode='detect', fade_low_point_frame=start_frame)
                                fade_out = fades(sequence, fade_length=0, type='out', mode='detect', fade_low_point_frame=end_frame)
                                if fade_in > 0:
                                    fades(sequence, fade_length=fade_in, type='in', mode='set')
                                if fade_out > 0:
                                    fades(sequence, fade_length=fade_out, type='out', mode='set')

                            if prefs.parenting and scene.vseqf.children and not scene.vseqf.selectchildren:
                                # resize children if it has some and their endpoints match the pre-resized endpoints, and fix their fades if needed
                                children = find_children(sequence)
                                for child in children:
                                    if child.frame_final_start == start_frame:
                                        child.frame_final_start = sequence.frame_final_start
                                        child_fade_in = fades(child, fade_length=0, type='in', mode='detect', fade_low_point_frame=start_frame)
                                        if child_fade_in > 0:
                                            fades(child, fade_length=child_fade_in, type='in', mode='set')

                                    if child.frame_final_end == end_frame:
                                        child.frame_final_end = sequence.frame_final_end
                                        child_fade_out = fades(child, fade_length=0, type='out', mode='detect', fade_low_point_frame=end_frame)
                                        if child_fade_out > 0:
                                            fades(child, fade_length=child_fade_out, type='out', mode='set')

                    # Deal with new sequences
                    build_proxy_on = []
                    if prefs.parenting or prefs.proxy:
                        for sequence in new_sequences:
                            if prefs.proxy and scene.vseqf.enableproxy and (sequence.type == "MOVIE" or sequence.type == "SCENE"):
                                build_proxy_on.append(sequence)
                                sequence.use_proxy = True
                                sequence.proxy.build_25 = scene.vseqf.proxy25
                                sequence.proxy.build_50 = scene.vseqf.proxy50
                                sequence.proxy.build_75 = scene.vseqf.proxy75
                                sequence.proxy.build_100 = scene.vseqf.proxy100
                                sequence.proxy.quality = scene.vseqf.proxyquality

                            if prefs.parenting and scene.vseqf.autoparent:
                                # auto parent sound sequences to their movie sequence
                                if sequence.type == 'SOUND':
                                    if not sequence.parent:
                                        for seq in new_sequences:
                                            if seq.type == 'MOVIE':
                                                if seq.filepath == sequence.sound.filepath:
                                                    print("Parenting " + sequence.name + " to " + seq.name)
                                                    add_children(seq, [sequence])

                    # Build proxies if needed
                    if scene.vseqf.buildproxy and len(build_proxy_on) > 0:
                        last_selected = bpy.context.selected_sequences
                        for seq in sequences:
                            seq.select = False
                        for sequence in build_proxy_on:
                            sequence.select = True

                        area = False
                        region = False
                        for screenarea in bpy.context.window.screen.areas:
                            if screenarea.type == 'SEQUENCE_EDITOR':
                                area = screenarea
                                for arearegion in area.regions:
                                    if arearegion.type == 'WINDOW':
                                        region = arearegion
                        if area and region:
                            override = bpy.context.copy()
                            override['area'] = area
                            override['region'] = region
                            bpy.ops.sequencer.rebuild_proxy(override, 'INVOKE_DEFAULT')

                        for seq in sequences:
                            seq.select = False
                        for sequence in last_selected:
                            sequence.select = True

                    # Deal with deleted sequences
                    ripple_sequences = []
                    for sequence in removed_sequences:
                        name, frame_final_start, frame_final_end, parent, do_not_ripple = sequence
                        if not do_not_ripple:
                            ripple_sequences.append(sequence)
                        if vseqf.deletechildren:
                            # delete child sequences if required
                            children = find_children(name, name=True)
                            if len(children) > 0:
                                original_selected = bpy.context.selected_sequences
                                original_active = scene.sequence_editor.active_strip
                                for seq in original_selected:
                                    seq.select = False
                                for child in children:
                                    vseqf.lastsequences[child.name].do_not_ripple = True
                                    child.parent = 'do_not_ripple'
                                    child.select = True
                                bpy.ops.sequencer.delete()

                                for select in original_selected:
                                    select.select = True
                                scene.sequence_editor.active_strip = original_active

                    if scene.vseqf.ripple and (len(ripple_sequences) > 0):
                        # determine ripple amount
                        start_frame = ripple_sequences[0][1]
                        end_frame = ripple_sequences[0][2]
                        for sequence in ripple_sequences:
                            name, frame_final_start, frame_final_end, parent, do_not_ripple = sequence
                            if frame_final_start < start_frame:
                                # determine starting frame by the starting point of the first deleted strip
                                start_frame = frame_final_start
                            if frame_final_end > end_frame:
                                end_frame = frame_final_end
                        total_length = end_frame - start_frame
                        offset = total_length
                        # move sequences after the deleted one up in the timeline
                        sequences_to_check = sequencer.sequences
                        update_sequences = sequences_after_frame(sequences_to_check, start_frame, add_locked=False, add_parented=(not vseqf.children), add_effect=False)
                        for seq in update_sequences:
                            # move sequences
                            if seq.frame_final_start >= end_frame:
                                seq.frame_start = seq.frame_start - offset
                            else:
                                seq.frame_start = seq.frame_start - (seq.frame_final_start - start_frame)

                    # Deal with cut sequences
                    for sequenceinfo in cut_to_sequences:
                        sequence, last_frame_final_start, last_frame_final_duration = sequenceinfo
                        # fix parent relationships for cut clips
                        if sequence.parent:
                            for parentinfo in cut_sequences:
                                if parentinfo[0].name == sequence.parent:
                                    # parent of this strip was cut, figure out what it was cut to
                                    for cut_to in cut_to_sequences:
                                        if cut_to[0].channel == parentinfo[0].channel:
                                            sequence.parent = cut_to[0].name

                    if scene.vseqf.children:
                        for sequenceinfo in cut_sequences:
                            sequence, last_frame_final_start, last_frame_final_duration = sequenceinfo
                            # cut child clips if needed
                            original_children = find_children(sequence)
                            for child in original_children:
                                if child.frame_final_start < frame_current and child.frame_final_end > frame_current:
                                    # child sequence needs to be cut and new child sequence parented to new sequence
                                    original_selected = bpy.context.selected_sequences
                                    original_active = scene.sequence_editor.active_strip
                                    for seq in sequences:
                                        seq.select = False

                                    child.select = True
                                    bpy.ops.sequencer.cut(frame=frame_current)

                                    new_cut_sequences = bpy.context.selected_sequences

                                    # figure out what 'sequence' was cut to
                                    new_sequence = False
                                    for cut_to in cut_to_sequences:
                                        if cut_to[0].channel == sequence.channel:
                                            new_sequence = cut_to[0]

                                    if new_sequence:
                                        # the new cut sequence was found, so copy the new child sequences to it
                                        for new_cut_sequence in new_cut_sequences:
                                            if new_cut_sequence != child:
                                                # cut sequence is not the child of the original sequence
                                                add_children(new_sequence, [new_cut_sequence])

                                    for seq in sequences:
                                        seq.select = False
                                    for select in original_selected:
                                        select.select = True
                                    scene.sequence_editor.active_strip = original_active

                    # iterate through selected sequences and select child sequences
                    if prefs.parenting and vseqf.selectchildren:
                        for sequence in bpy.context.selected_sequences:
                            children = find_children(sequence)
                            for child in children:
                                if not child.select:
                                    child.select = True
                                    if child.frame_final_start == sequence.frame_final_start:
                                        child.select_left_handle = sequence.select_left_handle
                                    if child.frame_final_end == sequence.frame_final_end:
                                        child.select_right_handle = sequence.select_right_handle


# Functions related to QuickSpeed

# Function for frame skipping with the speed step handler
@persistent
def frame_step(scene):
    scene = bpy.context.scene
    step = scene.vseqf.step
    if (step == 1):
        # if the step is 1, only one frame in every 3 will be skipped
        if (scene.frame_current % 3 == 0):
            scene.frame_current = scene.frame_current + 1
    if (step == 2):
        # if the step is 2, every other frame is skipped
        if (scene.frame_current % 2 == 0):
            scene.frame_current = scene.frame_current + 1
    if (step > 2):
        # if the step is greater than 2, (step-2) frames will be skipped per frame
        scene.frame_current = scene.frame_current + (step - 2)

# Draws the speed selector in the sequencer header


def draw_quickspeed_header(self, context):
    layout = self.layout
    scene = context.scene
    self.layout_width = 30
    layout.prop(scene.vseqf, 'step', text="Speed Step")


# Functions related to QuickZoom

# Draws the menu for the QuickZoom shortcuts
def draw_quickzoom_menu(self, context):
    layout = self.layout
    layout.menu('vseqf.quickzooms_menu', text="Quick Zoom")

# Function to zoom to an area on the sequencer timeline


def zoom_custom(begin, end):
    scene = bpy.context.scene
    selected = []

    # Find sequence editor, or create if not found
    try:
        sequences = bpy.context.sequences
    except:
        scene.sequence_editor_create()
        sequences = bpy.context.sequences

    # Save selected sequences and active strip because they will be overwritten
    for sequence in sequences:
        if (sequence.select):
            selected.append(sequence)
            sequence.select = False
    active = bpy.context.scene.sequence_editor.active_strip

    # Determine preroll for the zoom
    zoomlength = end - begin
    if zoomlength > 60:
        preroll = (zoomlength - 60) / 10
    else:
        preroll = 0

    # Create a temporary sequence, zoom in on it, then delete it
    zoomClip = scene.sequence_editor.sequences.new_effect(name='temp', type='ADJUSTMENT', channel=1, frame_start=begin - preroll, frame_end=end)
    scene.sequence_editor.active_strip = zoomClip
    for region in bpy.context.area.regions:
        if (region.type == 'WINDOW'):
            override = {'region': region, 'window': bpy.context.window, 'screen': bpy.context.screen, 'area': bpy.context.area, 'scene': bpy.context.scene}
            bpy.ops.sequencer.view_selected(override)
    bpy.ops.sequencer.delete()

    # Reset selected sequences and active strip
    for sequence in selected:
        sequence.select = True
    bpy.context.scene.sequence_editor.active_strip = active

# Function to zoom near the cursor based on the 'zoomsize' scene variable


def zoom_cursor(self=None, context=None):
    cursor = bpy.context.scene.frame_current
    zoom_custom(cursor, (cursor + bpy.context.scene.vseqf.zoomsize))


# Functions related to QuickFades

# Function to add a crossfade between two sequences, the transition type is determined by the scene variable 'transition'
def crossfade(first_sequence, second_sequence):
    type = bpy.context.scene.vseqf.transition
    sequences = bpy.context.sequences

    bpy.ops.sequencer.select_all(action='DESELECT')
    first_sequence.select = True
    second_sequence.select = True
    bpy.context.scene.sequence_editor.active_strip = second_sequence
    bpy.ops.sequencer.effect_strip_add(type=type)

# Function to detect, create and edit fadein and fadeout for sequences


def fades(sequence, fade_length, type, mode, fade_low_point_frame=False):
    # sequence = vse sequence
    # fade_length = positive value of fade in frames
    # type = 'in' or 'out'
    # mode = 'detect' or 'set' or 'clear'

    scene = bpy.context.scene

    # These functions check for the needed variables and create them if in set mode.  Otherwise, ends the function.
    if scene.animation_data == None:
        # No animation data in scene, create it
        if (mode == 'set'):
            scene.animation_data_create()
        else:
            return 0
    if scene.animation_data.action == None:
        # No action in scene, create it
        if mode == 'set':
            action = bpy.data.actions.new(scene.name + "Action")
            scene.animation_data.action = action
        else:
            return 0

    all_curves = scene.animation_data.action.fcurves
    fade_curve = False  # curve for the fades
    fade_low_point = False  # keyframe that the fade reaches minimum value at
    fade_high_point = False  # keyframe that the fade starts maximum value at
    if (type == 'in'):
        if not fade_low_point_frame:
            fade_low_point_frame = sequence.frame_final_start
    else:
        if not fade_low_point_frame:
            fade_low_point_frame = sequence.frame_final_end
        fade_length = -fade_length
    fade_high_point_frame = fade_low_point_frame + fade_length

    fade_max_value = 1  # set default fade max value, this may change

    # set up the data value to fade
    if sequence.type == 'SOUND':
        fade_variable = 'volume'
    else:
        fade_variable = 'blend_alpha'

    # attempts to find the fade keyframes by iterating through all curves in scene
    for curve in all_curves:
        if (curve.data_path == 'sequence_editor.sequences_all["' + sequence.name + '"].' + fade_variable):
            # keyframes found
            fade_curve = curve

            # delete keyframes and end function
            if mode == 'clear':
                all_curves.remove(fade_curve)
                return 0

    if not fade_curve:
        # no fade animation curve found, create and continue if instructed to, otherwise end function
        if (mode == 'set'):
            fade_curve = all_curves.new(data_path=sequence.path_from_id(fade_variable))
            keyframes = fade_curve.keyframe_points
        else:
            return 0

    # Detect fades or add if set mode
    fade_keyframes = fade_curve.keyframe_points
    if len(fade_keyframes) == 0:
        # no keyframes found, create them if instructed to do so
        if (mode == 'set'):
            fade_max_value = getattr(sequence, fade_variable)
            set_fade(fade_keyframes, type, fade_low_point_frame, fade_high_point_frame, fade_max_value)
        else:
            return 0

    elif len(fade_keyframes) == 1:
        # only one keyframe, use y value of keyframe as the max value for a new fade
        if (mode == 'set'):
            # determine fade_max_value from value at one keyframe
            fade_max_value = fade_keyframes[0].co[1]
            if fade_max_value == 0:
                fade_max_value = 1

            # remove lone keyframe, then add new fade
            fade_keyframes.remove(fade_keyframes[0])
            set_fade(fade_keyframes, type, fade_low_point_frame, fade_high_point_frame, fade_max_value)
        else:
            return 0

    elif len(fade_keyframes) > 1:
        # at least 2 keyframes, there may be a fade already
        if type == 'in':
            fade_low_point = fade_keyframes[0]
            fade_high_point = fade_keyframes[1]
        elif type == 'out':
            fade_low_point = fade_keyframes[-1]
            fade_high_point = fade_keyframes[-2]

        # check to see if the fade points are valid
        if fade_low_point.co[1] == 0:
            # opacity is 0, assume there is a fade
            if fade_low_point.co[0] == fade_low_point_frame:
                # fade low point is in the correct location
                if fade_high_point.co[1] > fade_low_point.co[1]:
                    # both fade points are valid
                    if mode == 'set':
                        fade_max_value = fade_high_point.co[1]
                        set_fade(fade_keyframes, type, fade_low_point_frame, fade_high_point_frame, fade_max_value, fade_low_point=fade_low_point, fade_high_point=fade_high_point)
                        return fade_length
                    else:
                        # fade detected!
                        return abs(fade_high_point.co[0] - fade_low_point.co[0])
                else:
                    # fade high point is not valid, low point is tho
                    if mode == 'set':
                        fade_max_value = fade_curve.evaluate(fade_high_point_frame)
                        set_fade(fade_keyframes, type, fade_low_point_frame, fade_high_point_frame, fade_max_value, fade_low_point=fade_low_point)
                        return fade_length
                    else:
                        return 0
            else:
                # fade low point is not in the correct location
                if mode == 'set':
                    # check fade high point
                    if fade_high_point.co[1] > fade_low_point.co[1]:
                        # fade exists, but is not set up properly
                        fade_max_value = fade_high_point.co[1]
                        set_fade(fade_keyframes, type, fade_low_point_frame, fade_high_point_frame, fade_max_value, fade_low_point=fade_low_point, fade_high_point=fade_high_point)
                        return fade_length
                    else:
                        # no valid fade high point
                        fade_max_value = fade_curve.evaluate(fade_high_point_frame)
                        set_fade(fade_keyframes, type, fade_low_point_frame, fade_high_point_frame, fade_max_value, fade_low_point=fade_low_point)
                        return fade_length
                else:
                    return 0

        else:
            # no valid fade detected, other keyframes are on the curve tho
            if mode == 'set':
                fade_max_value = fade_curve.evaluate(fade_high_point_frame)
                set_fade(fade_keyframes, type, fade_low_point_frame, fade_high_point_frame, fade_max_value)
                return fade_length
            else:
                return 0

# creates a fade in or out on a set of keyframes, can be passed keyframes to adjust


def set_fade(fade_keyframes, direction, fade_low_point_frame, fade_high_point_frame, fade_max_value, fade_low_point=None, fade_high_point=None):
    # check if any keyframe points other than the fade high and low points are in the fade area, delete them if needed
    for keyframe in fade_keyframes:
        if direction == 'in':
            if (keyframe.co[0] < fade_high_point_frame) and (keyframe.co[0] > fade_low_point_frame):
                if (keyframe != fade_low_point) and (keyframe != fade_high_point):
                    fade_keyframes.remove(keyframe)
        if direction == 'out':
            if (keyframe.co[0] > fade_high_point_frame) and (keyframe.co[0] < fade_low_point_frame):
                if (keyframe != fade_low_point) and (keyframe != fade_high_point):
                    fade_keyframes.remove(keyframe)

    fade_length = abs(fade_high_point_frame - fade_low_point_frame)
    handle_offset = fade_length * .38
    if fade_low_point:
        if fade_length != 0:
            # move fade low point to where it should be
            fade_low_point.co = ((fade_low_point_frame, 0))
            fade_low_point.handle_left = ((fade_low_point_frame - handle_offset, 0))
            fade_low_point.handle_right = ((fade_low_point_frame + handle_offset, 0))
        else:
            # remove fade low point
            fade_keyframes.remove(fade_low_point)
    else:
        if fade_high_point_frame != fade_low_point_frame:
            # create new fade low point
            fade_keyframes.insert(frame=fade_low_point_frame, value=0)

    if fade_high_point:
        # move fade high point to where it should be
        fade_high_point.co = ((fade_high_point_frame, fade_max_value))
        fade_high_point.handle_left = ((fade_high_point_frame - handle_offset, fade_max_value))
        fade_high_point.handle_right = ((fade_high_point_frame + handle_offset, fade_max_value))
    else:
        # create new fade high point
        fade_keyframes.insert(frame=fade_high_point_frame, value=fade_max_value)


# Functions related to QuickParents

# Function to look for a sound sequence that is tied to a video sequence
def find_sound_child(parent_sequence, sequences):
    for sequence in sequences:
        if ((os.path.splitext(sequence.name)[0] == os.path.splitext(parent_sequence.name)[0]) & (sequence.type == 'SOUND')):
            return sequence
    return False

# Function to add QuickParents relationships between a parent sequence and one or more child sequences


def add_children(parent_sequence, child_sequences):
    for child_sequence in child_sequences:
        if (child_sequence.name != parent_sequence.name):
            child_sequence.parent = parent_sequence.name

# Function to return a list of sequences that are QuickParents children of an inputted sequence


def find_children(parent_sequence, name=False):
    if name:
        parent_name = parent_sequence
    else:
        parent_name = parent_sequence.name
    scene = bpy.context.scene
    sequences = scene.sequence_editor.sequences_all
    child_sequences = []
    for sequence in sequences:
        if sequence.parent == parent_name:
            child_sequences.append(sequence)
    return child_sequences

# Function to return the QuickParents parent sequence to a child sequence


def find_parent(child_sequence):
    scene = bpy.context.scene
    sequences = scene.sequence_editor.sequences_all
    if child_sequence.parent in sequences:
        return sequences[child_sequence.parent]
    else:
        return False

# Function to remove QuickParents children from a parent sequence


def clear_children(parent_sequence):
    scene = bpy.context.scene
    sequences = scene.sequence_editor.sequences_all
    for sequence in sequences:
        if sequence.parent == parent_sequence.name:
            clear_parent(sequence)

# Function to remove a QuickParents parent relationship from a child sequence


def clear_parent(child_sequence):
    child_sequence.parent = ''

# Function that finds QuickParents child sequences, then selects them


def select_children(parent_sequence):
    children = find_children(parent_sequence)
    for child in children:
        child.select = True

# Function that finds a QuickParents parent sequence and selects it


def select_parent(child_sequence):
    parent = find_parent(child_sequence)
    if parent:
        parent.select = True


# Functions related to QuickSnaps

# Draws the QuickSnaps menu
def draw_quicksnap_menu(self, context):
    layout = self.layout
    layout.menu('vseqf.quicksnaps_menu', text="Quick Snaps")


# Classes related to QuickList

# QuickList panel
class VSEQFQuickListPanel(bpy.types.Panel):
    bl_label = "Quick List"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        # Check if panel is disabled
        prefs = context.user_preferences.addons[__name__].preferences

        # Check for sequences
        if not bpy.context.sequences:
            return False
        if len(bpy.context.sequences) > 0:
            return prefs.list
        else:
            return False

    def draw(self, contex):
        scene = bpy.context.scene
        sequencer = scene.sequence_editor
        sequences = bpy.context.sequences

        # Sort the sequences
        sorted = list(sequences)
        if (scene.vseqf.quicklistsort == 'Title'):
            sorted.sort(key=lambda sequence: sequence.name)
        elif (scene.vseqf.quicklistsort == 'Length'):
            sorted.sort(key=lambda sequence: sequence.frame_final_duration)
        else:
            sorted.sort(key=lambda sequence: sequence.frame_final_start)

        # Check for effect sequences and move them next to their parent sequence
        for sequence in sorted:
            if hasattr(sequence, 'input_1'):
                resort = sorted.pop(sorted.index(sequence))
                parentindex = sorted.index(sequence.input_1)
                sorted.insert(parentindex + 1, resort)

        layout = self.layout

        # Display Mode
        row = layout.row()
        row.prop(scene.vseqf, 'quicklistdisplay')

        # Select all and sort buttons
        if scene.vseqf.quicklistdisplay == 'STANDARD':
            row = layout.row()
            row.operator('vseqf.quicklist_select', text='Select/Deselect All Sequences').sequence = ''

            row = layout.row(align=True)
            row.alignment = 'EXPAND'
            row.label('Sort By:')
        else:
            row = layout.row(align=True)
            row.alignment = 'EXPAND'
            row.operator('vseqf.quicklist_select', text='Select All').sequence = ''
            row.label('Sort:')
        sub = row.column(align=True)
        sub.operator('vseqf.quicklist_sortby', text='Position').method = 'Position'
        if scene.vseqf.quicklistsort == 'Position':
            sub.active = True
        else:
            sub.active = False
        sub = row.column(align=True)
        sub.operator('vseqf.quicklist_sortby', text='Title').method = 'Title'
        if scene.vseqf.quicklistsort == 'Title':
            sub.active = True
        else:
            sub.active = False
        sub = row.column(align=True)
        sub.operator('vseqf.quicklist_sortby', text='Length').method = 'Length'
        if scene.vseqf.quicklistsort == 'Length':
            sub.active = True
        else:
            sub.active = False

        # Display all sequences
        for index, sequence in enumerate(sorted):
            if (hasattr(sequence, 'input_1')):
                # Effect sequence, add an indent
                row = box.row()
                row.separator()
                row.separator()
                outline = row.split()
            else:
                if scene.vseqf.quicklistdisplay == 'STANDARD' or scene.vseqf.quicklistdisplay == 'ONELINE':
                    outline = layout.box()
                else:
                    row.separator()
                    row = layout.row()
                    outline = layout.row()
            box = outline.column()

            if scene.vseqf.quicklistdisplay == 'ONELINE' or scene.vseqf.quicklistdisplay == 'ONELINECOMPACT':
                row = box.row(align=True)
                split = row.split(align=True)
                split.prop(sequence, 'mute', text='')
                split.prop(sequence, 'lock', text='')
                split = row.split(align=True, percentage=0.2)
                col = split.column(align=True)
                col.operator('vseqf.quicklist_select', text="(" + sequence.type + ")").sequence = sequence.name
                col.active = sequence.select
                col = split.column(align=True)
                col.prop(sequence, 'name', text='')

                split = row.split(percentage=0.8)
                col = split.row(align=True)
                col.prop(sequence, 'frame_final_duration', text="Len:" + timecode_from_frames(sequence.frame_final_duration, (scene.render.fps / scene.render.fps_base)) + ", ")
                col.prop(sequence, 'frame_start', text="Pos:" + timecode_from_frames(sequence.frame_start, (scene.render.fps / scene.render.fps_base)) + ", ")
                col = split.row()
                if (sequence.type != 'SOUND') and (not hasattr(sequence, 'input_1')):
                    col.prop(sequence, 'use_proxy', text='Proxy')
                    if (sequence.use_proxy):
                        # Proxy is enabled, add row for proxy settings
                        row = box.row()
                        split = row.split(percentage=0.33)
                        col = split.row(align=True)
                        col.prop(sequence.proxy, 'quality')
                        col = split.row(align=True)
                        col.prop(sequence.proxy, 'build_25')
                        col.prop(sequence.proxy, 'build_50')
                        col.prop(sequence.proxy, 'build_75')
                        col.prop(sequence.proxy, 'build_100')
                else:
                    col.label('')

            else:
                # First row - mute, lock, type and title
                row = box.row(align=True)
                split = row.split(align=True)
                split.prop(sequence, 'mute', text='')
                split.prop(sequence, 'lock', text='')
                split = row.split(align=True, percentage=0.2)
                col = split.column(align=True)
                col.operator('vseqf.quicklist_select', text="(" + sequence.type + ")").sequence = sequence.name
                col.active = sequence.select
                col = split.column(align=True)
                col.prop(sequence, 'name', text='')

                # Second row - length, position and proxy toggle
                row = box.row()
                split = row.split(percentage=0.8)
                col = split.row(align=True)
                col.prop(sequence, 'frame_final_duration', text="Len:" + timecode_from_frames(sequence.frame_final_duration, (scene.render.fps / scene.render.fps_base)) + ", ")
                col.prop(sequence, 'frame_start', text="Pos:" + timecode_from_frames(sequence.frame_start, (scene.render.fps / scene.render.fps_base)) + ", ")
                col = split.row()
                if (sequence.type != 'SOUND') and (not hasattr(sequence, 'input_1')):
                    col.prop(sequence, 'use_proxy', text='Proxy')
                    if (sequence.use_proxy):
                        # Proxy is enabled, add row for proxy settings
                        row = box.row()
                        split = row.split(percentage=0.33)
                        col = split.row(align=True)
                        col.prop(sequence.proxy, 'quality')
                        col = split.row(align=True)
                        col.prop(sequence.proxy, 'build_25')
                        col.prop(sequence.proxy, 'build_50')
                        col.prop(sequence.proxy, 'build_75')
                        col.prop(sequence.proxy, 'build_100')

            # List children sequences if found
            children = find_children(sequence)
            if len(children) > 0 and (scene.vseqf.quicklistdisplay != 'COMPACT' and scene.vseqf.quicklistdisplay != 'ONELINECOMPACT'):
                row = box.row()
                split = row.split(percentage=0.25)
                col = split.column()
                col.label('Children:')
                col = split.column()
                for child in children:
                    col.label(child.name)

            # List sub-sequences in a meta sequence
            if sequence.type == 'META' and (scene.vseqf.quicklistdisplay != 'COMPACT' and scene.vseqf.quicklistdisplay != 'ONELINECOMPACT'):
                row = box.row()
                split = row.split(percentage=0.25)
                col = split.column()
                col.label('Sub-sequences:')
                col = split.column()
                for index, subsequence in enumerate(sequence.sequences):
                    if index > 10:
                        # Stops listing sub-sequences if list is too long
                        col.label('...')
                        break
                    col.label(subsequence.name)

# Operator to change scene.quicklistsort method


class VSEQFQuickListSortBy(bpy.types.Operator):
    bl_idname = "vseqf.quicklist_sortby"
    bl_label = "VSEQF Quick List Sort By"
    method = bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        scene.vseqf.quicklistsort = self.method
        return {'FINISHED'}

# Operator to select a sequence, or multiple sequences


class VSEQFQuickListSelect(bpy.types.Operator):
    bl_idname = "vseqf.quicklist_select"
    bl_label = "VSEQF Quick List Select Sequence"
    sequence = bpy.props.StringProperty()

    def execute(self, context):
        sequences = context.sequences
        if (self.sequence == ''):
            bpy.ops.sequencer.select_all(action='TOGGLE')
        else:
            for sequence in sequences:
                if (sequence.name == self.sequence):
                    sequence.select = not sequence.select
        return {'FINISHED'}


# Classes related to QuickParents

# Pop-up menu for QuickParents
class VSEQFQuickParentsMenu(bpy.types.Menu):
    bl_idname = "vseqf.quickparents_menu"
    bl_label = "Quick Parents"

    @classmethod
    def poll(self, context):
        prefs = context.user_preferences.addons[__name__].preferences
        return prefs.parenting

    def draw(self, context):
        scene = bpy.context.scene
        sequence = scene.sequence_editor.active_strip
        layout = self.layout

        if sequence:
            # Active sequence set

            selected = bpy.context.selected_sequences
            children = find_children(sequence)
            parent = find_parent(sequence)

            layout.operator('vseqf.quickparents', text='Select Children').action = 'selectchildren'
            layout.operator('vseqf.quickparents', text='Select Parent').action = 'selectparent'
            if len(selected) > 1:
                # more than one sequence is selected, so children can be set
                layout.operator('vseqf.quickparents', text='Set Active As Parent').action = 'add'

            layout.operator('vseqf.quickparents', text='Clear Children').action = 'clearchildren'
            layout.operator('vseqf.quickparents', text='Clear Parent').action = 'clearparent'

            if parent:
                # Parent sequence is found, display it
                layout.separator()
                layout.label("     Parent: ")
                layout.label(parent.name)
                layout.separator()

            if len(children) > 0:
                # At least one child sequence is found, display them
                layout.separator()
                layout.label("     Children:")
                index = 0
                while index < len(children):
                    layout.label(children[index].name)
                    index = index + 1
                layout.separator()

        else:
            layout.label('No Sequence Selected')

# Operator for changing parenting relationships


class VSEQFQuickParents(bpy.types.Operator):
    bl_idname = 'vseqf.quickparents'
    bl_label = 'VSEQF Quick Parents'
    bl_description = 'Sets Or Removes Strip Parents'

    # Defines what the operator will attempt to do
    # Can be set to: 'add', 'selectchildren', 'selectparent', 'clearparent', 'clearchildren'
    action = bpy.props.StringProperty()

    def execute(self, context):
        selected = bpy.context.selected_sequences
        active = bpy.context.scene.sequence_editor.active_strip

        if (self.action == 'add') and (len(selected) > 1):
            add_children(active, selected)
        else:
            for sequence in selected:
                if self.action == 'selectchildren':
                    select_children(sequence)
                if self.action == 'selectparent':
                    select_parent(sequence)
                if self.action == 'clearparent':
                    clear_parent(sequence)
                if self.action == 'clearchildren':
                    clear_children(sequence)
        return {'FINISHED'}


# Classes related to QuickSnaps

# Pop-up menu for QuickSnaps
class VSEQFQuickSnapsMenu(bpy.types.Menu):
    bl_idname = "vseqf.quicksnaps_menu"
    bl_label = "Quick Snaps"

    def draw(self, context):
        layout = self.layout
        layout.operator('vseqf.quicksnaps', text='Cursor To Nearest Second').type = 'cursor_to_seconds'
        scene = bpy.context.scene

        try:
            # Display only if active sequence is set
            sequence = scene.sequence_editor.active_strip
            if (sequence):
                layout.operator('vseqf.quicksnaps', text='Cursor To Beginning Of Sequence').type = 'cursor_to_beginning'
                layout.operator('vseqf.quicksnaps', text='Cursor To End Of Sequence').type = 'cursor_to_end'
                layout.separator()
                layout.operator('vseqf.quicksnaps', text='Selected To Cursor').type = 'selected_to_cursor'
                layout.operator('vseqf.quicksnaps', text='Sequence Beginning To Cursor').type = 'begin_to_cursor'
                layout.operator('vseqf.quicksnaps', text='Sequence End To Cursor').type = 'end_to_cursor'
                layout.operator('vseqf.quicksnaps', text='Sequence To Previous Sequence').type = 'sequence_to_previous'
                layout.operator('vseqf.quicksnaps', text='Sequence To Next Sequence').type = 'sequence_to_next'

        except:
            pass

# Operator for snapping cursor and sequences


class VSEQFQuickSnaps(bpy.types.Operator):
    bl_idname = 'vseqf.quicksnaps'
    bl_label = 'VSEQF Quick Snaps'
    bl_description = 'Snaps selected sequences'

    # Snapping operation to perform
    type = bpy.props.StringProperty()

    def execute(self, context):
        # Set up variables needed for operator
        selected = bpy.context.selected_sequences
        scene = bpy.context.scene
        active = bpy.context.scene.sequence_editor.active_strip
        frame = scene.frame_current

        # Cursor snaps
        if self.type == 'cursor_to_seconds':
            fps = scene.render.fps / scene.render.fps_base
            scene.frame_current = round(round(scene.frame_current / fps) * fps)

        if self.type == 'cursor_to_beginning':
            scene.frame_current = active.frame_final_start

        if self.type == 'cursor_to_end':
            scene.frame_current = active.frame_final_end

        if self.type == 'selected_to_cursor':
            bpy.ops.sequencer.snap(frame=frame)

        # Sequence snaps
        if self.type == 'begin_to_cursor':
            for sequence in selected:
                offset = sequence.frame_final_start - sequence.frame_start
                sequence.frame_start = (frame - offset)

        if self.type == 'end_to_cursor':
            for sequence in selected:
                offset = sequence.frame_final_start - sequence.frame_start
                sequence.frame_start = (frame - offset - sequence.frame_final_duration)

        if self.type == 'sequence_to_previous':
            previous = find_close_sequence(scene.sequence_editor.sequences, active, 'previous', 'any')

            if previous:
                for sequence in selected:
                    offset = sequence.frame_final_start - sequence.frame_start
                    sequence.frame_start = (previous.frame_final_end - offset)

            else:
                self.report({'WARNING'}, 'No Previous Sequence Found')

        if self.type == 'sequence_to_next':
            next = find_close_sequence(scene.sequence_editor.sequences, active, 'next', 'any')

            if (next):
                for sequence in selected:
                    offset = sequence.frame_final_start - sequence.frame_start
                    sequence.frame_start = (next.frame_final_start - offset - sequence.frame_final_duration)

            else:
                self.report({'WARNING'}, 'No Next Sequence Found')

        return{'FINISHED'}


# Classes related to QuickMarkers

# Defines a marker preset
class VSEQFMarkerPreset(bpy.types.PropertyGroup):
    text = bpy.props.StringProperty(name="Text", default="")

# Panel for QuickMarkers operators and properties


class VSEQFQuickMarkersPanel(bpy.types.Panel):
    bl_label = "Quick Markers"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        prefs = context.user_preferences.addons[__name__].preferences
        return prefs.markers

    def draw(self, context):
        scene = bpy.context.scene
        vseqf = scene.vseqf
        layout = self.layout

        for index, marker in enumerate(vseqf.markerpresets):
            row = layout.row()
            split = row.split(percentage=.9, align=True)
            split.operator('vseqf.quickmarkers_place', text=marker.text).marker = marker.text
            split.operator('vseqf.quickmarkers_remove_preset', text='', icon='X').marker = index
        row = layout.row()
        split = row.split(percentage=.9, align=True)
        split.prop(vseqf, 'currentmarker')
        split.operator('vseqf.quickmarkers_add_preset', text="", icon="PLUS").preset = vseqf.currentmarker
        row = layout.row()
        row.prop(vseqf, 'markerdeselect')
        row = layout.row()
        box = row.box()
        split = box.split(percentage=.1)
        split.prop(scene.vseqf, 'expandedmarkers', icon="TRIA_DOWN" if scene.vseqf.expandedmarkers else "TRIA_RIGHT", icon_only=True, emboss=False)
        col = split.column()
        if scene.vseqf.expandedmarkers:
            col.label("Marker List:")
            markersort = sorted(scene.timeline_markers, key=lambda x: x.frame)
            for marker in markersort:
                timecode = timecode_from_frames(marker.frame, (scene.render.fps / scene.render.fps_base), levels=0, subsecondtype='frames')
                colsplit = col.split(percentage=.9, align=True)
                subsplit = colsplit.split(align=True)
                subsplit.operator('vseqf.quickmarkers_jump', text=marker.name + ' (' + timecode + ')').frame = marker.frame
                if marker.frame == scene.frame_current:
                    subsplit.enabled = False
                colsplit.operator('vseqf.quickmarkers_delete', text='', icon='X').frame = marker.frame
        else:
            col.label("Marker List:")


class VSEQFQuickMarkerDelete(bpy.types.Operator):
    bl_idname = 'vseqf.quickmarkers_delete'
    bl_label = 'Delete Marker At Frame'

    frame = bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        markers = scene.timeline_markers
        for marker in markers:
            if marker.frame == self.frame:
                markers.remove(marker)
                break
        return{'FINISHED'}


class VSEQFQuickMarkerJump(bpy.types.Operator):
    bl_idname = 'vseqf.quickmarkers_jump'
    bl_label = 'Jump To Timeline Marker'

    frame = bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        scene.frame_current = self.frame
        return{'FINISHED'}


class VSEQFQuickMarkersMenu(bpy.types.Menu):
    bl_idname = "vseqf.quickmarkers_menu"
    bl_label = "Quick Markers"

    @classmethod
    def poll(self, context):
        prefs = context.user_preferences.addons[__name__].preferences
        return prefs.markers

    def draw(self, context):
        scene = bpy.context.scene
        vseqf = scene.vseqf
        layout = self.layout
        for marker in vseqf.markerpresets:
            layout.operator('vseqf.quickmarkers_place', text=marker.text).marker = marker.text


class VSEQFQuickMarkersPlace(bpy.types.Operator):
    bl_idname = 'vseqf.quickmarkers_place'
    bl_label = 'VSEQF Quick Markers Place A Marker'

    marker = bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        vseqf = scene.vseqf
        frame = scene.frame_current
        exists = False
        for marker in scene.timeline_markers:
            if marker.frame == frame:
                exists = True
        if not exists:
            marker = scene.timeline_markers.new(name=self.marker, frame=frame)
            if vseqf.markerdeselect:
                marker.select = False
        return{'FINISHED'}


class VSEQFQuickMarkersRemovePreset(bpy.types.Operator):
    bl_idname = 'vseqf.quickmarkers_remove_preset'
    bl_label = 'VSEQF Quick Markers Remove Preset'

    # marker index to be removed
    marker = bpy.props.IntProperty()

    def execute(self, context):
        vseqf = context.scene.vseqf
        vseqf.markerpresets.remove(self.marker)
        return{'FINISHED'}


class VSEQFQuickMarkersAddPreset(bpy.types.Operator):
    bl_idname = 'vseqf.quickmarkers_add_preset'
    bl_label = 'VSEQF Quick Markers Add Preset'

    preset = bpy.props.StringProperty()

    def execute(self, context):
        vseqf = context.scene.vseqf
        preset = vseqf.markerpresets.add()
        preset.text = self.preset
        return{'FINISHED'}


# Classes related to QuickFades

# Panel for QuickFades operators and properties
class VSEQFQuickFadesPanel(bpy.types.Panel):
    bl_label = "Quick Fades"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'

    @classmethod
    def poll(self, context):
        # Check if panel is disabled
        prefs = context.user_preferences.addons[__name__].preferences
        try:
            # Check for an active sequence to operate on
            sequence = context.scene.sequence_editor.active_strip
            if (sequence):
                return prefs.fades
            else:
                return False

        except:
            return False

    def draw(self, context):
        # Set up basic variables needed by panel
        scene = bpy.context.scene
        vseqf = scene.vseqf
        active_sequence = scene.sequence_editor.active_strip
        frame = scene.frame_current
        fadein = fades(sequence=active_sequence, fade_length=0, type='in', mode='detect')
        fadeout = fades(sequence=active_sequence, fade_length=0, type='out', mode='detect')

        layout = self.layout

        # First row, detected fades
        row = layout.row()
        if fadein > 0:
            row.label("Fadein: " + str(round(fadein)) + " Frames")
        else:
            row.label("No Fadein Detected")
        if fadeout > 0:
            row.label("Fadeout: " + str(round(fadeout)) + " Frames")
        else:
            row.label("No Fadeout Detected")

        # Setting fades section
        row = layout.row()
        row.prop(vseqf, 'fade')
        row = layout.row()
        row.operator('vseqf.quickfades', text='Set Fadein').type = 'in'
        row.operator('vseqf.quickfades', text='Set Fadeout').type = 'out'
        row = layout.row()
        row.operator('vseqf.quickfades_clear', text='Clear Fades')
        row = layout.row()
        row.separator()

        # Crossfades section
        row = layout.row()
        row.menu('vseqf.quickfades_transition_menu', text="Transition Type: " + scene.vseqf.transition)
        row = layout.row()
        row.operator('vseqf.quickfades_cross', text='Crossfade Prev Clip').type = 'previous'
        row.operator('vseqf.quickfades_cross', text='Crossfade Next Clip').type = 'next'
        row = layout.row()
        row.operator('vseqf.quickfades_cross', text='Smart Cross to Prev').type = 'previoussmart'
        row.operator('vseqf.quickfades_cross', text='Smart Cross to Next').type = 'nextsmart'

# Pop-up menu for QuickFade operators


class VSEQFQuickFadesMenu(bpy.types.Menu):
    bl_idname = "vseqf.quickfades_menu"
    bl_label = "Quick Fades"

    @classmethod
    def poll(self, context):
        prefs = context.user_preferences.addons[__name__].preferences
        return prefs.fades

    def draw(self, context):
        scene = bpy.context.scene
        sequences = bpy.context.selected_sequences
        sequence = scene.sequence_editor.active_strip

        layout = self.layout
        if sequence and len(sequences) > 0:
            # If a sequence is active
            frame = scene.frame_current
            vseqf = scene.vseqf
            fadein = fades(sequence=sequence, fade_length=0, type='in', mode='detect')
            fadeout = fades(sequence=sequence, fade_length=0, type='out', mode='detect')

            # Detected fades section
            if fadein > 0:
                layout.label("Fadein: " + str(round(fadein)) + " Frames")
            else:
                layout.label("No Fadein Detected")
            if fadeout > 0:
                layout.label("Fadeout: " + str(round(fadeout)) + " Frames")
            else:
                layout.label("No Fadeout Detected")

            # Fade length
            layout.prop(vseqf, 'fade')
            layout.operator('vseqf.quickfades', text='Set Fadein').type = 'in'
            layout.operator('vseqf.quickfades', text='Set Fadeout').type = 'out'
            layout.operator('vseqf.quickfades_clear', text='Clear Fades')

            # Add crossfades
            layout.separator()
            layout.menu('vseqf.quickfades_transition_menu', text="Transition Type: " + scene.vseqf.transition)
            layout.operator('vseqf.quickfades_cross', text='Crossfade Prev Sequence').type = 'previous'
            layout.operator('vseqf.quickfades_cross', text='Crossfade Next Sequence').type = 'next'
            layout.operator('vseqf.quickfades_cross', text='Smart Cross to Prev').type = 'previoussmart'
            layout.operator('vseqf.quickfades_cross', text='Smart Cross to Next').type = 'nextsmart'

        else:
            layout.label("No Sequence Selected")

# Operator to add fades to selected sequences


class VSEQFQuickFades(bpy.types.Operator):
    bl_idname = 'vseqf.quickfades'
    bl_label = 'VSEQF Quick Fades Set Fade'
    bl_description = 'Adds or changes fade for selected sequences'

    # Should be set to 'in' or 'out'
    type = bpy.props.StringProperty()

    def execute(self, context):
        for sequence in bpy.context.selected_sequences:
            # iterate through selected sequences and apply fades to them
            fades(sequence=sequence, fade_length=bpy.context.scene.vseqf.fade, type=self.type, mode='set')

        return{'FINISHED'}

# Operator to clear fades on selected sequences


class VSEQFQuickFadesClear(bpy.types.Operator):
    bl_idname = 'vseqf.quickfades_clear'
    bl_label = 'VSEQF Quick Fades Clear Fades'
    bl_description = 'Clears fade in and out for selected sequences'

    def execute(self, context):
        for sequence in bpy.context.selected_sequences:
            # iterate through selected sequences, remove fades, and set opacity to full
            fades(sequence=sequence, fade_length=bpy.context.scene.vseqf.fade, type='both', mode='clear')
            sequence.blend_alpha = 1

        return{'FINISHED'}

# Operator to add crossfades between sequences


class VSEQFQuickFadesCross(bpy.types.Operator):
    bl_idname = 'vseqf.quickfades_cross'
    bl_label = 'VSEQF Quick Fades Add Crossfade'
    bl_description = 'Adds a crossfade between selected sequence and next or previous sequence in timeline'

    # Should be set to 'nextsmart', 'previoussmart', 'next', 'previous'
    type = bpy.props.StringProperty()

    def execute(self, context):
        sequences = bpy.context.sequences

        # store a list of selected sequences since adding a crossfade destroys the selection
        selected_sequences = bpy.context.selected_sequences
        active_sequence = bpy.context.scene.sequence_editor.active_strip

        for sequence in selected_sequences:
            if sequence.type != 'SOUND' and not hasattr(sequence, 'input_1'):
                # iterate through selected sequences and add crossfades to previous or next sequence

                if self.type == 'nextsmart':
                    # Need to find next sequence
                    first_sequence = sequence
                    second_sequence = find_close_sequence(sequences, first_sequence, 'next', mode='all')

                elif self.type == 'previoussmart':
                    # Need to find previous sequence
                    second_sequence = sequence
                    first_sequence = find_close_sequence(sequences, second_sequence, 'prev', mode='all')

                elif self.type == 'next':
                    # Need to find next sequence
                    first_sequence = sequence
                    second_sequence = find_close_sequence(sequences, first_sequence, 'next', mode='all')

                elif self.type == 'previous':
                    # Need to find previous sequence
                    second_sequence = sequence
                    first_sequence = find_close_sequence(sequences, second_sequence, 'prev', mode='all')

                if (second_sequence != False) & (first_sequence != False):
                    if 'smart' in self.type:
                        # adjust start and end frames of sequences based on frame_offset_end/start to overlap by amount of crossfade
                        target_fade = bpy.context.scene.vseqf.fade
                        current_fade = first_sequence.frame_final_end - second_sequence.frame_final_start

                        # if current_fade is negative, there is open space between clips, if positive, clips are overlapping
                        if current_fade <= 0:
                            fade_offset = abs(current_fade + target_fade)
                            first_sequence_offset = -round((fade_offset / 2) + .1)
                            second_sequence_offset = -round((fade_offset / 2) - .1)
                        else:
                            fade_offset = abs(current_fade - target_fade)
                            first_sequence_offset = round((fade_offset / 2) + .1)
                            second_sequence_offset = round((fade_offset / 2) - .1)

                        if abs(current_fade) < target_fade:
                            # detected overlap is not enough, extend the ends of the sequences to match the target overlap

                            if ((first_sequence.frame_offset_end > first_sequence_offset) & (second_sequence.frame_offset_start > second_sequence_offset)) | ((first_sequence.frame_offset_end == 0) & (first_sequence.frame_offset_start == 0)):
                                # both sequence offsets are larger than both target offsets or neither sequence has offsets
                                first_sequence.frame_final_end = first_sequence.frame_final_end + first_sequence_offset
                                second_sequence.frame_final_start = second_sequence.frame_final_start - second_sequence_offset

                            else:
                                # sequence offsets need to be adjusted individually
                                currentOffset = first_sequence.frame_offset_end + second_sequence.frame_offset_start
                                first_sequence_offset_percent = first_sequence.frame_offset_end / currentOffset
                                second_sequence_offset_percent = second_sequence.frame_offset_start / currentOffset
                                first_sequence.frame_final_end = first_sequence.frame_final_end + (round(first_sequence_offset_percent * fade_offset))
                                second_sequence.frame_final_start = second_sequence.frame_final_start - (round(second_sequence_offset_percent * fade_offset))

                        elif abs(current_fade) > target_fade:
                            # detected overlap is larger than target fade, subtract equal amounts from each sequence
                            first_sequence.frame_final_end = first_sequence.frame_final_end - first_sequence_offset
                            second_sequence.frame_final_start = second_sequence.frame_final_start + second_sequence_offset

                    crossfade(first_sequence, second_sequence)

                else:
                    self.report({'WARNING'}, 'No Second Sequence Found')

        bpy.ops.sequencer.select_all(action='DESELECT')
        for sequence in selected_sequences:
            sequence.select = True
        bpy.context.scene.sequence_editor.active_strip = active_sequence
        bpy.ops.ed.undo_push()
        return{'FINISHED'}

# Menu for transition types


class VSEQFQuickFadesTransitionMenu(bpy.types.Menu):
    bl_idname = 'vseqf.quickfades_transition_menu'
    bl_label = 'List Available Transitions'

    def draw(self, context):
        layout = self.layout

        layout.operator("vseqf.quickfades_change_transition", text="Crossfade").transition = "CROSS"
        layout.operator("vseqf.quickfades_change_transition", text="Wipe").transition = "WIPE"
        layout.operator("vseqf.quickfades_change_transition", text="Gamma Cross").transition = "GAMMA_CROSS"

# Applies a transition type to the scene transition variable


class VSEQFQuickFadesChangeTransition(bpy.types.Operator):
    bl_idname = 'vseqf.quickfades_change_transition'
    bl_label = 'VSEQF Quick Fades Change Transition'

    # Transition type to be applied
    transition = bpy.props.StringProperty()

    def execute(self, context):
        bpy.context.scene.vseqf.transition = self.transition
        return{'FINISHED'}


# Classes related to QuickZooms

# Pop-up menu for sequencer zoom shortcuts
class VSEQFQuickZoomsMenu(bpy.types.Menu):
    bl_idname = "vseqf.quickzooms_menu"
    bl_label = "Quick Zooms"

    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout

        layout.operator('vseqf.quickzooms', text='Zoom All').area = 'all'
        if (len(bpy.context.selected_sequences) > 0):
            # Only show if a sequence is selected
            layout.operator('vseqf.quickzooms', text='Zoom Selected').area = 'selected'

        layout.operator('vseqf.quickzooms', text='Zoom Cursor').area = 'cursor'
        layout.prop(scene.vseqf, 'zoomsize', text="Size")

        layout.separator()
        layout.operator('vseqf.quickzooms', text='Zoom 2 Seconds').area = '2'
        layout.operator('vseqf.quickzooms', text='Zoom 10 Seconds').area = '10'
        layout.operator('vseqf.quickzooms', text='Zoom 30 Seconds').area = '30'
        layout.operator('vseqf.quickzooms', text='Zoom 1 Minute').area = '60'
        layout.operator('vseqf.quickzooms', text='Zoom 2 Minutes').area = '120'
        layout.operator('vseqf.quickzooms', text='Zoom 5 Minutes').area = '300'
        layout.operator('vseqf.quickzooms', text='Zoom 10 Minutes').area = '600'


class VSEQFSequence(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(
        name="Sequence Name")
    frame_final_start = bpy.props.IntProperty()
    frame_final_end = bpy.props.IntProperty()
    parent = bpy.props.StringProperty()
    do_not_ripple = bpy.props.BoolProperty(default=False)


class VSEQFQuickZooms(bpy.types.Operator):
    bl_idname = 'vseqf.quickzooms'
    bl_label = 'VSEQF Quick Zooms'
    bl_description = 'Changes zoom level of the sequencer timeline'

    # Should be set to 'all', 'selected', cursor', or a positive number of seconds
    area = bpy.props.StringProperty()

    def execute(self, context):
        if self.area.isdigit():
            # Zoom value is a number of seconds
            scene = bpy.context.scene
            cursor = scene.frame_current

            zoom_custom(cursor, (cursor + (scene.render.fps * int(self.area))))

        elif self.area == 'all':
            bpy.ops.sequencer.view_all()

        elif self.area == 'selected':
            bpy.ops.sequencer.view_selected()

        elif self.area == 'cursor':
            zoom_cursor()

        return{'FINISHED'}


# Miscellaneous Classes

# Pop-up menu for Quick Function settings
class VSEQFSettingsMenu(bpy.types.Menu):
    bl_idname = "vseqf.settings_menu"
    bl_label = "Quick Settings"

    def draw(self, context):
        layout = self.layout
        scene = bpy.context.scene
        prefs = context.user_preferences.addons[__name__].preferences

        layout.prop(scene.vseqf, 'continuousenable')


# Property group to store vseqf settings
class VSEQFSetting(bpy.types.PropertyGroup):
    continuousenable = bpy.props.BoolProperty(
        name="Enable Continuous Options",
        default=False)
    follow = bpy.props.BoolProperty(
        name="Cursor Following",
        default=False)
    children = bpy.props.BoolProperty(
        name="Cut/Move Children",
        default=True)
    autoparent = bpy.props.BoolProperty(
        name="Auto-Parent New Audio To Video",
        default=True)
    selectchildren = bpy.props.BoolProperty(
        name="Auto-Select Children",
        default=False)
    transition = bpy.props.StringProperty(
        name="Transition Type",
        default="CROSS")
    fade = bpy.props.IntProperty(
        name="Fade Length",
        default=0,
        min=0,
        description="Default Fade Length In Frames")
    fadein = bpy.props.IntProperty(
        name="Fade In Length",
        default=0,
        min=0,
        description="Current Fade In Length In Frames")
    fadeout = bpy.props.IntProperty(
        name="Fade Out Length",
        default=0,
        min=0,
        description="Current Fade Out Length In Frames")
    zoomsize = bpy.props.IntProperty(
        name='Zoom Amount',
        default=200,
        min=1,
        description="Zoom size in frames",
        update=zoom_cursor)
    quicklistdisplay = bpy.props.EnumProperty(
        name='Display Mode',
        default='STANDARD',
        items=[('STANDARD', 'Standard', '', 1), ('COMPACT', 'Standard Compact', '', 2), ('ONELINE', 'One Line', '', 3), ('ONELINECOMPACT', 'One Line Compact', '', 4)])
    step = bpy.props.IntProperty(
        name="Frame Step",
        default=0,
        min=0,
        max=6)
    quicklistsort = bpy.props.StringProperty(
        name="Sort Method",
        default='Position')
    enableproxy = bpy.props.BoolProperty(
        name="Enable Proxy On Import",
        default=False)
    buildproxy = bpy.props.BoolProperty(
        name="Auto-Build Proxy On Import",
        default=False)
    proxy25 = bpy.props.BoolProperty(
        name="25%",
        default=True)
    proxy50 = bpy.props.BoolProperty(
        name="50%",
        default=False)
    proxy75 = bpy.props.BoolProperty(
        name="75%",
        default=False)
    proxy100 = bpy.props.BoolProperty(
        name="100%",
        default=False)
    proxyquality = bpy.props.IntProperty(
        name="Quality",
        default=90,
        min=1,
        max=100)
    markerpresets = bpy.props.CollectionProperty(
        type=VSEQFMarkerPreset)
    expandedmarkers = bpy.props.BoolProperty(default=True)
    currentmarker = bpy.props.StringProperty(
        name="New Preset",
        default='')
    markerdeselect = bpy.props.BoolProperty(
        name="Deselect New Markers",
        default=True)
    expandedchildren = bpy.props.BoolProperty(default=True)
    deletechildren = bpy.props.BoolProperty(
        name="Auto-Delete Children",
        default=False)
    lastsequences = bpy.props.CollectionProperty(type=VSEQFSequence)
    ripple = bpy.props.BoolProperty(
        name="Ripple Editing Mode",
        default=False)
    skip_index = bpy.props.IntProperty(
        default=0)
    lastsequencer = bpy.props.StringProperty()


class VSEQuickFunctionSettings(bpy.types.AddonPreferences):
    bl_idname = __name__
    parenting = bpy.props.BoolProperty(
        name="Enable Quick Parenting",
        default=True)
    fades = bpy.props.BoolProperty(
        name="Enable Quick Fades",
        default=True)
    list = bpy.props.BoolProperty(
        name="Enable Quick List",
        default=True)
    proxy = bpy.props.BoolProperty(
        name="Enable Quick Proxy",
        default=True)
    markers = bpy.props.BoolProperty(
        name="Enable Quick Markers",
        default=True)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "parenting")
        layout.prop(self, "fades")
        layout.prop(self, "list")
        layout.prop(self, "proxy")
        layout.prop(self, "markers")


# Register properties, operators, menus and shortcuts
def register():
    bpy.utils.register_class(VSEQuickFunctionSettings)

    # Register operators
    bpy.utils.register_module(__name__)

    bpy.types.SEQUENCER_PT_edit.append(edit_panel)
    bpy.types.SEQUENCER_PT_proxy.append(proxy_panel)

    # Add menus
    bpy.types.SEQUENCER_HT_header.append(draw_quickspeed_header)
    bpy.types.SEQUENCER_MT_view.append(draw_quickzoom_menu)
    bpy.types.SEQUENCER_MT_view.prepend(draw_quicksettings_menu)
    bpy.types.SEQUENCER_MT_strip.prepend(draw_quicksnap_menu)

    bpy.types.Scene.total_sequences = bpy.props.IntProperty(
        default=0)
    bpy.types.Scene.vseqf_skip_interval = bpy.props.IntProperty(
        default=0,
        min=0)

    # New Sequence variables
    bpy.types.Sequence.parent = bpy.props.StringProperty()
    bpy.types.Sequence.last_frame_final_start = bpy.props.IntProperty()
    bpy.types.Sequence.last_frame_start = bpy.props.IntProperty()
    bpy.types.Sequence.last_frame_final_duration = bpy.props.IntProperty()
    bpy.types.Sequence.last_select = bpy.props.BoolProperty()
    bpy.types.Sequence.last_channel = bpy.props.IntProperty()
    bpy.types.Sequence.last_name = bpy.props.StringProperty(default='')
    bpy.types.Sequence.new = bpy.props.BoolProperty(
        default=True)

    # Group properties
    bpy.types.Scene.vseqf = bpy.props.PointerProperty(type=VSEQFSetting)

    # Register shortcuts
    keymap = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='Sequencer', space_type='SEQUENCE_EDITOR', region_type='WINDOW')
    keymapitems = keymap.keymap_items

    for keymapitem in keymapitems:
        # Iterate through keymaps and delete old shortcuts
        if ((keymapitem.type == 'Z') | (keymapitem.type == 'P') | (keymapitem.type == 'F') | (keymapitem.type == 'S')):
            keymapitems.remove(keymapitem)
    keymapmarker = keymapitems.new('wm.call_menu', 'M', 'PRESS', alt=True)
    keymapmarker.properties.name = 'vseqf.quickmarkers_menu'
    keymapzoom = keymapitems.new('wm.call_menu', 'Z', 'PRESS')
    keymapzoom.properties.name = 'vseqf.quickzooms_menu'
    keymapfade = keymapitems.new('wm.call_menu', 'F', 'PRESS')
    keymapfade.properties.name = 'vseqf.quickfades_menu'
    keymapsnap = keymapitems.new('wm.call_menu', 'S', 'PRESS')
    keymapsnap.properties.name = 'vseqf.quicksnaps_menu'
    keymapparent = keymapitems.new('wm.call_menu', 'P', 'PRESS', ctrl=True)
    keymapparent.properties.name = 'vseqf.quickparents_menu'
    keymapparentselect = keymapitems.new('vseqf.quickparents', 'P', 'PRESS', shift=True)
    keymapparentselect.properties.action = 'selectchildren'

    # Register handler and modal operator
    handlers = bpy.app.handlers.frame_change_post
    for handler in handlers:
        if (" frame_step " in str(handler)):
            handlers.remove(handler)
    handlers.append(frame_step)
    handlers = bpy.app.handlers.scene_update_post
    for handler in handlers:
        if (" vseqf_continuous " in str(handler)):
            handlers.remove(handler)
    handlers.append(vseqf_continuous)


def unregister():
    # Unregister menus
    bpy.types.SEQUENCER_HT_header.remove(draw_quickspeed_header)
    bpy.types.SEQUENCER_MT_view.remove(draw_quickzoom_menu)
    bpy.types.SEQUENCER_MT_view.remove(draw_quicksettings_menu)
    bpy.types.SEQUENCER_MT_strip.remove(draw_quicksnap_menu)

    bpy.types.SEQUENCER_PT_edit.remove(edit_panel)
    bpy.types.SEQUENCER_PT_proxy.remove(proxy_panel)

    # Remove shortcuts
    keymapitems = bpy.context.window_manager.keyconfigs.addon.keymaps['Sequencer'].keymap_items
    for keymapitem in keymapitems:
        if ((keymapitem.type == 'Z') | (keymapitem.type == 'F') | (keymapitem.type == 'S')):
            keymapitems.remove(keymapitem)

    # Remove handlers for modal operators
    handlers = bpy.app.handlers.frame_change_post
    for handler in handlers:
        if (" frame_step " in str(handler)):
            handlers.remove(handler)
    handlers = bpy.app.handlers.scene_update_post
    for handler in handlers:
        if (" vseqf_continuous " in str(handler)):
            handlers.remove(handler)

    try:
        bpy.utils.unregister_class(VSEQuickFunctionSettings)
    except RuntimeError:
        pass

    # Unregister operators
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
