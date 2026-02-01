# Seek Functionality Specification for afplay-win

## Overview
This document specifies the implementation plan for adding seek functionality to the afplay-win project, allowing users to start playback from a specific time position in audio files.

## Current Implementation Analysis

### Current Architecture
- Uses Windows MCI (Media Control Interface) via `winmm.dll`
- Current MCI command flow:
  1. `open "{sound}" type mpegvideo alias {alias}`
  2. `play {alias} wait`
  3. `close {alias}`

### Current CLI Interface
- Single argument: sound file path
- Supports `.mp3` and `.wav` files
- Supports piped input

## Proposed Seek Functionality

### CLI Interface Design

#### New Command Line Options
- `--seek TIME` or `-t TIME`: Specify starting position
- Time format support:
  - Seconds: `30` (30 seconds)
  - Minutes:seconds: `1:30` (1 minute 30 seconds)
  - Hours:minutes:seconds: `1:10:30` (1 hour 10 minutes 30 seconds)

#### Usage Examples
```bash
# Play from 30 seconds
afplay song.mp3 --seek 30
afplay song.mp3 -t 30

# Play from 1 minute 30 seconds
afplay song.mp3 --seek 1:30
afplay song.mp3 -t 1:30

# Play from 1 hour 10 minutes 30 seconds
afplay song.mp3 --seek 1:10:30
afplay song.mp3 -t 1:10:30
```

### Technical Implementation

#### MCI Seek Command
- Use `seek {alias} to {milliseconds}` command
- MCI uses milliseconds for time positioning
- Command will be inserted between `open` and `play` commands

#### Time Parsing Logic
```python
def parse_time_to_ms(time_str):
    """Convert time string to milliseconds"""
    parts = time_str.split(':')
    if len(parts) == 1:  # Seconds
        return int(parts[0]) * 1000
    elif len(parts) == 2:  # Minutes:seconds
        return (int(parts[0]) * 60 + int(parts[1])) * 1000
    elif len(parts) == 3:  # Hours:minutes:seconds
        return (int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])) * 1000
    else:
        raise ValueError("Invalid time format")
```

#### Modified MCI Command Flow
```mci
open "song.mp3" type mpegvideo alias unique_id
seek unique_id to 30000  # Seek to 30 seconds (30000 ms)
play unique_id wait      # Play from the seek position
close unique_id
```

### Code Changes Required

#### 1. CLI Argument Parser (`create_parser()`)
```python
parser.add_argument(
    "--seek", "-t",
    type=str,
    help="Start playback from specified time (format: SS, MM:SS, or HH:MM:SS)",
    default=None
)
```

#### 2. Time Parsing Function
```python
def parse_time_to_milliseconds(time_str):
    """Convert time string to milliseconds for MCI seek command"""
    # Implementation as shown above
```

#### 3. Modified Playback Function (`_playsound_mci_winmm()`)
```python
def _playsound_mci_winmm(sound: str, seek_time: str = None) -> None:
    alias = str(uuid.uuid4())
    _send_winmm_mci_command(f'open "{sound}" type mpegvideo alias {alias}')

    if seek_time:
        ms = parse_time_to_milliseconds(seek_time)
        _send_winmm_mci_command(f'seek {alias} to {ms}')

    _send_winmm_mci_command(f"play {alias} wait")
    _send_winmm_mci_command(f"close {alias}")
```

#### 4. Updated Main Function (`mainrun()`)
```python
def mainrun(soundfile, seek_time=None):
    if soundfile.lower().endswith((".mp3", ".wav")):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        _ = _playsound_mci_winmm(soundfile, seek_time)
```

### Error Handling

#### Validation Rules
1. Time string must be valid format
2. Time values must be non-negative integers
3. At least one time component must be provided
4. No empty or malformed time components

#### Error Messages
- "Invalid time format. Use SS, MM:SS, or HH:MM:SS"
- "Time values must be non-negative integers"
- "Seek time cannot be empty"

### Testing Strategy

#### Unit Tests
1. Test time parsing function with various formats
2. Test error cases (invalid formats, negative values)
3. Test MCI command generation

#### Integration Tests
1. Test actual seeking functionality (Windows only)
2. Test backward compatibility (no seek parameter)
3. Test edge cases (seek to 0, seek beyond file duration)

### Backward Compatibility
- Seek parameter is optional
- Existing usage remains unchanged
- No breaking changes to existing API
- Default behavior (no seek) is identical to current implementation

### Edge Cases to Handle
- Invalid time formats (e.g., "abc", "1:abc", "1:2:3:4")
- Negative time values (e.g., "-30", "-1:30")
- Empty time string
- Non-numeric values in time components
- Seek time exceeding file duration (MCI handles this gracefully)

## Implementation Timeline
1. Add CLI argument parsing
2. Implement time parsing function
3. Modify MCI playback function
4. Update main execution flow
5. Add comprehensive tests
6. Update documentation

## Success Criteria
- Users can specify start time using `--seek` or `-t` option
- Time parsing works for all supported formats
- Seeking actually starts playback from correct position
- Backward compatibility is maintained
- All tests pass
- Error handling is robust and user-friendly