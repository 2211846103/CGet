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
from cget.utils.misc import validate_project_root
from cget.utils.install import install_dependency, install_all


@click.command("install")
@click.argument("source", required=False)
@click.option("--dev", is_flag=True, default=False, help="Add to development enviroment only")
@click.option("--force", is_flag=True, default=False, help="Force re-download of headers")
@click.option("--platforms", default=None, help="Comma-separated list of supported platforms")
def install_command(source: str, dev: bool, force: bool, platforms:str):
  """Add a dependency by user/repo format, e.g. fmtlib/fmt"""
  data = validate_project_root()
  if not data:
    return
  
  if source:
    install_dependency(source, platforms, dev, data, force)
  else:
    installed_count = install_all(data, force)
    click.echo(f"\nInstallation complete. {installed_count} packages installed or updated.")