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
import urllib.request
import shutil
import tempfile
import subprocess
from pathlib import Path


def acquire_headers(repo: str, dest_root):
   user, name = repo.split("/")
   dest_root = Path(dest_root) / name

   with tempfile.TemporaryDirectory() as tmpdir:
      print(f"Cloning {repo} into temporary directory...")
      subprocess.run(["git", "clone", "--depth", "1", f"http://github.com/{repo}.git"], cwd=tmpdir, check=True, stdout=subprocess.DEVNULL)

      source_dir = Path(tmpdir) / name

      headers = list(source_dir.rglob("*.h")) + list(source_dir.rglob("*.hpp")) + list(source_dir.rglob("*.hxx"))

      for header in headers:
         rel_path = header.relative_to(source_dir)
         target_path = dest_root / rel_path
         target_path.parent.mkdir(parents=True, exist_ok=True)
         shutil.copy2(header, target_path)
      
      print(f"Headers copied to: {dest_root}")


def create_project_structure(name, cmake_version, force):
  base = Path(name)
  if base.exists() and not force:
    click.echo(f"Directory '{name}' already exists.")
    return
  
  click.echo(f"Creating project: {name}")
  if base.exists():
    shutil.rmtree(base)
  base.mkdir()

  (base / ".gitignore").write_text("build/\n")
  (base / "README.md").write_text(f"# {name}\n\nProject generated with cget.")
  (base / "LICENSE.md").write_text("MIT License\n\n[Put your license text here]")
  (base / "CMakeLists.txt").write_text(f"""\
cmake_minimum_required(VERSION {cmake_version})
project({name})

include(cmake/CPM.cmake)
if(EXISTS "${{CMAKE_SOURCE_DIR}}/_dependencies.cmake")
    include("${{CMAKE_SOURCE_DIR}}/_dependencies.cmake")
endif()

add_subdirectory(src)
add_subdirectory(apps)
add_subdirectory(tests)
""")

  def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)

  def write(path, content=""):
    path.write_text(content)
  
  ensure_dir(base / "cmake")

  ensure_dir(base / "include" / name)
  write(base / "include" / name / "lib.hpp", f"#pragma once\n\nnamespace {name} {{\n  void hello();\n}}")
  
  ensure_dir(base / "src")
  write(base / "src" / "lib.cpp", f"""\
#include <iostream>
#include "{name}/lib.hpp"

namespace {name} {{
  void hello() {{
  std::cout << "Hello from {name}!\\n";
  }}
}}""")
  write(base / "src" / "CMakeLists.txt", f"""\
file(GLOB_RECURSE SRC "*.cpp")
add_library({name}_lib ${{SRC}})

target_include_directories({name}_lib PUBLIC
  ${{PROJECT_SOURCE_DIR}}/include
  ${{PROJECT_SOURCE_DIR}}/extern
)
target_compile_definitions({name}_lib PUBLIC ${{MACROS}})
""")

  ensure_dir(base / "apps")
  write(base / "apps" / "app.cpp", f"""\
#include "{name}/lib.hpp"

int main() {{
  {name}::hello();
  return 0;
}}
""")

  write(base / "apps" / "CMakeLists.txt", f"""\
add_executable({name}_app
    app.cpp
)
target_link_libraries({name}_app PRIVATE {name}_lib ${{DEPENDENCY_LIBS}})
target_compile_definitions({name}_app PUBLIC ${{MACROS}})
""")

  ensure_dir(base / "tests")
  write(base / "tests" / "testlib.cpp", "// TODO: Write tests")
  write(base / "tests" / "CMakeLists.txt", "enable_testing()\n# Add test executables here")

  ensure_dir(base / "docs")
  write(base / "docs" / "CMakeLists.txt", "# Optional doc generation scripts")

  ensure_dir(base / "extern")

  ensure_dir(base / "scripts")
  write(base / "scripts" / "helper.py", "#!/usr/bin/env python3\n\nprint('Helper script')")

  return base


def get_default_branch(owner_repo):
    url = f"https://api.github.com/repos/{owner_repo}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return data.get("default_branch", "main")
    except Exception as e:
        print(f"Warning: Failed to get default branch for {owner_repo}: {e}")
        return "main"