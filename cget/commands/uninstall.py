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
from cget.utils.misc import save_lock, load_lock
from pathlib import Path


@click.command("uninstall")
@click.argument("source")
def uninstall_command(source: str):
  """Uninstall a dependency by source"""
  if not os.path.exists("cget.json"):
    click.echo("Error: cget.json not found.")
    return
  
  with open("cget.json", "r") as f:
    data = json.load(f)

  found = False

  for section in ["dependencies", "devDependencies"]:
    deps = data.get(section, [])
    filtered = [d for d in deps if d["source"] != source]

    if len(filtered) != len(deps):
      data[section] = filtered
      found = True
      click.echo(f"Removed '{source}' from {section}.")

  if not found:
    click.echo(f"Dependency '{source}' not found.")
    return

  with open("cget.json", "w") as f:
    json.dump(data, f, indent=2)
  
  if os.path.exists("cget.lock.json"):
    lock_data = load_lock()

    to_remove = None
    for name, meta in lock_data.items():
      if meta.get("source") == source:
        to_remove = name
        break

    if to_remove:
      del lock_data[to_remove]
      save_lock(lock_data)
      click.echo(f"Updated cget.lock.json to remove '{to_remove}'.")

  _,repo = source.split("/", 1)

  extern_path = Path(os.path.join("extern", repo))
  if extern_path.exists() or extern_path.is_symlink():
        extern_path.unlink()

  package_path = os.path.join(".cget_packages", repo)
  if os.path.exists(package_path):
    shutil.rmtree(package_path)

  click.echo(f"Removed dependency '{source}'")