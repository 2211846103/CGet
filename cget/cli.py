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
from cget.commands.init import init_command
from cget.commands.install import install_command
from cget.commands.build import build_command
from cget.commands.uninstall import uninstall_command
from cget.commands.list import list_command


@click.group()
def cli():
  """C++ Package Manager based on CPM.cmake"""
  pass

cli.add_command(init_command)
cli.add_command(install_command)
cli.add_command(build_command)
cli.add_command(uninstall_command)
cli.add_command(list_command)