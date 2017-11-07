from moviepy.editor import VideoClip
from copy import deepcopy
from ValidatingObject import ValidatingObject
from fractal import Fractal
from utils import mat_to_color, point_to_image_mat


class FractalAnimator(ValidatingObject):
    """
    This class handles animating objects using the Fractal class.
    When generating movies, this class will be responsible for generating the correct number
    of frames.

    To Use this class call "generate_movie" with the correct params in kwargs
    reflected in the "Fractal" class. Any parameter (except selection_limiter) that normally
    has one value should have a start and end value.
    For example:
        params = {'run_count': (50000, 20000), 'dry_fire': 1000, 'point_count': 5,
              'scaling_factor': (2, 4),
              'selection_limiter': [True, False, False, False, False]}
        animator.generate_movie('my_movie.gif', 'gif', **params)

        In this example "run_count" is varied from 50000 to 20000
        and "scaling_factor" is varied from 2 to 4
    """
    # TODO: Currently the parameters are varied linearly. Offer option to change them along a custom curve
    PARAMS = {'fps': 24, 'resolution': (500, 500), 'duration': 3}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dict__.update(self.__class__.PARAMS)
        self.validate()

    def __generate_movie(self, fractal_params):
        """
        Inner class to generate movie quickly. Users should not run this.
        This class calls the required function to generate a fractal
        :param fractal_params: Initial params for Fractal class
        :return: Generator of matrices to be produced frame-by-frame
        """
        # Separate Fractal class params here
        params = deepcopy(fractal_params)
        while True:

            fractal = Fractal(**params)
            yield fractal

    def generate_movie(self, file_name, file_type, **kwargs):
        """

        :param file_name:
        :param file_type: Either "gif" or "mp4"
        :param kwargs: Varying params for Fractal class
        :return: None
        """
        gen_movie = self.__generate_movie()

        def make_frame(t):
            """ returns a numpy array of the frame at time t """
            mat_points = next(gen_movie)
            return mat_to_color(point_to_image_mat(mat_points))

        clip = VideoClip(make_frame, duration=self.duration)  # 3-second clip
        # clip.write_videofile("my_animation.mp4", fps=24) # export as video
        clip.write_gif(file_name, fps=self.fps)  # export as GIF

    def validate(self):
        pass
