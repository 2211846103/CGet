#    CGet - A lightweight package manager for C++ projects using CMake and CPM.
#    Copyright (C) 2025  Mohamed Ibrahim
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    For questions, feedback, or contributions, you can reach me at:
#                   Email: m.ibrahim9276@gmail.com


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