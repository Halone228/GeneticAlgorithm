import click
from simul import start
import os


@click.command()
@click.option('--gs', default=False, help='Enable or disable graphical simulation, default disabled', type=bool)
@click.argument('model_name')
@click.option('--save-best', default=False, help='Saves best solution of model', type=bool)
@click.option('--load-path',default=None, type=str)
def cli(gs, model_name, save_best, load_path):
    os.environ['gs'] = '1' if gs else ''
    os.environ['model_name'] = model_name
    os.environ['save_best'] = '1' if save_best else ''
    os.environ['load_path'] = '' if load_path is None else load_path
    start()


if __name__ == "__main__":
    cli()

