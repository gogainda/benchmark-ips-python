"""Standard deviation statistics implementation."""

from .stats_metric import StatsMetric
from .. import timing


class SD(StatsMetric):
    """Standard deviation statistics."""

    def __init__(self, samples):
        """
        Initialize SD statistics.

        Args:
            samples: List of sample values
        """
        self.samples = samples
        self._mean = timing.mean(samples)
        self.error = round(timing.stddev(samples, self._mean))

    @property
    def central_tendency(self):
        """
        Average stat value.

        Returns:
            float: Central tendency (mean)
        """
        return self._mean

    def slowdown(self, baseline):
        """
        Determines how much slower this stat is than the baseline stat.

        Args:
            baseline: Faster baseline stats

        Returns:
            tuple: (slowdown_factor, error) where error is None for SD
        """
        if baseline.central_tendency > self.central_tendency:
            return (baseline.central_tendency / self.central_tendency, None)
        else:
            return (self.central_tendency / baseline.central_tendency, None)

    def speedup(self, baseline):
        """
        Determines how much faster this stat is than the baseline stat.

        Args:
            baseline: Baseline stats

        Returns:
            tuple: (speedup_factor, error) where error is None for SD
        """
        return baseline.slowdown(self)

    def footer(self):
        """
        Return footer text for stats display.

        Returns:
            None: SD stats don't have a footer
        """
        return None
