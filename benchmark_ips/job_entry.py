"""Entry class for benchmark jobs."""

import inspect


class JobEntry:
    """Entries in Benchmark Jobs."""

    def __init__(self, label, action):
        """
        Initialize the Job Entry.

        Args:
            label: Label of benchmarked code
            action: Code to be benchmarked (callable or string)

        Raises:
            ValueError: If action is not callable or string
        """
        self.label = label
        self._action = action

        # Determine the call strategy based on the action type
        if isinstance(action, str):
            # String action: compile and execute as code
            self._call_times = self._make_string_caller(action)
        elif callable(action):
            # Check if the callable accepts an argument (manual loop)
            sig = inspect.signature(action)
            if len(sig.parameters) > 0:
                # Manual loop: action handles the iteration count
                self._call_times = lambda times: action(times)
            else:
                # Automatic loop: we handle the iterations
                self._call_times = self._make_block_caller(action)
        else:
            raise ValueError("invalid action, must be callable or string")

    @property
    def action(self):
        """
        The benchmarking action.

        Returns:
            Action to be called (callable or string)
        """
        return self._action

    def call_times(self, times):
        """
        Call action by given times.

        Args:
            times: Times to call the action

        Returns:
            int: Number of times the action has been called
        """
        return self._call_times(times)

    def _make_block_caller(self, action):
        """
        Create a caller that loops automatically.

        Args:
            action: Callable action

        Returns:
            function: Caller function
        """
        def caller(times):
            i = 0
            while i < times:
                action()
                i += 1
        return caller

    def _make_string_caller(self, code_str):
        """
        Create a caller for string-based code.

        Args:
            code_str: String of code to execute

        Returns:
            function: Caller function
        """
        # Compile the code string
        compiled = compile(code_str, '<benchmark>', 'exec')

        def caller(times):
            i = 0
            while i < times:
                exec(compiled)
                i += 1
        return caller
