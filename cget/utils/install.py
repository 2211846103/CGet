import click
import json
import shutil
import tempfile
import subprocess
import os
from pathlib import Path
from cget.utils.misc import save_lock, load_lock, find_best_tag, find_include_root


def parse_source_and_version(source: str) -> tuple[str, str]:
  version = None
  if "@" in source:
    source, version = source.split("@", 1)

  _, repo = source.split("/", 1)
  name = repo
  version = version or "latest"
  
  return (name, version)


def parse_platforms(platforms: str = None) -> (list[str] | None):
  if platforms:
    parsed_platforms = [p.strip().lower() for p in platforms.split(",")]
    return parsed_platforms
  

def prepare_dependency_sections(data: dict, dev: bool) -> tuple[str, str, list[dict], list[dict]]:
  if "dependencies" not in data:
    data["dependencies"] = []
  if "devDependencies" not in data:
    data["devDependencies"] = []
  
  section = "devDependencies" if dev else "dependencies"
  other_section = "dependencies" if dev else "devDependencies"
  deps = data[section]
  other_deps = data[other_section]

  return (section, other_section, deps, other_deps)


def check_for_existing_dependency(data: dict, name: str, dev: bool) -> tuple[dict | None, bool]:
  _, _, deps, other_deps = prepare_dependency_sections(data, dev)
  for d in deps:
    if d["name"] == name:
      return d, True

  for d in other_deps:
    if d["name"] == name:
      return d, False

  return None, False


def save_project_file(data: dict, existing: dict, name: str, version: str):
  with open("cget.json", "w") as f:
    json.dump(data, f, indent=2)
  click.echo(f"{'Updated' if existing else 'Added'} {name}@{version}")


def update_or_add_dependency(data: dict, dep: dict, dev: bool) -> bool:
  section, _, deps, other_deps = prepare_dependency_sections(data, dev)

  name = dep["name"]
  version = dep["version"]

  existing, in_correct_section = check_for_existing_dependency(data, name, dev)

  if existing:
    existing.update(dep)

    if not in_correct_section:
      other_deps.remove(existing)
      deps.append(existing)
      click.echo(f"Moved and updated dependency '{name}' to '{section}' section.")
    else:
      click.echo(f"Updated existing dependency '{name}' in '{section}'.")
    
    save_project_file(data, existing, name, version)
    return False
  else:
    deps.append(dep)
    click.echo(f"Added new dependency '{name}' to '{section}'.")

    save_project_file(data, existing, name, version)
    return True


def download_package(name: str, source: str, version: str, updated: bool, force: bool) -> bool:
  header_path = Path("extern") / name

  dest_dir = Path(".cget_packages") / f"{name}@{version}"

  if force or updated or not header_path.exists() or not dest_dir.exists():
    if dest_dir.exists():
      shutil.rmtree(dest_dir)

    with tempfile.TemporaryDirectory() as tmpdir:
      click.echo(f"Cloning {source}@{version} into temporary directory...")
      subprocess.run([
        "git", "clone", "--depth", "1", "--branch", version, f"https://github.com/{source}.git"
      ], cwd=tmpdir, check=True)

      source_dir = Path(tmpdir) / name
      shutil.copytree(source_dir, dest_dir)
      click.echo(f"Package copied to: {dest_dir}")

    try:
      dest_dir = find_include_root(dest_dir, name)
      if header_path.exists() or header_path.is_symlink():
        header_path.unlink()
        
      os.symlink(dest_dir.resolve(), header_path)
      click.echo(f"Created symlink: {header_path} -> {dest_dir}")
      return True
    except OSError as e:
      click.echo(f"Failed to create symlink: {e}. Try running as Administrator.")
      return False
  else:
    click.echo(f"Package {name}@{version} already installed. Use --force to re-download.")
    return True

  
def update_lock_file(name: str, source: str, version: str, platforms: list[str] = None):
  lock = load_lock()
  lock[name] = {
      "name": name,
      "source": source,
      "resolved": f"https://github.com/{source}.git", # optional, you can use latest tag or fake
      "version": version,
      "platforms": platforms
  }
  save_lock(lock)


def install_dependency(source: str, platforms: str | None, dev: bool, data: dict, force: bool) -> bool:
  if "/" not in source:
    click.echo("Error: Dependency must be in 'user/repo' format.")
    return False
  
  name, version = parse_source_and_version(source)
  parsed_platforms = parse_platforms(platforms)

  updated = update_or_add_dependency(data, {
    "name": name,
    "source": source,
    "version": version,
    "platforms": parsed_platforms
  }, dev)

  version = find_best_tag(source, version)

  if not download_package(name, source, version, updated, force):
    return False

  update_lock_file(name, source, version)
  return True


def install_all(data: dict, force: bool = False) -> bool:
  click.echo("Installing all dependencies from cget.lock.json...")

  dependencies = data.get("dependencies", []) + data.get("devDependencies", [])
  if not dependencies:
    return 0
  
  installed_count = 0
  lock = load_lock()
  for dep in dependencies:
    source = dep["source"]
    name, version = parse_source_and_version(source)
    version = find_best_tag(source, version)
    locked = lock.get(name)
    if locked:
        source = locked["source"]
        version = locked["version"]

    header_path = Path("extern") / name
    package_path = Path(".cget_packages") / f"{name}@{version}"

    if not force and package_path.exists() and header_path.exists():
      click.echo(f"-> Skipping '{name}' (already installed)")
      continue

    click.echo(f"-> Installing '{name}' from {source}...")

    if not download_package(name, source, version, True, force):
      return installed_count
    installed_count += 1
  
  return installed_count