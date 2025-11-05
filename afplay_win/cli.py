import argparse
import uuid
import ctypes
import logging
import signal
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def _send_winmm_mci_command(command):
    winmm = ctypes.WinDLL("winmm.dll")
    buffer = ctypes.create_string_buffer(255)
    error_code = winmm.mciSendStringA(ctypes.c_char_p(command.encode()), buffer, 254, 0)
    if error_code:
        logger.error("MCI error code: %s", error_code)
    return buffer.value


def _playsound_mci_winmm(sound: str) -> None:
    """Play a sound utilizing windll.winmm."""

    # Select a unique alias for the sound
    alias = str(uuid.uuid4())
    logger.debug("winmm: starting playing %s", sound)
    _send_winmm_mci_command(f'open "{sound}" type mpegvideo alias {alias}')
    _send_winmm_mci_command(f"play {alias} wait")
    _send_winmm_mci_command(f"close {alias}")
    logger.debug("winmm: finishing play %s", sound)


def create_parser():
    parser = argparse.ArgumentParser(description="afplay for windows using python")
    parser.add_argument(
        "sound",
        type=str,
        nargs="?",
        help="Path to .mp3 or .wav file (or pipe the path)",
    )
    return parser


def cli():
    "afplay for windows using python"
    parser = create_parser()
    args = parser.parse_args()
    sound = args.sound

    # If no argument and something piped in
    if sound is None and not sys.stdin.isatty():
        piped = sys.stdin.read().strip()
        if piped:
            sound = piped

    # If still nothing, show error like normal argparse would
    if not sound:
        parser.error("No input sound file provided. Pass a file or pipe a name.")

    # Validate extension
    if not (Path(sound).match("*.mp3") or Path(sound).match("*.wav")):
        parser.error("Only .mp3 or .wav files supported.")

    # Validate exists
    if not os.path.exists(sound):
        parser.error(f"File not found: {sound}")
    mainrun(sound)


def mainrun(soundfile):
    if soundfile.lower().endswith((".mp3", ".wav")):
        logger.debug("Playing", soundfile)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        _ = _playsound_mci_winmm(soundfile)
