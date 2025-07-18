import click
import os
import json
from cget.utils import acquire_headers, save_lock, find_best_tag


@click.command("update")
def update_command():
  """Update all dependencies to latest compatible versions and update lock file"""
  if not os.path.exists("cget.json"):
    click.echo("Error: cget.json not found.")
    return
  
  with open("cget.json", "r") as f:
    manifest = json.load(f)

  all_sections = ["dependencies", "devDependencies"]
  combined_lock_data = {}

  for section in all_sections:
    deps = manifest.get(section, [])
    if not deps:
      click.echo(f"No {section} to update.")
      return

    for dep in deps:
      name = dep["name"]
      source = dep["source"]
      version = dep.get("version", None)

      acquire_headers(source, "extern")

      combined_lock_data[name] = {
        "name": name,
        "source": source,
        "resolved": f"https://github.com/{source}.git",
        "version": find_best_tag(source, version)
      }

      click.echo(f"Updated '{name}' to {combined_lock_data[name]['version']}")
  
  save_lock(combined_lock_data)
  click.echo("All dependencies updated and lock file saved.")