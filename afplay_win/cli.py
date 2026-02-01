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


def parse_time_to_milliseconds(time_str):
    """Convert time string to milliseconds for MCI seek command.

    Supports formats:
    - SS: seconds (e.g., "30" -> 30000ms)
    - MM:SS: minutes:seconds (e.g., "1:30" -> 90000ms)
    - HH:MM:SS: hours:minutes:seconds (e.g., "1:10:30" -> 4230000ms)

    Args:
        time_str: Time string in supported format

    Returns:
        int: Time in milliseconds

    Raises:
        ValueError: If time format is invalid or values are negative
    """
    if not time_str or not time_str.strip():
        raise ValueError("Seek time cannot be empty")

    parts = time_str.strip().split(':')

    if len(parts) == 1:  # Seconds
        try:
            seconds = int(parts[0])
        except ValueError:
            raise ValueError(f"Invalid time format: '{time_str}'. Expected number for seconds.")

        if seconds < 0:
            raise ValueError("Time values must be non-negative")

        return seconds * 1000

    elif len(parts) == 2:  # Minutes:seconds
        try:
            minutes = int(parts[0])
            seconds = int(parts[1])
        except ValueError:
            raise ValueError(f"Invalid time format: '{time_str}'. Expected numbers for minutes and seconds.")

        if minutes < 0 or seconds < 0:
            raise ValueError("Time values must be non-negative")

        return (minutes * 60 + seconds) * 1000

    elif len(parts) == 3:  # Hours:minutes:seconds
        try:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
        except ValueError:
            raise ValueError(f"Invalid time format: '{time_str}'. Expected numbers for hours, minutes, and seconds.")

        if hours < 0 or minutes < 0 or seconds < 0:
            raise ValueError("Time values must be non-negative")

        return (hours * 3600 + minutes * 60 + seconds) * 1000

    else:
        raise ValueError(f"Invalid time format: '{time_str}'. Use SS, MM:SS, or HH:MM:SS format.")


def _playsound_mci_winmm(sound: str, seek_time: str = None) -> None:
    """Play a sound utilizing windll.winmm.

    Args:
        sound: Path to sound file
        seek_time: Optional seek time string (format: SS, MM:SS, or HH:MM:SS)
    """
    # Select a unique alias for the sound
    alias = str(uuid.uuid4())
    logger.debug("winmm: starting playing %s", sound)

    _send_winmm_mci_command(f'open "{sound}" type mpegvideo alias {alias}')

    # Add seek command if seek time is provided
    if seek_time:
        try:
            seek_ms = parse_time_to_milliseconds(seek_time)
            logger.debug("winmm: seeking to %s ms", seek_ms)
            _send_winmm_mci_command(f'seek {alias} to {seek_ms}')
        except ValueError as e:
            logger.error("Seek error: %s", e)
            raise

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
    parser.add_argument(
        "--seek", "-t",
        type=str,
        help="Start playback from specified time (format: SS, MM:SS, or HH:MM:SS)",
        default=None
    )
    return parser


def cli():
    "afplay for windows using python"
    parser = create_parser()
    args = parser.parse_args()
    sound = args.sound
    seek_time = args.seek

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

    mainrun(sound, seek_time)


def mainrun(soundfile, seek_time=None):
    """Main function to run audio playback.

    Args:
        soundfile: Path to sound file
        seek_time: Optional seek time string
    """
    if soundfile.lower().endswith((".mp3", ".wav")):
        logger.debug("Playing %s", soundfile)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        _ = _playsound_mci_winmm(soundfile, seek_time)
