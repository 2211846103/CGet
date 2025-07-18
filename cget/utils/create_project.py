import click
import shutil
import cget.config as config
from pathlib import Path
from string import Template
from collections.abc import Mapping
from importlib.resources import files


def load_template(filename: str, mapping: Mapping[str, object] = {}):
  path: Path = files("cget.templates") / filename
  text: str = read(path)
  return Template(text).safe_substitute(mapping)


def ensure_dir(path: Path):
  path.mkdir(parents=True, exist_ok=True)


def write(path: Path, content: str =""):
  path.write_text(content)


def read(path: Path) -> str:
  return path.read_text()


def create_files(base: Path, name: str, version: str, cmake_version: str):
  write(base / ".gitignore", "\n".join(config.GITIGNORE))
  write(base / "README.md", load_template("README.md", {"project_name": name}))
  write(base / "LICENSE", load_template("LICENSE"))
  write(base / "CMakeLists.txt", load_template("main_cmake.txt", {"project_name": name, "version": version, "cmake_version": cmake_version}))
  write(base / "include" / name / "lib.hpp", load_template("lib.hpp", {"project_name": name}))
  write(base / "src" / "lib.cpp", load_template("lib.cpp", {"project_name": name}))
  write(base / "src" / "CMakeLists.txt", load_template("src_cmake.txt", {"project_name": name}))
  write(base / "apps" / "app.cpp", load_template("app.cpp", {"project_name": name}))
  write(base / "apps" / "CMakeLists.txt", load_template("app_cmake.txt", {"project_name": name}))
  write(base / "tests" / "testlib.cpp", load_template("testlib.cpp"))
  write(base / "tests" / "CMakeLists.txt", load_template("tests_cmake.txt"))
  write(base / "docs" / "CMakeLists.txt", load_template("docs_cmake.txt"))
  write(base / "scripts" / "helper.py", load_template("helper.py"))


def create_directories(base: Path, name: str):
  ensure_dir(base / "cmake")
  ensure_dir(base / "include" / name)
  ensure_dir(base / "src")
  ensure_dir(base / "apps")
  ensure_dir(base / "tests")
  ensure_dir(base / "docs")
  ensure_dir(base / "extern")
  ensure_dir(base / "scripts")


def create_project_structure(name, version, cmake_version, force):
  base = Path(name)
  if base.exists() and not force:
    click.echo(f"Directory '{name}' already exists.")
    return
  
  click.echo(f"Creating project: {name}")
  if base.exists():
    shutil.rmtree(base)
  base.mkdir()

  create_directories(base, name)

  create_files(base, name, version, cmake_version)
  
  return base