import json
import os
import sys


def pytest_configure():
    # Path to the settings.json file
    settings_path = os.path.join(os.path.dirname(__file__), ".vscode", "settings.json")

    # Read the settings.json file
    with open(settings_path, "r") as f:
        settings = json.load(f)

    # Extract the extraPaths
    extra_paths = settings.get("python.analysis.extraPaths", [])

    # Add each path to sys.path
    for path in extra_paths:
        full_path = os.path.join(os.path.dirname(__file__), path)
        if full_path not in sys.path:
            sys.path.append(full_path)
