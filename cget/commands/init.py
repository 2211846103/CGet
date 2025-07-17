import click
import json
from pathlib import Path
from cget.utils import create_project_structure


@click.command("init")
@click.option("--name", prompt="Project name", help="Name of your project")
@click.option("--cmake-version", default="3.27", help="Version of CMake")
@click.option("--force", is_flag=True, default=False, help="Force reset project")
def init_command(name, cmake_version, force):
  """Initialize a new cget.json"""
  base: Path = create_project_structure(name, cmake_version, force)

  data = {
    "name": name,
    "version": "0.1.0",
    "dependencies": []
  }

  with open(base / "cget.json", "w") as out:
    json.dump(data, out, indent=2)

  print("Intialized cget.json")