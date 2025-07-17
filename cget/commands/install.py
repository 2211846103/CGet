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
from pathlib import Path
from cget.utils import acquire_headers


@click.command("install")
@click.argument("source", required=False)
@click.option("--dev", is_flag=True, default=False, help="Add to development enviroment only")
@click.option("--version", default=None, help="Version or Tag to checkout (optional)")
@click.option("--force", is_flag=True, default=False, help="Force re-download of headers")
@click.option("--platforms", default=None, help="Comma-separated list of supported platforms")
def install_command(source: str, version, dev: bool, force: bool, platforms:str):
  """Add a dependency by user/repo format, e.g. fmtlib/fmt"""
  if not os.path.exists("cget.json"):
    click.echo("Error: cget.json not found. Run `cget init` first.")
    return
  
  with open("cget.json", "r") as f:
    data = json.load(f)
  
  if source:
    if "/" not in source:
      click.echo("Error: Dependency must be in 'user/repo' format.")
      return
    
    user, repo = source.split("/", 1)
    name = repo
    version = version or "latest"
    if platforms:
      platforms = [p.string().lower() for p in platforms.split(",")]

    if "dependencies" not in data:
      data["dependencies"] = []

    existing = next((d for d in data["dependencies"] if d["name"] == name), None)
    updated = False

    if existing:
      if existing["version"] != version or existing["build"] != ("dev" if dev else "release"):
        click.echo(f"Dependency '{name}' exists, updating it.")
        existing["version"] = version
        existing["build"] = "dev" if dev else "release"
        if platforms:
          existing["platforms"] = platforms
        updated = True
      else:
        click.echo(f"Dependency '{name}' already exists.")
    else:
      dep = {
        "name": name,
        "source": source,
        "version": version,
        "build": "dev" if dev else "release"
      }
      if platforms:
        dep["platforms"] = platforms
      data["dependencies"].append(dep)
      updated = True

    if updated:
      with open("cget.json", "w") as f:
        json.dump(data, f, indent=2)
      click.echo(f"{'Updated' if existing else 'Added'} {name}@{version}")

    header_path = Path("extern") / name
    if force or updated or not header_path.exists():
      acquire_headers(source, "extern")
    else:
      click.echo("Headers already installed. Use --force to re-download.")

  else:
    click.echo("Installing all dependencies from cget.json...")

    dependencies = data.get("dependencies", [])
    if not dependencies:
      click.echo("No dependencies found in cget.json. Nothing to do.")
      return
    
    installed_count = 0
    for dep in dependencies:
      dep_name = dep["name"]
      dep_source = dep["source"]
      header_path = Path("extern") / dep_name
      
      if not force and header_path.exists():
        click.echo(f"-> Skipping '{dep_name}' (already installed)")
        continue
      
      click.echo(f"-> Installing '{dep_name}' from {dep_source}...")
      try:
        acquire_headers(dep_source, "extern")
        installed_count += 1
      except Exception as e:
        click.secho(f"   Error installing {dep_name}: {e}", fg="red")
        
    click.echo(f"\nInstallation complete. {installed_count} packages installed or updated.")