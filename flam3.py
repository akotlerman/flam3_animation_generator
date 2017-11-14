from utils import mat_to_color, point_to_image_mat
from fractal import Fractal
import matplotlib.pyplot as plt
import click
from collections import Iterable


@click.group()
def cli():
    pass


def validate_selection_limiter(ctx, param, value):
    try:
        if value is not None:
            point_count = ctx.params['point_count']
            values = [int(v) for v in value.split(',') if v]
            assert (len(values) == point_count)
            return values
    except:
        msg = 'For {} points, selection limiter has to be in the form {}.'.format(point_count,
                                                                                  ','.join(['0'] * point_count))
        raise click.BadParameter(msg)


@click.command()
@click.option('--point-count', '-p', default=3, type=click.IntRange(3, 10),
              help='Number of vertices to use to make a circle. Value in range (3,10) inclusive.')
@click.option('--selection-limiter', '-l', default=None, callback=validate_selection_limiter,
              help='Limits the choices we can make compared to last choice')
@click.option('--scaling-factor', '-s', default=2, type=click.FLOAT,
              help='Scales the point generator function.')
# TODO: How to make run-count scaling with point-count and selection-limiter?
@click.option('--run-count', '-r', default=50000, type=click.IntRange(1000, 1000000),
              help='Number of loop to run')
@click.option('--dry-fire', '-d', default=1000, type=click.IntRange(0, 10000),
              help='Number of non-interactive runs to establish flam3 algorithm. Value in range (0, 10000).')
def gen_fractal(run_count, dry_fire, point_count, scaling_factor, selection_limiter):
    mat_points = Fractal(run_count=run_count, dry_fire=dry_fire, point_count=point_count,
                         scaling_factor=scaling_factor, selection_limiter=selection_limiter).execute()
    fig, ax = plt.subplots()
    h = ax.imshow(mat_to_color(point_to_image_mat(mat_points)))
    """
    mat_points1 = Fractal(point_count=6, selection_limiter=[False, True, False, False, False, False]).execute()
    mat_points2 = Fractal(point_count=6, selection_limiter=[False, False, False, False, False, True]).execute()
    fig, ax = plt.subplots(2)
    h = ax[0].imshow(mat_to_color(point_to_image_mat(mat_points1)))
    h = ax[1].imshow(mat_to_color(point_to_image_mat(mat_points2)))
    """
    plt.show()


def validate_file_type(ctx, param, value):
    if value.lower() in ('gif', 'mp4'):
        return value.lower()

    raise click.BadParameter('{} is not a valid file type. Must be {} or {}.'.format(value, 'gif', 'mp4'))


@click.command()
@click.option('--file-name', '-f', default='output.gif', type=click.Path(exists=False),
              help='Output file name')
@click.option('--file-type', '-t', default='gif', type=click.Path(exists=False), callback=validate_file_type,
              help='Output file type')
@click.option('--point-count', '-p', default=3, type=click.IntRange(3, 10),
              help='Number of vertices to use to make a circle. Value in range (3,10) inclusive.')
@click.option('--selection-limiter', '-l', default=None, callback=validate_selection_limiter,
              help='Limits the choices we can make compared to last choice.')
@click.option('--scaling-factor', '-s', default=(2., 3.), type=(float, float),
              help='Scales the point generator function between two float values.')
# TODO: How to make run-count scaling with point-count and selection-limiter?
@click.option('--run-count', '-r', default=(50000, 50000),
              type=click.Tuple([click.IntRange(1000, 1000000), click.IntRange(1000, 1000000)]),
              help='Number of loops to run: initial and final integers between 1000 and 1000000')
@click.option('--dry-fire', '-d', default=1000, type=click.IntRange(0, 10000),
              help='Number of non-interactive runs to establish flam3 algorithm. Value in range (0, 10000).')
def gen_animation(file_name, file_type, run_count, dry_fire, point_count, scaling_factor, selection_limiter):
    # Current iterables are scaling-factor and run-count


    return Fractal


cli.add_command(gen_fractal, 'fractal')
cli.add_command(gen_animation, 'animation')

if __name__ == '__main__':
    cli()
