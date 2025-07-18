import click
import os
import json
from cget.utils.install import download_package
from cget.utils.misc import find_best_tag, save_lock


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
      continue

    for dep in deps:
      name = dep["name"]
      version_range = dep.get("version", "latest")
      source = dep.get("source")
      
      if not source:
        # Default to user/repo = name if source not set
        source = name

      resolved_version = find_best_tag(source, version_range)

      success = download_package(name, source, resolved_version, updated=True, force=True)
      if not success:
        click.echo(f"Failed to update '{name}'")
        continue

      combined_lock_data[name] = {
        "name": name,
        "source": source,
        "resolved": f"https://github.com/{source}.git",
        "version": resolved_version
      }

      click.echo(f"Updated '{name}' to version '{resolved_version}'")

  save_lock(combined_lock_data)
  click.echo("All dependencies updated and lock file saved.")