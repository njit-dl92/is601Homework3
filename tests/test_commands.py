import pytest
from app import App
from app.commands.goodbye import GoodbyeCommand
from app.commands.greet import GreetCommand
import logging

def test_greet_command(caplog):
    command = GreetCommand()
    with caplog.at_level(logging.INFO):
        command.execute()
    assert "Hello, World!" in caplog.text, "The GreetCommand should log 'Hello, World!'"

def test_goodbye_command(caplog):
    command = GoodbyeCommand()  # Ensure you instantiate GoodbyeCommand
    with caplog.at_level(logging.INFO):
        command.execute()
    assert "Goodbye" in caplog.text, "The GoodbyeCommand should log 'Goodbye'"

def test_app_greet_command(caplog, capfd, monkeypatch):
    """Test that the REPL correctly handles the 'greet' command."""
    # Simulate user entering 'greet' followed by 'exit'
    inputs = iter(['greet', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()  # This should raise SystemExit
    
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

def test_app_menu_command(caplog, capfd, monkeypatch):
    """Test that the REPL correctly handles the 'menu' command."""
    # Simulate user entering 'menu' followed by 'exit'
    inputs = iter(['menu', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()  # This should raise SystemExit
    
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

