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
import os


@click.command("list")
def list_command():
  """List all installed dependencies"""
  if not os.path.exists("cget.json"):
    click.echo("Error: cget.json not found.")
    return

  with open("cget.json", "r") as f:
    data = json.load(f)

  deps = data.get("dependencies", [])
  if not deps:
    click.echo("No dependencies installed.")
    return

  click.echo("Installed dependencies:")
  for dep in deps:
    version = dep.get("version", "unspecified")
    build = dep.get("build", "release")
    click.echo(f" - {dep['name']} ({version}, {build})")