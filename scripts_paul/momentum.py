import pandas as pd


class MOM:
    """
    Momentum cryptocurrency factor as discussed
    in Y. Liu, A. Tsyvinski, Xi Wu, "Common Risk
    Factors in Cryptocurrency", pp. 20-21, see
    https://dx.doi.org/10.2139/ssrn.3379131
    """
    def __init__(self, **kwargs):

        # example
        self.a = kwargs.get('a', 0)
        assert isinstance(self.a, int)



