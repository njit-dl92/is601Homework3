import os
import pytest
import logging
import multiprocessing
from app import App


@pytest.fixture
def app():
    """Create a fresh instance of the App for testing."""
    return App()


def test_is_valid_command(app):
    """Test command validation."""
    app.command_handler.commands = {'hello': 'HelloCommand'}  # Mocking the command handler
    
    assert app.is_valid_command('hello') is True, "Command 'hello' should be valid."
    assert app.is_valid_command('unknown_command') is False, "Unknown command should not be valid."



def test_execute_in_process_unknown_command(app, caplog):
    """Test how the app handles an unknown command."""
    app.command_handler.commands = {'hello': 'HelloCommand'}  # Mocking the command handler
    
    with caplog.at_level(logging.INFO):
        app.execute_in_process('unknown_command')
    
    assert "No such command: unknown_command" in caplog.text, "The log should indicate an unknown command."


def test_load_plugins(app, monkeypatch):
    """Test if plugins are loaded correctly."""
    # Mock the CommandHandler to avoid errors
    app.command_handler.commands = {}  # Initialize to an empty dictionary

    # Mocking the pkgutil to simulate plugin loading
    with monkeypatch.context() as m:
        m.setattr('pkgutil.iter_modules', lambda x: [(None, 'test_plugin', True)])
        m.setattr('importlib.import_module', lambda x: None)  # Mock import to avoid ImportError
        # Simulate a plugin registering a command
        app.command_handler.commands['plugin_command'] = 'PluginCommand'
        app.load_plugins()  # Call load_plugins
        
    assert 'plugin_command' in app.command_handler.commands, "Commands should be registered from plugins."


def test_cleanup_processes(app):
    """Test cleanup of processes."""
    # Create a mock process
    process = multiprocessing.Process(target=lambda: None)
    process.start()  # Start the process before appending to the list
    app.processes.append(process)
    
    app.cleanup_processes()  # Call cleanup_processes
    
    # Verify that the process has been joined (which means it has finished)
    assert not process.is_alive(), "The process should be cleaned up and not alive."


def test_app_start_exit_command(app, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')

    try:
        app.start()  # This should raise SystemExit
    except SystemExit as e:
        assert str(e) == "Exiting...", "The app should exit with 'Exiting...' message."


def test_app_start_unknown_command(app, caplog, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    with caplog.at_level(logging.INFO):
        with pytest.raises(SystemExit):
            app.start()  # Start the app to run the REPL

    assert "No such command: unknown_command" in caplog.text, "The log should indicate an unknown command."
