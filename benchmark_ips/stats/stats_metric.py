"""Base statistics metric interface."""


class StatsMetric:
    """Base class for statistics metrics."""

    def error_percentage(self):
        """
        Return standard deviation of iteration per second in percentage.

        Returns:
            float: Error in percentage
        """
        return 100.0 * (self.error / self.central_tendency)

    def overlaps(self, baseline):
        """
        Check if this stat overlaps with baseline within error margins.

        Args:
            baseline: Baseline stats to compare against

        Returns:
            bool: True if overlaps within error
        """
        baseline_low = baseline.central_tendency - baseline.error
        baseline_high = baseline.central_tendency + baseline.error
        my_high = self.central_tendency + self.error
        my_low = self.central_tendency - self.error
        return my_high > baseline_low and my_low < baseline_high
