
import click


class CLILayer:
    
    @click.command()
    @click.option('--name', prompt='Name of the project', help='Name of the fastapi apploication')
    def init_melia(name):
        return click.echo(f"test init command: {name}")
