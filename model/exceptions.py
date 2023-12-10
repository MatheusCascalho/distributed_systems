class MotorNotFoundError(Exception):
    def __init__(self, motor: str):
        self.message = f"{motor} not found"
        super().__init__(self.message)
