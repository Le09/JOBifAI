
class Unauthorized(Exception):
    def __init__(self, service_name, message):
        self.service_name = service_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.service_name}] {self.message}"


class RetryableError(Exception):
    pass
