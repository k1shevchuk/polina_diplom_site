from dataclasses import dataclass
from typing import Any


@dataclass
class AppError:
    code: str
    message: str
    details: dict[str, Any] | None = None
