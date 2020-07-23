import operator
import time
import unittest

import fungraph
from tests.utils import timeonce


def _slow_func(*args, seconds=1):
    time.sleep(seconds)
    return args

class TestFunctionNodeWithAlternativeCache(unittest.TestCase):

    def test_cache_compute_dict(self):
        f = fungraph.fun(operator.add, 1, 2)
        cache = dict()
        f.cachedcompute(cache=cache)
        self.assertEqual(list(cache.values())[0], 3)

    def test_cache_compute_dict_speed(self):
        f = fungraph.fun(_slow_func, 1, 2)
        cache = dict()
        t1 = timeonce(lambda : f.cachedcompute(cache=cache))
        t2 = timeonce(lambda: f.cachedcompute(cache=cache))
        self.assertGreater(t1, 0.5)
        self.assertLess(t2, 0.5)


    def test_cache_compute_none(self):
        f = fungraph.fun(_slow_func, 1, 2)
        t1 = timeonce(lambda : f.cachedcompute(cache=None))
        t2 = timeonce(lambda : f.cachedcompute(cache=None))
        self.assertAlmostEqual(t1, t2, delta=0.1)