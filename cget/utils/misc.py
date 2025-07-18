import click
import json
import os
import requests
from pathlib import Path
from packaging.specifiers import SpecifierSet
from packaging.version import Version, InvalidVersion


def validate_project_root() -> dict:
  if not os.path.exists("cget.json"):
    click.echo("Error: cget.json not found. Run `cget init` first.")
    return False

  with open("cget.json", "r") as f:
    data = json.load(f)
  
  return data


def get_github_tags(source) -> list[str]:
  """Fetch all git tags from GitHub repo 'user/repo'."""
  url = f"https://api.github.com/repos/{source}/tags"
  tags = []
  page = 1

  while True:
    response = requests.get(url, params={"per_page": 100, "page": page})
    response.raise_for_status()
    data = response.json()
    if not data:
      break
    tags.extend([tag["name"] for tag in data])
    page += 1
    
  return tags


def find_best_tag(source: str, version_range: str):
  """Finds the latest stable version from source that satisfies the range"""
  if version_range == "latest":
    version_range = ">=0.0"

  spec = SpecifierSet(version_range)

  candidate_versions = []
  for tag in get_github_tags(source):
      clean_tag = tag.lstrip('v')
      try:
          version = Version(clean_tag)
          if not version.is_prerelease and version in spec:
              candidate_versions.append(version)
      except InvalidVersion:
          continue

  if not candidate_versions:
      return None

  best_version = max(candidate_versions)
  return str(best_version)


def save_lock(lock_data):
  with open("cget.lock.json", "w") as f:
    json.dump(lock_data, f, indent=2)


def load_lock() -> dict:
  if Path("cget.lock.json").exists():
    with open("cget.lock.json", "r") as f:
      return json.load(f)
  return {}


def find_include_root(dest_dir: Path, name: str) -> Path:
  """
  Tries to find the correct subdirectory in dest_dir to symlink as the include path.
  Prefers: <dest_dir>/include/<name>, <dest_dir>/<name>, or just <dest_dir> itself if it contains headers.
  """
  candidates = [
    dest_dir / "include" / name,
    dest_dir / name,
    dest_dir / "include",
    dest_dir,
  ]

  for path in candidates:
    if path.exists() and any(path.rglob("*.h")):
      return path

  raise RuntimeError(f"Could not find a valid include path in {dest_dir}")