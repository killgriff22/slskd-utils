"""Main slskd-utils CLI entrypoint"""

import click


@click.group()
def cli():
    """Soulseek daemon utilities"""


@cli.command()
def room():
    """Base command for all room operations"""
    click.echo("Currently joined rooms:")


@cli.command()
def search():
    """Base command for all search operations"""
    click.echo("Past searches:")
