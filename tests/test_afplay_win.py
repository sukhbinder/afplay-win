import sys
import pytest
from afplay_win import cli


def test_create_parser():
    parser = cli.create_parser()
    result = parser.parse_args(["hello.mp3"])
    assert result.sound == "hello.mp3"
    assert result.seek is None


def test_create_parser_with_seek():
    parser = cli.create_parser()
    result = parser.parse_args(["hello.mp3", "--seek", "30"])
    assert result.sound == "hello.mp3"
    assert result.seek == "30"


def test_parse_time_to_milliseconds():
    """Test time parsing function with various formats."""
    # Test seconds format
    assert cli.parse_time_to_milliseconds("30") == 30000
    assert cli.parse_time_to_milliseconds("0") == 0
    assert cli.parse_time_to_milliseconds("60") == 60000
    
    # Test minutes:seconds format
    assert cli.parse_time_to_milliseconds("1:30") == 90000
    assert cli.parse_time_to_milliseconds("0:30") == 30000
    assert cli.parse_time_to_milliseconds("2:00") == 120000
    
    # Test hours:minutes:seconds format
    assert cli.parse_time_to_milliseconds("1:10:30") == 4230000
    assert cli.parse_time_to_milliseconds("0:1:30") == 90000
    assert cli.parse_time_to_milliseconds("1:0:0") == 3600000


def test_parse_time_errors():
    """Test error cases for time parsing."""
    # Test empty string
    with pytest.raises(ValueError, match="Seek time cannot be empty"):
        cli.parse_time_to_milliseconds("")
    
    with pytest.raises(ValueError, match="Seek time cannot be empty"):
        cli.parse_time_to_milliseconds("   ")
    
    # Test invalid formats
    with pytest.raises(ValueError, match="Invalid time format"):
        cli.parse_time_to_milliseconds("abc")
    
    with pytest.raises(ValueError, match="Invalid time format"):
        cli.parse_time_to_milliseconds("1:abc")
    
    with pytest.raises(ValueError, match="Invalid time format"):
        cli.parse_time_to_milliseconds("1:2:3:4")
    
    # Test negative values
    with pytest.raises(ValueError, match="Time values must be non-negative"):
        cli.parse_time_to_milliseconds("-30")
    
    with pytest.raises(ValueError, match="Time values must be non-negative"):
        cli.parse_time_to_milliseconds("-1:30")
    
    with pytest.raises(ValueError, match="Time values must be non-negative"):
        cli.parse_time_to_milliseconds("1:-30")
    
    with pytest.raises(ValueError, match="Time values must be non-negative"):
        cli.parse_time_to_milliseconds("1:30:-5")


def test_mainrun(monkeypatch):
    def mockret(*args, **kwargs):
        return 0

    monkeypatch.setattr(cli, "_playsound_mci_winmm", mockret)
    cli.mainrun("test.mp3")  # No seek
    cli.mainrun("test.mp3", "30")  # With seek


def test_mainrun_with_invalid_seek(monkeypatch):
    # Test that invalid seek time raises ValueError in parse_time_to_milliseconds
    # We need to mock the Windows-specific MCI calls on non-Windows platforms
    
    def mock_mci_command(command):
        # Mock the MCI command function to avoid Windows-specific calls
        return b""
    
    monkeypatch.setattr(cli, "_send_winmm_mci_command", mock_mci_command)
    
    with pytest.raises(ValueError, match="Invalid time format"):
        cli.mainrun("test.mp3", "invalid")


@pytest.mark.skipif(sys.platform != "win32", reason="requires Windows")
def test_integration():
    """Test that the sound is played without errors."""
    cli.mainrun("tests/hello.mp3")


@pytest.mark.skipif(sys.platform != "win32", reason="requires Windows")
def test_integration_with_seek():
    """Test that seeking works correctly."""
    cli.mainrun("tests/hello.mp3", "5")  # Seek to 5 seconds
