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
import subprocess
import platform
import urllib.request
from pathlib import Path
from cget.utils.misc import load_lock
from cget.utils.generate_build_cmake import generate_build_cmake


@click.command("build")
@click.option("--dev", is_flag=True, default=False, help="Build the project in Development mode.")
@click.option("--generator", default=None, help="CMake generator to use.")
@click.option("--build-dir", default="./build", help="Build path")
@click.option("--verbose", is_flag=True, default=False, help="Verbose output")
def build_command(dev: bool, generator: str, build_dir, verbose):
  """Install all dependencies and build project"""
  
  project_root = Path(".")
  cget_path = project_root / "cget.json"
  cpm_path = project_root / "cmake" / "CPM.cmake"
  cmake_path = project_root / "CMakeLists.txt"
  dependencies_path = project_root / "_dependencies.cmake"
  build_dir = Path(build_dir)

  if not cget_path.exists():
    click.echo("Error: cget.json not found.")
    return
  
  if not cmake_path.exists():
    click.echo("Error: CMakeLists.txt not found.")
    return
  
  if not cpm_path.exists():
    click.echo("Downloading CPM.cmake...")
    os.makedirs(project_root / "cmake", exist_ok=True)
    url = "https://github.com/cpm-cmake/CPM.cmake/releases/latest/download/CPM.cmake"
    urllib.request.urlretrieve(url, cpm_path)
    click.echo("CPM.cmake downloaded")

  with open(cget_path, "r") as f:
    data = json.load(f)

  dependencies = data.get("dependencies", [])
  if dev:
    dependencies += data.get("devDependencies", [])
    
  compiler_options = data.get("compilerOptions", {})
  
  generate_build_cmake(dependencies, dependencies_path, compiler_options)
  
  build_dir.mkdir(exist_ok=True)

  click.echo("Running CMake configuration...")
  cmd = ["cmake", ".."]
  if verbose:
      cmd.append("--verbose")
  if generator:
    cmd.append("-G")
    cmd.append(f"{generator}")
  if dev:
    cmd.append("-DCMAKE_BUILD_TYPE=Debug")
  result = subprocess.run(cmd, cwd=build_dir)
  if result.returncode != 0:
    click.echo("CMake configuration failed.")
    return
  
  click.echo("Building project...")
  result = subprocess.run(["cmake", "--build", "."], cwd=build_dir)
  if result.returncode != 0:
    click.echo("Build failed.")
    return
  
  os.remove(dependencies_path)

  click.echo("Build complete.")