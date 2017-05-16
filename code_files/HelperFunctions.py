import itertools

# HelperFunctions
class HelperFunctions:

    def __init__(self):
        pass

    @staticmethod
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)
