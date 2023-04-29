from logging import Logger

import click

@click.group()
def cli():
    pass

@cli.command("hello")
def hello():
    Logger.info("Hello world!")
