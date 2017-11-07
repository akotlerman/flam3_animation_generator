"""
ValidatingObject is a simple class that takes in the PARAMS dict from another inheriting class
and makes sure the parameters sent are valid. Any parameters not in the PARAMS list simply throws
an exception.

"""


class ValidatingObject:
    PARAMS = None

    def __init__(self, **kwargs):
        invalid_params = []
        if self.__class__.PARAMS is not None:
            for k, v in kwargs.items():
                if k in self.__class__.PARAMS:
                    self.__dict__[k] = v
                else:
                    invalid_params.append((k, v))

            if invalid_params:
                raise Exception('The following params are invalid: {}'.format(invalid_params))
