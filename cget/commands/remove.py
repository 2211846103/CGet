import click
import os
import json
import shutil


@click.command("remove")
@click.argument("name")
def remove_command(name: str):
  """Remove a dependency by name"""
  if not os.path.exists("cget.json"):
    click.echo("Error: cget.json not found.")
    return
  
  with open("cget.json", "r") as f:
    data = json.load(f)

  deps = data.get("dependencies", [])
  filtered = [d for d in deps if d["name"] != name]

  if len(filtered) == len(deps):
    click.echo(f"Dependency '{name}' not found.")
    return
  
  data["dependencies"] = filtered

  with open("cget.json", "w") as f:
    json.dump(data, f, indent=2)

  path = os.path.join("extern", name)
  if os.path.exists(path):
    shutil.rmtree(path)
    click.echo(f"Removed header folder: extern/{name}")

  click.echo(f"Removed dependency '{name}'")