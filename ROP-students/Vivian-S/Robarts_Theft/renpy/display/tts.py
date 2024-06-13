# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import sys
import os
import re
import subprocess

import pygame_sdl2 as pygame
import renpy


class TTSDone(str):
    """
    A subclass of string that is returned from a tts function to stop
    further TTS processing.
    """


class TTSRoot(Exception):
    """
    An exception that can be used to cause the TTS system to read the text
    of the root displayable, rather than text of the currently focused
    displayable.
    """


# The root of the scene.
root = None

# The text of the last displayable.
last = ""

# The text of the last displayable, before config.tts_dictionary was applied.
last_raw = ""

# The speech synthesis process.
process = None


def periodic():
    global process

    if process is not None:
        if process.poll() is not None:
            process = None


def is_active():

    return process is not None


def default_tts_function(s):
    """
    Default function which speaks messages using an os-specific method.
    """

    global process

    # Stop the existing process.
    if process is not None:
        try:
            process.terminate()
            process.wait()
        except Exception:
            pass

    process = None

    s = s.strip()

    if not s:
        return

    if renpy.game.preferences.self_voicing == "clipboard":
        try:
            pygame.scrap.put(pygame.scrap.SCRAP_TEXT, s.encode("utf-8"))
        except Exception:
            pass

        return

    if renpy.game.preferences.self_voicing == "debug":
        renpy.exports.restart_interaction()
        return

    fsencode = renpy.exports.fsencode

    amplitude = renpy.game.preferences.get_mixer("voice")
    amplitude_100 = int(amplitude * 100)


    if "RENPY_TTS_COMMAND" in os.environ:

        process = subprocess.Popen([ os.environ["RENPY_TTS_COMMAND"], fsencode(s) ])

    elif renpy.linux:

        cmd = [ "espeak", "-a", fsencode(str(amplitude_100)) ]

        if renpy.config.tts_voice is not None:
            cmd.extend([ "-v", fsencode(renpy.config.tts_voice) ])

        cmd.append(fsencode(s))

        process = subprocess.Popen(cmd)

    elif renpy.macintosh:

        s = "[[volm {}]]".format(amplitude) + s

        if renpy.config.tts_voice is None:
            process = subprocess.Popen([ "say", fsencode(s) ])
        else:
            process = subprocess.Popen([ "say", "-v", fsencode(renpy.config.tts_voice), fsencode(s) ])

    elif renpy.windows:

        if renpy.config.tts_voice is None:
            voice = "default voice" # something that is unlikely to match.
        else:
            voice = renpy.config.tts_voice

        say_vbs = os.path.join(os.path.dirname(sys.executable), "say.vbs")
        s = s.replace('"', "")
        process = subprocess.Popen([ "wscript", fsencode(say_vbs), fsencode(s), fsencode(voice), fsencode(str(amplitude_100)) ])

    elif renpy.emscripten and renpy.config.webaudio:

        try:
            from renpy.audio.webaudio import call
            call("tts", s, amplitude)
        except Exception:
            pass

# A List of (regex, string) pairs.
tts_substitutions = [ ]

def init():
    """
    Initializes the TTS system. This is called automatically by ts, below.
    """

    for pattern, replacement in renpy.config.tts_substitutions:

        if isinstance(pattern, basestring):
            pattern = r'\b' + re.escape(pattern) + r'\b'
            pattern = re.compile(pattern, re.IGNORECASE)
            replacement = re.escape(replacement)


        tts_substitutions.append((pattern, replacement))


def apply_substitutions(s):
    """
    Applies the TTS dictionary to `s`, returning the result.
    """

    def replace(m):
        old = m.group(0)
        if old.istitle():
            template = replacement.title()
        elif old.isupper():
            template = replacement.upper()
        elif old.islower():
            template = replacement.lower()
        else:
            template = replacement

        return m.expand(template)

    for pattern, replacement in tts_substitutions:
        s = pattern.sub(replace, s)

    return s


def tts(s):
    """
    Causes `s` to be spoken.
    """

    try:
        renpy.config.tts_function(s)
    except Exception:
        pass


def speak(s, translate=True, force=False):
    """
    This is called by the system to queue the speaking of message `s`.
    """

    if not force and not renpy.game.preferences.self_voicing:
        return

    if translate:
        s = renpy.translation.translate_string(s)

    tts(s)


def set_root(d):
    global root
    root = d


# The old value of the self_voicing preference.
old_self_voicing = False


def displayable(d):
    """
    Causes the TTS system to read the text of the displayable `d`.
    """

    global old_self_voicing
    global last
    global last_raw

    self_voicing = renpy.game.preferences.self_voicing

    if not self_voicing:
        if old_self_voicing:
            old_self_voicing = self_voicing
            speak(renpy.translation.translate_string("Self-voicing disabled."), force=True)

        last = ""

        return

    prefix = ""

    if not old_self_voicing:
        old_self_voicing = self_voicing

        if self_voicing == "clipboard":
            prefix = renpy.translation.translate_string("Clipboard voicing enabled. ")
        else:
            prefix = renpy.translation.translate_string("Self-voicing enabled. ")

        last_raw = None

    for i in renpy.config.tts_voice_channels:
        if not prefix and renpy.audio.music.get_playing(i):
            return

    if d is None:
        d = root

    while True:
        try:
            s = d._tts_all()
            break
        except TTSRoot:
            if d is root:
                return
            else:
                d = root


    if s != last_raw:
        last_raw = s
        s = apply_substitutions(s)
        last = s
        tts(prefix + s)
