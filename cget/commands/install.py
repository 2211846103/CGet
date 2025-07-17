import click
import json
import os
from pathlib import Path
from cget.utils import acquire_headers


@click.command("install")
@click.argument("source")
@click.option("--dev", is_flag=True, default=False, help="Add to development enviroment only")
@click.option("--version", default=None, help="Version or Tag to checkout (optional)")
@click.option("--force", is_flag=True, default=False, help="Force re-download of headers")
@click.option("--platforms", default=None, help="Comma-separated list of supported platforms")
def install_command(source: str, version, dev: bool, force: bool, platforms:str):
  """Add a dependency by user/repo format, e.g. fmtlib/fmt"""
  if not os.path.exists("cget.json"):
    click.echo("Error: cget.json not found. Run `cget init` first.")
    return
  
  if "/" not in source:
    click.echo("Error: Dependency must be in 'user/repo' format.")
    return
  
  user, repo = source.split("/", 1)
  name = repo
  version = version or "latest"
  if platforms:
    platforms = [p.string().lower() for p in platforms.split(",")]

  with open("cget.json", "r") as f:
    data = json.load(f)

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

  with open("cget.json", "w") as f:
    json.dump(data, f, indent=2)

  click.echo(f"{'Updated' if existing else 'Added'} {name}@{version}")

  header_path = Path("extern") / name
  if force or updated or not header_path.exists():
    acquire_headers(source, "extern")
  else:
    click.echo("Headers already installed. Use --force to re-download.")