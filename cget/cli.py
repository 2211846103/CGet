import click
from cget.commands.init import init_command
from cget.commands.install import install_command
from cget.commands.build import build_command
from cget.commands.remove import remove_command
from cget.commands.list import list_command


@click.group()
def cli():
  """C++ Package Manager based on CPM.cmake"""
  pass

cli.add_command(init_command)
cli.add_command(install_command)
cli.add_command(build_command)
cli.add_command(remove_command)
cli.add_command(list_command)