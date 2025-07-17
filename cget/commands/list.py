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