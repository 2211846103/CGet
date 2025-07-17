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
import os
import json
import shutil


@click.command("uninstall")
@click.argument("source")
def uninstall_command(source: str):
  """Uninstall a dependency by source"""
  if not os.path.exists("cget.json"):
    click.echo("Error: cget.json not found.")
    return
  
  with open("cget.json", "r") as f:
    data = json.load(f)

  deps = data.get("dependencies", [])
  filtered = [d for d in deps if d["source"] != source]

  if len(filtered) == len(deps):
    click.echo(f"Dependency '{source}' not found.")
    return
  
  data["dependencies"] = filtered

  with open("cget.json", "w") as f:
    json.dump(data, f, indent=2)

  _,repo = source.split("/", 1)

  path = os.path.join("extern", repo)
  if os.path.exists(path):
    shutil.rmtree(path)

  click.echo(f"Removed dependency '{source}'")