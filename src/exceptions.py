from typing import Any


# Implement model exceptions for the detailed error stracktrace
class AppBaseException(Exception):
    ERROR_CODE: str = 'UNKNOWN_ERROR'
    STATUS_CODE: int = 500

    def __init__(self, error_message: str):
        super().__init__()
        self.error_message = error_message

    def dump(self) -> dict[str, Any]:
        return {
            'error': self.error_message,
            'error_code': self.ERROR_CODE,
            'error_details': self.dump_error_details(),
        }

    def dump_error_details(self) -> dict[str, Any]:
        return {}


class AppInvalidInputException(AppBaseException):
    ERROR_CODE = 'INVALID_INPUT'
    STATUS_CODE = 400

    def __init__(self, error_message: str, field_name: str | None = None):
        super().__init__(error_message)
        self.field_name = field_name

    def dump_error_details(self) -> dict[str, Any]:
        return {'field_name': self.field_name} if self.field_name else {}
