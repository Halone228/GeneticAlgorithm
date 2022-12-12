import click
from simul import start
import os
import logging
logging.basicConfig(filename='base.log')


@click.command()
@click.option('--gs', default=False, help='Enable or disable graphical simulation, default disabled', type=bool)
@click.argument('model_name')
@click.option('--save-path', default='', help='Saves best solution of model', type=str)
@click.option('--load-path',default=None, type=str)
@click.option('--plot', default=False, type=bool)
def cli(gs, model_name, save_path, load_path, plot):
    os.environ['gs'] = '1' if gs else ''
    os.environ['model_name'] = model_name
    os.environ['save_path'] = save_path if save_path else ''
    os.environ['load_path'] = '' if load_path is None else load_path
    os.environ['plot'] = '1' if plot else ''
    start()


if __name__ == "__main__":
    cli()

