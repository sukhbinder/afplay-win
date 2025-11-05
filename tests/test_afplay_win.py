import sys
import pytest
from afplay_win import cli


def test_create_parser():
    parser = cli.create_parser()
    result = parser.parse_args(["hello.mp3"])
    assert result.sound == "hello.mp3"


def test_mainrun(monkeypatch):
    def mockret(*args, **kwargs):
        return 0

    monkeypatch.setattr(cli, "_playsound_mci_winmm", mockret)
    cli.mainrun("test.mp3")


@pytest.mark.skipif(sys.platform != "win32", reason="requires Windows")
def test_integration():
    """Test that the sound is played without errors."""
    cli.mainrun("tests/hello.mp3")
