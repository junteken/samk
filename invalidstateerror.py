class InvalidStateError(RuntimeError):
    def __init__(self, current_state, expected_state):
        self.current_state = current_state
        self.expected_state = expected_state
        message = f"Expected state '{expected_state}', but got '{current_state}'"
        super().__init__(message)