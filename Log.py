from enum import Enum

class LogLevel(Enum):
    WARNING = 0
    ERROR = 1
    FATAL_ERROR = 2

def log(message: str, log_level: LogLevel) -> None:
    print(f"{log_level.name}: {message}")